"""Find REAL search queries people type, via Google Autocomplete (free, no key).

This makes the blog demand-driven: we write articles that target actual searches
(long-tail keywords) instead of guessing topics -> better ranking + traffic.
"""
import json
import requests

# ONE blog, ALL niches. Add a niche = just add a few seeds here (no new repo!).
SEEDS = [
    # money & finance (high AdSense RPM)
    "how to save money", "how to get personal loan", "how to improve cibil score",
    "best credit card for", "how to save tax", "best investment for beginners",
    "how to earn money online", "best savings account",
    # tech & gadgets
    "best phone under", "best laptop under", "best earbuds under",
    "best smartwatch under", "how to fix phone", "best phone for",
    # health & fitness
    "how to lose weight", "home remedies for", "benefits of", "how to increase",
    "best exercise for", "foods to eat for",
    # government schemes & jobs (huge India search volume)
    "how to apply for", "government scheme for", "how to check", "how to download",
    "sarkari yojana", "how to get job in",
    # general how-to / everyday
    "how to", "what is", "best apps for", "how to make", "how to start",
]
UA = {"User-Agent": "Mozilla/5.0"}


def _suggest(query: str):
    """Return Google's autocomplete suggestions for a query (India, English)."""
    try:
        r = requests.get(
            "https://suggestqueries.google.com/complete/search",
            params={"client": "firefox", "q": query, "hl": "en", "gl": "in"},
            timeout=15, headers=UA,
        )
        return json.loads(r.text)[1]
    except Exception as ex:
        print(f"[keywords] suggest failed for '{query}': {ex}")
        return []


def get_keywords(limit: int = 60):
    """A de-duplicated pool of real search queries across all seeds."""
    pool, seen = [], set()
    for s in SEEDS:
        for k in _suggest(s):
            k = (k or "").strip()
            kl = k.lower()
            # keep useful, specific, India-relevant queries
            if k and kl not in seen and 15 <= len(k) <= 70:
                seen.add(kl)
                pool.append(k)
        if len(pool) >= limit:
            break
    return pool[:limit]


def pick_keyword(used_titles: list[str]):
    """Pick one real search query not already covered. Prefers longer-tail
    (more specific) queries - easier for a new blog to rank for."""
    used = [t.lower() for t in used_titles]
    # more words first = more specific / lower competition
    pool = sorted(get_keywords(80), key=lambda k: len(k.split()), reverse=True)
    for k in pool:
        kl = k.lower()
        if not any(kl in t or t in kl for t in used):
            print(f"[keywords] target search query: {k}")
            return k
    return None
