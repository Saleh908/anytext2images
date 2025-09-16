# anytext2images
Any blob of text → Extract the images → Preview & download = Fast

Turn any blob of text into a gallery of images then download what you want.
Paste messy HTML, logs, or random snippets containing URLs — anytext2images finds the image links, previews them, and lets you download them individually or all at once as a ZIP.
<img width="800" height="800" alt="Screenshot 2025-09-16 at 2 39 04 PM" src="https://github.com/user-attachments/assets/be51a739-9c7a-4e19-9f2f-238aff8cbfe5" />

# Why?
Because sometimes you’re buried in a wall of garbage HTML, and all you want are the damn images.

Features
Streamlit UI – paste text and instantly see images in a clean grid.
One-click downloads – save individual images or grab everything in a ZIP.
CLI tool – extract image URLs or bulk download them without leaving the terminal.
Smart parsing – handles messy HTML, srcset attributes, and weird trailing punctuation.
Filters & safety – optional file-extension filtering, optional HEAD verification, and a per-file size cap.
Zero config – no database, no API keys, no secrets. Just works.



Quick Start
# clone and install
git clone https://github.com/aiwebautomation/anytext2images.git

cd anytext2images

python3 -m venv .venv && source .venv/bin/activate

pip install -r requirements.txt

# launch UI
streamlit run app.py

Open http://localhost:8501 and paste your blob.

CLI Usage
python cli.py -i input.txt -o images.zip
python cli.py -i input.txt --print-urls

## Disclaimer
This tool is for personal and educational use only. It does not bypass paywalls or access protected content.  
Be mindful of copyright and terms of service when downloading or reusing images.
