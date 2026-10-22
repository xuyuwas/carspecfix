#!/usr/bin/env python3
"""Live-site audit for carspecfix.com: fetch every sitemap URL and collect
on-page signals (title, description, canonical, H1/H2, word count, JSON-LD,
internal links, images, hreflang/robots meta). Read-only."""
import json
import re
import ssl
import sys
import time
import urllib.request
import urllib.error
import html as htmllib

BASE = "https://carspecfix.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
CTX = ssl.create_default_context()


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            raw = r.read()
            enc = r.headers.get("Content-Encoding", "")
            if "gzip" in enc:
                import gzip
                raw = gzip.decompress(raw)
            return r.status, raw.decode("utf-8", "replace"), time.time() - t0, dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, "", time.time() - t0, dict(e.headers or {})
    except Exception as e:
        return 0, str(e), time.time() - t0, {}


def text_of(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<svg.*?</svg>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", htmllib.unescape(h)).strip()


def meta(h, name, attr="name"):
    m = re.search(r'<meta[^>]+%s="%s"[^>]+content="([^"]*)"' % (attr, re.escape(name)), h, re.I)
    if m:
        return htmllib.unescape(m.group(1))
    m = re.search(r'<meta[^>]+content="([^"]*)"[^>]+%s="%s"' % (attr, re.escape(name)), h, re.I)
    return htmllib.unescape(m.group(1)) if m else None


def one(h, pat):
    m = re.search(pat, h, re.I | re.S)
    return htmllib.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else None


def main():
    st, sm, _, _ = get(BASE + "/sitemap.xml")
    urls = re.findall(r"<loc>(.*?)</loc>", sm)
    print(f"sitemap status={st} urls={len(urls)}", file=sys.stderr)
    rows = []
    for u in urls:
        st, h, dt, hd = get(u)
        row = {
            "url": u.replace(BASE, "") or "/",
            "status": st,
            "ms": round(dt * 1000),
            "bytes": len(h),
            "title": one(h, r"<title[^>]*>(.*?)</title>"),
            "desc": meta(h, "description"),
            "canonical": (re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]*)"', h, re.I) or [None, None])[1],
            "robots": meta(h, "robots"),
            "h1": [re.sub(r"\s+", " ", x).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.I | re.S)],
            "h2count": len(re.findall(r"<h2[^>]*>", h, re.I)),
            "words": len(text_of(re.sub(r"<(nav|footer|header).*?</\1>", " ", h, flags=re.S | re.I)).split()),
            "jsonld": re.findall(r'"@type"\s*:\s*"([^"]+)"', h),
            "imgs": len(re.findall(r"<img\b", h, re.I)),
            "img_alt_missing": len([x for x in re.findall(r"<img\b[^>]*>", h, re.I) if "alt=" not in x]),
            "links_internal": len(set(re.findall(r'href="(/[^"#?]*)"', h))),
            "hreflang": len(re.findall(r'hreflang=', h, re.I)),
            "lang": (re.search(r'<html[^>]+lang="([^"]*)"', h, re.I) or [None, None])[1],
            "og_image": meta(h, "og:image", "property"),
            "cache": hd.get("Cache-Control") or hd.get("cache-control"),
        }
        rows.append(row)
        print(f"  {st} {row['ms']:>5}ms {row['bytes']:>6}B {row['url']}", file=sys.stderr)
    json.dump(rows, open("/tmp/audit.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(rows, ensure_ascii=False))


if __name__ == "__main__":
    main()
