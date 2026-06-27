"""Config for the auto-blog bot."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except Exception:
    pass

BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"          # GitHub Pages serves from /docs
STATE_FILE = BASE_DIR / "state.json"  # published articles list
DOCS_DIR.mkdir(exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
ADSENSE_CLIENT = os.getenv("ADSENSE_CLIENT", "").strip()
# Google Search Console verification (the 'content' value from its HTML-tag method).
GSC_VERIFY = os.getenv("GSC_VERIFY", "H3ZI_r2rt6CNxSW5c4c--3q8e1savcV4D6je3-FaqWc").strip()
# Google Analytics 4 Measurement ID (e.g. G-XXXXXXXXXX) to track traffic. Optional.
GA_ID = os.getenv("GA_ID", "").strip()
SITE_TITLE = os.getenv("SITE_TITLE", "Smart Daily Tips").strip()
SITE_TAGLINE = os.getenv("SITE_TAGLINE", "Practical tips for everyday life").strip()

# Public base URL (no trailing slash) - for canonical links, sitemap, OG tags.
SITE_URL = os.getenv("SITE_URL", "https://pradeepprajapati9.github.io/blog_bot").rstrip("/")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "prajapatipradeepkumar954@gmail.com").strip()
# Cross-promotion: link the assets to each other so they feed one audience.
YOUTUBE_URL = os.getenv("YOUTUBE_URL", "https://www.youtube.com/@Creati_Vity_99").strip()
TELEGRAM_URL = os.getenv("TELEGRAM_URL", "").strip()   # add your channel invite link

# ONE multi-niche blog: money/finance, tech, health, govt schemes, everyday how-to.
NICHE = os.getenv(
    "NICHE",
    "practical, accurate how-to guides for Indian readers across money & finance "
    "(loans, credit, savings, tax), tech & gadgets, health & fitness, government "
    "schemes & jobs, and everyday-life tips. Educational only - never specific "
    "investment, medical, or legal advice",
)
