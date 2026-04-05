import os
import glob
import re

html_files = glob.glob("*.html")

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "        // Sign In Modal Logic" in content and "<script>\n        // Sign In Modal Logic" not in content:
        content = content.replace("        // Sign In Modal Logic", "    <script>\n        // Sign In Modal Logic")
        
        # Replace the bit before </body>
        # It looks like:
        #             });
        #         }
        # 
        # </body>
        
        content = content.replace("            });\n        }\n\n</body>", "            });\n        }\n    </script>\n</body>")
        content = content.replace("            });\n        }\n</body>", "            });\n        }\n    </script>\n</body>")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {fpath}")
