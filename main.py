"""Auto-blog bot: writes one SEO article per run and publishes to /docs
(served free by GitHub Pages). Run daily via GitHub Actions.

  pick fresh topic -> Gemini writes article -> render HTML -> update homepage
"""
import sys
import json
import traceback
from datetime import datetime

import config
import writer
import render
import keywords

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _load():
    if config.STATE_FILE.exists():
        try:
            return json.loads(config.STATE_FILE.read_text("utf-8"))
        except Exception:
            pass
    return {"articles": []}


def _save(data):
    config.STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


def run():
    render.write_css()      # keep the shared theme (style.css) up to date
    data = _load()
    used = [a["title"] for a in data["articles"]]
    print(f"[blog] {len(used)} articles so far; writing a new one...")

    # demand-driven: target a REAL Google search query (falls back to Gemini's pick)
    target = keywords.pick_keyword(used) or ""
    art = writer.write_article(used, target)
    if not art:
        print("[blog] could not generate an article (Gemini issue). Try again later.")
        return

    date_str = datetime.now().strftime("%d %b %Y")
    # avoid slug collisions
    slug = art["slug"]
    existing = {a["slug"] for a in data["articles"]}
    if slug in existing:
        slug = f"{slug}-{len(data['articles'])+1}"
    art["slug"] = slug

    # write the article page
    (config.DOCS_DIR / f"{slug}.html").write_text(
        render.article_page(art, date_str), "utf-8")

    # record + rebuild homepage (newest first)
    data["articles"].append({
        "title": art["title"], "slug": slug,
        "meta_description": art.get("meta_description", ""), "date": date_str,
    })
    ordered = list(reversed(data["articles"]))
    (config.DOCS_DIR / "index.html").write_text(render.index_page(ordered), "utf-8")
    _save(data)

    print(f"[blog] published: {art['title']}")
    print(f"[blog] total articles: {len(data['articles'])}")


if __name__ == "__main__":
    try:
        run()
    except Exception:
        print("ERROR:\n" + traceback.format_exc())
        sys.exit(1)
