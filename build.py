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


S = G["scores"]
score_rows = rows([(f"{e(s['name'])}: {e(s['note'])}", f"{s['score']}/10") for s in S])

sections = []

sections.append(f"""<section aria-labelledby="h-stand">
<h2 id="h-stand">Where it stands</h2>
<p class="sub">Self-assessed on the viewing result, not a measured match. Frame rate matters most for the racket and ball.</p>
{stat([("8/10","body motion"),("6/10","racket motion"),("2/10","likeness")])}
{score_rows}
<p class="cap">gold standard: Hawk-Eye SkeleTRACK, 29 body points and 7 racket points from a stadium camera system · cited numbers come from the papers' own benchmarks, not this footage</p>
</section>""")

sections.append(f"""<section aria-labelledby="h-motion">
<h2 id="h-motion">Video to motion</h2>
<p class="sub">One camera, one point, a body that moves like the player. Modal rents the GPU; FlowHMR gives the body; RacketVision finds the racket; the rest is local.</p>
{steps([("Pick a clip","court-level YouTube footage, player large in frame, cut to one point","yt-dlp"),
        ("Body","joints, shape and camera per frame","FlowHMR · Modal"),
        ("Racket points","five keypoints where the racket is visible","RacketVision · Modal"),
        ("Racket through the arm","forearm twist and wrist angle inside limits, spin capped","Python"),
        ("Contact rule","label contact frame and shot, pin the face angle","by eye"),
        ("Render","source, front, side, back; GLB for the web","Blender")])}
<p class="cap">about $0.35 of Modal per clip · open weights · nothing re-solved by hand</p>
{model("tennis-lab-shelton-coria","Ben Shelton, serve and volley · the whole point, both players · drag to orbit", full=True)}
{model("tennis-lab-shelton-serve","Ben Shelton serve · the first accepted motion, Oct 22", full=True)}
{video("media/library/featured-serve-volley.mp4","media/library/featured-serve-volley-poster.jpg","the same point from the Tennis Lab demo, Behind camera")}
</section>""")

sections.append(f"""<section aria-labelledby="h-lib">
<h2 id="h-lib">The rear-court library</h2>
<p class="sub">Sixteen points, six players, one recipe. Court level from behind, 30 fps, 1080p cut from 4K. Tap a tile to load its model.</p>
<p class="cap">serves</p>
{two([lib_model(p) for p in ("shelton-serve-b","shelton-serve-d","shelton-serve-f","shelton-serve-g2")])}
<p class="cap">returns</p>
{two([lib_model(p) for p in ("sinner-return","djokovic-turin-return","cabolli-return")])}
<p class="cap">served points with groundstrokes</p>
{two([lib_model(p) for p in ("alcaraz-serve","alcaraz-a","alcaraz-b","djokovic-iw-a","djokovic-iw-c","cobolli-b1","cobolli-b2","cobolli-c1","cobolli-c2")])}
{rows([("Shelton is left-handed; the racket stays in the left hand across frames","handedness"),
       ("Djokovic IW-A frame 145 and IW-C frame 312 are one-handed slices; Alcaraz-A 303 is a two-handed backhand","contacts"),
       ("Racket error 4.7 to 12.5 px median per point; arm limits exceeded on 0 to 37 frames","numbers"),
       ("Face angle at contact is set by rule, not measured","limit")])}
</section>""")

