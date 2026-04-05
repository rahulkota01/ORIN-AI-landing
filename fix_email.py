import os
import glob

html_files = glob.glob("*.html")

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the mailto with a Gmail compose URL to ensure it always opens
    if 'href="mailto:orchestration.ro@gmail.com"' in content:
        content = content.replace('href="mailto:orchestration.ro@gmail.com"', 'href="https://mail.google.com/mail/?view=cm&fs=1&to=orchestration.ro@gmail.com" target="_blank"')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed email link in {fpath}")
