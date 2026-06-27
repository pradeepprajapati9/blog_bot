"""Pick an SEO topic and write a full article with Gemini (free, resilient)."""
import re
import json
import time
import requests
import config

MODELS = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-flash-lite"]


def _gemini(prompt: str) -> str:
    if not config.GEMINI_API_KEY:
        return ""
    for attempt in range(2):
        for model in MODELS:
            url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                   f"{model}:generateContent?key={config.GEMINI_API_KEY}")
            try:
                r = requests.post(url, timeout=90,
                                  json={"contents": [{"parts": [{"text": prompt}]}]})
                if r.status_code == 200:
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
                if r.status_code in (429, 503):
                    continue
                print(f"[writer] {model} http {r.status_code}: {r.text[:120]}")
            except Exception as ex:
                print(f"[writer] {model} error: {ex}")
        if attempt == 0:
            time.sleep(3)
    return ""


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:70] or "post"


def write_article(used_titles: list[str], target: str = "") -> dict | None:
    avoid = "; ".join(used_titles[-60:]) or "none yet"
    if target:
        topic_line = (
            f"Write an article that will RANK on Google for this exact search query "
            f"that real people type: '{target}'. The title should closely match the "
            f"search query (natural, under 65 chars), and the article must fully and "
            f"directly answer that search intent.\n")
    else:
        topic_line = (
            f"Pick ONE fresh, high-search-demand article topic (a real thing people "
            f"Google). Do NOT repeat or resemble these existing posts: {avoid}.\n")
    prompt = (
        f"You are an SEO content writer for a blog about: {config.NICHE}.\n"
        f"{topic_line}"
        f"Write a genuinely useful, original article.\n"
        f"Return ONLY valid JSON, no markdown:\n"
        f'{{"title": "...", "meta_description": "...", "intro": "...", '
        f'"sections": [{{"heading": "...", "content": "..."}}], "conclusion": "..."}}\n'
        f"Rules: title = clear, SEO-friendly, under 65 chars. meta_description = 140-155 "
        f"chars. 5-7 sections, each 120-200 words of practical, accurate, helpful info "
        f"with concrete details (no fluff, no fake stats). Friendly, simple English. "
        f"Plain text only (no markdown, no links)."
    )
    raw = _gemini(prompt)
    if not raw:
        return None
    try:
        raw = raw[raw.find("{"): raw.rfind("}") + 1]
        raw = re.sub(r",\s*([}\]])", r"\1", raw)   # strip trailing commas
        art = json.loads(raw)
        if art.get("title") and art.get("sections"):
            art["slug"] = slugify(art["title"])
            return art
    except Exception as ex:
        print(f"[writer] JSON parse failed: {ex}")
    return None