sections.append(f"""<section aria-labelledby="h-cams">
<h2 id="h-cams">Other cameras and frame rates</h2>
<p class="sub">Same FlowHMR, different footage. This is where quality changes.</p>
{video("media/racket/alcaraz-120-forehand-v2.mp4","media/racket/alcaraz-120-forehand-v2-poster.jpg","Alcaraz forehand · 4K 120 fps · the detector keeps the racket through contact: 81% of frames found vs 32–40% at 30 fps")}
{two([model("tennis-lab-shelton-atp","ATP broadcast · elevated camera, 169 frames · body only"),
      model("tennis-lab-ucla-point8-combined","college match · fixed club camera · body + charted ball arcs"),
      model("tennis-lab-shelton-long-rally","14-second rally · drift and hidden hands over time"),
      model("tennis-lab-shelton-wide","wide-view movement · behind the baseline"),
      model("tennis-lab-shelton-rally","forehand and backhand · near-side player"),
      model("tennis-lab-quan-gomez-point","Quan vs Gomez · Hawk-Eye capsule replay")])}
{video("media/racket/djokovic-groundstroke-v2.mp4","media/racket/djokovic-groundstroke-v2-poster.jpg","Djokovic groundstrokes · high diagonal seat, 4K crop · body fit improved, racket detection got worse: this camera is the ceiling")}
{rows([("Broadcast and high-seat footage give a body but no usable wrist or face","why"),
       ("Only the 120 fps clip shows the racket through contact","frame rate"),
       ("Two-player point and the long rally stay as test scenes","status")])}
</section>""")

sections.append(f"""<section aria-labelledby="h-racket">
<h2 id="h-racket">The racket</h2>
<p class="sub">A model, a detector, and a solver that moves it through the arm.</p>
{model("racket-arm-solved","the rebuilt racket · frame, throat, grommets, woven strings, grip · built in Blender from reference contours", full=True)}
{model("tennis-lab-equipment-aero-motion","Pure Aero on the serve · traced from manufacturer photos", full=True)}
{two([model("racket-ezone","EZONE 98 · photo-textured, the library stand-in"), model("racket-aero","Pure Aero 98 · traced"), model("racket-vcore","VCORE 98 · traced"), model("racket-blade","Blade 98 v10 · traced")])}
{fig("media/racket/ovl-djokovic-iw-a.jpg","solved through the arm · red old fit, green arm solve, cyan detections · no frame over 2,600°/s on 15 of 16 points")}
{fig("media/racket/hfr-contact.jpg","120 fps through contact · green fit on cyan detections · 15.5 px on held-out frames")}
{fig("media/racket/edge-before-after.jpg","face angle at contact, before and after the rule · 7 of 34 plausible → 34 of 34")}
{fig("media/racket/all-grip.jpg","hand-to-handle registration for every point")}
{rows([("Five racket points per frame where visible; availability is not accuracy","RacketVision"),
       ("Seen from behind, open and closed faces shrink the outline the same way; the rule chose the angle","limit"),
       ("Next: segment the racket in the lag phase, hand model for grip, ground truth under 5 px","next")])}
</section>""")

sections.append(f"""<section aria-labelledby="h-bodies">
<h2 id="h-bodies">Bodies from photos</h2>
<p class="sub">Two or three frames of the player's own video to Rodin 2.5 through fal.ai, bound to the FlowHMR motion.</p>
{video("media/bodies/shelton-serve-fal.mp4","media/bodies/shelton-serve-fal-poster.jpg","Shelton serve with his own Rodin body · outfit matches the footage · face generated, not a likeness")}
{two([model("rodin-shelton","Shelton · Rodin 2.5"), model("rodin-cobolli","Cobolli · Rodin 2.5"), model("rodin-alcaraz","Alcaraz · Rodin 2.5"), model("rodin-perricard","Mpetshi Perricard · Rodin 2.5"), model("rodin-djokovic-2","Djokovic take 2 · Rodin 2.5"), model("rodin-shelton-rigged","Shelton · cleaned and rigged")])}
{fig("media/bodies/compare-serve.jpg","source, plain body, Rodin body across the serve")}
{rows([("Eight bodies at about $0.40 each; all paused on Oct 28: wrinkled, bent spine, changed height","paused"),
       ("The hand stays open under the grip; loose clothing bulges because the shirt is part of the mesh","limit"),
       ("UP2You and MICA face fits rejected at 2/10 and 4/10","rejected")])}
</section>""")

