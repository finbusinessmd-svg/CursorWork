#!/usr/bin/env python3
"""Download unique full-size VirtueMart cover images."""
from __future__ import annotations

import re
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

OUT = Path("/workspace/Hiperboreja")
RAW = OUT / "archive" / "raw"
COVERS = OUT / "content" / "covers"
ASSETS = OUT / "archive" / "assets" / "images" / "stories" / "virtuemart" / "product"
UA = "HiperborejaOwnerArchive/1.0"

COVERS.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

urls = set()
for f in RAW.rglob("*.html"):
    html = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(
        r'https?://hiperboreja\.ru(/images/stories/virtuemart/product/(?!resized/)[^"\s>]+\.(?:jpg|jpeg|png|gif))',
        html,
        re.I,
    ):
        urls.add("https://hiperboreja.ru" + m.group(1))
    for m in re.finditer(
        r'src="(/images/stories/virtuemart/product/(?!resized/)[^"]+\.(?:jpg|jpeg|png|gif))"',
        html,
        re.I,
    ):
        urls.add("https://hiperboreja.ru" + m.group(1))
    for m in re.finditer(
        r'src="(/images/[^"]+\.(?:jpg|jpeg|png|gif))"',
        html,
        re.I,
    ):
        if "/resized/" not in m.group(1) and "virtuemart/product/" not in m.group(1):
            urls.add("https://hiperboreja.ru" + m.group(1))

print(f"Unique image URLs: {len(urls)}")
ok = fail = 0
for url in sorted(urls):
    name = url.split("/")[-1]
    dest_cover = COVERS / name
    # also keep path under assets
    rel = url.split("hiperboreja.ru/")[-1]
    dest_asset = OUT / "archive" / "assets" / rel
    if dest_cover.exists() and dest_cover.stat().st_size > 1000:
        print(f"skip {name}")
        continue
    print(f"GET {url}")
    req = Request(url, headers={"User-Agent": UA})
    try:
        with urlopen(req, timeout=40) as resp:
            data = resp.read()
        dest_cover.write_bytes(data)
        dest_asset.parent.mkdir(parents=True, exist_ok=True)
        dest_asset.write_bytes(data)
        print(f"  {len(data)} bytes -> {name}")
        ok += 1
    except (HTTPError, URLError, Exception) as e:
        print(f"  FAIL {e}")
        fail += 1
    time.sleep(0.2)
print({"ok": ok, "fail": fail, "covers": len(list(COVERS.glob('*')))})
