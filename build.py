#!/usr/bin/env python3
"""Build index.html from gallery.json. No dependencies beyond Python 3."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
G = json.loads((ROOT / "gallery.json").read_text())

VERDICT = {
    "accepted": "good", "used on page": "good", "built": "mid", "paused": "mid",
    "diagnostic": "mid", "not adopted": "bad", "rejected": "bad", "failed": "bad",
}
e = html.escape


def imgs(paths, cls=""):
    if not paths:
        return '<div class="none">no image kept</div>'
    return "".join(
        f'<a href="{e(p)}" target="_blank" rel="noopener"><img src="{e(p)}" loading="lazy" alt=""></a>' for p in paths
    )


def call_card(c):
    parts = [c["service"], c.get("model") or "", c["date"], c.get("cost") or ""]
    meta = " · ".join(e(x) for x in parts if x)
    v = f'<span class="v {VERDICT.get(c["verdict"], "")}">{e(c["verdict"])}</span>'
    return f"""<article class="card" id="{e(c['id'])}">
<h3>{e(c['title'])}</h3><div class="meta">{meta} · {v}</div>
<div class="io"><div class="imgs">{imgs(c['inputs'])}</div><div class="arrow" aria-hidden="true">→</div><div class="imgs">{imgs(c['outputs'])}</div></div>
</article>"""


def calls(section):
    return "\n".join(call_card(c) for c in G["calls"] if c["section"] == section)


def figure(src, caption, poster=None):
    if src.endswith(".mp4"):
        media = f'<video src="{e(src)}" poster="{e(poster or "")}" controls muted loop playsinline preload="none"></video>'
    else:
        media = f'<a href="{e(src)}" target="_blank" rel="noopener"><img src="{e(src)}" loading="lazy" alt=""></a>'
    return f"<figure>{media}<figcaption>{e(caption)}</figcaption></figure>"


def library():
    cards = []
    for p in G["library"]:
        hand = f" · {e(p['hand'])}" if p["hand"] else ""
        cards.append(f"""<figure class="clip">