sections.append(f"""<section aria-labelledby="h-scenes">
<h2 id="h-scenes">Scenes and cast</h2>
<p class="sub">The venue backgrounds are data, not generated images: OpenStreetMap footprints, USGS terrain, a NAIP aerial photo, Poly Haven props. Meshy made the people.</p>
{model("shelton-coria-point","the USTA story opener · the same point as a plain grey body, live on jerrythegoat.com/usta", full=True)}
{two([model("ball-usopen","the Wilson US Open ball · 6.7 cm, felt and print authored from reference photos"), model("straus-stands","Straus Stadium stands · 3D Warehouse model used on the UCLA page")])}
{fig("media/venues/usta-sheet.jpg","US Open · Arthur Ashe and Flushing Meadows from OSM and code","https://jerrythegoat.com/usta/")}
{fig("media/venues/ucla-full.jpg","UCLA · Westwood on real terrain, aerial photo ground, 52k trees from its near-infrared band","https://jerrythegoat.com/ucla/")}
{fig("media/venues/galaxy-full.jpg","Galaxy, Kings, Reign · Dignity Health Sports Park from OSM, Poly Haven props","https://jerrythegoat.com/galaxy/")}
<p class="cap">the Meshy cast · photo → A-pose still → Meshy 7.1 image-to-3D → rig · tap to load</p>
{two([model("shelton-2","Ben Shelton · likeness v2, live"), model("gauff-2","Coco Gauff · likeness v2"), model("gilbert","Brad Gilbert · live"), model("martin","Billy Martin · live"),
      model("quan-iw","Rudy Quan · live"), model("jerry","Jerry · four-photo rebuild, live"), model("umpire","chair umpire · live"), model("ballkid","ball kid · live"),
      model("stu-1","walking student"), model("sp-1","seated spectator · remeshed for the crowd"), model("fan-1","Galaxy fan"), model("pro-a","generic pro · plays soccer and hockey too"),
      model("palm","palm · instanced 200+ times"), model("analyst","front-row analyst"), model("jerry-serve","Jerry serve · mocap retargeted"), model("coach","generic coach"), model("bruin","UCLA figure"), model("crowd-sp-1","crowd impostor · 1.5k polys")])}
{rows([("About 1,900 Meshy credits for the cast, crowd and props in five days","cost"),
       ("Fast and consistent for stylised people; heads rejected as likeness, hands came out as mittens","verdict"),
       ("Source stills and prompts were deleted with the scratch folder on Oct 27; the GLBs survive","note")])}
</section>""")

sections.append(f"""<section aria-labelledby="h-loader">
<h2 id="h-loader">The goat, the ibex and the mountain</h2>
<p class="sub">The home-page intro animal and wallpaper, and the generated variants that were tried.</p>
{two([model("goat-loader","dot goat · CC0 goat reshaped in Blender · the default"), model("toy-ibex","toy ibex · nano-banana still → Tripo"),
      model("toy-ibex-hunyuan-raw","toy ibex · the Hunyuan3D attempt, not used"), model("toy-mountain","toy mountain · nano-banana still → Tripo"), model("boulder-loader","the boulder · Poly Haven, decimated"), model("mountainside-loader","mountainside · Poly Haven")])}
{video("media/loader/three-loaders.mp4","media/loader/three-loaders-poster.jpg","dot, toy, real · the same climb on three animals")}
{fig("media/loader/theme-backdrops.jpg","blue-hour backdrops from nano-banana · rejected: feels like greenscreen")}
{fig("media/loader/mountain-flux-outpaint.jpg","home-page mountain · an ink painting extended by FLUX outpainting, original pixels unchanged · $0.35")}
{fig("media/loader/goat-mark-candidates.jpg","header mark · four traced candidates, C chosen")}
{rows([("Rodin text-to-3D granite crag for the wild scene rejected as a marble column","rejected"),
       ("Cingino dam rebuild with a Rodin ibex stayed on staging","paused"),
       ("Goat intro now plays on the home page only and draws every 8 ms","live")])}
</section>""")

