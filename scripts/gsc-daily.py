#!/usr/bin/env python3
"""
GSC 每日分析：拉数据 -> 与前一周期对比 -> 输出可供分析的结构化摘要。

设计原则：
  1. 所有对比窗口的锚点 = 「最后完整日」，绝不使用未定稿日期。
  2. 日环比 = 最后完整日 vs 前一日
     周环比 = 最后完整日往前 7 天 vs 再往前 7 天
  3. 只输出事实与差值，不做主观判断（判断交给下游分析环节）。

站点与数据目录来自 .gsc-config.json / 环境变量 / 命令行，不写死。

用法：
  python scripts/gsc-daily.py                # 输出摘要到 stdout
  python scripts/gsc-daily.py --md           # 另存 <dataDir>/daily-<anchor>.md
  python scripts/gsc-daily.py --json         # 额外输出机器可读 JSON 到 stdout 末尾
"""

import argparse
import importlib.util
import json
import os
import sys
from datetime import date, datetime, timedelta

DATA = SNAPS = ""


def _load_fetch():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsc-fetch.py")
    spec = importlib.util.spec_from_file_location("gsc_fetch", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gsc = _load_fetch()


def apply_config(root=None, site=None, data_dir=None):
    """解析项目配置并设置全局路径。必须在 main 开头调用一次。"""
    global DATA, SNAPS, SITE
    cfg = gsc.load_config(root)
    SITE = site or cfg["site"]
    DATA = data_dir or cfg["dataDir"]
    SNAPS = os.path.join(DATA, "snapshots")
    return cfg


def delta(cur, prev):
    if prev in (0, None):
        return None
    return (cur - prev) / prev


def fmt_delta(cur, prev):
    """基数过小时百分比会失真（如 5->4318 显示 +86260%），改为直接标注基数。"""
    if prev in (0, None):
        return "新增（前期无数据）"
    if prev < 30:
        return f"{prev} → {cur}（基数过小，百分比无意义）"
    return f"{(cur - prev) / prev * 100:+.1f}%"


def short(url):
    return gsc.short(url)


def index_by(rows, keyfn=lambda r: r["keys"][0]):
    out = {}
    for r in rows:
        out[keyfn(r)] = r
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", help="项目根目录")
    ap.add_argument("--site", help="GSC 资源，如 sc-domain:example.com")
    ap.add_argument("--key", help="服务账号 JSON 路径")
    ap.add_argument("--data-dir", help="数据目录，默认 <root>/.workbuddy/gsc-data")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", action="store_true", help="把摘要写入 <dataDir>/daily-<anchor>.md")
    ap.add_argument("--days", type=int, default=30)
    args = ap.parse_args()

    cfg = apply_config(args.root, args.site, args.data_dir)
    creds = gsc.build_credentials(args.key or cfg["key"])
    site = gsc.resolve_site(creds, SITE)
    os.makedirs(SNAPS, exist_ok=True)

    # ---------- 1. 按天数据，确定锚点 ----------
    end = gsc.gsc_today().isoformat()
    start = (gsc.gsc_today() - timedelta(days=args.days - 1)).isoformat()
    drows, _ = gsc.query(creds, site, ["date"], start, end, 25000, "final", "web")
    drows = sorted(drows, key=lambda r: r["keys"][0])

    if len(drows) < 2:
        sys.exit(f"[FAIL] 按天数据仅 {len(drows)} 天，连日环比都做不了。请检查 API 或权限。")
    # 新站 / 刚接入 GSC 的属性历史不足 9 天时，7 日窗口不完整。
    # 不阻断：降级为「逐日 + 可用窗口」，并在摘要显式标注，避免 automation 连续几天全红。
    short_history = len(drows) < 9

    anchor = drows[-1]["keys"][0]
    a = date.fromisoformat(anchor)

    d_cur = drows[-1]
    d_prev = drows[-2]

    # 周窗口
    w1_lo, w1_hi = (a - timedelta(days=6)), a
    w0_lo, w0_hi = (a - timedelta(days=13)), (a - timedelta(days=7))

    def in_win(d, lo, hi):
        return lo.isoformat() <= d <= hi.isoformat()

    w1 = [r for r in drows if in_win(r["keys"][0], w1_lo, w1_hi)]
    w0 = [r for r in drows if in_win(r["keys"][0], w0_lo, w0_hi)]

    def agg(rows):
        c = sum(r["clicks"] for r in rows)
        i = sum(r["impressions"] for r in rows)
        p = sum(r["position"] * r["impressions"] for r in rows) / i if i else 0
        return {"clicks": c, "impressions": i, "ctr": c / i if i else 0, "position": p}

    w1a, w0a = agg(w1), agg(w0)

    # ---------- 2. 页面维度两个窗口 ----------
    p1, _ = gsc.query(creds, site, ["page"], w1_lo.isoformat(), w1_hi.isoformat(), 25000, "final", "web")
    p0, _ = gsc.query(creds, site, ["page"], w0_lo.isoformat(), w0_hi.isoformat(), 25000, "final", "web")
    p1i, p0i = index_by(p1), index_by(p0)

    # ---------- 3. 查询词两个窗口 ----------
    q1, _ = gsc.query(creds, site, ["query"], w1_lo.isoformat(), w1_hi.isoformat(), 25000, "final", "web")
    q0, _ = gsc.query(creds, site, ["query"], w0_lo.isoformat(), w0_hi.isoformat(), 25000, "final", "web")
    q1i, q0i = index_by(q1), index_by(q0)

    new_queries = sorted(
        [r for k, r in q1i.items() if k not in q0i and r["impressions"] >= 3],
        key=lambda r: (-r["impressions"], -r["clicks"]),
    )
    rising_q = sorted(
        [
            r
            for k, r in q1i.items()
            if k in q0i and r["impressions"] > q0i[k]["impressions"]
        ],
        key=lambda r: -(r["impressions"] - q0i[r["keys"][0]]["impressions"]),
    )
    falling_q = sorted(
        [
            r
            for k, r in q0i.items()
            if (k not in q1i or q1i[k]["impressions"] < r["impressions"] * 0.7)
            and r["impressions"] >= 10
        ],
        key=lambda r: -r["impressions"],
    )

    # ---------- 4. 页面环比 ----------
    page_changes = []
    for k in set(p1i) | set(p0i):
        cur = p1i.get(k, {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0})
        old = p0i.get(k, {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0})
        page_changes.append(
            {
                "page": short(k),
                "clicks": cur["clicks"],
                "clicks_prev": old["clicks"],
                "impr": cur["impressions"],
                "impr_prev": old["impressions"],
                "pos": cur["position"],
                "pos_prev": old["position"],
                "d_clicks": cur["clicks"] - old["clicks"],
                "d_impr": cur["impressions"] - old["impressions"],
            }
        )
    page_up = sorted(page_changes, key=lambda x: -x["d_impr"])[:6]
    page_down = sorted(page_changes, key=lambda x: x["d_impr"])[:6]

    # ---------- 5. 机会池（基于本周页面数据） ----------
    opp_striking = [  # 排名 8-20、有曝光 → 差一点上首页
        {"page": short(r["keys"][0]), "impr": r["impressions"], "pos": r["position"], "ctr": r["ctr"]}
        for r in p1
        if 8 <= r["position"] <= 20 and r["impressions"] >= 30
    ]
    opp_striking.sort(key=lambda x: (x["pos"], -x["impr"]))

    opp_ctr = [  # 排名靠前但 CTR 低 → 标题/描述优化空间
        {"page": short(r["keys"][0]), "impr": r["impressions"], "pos": r["position"], "ctr": r["ctr"]}
        for r in p1
        if r["position"] <= 10 and r["impressions"] >= 80 and r["ctr"] < 0.02
    ]
    opp_ctr.sort(key=lambda x: -x["impr"])

    opp_query = [  # 词排在 11-20 且有曝光
        {"q": r["keys"][0], "impr": r["impressions"], "pos": r["position"], "clicks": r["clicks"]}
        for r in q1
        if 11 <= r["position"] <= 20 and r["impressions"] >= 5
    ]
    opp_query.sort(key=lambda x: -x["impr"])

    # ---------- 6. 快照 ----------
    snap = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "site": site,
        "anchor": anchor,
        "coverage": {
            "days": len(drows),
            "first": drows[0]["keys"][0],
            "last": drows[-1]["keys"][0],
            "shortHistory": short_history,
        },
        "latestCompleteDay": {
            "date": d_cur["keys"][0],
            "clicks": d_cur["clicks"],
            "impressions": d_cur["impressions"],
            "ctr": d_cur["ctr"],
            "position": d_cur["position"],
            "dod_clicks": delta(d_cur["clicks"], d_prev["clicks"]),
            "dod_impr": delta(d_cur["impressions"], d_prev["impressions"]),
        },
        "week1": {"window": [w1_lo.isoformat(), w1_hi.isoformat()], **w1a},
        "week0": {"window": [w0_lo.isoformat(), w0_hi.isoformat()], **w0a},
        "wow": {
            "clicks": delta(w1a["clicks"], w0a["clicks"]),
            "impressions": delta(w1a["impressions"], w0a["impressions"]),
            "ctr": delta(w1a["ctr"], w0a["ctr"]),
        },
        "page_up": page_up,
        "page_down": page_down,
        "new_queries": new_queries[:10],
        "rising_queries": [
            {"q": r["keys"][0], "impr": r["impressions"], "impr_prev": q0i[r["keys"][0]]["impressions"],
             "clicks": r["clicks"], "pos": r["position"]}
            for r in rising_q[:10]
        ],
        "falling_queries": [
            {"q": r["keys"][0], "impr": r["impressions"], "clicks": r["clicks"], "pos": r["position"]}
            for r in falling_q[:10]
        ],
        "opportunities": {
            "striking_distance": opp_striking[:8],
            "low_ctr": opp_ctr[:8],
            "query_striking": opp_query[:10],
        },
    }

    snap_path = os.path.join(SNAPS, f"{anchor}.json")
    with open(snap_path, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, ensure_ascii=False, indent=2)

    # ---------- 7. 摘要 ----------
    L = []
    L.append(f"# GSC 每日摘要 · {site} · 数据截止 {anchor}（太平洋时间）")
    L.append("")
    L.append(f"生成时间 {snap['generatedAt']}　锚点=最后完整日　拉取区间 {start} ~ {end}")
    L.append("")
    L.append("## 1. 最新完整日")
    L.append(f"- {d_cur['keys'][0]}：点击 {d_cur['clicks']}　曝光 {d_cur['impressions']:,}　"
             f"CTR {d_cur['ctr']*100:.2f}%　均排 {d_cur['position']:.1f}")
    L.append(f"- 日环比：点击 {fmt_delta(d_cur['clicks'], d_prev['clicks'])}　"
             f"曝光 {fmt_delta(d_cur['impressions'], d_prev['impressions'])}"
             f"（前一日 {d_prev['clicks']} 点击 / {d_prev['impressions']:,} 曝光）")
    L.append("")
    L.append("## 2. 周环比（7 日 vs 前 7 日）")
    L.append(f"- 本周 {w1_lo}~{w1_hi}：点击 {w1a['clicks']}　曝光 {w1a['impressions']:,}　"
             f"CTR {w1a['ctr']*100:.2f}%　均排 {w1a['position']:.1f}")
    L.append(f"- 上周 {w0_lo}~{w0_hi}：点击 {w0a['clicks']}　曝光 {w0a['impressions']:,}　"
             f"CTR {w0a['ctr']*100:.2f}%　均排 {w0a['position']:.1f}")
    L.append(f"- 变化：点击 {fmt_delta(w1a['clicks'], w0a['clicks'])}　"
             f"曝光 {fmt_delta(w1a['impressions'], w0a['impressions'])}　"
             f"CTR {fmt_delta(round(w1a['ctr']*1000), round(w0a['ctr']*1000))}")
    if w0a["impressions"] < 100:
        L.append(f"- ⚠️ 上周曝光仅 {w0a['impressions']}，周环比百分比不可作为趋势判断，只能看绝对增量。")
    if short_history:
        L.append(f"- ⚠️ 历史仅 {len(drows)} 天（首日 {drows[0]['keys'][0]}），7 日窗口不完整：本周窗口只覆盖 "
                 f"{min(w1, key=lambda r: r['keys'][0])['keys'][0] if w1 else '无'} 起，上周窗口基本为空。"
                 "周环比只能当「有 / 无」看，不能算趋势。")
    L.append("")
    L.append("## 3. 页面曝光变化")
    L.append("上升：")
    for x in page_up:
        if x["d_impr"] <= 0:
            continue
        L.append(f"- {x['page']}　曝光 {x['impr_prev']} → {x['impr']}（{x['d_impr']:+d}）　"
                 f"点击 {x['clicks_prev']} → {x['clicks']}　均排 {x['pos']:.1f}")
    L.append("下降：")
    for x in page_down:
        if x["d_impr"] >= 0:
            continue
        L.append(f"- {x['page']}　曝光 {x['impr_prev']} → {x['impr']}（{x['d_impr']:+d}）　"
                 f"点击 {x['clicks_prev']} → {x['clicks']}　均排 {x['pos']:.1f}")
    L.append("")
    L.append(f"## 4. 查询词（本周 {len(q1)} 个 / 上周 {len(q0)} 个）")
    L.append("新出现（上周无、本周曝光≥3）：")
    for r in new_queries[:8]:
        L.append(f"- {r['keys'][0]}　曝光 {r['impressions']}　点击 {r['clicks']}　均排 {r['position']:.1f}")
    L.append("上升最快：")
    for x in snap["rising_queries"][:8]:
        L.append(f"- {x['q']}　曝光 {x['impr_prev']} → {x['impr']}　点击 {x['clicks']}　均排 {x['pos']:.1f}")
    L.append("明显回落：")
    for x in snap["falling_queries"][:8]:
        L.append(f"- {x['q']}　上周曝光 {x['impr']} → 本周消失或大降　点击 {x['clicks']}　均排 {x['pos']:.1f}")
    L.append("")
    L.append("## 5. 机会池")
    L.append("差一点进首页（排名 8-20，曝光≥30）：")
    for x in opp_striking[:6]:
        L.append(f"- {x['page']}　曝光 {x['impr']}　均排 {x['pos']:.1f}　CTR {x['ctr']*100:.1f}%")
    L.append("排名靠前但 CTR 低（排名≤10，曝光≥80，CTR<2%）：")
    for x in opp_ctr[:6]:
        L.append(f"- {x['page']}　曝光 {x['impr']}　均排 {x['pos']:.1f}　CTR {x['ctr']*100:.1f}%")
    L.append("词排 11-20（曝光≥5）：")
    for x in opp_query[:8]:
        L.append(f"- {x['q']}　曝光 {x['impr']}　均排 {x['pos']:.1f}　点击 {x['clicks']}")
    if not (opp_striking or opp_ctr or opp_query):
        L.append(f"- 三类机会池全空（本周曝光 {w1a['impressions']:,}）。阈值（曝光≥30 / ≥80 / ≥5）"
                 "在低基数下不适用：当前瓶颈是「有多少页已被收录并拿到曝光」，不是标题文案。")

    L.append("")
    L.append("## 6. 近 14 天逐日（看趋势，勿只看单日）")
    L.append("| 日期 | 点击 | 曝光 | CTR | 均排 |")
    L.append("|---|---|---|---|---|")
    for r in drows[-14:]:
        L.append(f"| {r['keys'][0]} | {r['clicks']} | {r['impressions']:,} | "
                 f"{r['ctr']*100:.2f}% | {r['position']:.1f} |")

    out = "\n".join(L)
    print(out)
    print(f"\n[snapshot] {snap_path}")

    if args.md:
        os.makedirs(DATA, exist_ok=True)
        md_path = os.path.join(DATA, f"daily-{anchor}.md")
        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
        print(f"\n[markdown] {md_path}")
        print(f"[data-dir] {DATA}")

    if args.json:
        print("\n---JSON---")
        print(json.dumps(snap, ensure_ascii=False))


if __name__ == "__main__":
    main()
