"""Generate the supporting pieces a real, monetizable site needs:
Privacy Policy / About / Contact (AdSense requires these), favicon, sitemap.xml,
robots.txt. Called by main.py every run.
"""
import config
import render

U = config.SITE_URL
EMAIL = config.CONTACT_EMAIL


def _page(slug, title, desc, body_html):
    canonical = f"{U}/{slug}.html"
    html = (render._head(title, desc, canonical) +
            f'<main class="wrap"><h1 class="title">{title}</h1>{body_html}</main>' +
            render.FOOT)
    (config.DOCS_DIR / f"{slug}.html").write_text(html, "utf-8")


def write_pages():
    _page("privacy", f"Privacy Policy - {config.SITE_TITLE}",
          "Privacy policy: how this site uses cookies and third-party advertising.",
          f"""
<p>Your privacy is important to us. This page explains how {config.SITE_TITLE}
handles information when you visit our website.</p>
<h2>Cookies</h2>
<p>This site uses cookies to improve your experience. You can disable cookies in
your browser settings at any time.</p>
<h2>Advertising &amp; Google AdSense</h2>
<p>We may use third-party advertising companies, including Google AdSense, to
serve ads when you visit our site. Google, as a third-party vendor, uses cookies
(including the DART cookie) to serve ads based on your visits to this and other
websites. You may opt out of personalised advertising by visiting
<a href="https://www.google.com/settings/ads">Google Ads Settings</a>.</p>
<h2>Third-Party Vendors</h2>
<p>Third-party vendors and ad networks may use cookies and web beacons to collect
non-personally identifiable information for ad personalisation and measurement.
We do not control these third-party cookies.</p>
<h2>External Links</h2>
<p>Our articles may link to external sites. We are not responsible for the
content or privacy practices of those sites.</p>
<h2>Consent</h2>
<p>By using this website, you consent to this privacy policy.</p>
<h2>Contact</h2>
<p>Questions? Email us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>""")

    _page("about", f"About - {config.SITE_TITLE}",
          f"About {config.SITE_TITLE} - practical, accurate guides for Indian readers.",
          f"""
<p>{config.SITE_TITLE} is an independent blog that publishes practical, easy-to-follow
guides on money &amp; finance, technology, health, government schemes and everyday
life - written specially for Indian readers.</p>
<p>Our goal is simple: give you clear, accurate, useful information that actually
helps in real life - no jargon, no fluff. We also offer free
<a href="{U}/tools/index.html">online calculators and tools</a>.</p>
<p>All content is for information and education only and is not professional
financial, medical, or legal advice. Always verify details and consult a qualified
professional before making important decisions.</p>
<p>Run by Pradeep Pk. Reach us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>""")

    _page("contact", f"Contact - {config.SITE_TITLE}",
          f"Contact {config.SITE_TITLE}.",
          f"""
<p>We'd love to hear from you - feedback, suggestions, corrections, or
partnership enquiries.</p>
<p><b>Email:</b> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>We usually reply within a few days.</p>""")


def write_favicon():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
           '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
           '<stop offset="0" stop-color="#6366f1"/><stop offset="1" stop-color="#ec4899"/>'
           '</linearGradient></defs><rect width="64" height="64" rx="14" fill="url(#g)"/>'
           f'<text x="32" y="44" font-size="38" font-family="Arial" font-weight="bold" '
           f'text-anchor="middle" fill="#fff">{config.SITE_TITLE[:1]}</text></svg>')
    (config.DOCS_DIR / "favicon.svg").write_text(svg, "utf-8")


def write_sitemap(articles):
    urls = [f"{U}/", f"{U}/about.html", f"{U}/contact.html", f"{U}/privacy.html",
            f"{U}/tools/index.html"]
    urls += [f"{U}/tools/{s}.html" for s in
             ("emi-calculator", "sip-calculator", "age-calculator",
              "gst-calculator", "percentage-calculator")]
    urls += [f'{U}/{a["slug"]}.html' for a in articles]
    body = "".join(f"<url><loc>{u}</loc></url>" for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           f'{body}</urlset>')
    (config.DOCS_DIR / "sitemap.xml").write_text(xml, "utf-8")


def write_robots():
    (config.DOCS_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {U}/sitemap.xml\n", "utf-8")


def write_all(articles):
    write_pages()
    write_favicon()
    write_sitemap(articles)
    write_robots()
