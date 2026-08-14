#!/usr/bin/env python3
"""Extract books, articles, poems, and pages from archived HTML."""
from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path

OUT = Path("/workspace/Hiperboreja")
RAW = OUT / "archive" / "raw"
DATA = OUT / "archive" / "extracted"
CONTENT = OUT / "content"


def strip_tags(html: str) -> str:
    html = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", html)
    html = re.sub(r"(?is)<br\s*/?>", "\n", html)
    html = re.sub(r"(?is)</p>", "\n\n", html)
    html = re.sub(r"(?is)</h[1-6]>", "\n\n", html)
    html = re.sub(r"(?is)<[^>]+>", " ", html)
    html = unescape(html)
    html = re.sub(r"[ \t]+\n", "\n", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    html = re.sub(r"[ \t]{2,}", " ", html)
    return html.strip()


def first(pat: str, text: str, flags=re.I | re.S) -> str | None:
    m = re.search(pat, text, flags)
    return unescape(m.group(1).strip()) if m else None


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[«»\"'`]", "", s)
    s = re.sub(r"[^0-9a-zа-яё\- ]+", "", s, flags=re.I)
    s = re.sub(r"\s+", "-", s)
    return s[:80] or "untitled"


def extract_product(html: str, src: str) -> dict | None:
    if 'class="product-name"' not in html and "productdetails-view" not in html:
        return None
    name = first(r'<h1 class="product-name">([^<]+)</h1>', html)
    if not name:
        return None
    if "Товар не найден" in html or "product not found" in html.lower():
        return None
    pid = first(r"virtuemart_product_id=(\d+)", html)
    cid = first(r"virtuemart_category_id=(\d+)", html)
    price = first(r'<span class="PricesalesPrice"\s*>\s*([^<]+)</span>', html)
    short = first(r'<div class="product-short-description">(.*?)</div>', html)
    desc = first(r'<div class="product-description"[^>]*>(.*?)</div>\s*(?:<div|$)', html)
    if not desc:
        desc = first(r'id="description"[^>]*>(.*?)</div>', html)
    # longer description often in product-description
    long_block = first(
        r'<div class="product-description">(.*?)</div>\s*<div class="clear"', html
    )
    img = first(
        r'class="main-image".*?<img[^>]+src="([^"]+)"', html
    ) or first(r'rel=\'vm-additional-images\' href="([^"]+)"', html)
    sku = first(r'Артикул[:\s]*</span>\s*([^<]+)', html) or first(
        r'class="product-sku"[^>]*>([^<]+)', html
    )
    return {
        "id": int(pid) if pid else None,
        "category_id": int(cid) if cid else None,
        "title": name,
        "price": price,
        "sku": sku,
        "image": img,
        "short_html": short,
        "short_text": strip_tags(short or ""),
        "description_html": long_block or desc,
        "description_text": strip_tags(long_block or desc or ""),
        "source_file": src,
    }


def extract_k2(html: str, src: str) -> dict | None:
    if "itemTitle" not in html:
        return None
    title = first(r'<h2 class="itemTitle">\s*(?:<a[^>]*>)?([^<]+)', html)
    if not title:
        return None
    if title.strip() in {"", "K2"}:
        return None
    # skip empty 404-ish
    if "Item not found" in html or "Материал не найден" in html:
        return None
    kid = first(r"view=item&(?:amp;)?id=(\d+)", html) or first(
        r"/item/(\d+)-", html
    )
    date = first(r'class="itemDateCreated"[^>]*>\s*([^<]+)', html)
    author = first(r'class="itemAuthor"[^>]*>.*?>([^<]+)</a>', html)
    cat = first(r'class="itemCategory"[^>]*>.*?<a[^>]*>([^<]+)</a>', html)
    intro = first(r'<div class="itemIntroText">\s*(.*?)</div>\s*<div class="itemFullText', html)
    full = first(r'<div class="itemFullText">\s*(.*?)</div>\s*(?:<div class="itemContentFooter"|<div class="itemToolbar"|<div class="itemRatingBlock"|<div class="clr")', html)
    body_html = " ".join(x for x in [intro, full] if x)
    if not body_html:
        body_html = first(r'<div class="itemBody">(.*?)</div>\s*<div class="clr"', html)
    text = strip_tags(body_html or "")
    if len(text) < 40:
        return None
    return {
        "id": int(kid) if kid else None,
        "title": title.strip(),
        "date": (date or "").strip(),
        "author": (author or "").strip(),
        "category": (cat or "").strip(),
        "html": body_html,
        "text": text,
        "source_file": src,
    }


def extract_article(html: str, src: str) -> dict | None:
    if "com_content" not in html and 'item-page' not in html:
        return None
    title = first(r'<h2[^>]*class="contentheading"[^>]*>\s*(?:<a[^>]*>)?([^<]+)', html)
    if not title:
        title = first(r'<h1[^>]*>([^<]+)</h1>', html)
    body = first(r'<div class="item-page"[^>]*>(.*?)</div>\s*(?:<div id="jc"|$)', html)
    if not body:
        body = first(r'<div class="article-content"[^>]*>(.*?)</div>', html)
    if not title or not body:
        return None
    text = strip_tags(body)
    if len(text) < 80:
        return None
    return {
        "title": title.strip(),
        "html": body,
        "text": text,
        "source_file": src,
    }


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    CONTENT.mkdir(parents=True, exist_ok=True)
    (CONTENT / "books").mkdir(exist_ok=True)
    (CONTENT / "blog").mkdir(exist_ok=True)
    (CONTENT / "pages").mkdir(exist_ok=True)

    products = {}
    k2_items = {}
    articles = {}

    files = list(RAW.rglob("*.html")) + list(RAW.rglob("*.htm"))
    print(f"Scanning {len(files)} html files")
    for f in files:
        html = f.read_text(encoding="utf-8", errors="replace")
        rel = str(f.relative_to(OUT))
        p = extract_product(html, rel)
        if p and p["id"] is not None:
            prev = products.get(p["id"])
            if not prev or len(p["description_text"]) > len(prev["description_text"]):
                products[p["id"]] = p
        k = extract_k2(html, rel)
        if k:
            key = k["id"] if k["id"] is not None else k["title"]
            prev = k2_items.get(key)
            if not prev or len(k["text"]) > len(prev["text"]):
                k2_items[key] = k
        a = extract_article(html, rel)
        if a:
            prev = articles.get(a["title"])
            if not prev or len(a["text"]) > len(prev["text"]):
                articles[a["title"]] = a

    books = sorted(products.values(), key=lambda x: (x["title"] or "", x["id"] or 0))
    posts = sorted(k2_items.values(), key=lambda x: (x.get("date") or "", x["title"]))
    pages = sorted(articles.values(), key=lambda x: x["title"])

    (DATA / "books.json").write_text(
        json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DATA / "blog.json").write_text(
        json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DATA / "pages.json").write_text(
        json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    for b in books:
        name = f"{b['id']:02d}-{slugify(b['title'])}.md"
        md = [
            f"# {b['title']}",
            "",
            f"- ID: {b['id']}",
            f"- Preț: {b['price'] or '—'}",
            f"- Imagine: {b['image'] or '—'}",
            "",
            "## Date scurte",
            "",
            b["short_text"] or "—",
            "",
            "## Descriere",
            "",
            b["description_text"] or "—",
            "",
        ]
        (CONTENT / "books" / name).write_text("\n".join(md), encoding="utf-8")

    for p in posts:
        ident = p["id"] if p["id"] is not None else slugify(p["title"])[:20]
        name = f"{ident}-{slugify(p['title'])}.md"
        md = [
            f"# {p['title']}",
            "",
            f"- ID: {p['id']}",
            f"- Dată: {p['date'] or '—'}",
            f"- Autor: {p['author'] or '—'}",
            f"- Categorie: {p['category'] or '—'}",
            "",
            p["text"],
            "",
        ]
        (CONTENT / "blog" / name).write_text("\n".join(md), encoding="utf-8")

    for a in pages:
        name = f"{slugify(a['title'])}.md"
        (CONTENT / "pages" / name).write_text(
            f"# {a['title']}\n\n{a['text']}\n", encoding="utf-8"
        )

    catalog = {
        "books": len(books),
        "blog_posts": len(posts),
        "pages": len(pages),
        "book_titles": [b["title"] for b in books],
        "blog_titles": [p["title"] for p in posts],
        "page_titles": [a["title"] for a in pages],
    }
    (DATA / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(catalog, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
