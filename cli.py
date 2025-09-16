#!/usr/bin/env python3
import argparse
import io
import re
import sys
import zipfile
from urllib.parse import urlparse

import requests

URL_REGEX = re.compile(r"(https?://[^\s\"'<>)\]]+)", re.IGNORECASE)
IMG_EXTS = {".jpg",".jpeg",".png",".gif",".webp",".bmp",".svg",".avif"}
TIMEOUT = 12
MAX_BYTES = 12 * 1024 * 1024

def looks_like_image_url(url: str) -> bool:
    return any(urlparse(url).path.lower().endswith(ext) for ext in IMG_EXTS)

def fetch(url: str):
    r = requests.get(url, stream=True, timeout=TIMEOUT)
    r.raise_for_status()
    buf, total = io.BytesIO(), 0
    for chunk in r.iter_content(8192):
        if not chunk: continue
        total += len(chunk)
        if total > MAX_BYTES:
            raise ValueError("file too large")
        buf.write(chunk)
    buf.seek(0)
    name = urlparse(url).path.split("/")[-1] or "image"
    if "." not in name:
        ctype = r.headers.get("Content-Type","")
        if ctype.startswith("image/"):
            name = f"image.{ctype.split('/')[-1].split(';')[0]}"
    return name, buf.getvalue()

def main():
    ap = argparse.ArgumentParser(description="Extract image URLs from text, optionally download to a ZIP.")
    ap.add_argument("-i", "--input", help="Path to text file (default: stdin)")
    ap.add_argument("-o", "--output", default="images.zip", help="ZIP filename (default: images.zip)")
    ap.add_argument("--no-ext-filter", action="store_true", help="Do not filter by image extensions")
    ap.add_argument("--print-urls", action="store_true", help="Only print URLs (no download)")
    args = ap.parse_args()

    text = open(args.input, "r", encoding="utf-8").read() if args.input else sys.stdin.read()
    urls = [m.group(1).rstrip('.,);\'">]') for m in URL_REGEX.finditer(text)]
    if not args.no-ext-filter:
        urls = [u for u in urls if looks_like_image_url(u)]

    urls = list(dict.fromkeys(urls))  # dedupe preserve order

    if args.print-urls:
        for u in urls:
            print(u)
        return

    if not urls:
        print("No image URLs found.", file=sys.stderr)
        sys.exit(1)

    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        seen = set()
        for u in urls:
            try:
                name, data = fetch(u)
            except Exception as e:
                print(f"[skip] {u} -> {e}", file=sys.stderr)
                continue
            base, final, k = name or "image", None, 1
            final = base
            while final in seen:
                parts = base.rsplit(".", 1)
                final = f"{parts[0]}_{k}.{parts[1]}" if len(parts)==2 else f"{base}_{k}"
                k += 1
            seen.add(final)
            zf.writestr(final, data)
    with open(args.output, "wb") as f:
        f.write(zbuf.getvalue())
    print(f"Wrote {args.output} with {len(seen)} files.")

if __name__ == "__main__":
    main()
