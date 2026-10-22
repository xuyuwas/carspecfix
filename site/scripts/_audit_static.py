#!/usr/bin/env python3
"""Static analysis over site/dist: link graph (orphans, depth), title patterns,
boilerplate similarity between year pages. Read-only."""
import html as H
import json
import os
import re
import collections

ROOT = "site/dist"
pages = {}
for dirpath, _, files in os.walk(ROOT):
    if "index.html" in files:
        p = os.path.join(dirpath, "index.html")
        url = "/" + os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
        url = "/" if url == "/." else url.rstrip("/") + "/"
        pages[url] = open(p, encoding="utf-8").read()

def text(h):
    h = re.sub(r"<(script|style|svg|nav|footer|header).*?</\1>", " ", h, flags=re.S | re.I)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", h))).strip()

links = {}
for u, h in pages.items():
    tgt = set()
    for href in re.findall(r'href="(/[^"#?]*)"', h):
        tgt.add(href if href.endswith("/") or "." in href.split("/")[-1] else href + "/")
    links[u] = {t for t in tgt if t in pages}

indeg = collections.Counter()
for u, ts in links.items():
    for t in ts:
        indeg[t] += 1

print("pages:", len(pages))
print("\n-- orphans (0 inbound internal links) --")
orph = [u for u in pages if indeg[u] == 0 and u != "/"]
print(orph or "none")

# depth from home (BFS, html pages only)
depth = {"/": 0}
q = collections.deque(["/"])
while q:
    cur = q.popleft()
    for t in links.get(cur, ()):
        if t not in depth:
            depth[t] = depth[cur] + 1
            q.append(t)
unreach = [u for u in pages if u not in depth]
print("\n-- unreachable from home within HTML links --")
print(unreach or "none")
print("depth histogram:", dict(sorted(collections.Counter(depth.values()).items())))

print("\n-- outbound internal links: fewest --")
for u, n in sorted(((u, len(t)) for u, t in links.items()), key=lambda x: x[1])[:8]:
    print(f"  {n:>3} {u}")

print("\n-- title patterns --")
for u in sorted(pages):
    h = pages[u]
    t = re.search(r"<title[^>]*>(.*?)</title>", h, re.S)
    t = H.unescape(t.group(1)).strip() if t else ""
    if "/specs/" in u and re.search(r"/\d{4}/$", u):
        kw = [k for k in ("Oil Capacity", "Oil", "Tire Size", "Tire Sizes", "Pressure", "Recalls") if k in t]
        print(f"  {len(t):>3} {','.join(kw):<38} {t}")

print("\n-- boilerplate similarity between RAV4 year pages --")
def shingles(s, n=5):
    w = re.findall(r"[a-z0-9]+", s.lower())
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}
rav = sorted([u for u in pages if "/specs/toyota/rav4/" in u and u.rstrip("/").split("/")[-1].isdigit()])
base = {u: shingles(text(pages[u])) for u in rav}
import itertools
sims = []
for a, b in itertools.combinations(rav, 2):
    A, B = base[a], base[b]
    sims.append((round(len(A & B) / max(1, len(A | B)), 3), a, b))
sims.sort(reverse=True)
print("pairs:", len(sims), "| median Jaccard:", sorted(s[0] for s in sims)[len(sims) // 2])
for s in sims[:5]:
    print("  ", s)
