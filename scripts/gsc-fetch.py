#!/usr/bin/env python3
"""
Google Search Console - Search Analytics 取数脚本（服务账号认证）

站点与路径不再写死，按以下优先级解析：
  命令行参数  >  环境变量  >  <root>/.gsc-config.json  >  默认值

用法：
  # 0) 验证凭据与资源权限（配置完第一步跑这个）
  python scripts/gsc-fetch.py --check

  # 1) 还原 GSC 页面的 24 小时按小时视图
  python scripts/gsc-fetch.py --mode hourly --days 2

  # 2) 按天，最近 28 天
  python scripts/gsc-fetch.py --mode daily --days 28

  # 3) 页面维度 / 查询维度
  python scripts/gsc-fetch.py --mode pages --days 28 --top 30
  python scripts/gsc-fetch.py --mode queries --days 28 --top 30

  # 4) 自定义维度组合
  python scripts/gsc-fetch.py --dimensions page,country --days 7 --out out.json

  # 5) 换项目 / 换站点
  python scripts/gsc-fetch.py --root /path/to/project --site sc-domain:example.com

依赖：google-auth + requests
"""

import argparse
import json
import os
import sys
import time
from datetime import date, datetime, timedelta
from urllib.parse import quote, urlsplit
from zoneinfo import ZoneInfo

import requests
from google.oauth2 import service_account

# GSC 所有日期/小时数据均以太平洋时间为准，不能拿本地日期去算区间
GSC_TZ = ZoneInfo("America/Los_Angeles")
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
API = "https://searchconsole.googleapis.com/webmasters/v3"
CONFIG_NAME = ".gsc-config.json"

MODES = {
    "hourly": ["hour"],
    "daily": ["date"],
    "pages": ["page"],
    "queries": ["query"],
    "countries": ["country"],
    "devices": ["device"],
}


def gsc_today():
    return datetime.now(GSC_TZ).date()


# ---------------------------------------------------------------- 配置解析


def find_root(cli_root=None):
    """确定项目根目录：参数 > GSC_ROOT > 向上找 .gsc-config.json > 脚本所在项目的父目录。"""
    if cli_root:
        return os.path.abspath(os.path.expanduser(cli_root))
    env_root = os.environ.get("GSC_ROOT")
    if env_root:
        return os.path.abspath(os.path.expanduser(env_root))
    d = os.getcwd()
    for _ in range(8):
        if os.path.isfile(os.path.join(d, CONFIG_NAME)):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config(root=None):
    """读配置。返回 {root, site, dataDir, key, cfgPath}。

    环境变量优先于配置文件，便于临时覆盖：
      GSC_ROOT / GSC_SITE / GSC_KEY / GSC_DATA_DIR
    """
    root = find_root(root)
    cfg_path = os.path.join(root, CONFIG_NAME)
    raw = {}
    if os.path.isfile(cfg_path):
        try:
            with open(cfg_path, encoding="utf-8") as fh:
                raw = json.load(fh) or {}
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] 配置文件解析失败，已忽略：{cfg_path}（{exc}）")

    def pick(env, *keys):
        v = os.environ.get(env)
        if v:
            return v
        for k in keys:
            if raw.get(k):
                return raw[k]
        return None

    data_dir = pick("GSC_DATA_DIR", "dataDir", "data_dir") or ".workbuddy/gsc-data"
    key = pick("GSC_KEY", "key", "keyPath") or ".secrets/gsc-sa.json"
    site = pick("GSC_SITE", "site", "resourceId")

    data_dir = os.path.expanduser(data_dir)
    key = os.path.expanduser(key)
    if not os.path.isabs(data_dir):
        data_dir = os.path.join(root, data_dir)
    if not os.path.isabs(key):
        key = os.path.join(root, key)

    return {
        "root": root,
        "site": site,
        "dataDir": data_dir,
        "key": key,
        "cfgPath": cfg_path if os.path.isfile(cfg_path) else None,
    }


def short(url, site=None):
    """URL → 站内路径。不依赖任何具体域名。"""
    path = urlsplit(url).path or "/"
    if not path.startswith("/"):
        path = "/" + path
    return path


# ---------------------------------------------------------------- 认证


def build_credentials(key_path):
    if not os.path.isfile(key_path):
        sys.exit(
            f"找不到服务账号密钥：{key_path}\n"
            f"请把下载的 JSON 重命名为 gsc-sa.json 放到 .secrets/ 目录下，"
            f"或用 --key 指定路径 / 设置 GSC_KEY 环境变量。"
        )
    try:
        return service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"密钥文件读取失败：{exc}")


def creds_email(key_path):
    try:
        with open(key_path, encoding="utf-8") as fh:
            return json.load(fh).get("client_email", "")
    except Exception:  # noqa: BLE001
        return ""


