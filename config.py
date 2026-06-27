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
SITE_TITLE = os.getenv("SITE_TITLE", "Smart Daily Tips").strip()
SITE_TAGLINE = os.getenv("SITE_TAGLINE", "Practical tips for everyday life").strip()

# The blog's niche - keeps content consistent (better for SEO).
NICHE = os.getenv(
    "NICHE",
    "practical how-to guides, tech & gadget tips, money-saving and online-earning "
    "tips, and useful everyday-life explainers for Indian readers",
)
