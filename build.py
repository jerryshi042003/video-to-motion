#!/usr/bin/env python3
"""Build index.html: one phone-width column in the jerrythegoat.com write-up style,
with interactive model viewers for every GLB. Python 3 only."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
G = json.loads((ROOT / "gallery.json").read_text())
MANIFEST = ROOT / "media" / "models" / "manifest.json"
def _load_models():
    if not MANIFEST.exists():
        return {}
    raw = json.loads(MANIFEST.read_text())
    items = raw["models"] if isinstance(raw, dict) else raw
    out = {}
    for m in items:
        m = dict(m)
        m["file"] = "media/models/" + m["file"]
        m["poster"] = "media/models/" + m["poster"]
        out[m["id"]] = m
    return out
MODELS = _load_models()
CARDS = {}
for p in G["processes"]:
    for g in p["groups"]:
        for it in g.get("items", []):
            CARDS[it["id"]] = it
        for s in g.get("subgroups", []):
            for it in s["items"]:
                CARDS[it["id"]] = it
LIB_IDS = ("shelton-serve-b", "shelton-serve-d", "shelton-serve-f", "shelton-serve-g2", "alcaraz-serve", "sinner-return",
           "djokovic-turin-return", "cabolli-return", "alcaraz-a", "alcaraz-b", "djokovic-iw-a", "djokovic-iw-c",
           "cobolli-b1", "cobolli-b2", "cobolli-c1", "cobolli-c2")
e = html.escape
MISSING = []


def model(mid, cap, title=None, full=False):
    m = MODELS.get(mid)
    if not m:
        MISSING.append(mid)
        return ""
    anim = " autoplay" if m.get("animations") else ""
    kb = f"{round(m['bytes']/1024)} KB"
    label = e(title or m["title"])
    return f"""<figure class="model{' full' if full else ''}">
<model-viewer src="{e(m['file'])}" poster="{e(m['poster'])}" alt="{label}" loading="lazy" reveal="interaction" camera-controls touch-action="pan-y" auto-rotate{anim} interaction-prompt="none" shadow-intensity="0.5" exposure="1"><button slot="poster" class="tap" type="button" aria-label="Load {label}" style="background-image:url('{e(m['poster'])}')"><span>tap to load · {kb}</span></button></model-viewer>
<figcaption class="cap">{cap}</figcaption></figure>"""


def video(src, poster, cap):
    return f"""<figure class="vid"><video class="auto" src="{e(src)}" poster="{e(poster)}" muted loop playsinline preload="none" disablepictureinpicture></video><figcaption class="cap">{cap}</figcaption></figure>"""


def fig(src, cap, link=None):
    img = f'<img src="{e(src)}" loading="lazy" alt="">'
    if link:
        img = f'<a href="{e(link)}" target="_blank" rel="noopener">{img}</a>'
    return f'<figure class="fig">{img}<figcaption class="cap">{cap}</figcaption></figure>'


def rows(items):
    out = []
    for it in items:
        if isinstance(it, tuple):
            text, tag = it
            out.append(f"<li>{text} <code>{e(tag)}</code></li>")
        else:
            out.append(f"<li>{it}</li>")
    return '<ul class="rows plain">' + "".join(out) + "</ul>"


def dated_rows(items):
    return '<ul class="rows">' + "".join(
        f'<li><div><time>{e(d)}</time><span>{e(t)}</span><code>{e(c)}</code></div></li>' for d, t, c in items) + "</ul>"


def steps(items):
    return '<ol class="steps">' + "".join(
        f'<li><div class="ic"><span class="n">{i+1}</span></div><div><b>{e(t)}</b><small>{e(d)}</small></div><code>{e(c)}</code></li>'
        for i, (t, d, c) in enumerate(items)) + "</ol>"


def stat(items):
    return '<div class="stat">' + "".join(f'<div><b>{e(b)}</b><span>{e(s)}</span></div>' for b, s in items) + "</div>"


def two(blocks):
    return '<div class="two">' + "".join(b for b in blocks if b) + "</div>"


def lib_model(pid):
    c = CARDS.get(pid)
    cap = f"{e(c['title'])} · {e(c['meta'][0])} · {e(c['meta'][1])}" if c else e(pid)
    m = model("lib-" + pid, cap, title=c["title"] if c else pid)
    if m:
        return m
    # not converted yet: fall back to the four-up video
    if c:
        return video(c["video"], c["poster"], cap)
    return ""



def score_cards(items):
    out = []
    for img, name, line, score in items:
        out.append(f'<li><img src="{e(img)}" loading="lazy" alt=""><div><b>{e(name)}</b><small>{e(line)}</small></div><code>{e(score)}</code></li>')
    return '<ul class="scores">' + "".join(out) + "</ul>"

sections = []

sections.append(f"""<section aria-labelledby="h-stand">
<h2 id="h-stand">Where it stands</h2>
<p class="sub">Judged on the viewing result, not a measured match.</p>
{score_cards([
 ("media/refs/flowhmr-teaser.jpg","Body motion","FlowHMR · 82% tracking success on Wild-4K in its paper","8/10"),
 ("media/refs/racketvision-teaser.jpg","Ball","found in frame, estimated arcs · not spin or 3D flight","8/10"),
 ("media/racket/racket-full.jpg","Racket model","traced outline, woven strings, drilled grommets","7/10"),
 ("media/racket/ovl-djokovic-iw-a.jpg","Racket motion","RacketVision sees it in 32–40% of frames at 30 fps, 81% at 120","6/10"),
 ("media/logos/meshy.png","Skin and face, Meshy","outfit and surface yes · heads and hands no","5/10"),
 ("media/library/featured-serve-volley-poster.jpg","Body shape of the person","everyone shares the FlowHMR body","2/10"),
 ("media/bodies/shelton-serve-fal-poster.jpg","Skin and face, FlowHMR","plain grey body","2/10"),
 ("media/logos/hyper3d.png","Face likeness","Rodin, UP2You and Meshy all generate a face, none is the person","2/10"),
 ("media/refs/hawkeye-skeletrack.jpg","Gold standard","Hawk-Eye SkeleTRACK · 29 body points, 7 racket points, stadium cameras","ref"),
])}
</section>""")

sections.append(f"""<section aria-labelledby="h-motion">
<h2 id="h-motion">Video to motion</h2>
<p class="sub">One camera, one point, a body that moves like the player.</p>
{steps([("Pick a clip","court-level footage, player large in frame, one point","yt-dlp"),
        ("Body","joints, shape and camera per frame","FlowHMR · Modal"),
        ("Racket points","five keypoints where visible","RacketVision · Modal"),
        ("Racket through the arm","forearm and wrist inside limits, spin capped","Python"),
        ("Contact rule","label contact and shot, pin the face angle","by eye"),
        ("Render","four-up video and GLB","Blender")])}
