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

LABCAM = json.loads((ROOT / "media/data/lab-cams.json").read_text())
REVCAM = json.loads((ROOT / "media/data/review-cams.json").read_text())


def scene(params, cap="", h=720):
    src = "scene/?" + "&".join(f"{k}={v}" for k, v in params.items())
    c = f'<figcaption class="cap">{cap}</figcaption>' if cap else ""
    return f'<figure class="scene"><iframe data-src="{e(src)}" title="{e(cap or params.get("m",""))}" allow="autoplay" style="height:{h}px"></iframe>{c}</figure>'


def lab(match, cap="", h=720, ball=None, cam=None):
    """A Tennis Lab point in the gallery's own viewer: footage above, court below, starts at the source camera."""
    L = LABCAM[match]; rx, ry, rz = L["roots"][0][1]
    cx, cy, cz = cam or (-0.03, 2.4, 7.71)
    p = {"m": L["glb"], "v": f"../lab/media/sources/{match}.mp4", "court": 1, "fov": 20,
         "cp": f"{rx+cx:.2f},{ry+cy:.2f},{rz+cz:.2f}", "ct": f"{rx:.2f},1.0,{rz-0.6:.2f}"}
    if ball: p["ball"] = ball
    return scene(p, cap, h)


def review(point, cap="", h=640):
    R = REVCAM[point]; cx, cy, cz = R["cam"]; px, py, pz = R["pelvis"]
    # the review footage is a crop around the player, so keep the source camera's line of sight but come in closer
    k = 0.42; cx, cy, cz = px + (cx - px) * k, py + (cy - py) * k, pz + (cz - pz) * k
    p = {"m": f"lib-{point}", "v": f"../review/data/{point}-source.mp4", "fov": 36, "cp": f"{cx:.2f},{cy:.2f},{cz:.2f}", "ct": f"{px:.2f},{py:.2f},{pz:.2f}"}
    if point == "alcaraz-hfr": p["vs"] = 0.5   # 120 fps motion over 60 fps slow-motion footage
    return scene(p, cap, h)


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


SPIN = [("shelton-serve-b","Shelton serve B",4841,2039),("shelton-serve-d","Shelton serve D",1313,2154),("shelton-serve-f","Shelton serve F",772,1287),("shelton-serve-g2","Shelton serve G2",694,1215),
        ("alcaraz-serve","Perricard point",1654,1770),("sinner-return","Sinner return",5397,1859),("djokovic-turin-return","Djokovic Turin",4295,1729),("djokovic-iw-a","Djokovic IW-A",4666,1226),
        ("djokovic-iw-c","Djokovic IW-C",1893,2461),("alcaraz-a","Alcaraz A",5112,1926),("alcaraz-b","Alcaraz B",2509,2968),("cabolli-return","Cobolli return",293,592),
        ("cobolli-b1","Cobolli B1",1946,2148),("cobolli-b2","Cobolli B2",4286,2133),("cobolli-c1","Cobolli C1",2431,2077),("cobolli-c2","Cobolli C2",1862,1902)]
