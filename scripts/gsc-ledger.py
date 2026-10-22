#!/usr/bin/env python3
"""
GSC 台账：把每日数据增量并入 CSV，供后续校对与长周期趋势分析。

三个台账（都在 <dataDir>/ledger/）：
  daily.csv   一行 = 一天（全站汇总）
  pages.csv   一行 = 一天 × 一个页面
  queries.csv 一行 = 一天 × 一个查询词

设计要点：
  - 幂等：同一日期重复跑不会产生重复行，窗口内以最新拉取为准（GSC 定稿后仍会微调）
  - 窗口外历史数据一律保留，不做全量重写
  - 每次重写前留 .bak，防止误操作毁掉台账

用法：
  python scripts/gsc-ledger.py                 # 增量并入最近 3 天（日常用这个）
  python scripts/gsc-ledger.py --days 30       # 回填最近 30 天
  python scripts/gsc-ledger.py --audit         # 只检查台账完整性，不联网
  python scripts/gsc-ledger.py --trend "page:/pricing/"
"""

import argparse
import csv
import importlib.util
import os
import shutil
import sys
from datetime import date, datetime, timedelta

LEDGER = ""
SITE = None

DAILY_COLS = ["date", "clicks", "impressions", "ctr", "position", "pages", "queries", "updated_at"]
PAGE_COLS = ["date", "page", "clicks", "impressions", "ctr", "position"]
QUERY_COLS = ["date", "query", "clicks", "impressions", "ctr", "position"]


