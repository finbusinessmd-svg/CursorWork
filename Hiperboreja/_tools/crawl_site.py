#!/usr/bin/env python3
"""Archive public content from hiperboreja.ru (owner backup)."""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = "https://hiperboreja.ru/"
OUT = Path("/workspace/Hiperboreja")
RAW = OUT / "archive" / "raw"
ASSETS = OUT / "archive" / "assets"
DATA = OUT / "archive" / "extracted"
UA = "HiperborejaOwnerArchive/1.0 (site backup before hosting expiry)"

SKIP_PREFIXES = (
    "/administrator/",
    "/cache/",
    "/cli/",
    "/includes/",
    "/installation/",
    "/libraries/",
    "/logs/",
    "/tmp/",
)
SKIP_EXT = {".php?"}  # not used
ASSET_EXT = {
    ".css",
    ".js",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".pdf",
    ".mp3",
    ".mp4",
    ".zip",
    ".doc",
    ".docx",
    ".epub",
    ".fb2",
}

SEED_PATHS = [
    "/",
    "/robots.txt",
    "/index.php?format=feed&type=rss",
    "/index.php?format=feed&type=atom",
    "/index.php?option=com_content&view=article&id=1:izdatelistvo-hiperboreja&catid=2&Itemid=101",
    "/index.php?option=com_content&view=article&id=3",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=8&Itemid=125",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=5&Itemid=126",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=6&Itemid=127",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=7&Itemid=128",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=10&Itemid=160",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=1&Itemid=129",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=4&Itemid=130",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=2&Itemid=131",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=3&Itemid=132",
    "/index.php?option=com_virtuemart&view=category&virtuemart_category_id=9&Itemid=159",
    "/index.php?option=com_k2&view=itemlist&layout=category&task=category&id=1&Itemid=133",
    "/index.php?option=com_k2&view=itemlist&layout=category&task=category&id=2&Itemid=145",
    "/index.php?option=com_k2&view=itemlist&task=user&id=42",
    "/index.php?option=com_k2&view=itemlist&task=user&id=43",
    "/index.php?option=com_search",
    "/index.php?option=com_virtuemart&view=cart",
    "/index.php?option=com_virtuemart&view=user",
    "/index.php?option=com_virtuemart&view=manufacturer",
    "/index.php?option=com_virtuemart&view=virtuemart",
    "/index.php?option=com_contact",
    "/index.php?option=com_users&view=login",
    "/index.php?option=com_acymailing",
]

# Probe likely product IDs (VirtueMart often sequential)
for i in range(1, 80):
    SEED_PATHS.append(
        f"/index.php?option=com_virtuemart&view=productdetails&virtuemart_product_id={i}"
    )
for i in range(1, 80):
    SEED_PATHS.append(f"/index.php?option=com_k2&view=item&id={i}&Itemid=133")
for i in range(1, 30):
    SEED_PATHS.append(f"/index.php?option=com_content&view=article&id={i}")
for i in range(1, 20):
    SEED_PATHS.append(
        f"/index.php?option=com_virtuemart&view=category&virtuemart_category_id={i}"
    )

# Common image/media folders
for folder in [
    "/images/",
    "/images/stories/",
    "/images/stories/virtuemart/",
    "/images/stories/virtuemart/product/",
    "/images/stories/virtuemart/category/",
    "/media/",
    "/templates/ja_vintas/",
]:
    SEED_PATHS.append(folder)


class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.texts = []
        self._capture = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag == "a" and "href" in ad:
            self.links.append(("a", ad["href"]))
            self._capture = "a"
            self._buf = []
        if tag == "img" and "src" in ad:
            self.links.append(("img", ad["src"]))
            if "alt" in ad:
                self.texts.append(("img_alt", ad["alt"]))
        for attr in ("src", "href", "data-src", "poster"):
            if attr in ad and tag in {
                "script",
                "link",
                "iframe",
                "source",
                "video",
                "audio",
                "embed",
            }:
                self.links.append((tag, ad[attr]))
        if tag == "meta" and ad.get("property") in {"og:image", "og:url"}:
            if "content" in ad:
                self.links.append(("meta", ad["content"]))

    def handle_endtag(self, tag):
        if tag == "a" and self._capture == "a":
            self.texts.append(("a", "".join(self._buf).strip()))
            self._capture = None

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)