# face angle at contact, degrees: negative closed, positive open (from the 34 labelled contacts)
CONTACTS = [("Shelton B 134","serve",18,-15),("Shelton D 120","serve",14,-15),("Shelton F 117","serve",30,-14),("Shelton G2 120","serve",-21,-15),
            ("Perricard 92","serve",-23,-15),("Perricard 148","topspin",-23,-5),("Perricard 221","topspin",5,-15),
            ("Sinner 82","topspin",-82,-15),("Sinner 159","topspin",2,2),("Sinner 230","topspin",60,-4),
            ("Djokovic Turin 134","topspin",35,-4),("Djokovic Turin 216","topspin",47,2),
            ("Djokovic IW-A 78","topspin",-47,-15),("Djokovic IW-A 145","topspin",35,2),("Djokovic IW-A 328","topspin",-44,-15),
            ("Djokovic IW-C 10","topspin",70,2),("Djokovic IW-C 169","topspin",46,2),("Djokovic IW-C 242","topspin",-2,-7),("Djokovic IW-C 312","topspin",59,-3),
            ("Alcaraz A 249","serve",-25,-11),("Alcaraz A 303","topspin",38,2),("Alcaraz B 177","serve",-11,-2),("Alcaraz B 238","topspin",-41,-15),
            ("Cobolli B1 8","serve",-2,1),("Cobolli B1 62","topspin",23,-10),("Cobolli B1 133","topspin",12,-2),
            ("Cobolli B2 147","serve",19,10),("Cobolli B2 202","topspin",22,-11),("Cobolli B2 276","topspin",-2,-1),
            ("Cobolli C1 66","serve",-3,-14),("Cobolli C1 124","topspin",26,2),("Cobolli C1 200","topspin",-32,-15),("Cobolli C1 278","topspin",-6,-8),("Cobolli C2 77","serve",-16,-11)]

def chart(kind, data, cap, extra=""):
    return f'<figure class="chart"><div class="d3" data-chart="{kind}" data-json=\'{json.dumps(data)}\' {extra}></div><figcaption class="cap">{cap}</figcaption></figure>'


def refs(items):
    return '<ul class="scores">' + "".join(f'<li><img src="{e(i)}" loading="lazy" alt=""><div><b>{e(n)}</b><small>{e(l)}</small></div><code>{e(c)}</code></li>' for i, n, l, c in items) + "</ul>"


S = []

# ---------- hero ----------
S.append(f"""<section aria-label="Hero" class="hero">
{lab("shelton-coria", "", h=720, ball="auto")}
<p class="cap">Ben Shelton, serve and volley · drag to orbit · the footage above drives the scene</p>
</section>""")

# ---------- 1 plan ----------
S.append(f"""<section aria-labelledby="h-plan">
<h2 id="h-plan">1 · The plan</h2>
<p class="sub">Take one YouTube clip of a point and get back a 3D body, racket and ball on a court that a viewer can orbit. No markers, no multi-camera rig, no paid capture.</p>
{steps([("Clip","one point, cut from a court-level YouTube video","yt-dlp"),("Body","joints, shape and camera per frame from the single view","FlowHMR · Modal"),("Racket","five keypoints per frame, then a racket moved through the arm","RacketVision + solver"),("Ball","authored to the motion's events: toss, contact, bounce, next racket","Python"),("Person","a body and face that are the player","Rodin · Meshy"),("Scene","court, stadium, crowd; interactive on the web","three.js")])}
<p class="cap">done looks like: the point plays from any angle and matches the footage frame for frame</p>
</section>""")

# ---------- 2 examples ----------
S.append(f"""<section aria-labelledby="h-ex">
<h2 id="h-ex">2 · Examples</h2>
<p class="sub">Three more points, each with the original footage inside the scene. Press Front, Side or Top; scrub the time.</p>
{review("shelton-serve-d", "Shelton serve · 3.8 px median racket error")}
{review("alcaraz-hfr", "Alcaraz forehand at 120 fps · the racket stays through contact")}
{review("djokovic-turin-return", "Djokovic return · 5.7 px, the cleanest groundstroke")}
</section>""")