<p class="cap">about $0.35 of Modal per clip · open weights</p>
{model("tennis-lab-shelton-coria","Ben Shelton, serve and volley · the whole point, both players · drag to orbit", full=True)}
{model("tennis-lab-shelton-serve","Ben Shelton serve · the first accepted motion", full=True)}
</section>""")

sections.append(f"""<section aria-labelledby="h-lib">
<h2 id="h-lib">The rear-court library</h2>
<p class="sub">Sixteen points, six players, one recipe. The eight distinct ones; the rest look the same.</p>
{lib_model("shelton-serve-d")}
{lib_model("alcaraz-serve")}
{lib_model("sinner-return")}
{lib_model("djokovic-turin-return")}
{lib_model("cabolli-return")}
{lib_model("alcaraz-a")}
{lib_model("djokovic-iw-a")}
{lib_model("cobolli-c1")}
</section>""")

sections.append(f"""<section aria-labelledby="h-cams">
<h2 id="h-cams">Other cameras and frame rates</h2>
<p class="sub">Same FlowHMR, different footage. This is where quality changes.</p>
{video("media/racket/alcaraz-120-forehand-v2.mp4","media/racket/alcaraz-120-forehand-v2-poster.jpg","Alcaraz forehand · 4K 120 fps · the racket stays through contact")}
{model("tennis-lab-shelton-atp","ATP broadcast · elevated camera · body only, no usable wrist", full=True)}
{model("tennis-lab-ucla-point8-combined","college match · fixed club camera · body + charted ball", full=True)}
{model("tennis-lab-shelton-long-rally","14-second rally · drift and hidden hands over time", full=True)}
{video("media/racket/djokovic-groundstroke-v2.mp4","media/racket/djokovic-groundstroke-v2-poster.jpg","Djokovic · high diagonal seat, 4K crop · the ceiling for groundstrokes")}
</section>""")

sections.append(f"""<section aria-labelledby="h-racket">
<h2 id="h-racket">The racket</h2>
<p class="sub">A model, a detector, and a solver that moves it through the arm.</p>
{model("racket-arm-solved","the rebuilt racket · frame, throat, grommets, woven strings, grip", full=True)}
{model("tennis-lab-equipment-aero-motion","Pure Aero on the serve · traced from manufacturer photos", full=True)}
{fig("media/racket/ovl-djokovic-iw-a.jpg","solved through the arm · red old fit, green arm solve, cyan detections")}
{fig("media/racket/edge-before-after.jpg","face angle at contact, before and after the rule")}
</section>""")

sections.append(f"""<section aria-labelledby="h-bodies">
<h2 id="h-bodies">Bodies from photos</h2>
<p class="sub">Three frames of the player's own video to Rodin 2.5 through fal.ai, bound to the motion.</p>
{video("media/bodies/shelton-serve-fal.mp4","media/bodies/shelton-serve-fal-poster.jpg","Shelton with his own Rodin body · outfit matches the footage · face generated")}
{model("rodin-shelton","the Rodin body itself · about $0.40", full=True)}
{rows([("Eight bodies built, all paused: wrinkles, bent spine, changed height","paused"),("UP2You and MICA face fits rejected","rejected")])}
</section>""")

sections.append(f"""<section aria-labelledby="h-scenes">
<h2 id="h-scenes">Scenes and cast</h2>
<p class="sub">Venues are data, not generated images: OpenStreetMap, USGS terrain, an aerial photo, Poly Haven props. Meshy made the people.</p>
{model("shelton-coria-point","the USTA opener · plain grey body with the Wilson ball · live on jerrythegoat.com/usta", full=True)}
{model("ball-usopen","the Wilson US Open ball · 6.7 cm, felt and print from reference photos", full=True)}
{fig("media/venues/usta-sheet.jpg","US Open · Arthur Ashe and Flushing Meadows from OSM and code","https://jerrythegoat.com/usta/")}
{fig("media/venues/ucla-full.jpg","UCLA · real terrain, aerial photo ground, 52k trees from its near-infrared band","https://jerrythegoat.com/ucla/")}
{fig("media/venues/galaxy-full.jpg","Galaxy, Kings, Reign · Dignity Health Sports Park from OSM","https://jerrythegoat.com/galaxy/")}
<p class="cap">the Meshy cast · photo → A-pose still → image-to-3D → rig</p>
{model("shelton-2","Ben Shelton · Meshy likeness, live on the USTA page before the rebuild", full=True)}
{model("gauff-2","Coco Gauff · Meshy likeness", full=True)}
{model("martin","Billy Martin · UCLA head coach", full=True)}
{model("jerry","Jerry · four-photo rebuild", full=True)}
{model("umpire","chair umpire · from a text prompt", full=True)}
{model("sp-1","seated spectator · remeshed to 1.5k polys for the crowd", full=True)}
{model("palm","palm · instanced 200+ times around Carson", full=True)}
</section>""")

sections.append(f"""<section aria-labelledby="h-loader">
<h2 id="h-loader">The goat, the ibex and the mountain</h2>
<p class="sub">The home-page intro animal and wallpaper.</p>
{model("goat-loader","dot goat · a CC0 goat reshaped in Blender · the default", full=True)}
{model("toy-ibex","toy ibex · nano-banana still → Tripo", full=True)}
{model("toy-mountain","toy mountain · nano-banana still → Tripo", full=True)}
{video("media/loader/three-loaders.mp4","media/loader/three-loaders-poster.jpg","dot, toy, real · the same climb on three animals")}
{fig("media/loader/mountain-flux-outpaint.jpg","home-page mountain · an ink painting extended by FLUX outpainting · $0.35")}
</section>""")

sections.append(f"""<section aria-labelledby="h-films">
<h2 id="h-films">Films and thumbnails</h2>
<p class="sub">HyperFrames renders HTML to video frame by frame in headless Chrome.</p>
{video("media/hyperframes/cycling-film.mp4","media/hyperframes/cycling-film-poster.jpg","cycling film · 17 s · live at /cycling")}
{video("media/hyperframes/reel-v3.mp4","media/hyperframes/reel-v3-poster.jpg","sports data reel · 31 s")}
{video("media/hyperframes/shield-genie.mp4","media/hyperframes/shield-genie-poster.jpg","Shield · ask the season goal")}
{video("media/hyperframes/radio-captions.mp4","media/hyperframes/radio-captions-poster.jpg","radio · word-by-word captions · live card")}
{video("media/thumbs/final-galaxy.mp4","media/thumbs/final-galaxy-poster.jpg","Galaxy card · chosen from 140 options, ends on Ontario Reign")}
{fig("media/thumbs/review-desktop.jpg","the review page · 140 candidates, one chosen per project")}
</section>""")

sections.append(f"""<section aria-labelledby="h-dropped">
<h2 id="h-dropped">Tried and dropped</h2>
{rows([("Kling 3.0 motion-control video failed the anatomy gate","fal.ai"),
       ("GEM-X and Kimodo mocap loops, none adopted","Modal"),
       ("Meshy heads on the serve body: detached","Meshy"),
       ("Rodin granite crag: a marble column","fal.ai"),
       ("nano-banana backdrops: greenscreen","fal.ai")])}
