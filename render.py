"""Render articles + homepage to clean, modern, AdSense-ready HTML.

CSS lives in an external docs/style.css (write_css) so the whole site - every
page, old and new - shares one beautiful theme; edit once, all pages update.
"""
import html
import json
import config

# Modern gradient theme.
CSS = """
:root{--grad:linear-gradient(135deg,#6366f1 0%,#8b5cf6 50%,#ec4899 100%);
--accent:#6366f1;--bg:#f6f7fc;--card:#fff;--fg:#1e2330;--mut:#6b7280;--line:#eceef3}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:'Segoe UI',system-ui,-apple-system,Roboto,Arial,sans-serif;
color:var(--fg);background:var(--bg);line-height:1.75;font-size:17px}
.wrap{max-width:780px;margin:0 auto;padding:0 18px}
header.site{background:var(--grad);color:#fff;padding:34px 0 32px;
box-shadow:0 6px 24px rgba(99,102,241,.28)}
header.site a{color:#fff;text-decoration:none}
header.site h1{margin:0;font-size:27px;font-weight:800;letter-spacing:-.5px}
header.site .tag{margin:6px 0 0;opacity:.92;font-size:15px}
header.site nav{margin-top:15px}
header.site nav a{background:rgba(255,255,255,.18);padding:7px 15px;border-radius:20px;
margin-right:8px;display:inline-block;font-size:14px;font-weight:600}
header.site nav a:hover{background:rgba(255,255,255,.32)}
main{background:var(--card);margin:-20px auto 24px;padding:34px;border-radius:18px;
box-shadow:0 10px 34px rgba(30,35,48,.09)}
h1.title{font-size:32px;line-height:1.25;margin:.1em 0 .3em;font-weight:800;letter-spacing:-.5px}
.meta{color:var(--mut);font-size:14px;margin-bottom:22px;border-bottom:1px solid var(--line);
padding-bottom:14px}
h2{font-size:23px;margin-top:1.7em;font-weight:700;background:var(--grad);
-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
p{margin:.7em 0}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.card{background:var(--card);border-radius:14px;padding:20px 22px;margin:14px 0;
box-shadow:0 3px 14px rgba(30,35,48,.07);border-left:4px solid transparent;
transition:transform .15s,box-shadow .15s,border-color .15s}
.card:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(99,102,241,.18);
border-left-color:var(--accent)}
.card a{font-weight:700;font-size:20px;color:var(--fg)}
.card a:hover{color:var(--accent);text-decoration:none}
.card p{color:var(--mut);margin:.5em 0 0;font-size:15px}
footer{color:var(--mut);text-align:center;padding:30px;font-size:13px}
.tool label{display:block;margin:16px 0 6px;font-weight:600;font-size:15px}
.tool input,.tool select{width:100%;padding:13px;font-size:16px;border:1.5px solid #d8dce6;
border-radius:10px;background:#fbfcfe}
.tool input:focus,.tool select:focus{outline:none;border-color:var(--accent);
box-shadow:0 0 0 3px rgba(99,102,241,.15)}
.tool button{margin-top:22px;width:100%;padding:15px;font-size:17px;font-weight:700;
background:var(--grad);color:#fff;border:0;border-radius:12px;cursor:pointer;
box-shadow:0 6px 18px rgba(99,102,241,.35);transition:transform .12s}
.tool button:hover{transform:translateY(-2px)}
.result{margin-top:24px;padding:22px;background:linear-gradient(135deg,#eef2ff,#fbf0fb);
border-radius:14px;font-size:17px;border:1px solid #e6e9f5}
.result b{font-size:26px;background:var(--grad);-webkit-background-clip:text;
background-clip:text;-webkit-text-fill-color:transparent;font-weight:800}
.row{display:flex;gap:14px}.row>div{flex:1}
@media(max-width:560px){h1.title{font-size:26px}main{padding:22px;border-radius:14px;margin-top:-14px}}
"""


def write_css():
    (config.DOCS_DIR / "style.css").write_text(CSS, "utf-8")


def _ads_head():
    if not config.ADSENSE_CLIENT:
        return ""
    return (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/'
            f'adsbygoogle.js?client={config.ADSENSE_CLIENT}" crossorigin="anonymous"></script>')


