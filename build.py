#!/usr/bin/env python3
"""Build index.html: one phone-width column in the jerrythegoat.com write-up style.
Organised by pipeline step; every 3D result is the real interactive scene, embedded inline."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
MANIFEST = ROOT / "media" / "models" / "manifest.json"
e = html.escape


def _models():
    if not MANIFEST.exists():
        return {}
    raw = json.loads(MANIFEST.read_text())
    out = {}
    for m in (raw["models"] if isinstance(raw, dict) else raw):
        m = dict(m); m["file"] = "media/models/" + m["file"]; m["poster"] = "media/models/" + m["poster"]; out[m["id"]] = m
    return out


MODELS = _models()
MISSING = []

# ---------- components ----------

def lab(match, cap, camera="behind", footage=1, h=720):
    src = f"lab/?source=motion&match={match}&embed=1&camera={camera}&footage={footage}&autoplay=1"
    return f'<figure class="scene"><iframe src="{e(src)}" loading="lazy" title="{e(cap)}" allow="autoplay" style="height:{h}px"></iframe><figcaption class="cap">{cap}</figcaption></figure>'


def review(point, cap, camera="behind", h=640):
    src = f"review/?point={point}&embed=1&camera={camera}&footage=1&autoplay=1"
    return f'<figure class="scene"><iframe src="{e(src)}" loading="lazy" title="{e(cap)}" allow="autoplay" style="height:{h}px"></iframe><figcaption class="cap">{cap}</figcaption></figure>'


def yt(vid, start, end, cap, clip=None):
    """The actual footage excerpt, played here (the channels block YouTube embeds). Credit links to the video at the timestamp."""
    url = f"https://www.youtube.com/watch?v={vid}&t={start}s"
    if clip:
        poster = "media/refs/clips/" + Path(clip).stem + ".jpg"
        return (f'<figure class="vid src-vid"><video class="auto" src="{e(clip)}" poster="{e(poster)}" muted loop playsinline preload="none" disablepictureinpicture></video>'
                f'<figcaption class="cap"><a href="{e(url)}" target="_blank" rel="noopener">{cap} · YouTube</a></figcaption></figure>')
    n = vid.replace("-", "_", 1) if vid.startswith("-") else vid
    return (f'<figure class="yt"><a href="{e(url)}" target="_blank" rel="noopener"><img src="media/refs/yt-{e(n)}.jpg" loading="lazy" alt="">'
            f'<span class="play"><img src="media/refs/youtube.svg" alt=""> {e(cap)}</span></a></figure>')


def model(mid, cap, h=360, attrs=""):
    m = MODELS.get(mid)
    if not m:
        MISSING.append(mid); return ""
    anim = " autoplay" if m.get("animations") else ""
    return (f'<figure class="model"><model-viewer src="{e(m["file"])}" poster="{e(m["poster"])}" alt="{e(m["title"])}" loading="lazy" reveal="auto" '
            f'camera-controls touch-action="pan-y" {anim} interaction-prompt="none" shadow-intensity="0.5" exposure="1.1" environment-image="neutral" style="height:{h}px" {attrs}></model-viewer>'
            f'<figcaption class="cap">{cap}</figcaption></figure>')


def video(src, poster, cap):
    return f'<figure class="vid"><video class="auto" src="{e(src)}" poster="{e(poster)}" muted loop playsinline preload="none" disablepictureinpicture></video><figcaption class="cap">{cap}</figcaption></figure>'


def fig(src, cap):
    return f'<figure class="fig"><img src="{e(src)}" loading="lazy" alt=""><figcaption class="cap">{cap}</figcaption></figure>'


def source(avatar, channel, title, vid, bullets, changed):
    b = "".join(f"<li>{e(x)}</li>" for x in bullets)
    return f"""<div class="src">