# ---------- 3 research ----------
S.append(f"""<section aria-labelledby="h-res">
<h2 id="h-res">3 · Research</h2>
<p class="sub">How the best systems do it, and what one camera can do in 2026.</p>
{refs([("media/refs/hawkeye-skeletrack.jpg","Hawk-Eye SkeleTRACK","29 body points and 7 racket points from 10–14 stadium cameras; used since the 2024 Laver Cup. The gold standard, and private.","stadium"),
       ("media/refs/flowhmr-teaser.jpg","FlowHMR","body motion from one camera; 82% physical tracking success on Wild-4K in its paper, 63% for the next best. What we use.","1 camera"),
       ("media/refs/racketvision-teaser.jpg","RacketVision, AAAI 2026","five racket keypoints per frame from broadcast clips; 89.6% correct on tennis, side points weakest at 80%. What we use.","1 camera"),
       ("media/logos/hyper3d.png","Rodin 2.5","a whole clothed body from two or three photos; no likeness promised. Tried.","photos"),
       ("media/logos/meshy.png","Meshy 7.1","image to 3D with a rig in minutes; faces flatten and fingers fuse, by its own help page. Tried.","image")])}
<p class="cap">games like TopSpin 2K25 record players in mocap suits; nobody has a solved single-camera racket</p>
<h3>Where it stands</h3>
{bars([
 ("Body motion", 8, "FlowHMR from one camera. Depth is monocular and no physics ran, so feet can slide and a cropped toss loses height."),
 ("Ball", 8, "Authored to the motion's events; lands where it should. Not spin, not measured 3D flight."),
 ("Racket model", 7, "Traced outline, woven strings, drilled grommets. Depth and sidewalls approximate."),
 ("Racket motion", 6, "Solved through the arm. At 30 fps the detector sees the racket in 32–40% of frames; at 120 fps, 81%. Face angle at contact is set by rule."),
 ("Skin and face, Meshy", 5, "Outfit and surface read well. Heads rejected as likeness, hands came out as mittens."),
 ("Body shape of the person", 2, "Everyone shares the FlowHMR body. The Rodin bodies that fix this are paused."),
 ("Face likeness", 2, "Rodin, UP2You and Meshy all generate a face. None is the person."),
])}
</section>""")

# ---------- 4 footage ----------
S.append(f"""<section aria-labelledby="h-src">
<h2 id="h-src">4 · Where the videos come from, and why quality differs</h2>
<p class="sub">Same model every time. The camera and the frame rate decide the result.</p>

{source(*CLT, "Ben Shelton serving up close · court level practice 2025", "vF9WB1ZhgsI",
        ["camera: low, directly behind the server", "4K 60 fps · 1080p 30 fps into the model", "player about 490 px tall in frame"],
        "The best footage of the project: low and behind means the body is big and the swing plane is visible. This is the recipe every later point reuses.")}
{lab("shelton-serve", "the first accepted motion, Oct 22")}

{source(*SMT, "Ben Shelton practice set with Federico Coria · 4K 60 fps", "cDV-pQCJkP4",
        ["camera: low behind the baseline, both players in frame", "4K 60 fps · 1080p 30 fps into the model", "serve contact partly above the frame"],
        "The only two-player point. Both bodies from one camera; the far player and hidden hands are less reliable.")}
{lab("shelton-long-rally", "14 seconds of rally · drift and hidden hands show over time")}

{source(*CLT, "Alcaraz vs Perricard · court-level matchplay 2025", "9Dl84UYDks0",
        ["camera: low behind the near player", "4K 60 fps", "served points with groundstrokes"],
        "Same recipe on matchplay. The racket blurs at the fastest frames because this is 30 fps into the model.")}
{review("alcaraz-a", "Alcaraz · serve at frame 249, two-handed backhand at 303 · 10.9 px")}

{source(*CLT, "Cobolli vs Sinner · court-level practice set 2026", "D6wCPsoAd58",
        ["camera: low behind the near player", "4K 60 fps", "returns and served points"],
        "Returns are the cleanest: a compact swing in front of the body, 4.8 px median on Cobolli.")}
{review("sinner-return", "Sinner return · 293 frames · 10.7 px")}

{source("media/refs/focused-tennis.jpg", "FocusedTennis", "Djokovic · 2024 Indian Wells practice match, court level 4K 60 fps", "xsP3PjNgId8",
        ["camera: court level behind the player", "4K 60 fps", "one-handed slices at frames 145 and 312"],
        "The slices were first labelled topspin; the contact rule needs the shot type right, so they were relabelled by eye.")}
{review("djokovic-iw-a", "Djokovic IW-A · forehand, slice, forehand · 9.0 px")}

{source(*SMT, "Carlos Alcaraz · forehand and backhand · slow motion 4K 120 fps", "-Eu80hGbgVA",
        ["camera: court level, side-rear", "4K 120 fps: the only high-frame-rate clip", "7 s of rallying"],
        "At 30 fps a fast swing is a blur and the detector loses the racket at contact. At 120 fps it keeps it through contact and the follow-through. The single largest gain, and it cost nothing.")}
{chart("bars", {"rows":[{"label":"Djokovic IW, 30 fps","value":36,"color":"#b4442c"},{"label":"Sinner, 30 fps","value":34,"color":"#b4442c"},{"label":"Alcaraz, 120 fps","value":81,"color":"#236442"}],"max":100,"unit":"%"}, "frames where the racket was found")}

{source("media/refs/tennistv.jpg", "Tennis TV", "Shelton vs Nakashima · Indian Wells 2025 highlights", "tQdVQu-CQwQ",
        ["camera: elevated broadcast, full court", "1080p 50 fps into 1080p 30 fps", "player about 220 px tall"],
        "A body, but no usable wrist or face: the player is too small. A benchmark for court-pattern context only.")}
{lab("shelton-atp", "ATP broadcast · body only", cam=(3.0, 9.0, 24.0))}

{source("media/refs/ucla-tennis-consulting.jpg", "UCLA Tennis Consulting", "Spencer Johnson (UCLA) vs Samir Banerjee (Stanford) · PlaySight", "ot8tSR3q9gI",
        ["camera: fixed club camera behind the baseline", "1080p 30 fps", "one indexed point, charted shots"],
        "The only clip with a charted ball: tagged contacts and bounces from a Stanford dataset give the arcs; no racket solve.")}
{lab("ucla-point8", "college match · body plus the charted ball")}
</section>""")

