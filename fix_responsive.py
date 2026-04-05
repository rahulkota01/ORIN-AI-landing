import glob, re

# CSS block to inject before </style> in each file
MOBILE_CSS = """
        /* ============================================
           FULL MOBILE / TABLET RESPONSIVE OVERHAUL
           ============================================ */

        /* Hamburger Button */
        .hamburger {
            display: none;
            flex-direction: column;
            gap: 5px;
            cursor: pointer;
            padding: 6px;
            background: none;
            border: none;
        }
        .hamburger span {
            display: block;
            width: 22px;
            height: 2px;
            background-color: var(--text-main, #1a1a1a);
            border-radius: 2px;
            transition: all 0.3s ease;
        }
        /* Mobile nav drawer */
        .mobile-nav-open .nav-links {
            display: flex !important;
        }

        /* ---- Tablet (≤ 992px) ---- */
        @media (max-width: 992px) {
            .hero-inner {
                flex-direction: column;
                gap: 32px;
            }
            .hero-left, .hero-center {
                width: 100%;
            }
            .hero-right { display: none; }
            .hero-center {
                height: 220px;
            }
            .opp-grid, .founding-team-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .wn-grid, .ask-grid {
                grid-template-columns: 1fr;
            }
            .pricing-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .problem-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .solution-list {
                grid-template-columns: 1fr;
            }
        }

        /* ---- Mobile (≤ 768px) ---- */
        @media (max-width: 768px) {
            /* Navbar */
            .nav-inner {
                height: auto;
                flex-wrap: nowrap;
                padding: 14px 0;
                position: relative;
            }
            .nav-logo-box {
                flex-grow: 1;
            }
            .hamburger {
                display: flex;
                order: 3;
            }
            .nav-links {
                display: none !important;
                flex-direction: column;
                width: 100%;
                order: 4;
                background: var(--bg-page, #F7F5F0);
                border-top: 1px solid var(--border, #E5E0D8);
                padding: 16px 0 8px;
                gap: 4px;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                z-index: 999;
                padding: 12px 24px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            }
            .nav-links.open {
                display: flex !important;
            }
            .nav-links a {
                padding: 10px 0;
                border-bottom: 1px solid var(--border, #E5E0D8);
                font-size: 15px;
            }
            .nav-links a:last-child { border-bottom: none; }
            .nav-right {
                order: 2;
                gap: 12px;
            }
            .btn-early {
                display: none;
            }

            /* Hero */
            .hero { padding: 80px 0 60px; }
            .hero-inner { flex-direction: column; gap: 24px; }
            .hero-left { width: 100%; }
            .hero-center { width: 100%; height: 180px; }
            .hero-desc { max-width: 100%; }
            .scroller-item.active { font-size: 40px; }
            .scroller-item.prev-1,
            .scroller-item.next-1,
            .scroller-item.prev-2,
            .scroller-item.next-2 { font-size: 32px; }

            /* Sections */
            .section-title, .cta-title, .hero-title { font-size: 36px !important; }
            .section-sub, .hero-sub { font-size: 15px; }
            .pt-title { font-size: 32px; }

            /* Grids */
            .problem-grid,
            .pricing-grid,
            .opp-grid,
            .wn-grid,
            .ask-grid,
            .founding-team-grid {
                grid-template-columns: 1fr;
            }
            .solution-list { grid-template-columns: 1fr; }

            /* Stats */
            .stats-row { flex-direction: column; gap: 32px; }
            .stat-divider { display: none; }
            .st-num { font-size: 48px; }

            /* CTA Form */
            .cta-form { flex-direction: column; align-items: stretch; }
            .cta-input { width: 100%; }
            .hero-actions { flex-direction: column; }
            .hero-actions a, .btn-hero { width: 100%; text-align: center; }

            /* Footer */
            .footer-top { flex-direction: column; gap: 32px; }
            .footer-links-grid { flex-wrap: wrap; gap: 32px; }
            .f-logo { font-size: 22px; }
            .fl-col { min-width: 40%; }

            /* Price cards */
            .price-card { padding: 28px 24px; }
            .ac-amount { font-size: 36px !important; }

            /* Ask cards */
            .ask-card { padding: 32px 24px; }

            /* Contact form */
            .contact-form { margin: 32px 16px 0; }

            /* Traction layout */
            .traction-layout { max-width: 100%; }
        }

        /* ---- Small phones (≤ 480px) ---- */
        @media (max-width: 480px) {
            .section-title, .cta-title, .hero-title { font-size: 28px !important; line-height: 1.2; }
            .btn-early { display: inline-block; font-size: 12px; padding: 8px 14px; }
            .scroller-item.active { font-size: 32px; }
            .hero { padding: 60px 0 40px; }
            .container { padding: 0 16px; }
        }
"""

# JS for hamburger toggle — to inject before </body>
HAMBURGER_JS = """
    <script>
        // Hamburger Menu Toggle
        const hamburger = document.getElementById('hamburger-btn');
        const navLinks = document.querySelector('.nav-links');
        if (hamburger && navLinks) {
            hamburger.addEventListener('click', function() {
                navLinks.classList.toggle('open');
                this.classList.toggle('active');
                const spans = this.querySelectorAll('span');
                if (this.classList.contains('active')) {
                    spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                    spans[1].style.opacity = '0';
                    spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
                } else {
                    spans[0].style.transform = '';
                    spans[1].style.opacity = '';
                    spans[2].style.transform = '';
                }
            });
            // Close menu on link click
            navLinks.querySelectorAll('a').forEach(a => {
                a.addEventListener('click', () => {
                    navLinks.classList.remove('open');
                    hamburger.classList.remove('active');
                    hamburger.querySelectorAll('span').forEach(s => s.style.transform = s.style.opacity = '');
                });
            });
        }
    </script>
"""

# Hamburger HTML to inject in navbar (before closing </div> of nav-inner)
HAMBURGER_HTML = '            <button class="hamburger" id="hamburger-btn" aria-label="Menu"><span></span><span></span><span></span></button>'

html_files = glob.glob("*.html")

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already added
    if 'hamburger-btn' in content:
        # Still update CSS and JS if needed
        pass
    else:
        # Remove old conflicting mobile CSS that was injected by previous scripts
        # (the nav-inner/nav-links blocks from fix_mobile_nav.py)
        old_nav_fix = """            .nav-inner {
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
        content = content.replace(old_nav_fix, "")

        # Add hamburger button into nav-inner before </div>
        # Find the nav-inner closing </div> that's just before </div></nav> pattern
        content = re.sub(
            r'(<div class="nav-right">.*?</div>)\s*(</div>\s*</nav>)',
            lambda m: m.group(1) + '\n' + HAMBURGER_HTML + '\n        ' + m.group(2),
            content,
            count=1,
            flags=re.DOTALL
        )

    # 1. Remove old @media blocks injected by our scripts to avoid duplicate
    # Only add MOBILE_CSS if not already present
    if '/* FULL MOBILE / TABLET RESPONSIVE OVERHAUL */' not in content:
        content = content.replace('</style>', MOBILE_CSS + '\n    </style>', 1)

    # 2. Add hamburger JS before </body>
    if 'Hamburger Menu Toggle' not in content:
        content = content.replace('</body>', HAMBURGER_JS + '\n</body>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Mobile-optimised: {fpath}")