def _ga():
    if not config.GA_ID:
        return ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id='
            f'{config.GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];'
            f'function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());'
            f'gtag("config","{config.GA_ID}");</script>')


def _head(title, description, canonical=None, css_path="style.css",
          home="index.html", tools="tools/index.html"):
    canonical = canonical or (config.SITE_URL + "/")
    t, d = html.escape(title), html.escape(description)
    return (
        f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{t}</title><meta name="description" content="{d}">'
        + (f'<meta name="google-site-verification" content="{config.GSC_VERIFY}">'
           if config.GSC_VERIFY else "") +
        f'<link rel="canonical" href="{canonical}">'
        f'<link rel="icon" type="image/svg+xml" href="{config.SITE_URL}/favicon.svg">'
        f'<meta property="og:title" content="{t}">'
        f'<meta property="og:description" content="{d}">'
        f'<meta property="og:type" content="website">'
        f'<meta property="og:url" content="{canonical}">'
        f'<meta name="twitter:card" content="summary">'
        f'<link rel="stylesheet" href="{css_path}">{_ga()}{_ads_head()}</head><body>'
        f'<header class="site"><div class="wrap">'
        f'<a href="{home}"><h1>{html.escape(config.SITE_TITLE)}</h1></a>'
        f'<p class="tag">{html.escape(config.SITE_TAGLINE)}</p>'
        f'<nav><a href="{home}">Home</a><a href="{tools}">Free Tools</a></nav>'
        f'</div></header>'
    )


def _footer():
    u = config.SITE_URL
    links = [f'<a href="{u}/about.html">About</a>',
             f'<a href="{u}/contact.html">Contact</a>',
             f'<a href="{u}/privacy.html">Privacy Policy</a>']
    follow = []
    if config.YOUTUBE_URL:
        follow.append(f'<a href="{config.YOUTUBE_URL}">YouTube</a>')
    if config.TELEGRAM_URL:
        follow.append(f'<a href="{config.TELEGRAM_URL}">Telegram</a>')
    foll = (" &middot; Follow: " + " ".join(follow)) if follow else ""
    return (f'<footer><p>{" &middot; ".join(links)}{foll}</p>'
            f'<p>&copy; {html.escape(config.SITE_TITLE)}. For information purposes only; '
            f'not professional advice.</p></footer></body></html>')


FOOT = _footer()


def article_page(art: dict, date_str: str, related: list[dict] | None = None) -> str:
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
        body.append(f'<h2>{html.escape(h)}</h2><p>{html.escape(c)}</p>')
    if art.get("conclusion"):
        body.append(f'<h2>Conclusion</h2><p>{html.escape(art["conclusion"])}</p>')
    if related:
        items = "".join(
            f'<div class="card"><a href="{r["slug"]}.html">{html.escape(r["title"])}</a></div>'
            for r in related)
        body.append(f'<h2>Related Articles</h2>{items}')
    body.append('<p style="margin-top:24px"><a href="index.html">&larr; More articles</a></p>')
    canonical = f'{config.SITE_URL}/{art["slug"]}.html'
    schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": art["title"], "description": art.get("meta_description", ""),
        "author": {"@type": "Person", "name": "Pradeep Pk"},
        "publisher": {"@type": "Organization", "name": config.SITE_TITLE},
        "mainEntityOfPage": canonical, "datePublished": date_str,
    }
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>'
    return _head(art["title"], art.get("meta_description", art["title"]), canonical) + \
        '<main class="wrap">' + "".join(body) + '</main>' + ld + FOOT


def index_page(articles: list[dict]) -> str:
    cards = []
    for a in articles:
        cards.append(
            f'<div class="card"><a href="{a["slug"]}.html">{html.escape(a["title"])}</a>'
            f'<p>{html.escape(a.get("meta_description",""))}</p>'
            f'<p style="font-size:12px">{a.get("date","")}</p></div>')
    return _head(config.SITE_TITLE, config.SITE_TAGLINE) + \
        '<main class="wrap"><h1 class="title">Latest Articles</h1>' + \
        ("".join(cards) or "<p>Articles coming soon...</p>") + '</main>' + FOOT