<div class="who"><img src="{e(avatar)}" alt=""><div><b>{e(channel)}</b><span>{e(title)}</span></div><img class="ytm" src="media/refs/youtube.svg" alt="YouTube"></div>
<ul class="facts">{b}</ul>
<p class="changed">{e(changed)}</p>
</div>"""


def bars(items):
    out = []
    for name, score, why in items:
        out.append(f'<li><div class="row"><b>{e(name)}</b><code>{score}/10</code></div><div class="track"><i style="--w:{score*10}%"></i></div><small>{e(why)}</small></li>')
    return '<ul class="bars">' + "".join(out) + "</ul>"


def mini(items):
    out = "".join(f'<li><span>{e(n)}</span><div class="track"><i style="--w:{s*10}%"></i></div><code>{s}</code><small>{e(w)}</small></li>' for n, s, w in items)
    return f'<ul class="mini">{out}</ul>'


def steps(items):
    return '<ol class="steps">' + "".join(
        f'<li><div class="ic"><span class="n">{i+1}</span></div><div><b>{e(t)}</b><small>{e(d)}</small></div><code>{e(c)}</code></li>'
        for i, (t, d, c) in enumerate(items)) + "</ol>"


def rows(items):
    return '<ul class="rows plain">' + "".join(f"<li>{e(t)} <code>{e(c)}</code></li>" for t, c in items) + "</ul>"


def dated_rows(items):
    return '<ul class="rows">' + "".join(f'<li><div><time>{e(d)}</time><span>{e(t)}</span><code>{e(c)}</code></div></li>' for d, t, c in items) + "</ul>"


CLT = ("media/refs/court-level-tennis.jpg", "Court Level Tennis")
SMT = ("media/refs/slow-mo-tennis.jpg", "Slow-Mo Tennis")
CAST = 'camera-orbit="25deg 80deg 3.2m" camera-target="0m 0.95m 0m"'

S = []

S.append(f"""<section aria-labelledby="h-stand">
<h2 id="h-stand">Where it stands</h2>
<p class="sub">Judged on the viewing result, not a measured match. The bar is how close it looks to real; the line under it is why it is not a 10.</p>
{bars([
 ("Body motion", 8, "FlowHMR from one camera. Depth is monocular and no physics ran, so feet can slide and a cropped toss loses height."),
 ("Ball", 8, "Found in frame and the arcs are authored to the motion's events. Not spin, not measured 3D flight."),
 ("Racket model", 7, "Traced outline, woven strings, drilled grommets. Depth and sidewalls are approximate, not CAD."),
 ("Racket motion", 6, "Solved through the arm. At 30 fps the detector sees the racket in only 32–40% of frames; at 120 fps, 81%. Face angle at contact is set by rule."),
 ("Skin and face, Meshy", 5, "Outfit and surface read well. Heads were rejected as likeness and hands came out as mittens."),
 ("Body shape of the person", 2, "Everyone shares the FlowHMR body. The Rodin bodies that fix this are paused for wrinkles and a bent spine."),
 ("Skin and face, FlowHMR", 2, "A plain grey body."),
 ("Face likeness", 2, "Rodin, UP2You and Meshy all generate a face. None is the person, and no vendor promises one from two or three photos."),
])}
<p class="cap">gold standard · Hawk-Eye SkeleTRACK, 29 body points and 7 racket points from stadium cameras</p>
</section>""")

S.append(f"""<section aria-labelledby="h-body">
<h2 id="h-body">1 · Body motion</h2>
<p class="sub">FlowHMR on Modal turns one clip into joints, shape and camera per frame. What you get depends on the footage, so this is organised by footage. Every scene below is the real one: drag to orbit, pinch to zoom, use the camera buttons, play the footage beside it.</p>
{steps([("Clip","one point, cut from YouTube","yt-dlp"),("Body","joints, shape, camera per frame","FlowHMR · Modal"),("Court","align the body to the court lines","Python"),("Scene","body, racket, ball on the court","three.js")])}

{source(*CLT, "Ben Shelton serving up close · court level practice 2025", "vF9WB1ZhgsI",
        ["camera: low, directly behind the server", "4K 60 fps, 1080p 30 fps into the model", "player about 490 px tall in frame"],
        "The best footage of the project. Low and behind means the body is big and the swing plane is visible; this is the recipe every later point reuses.")}
{yt("vF9WB1ZhgsI", 26, 32, "the source · 26–32 s", clip="lab/media/sources/shelton-serve.mp4")}
{lab("shelton-serve", "the first accepted motion · Oct 22 · same clip, as the scene")}
{review("shelton-serve-d", "the same serve in the 16-point library · racket solved through the arm, ball authored · 4.7 px median")}