def normalize(url: str) -> str | None:
    if not url:
        return None
    url = url.strip()
    if url.startswith(("javascript:", "mailto:", "tel:", "#")):
        return None
    url = urljoin(BASE, url)
    p = urlparse(url)
    if p.scheme not in {"http", "https"}:
        return None
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    if host != "hiperboreja.ru":
        return None
    path = p.path or "/"
    for skip in SKIP_PREFIXES:
        if path.startswith(skip):
            return None
    # drop fragments
    q = p.query.replace("&amp;", "&")
    return urlunparse(("https", "hiperboreja.ru", path, "", q, ""))


def is_asset(url: str) -> bool:
    path = urlparse(url).path.lower()
    ext = os.path.splitext(path)[1]
    return ext in ASSET_EXT or path.startswith(("/images/", "/media/", "/t3-assets/", "/templates/", "/plugins/", "/modules/", "/components/"))


def safe_filename(url: str, is_html: bool) -> Path:
    p = urlparse(url)
    path = unquote(p.path)
    if path.endswith("/"):
        path = path + "index.html"
    if not path or path == "/":
        path = "/index.html"
    if is_html and not path.endswith((".html", ".htm", ".xml", ".txt", ".rss", ".atom")):
        if p.query:
            h = hashlib.md5(p.query.encode()).hexdigest()[:12]
            path = path.rstrip("/") + f"__{h}.html"
        else:
            path = path.rstrip("/") + ".html"
    # keep query-less assets as-is
    if not is_html and p.query:
        h = hashlib.md5(p.query.encode()).hexdigest()[:8]
        root, ext = os.path.splitext(path)
        path = f"{root}__{h}{ext}"
    rel = path.lstrip("/")
    rel = re.sub(r"[^A-Za-z0-9._/\-]+", "_", rel)
    return RAW / rel if is_html else ASSETS / rel


def fetch(url: str, timeout=40) -> tuple[int, str, bytes]:
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            ctype = resp.headers.get("Content-Type", "")
            return resp.status, ctype, data
    except HTTPError as e:
        data = e.read() if e.fp else b""
        return e.code, e.headers.get("Content-Type", "") if e.headers else "", data
    except URLError as e:
        return 0, str(e.reason), b""
    except Exception as e:
        return 0, str(e), b""


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    queue = deque()
    seen = set()
    for s in SEED_PATHS:
        n = normalize(s)
        if n and n not in seen:
            seen.add(n)
            queue.append(n)

    pages = []
    assets = []
    errors = []
    extra_found = 0

    while queue:
        url = queue.popleft()
        print(f"[{len(pages)+len(assets)+1}] {url}", flush=True)
        status, ctype, body = fetch(url)
        time.sleep(0.15)
        if status == 0 or not body:
            errors.append({"url": url, "status": status, "error": ctype})
            continue
        if status >= 400:
            errors.append({"url": url, "status": status, "bytes": len(body)})
            continue

        htmlish = "text/html" in ctype or "xml" in ctype or "text/plain" in ctype or url.endswith((".xml", ".txt", ".rss"))
        if htmlish and not is_asset(url):
            dest = safe_filename(url, True)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(body)
            rec = {
                "url": url,
                "status": status,
                "ctype": ctype,
                "bytes": len(body),
                "file": str(dest.relative_to(OUT)),
            }
            pages.append(rec)
            try:
                text = body.decode("utf-8", errors="replace")
            except Exception:
                text = ""
            parser = LinkExtractor()
            try:
                parser.feed(text)
            except Exception:
                pass
            for _, href in parser.links:
                n = normalize(href)
                if n and n not in seen:
                    seen.add(n)
                    queue.append(n)
                    extra_found += 1
            # CSS url() refs
            for m in re.finditer(r"url\((['\"]?)([^)'\"]+)\1\)", text):
                n = normalize(m.group(2))
                if n and n not in seen:
                    seen.add(n)
                    queue.append(n)
        else:
            dest = safe_filename(url, False)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(body)
            assets.append(
                {
                    "url": url,
                    "status": status,
                    "ctype": ctype,
                    "bytes": len(body),
                    "file": str(dest.relative_to(OUT)),
                }
            )
            if "css" in ctype or url.endswith(".css"):
                try:
                    text = body.decode("utf-8", errors="replace")
                except Exception:
                    text = ""
                for m in re.finditer(r"url\((['\"]?)([^)'\"]+)\1\)", text):
                    n = normalize(m.group(2))
                    if n and n not in seen:
                        seen.add(n)
                        queue.append(n)

    (DATA / "pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "pages": len(pages),
        "assets": len(assets),
        "errors": len(errors),
        "seen": len(seen),
        "discovered_during_crawl": extra_found,
    }
    (DATA / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("DONE", summary)


if __name__ == "__main__":
    main()
