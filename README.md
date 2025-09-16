# anytext2images
**Any blob of text → Extract images → Preview & download = Fast**

Turn any blob of text into a gallery of images, then download what you want.  
Paste messy HTML, logs, or random snippets containing URLs — `anytext2images` finds the image links, previews them, and lets you download them individually or all at once as a ZIP.

---

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Why?
Because sometimes you’re buried in a wall of garbage HTML, and all you want are the damn images.

<img width="800" height="800" alt="Screenshot 2025-09-16 at 2 39 04 PM" src="https://github.com/user-attachments/assets/be51a739-9c7a-4e19-9f2f-238aff8cbfe5" />
---

## Features
- **Streamlit UI** – paste text and instantly see images in a clean grid  
- **One-click downloads** – save individual images or grab everything in a ZIP  
- **CLI tool** – extract image URLs or bulk download them without leaving the terminal  
- **Smart parsing** – handles messy HTML, `srcset` attributes, and weird trailing punctuation  
- **Filters & safety** – optional file-extension filtering, optional `HEAD` verification, and a per-file size cap  
- **Zero config** – no database, no API keys, no secrets. Just works  

---

## Quick Start

```bash
# clone and install
git clone https://github.com/aiwebautomation/anytext2images.git
cd anytext2images
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# launch UI
streamlit run app.py

Open http://localhost:8501
 and paste your blob.

## CLI Usage
# extract and download images to ZIP
python cli.py -i input.txt -o images.zip

# print URLs only (no download)
python cli.py -i input.txt --print-urls

# skip extension filter (for CDN links without file extensions)
python cli.py -i input.txt --no-ext-filter


## Troubleshooting:
11k+ files staged after install: you created .venv inside the repo. Add .venv/ to .gitignore, then:
 git rm -r --cached .
 git add .
 git commit -m "fix: ignore venv"


 No images found: disable filter by extension or enable HEAD verification in the sidebar (some CDNs hide extensions).

 403/blocked previews: some hosts disallow hotlinking or HEAD. Toggle verification off or use CLI.

 Huge downloads: raise MAX_BYTES in app.py.

Known Limitations
Hotlinking may fail on domains that block external previews.

Some srcset URLs are device/width-specific and won’t resolve directly.

HEAD verification can be blocked; use GET or disable verification.

This is a text parser, not a crawler: it won’t find images that aren’t present in your pasted text.

##Disclaimer
This tool is for personal and educational use.
It does not bypass paywalls or access protected content.
Respect site terms and copyright — you’re responsible for how you use downloaded images.