# ---------- 5 problems and fixes ----------
S.append(f"""<section aria-labelledby="h-fix">
<h2 id="h-fix">5 · Problems, and how each was fixed</h2>
<p class="sub">Every fix is measured on the same points before and after.</p>

<h3>The racket flipped at the wrist</h3>
<p>A racket seen from behind looks the same rotated 180° about its handle, so a free-wrist fit flipped the face between frames: up to 5,400°/s. The fix solves the arm instead of the racket: forearm twist and wrist angle per frame inside anatomical limits, smoothed, spin capped at 2,500°/s, the racket following the hand where the detector sees nothing.</p>
{chart("spin", {"rows":[{"point":p,"label":l,"before":b,"after":a} for p,l,b,a in SPIN]}, "fastest racket spin per point · red: free-wrist fit · green: solved through the arm · no frame over the cap on 15 of 16 points")}
{chart("trace", {"src":"media/data/racket-trace.json","key":"shelton-serve-d","label":"Shelton serve D · final fit, °/s per frame"}, "the same metric live: racket angular speed through the serve in section 2, frame by frame")}
{fig("media/racket/ovl-djokovic-iw-a.jpg", "red: old fit · green: arm solve · cyan: detections")}

<h3>The face was open at contact</h3>
<p>From behind, tilting the face open or closed shrinks its outline by the same amount, so five points cannot tell them apart. The first solves had the face 36° open at contact, which a topspin forehand cannot do. The fix labels every contact frame and shot type by eye and holds the face for ±3 frames: vertical to 15° closed for topspin, 15° closed to 10° open for a serve.</p>
{chart("contact", {"rows":[{"label":l,"shot":s,"before":b,"after":a} for l,s,b,a in CONTACTS],"band":[-15,10]}, "34 labelled contacts · red: before · green: after the rule · 7 plausible → 34 · the rule chose the angle, not the video")}
{fig("media/racket/edge-before-after.jpg", "camera looking along the face at contact · top: before · bottom: after")}

<h3>Why the racket still looks wrong, and what runs next</h3>
<p>The detailed racket mesh changed the look, not the motion: both fits share the same pose per frame. The motion is limited by the detector. RacketVision finds the racket in a third of 30 fps frames and its two side points, the ones that set the face, are its weakest at 80%. The next run uses the hand instead of the racket edges: a hand model gives the grip every frame, the racket is rigid in the grip, and the face at contact comes from the hand and the contact frame rather than a rule.</p>
{refs([("media/refs/next/wilor.jpg","WiLoR, CVPR 2025","hand detector and 3D hand mesh in one model, 5.5 mm on FreiHAND; frame by frame, no temporal part. Runs next on hand crops of every frame.","next"),
       ("media/refs/next/gigapose.jpg","GigaPose, CVPR 2024","6-DoF pose of a known mesh from one RGB frame, template matching; a coarse start for the racket on frames where it is visible.","next"),
       ("media/refs/next/caddie.jpg","CADDIE, CVPR 2026 workshop","golf club keypoints with the same five-point idea; detects on a subset of frames and interpolates between them by motion type.","pattern"),
       ("media/refs/next/egoxtreme.jpg","EgoXtreme, 2026","swung rackets and bats under blur: deblurring gave no gain, temporal tracking did. Preprocessing is the wrong place to spend.","finding")])}
<h3>The hand run, measured</h3>
<p>WiLoR ran on every frame of three points (A10G on Modal, 26 cents). It did not help: the hitting hand is 17 to 42 px wide and blurred, and the hand's orientation scattered by tens of degrees between two crops of the same frame. Every hand-driven variant lost to the current fit on every check. The useful finding came from the checks themselves: the racket is bolted to the body's 30 Hz wrist, so its head moves at 12 to 16 m/s where a real serve is 37 to 39 and a real forehand 33. The jitter and the slow swing are the body wrist, not the racket solve, and the next fix fits the racket to the detections between body samples instead of to the wrist.</p>
{video("media/racket/wilor-overlay-shelton.mp4", "media/racket/wilor-overlay-shelton-poster.jpg", "Shelton serve · red: free wrist · green: arm solve · blue: hand-driven · magenta: detections · yellow: the hand model")}
{chart("bars", {"rows":[{"label":"serve · real (Tubez)","value":38,"color":"#6e6e76"},{"label":"serve · arm solve","value":15.2,"color":"#236442"},{"label":"serve · hand-driven","value":17.6,"color":"#2d5fa6"},{"label":"forehand · real (Landlinger)","value":33,"color":"#6e6e76"},{"label":"forehand 120 fps · arm solve","value":11.8,"color":"#236442"},{"label":"return · real","value":33,"color":"#6e6e76"},{"label":"return · arm solve","value":15.8,"color":"#236442"}],"max":42,"unit":" m/s"}, "peak racket head speed · every fit sits at a third of the real number because the head follows the 30 Hz wrist")}
{chart("bars", {"rows":[{"label":"serve · free wrist","value":5.0,"color":"#b4442c"},{"label":"serve · arm solve","value":3.8,"color":"#236442"},{"label":"serve · hand-driven","value":34.1,"color":"#2d5fa6"},{"label":"forehand · free wrist","value":13.4,"color":"#b4442c"},{"label":"forehand · arm solve","value":11.3,"color":"#236442"},{"label":"forehand · hand-driven","value":39.5,"color":"#2d5fa6"},{"label":"return · free wrist","value":6.0,"color":"#b4442c"},{"label":"return · arm solve","value":4.7,"color":"#236442"},{"label":"return · hand-driven","value":27.3,"color":"#2d5fa6"}],"max":42,"unit":" px"}, "median racket error against the detections, on detected frames only · lower is better")}
<p class="cap">face at serve contact, read off the footage: near vertical, a few degrees closed · free wrist −6° · arm solve −3° · hand-driven +30°, the wrong way</p>

<h3>The server drifted inside the baseline</h3>
<p>FlowHMR carried Shelton about 1.1 m into the court by contact because the footage crops the toss. The fix counter-translates his root along the court during the serve so both feet stay behind the line, then blends out over the first approach steps; the return and the volley are untouched.</p>
{chart("bars", {"rows":[{"label":"hips at contact, before","value":10.76,"color":"#b4442c"},{"label":"hips at contact, after","value":11.54,"color":"#236442"},{"label":"baseline","value":11.885,"color":"#6e6e76"}],"max":12.5,"unit":" m"}, "court metres from the net · feet min 11.97 after the fix")}

<h3>No ball</h3>
<p>No model tracks the ball in 3D from one camera here, and the Tennis Lab export has none. The ball is authored to events read off the motion: in the tossing hand to release, contact at the racket head, a landing inside the box, the next racket. It is a Wilson US Open ball, 6.7 cm, rebuilt from product photos: seam fitted to the photo, felt, the Wilson and us open marks.</p>
{model("ball-usopen", "drag to inspect", h=300, attrs='camera-orbit="40deg 70deg 0.3m" auto-rotate')}
{mini([("in hand through the toss", 9, "attached to the tossing hand"), ("leaves the strings at contact", 9, "at the racket head"), ("lands where it should", 7, "inside the box; the exact spot is modelled"), ("spin and true 3D flight", 2, "not measured")])}

<h3>Before and after the rebuild</h3>
<div class="pair">
{scene({"m": "tennis-lab-shelton-serve", "court": 1, "fov": 24, "cp": "1.8,1.6,15.8", "ct": "0,0.95,9.6"}, "before · the FlowHMR body, as captured", h=420)}
{model("shelton-2", "after · the Shelton on the bike at jerrythegoat.com/usta", h=420, attrs='camera-orbit="20deg 78deg 3.4m" camera-target="0m 0.95m 0m" animation-name="sv"')}
</div>
{model("rodin-shelton", "Rodin 2.5 body from three frames of the same video", h=420, attrs=CAST)}
</section>""")

