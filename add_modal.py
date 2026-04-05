import os
import glob

css = """
        /* Sign In Modal */
        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
            display: none; align-items: center; justify-content: center; z-index: 2000;
            opacity: 0; transition: opacity 0.3s;
        }
        .modal-overlay.show { display: flex; opacity: 1; }
        .modal-content {
            background: var(--bg-page, #F7F5F0); padding: 40px; border-radius: 12px;
            text-align: center; max-width: 400px; position: relative;
            transform: translateY(20px); transition: transform 0.3s;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .modal-overlay.show .modal-content { transform: translateY(0); }
        .modal-close {
            position: absolute; top: 12px; right: 16px; font-size: 24px;
            cursor: pointer; color: var(--text-sec, #6B7280);
        }
        .spinner {
            width: 40px; height: 40px; border: 3px solid rgba(0,0,0,0.1);
            border-top: 3px solid var(--accent, #4A90D9); border-radius: 50%;
            animation: spin 1s linear infinite; margin: 0 auto 24px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .modal-title { font-family: var(--font-head, 'DM Serif Display', serif); font-size: 24px; color: var(--text-main, #1a1a1a); margin-bottom: 12px; }
        .modal-text { font-family: var(--font-body, 'Inter', sans-serif); font-size: 15px; color: var(--text-sec, #6B7280); line-height: 1.6; }
"""

html = """
    <!-- Sign In Modal -->
    <div id="signin-modal" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-close">&times;</div>
            <div class="spinner"></div>
            <div class="modal-title">Access Restricted</div>
            <div class="modal-text">We are currently providing early access to a select group of researchers. Please email the team to request access, or wait for the official public announcement.</div>
            <a href="mailto:orchestration.ro@gmail.com" class="btn-early" style="display:inline-block; margin-top:24px;">Email Team ORIN</a>
        </div>
    </div>
"""

js = """
        // Sign In Modal Logic
        document.querySelectorAll('.btn-signin').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const modal = document.getElementById('signin-modal');
                if(!modal) return;
                modal.style.display = 'flex';
                // Trigger reflow
                void modal.offsetWidth;
                modal.classList.add('show');
            });
        });
        
        const modalClose = document.querySelector('.modal-close');
        if(modalClose) {
            modalClose.addEventListener('click', function() {
                const modal = document.getElementById('signin-modal');
                modal.classList.remove('show');
                setTimeout(() => modal.style.display = 'none', 300);
            });
        }
        
        const signinModal = document.getElementById('signin-modal');
        if(signinModal) {
            signinModal.addEventListener('click', function(e) {
                if(e.target === this) {
                    this.classList.remove('show');
                    setTimeout(() => this.style.display = 'none', 300);
                }
            });
        }
"""

html_files = glob.glob("*.html")

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already added
    if 'id="signin-modal"' in content:
        continue

    # Insert CSS before </style>
    content = content.replace("</style>", css + "\n    </style>", 1)

    # Insert HTML after <body>
    content = content.replace("<body>", "<body>\n" + html, 1)

    # Insert JS before </body>
    content = content.replace("</body>", js + "\n</body>", 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {fpath}")
