"""One-time: write style.css and switch ALL existing pages (which had inlined
CSS) to the shared external stylesheet, so the whole site gets the new theme."""
import re
import config
import render

render.write_css()
n = 0
for f in config.DOCS_DIR.rglob("*.html"):
    rel = "../" if f.parent.name == "tools" else ""
    t = f.read_text("utf-8")
    new = re.sub(r"<style>.*?</style>",
                 f'<link rel="stylesheet" href="{rel}style.css">', t, flags=re.S)
    if new != t:
        f.write_text(new, "utf-8")
        n += 1
print(f"restyled {n} pages + wrote style.css")
