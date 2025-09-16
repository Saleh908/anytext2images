import io
import re
import zipfile
from urllib.parse import urlparse

import requests
import streamlit as st

# --- Config ---
MAX_BYTES = 12 * 1024 * 1024  # 12 MB cap per file
TIMEOUT = 12  # seconds
IMG_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".avif"}

URL_REGEX = re.compile(
    r"""(?P<url>
        https?://
        [^\s"'<>)\]]+
    )""",
    re.VERBOSE | re.IGNORECASE,
)

def looks_like_image_url(url: str) -> bool:
    return any(urlparse(url).path.lower().endswith(ext) for ext in IMG_EXTS)

def clean_candidates(candidates):
    cleaned = []
    for raw in candidates:
        url = raw.rstrip('.,);\'">]')
        cleaned.extend(p.strip() for p in url.split(","))
    return cleaned

def unique_in_order(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x); out.append(x)
    return out

def head_is_image(url: str) -> bool:
    try:
        r = requests.head(url, allow_redirects=True, timeout=TIMEOUT)
        return r.headers.get("Content-Type", "").startswith("image/")
    except requests.RequestException:
        return False

def fetch_image(url: str):
    r = requests.get(url, stream=True, timeout=TIMEOUT)
    r.raise_for_status()
    buf, total = io.BytesIO(), 0
    for chunk in r.iter_content(8192):
        if not chunk: continue
        total += len(chunk)
        if total > MAX_BYTES:
            raise ValueError(f"File too large (> {MAX_BYTES // (1024*1024)} MB)")
        buf.write(chunk)
    buf.seek(0)
    name = urlparse(url).path.split("/")[-1] or "image"
    if "." not in name:
        ctype = r.headers.get("Content-Type", "")
        if ctype.startswith("image/"):
            name = f"image.{ctype.split('/')[-1].split(';')[0]}"
    return name, buf

st.set_page_config(page_title="anytext2images", page_icon="🖼️", layout="wide")
st.title("anytext2images")
st.caption("Paste any blob of text → Extract the images → Preview & Download = Fast")

with st.sidebar:
    st.header("Options")
    verify = st.checkbox("Verify via HEAD (slower, fewer false positives)", value=False)
    only_img_exts = st.checkbox("Filter by image extensions", value=True)
    st.write("Tip: turn on verification for CDN links without file extensions.")

blob = st.text_area("Paste text/HTML/logs", height=260, placeholder="Drop in your chaotic HTML or logs...")

col_a, col_b = st.columns([1, 3])
with col_a:
    run = st.button("Extract & Render", type="primary")

if run:
    raw_urls = [m.group("url") for m in URL_REGEX.finditer(blob)]
    candidates = unique_in_order(clean_candidates(raw_urls))

    urls = []
    for u in candidates:
        if only_img_exts and looks_like_image_url(u):
            urls.append(u)
        elif not only_img_exts:
            urls.append(u)

    if verify:
        urls = [u for u in urls if head_is_image(u)]

    st.subheader(f"Found {len(urls)} image URL{'s' if len(urls)!=1 else ''}")
    if not urls:
        st.info("No image URLs found. Tweak filters in the sidebar.")
    else:
        dl_all = []
        grid = st.columns(3)
        for i, url in enumerate(urls):
            with grid[i % 3]:
                st.write(f"**{i+1}.** {url}")
                try:
                    name, data = fetch_image(url)
                    st.image(data, use_column_width=True)
                    st.download_button(
                        "Download",
                        data=data.getvalue(),
                        file_name=name,
                        mime="application/octet-stream",
                        key=f"dl-{i}",
                    )
                    dl_all.append((name, data.getvalue()))
                except Exception as e:
                    st.warning(f"Preview/download failed: {e}")

        if dl_all:
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                existing = set()
                for name, bytes_ in dl_all:
                    base = name or "image"
                    final, k = base, 1
                    while final in existing:
                        parts = base.rsplit(".", 1)
                        final = f"{parts[0]}_{k}.{parts[1]}" if len(parts)==2 else f"{base}_{k}"
                        k += 1
                    existing.add(final)
                    zf.writestr(final, bytes_)
            zip_buf.seek(0)
            st.download_button(
                "Download All as ZIP",
                data=zip_buf.getvalue(),
                file_name="images.zip",
                mime="application/zip",
                type="primary",
            )

st.markdown("---")
st.caption("anytext2images — Built to simply work right out of the box.")