</section>""")

T = G["timeline"]
sections.append(f"""<section aria-labelledby="h-time">
<h2 id="h-time">Timeline</h2>
{dated_rows([(t["date"], t["what"], "done") for t in T["done"]] + [("Oct 29", "16-point library and the audit; USTA opener rebuilt on the serve-and-volley point", "done"), ("Oct 30", "Serve kept behind the baseline; goat intro on the home page only; deployed", "live")])}
<p class="cap">next · 120 fps footage only · racket silhouette in the lag phase · a hand model · ground truth under 5 px · a body and face that are the person</p>
</section>""")

sections.append("""<section class="try" aria-label="Open">
<a class="btn" href="https://jerrythegoat.com/usta/">Open the USTA story</a>
<a class="btn2" href="https://jerry-tennis-lab.vercel.app/">The Tennis Lab demos</a>
<footer>FlowHMR and RacketVision on Modal · Rodin, Tripo, Hunyuan3D, Kling, FLUX and nano-banana through fal.ai · Meshy · Blender · HyperFrames · footage: Court Level Tennis, Slow-Mo Tennis, TennisTV, UCLA Tennis Consulting · depth is monocular, no physics · faces are generated, not likenesses</footer>
</section>""")

CSS = (ROOT / "writeup.css").read_text()
EXTRA = """
/* gallery additions, same contract: hairlines, fill, mono captions, one accent */
figure{margin:0}
.fig img{display:block;width:100%;height:auto;border-radius:12px;border:1px solid var(--line);background:var(--fill)}
.vid video{display:block;width:100%;height:auto;border-radius:12px;border:1px solid var(--line);background:var(--fill)}
.model model-viewer{display:block;width:100%;height:auto;aspect-ratio:1/1;border-radius:12px;border:1px solid var(--line);background:var(--fill);--poster-color:transparent}
.model.full model-viewer{aspect-ratio:4/3}
.tap{position:absolute;inset:0;width:100%;height:100%;border:0;background:var(--fill) center/cover no-repeat;cursor:pointer;border-radius:12px;display:flex;align-items:flex-end;justify-content:center;padding:8px}
.tap span{font:11px var(--mono);color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:4px 9px}
.scores{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.scores li{display:grid;grid-template-columns:56px 1fr auto;gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid var(--line)}
.scores img{width:56px;height:56px;object-fit:cover;border-radius:12px;background:var(--fill);border:1px solid var(--line)}
.scores b{display:block;font-weight:600}
.scores small{display:block;color:var(--muted);font-size:12.5px;line-height:1.35}
.scores code{font:12px var(--mono);color:var(--fg);background:var(--fill);border-radius:6px;padding:3px 7px}
.steps .ic .n{font:12px var(--mono);color:var(--fg)}
section > .model, section > .vid, section > .fig, section > .rows, section > .scores{margin-top:16px}
section > .cap + .model{margin-top:8px}
section > .sub + *{margin-top:0}
"""

page = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Video to Motion</title>
<meta name="description" content="What FlowHMR, RacketVision, Rodin, Meshy, HyperFrames and Blender actually produced: tennis video to 3D motion, rackets, bodies, scenes and films. Every model is interactive.">
<meta property="og:title" content="Video to Motion"><meta property="og:description" content="One camera, one point, a body that moves like the player. Every 3D model we made, interactive.">
<style>{CSS}{EXTRA}</style>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@4.1.0/dist/model-viewer.min.js"></script>
</head><body>
<main class="col">
<div class="made"><a href="https://jerrythegoat.com/">jerrythegoat.com</a> · video to motion</div>
<header><h1>Video to Motion</h1><p>Tennis video to 3D motion, rackets, bodies, scenes and films. What each generator actually produced, with every model interactive.</p></header>
{''.join(sections)}
</main>
<script>
(function(){{
  var setDecoder=function(){{var c=customElements.get('model-viewer'); if(c) c.meshoptDecoderLocation='https://cdn.jsdelivr.net/npm/meshoptimizer@0.22.0/meshopt_decoder.js';}};
  customElements.whenDefined('model-viewer').then(setDecoder);
  document.querySelectorAll('.tap').forEach(function(b){{b.addEventListener('click',function(ev){{ev.preventDefault();var mv=b.closest('model-viewer');mv.dismissPoster();}});}});
  var vids=[].slice.call(document.querySelectorAll('video.auto'));
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(es){{es.forEach(function(x){{var v=x.target;if(x.isIntersecting){{if(v.preload==='none'){{v.preload='auto';v.load();}}v.play().catch(function(){{}});}}else{{v.pause();}}}});}},{{rootMargin:'160px 0px'}});
    vids.forEach(function(v){{io.observe(v);}});
  }}
}})();
</script>
</body></html>
"""
(ROOT / "index.html").write_text(page)
print("wrote index.html", len(page), "bytes; models in manifest:", len(MODELS), "; missing refs:", sorted(set(MISSING)))