def auth_headers(creds):
    from google.auth.transport.requests import Request

    if not creds.valid:
        # token 刷新同样走网络，代理抖动时会抛 TransportError，一并重试
        for attempt in range(3):
            try:
                creds.refresh(Request())
                break
            except Exception as exc:  # noqa: BLE001
                if attempt == 2:
                    sys.exit(f"[FAIL] token 刷新失败（重试 3 次）：{exc}")
                time.sleep(2 * (attempt + 1))
    return {"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"}


RETRYABLE = (
    requests.exceptions.ProxyError,
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
    requests.exceptions.ChunkedEncodingError,
)


def _with_retry(call, attempts=3):
    """沙箱代理会随机 Broken pipe，日常 automation 必须能扛住。"""
    last = None
    for attempt in range(attempts):
        try:
            resp = call()
        except RETRYABLE as exc:
            last = exc
            if attempt == attempts - 1:
                sys.exit(f"[FAIL] 网络请求失败（重试 {attempts} 次）：{exc}")
            time.sleep(2 * (attempt + 1))
            continue
        # 5xx 与 429 视为可重试的服务端抖动
        if resp.status_code in (429, 500, 502, 503, 504) and attempt < attempts - 1:
            time.sleep(2 * (attempt + 1))
            continue
        return resp
    sys.exit(f"[FAIL] 网络请求失败：{last}")


def api_get(creds, path):
    return _with_retry(
        lambda: requests.get(f"{API}{path}", headers=auth_headers(creds), timeout=30)
    )


def api_post(creds, path, payload):
    return _with_retry(
        lambda: requests.post(
            f"{API}{path}",
            headers=auth_headers(creds),
            data=json.dumps(payload),
            timeout=90,
        )
    )


# ---------------------------------------------------------------- 权限与站点


def list_sites(creds):
    resp = api_get(creds, "/sites")
    if resp.status_code != 200:
        print(f"[FAIL] /sites 返回 {resp.status_code}: {resp.text[:300]}")
        return []
    return resp.json().get("siteEntry", [])


def check(creds, site=None, key_path=None):
    entries = list_sites(creds)
    print(f"[OK] 服务账号可访问 {len(entries)} 个资源：")
    for e in entries:
        print(f"  - {e.get('siteUrl')}  ({e.get('permissionLevel')})")

    if not site:
        if len(entries) == 1:
            print(f"\n[OK] 未指定 --site，自动采用唯一资源：{entries[0].get('siteUrl')}")
            return True
        if not entries:
            print("\n[WARN] 该服务账号没有任何 GSC 资源。")
            _print_add_user_hint(key_path)
            return False
        print("\n[WARN] 有多个资源，请用 --site 指定其中一个，并写入 .gsc-config.json。")
        return False

    urls = {e.get("siteUrl") for e in entries}
    if site not in urls:
        print(f"\n[WARN] 目标资源 {site} 不在列表里。")
        _print_add_user_hint(key_path)
        return False
    print(f"\n[OK] 目标资源 {site} 权限已就绪。")
    return True


def _print_add_user_hint(key_path):
    email = creds_email(key_path) if key_path else ""
    if email:
        print(f"       把服务账号邮箱加进 GSC：{email}")
    print("       GSC → 设置 → 用户和权限 → 添加用户 → 权限选「完全」")
    print("       必须在 Domain property（sc-domain:xxx）上加，不是网址前缀属性。")


def resolve_site(creds, site=None):
    """没配站点时自动探测；多资源则要求显式指定，绝不猜。"""
    entries = list_sites(creds)
    urls = [e.get("siteUrl") for e in entries if e.get("siteUrl")]
    if site:
        if site in urls:
            return site
        guess = f"sc-domain:{site.lstrip('/').replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]}"
        if guess in urls:
            print(f"[info] {site} 归一化为 {guess}")
            return guess
        sys.exit(
            f"[FAIL] 该服务账号无法访问 {site}。可访问：{', '.join(urls) or '（无）'}\n"
            f"       检查 .gsc-config.json 的 site 字段，或把服务账号加为站点用户。"
        )
    if len(urls) == 1:
        print(f"[info] 未配置站点，自动采用唯一资源：{urls[0]}")
        return urls[0]
    if not urls:
        sys.exit("[FAIL] 该服务账号没有任何 GSC 资源，先把它加为站点用户。")
    sys.exit(
        "[FAIL] 该服务账号可访问多个资源，必须显式指定：\n"
        + "\n".join(f"       --site {u}" for u in urls)
        + "\n       选定后写入 <project>/.gsc-config.json 的 site 字段。"
    )


# ---------------------------------------------------------------- 取数


def query(creds, site, dimensions, start, end, row_limit, data_state, type_):
    payload = {
        "startDate": start,
        "endDate": end,
        "dimensions": dimensions,
        "rowLimit": min(row_limit, 25000),
        "startRow": 0,
    }
    if data_state:
        payload["dataState"] = data_state
    if type_:
        payload["type"] = type_

    rows = []
    meta = {}
    while True:
        resp = api_post(creds, f"/sites/{quote(site, safe='')}/searchAnalytics/query", payload)
        if resp.status_code != 200:
            sys.exit(f"[FAIL] query 返回 {resp.status_code}: {resp.text[:600]}")
        body = resp.json()
        meta = body.get("metadata", meta)
        batch = body.get("rows", [])
        rows.extend(batch)
        if len(batch) < payload["rowLimit"] or len(rows) >= row_limit:
            break
        payload["startRow"] += payload["rowLimit"]
    return rows[:row_limit], meta


