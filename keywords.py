"""Find REAL search queries people type, via Google Autocomplete (free, no key).

This makes the blog demand-driven: we write articles that target actual searches
(long-tail keywords) instead of guessing topics -> better ranking + traffic.
"""
import re
import json
import requests

# ONE blog, ALL niches. Add a niche = just add a few seeds here (no new repo!).
# NOTE: seeds are intentionally SAFE. We avoid "loan / earn money online / credit
# card / instant" style money seeds because Google Autocomplete expands them into
# scam-flavoured queries ("...without investment instant withdrawal", "...bad
# credit instant approval") that get the whole site flagged as a deceptive site.
# A hard safety filter (is_safe / BANNED below) is the real backstop.
SEEDS = [
    # personal finance — EDUCATIONAL & safe (no loans/earn-quick/credit-card)
    "how to save money", "how to save tax", "how to make a budget",
    "how to use upi", "what is mutual fund", "how to pay bills online",
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

# --- SAFETY: phrases that make Google flag a site as deceptive/scam/phishing, or
# that break AdSense policy. Any keyword OR generated article containing one of
# these is rejected before it can be published. This is what keeps the whole
# github.io domain (and every other bot on it) out of the "Dangerous site" list.
BANNED = [
    # get-rich / earn-quick scam language
    "earn money online", "earn money from", "make money online", "make money fast",
    "money online", "online earning", "earning app", "earning apps", "earn from home",
    "without investment", "no investment", "zero investment", "instant withdrawal",
    "instant payout", "instant cash", "quick money", "fast cash", "get rich",
    "double your money", "guaranteed income", "guaranteed return", "passive income app",
    "refer and earn", "paise kamao", "paise kaise kamaye",
    # loan / instant-credit scam language
    "personal loan", "instant loan", "instant approval", "loan without",
    "loan app", "payday loan", "loan from", "bad credit", "low credit score",
    "credit card for", "best credit card", "loan to pay off", "stop calling",
    # spammy "quick fix" credit-repair language
    "cibil score in one day", "cibil score in a day", "cibil in one day",
    "improve cibil score in", "increase cibil score fast",
    # other high-risk / policy-violating niches
    "crypto", "bitcoin", "forex", "betting", "gambling", "lottery", "casino",
    "dating", "adult", "hack", "cheat", "free recharge", "free fire diamond",
]


def is_safe(text: str) -> bool:
    """True only if `text` contains none of the deceptive/scam trigger phrases.
    Used both to reject risky search queries and to reject risky generated
    articles, so nothing that could get the site flagged ever gets published."""
    t = (text or "").lower()
    return not any(bad in t for bad in BANNED)


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
            # keep useful, specific, India-relevant queries — and SKIP anything
            # that trips the scam/deceptive filter so it can never be published.
            if k and kl not in seen and 15 <= len(k) <= 70 and is_safe(k):
                seen.add(kl)
                pool.append(k)
        if len(pool) >= limit:
            break
    return pool[:limit]


# Filler words that carry no topic meaning - ignored when comparing queries so
# that "how to get A PERSONAL loan with A low credit score" and "how to get
# personal loan with low credit score" are correctly seen as the SAME topic.
_STOP = {
    "how", "to", "a", "an", "the", "for", "of", "in", "on", "with", "without",
    "your", "you", "is", "are", "and", "or", "my", "me", "it", "at", "by",
    "best", "top", "guide", "india", "indian", "online", "free",
}


def _topic_words(text: str) -> set[str]:
    """The meaningful words of a query/title (lowercased, fillers removed)."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if w not in _STOP and len(w) > 2}


def _too_similar(cand: set[str], used_sets: list[set[str]]) -> bool:
    """True if `cand` shares most of its meaningful words with any past topic."""
    if not cand:
        return True
    for u in used_sets:
        if not u:
            continue
        overlap = len(cand & u)
        # near-identical topic if ~80%+ of the smaller set's words match
        if overlap and overlap / min(len(cand), len(u)) >= 0.8:
            return True
    return False


def pick_keyword(used_titles: list[str]):
    """Pick one real search query not already covered. Prefers longer-tail
    (more specific) queries - easier for a new blog to rank for."""
    used_sets = [_topic_words(t) for t in used_titles]
    # more words first = more specific / lower competition
    pool = sorted(get_keywords(80), key=lambda k: len(k.split()), reverse=True)
    for k in pool:
        if not _too_similar(_topic_words(k), used_sets):
            print(f"[keywords] target search query: {k}")
            return k
    print("[keywords] every fresh query already covered; letting Gemini pick.")
    return None