def _load_fetch():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsc-fetch.py")
    spec = importlib.util.spec_from_file_location("gsc_fetch", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gsc = _load_fetch()


def apply_config(root=None, site=None, data_dir=None):
    global LEDGER, SITE
    cfg = gsc.load_config(root)
    SITE = site or cfg["site"]
    LEDGER = os.path.join(data_dir or cfg["dataDir"], "ledger")
    return cfg


def path_of(name):
    return os.path.join(LEDGER, f"{name}.csv")


def read_rows(name, cols):
    p = path_of(name)
    if not os.path.isfile(p):
        return []
    with open(p, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return []
        return [{c: r.get(c, "") for c in cols} for r in reader]


def write_rows(name, cols, rows):
    os.makedirs(LEDGER, exist_ok=True)
    p = path_of(name)
    if os.path.isfile(p):
        shutil.copy2(p, p + ".bak")
    tmp = p + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    os.replace(tmp, p)


def merge(existing, fresh, key_cols, window_start):
    """窗口内以新数据为准，窗口外保留旧数据。"""
    kept = [r for r in existing if r[key_cols[0]] < window_start]
    out = kept + fresh
    out.sort(key=lambda r: tuple([r[k] for k in key_cols]))
    return out


def rnd(v, n=4):
    return f"{v:.{n}f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", help="项目根目录")
    ap.add_argument("--site", help="GSC 资源，如 sc-domain:example.com")
    ap.add_argument("--key", help="服务账号 JSON 路径")
    ap.add_argument("--data-dir", help="数据目录，默认 <root>/.workbuddy/gsc-data")
    ap.add_argument("--days", type=int, default=3, help="增量窗口天数（默认 3，覆盖 GSC 回填延迟）")
    ap.add_argument("--audit", action="store_true", help="只做台账完整性检查，不联网")
    ap.add_argument("--trend", help="查单个对象的历史走势，如 --trend page:/pricing/ 或 --trend \"query:brand name\"")
    args = ap.parse_args()

    cfg = apply_config(args.root, args.site, args.data_dir)

    if args.audit:
        audit()
        return

    if args.trend:
        trend(args.trend)
        return

    creds = gsc.build_credentials(args.key or cfg["key"])
    site = gsc.resolve_site(creds, SITE)
    today = gsc.gsc_today()
    end = today.isoformat()
    start = (today - timedelta(days=args.days - 1)).isoformat()
    now = datetime.now().isoformat(timespec="seconds")

    print(f"[fetch] {site}　窗口 {start} ~ {end}（太平洋时间）")

    # ---- 按天 ----
    drows, _ = gsc.query(creds, site, ["date"], start, end, 25000, "final", "web")

    # ---- 按天 × 页面 ----
    prow, _ = gsc.query(creds, site, ["date", "page"], start, end, 25000, "final", "web")

    # ---- 按天 × 查询词 ----
    qrow, _ = gsc.query(creds, site, ["date", "query"], start, end, 25000, "final", "web")

    pages_per_day = {}
    for r in prow:
        d = r["keys"][0]
        pages_per_day[d] = pages_per_day.get(d, 0) + 1
    queries_per_day = {}
    for r in qrow:
        d = r["keys"][0]
        queries_per_day[d] = queries_per_day.get(d, 0) + 1

    # ---- 合并 daily ----
    new_daily = [
        {
            "date": r["keys"][0],
            "clicks": r["clicks"],
            "impressions": r["impressions"],
            "ctr": rnd(r["ctr"]),
            "position": rnd(r["position"], 2),
            "pages": pages_per_day.get(r["keys"][0], 0),
            "queries": queries_per_day.get(r["keys"][0], 0),
            "updated_at": now,
        }
        for r in drows
    ]
    old_daily = read_rows("daily", DAILY_COLS)
    merged_daily = merge(old_daily, new_daily, ["date"], start)
    write_rows("daily", DAILY_COLS, merged_daily)

    # ---- 合并 pages ----
    new_pages = [
        {
            "date": r["keys"][0],
            "page": r["keys"][1],
            "clicks": r["clicks"],
            "impressions": r["impressions"],
            "ctr": rnd(r["ctr"]),
            "position": rnd(r["position"], 2),
        }
        for r in prow
    ]
    old_pages = read_rows("pages", PAGE_COLS)
    merged_pages = merge(old_pages, new_pages, ["date", "page"], start)
    write_rows("pages", PAGE_COLS, merged_pages)

    # ---- 合并 queries ----
    new_queries = [
        {
            "date": r["keys"][0],
            "query": r["keys"][1],
            "clicks": r["clicks"],
            "impressions": r["impressions"],
            "ctr": rnd(r["ctr"]),
            "position": rnd(r["position"], 2),
        }
        for r in qrow
    ]
    old_queries = read_rows("queries", QUERY_COLS)
    merged_queries = merge(old_queries, new_queries, ["date", "query"], start)
    write_rows("queries", QUERY_COLS, merged_queries)

    print(f"[daily]   窗口内 {len(new_daily)} 天 → 台账共 {len(merged_daily)} 天")
    print(f"[pages]   窗口内 {len(new_pages)} 行 → 台账共 {len(merged_pages)} 行")
    print(f"[queries] 窗口内 {len(new_queries)} 行 → 台账共 {len(merged_queries)} 行")
    if merged_daily:
        print(f"[覆盖]    {merged_daily[0]['date']} ~ {merged_daily[-1]['date']}")
    print(f"[ledger]  {LEDGER}")

    audit(quiet=True)


def trend(target):
    """查单个页面或查询词的历史走势。"""
    if ":" not in target:
        sys.exit('格式：--trend "page:/pricing/"  或  --trend "query:brand name"')
    kind, key = target.split(":", 1)
    kind, key = kind.strip().lower(), key.strip()

    if kind == "page":
        rows, col = read_rows("pages", PAGE_COLS), "page"
    elif kind == "query":
        rows, col = read_rows("queries", QUERY_COLS), "query"
    else:
        sys.exit("只支持 page: 或 query:")

    if not rows:
        sys.exit("台账为空，先跑一次 gsc-ledger.py 回填")

    exact = [r for r in rows if r[col].lower() == key.lower()]
    hits = exact or [r for r in rows if key.lower() in r[col].lower()]

    if not hits:
        sys.exit(f"台账里没有匹配的 {kind}：{key}")

    keys = sorted({r[col] for r in hits})
    if len(keys) > 1:
        print(f"匹配到 {len(keys)} 个对象，取曝光最高的一个。全部候选：")
        for k in keys:
            print("   ", k)
        print()
        best = max(
            keys,
            key=lambda k: sum(int(r["impressions"]) for r in hits if r[col] == k),
        )
    else:
        best = keys[0]

    sel = sorted([r for r in hits if r[col] == best], key=lambda r: r["date"])
    tot_c = sum(int(r["clicks"]) for r in sel)
    tot_i = sum(int(r["impressions"]) for r in sel)

    print(f"# {best}")
    print(f"记录 {len(sel)} 天　{sel[0]['date']} ~ {sel[-1]['date']}　"
          f"累计点击 {tot_c}　累计曝光 {tot_i}"
          + (f"　CTR {tot_c/tot_i*100:.2f}%" if tot_i else ""))
    print()
    print("| 日期 | 点击 | 曝光 | CTR | 均排 |")
    print("|---|---|---|---|---|")
    for r in sel:
        print(f"| {r['date']} | {r['clicks']} | {int(r['impressions']):,} | "
              f"{float(r['ctr'])*100:.2f}% | {float(r['position']):.1f} |")

    if len(sel) >= 2:
        first, last = sel[0], sel[-1]
        print()
        print(f"首日 {first['date']}：曝光 {first['impressions']}　均排 {float(first['position']):.1f}")
        print(f"末日 {last['date']}：曝光 {last['impressions']}　均排 {float(last['position']):.1f}")
        pi, li = int(first["impressions"]), int(last["impressions"])
        pp, lp = float(first["position"]), float(last["position"])
        if pi >= 30:
            print(f"曝光变化 {(li-pi)/pi*100:+.0f}%　排名{'前进' if lp < pp else '后退'} {abs(pp-lp):.1f} 位")
        else:
            print(f"曝光 {pi} → {li}（首日基数小，百分比不可用）")


def audit(quiet=False):
    """台账完整性检查：连续性、自洽性、异常跳变。"""
    daily = read_rows("daily", DAILY_COLS)
    pages = read_rows("pages", PAGE_COLS)
    queries = read_rows("queries", QUERY_COLS)

    if not daily:
        print("[audit] 台账为空，先跑一次 gsc-ledger.py")
        return

    daily.sort(key=lambda r: r["date"])
    problems = []

    # 1. 日期连续性
    d0 = date.fromisoformat(daily[0]["date"])
    d1 = date.fromisoformat(daily[-1]["date"])
    have = {r["date"] for r in daily}
    missing = []
    cur = d0
    while cur <= d1:
        if cur.isoformat() not in have:
            missing.append(cur.isoformat())
        cur += timedelta(days=1)

    # 2. 自洽性：页面点击加总 vs 全站点击
    click_by_day = {}
    impr_by_day = {}
    for r in pages:
        click_by_day[r["date"]] = click_by_day.get(r["date"], 0) + int(r["clicks"])
        impr_by_day[r["date"]] = impr_by_day.get(r["date"], 0) + int(r["impressions"])

    for r in daily:
        c = int(r["clicks"])
        i = int(r["impressions"])
        if c > i:
            problems.append(f"{r['date']}: 点击 {c} > 曝光 {i}（不可能）")
        pc = click_by_day.get(r["date"])
        if pc is not None and pc != c:
            diff = abs(pc - c)
            if diff > max(1, c * 0.02):
                problems.append(f"{r['date']}: 页面点击加总 {pc} ≠ 全站 {c}（差 {diff}）")

    # 3. 异常跳变（仅作提示，不下结论）
    jumps = []
    for prev, cur in zip(daily, daily[1:]):
        pi, ci = int(prev["impressions"]), int(cur["impressions"])
        if pi >= 50:
            ratio = (ci - pi) / pi
            if ratio > 3 or ratio < -0.7:
                jumps.append(f"{cur['date']}: 曝光 {pi} → {ci}（{ratio*100:+.0f}%）")

    print()
    print("=" * 58)
    print("台账完整性检查")
    print("=" * 58)
    print(f"ledger  {LEDGER}")
    print(f"daily   {len(daily):>4} 天  {daily[0]['date']} ~ {daily[-1]['date']}")
    print(f"pages   {len(pages):>4} 行  ({len({r['page'] for r in pages})} 个不同页面)")
    print(f"queries {len(queries):>4} 行  ({len({r['query'] for r in queries})} 个不同查询词)")
    tot_c = sum(int(r["clicks"]) for r in daily)
    tot_i = sum(int(r["impressions"]) for r in daily)
    if tot_i:
        print(f"累计    点击 {tot_c:,} / 曝光 {tot_i:,} / CTR {tot_c/tot_i*100:.2f}%")
    print()
    if missing:
        print(f"[缺口] 缺失 {len(missing)} 天：{', '.join(missing[:10])}")
        print("       用 --days N 回填，N 覆盖到最早缺口日期。")
    else:
        print("[缺口] 无，日期连续")
    if problems:
        print(f"[自洽] 发现 {len(problems)} 处异常：")
        for p in problems[:10]:
            print(f"       - {p}")
    else:
        print("[自洽] 通过：页面点击加总 = 全站点击")
    if jumps:
        print(f"[跳变] {len(jumps)} 处（提示用，未必是异常）：")
        for j in jumps[:8]:
            print(f"       - {j}")
    else:
        print("[跳变] 无")

    # 最近 7 天速览
    tail = daily[-7:]
    if len(tail) >= 2:
        print()
        print("最近记录：")
        for r in tail:
            print(f"  {r['date']}  点击 {int(r['clicks']):>4}  曝光 {int(r['impressions']):>6}  "
                  f"CTR {float(r['ctr'])*100:>5.2f}%  均排 {float(r['position']):>5.1f}  "
                  f"页 {r['pages']:>3}  词 {r['queries']:>4}")


if __name__ == "__main__":
    main()