def fmt_num(v, digits=0):
    return f"{v:,.{digits}f}"


def print_table(rows, dimensions, top):
    if not rows:
        print("（无数据）")
        return
    headers = dimensions + ["clicks", "impressions", "ctr", "position"]
    widths = [max(len(d), 12) for d in dimensions] + [10, 13, 9, 9]

    def line(cells):
        return "  ".join(str(c).ljust(w) for c, w in zip(cells, widths))

    print(line(headers))
    print("-" * (sum(widths) + 2 * (len(widths) - 1)))
    for r in rows[:top]:
        keys = [str(k)[:34] for k in r["keys"]]
        print(
            line(
                keys
                + [
                    fmt_num(r.get("clicks", 0)),
                    fmt_num(r.get("impressions", 0)),
                    f"{r.get('ctr', 0) * 100:.2f}%",
                    f"{r.get('position', 0):.1f}",
                ]
            )
        )
    total_clicks = sum(r.get("clicks", 0) for r in rows)
    total_impr = sum(r.get("impressions", 0) for r in rows)
    print("-" * (sum(widths) + 2 * (len(widths) - 1)))
    print(
        f"共 {len(rows)} 行 | 点击 {fmt_num(total_clicks)} | 曝光 {fmt_num(total_impr)}"
        + (f" | CTR {total_clicks / total_impr * 100:.2f}%" if total_impr else "")
    )


def main():
    ap = argparse.ArgumentParser(description="GSC Search Analytics 取数")
    ap.add_argument("--root", help="项目根目录（默认：向上找 .gsc-config.json）")
    ap.add_argument("--key", help="服务账号 JSON 路径")
    ap.add_argument("--site", help="GSC 资源，如 sc-domain:example.com")
    ap.add_argument("--check", action="store_true", help="只验证权限，不取数")
    ap.add_argument("--mode", choices=sorted(MODES), default="daily")
    ap.add_argument("--dimensions", help="逗号分隔，覆盖 --mode，如 page,country")
    ap.add_argument("--days", type=int, default=28, help="回溯天数，含今天")
    ap.add_argument("--start", help="YYYY-MM-DD（太平洋时间），覆盖 --days")
    ap.add_argument("--end", help="YYYY-MM-DD，默认今天")
    ap.add_argument("--row-limit", type=int, default=1000, help="请求行数上限")
    ap.add_argument("--top", type=int, default=25, help="表格打印行数")
    ap.add_argument("--type", default="web", help="web/image/video/news/discover/googleNews")
    ap.add_argument("--data-state", default=None, help="final/all/hourly_all")
    ap.add_argument("--out", help="把原始 JSON 写入该文件")
    args = ap.parse_args()

    cfg = load_config(args.root)
    key_path = args.key or cfg["key"]
    creds = build_credentials(key_path)

    if args.check:
        sys.exit(0 if check(creds, args.site or cfg["site"], key_path) else 1)

    site = resolve_site(creds, args.site or cfg["site"])

    if args.dimensions:
        dimensions = [d.strip() for d in args.dimensions.split(",") if d.strip()]
    else:
        dimensions = MODES[args.mode]

    end = args.end or gsc_today().isoformat()
    if args.start:
        start = args.start
    else:
        start = (date.fromisoformat(end) - timedelta(days=max(args.days - 1, 0))).isoformat()

    # hour 维度必须配 hourly_all，否则拿不到未定稿数据
    data_state = args.data_state or ("hourly_all" if "hour" in dimensions else "final")

    rows, meta = query(
        creds, site, dimensions, start, end, args.row_limit, data_state, args.type
    )

    print(f"资源   : {site}")
    print(f"区间   : {start} ~ {end}（太平洋时间）")
    print(f"维度   : {','.join(dimensions)}   dataState={data_state}   type={args.type}")
    if meta:
        print(f"metadata: {json.dumps(meta, ensure_ascii=False)}")
    print()
    print_table(rows, dimensions, args.top)

    if args.out:
        out_path = args.out
        if not os.path.isabs(out_path):
            out_path = os.path.join(os.getcwd(), out_path)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(
                {
                    "site": site,
                    "start": start,
                    "end": end,
                    "dimensions": dimensions,
                    "dataState": data_state,
                    "type": args.type,
                    "metadata": meta,
                    "fetchedAt": datetime.now().isoformat(timespec="seconds"),
                    "rows": rows,
                },
                fh,
                ensure_ascii=False,
                indent=2,
            )
        print(f"\n原始数据已写入 {out_path}")


if __name__ == "__main__":
    main()