{source(*SMT, "Ben Shelton practice set with Federico Coria · 4K 60 fps", "cDV-pQCJkP4",
        ["camera: low behind the baseline, both players in frame", "4K 60 fps, 1080p 30 fps into the model", "serve contact partly above the frame"],
        "The only two-player point: serve out wide from the deuce side, approach, volley. Both bodies from one camera; the far player and hidden hands are less reliable. This is the point on the USTA page.")}
{yt("cDV-pQCJkP4", 101, 109, "the source · 1:41.5–1:48.5", clip="lab/media/sources/shelton-coria.mp4")}
{lab("shelton-coria", "serve and volley · both players · the whole point")}
{lab("shelton-long-rally", "14 seconds of rally from the same set · drift and hidden hands show over time")}

{source(*CLT, "Alcaraz vs Perricard · court-level matchplay 2025", "9Dl84UYDks0",
        ["camera: low behind the near player", "4K 60 fps", "two players, served points with groundstrokes"],
        "Same recipe on matchplay. Serves and groundstrokes come through; the racket blurs at the fastest frames because this is 30 fps into the model.")}
{yt("9Dl84UYDks0", 586, 601, "the source · 586–600 s", clip="review/data/alcaraz-a-source.mp4")}
{review("alcaraz-a", "Alcaraz · serve at frame 249, two-handed backhand at 303 · 10.9 px")}
{review("alcaraz-serve", "Mpetshi Perricard · 2.03 m in life, 1.82 m in the model: the shared body")}

{source(*CLT, "Cobolli vs Sinner · court-level practice set 2026", "D6wCPsoAd58",
        ["camera: low behind the near player", "4K 60 fps", "returns and served points"],
        "Returns are the cleanest: a compact swing in front of the body, 4.8 px median on Cobolli.")}
{yt("D6wCPsoAd58", 109, 119, "the source · 109–119 s", clip="review/data/sinner-return-source.mp4")}
{review("sinner-return", "Sinner return · 293 frames · 10.7 px")}
{review("cobolli-c1", "Cobolli · serve, then three topspin contacts · 7.0 px")}

{source("media/refs/focused-tennis.jpg", "FocusedTennis", "Djokovic · 2024 Indian Wells practice match, court level 4K 60 fps", "xsP3PjNgId8",
        ["camera: court level behind the player", "4K 60 fps", "one-handed slices at frames 145 and 312"],
        "Djokovic's slices were first labelled topspin; the contact rule needs the shot type right, so these were relabelled by eye.")}
{yt("xsP3PjNgId8", 399, 414, "the source · 399–413 s", clip="review/data/djokovic-iw-a-source.mp4")}
{review("djokovic-iw-a", "Djokovic IW-A · forehand, slice, forehand · 9.0 px")}

{source("media/refs/courtleveltv-tennis5245.jpg", "Court Level TV", "Djokovic and Auger-Aliassime · ATP Finals Turin 2022 practice, 4K 60 fps", "-KoAgZkCIx8",
        ["camera: low behind the baseline", "4K 60 fps", "a return point"],
        "A clean return: 5.7 px median, the best Djokovic fit.")}
{yt("-KoAgZkCIx8", 29, 42, "the source · 29–42 s", clip="review/data/djokovic-turin-return-source.mp4")}
{review("djokovic-turin-return", "Djokovic Turin return · 366 frames · 5.7 px")}

{source("media/refs/tennistv.jpg", "Tennis TV", "Shelton vs Nakashima · Indian Wells 2025 highlights", "tQdVQu-CQwQ",
        ["camera: elevated broadcast, full court", "1080p 50 fps into 1080p 30 fps", "player about 220 px tall"],
        "A body, but no usable wrist or face: the player is too small. Kept as a benchmark for court-pattern context only.")}
{yt("tQdVQu-CQwQ", 16, 22, "the source · 16.4–22 s", clip="lab/media/sources/shelton-atp.mp4")}
{lab("shelton-atp", "ATP broadcast · body only · no racket, ball or opponent solved")}

