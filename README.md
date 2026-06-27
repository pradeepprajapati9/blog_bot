# 📝 Auto Blog Bot (free, AdSense income)

Gemini writes one SEO article per run and publishes it to `/docs`, served free by
**GitHub Pages**. Over ~6-12 months the articles rank on Google and earn passive
**AdSense** ad revenue. Fully automated, no server, no cost.

## How it works
```
pick a high-demand SEO topic -> Gemini writes the article -> render HTML
-> update homepage -> commit to /docs -> GitHub Pages serves it live
```

## Setup
1. Push this folder to a GitHub repo (e.g. `blog`).
2. Repo **Settings -> Pages** -> Source: **Deploy from a branch** -> Branch: `main` `/docs` -> Save.
   Your blog goes live at `https://<username>.github.io/<repo>/`.
3. Add Actions secret **GEMINI_API_KEY**. (Optional: **ADSENSE_CLIENT** after AdSense approval.)
4. (Optional) Repo **Settings -> Secrets and variables -> Actions -> Variables**:
   `SITE_TITLE`, `SITE_TAGLINE`.
5. `.github/workflows/blog.yml` then auto-posts 2 articles/day.

## AdSense (the income part) - later
- Let the blog build up ~20-30 articles + some weeks of age first.
- Apply at https://adsense.google.com with your `*.github.io` blog URL.
- After approval, add your `ca-pub-...` id as the `ADSENSE_CLIENT` secret.
  Auto-ads then appear on every page and start earning.

## Local test
```powershell
copy .env.example .env   # add GEMINI_API_KEY
pip install -r requirements.txt
python main.py           # writes one article into /docs
```

> Keep content genuinely useful (it already is) - Google rewards helpful content
> and AdSense rejects low-effort spam.
