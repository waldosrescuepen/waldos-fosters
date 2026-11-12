#!/usr/bin/env python3
"""Render docs/index.html (the GitHub Pages site) from dogs.json.

Usage:  python3 build.py
Each dog in dogs.json:
  name, aka (optional nickname), photo (docs-relative path or full https URL),
  badge (e.g. "Foster needed by 11/8"), urgent (true = orange badge),
  tags (list of short strings), bio, petstablished_id (optional),
  name_split (optional: where the name switches to teal, default = half).
"""
import datetime
import html
import json
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
data = json.loads((ROOT / "dogs.json").read_text())
e = html.escape


def photo_url(p):
    if p.startswith("http"):
        return p
    site = data.get("site_url", "").rstrip("/")
    return f"{site}/{p}" if site else p


def card(d):
    name = d["name"]
    k = d.get("name_split") or (len(name) + 1) // 2
    aka = f' <small>({e(d["aka"])})</small>' if d.get("aka") else ""
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in d.get("tags", []))
    badge = ""
    if d.get("badge"):
        cls = "badge urgent" if d.get("urgent") else "badge"
        badge = f'<span class="{cls}">{e(d["badge"])}</span>'
    email = d.get("apply_email") or data["apply_email"]
    subject = urllib.parse.quote(f"Foster application: {name}")
    body = urllib.parse.quote(f"Hi Andi,\n\nI'd like to foster {name}. A bit about me and my home:\n\n")
    apply = f"mailto:{email}?subject={subject}&body={body}"
    return f"""<article class="card">
<div class="photo"><img src="{e(d['photo'])}" alt="{e(name)}" loading="lazy">{badge}</div>
<div class="body"><h2><span class="w">{e(name[:k])}</span><span class="t">{e(name[k:])}</span>{aka}</h2>
<div class="tags">{tags}</div><p>{e(d['bio'])}</p>
<a class="cta" href="{e(apply)}">Apply to Foster {e(name)}</a></div></article>"""


dogs = data["dogs"]
n = len(dogs)
og_img = photo_url(dogs[0]["photo"]) if dogs else ""
updated = datetime.date.today().strftime("%B %-d, %Y")
desc = f"{n} Waldo's Rescue Pen dog{'s' if n != 1 else ''} who need a foster home now."
cards = "\n".join(card(d) for d in dogs) or '<p class="empty">All our dogs are in foster homes right now. Check back soon!</p>'

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(data['title'])} | Waldo's Rescue Pen</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(data['title'])} | Waldo's Rescue Pen">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{e(og_img)}">
<meta property="og:type" content="website">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0d1a19;--card:#13262a;--teal:#40a9a0;--orange:#E8724A;--text:#e9f1f0;--muted:#a9bdbb}}
*{{box-sizing:border-box}}html{{background:var(--bg);color-scheme:dark}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:'DM Sans',system-ui,sans-serif;line-height:1.55}}
header{{text-align:center;padding:40px 16px 8px}}
header .kick{{color:var(--teal);letter-spacing:.18em;font-size:13px;font-weight:700;text-transform:uppercase}}
header h1{{font-family:'Playfair Display',serif;font-size:clamp(34px,7vw,56px);margin:8px 0}}header h1 span{{color:var(--teal)}}
header p{{color:var(--muted);max-width:620px;margin:0 auto}}
main{{max-width:800px;margin:0 auto;padding:24px 16px 48px;display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(min(310px,100%),1fr))}}
.card{{background:var(--card);border-radius:20px;overflow:hidden;display:flex;flex-direction:column;border:1px solid rgba(64,169,160,.25)}}
.photo{{position:relative;aspect-ratio:3/4}}.photo img{{width:100%;height:100%;object-fit:cover;display:block}}
.photo::after{{content:"";position:absolute;inset:auto 0 0 0;height:30%;background:linear-gradient(transparent,var(--card))}}
.badge{{position:absolute;top:14px;left:14px;z-index:1;background:rgba(13,26,25,.6);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.35);padding:7px 14px;border-radius:999px;font-weight:700;font-size:13px;letter-spacing:.04em;text-transform:uppercase}}
.badge.urgent{{background:var(--orange);border-color:var(--orange)}}
.body{{padding:4px 22px 24px;display:flex;flex-direction:column;flex:1}}
h2{{font-family:'Playfair Display',serif;font-size:36px;margin:0 0 12px;line-height:1.1}}h2 .t{{color:var(--teal)}}
h2 small{{font-family:'DM Sans',sans-serif;font-size:16px;color:var(--muted);font-weight:500}}
.tags{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}}
.tag{{border:1.5px solid var(--teal);color:var(--teal);border-radius:999px;padding:4px 12px;font-size:13px;font-weight:500}}
p{{margin:0 0 20px;font-size:15.5px}}.empty{{text-align:center;color:var(--muted);grid-column:1/-1}}
.cta{{margin-top:auto;display:block;text-align:center;background:var(--orange);color:#fff;text-decoration:none;font-weight:700;padding:14px;border-radius:999px}}
footer{{text-align:center;color:var(--muted);padding:0 16px 40px;font-size:14px}}footer a{{color:var(--teal)}}
</style></head><body>
<header><div class="kick">Waldo's Rescue Pen</div><h1>Fosters <span>Needed</span></h1>
<p>{e(data['intro'])}</p></header>
<main>
{cards}
</main>
<footer>Waldo's Rescue Pen is a 501(c)(3) foster-based rescue · <a href="https://www.instagram.com/{e(data['instagram'])}" target="_blank" rel="noopener">@{e(data['instagram'])}</a><br>Updated {updated}</footer>
</body></html>
"""
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs" / "index.html").write_text(page)
print(f"Built docs/index.html with {n} dog(s): {', '.join(d['name'] for d in dogs)}")
