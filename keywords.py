"""Find REAL search queries people type, via Google Autocomplete (free, no key).

This makes the blog demand-driven: we write articles that target actual searches
(long-tail keywords) instead of guessing topics -> better ranking + traffic.
"""
import json
import requests

# Niche-relevant seeds; Google expands each into real long-tail searches.
SEEDS = [
    "how to save money", "how to earn money online", "how to reduce electricity bill",
    "best phone under", "best laptop under", "best earphones under",
    "how to improve", "how to apply for", "how to check", "how to download",
    "how to make money", "what is", "how to start", "best apps for",
    "how to get", "government scheme for", "how to invest", "how to increase",
    "online earning app", "how to book", "how to link", "how to activate",
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