sections.append(f"""<section aria-labelledby="h-films">
<h2 id="h-films">Films and thumbnails</h2>
<p class="sub">HyperFrames renders HTML to video by seeking a paused timeline frame by frame in headless Chrome. Every hub clip and film came from it.</p>
{video("media/hyperframes/cycling-film.mp4","media/hyperframes/cycling-film-poster.jpg","cycling film · 17 s · live at /cycling")}
{video("media/hyperframes/reel-v3.mp4","media/hyperframes/reel-v3-poster.jpg","sports data reel v3 · 31 s · twelve segments")}
{two([video("media/hyperframes/shield-genie.mp4","media/hyperframes/shield-genie-poster.jpg","Shield · ask the season goal"),
      video("media/hyperframes/match-map.mp4","media/hyperframes/match-map-poster.jpg","Match Viewer · live card"),
      video("media/hyperframes/radio-captions.mp4","media/hyperframes/radio-captions-poster.jpg","radio · word-by-word captions"),
      video("media/hyperframes/hawkeye-loop.mp4","media/hyperframes/hawkeye-loop-poster.jpg","Hawk-Eye 3D match films")])}
<p class="cap">the live home-page cards · chosen from 140 options on Oct 27</p>
{two([video("media/thumbs/final-galaxy.mp4","media/thumbs/final-galaxy-poster.jpg","Galaxy · ends on Ontario Reign"),
      video("media/thumbs/final-usta.mp4","media/thumbs/final-usta-poster.jpg","USTA · serve first"),
      video("media/thumbs/final-ucla.mp4","media/thumbs/final-ucla-poster.jpg","UCLA · serve down the T"),
      video("media/thumbs/final-cycling.mp4","media/thumbs/final-cycling-poster.jpg","cycling · rider to infield to TV")])}
{fig("media/thumbs/review-desktop.jpg","the review page · 140 de-duplicated candidates, one chosen per project")}
</section>""")

sections.append(f"""<section aria-labelledby="h-dropped">
<h2 id="h-dropped">Tried and dropped</h2>
{rows([("Kling 3.0 motion-control video: both runs failed the anatomy gate, $2.50","fal.ai"),
       ("GEM-X mocap, 14 runs on an L40S: loops came back, none adopted, $3.35","Modal"),
       ("Kimodo: a ready-position loop, not released","Modal"),
       ("Meshy heads on the serve body: detached, 5/10","Meshy"),
       ("Internally generated mountain wings and pinnacle: rejected","image"),
       ("Up-front shader compile for the goat intro: slower under software GL, reverted","web")])}
</section>""")

T = G["timeline"]
sections.append(f"""<section aria-labelledby="h-time">
<h2 id="h-time">Timeline</h2>
{dated_rows([(t["date"], t["what"], "done") for t in T["done"]] + [("Oct 29", "16-point library and the audit; USTA opener rebuilt on the serve-and-volley point", "done"), ("Oct 30", "Serve kept behind the baseline; goat intro on the home page only; all three PRs merged and deployed", "live")])}
<p class="cap">next · 120 fps footage only · racket silhouette in the lag phase · a hand model for grip · ground truth under 5 px · a body and face that are the person</p>
</section>""")

sections.append("""<section class="try" aria-label="Open">
<a class="btn" href="https://jerrythegoat.com/usta/">Open the USTA story</a>
<a class="btn2" href="https://jerry-tennis-lab.vercel.app/">The Tennis Lab demos</a>
<footer>FlowHMR and RacketVision on Modal · Rodin, Tripo, Hunyuan3D, Kling, FLUX and nano-banana through fal.ai · Meshy · Blender · HyperFrames · footage: Court Level Tennis, Slow-Mo Tennis, TennisTV, UCLA Tennis Consulting · body depth is monocular, no physics simulated · faces are generated, not likenesses</footer>
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
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.two .cap{margin-top:8px}
.steps .ic .n{font:12px var(--mono);color:var(--fg)}
section > .model, section > .vid, section > .fig, section > .two, section > .rows, section > .stat{margin-top:16px}
section > .cap + .two{margin-top:8px}
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