# ---------- 6 the rest ----------
ENV = [f"""<section aria-label="Environments">
<p class="sub">The venues are data, not generated images: OpenStreetMap, USGS terrain, an aerial photo, Poly Haven props. Scroll inside each scene.</p>
<figure class="scene env"><iframe data-src="https://jerrythegoat.com/usta/" title="USTA" style="height:720px"></iframe><figcaption class="cap">US Open · Arthur Ashe and Flushing Meadows</figcaption></figure>
{fig("media/venues/usta-sheet.jpg", "Arthur Ashe and the grounds from OpenStreetMap footprints and code")}
{model("shelton-coria-point", "the USTA opener point · both players with the Wilson ball", h=420, attrs='camera-target="12m 1m -0.8m" camera-orbit="215deg 78deg 7m" min-camera-orbit="auto auto 2m" max-camera-orbit="auto auto 40m"')}
<figure class="scene env"><iframe data-src="https://jerrythegoat.com/ucla/" title="UCLA" style="height:720px"></iframe><figcaption class="cap">UCLA · Los Angeles Tennis Center</figcaption></figure>
{fig("media/venues/ucla-full.jpg", "real terrain, aerial photo ground, 52k trees from the near-infrared band")}
<figure class="scene env"><iframe data-src="https://jerrythegoat.com/galaxy/" title="LA Galaxy" style="height:720px"></iframe><figcaption class="cap">LA Galaxy · Dignity Health Sports Park, Carson</figcaption></figure>
<figure class="scene env"><iframe data-src="https://jerrythegoat.com/shield/" title="LA Kings" style="height:720px"></iframe><figcaption class="cap">LA Kings · the shield</figcaption></figure>
</section>"""]

