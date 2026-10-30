#!/usr/bin/env python3
"""Build index.html from gallery.json. Python 3 only, no dependencies."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
G = json.loads((ROOT / "gallery.json").read_text())
e = html.escape
VERDICT = {"accepted": "good", "used on page": "good", "built": "mid", "paused": "mid", "diagnostic": "mid",
           "not adopted": "bad", "rejected": "bad", "failed": "bad", "live": "good"}


def img(src, cls=""):
    return f'<img src="{e(src)}" loading="lazy" alt="" class="{cls}">'


def media(c):
    if c["kind"] == "video":
        return (f'<video class="auto" src="{e(c["video"])}" poster="{e(c.get("poster", ""))}" '
                f'muted loop playsinline preload="none" disablepictureinpicture></video>')
    if c["kind"] == "image":
        gal = "".join(img(g) for g in c.get("gallery", []))
        main = img(c["image"])
        if c.get("link"):
            main = f'<a href="{e(c["link"])}" target="_blank" rel="noopener">{main}</a>'
        return f'<div class="stack-media">{main}{gal}</div>' if gal else main
    # io: inputs -> outputs
    ins = "".join(img(p) for p in c.get("inputs", [])) or '<span class="none">no input kept</span>'
    outs = "".join(img(p) for p in c.get("outputs", [])) or '<span class="none">no output kept</span>'
    return f'<div class="io"><div class="imgs">{ins}</div><span class="arrow">→</span><div class="imgs">{outs}</div></div>'


def back(c):
    b = c.get("back", {})
    rows = []
    if b.get("source"):
        src = e(b["source"])
        if b.get("source_url"):
            src = f'<a href="{e(b["source_url"])}" target="_blank" rel="noopener">{src}</a>'
        rows.append(("Source", src))
    if b.get("ran"):
        rows.append(("What ran", e(b["ran"])))
    if b.get("why"):
        rows.append(("Result", e(b["why"])))
    if b.get("differs"):
        rows.append(("This one", e(b["differs"])))
    if b.get("cost"):
        rows.append(("Cost", e(b["cost"])))
    return "".join(f'<div class="kv"><span>{k}</span><p>{v}</p></div>' for k, v in rows)


def card(c):
    v = c.get("verdict", "")
    meta = " · ".join(e(m) for m in c.get("meta", []))
    sub = f'<span class="sub">{e(c["sub"])}</span>' if c.get("sub") else ""
    extra = " portrait" if c["id"].startswith("cast-") else ""
    return f"""<article class="card {c['kind']}{extra}" id="{e(c['id'])}" tabindex="0">
<div class="front">
<div class="media">{media(c)}</div>
<div class="cap"><h4>{e(c['title'])}{sub}</h4><div class="meta">{meta}{' · ' if meta and v else ''}<b class="v {VERDICT.get(v, '')}">{e(v)}</b></div></div>
</div>
<div class="back"><div class="kv-wrap"><h4>{e(c['title'])}</h4>{back(c)}</div></div>
<button class="flip" type="button" aria-label="Details">i</button>
</article>"""


def pipeline(steps):
    return '<ol class="pipe">' + "".join(
        f'<li><span class="n">{e(s["step"])}</span><b>{e(s["what"])}</b><span>{e(s["how"])}</span></li>' for s in steps
    ) + "</ol>"


def stack(items):
    out = []
    for s in items:
        logo = img(s["logo"], "logo dark" if s.get("dark") else "logo") if s.get("logo") else f'<span class="mono">{e(s.get("mono", s["name"][:2]))}</span>'
        out.append(f'<div class="tool">{logo}<div><b>{e(s["name"])}</b><span>{e(s["role"])}</span><span class="cost">{e(s["cost"])}</span></div></div>')
    return '<div class="tools">' + "".join(out) + "</div>"


def group(g):
    parts = [f'<h3>{e(g["title"])}</h3>']
    if g.get("note"):
        parts.append(f'<p class="note">{e(g["note"])}</p>')
    if g.get("subgroups"):
        for s in g["subgroups"]:
            parts.append(f'<h4 class="shot">{e(s["title"])}</h4><div class="grid">{"".join(card(c) for c in s["items"])}</div>')
    else:
        parts.append(f'<div class="grid">{"".join(card(c) for c in g["items"])}</div>')
    return "\n".join(parts)


def process(p):
    return f"""<section class="process" id="{e(p['id'])}">