{source("media/refs/ucla-tennis-consulting.jpg", "UCLA Tennis Consulting", "Spencer Johnson (UCLA) vs Samir Banerjee (Stanford) · PlaySight", "ot8tSR3q9gI",
        ["camera: fixed club camera behind the baseline", "1080p 30 fps", "one indexed point, charted shots"],
        "The only clip with a charted ball: tagged contacts and bounces from a Stanford dataset give the arcs; no racket solve.")}
{yt("ot8tSR3q9gI", 300, 309, "the source · 5:00–5:09", clip="lab/media/sources/ucla-point8.mp4")}
{lab("ucla-point8", "college match · body plus charted ball arcs")}
</section>""")

S.append(f"""<section aria-labelledby="h-racket">
<h2 id="h-racket">2 · Racket</h2>
<p class="sub">Three parts: a model, a detector, and a solver that moves the model through the arm. The weakest link is the footage frame rate.</p>
{steps([("Model","trace the outline, author strings, grommets, grip","Blender"),("Detect","five racket keypoints per frame where visible","RacketVision · Modal"),("Solve","through forearm and wrist, spin capped at 2,500°/s","Python"),("Pin contact","label 34 contacts, hold the face angle","by eye")])}
{model("racket-arm-solved", "the rebuilt racket · frame, throat, grommets, woven strings, grip · drag to inspect", h=380, attrs='camera-orbit="30deg 70deg 1.1m" auto-rotate')}
{mini([("outline", 8, "traced from manufacturer photos"), ("strings and grommets", 8, "woven bed, every string through its own hole"), ("depth and sidewalls", 5, "approximate, not CAD"), ("paint and decals", 6, "authored, not scanned")])}