CASTP = [f"""<section aria-label="Cast">
<p class="sub">Meshy made the people from one reference image each; the goat is a CC0 scan reshaped in Blender. Drag to orbit.</p>
{model("shelton-2", "Ben Shelton · the rebuilt body on the USTA page", h=420, attrs=CAST + ' animation-name="sv"')}
{model("rodin-shelton", "Ben Shelton · Rodin 2.5 body from three frames of his video", h=420, attrs=CAST)}
{model("gauff-2", "Coco Gauff", h=400, attrs=CAST)}
{model("jerry", "Jerry · four-photo rebuild", h=400, attrs=CAST)}
{model("martin", "Martin", h=400, attrs=CAST)}
{model("umpire", "umpire", h=400, attrs=CAST)}
{model("sp-1", "spectator", h=400, attrs=CAST)}
{model("goat-loader", "the home-page goat", h=360, attrs='auto-rotate')}
{model("toy-ibex", "toy ibex · nano-banana still → Tripo", h=360, attrs='auto-rotate')}
{model("toy-mountain", "toy mountain", h=360, attrs='auto-rotate')}
</section>"""]

FILMS = [f"""<section aria-label="Films">
<p class="sub">HyperFrames renders HTML to video frame by frame, so every render is the same twice.</p>
{video("media/hyperframes/cycling-film.mp4", "media/hyperframes/cycling-film-poster.jpg", "cycling film · 17 s")}
{video("media/hyperframes/reel-v3.mp4", "media/hyperframes/reel-v3-poster.jpg", "sports data reel · 31 s")}
{video("media/loader/three-loaders.mp4", "media/loader/three-loaders-poster.jpg", "the three loaders")}
{video("media/web/shield-galaxy.mp4", "media/web/shield-galaxy-poster.jpg", "the Galaxy animation behind the shield")}
<h3>Thumbnails</h3>
<div class="thumbs">
{"".join(f'<figure class="vid"><video class="auto" src="media/thumbs/final-{n}.mp4" poster="media/thumbs/final-{n}-poster.jpg" muted loop playsinline preload="none"></video><figcaption class="cap">{n}</figcaption></figure>' for n in ("usta","ucla","galaxy","matchviewer","orfeu","radio","cycling"))}
</div>
</section>"""]

