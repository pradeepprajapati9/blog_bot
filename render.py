"""Render articles + homepage to clean, SEO-friendly, AdSense-ready HTML."""
import html
import config

CSS = """
:root{--a:#1a73e8;--bg:#fff;--fg:#1f2328;--mut:#5b6470}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;
color:var(--fg);background:#f6f8fb;line-height:1.7}
.wrap{max-width:760px;margin:0 auto;padding:0 18px}
header.site{background:var(--a);color:#fff;padding:22px 0}
header.site a{color:#fff;text-decoration:none}
header.site h1{margin:0;font-size:22px}header.site p{margin:4px 0 0;opacity:.9;font-size:14px}
main{background:var(--bg);margin:18px auto;padding:26px;border-radius:12px;box-shadow:0 1px 6px rgba(0,0,0,.06)}
h1.title{font-size:30px;line-height:1.25;margin:.2em 0}
.meta{color:var(--mut);font-size:13px;margin-bottom:18px}
h2{font-size:22px;margin-top:1.6em}
.card{background:#fff;border-radius:10px;padding:18px;margin:12px 0;box-shadow:0 1px 5px rgba(0,0,0,.05)}
.card a{color:var(--a);text-decoration:none;font-weight:600;font-size:19px}
.card p{color:var(--mut);margin:.4em 0 0}
footer{color:var(--mut);text-align:center;padding:26px;font-size:13px}
a{color:var(--a)}
"""


def _ads_head():
    if not config.ADSENSE_CLIENT:
        return ""
    return (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/'
            f'adsbygoogle.js?client={config.ADSENSE_CLIENT}" crossorigin="anonymous"></script>')


def _head(title, description):
    return (
        f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)}</title>'
        f'<meta name="description" content="{html.escape(description)}">'
        f'{_ads_head()}<style>{CSS}</style></head><body>'
        f'<header class="site"><div class="wrap">'
        f'<a href="index.html"><h1>{html.escape(config.SITE_TITLE)}</h1></a>'
        f'<p>{html.escape(config.SITE_TAGLINE)}</p>'
        f'<p style="margin-top:8px"><a href="index.html">Home</a> &nbsp;|&nbsp; '
        f'<a href="tools/index.html">Free Tools &amp; Calculators</a></p>'
        f'</div></header>'
    )


FOOT = (f'<footer>&copy; {html.escape(config.SITE_TITLE)}. '
        f'For information purposes only.</footer></body></html>')


def article_page(art: dict, date_str: str) -> str:
    body = [f'<h1 class="title">{html.escape(art["title"])}</h1>',
            f'<div class="meta">{date_str}</div>',
            f'<p>{html.escape(art.get("intro",""))}</p>']
    for s in art["sections"]:
        if not isinstance(s, dict):
            continue
        h = s.get("heading") or s.get("title") or ""
        c = s.get("content") or s.get("text") or ""
        if not c:
            continue
        body.append(f'<h2>{html.escape(h)}</h2>')
        body.append(f'<p>{html.escape(c)}</p>')
    if art.get("conclusion"):
        body.append(f'<h2>Conclusion</h2><p>{html.escape(art["conclusion"])}</p>')
    body.append('<p style="margin-top:24px"><a href="index.html">&larr; More articles</a></p>')
    return _head(art["title"], art.get("meta_description", art["title"])) + \
        '<main class="wrap">' + "".join(body) + '</main>' + FOOT


def index_page(articles: list[dict]) -> str:
    cards = []
    for a in articles:                      # newest first (caller sorts)
        cards.append(
            f'<div class="card"><a href="{a["slug"]}.html">{html.escape(a["title"])}</a>'
            f'<p>{html.escape(a.get("meta_description",""))}</p>'
            f'<p style="font-size:12px">{a.get("date","")}</p></div>')
    return _head(config.SITE_TITLE, config.SITE_TAGLINE) + \
        '<main class="wrap"><h1 class="title">Latest Articles</h1>' + \
        ("".join(cards) or "<p>Articles coming soon...</p>") + '</main>' + FOOT