{source(*SMT, "Carlos Alcaraz · forehand and backhand · slow motion 4K 120 fps", "-Eu80hGbgVA",
        ["camera: court level, side-rear", "4K 120 fps: the only high-frame-rate clip", "7 s of rallying"],
        "At 30 fps a fast swing is a blur and the detector loses the racket exactly at contact. At 120 fps it keeps it through contact and the follow-through: 81% of frames found against 32–40%. The single largest gain, and it cost nothing.")}
{yt("-Eu80hGbgVA", 0, 30, "the source · 120 fps", clip="review/data/alcaraz-hfr-source.mp4")}
{review("alcaraz-hfr", "Alcaraz forehand at 120 fps · racket through contact, 15.5 px on held-out frames")}
{fig("media/racket/ovl-djokovic-iw-a.jpg", "solved through the arm · red: old free-wrist fit · green: arm solve · cyan: detections")}
{fig("media/racket/edge-before-after.jpg", "face angle at contact · top: before, 35–70° open · bottom: after the rule, near vertical")}
{mini([("racket found, 30 fps", 4, "32–40% of frames"), ("racket found, 120 fps", 8, "81% of frames"), ("fit where seen", 7, "4.7–12.5 px median per point"), ("face angle at contact", 5, "set by rule, not measured: from behind, open and closed look the same")])}
</section>""")

S.append(f"""<section aria-labelledby="h-ball">
<h2 id="h-ball">3 · Ball</h2>
<p class="sub">No model tracks the ball in 3D from one camera here. The ball is authored to events read off the motion: toss release, contact at the racket head, a landing inside the box, the next racket.</p>
{model("ball-usopen", "the Wilson US Open ball · 6.7 cm · felt, seam and print authored from reference photos", h=320, attrs='camera-orbit="40deg 70deg 0.3m" auto-rotate')}
{lab("shelton-coria", "the point with the ball · toss, serve out wide, return, volley")}
{mini([("in hand through the toss", 9, "attached to the tossing hand"), ("leaves the strings at contact", 9, "at the racket head"), ("lands where it should", 7, "inside the deuce box; the exact spot is modelled"), ("spin and true 3D flight", 2, "not measured")])}
</section>""")

S.append(f"""<section aria-labelledby="h-look">
<h2 id="h-look">4 · Appearance</h2>
<p class="sub">Three ways to put a person on the motion. Each is scored the same way: motion is inherited, body and face are the generator's.</p>
<h3>Plain FlowHMR body</h3>
{lab("shelton-serve", "the shared grey body · what every point uses today", camera="front")}
{mini([("motion", 8, "FlowHMR"), ("body shape", 2, "one body for everyone"), ("face", 1, "none"), ("clothes", 1, "none")])}
<h3>Rodin body from three frames</h3>
{model("rodin-shelton", "Shelton · Rodin 2.5 through fal.ai from three frames of the same video · about $0.40", h=440, attrs=CAST)}
{video("media/bodies/shelton-serve-fal.mp4", "media/bodies/shelton-serve-fal-poster.jpg", "the same body on the serve · motion unchanged")}
{mini([("motion", 8, "inherited from FlowHMR"), ("body shape", 6, "outfit matches, build close; the tank top is part of the mesh and bulges"), ("face", 2, "generated, not Shelton"), ("hands", 3, "the generated hand stays open under the grip")])}
<h3>Meshy likeness</h3>
{model("shelton-2", "Shelton · Meshy 7.1 from a four-view A-pose sheet · the figure the USTA page used before the rebuild", h=440, attrs=CAST)}
{mini([("motion", 5, "library idles and mocap strokes, no finger bones"), ("body shape", 6, "a tennis player, not this one"), ("face", 3, "reads as a game character"), ("hands", 2, "mittens")])}
{rows([("Eight Rodin bodies built; all paused for wrinkles, bent spine, changed height", "paused"), ("UP2You and MICA face fits rejected at 2/10 and 4/10", "rejected"), ("Three Meshy heads on the serve body: detached", "rejected")])}
</section>""")

S.append(f"""<section aria-labelledby="h-scenes">
<h2 id="h-scenes">5 · Scenes and cast</h2>
<p class="sub">The venues are data, not generated images: OpenStreetMap footprints, USGS terrain, an aerial photo, Poly Haven props, built in code. Meshy made the people. The USTA page plays the serve-and-volley point inside the stadium.</p>
{model("shelton-coria-point", "the USTA opener scene · both players, grey, with the Wilson ball", h=440, attrs='camera-target="12m 1m -0.8m" camera-orbit="215deg 78deg 7m" min-camera-orbit="auto auto 2m" max-camera-orbit="auto auto 40m"')}
{fig("media/venues/usta-sheet.jpg", "US Open · Arthur Ashe and Flushing Meadows from OSM and code")}
{fig("media/venues/ucla-full.jpg", "UCLA · real terrain, aerial photo ground, 52k trees placed from its near-infrared band")}
{fig("media/venues/galaxy-full.jpg", "Galaxy, Kings, Reign · Dignity Health Sports Park from OSM, Poly Haven props")}
<h3>The Meshy cast</h3>
{model("gauff-2", "Coco Gauff · Meshy likeness v2", h=400, attrs=CAST)}
{model("martin", "Billy Martin · UCLA head coach · live", h=400, attrs=CAST)}
{model("jerry", "Jerry · four-photo rebuild · live on all three pages", h=400, attrs=CAST)}
{model("umpire", "chair umpire · from a text prompt", h=400, attrs=CAST)}
{model("sp-1", "seated spectator · remeshed to 1.5k polys for the crowd", h=360, attrs='camera-orbit="25deg 80deg 3m" camera-target="0m 0.8m 0m"')}
{mini([("speed", 9, "about 44 credits and minutes per figure"), ("consistency", 8, "one style across 30 figures"), ("likeness", 3, "heads rejected"), ("hands", 2, "mittens")])}
</section>""")

S.append(f"""<section aria-labelledby="h-goat">
<h2 id="h-goat">6 · The goat and the mountain</h2>
<p class="sub">The home-page intro animal and wallpaper.</p>
{model("goat-loader", "dot goat · a CC0 goat reshaped in Blender · the default intro", h=380, attrs='auto-rotate')}
{model("toy-ibex", "toy ibex · nano-banana still → Tripo mesh · a style variant", h=380, attrs='auto-rotate')}
{model("toy-mountain", "toy mountain · nano-banana still → Tripo · the one generated 3D set", h=380, attrs='auto-rotate')}
{fig("media/loader/mountain-flux-outpaint.jpg", "home-page mountain · an ink painting extended by FLUX outpainting, original pixels unchanged")}
{mini([("goat silhouette", 8, "reads as an ibex at a glance"), ("toy ibex", 7, "good toy, not the brand"), ("photoreal ibex", 5, "Hunyuan3D, hooves fine, fur flat"), ("generated backdrops", 2, "feel like greenscreen, rejected")])}
</section>""")

S.append(f"""<section aria-labelledby="h-films">
<h2 id="h-films">7 · Films</h2>
<p class="sub">HyperFrames renders HTML to video frame by frame in headless Chrome. Every hub clip and film came from it.</p>
{video("media/hyperframes/cycling-film.mp4", "media/hyperframes/cycling-film-poster.jpg", "cycling film · 17 s")}
{video("media/hyperframes/reel-v3.mp4", "media/hyperframes/reel-v3-poster.jpg", "sports data reel · 31 s")}
{video("media/hyperframes/radio-captions.mp4", "media/hyperframes/radio-captions-poster.jpg", "radio · word-by-word captions")}
{video("media/thumbs/final-galaxy.mp4", "media/thumbs/final-galaxy-poster.jpg", "Galaxy card · chosen from 140 options")}
</section>""")

S.append(f"""<section aria-labelledby="h-dropped">
<h2 id="h-dropped">Tried and dropped</h2>
{rows([("Kling 3.0 motion-control video failed the anatomy gate", "fal.ai"), ("GEM-X and Kimodo mocap loops, none adopted", "Modal"), ("Rodin granite crag: a marble column", "fal.ai"), ("nano-banana backdrops: greenscreen", "fal.ai"), ("Internally generated mountain wings and pinnacle", "image")])}
</section>""")

S.append(f"""<section aria-labelledby="h-time">
<h2 id="h-time">Timeline</h2>
{dated_rows([("Sep 16","First tennis figure: Meshy 6 Lite from a generated reference","Meshy"),("Oct 19–21","Meshy cast, crowds and props for the story pages; Kling video fails","Meshy · fal"),("Oct 22","First FlowHMR run; Shelton serve accepted","Modal"),("Oct 23–26","Rallies, two-player point, broadcast and college benchmarks; Meshy heads rejected; rackets traced","Modal"),("Oct 27","Rodin bodies through fal.ai; 4K crop; face fits rejected","fal"),("Oct 28","16-point library; racket through the arm; 120 fps forehand; 34 contacts pinned","local"),("Oct 29–30","USTA opener rebuilt on the serve-and-volley point; serve kept behind the baseline; live","live")])}
<p class="cap">next · 120 fps footage only · racket silhouette in the lag phase · a hand model · ground truth under 5 px · a body and face that are the person</p>
</section>""")

S.append("""<section class="try" aria-label="Credits">
<footer>FlowHMR and RacketVision on Modal · Rodin, Tripo, Hunyuan3D, FLUX and nano-banana through fal.ai · Meshy · Blender · HyperFrames · footage belongs to Court Level Tennis, Slow-Mo Tennis, FocusedTennis, Court Level TV, Tennis TV and UCLA Tennis Consulting · depth is monocular, no physics · faces are generated, not likenesses</footer>
</section>""")

CSS = (ROOT / "writeup.css").read_text()
EXTRA = """
figure{margin:0}
h3{font-size:15px;font-weight:600;margin:28px 0 8px}
.fig img{display:block;width:100%;height:auto;border-radius:12px;border:1px solid var(--line);background:var(--fill)}
.vid video{display:block;width:100%;height:auto;border-radius:12px;border:1px solid var(--line);background:var(--fill)}
.model model-viewer{display:block;width:100%;height:360px;border-radius:12px;border:1px solid var(--line);background:var(--fill);--poster-color:transparent}
.scene iframe{display:block;width:100%;border:1px solid var(--line);border-radius:12px;background:var(--fill)}
.yt a{display:block;position:relative;text-decoration:none}
.yt img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:12px;border:1px solid var(--line)}
.yt .play{position:absolute;left:10px;bottom:10px;display:flex;align-items:center;gap:6px;font:11px var(--mono);color:#fff;background:rgba(0,0,0,.55);border-radius:999px;padding:5px 10px}
.yt .play img{width:16px;height:16px;border:0;border-radius:0;aspect-ratio:auto}
.src{border:1px solid var(--line);border-radius:12px;padding:12px;margin-top:28px}
.who{display:grid;grid-template-columns:44px 1fr 24px;gap:10px;align-items:center}
.who>img:first-child{width:44px;height:44px;border-radius:50%;object-fit:cover}
.who b{display:block;font-weight:600}.who span{display:block;color:var(--muted);font-size:12.5px;line-height:1.3}
.who .ytm{width:24px;height:24px}
.facts{margin:10px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:3px}
.facts li{font:11px/1.4 var(--mono);color:var(--muted)}
.facts li::before{content:"· "}
.changed{margin:10px 0 0;font-size:13px}
.bars,.mini{list-style:none;margin:0;padding:0}
.bars li{padding:10px 0;border-bottom:1px solid var(--line)}
.bars .row{display:flex;justify-content:space-between;align-items:baseline}
.bars b{font-weight:600}.bars code,.mini code{font:12px var(--mono);color:var(--muted)}
.track{height:6px;background:var(--fill);border-radius:99px;overflow:hidden;margin:6px 0}
.track i{display:block;height:100%;width:0;background:var(--accent);border-radius:99px;transition:width .9s cubic-bezier(.2,.7,.2,1)}
.on .track i{width:var(--w)}
.bars small{display:block;color:var(--muted);font-size:12.5px;line-height:1.35}
.mini{margin-top:10px}
.mini li{display:grid;grid-template-columns:150px 1fr 28px;gap:8px;align-items:center;padding:5px 0}
.mini span{font-size:13px}.mini .track{margin:0}.mini code{text-align:right}
.mini small{grid-column:1/-1;color:var(--muted);font-size:12px;line-height:1.3;margin:-2px 0 2px}
.steps .ic .n{font:12px var(--mono);color:var(--fg)}
section > .model, section > .vid, section > .fig, section > .rows, section > .bars, section > .scene, section > .yt{margin-top:16px}
.src + .yt, .src + .vid{margin-top:12px}
.src-vid .cap a{text-decoration:none}
@media (prefers-reduced-motion:reduce){.track i{transition:none}}
"""

page = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Video to Motion</title>
<meta name="description" content="How tennis video became 3D motion, a racket, a ball and a person: what each step can do today, scored honestly, with every scene interactive.">
<meta property="og:title" content="Video to Motion"><meta property="og:description" content="Tennis video to 3D motion, racket, ball and person. Every scene interactive, every result scored.">
<style>{CSS}{EXTRA}</style>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@4.1.0/dist/model-viewer.min.js"></script>
</head><body>
<main class="col">
<div class="made"><a href="https://jerrythegoat.com/">jerrythegoat.com</a> · notes</div>
<header><h1>Video to Motion</h1><p>How one YouTube clip becomes a body, a racket, a ball and a person on a court. What each step can do today, scored honestly, with every scene live on this page.</p></header>
{''.join(S)}
</main>
<script>
(function(){{
  customElements.whenDefined('model-viewer').then(function(){{customElements.get('model-viewer').meshoptDecoderLocation='https://cdn.jsdelivr.net/npm/meshoptimizer@0.22.0/meshopt_decoder.js';}});
  var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('on');io.unobserve(x.target);}}}});}},{{threshold:.3}});
  document.querySelectorAll('.bars li, .mini').forEach(function(el){{io.observe(el);}});
  var vids=[].slice.call(document.querySelectorAll('video.auto'));
  var vo=new IntersectionObserver(function(es){{es.forEach(function(x){{var v=x.target;if(x.isIntersecting){{if(v.preload==='none'){{v.preload='auto';v.load();}}v.play().catch(function(){{}});}}else{{v.pause();}}}});}},{{rootMargin:'160px 0px'}});
  vids.forEach(function(v){{vo.observe(v);}});
}})();
</script>
</body></html>
"""
(ROOT / "index.html").write_text(page)
print("wrote index.html", len(page), "bytes; missing models:", sorted(set(MISSING)))