S.append(f"""<section aria-labelledby="h-time">
<h2 id="h-time">Timeline</h2>
{dated_rows([("Sep 16","First tennis figure: Meshy 6 Lite from a generated reference","Meshy"),("Oct 19–21","Meshy cast, crowds and props for the story pages; Kling video fails","Meshy · fal"),("Oct 22","First FlowHMR run; Shelton serve accepted","Modal"),("Oct 23–26","Rallies, two-player point, broadcast and college benchmarks; Meshy heads rejected; rackets traced","Modal"),("Oct 27","Rodin bodies through fal.ai; 4K crop; face fits rejected","fal"),("Oct 28","16-point library; racket through the arm; 120 fps forehand; 34 contacts pinned","local"),("Oct 29–30","USTA opener rebuilt on the serve-and-volley point; serve kept behind the baseline; live","live"),("Oct 30","Own viewer with the footage driving every scene; research pass on the racket; hand-driven racket and ball-by-inference runs started","running")])}
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
.chart .d3{width:100%}
.pages{display:flex;gap:18px;margin:-6px 0 26px;font:12px var(--mono)}.pages a{color:var(--muted);text-decoration:none}.pages a:hover{color:var(--fg)}.pages b{font-weight:600}
.pair{display:grid;gap:12px}
.thumbs{display:grid;grid-template-columns:1fr 1fr;gap:10px}.thumbs .cap{text-align:center}
.scene iframe[data-src]:not([src]){background:var(--fill)}
.scores{list-style:none;margin:0 0 10px;padding:0}
.scores li{display:grid;grid-template-columns:64px 1fr auto;gap:12px;align-items:center;padding:10px 0;border-top:1px solid var(--line)}
.scores li:last-child{border-bottom:1px solid var(--line)}
.scores img{width:64px;height:64px;object-fit:cover;border-radius:6px;background:var(--panel)}
.scores b{display:block;font-size:14px;font-weight:600}.scores small{display:block;font-size:12px;color:var(--muted);line-height:1.4}
.scores code{font:11px var(--mono);color:var(--muted);align-self:start;padding-top:2px}
.hero{margin-top:-10px}
section p{margin:0 0 10px;font-size:14px}
@media (prefers-reduced-motion:reduce){.track i{transition:none}}
"""

PAGES = [("index", "Tennis", "Video to Motion", "How one YouTube clip becomes a body, a racket and a ball on a court. The plan, the examples, the research, where the footage comes from, and what broke and how it was fixed.", S),
         ("environments", "Environments", "Environments", "The US Open, UCLA, the Galaxy and the Kings as live 3D scenes.", ENV),
         ("cast", "Cast", "Cast", "The people and the goat, as interactive models.", CASTP),
         ("films", "Films", "Films", "HyperFrames films and the home-page thumbnails.", FILMS)]

def nav(cur):
    return '<nav class="pages" aria-label="Pages">' + "".join(
        (f'<b>{t}</b>' if k == cur else f'<a href="{"./" if k == "index" else k + ".html"}">{t}</a>') for k, t, *_ in PAGES) + '</nav>'

for key, tab, title, lede, parts in PAGES:
    page = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(lede)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(lede)}">
