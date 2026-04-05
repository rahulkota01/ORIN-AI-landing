import glob
import re

for fpath in glob.glob("*.html"):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Contact links
    content = content.replace('<a href="#">Contact</a>', '<a href="https://mail.google.com/mail/?view=cm&fs=1&to=orchestration.ro@gmail.com" target="_blank">Contact</a>')
    
    # 2. Make sure the early access form actually sends data
    # Need to add name="email" to the input so Formspree recognizes it
    content = content.replace('class="cta-input" placeholder="Enter your email" required>', 
                              'name="email" class="cta-input" placeholder="Enter your email" required>')
    
    # 3. Update the CTA Form JS to use fetch instead of mock
    old_js = """        document.getElementById('cta-form').addEventListener('submit', function (e) {
            e.preventDefault();
            this.style.display = 'none';
            document.getElementById('cta-success').style.display = 'block';
        });"""
        
    new_js = """        document.getElementById('cta-form').addEventListener('submit', function (e) {
            e.preventDefault();
            const form = e.target;
            fetch('https://formspree.io/f/xlgojgqb', {
                method: 'POST',
                body: new FormData(form),
                headers: { 'Accept': 'application/json' }
            }).then(() => {
                form.style.display = 'none';
                document.getElementById('cta-success').style.display = 'block';
            }).catch(() => alert("Something went wrong. Please try again."));
        });"""
        
    content = content.replace(old_js, new_js)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {fpath}")
