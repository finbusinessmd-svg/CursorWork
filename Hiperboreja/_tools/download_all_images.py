#!/usr/bin/env python3
"""Download every image referenced in the public archive."""
from __future__ import annotations

import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin
from urllib.request import Request, urlopen

BASE = "https://hiperboreja.ru/"
RAW = Path("/workspace/Hiperboreja/archive/raw")
OUT = Path("/workspace/Hiperboreja/content/images")
UA = "HiperborejaOwnerArchive/1.0"
OUT.mkdir(parents=True, exist_ok=True)

paths = set()
for f in RAW.rglob("*.html"):
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(
        r'(?:src|href)=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp|ico))["\']', t, re.I
    ):
        src = m.group(1).replace("&amp;", "&").strip()
        if src.startswith(("javascript:", "data:")):
            continue
        url = urljoin(BASE, src)
        if "hiperboreja.ru" not in url:
            continue
        paths.add(url)

# Also try original (non-resized) product files inferred from thumbs
extra = set()
for url in list(paths):
    if "/resized/" in url:
        extra.add(url.replace("/resized/", "/").replace("_210x320", ""))
paths |= extra

print(f"to fetch: {len(paths)}")
ok = fail = skip = 0
failed = []
for url in sorted(paths):
    rel = unquote(url.split("hiperboreja.ru/", 1)[-1].split("?", 1)[0].lstrip("/"))
    dest = OUT / rel
    if dest.exists() and dest.stat().st_size > 200:
        skip += 1
        continue
    print("GET", url)
    req = Request(url, headers={"User-Agent": UA})
    try:
        with urlopen(req, timeout=40) as resp:
            data = resp.read()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        print(f"  {len(data)} -> {dest.relative_to(OUT)}")
        ok += 1
    except (HTTPError, URLError, Exception) as e:
        print("  FAIL", e)
        fail += 1
        failed.append({"url": url, "error": str(e)})
    time.sleep(0.12)

print({"ok": ok, "skip": skip, "fail": fail, "files": len(list(OUT.rglob('*')))})
if failed:
    print("FAILED:")
    for x in failed:
        print(" ", x)