<style>{CSS}{EXTRA}</style>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@4.1.0/dist/model-viewer.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script defer src="charts.js"></script>
</head><body>
<main class="col">
<div class="made"><a href="https://jerrythegoat.com/">jerrythegoat.com</a> · notes</div>
<header><h1>{e(title)}</h1><p>{e(lede)}</p></header>
{nav(key)}
{''.join(parts)}
</main>
<script>
(function(){{
  customElements.whenDefined('model-viewer').then(function(){{customElements.get('model-viewer').meshoptDecoderLocation='https://cdn.jsdelivr.net/npm/meshoptimizer@0.22.0/meshopt_decoder.js';}});
  var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('on');io.unobserve(x.target);}}}});}},{{threshold:.3}});
  document.querySelectorAll('.bars li, .mini').forEach(function(el){{io.observe(el);}});
  var vids=[].slice.call(document.querySelectorAll('video.auto'));
  var vo=new IntersectionObserver(function(es){{es.forEach(function(x){{var v=x.target;if(x.isIntersecting){{if(v.preload==='none'){{v.preload='auto';v.load();}}v.play().catch(function(){{}});}}else{{v.pause();}}}});}},{{rootMargin:'160px 0px'}});
  vids.forEach(function(v){{vo.observe(v);}});
  // scenes and environments load only near the viewport and unload far away: one live WebGL scene at a time
  var fr=[].slice.call(document.querySelectorAll('iframe[data-src]'));
  var fo=new IntersectionObserver(function(es){{es.forEach(function(x){{var f=x.target;
    if(x.isIntersecting){{ if(!f.src) f.src=f.dataset.src; }} else if(f.src){{ f.removeAttribute('src'); }} }});}},{{rootMargin:'300px 0px'}});
  fr.forEach(function(f){{fo.observe(f);}});
  window.addEventListener('load',function(){{
    document.querySelectorAll('.d3').forEach(function(el){{
      var kind=el.dataset.chart, d=JSON.parse(el.dataset.json);
      if(kind==='spin') VTM.spinChart(el,d.rows);
      else if(kind==='contact') VTM.contactChart(el,d.rows,d.band);
      else if(kind==='bars') VTM.bars(el,d.rows,d.max,function(v){{return v+(d.unit||'');}});
      else if(kind==='trace') fetch(d.src).then(function(r){{return r.json();}}).then(function(j){{VTM.trace(el,j[d.key],d.label);}});
    }});
  }});
}})();
</script>
</body></html>
"""
    (ROOT / f"{key}.html").write_text(page)
    print("wrote", key + ".html", len(page), "bytes")
print("missing models:", sorted(set(MISSING)))