<header><h2>{e(p['name'])}</h2><p>{e(p.get('one_line', ''))}</p></header>
<div class="how"><div><h3>Stack</h3>{stack(p['stack'])}</div><div><h3>Pipeline</h3>{pipeline(p['pipeline'])}</div></div>
{''.join(group(g) for g in p['groups'])}
</section>"""


def scores():
    rows = "".join(
        f'<div class="score"><span class="name">{e(s["name"])}</span><span class="bar"><i style="width:{s["score"]*10}%"></i></span><span class="num">{s["score"]}/10</span><span class="why">{e(s["note"])}{(" <a href=\"" + e(s["ref"]) + "\" target=\"_blank\" rel=\"noopener\">paper</a>") if s.get("ref") else ""}</span></div>'
        for s in G["scores"])
    return f'<section id="scores"><header><h2>Where it stands</h2><p>{e(G.get("scores_note", ""))}</p></header><div class="scores">{rows}</div></section>'


def timeline():
    done = "".join(f'<li><span class="d">{e(t["date"])}</span><span>{e(t["what"])}</span></li>' for t in G["timeline"]["done"])
    nxt = "".join(f'<li><span class="d">next</span><span>{e(t)}</span></li>' for t in G["timeline"]["next"])
    return f'<section id="timeline"><header><h2>Timeline</h2></header><div class="tl"><ol>{done}</ol><ol class="next">{nxt}</ol></div></section>'


nav = "".join(f'<a href="#{e(p["id"])}">{e(p["name"])}</a>' for p in G["processes"]) + '<a href="#scores">Where it stands</a><a href="#timeline">Timeline</a>'

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Video to Motion</title>
<meta name="description" content="What Meshy, fal.ai, Modal (FlowHMR, RacketVision), HyperFrames and Blender produced: tennis video to 3D motion, rackets, bodies, scenes and films. Process first, results below.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<style>
:root{{--ink:#17202a;--muted:#596571;--line:#e3e6e8;--blue:#2458d3;--wash:#eef3fd;--paper:#fff;--good:#236442;--bad:#963c2f;--mid:#596571;color-scheme:light}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
a{{color:var(--blue);text-underline-offset:3px}}
.top{{border-top:3px solid var(--blue);border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--paper);z-index:20}}
.top .in{{max-width:1336px;margin:auto;padding:0 24px;height:56px;display:flex;align-items:center;gap:22px}}
.brand{{font-weight:700;font-size:18px;white-space:nowrap}}
.top nav{{display:flex;gap:16px;overflow-x:auto;font-size:13px}}.top nav a{{color:var(--muted);text-decoration:none;white-space:nowrap}}.top nav a:hover{{color:var(--ink)}}
main{{max-width:1336px;margin:auto;padding:28px 24px 80px}}
h1{{font-size:34px;line-height:1.15;letter-spacing:-.03em;margin:0 0 6px;font-weight:700}}
.lede{{color:var(--muted);margin:0 0 8px;max-width:72ch}}
section{{margin-top:56px}}section>header{{border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:18px}}
h2{{font-size:25px;letter-spacing:-.025em;margin:0}}section>header p{{margin:4px 0 0;color:var(--muted)}}
h3{{font-size:13px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin:28px 0 10px;font-weight:600}}
h4.shot{{font-size:14px;color:var(--ink);margin:16px 0 8px;font-weight:600}}
.note{{margin:-4px 0 12px;color:var(--muted);max-width:80ch}}
.how{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:28px;align-items:start}}
.tools{{display:grid;gap:8px}}.tool{{display:flex;gap:12px;align-items:flex-start;border:1px solid var(--line);border-radius:8px;padding:10px 12px}}
.tool .logo,.tool .mono{{width:34px;height:34px;flex:none;border-radius:7px;object-fit:contain;background:#f5f7fa;padding:5px}}
.tool .mono{{display:grid;place-items:center;font-size:11px;font-weight:700;color:var(--blue)}}.tool .logo.dark{{background:#1b1f1c}}
.tool b{{display:block;font-size:14px}}.tool span{{display:block;font-size:13px;color:var(--muted)}}.tool .cost{{color:var(--ink);font-size:12px;margin-top:2px}}
.pipe{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;counter-reset:s}}
.pipe li{{border:1px solid var(--line);border-radius:8px;padding:10px 12px;position:relative;font-size:13px}}
.pipe li .n{{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--wash);color:var(--blue);font-size:11px;font-weight:700;margin-bottom:6px}}
.pipe li b{{display:block;font-size:14px}}.pipe li span:last-child{{color:var(--muted)}}
.pipe li:not(:last-child)::after{{content:"→";position:absolute;right:-9px;top:12px;color:var(--muted);font-size:12px;background:var(--paper)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:14px}}
.card{{position:relative;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--paper);min-height:120px}}
.card.io{{grid-column:1/-1}}
.card .front,.card .back{{transition:opacity .18s}}
.card .back{{position:absolute;inset:0;background:var(--paper);opacity:0;pointer-events:none;overflow:auto;padding:14px 16px}}
.card.flipped .back{{opacity:1;pointer-events:auto}}.card.flipped .front{{opacity:.08}}
.media video,.media>img,.media .stack-media>img,.media .stack-media>a>img{{width:100%;display:block;background:#1a1f1d;aspect-ratio:16/9;object-fit:cover}}
.card.video .media video{{aspect-ratio:auto;height:auto}}
.card.portrait .media>img{{aspect-ratio:3/4;object-fit:contain;background:#d9dcd8}}
.stack-media{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px}}.stack-media>:first-child{{grid-column:1/-1}}
.stack-media img{{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#1a1f1d}}
.card.io .media{{padding:12px 14px 0}}.io{{display:grid;grid-template-columns:minmax(0,1fr) 22px minmax(0,1.4fr);gap:8px;align-items:start}}
.imgs{{display:flex;flex-wrap:wrap;gap:4px}}.imgs img{{height:120px;width:auto;max-width:100%;border-radius:3px;background:#1a1f1d;object-fit:contain}}
.arrow{{color:var(--muted);text-align:center;padding-top:62px}}.none{{color:var(--muted);font-size:12px}}
.cap{{padding:10px 14px 12px}}.cap h4{{margin:0;font-size:14px;font-weight:600;display:flex;flex-wrap:wrap;gap:4px 8px;align-items:baseline}}
.cap .sub{{color:var(--muted);font-weight:400;font-size:12.5px}}
.meta{{font-size:12.5px;color:var(--muted);margin-top:2px}}
.v{{font-weight:600}}.v.good{{color:var(--good)}}.v.bad{{color:var(--bad)}}.v.mid{{color:var(--mid)}}
.flip{{position:absolute;top:8px;right:8px;width:24px;height:24px;border-radius:50%;border:1px solid #b8c2cc;background:rgba(255,255,255,.92);font:600 12px/1 Inter,sans-serif;color:var(--ink);cursor:pointer;z-index:2}}
.flip:hover{{border-color:var(--blue);color:var(--blue)}}
.kv-wrap h4{{margin:0 0 8px;font-size:14px;padding-right:28px}}.kv{{display:grid;grid-template-columns:72px 1fr;gap:8px;font-size:13px;margin-bottom:8px}}
.kv span{{color:var(--muted)}}.kv p{{margin:0}}
.scores{{display:grid;gap:10px;max-width:980px}}
.score{{display:grid;grid-template-columns:260px 1fr 52px;gap:12px;align-items:center}}
.score .bar{{height:8px;background:#eef1f4;border-radius:99px;overflow:hidden}}.score .bar i{{display:block;height:100%;background:var(--blue)}}
.score .num{{font-weight:600;text-align:right}}.score .why{{grid-column:1/-1;color:var(--muted);font-size:13px;margin:-6px 0 2px}}
.tl{{display:grid;grid-template-columns:1fr 1fr;gap:32px}}.tl ol{{list-style:none;margin:0;padding:0;border-left:2px solid var(--line)}}
.tl li{{display:grid;grid-template-columns:78px 1fr;gap:10px;padding:0 0 14px 14px;position:relative;font-size:14px}}
.tl li::before{{content:"";position:absolute;left:-6px;top:6px;width:8px;height:8px;border-radius:50%;background:var(--blue)}}
.tl .next li::before{{background:#fff;border:2px solid var(--blue);width:6px;height:6px}}.tl .d{{color:var(--muted);font-size:12.5px}}
footer{{margin-top:64px;padding-top:14px;border-top:1px solid var(--line);font-size:13px;color:var(--muted);display:grid;gap:4px;max-width:90ch}}
@media (max-width:800px){{.how,.tl{{grid-template-columns:1fr}}.io{{grid-template-columns:1fr}}.arrow{{padding:0;transform:rotate(90deg)}}.score{{grid-template-columns:1fr 1fr 48px}}.score .name{{grid-column:1/-1}}}}
@media (prefers-reduced-motion:reduce){{.card .front,.card .back{{transition:none}}}}
</style></head><body>
<div class="top"><div class="in"><span class="brand">Video to Motion</span><nav>{nav}</nav></div></div>
<main>
<h1>What each generator actually produced</h1>
<p class="lede">Tennis video to 3D motion, rackets and bodies; scenes, films and thumbnails for jerrythegoat.com. One section per process: the stack and pipeline first, then the results. Videos play on their own; the small i on each card opens what ran, on what, and why it passed or failed.</p>
{''.join(process(p) for p in G['processes'])}
{scores()}
{timeline()}
<footer>
<span>Footage: Court Level Tennis, Slow-Mo Tennis, TennisTV, UCLA Tennis Consulting (PlaySight). Short excerpts for analysis, each linked to its source and time range.</span>
<span>Body depth is monocular and no physics was simulated. Racket face angle at contact is set by rule, not measured. Faces from Rodin, UP2You and Meshy are generated, not likenesses.</span>
</footer>
</main>
<script>
(function(){{
  var vids=[].slice.call(document.querySelectorAll('video.auto'));
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(es){{es.forEach(function(x){{var v=x.target;if(x.isIntersecting){{if(v.preload==='none'){{v.preload='auto';v.load();}}v.play().catch(function(){{}});}}else{{v.pause();}}}});}},{{rootMargin:'200px 0px'}});
    vids.forEach(function(v){{io.observe(v);}});
  }}else{{vids.forEach(function(v){{v.preload='auto';v.play().catch(function(){{}});}});}}
  document.querySelectorAll('.card').forEach(function(c){{
    var t=function(ev){{if(ev.target.closest('a,video'))return;c.classList.toggle('flipped');}};
    c.querySelector('.flip').addEventListener('click',function(ev){{ev.stopPropagation();c.classList.toggle('flipped');}});
    c.querySelector('.back').addEventListener('click',t);
    c.addEventListener('keydown',function(ev){{if(ev.key==='Enter'||ev.key===' '){{if(ev.target===c){{ev.preventDefault();c.classList.toggle('flipped');}}}}}});
  }});
}})();
</script>
</body></html>
"""
(ROOT / "index.html").write_text(page)
print("wrote index.html", len(page), "bytes")