<video src="{e(p['video'])}" poster="{e(p['poster'])}" controls muted loop playsinline preload="none"></video>
<figcaption>{e(p['player'])}{hand} · {p['frames']} frames · <a href="{e(p['source'])}" target="_blank" rel="noopener">source {e(p['range'])}</a></figcaption>
</figure>""")
    return "\n".join(cards)


NAV = [
    ("library", "The library"), ("motion", "Video to motion"), ("racket", "The racket"),
    ("bodies", "Bodies"), ("faces", "Faces"), ("meshy", "Meshy"), ("mocap", "Other mocap"), ("ibex", "Image to 3D"),
]

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Video to Motion</title>
<meta name="description" content="A visual library of what Modal (FlowHMR, RacketVision), fal.ai (Rodin, Kling, Hunyuan3D, Tripo) and Meshy produced when turning tennis video into 3D motion, rackets and bodies.">
<style>
:root{{--bg:#fff;--fg:#111;--muted:#666;--line:#e3e3e3;--good:#1f7a3f;--bad:#b4442c;--link:#0b57d0}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111;--fg:#eee;--muted:#999;--line:#2a2a2a;--good:#6cc08f;--bad:#e2775c;--link:#8ab4f8}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
main{{max-width:1280px;margin:0 auto;padding:28px 20px 60px}}
h1{{font-size:22px;margin:0 0 2px;font-weight:600}}
h2{{font-size:18px;margin:44px 0 12px;padding-top:14px;border-top:1px solid var(--line);font-weight:600;scroll-margin-top:16px}}
h3{{font-size:15px;margin:0;font-weight:600}}h3.sub{{margin:28px 0 10px;color:var(--muted);font-weight:500}}
.lede{{color:var(--muted);margin:0 0 14px}}
nav{{font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;gap:4px 14px}}nav a{{color:var(--muted);text-decoration:none}}nav a:hover{{color:var(--fg)}}
.card{{padding:14px 0;border-top:1px solid var(--line)}}.card:first-of-type{{border-top:0}}
.meta{{font-size:13px;color:var(--muted);margin:1px 0 8px}}
.v{{color:var(--muted)}}.v.good{{color:var(--good)}}.v.bad{{color:var(--bad)}}
.io{{display:grid;grid-template-columns:minmax(0,1fr) 24px minmax(0,1.4fr);gap:10px;align-items:start}}
.imgs{{display:flex;flex-wrap:wrap;gap:6px}}.imgs img{{height:180px;max-width:100%;width:auto;border-radius:3px;background:#222;object-fit:contain;display:block}}
.arrow{{color:var(--muted);text-align:center;padding-top:76px}}
.none{{color:var(--muted);font-size:13px;padding-top:4px}}
figure{{margin:0 0 16px;display:grid;gap:5px}}figure img,figure video{{width:100%;height:auto;display:block;border-radius:3px;background:#222}}
figcaption{{font-size:13px;color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,400px),1fr));gap:16px}}
.grid.wide{{grid-template-columns:repeat(auto-fill,minmax(min(100%,600px),1fr))}}
a{{color:var(--link)}}
footer{{margin-top:48px;padding-top:12px;border-top:1px solid var(--line);font-size:13px;color:var(--muted);display:grid;gap:4px}}
@media (max-width:720px){{.io{{grid-template-columns:1fr}}.arrow{{padding:0;transform:rotate(90deg)}}.imgs img{{height:140px}}}}
</style></head><body><main>
<h1>Video to Motion</h1>
<p class="lede">Tennis video to 3D motion, rackets and bodies. Input left, output right.</p>
<nav>{''.join(f'<a href="#{k}">{e(v)}</a>' for k, v in NAV)}</nav>

<h2 id="library">The library: 16 points, 6 players</h2>
<div class="grid">
{library()}
</div>

<h2 id="motion">Video to body motion</h2>
{calls('motion')}

<h2 id="racket">The racket</h2>
<div class="grid">
{figure('media/racket/racket-full.jpg', 'Racket model, built in Blender')}
{figure('media/racket/racket-face.jpg', 'Face')}
{figure('media/racket/racket-tip-macro.jpg', 'Tip grommets')}
{figure('media/racket/racket-strings-macro.jpg', 'Frame edge')}
</div>
<h3 class="sub">Finding the racket</h3>
{calls('racket-detect')}
<h3 class="sub">Solving the racket through the arm</h3>
<div class="grid wide">
{figure('media/racket/ovl-djokovic-iw-a.jpg', 'Djokovic, Indian Wells A. Red old fit, green arm solve, cyan detections')}
{figure('media/racket/ovl-djokovic-turin-return.jpg', 'Djokovic, Turin')}
{figure('media/racket/ovl-djokovic-iw-c.jpg', 'Djokovic, Indian Wells C')}
{figure('media/racket/ovl-sinner-return.jpg', 'Sinner return')}
</div>
<h3 class="sub">Grip</h3>
<div class="grid wide">
{figure('media/racket/all-grip.jpg', 'Grip registration, all 16 points')}
{figure('media/racket/hand-grip-contact.jpg', 'Hand at contact, 120 fps')}
</div>
<h3 class="sub">120 fps changes everything</h3>
{figure('media/racket/alcaraz-120-forehand-v2.mp4', 'Alcaraz forehand, 120 fps. Source, overlay, front, side, back', 'media/racket/alcaraz-120-forehand-v2-poster.jpg')}
<div class="grid wide">
{figure('media/racket/hfr-contact.jpg', 'Through contact')}
{figure('media/racket/hfr-follow.jpg', 'Follow-through')}
</div>
<h3 class="sub">Face angle at contact</h3>
<div class="grid wide">
{figure('media/racket/face-edge-compare.jpg', 'Face angle at contact, before and after')}
{figure('media/racket/edge-before-after.jpg', 'Same check across the library')}
</div>
<h3 class="sub">Djokovic groundstroke, rebuilt from a 4K crop</h3>
{figure('media/racket/djokovic-groundstroke-v2.mp4', 'Djokovic groundstroke from a 4K crop', 'media/racket/djokovic-groundstroke-v2-poster.jpg')}
<div class="grid wide">
{figure('media/racket/compare-a.jpg', 'Phases 20 to 80')}
{figure('media/racket/compare-b.jpg', 'Phases 84 to 155')}
</div>

<h2 id="bodies">Whole bodies from photos: fal.ai Rodin</h2>
{figure('media/bodies/shelton-serve-fal.mp4', 'Shelton serve, his own Rodin body', 'media/bodies/shelton-serve-fal-poster.jpg')}
{figure('media/bodies/compare-serve.jpg', 'Source, plain body, Rodin body')}
{calls('bodies')}

<h2 id="faces">Faces and whole-person reconstruction on Modal</h2>
{calls('faces')}

<h2 id="meshy">Meshy</h2>
{calls('meshy')}

<h2 id="mocap">Other motion capture tried</h2>
{calls('mocap')}

<h2 id="ibex">Image to 3D for a different subject: an ibex</h2>
{calls('ibex')}

<footer>
<span>Footage: Court Level Tennis, Slow-Mo Tennis, TennisTV, a college PlaySight camera. Short excerpts for analysis.</span>
<span>Tools: FlowHMR, RacketVision on Modal. Rodin 2.5, Kling 3.0, Hunyuan3D, Tripo, Flux, nano-banana on fal.ai. Meshy 6 Lite, 7.1. Blender.</span>
</footer>
</main></body></html>
"""
(ROOT / "index.html").write_text(page)
print("wrote index.html", len(page), "bytes")
