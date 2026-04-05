import glob

css_fix = """
        @media (max-width: 768px) {
            .nav-inner {
                flex-wrap: wrap;
                height: auto;
                padding: 16px 0;
                gap: 16px;
            }
            .nav-logo-box {
                flex-grow: 1;
            }
            .nav-links {
                display: flex !important;
                flex-wrap: wrap;
                gap: 16px;
                order: 3;
                width: 100%;
                justify-content: center;
                border-top: 1px solid var(--border);
                padding-top: 16px;
                font-size: 13px;
            }
            .nav-links a.active {
                padding-bottom: 8px;
                top: 0;
            }
            .nav-right {
                order: 2;
            }
            /* ... other 768px rules retain here ... */
"""

for fpath in glob.glob("*.html"):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The existing code has `.nav-links { display: none; }` inside `@media (max-width: 768px) {`
    # We will carefully patch it.
    
    if ".nav-links {\n                display: none;\n            }" in content:
        replacement = """
            .nav-inner {
                flex-wrap: wrap;
                height: auto;
                padding: 16px 0;
                gap: 16px;
            }
            .nav-logo-box {
                flex-grow: 1;
            }
            .nav-links {
                display: flex;
                flex-wrap: wrap;
                gap: 16px;
                order: 3;
                width: 100%;
                justify-content: center;
                border-top: 1px solid var(--border);
                padding-top: 16px;
            }
            .nav-right {
                order: 2;
            }
        """
        content = content.replace(".nav-links {\n                display: none;\n            }", replacement)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed mobile nav in {fpath}")

