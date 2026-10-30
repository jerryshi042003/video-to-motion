# Tennis Lab viewer, vendored for inline iframes

`lab/` is a static build of the Tennis Lab app (`apps/tennis-lab` on branch
`codex/tennis-lab-release` of `shishi88`, commit c27ae1972, Vite 8.3.4, three 0.186.1)
built with `npx vite build --base ./`, so it runs from any subfolder, for example
`http://host/lab/` or `http://host/lab/?source=motion&match=shelton-coria`.
No external site is needed; all data, models and footage excerpts are in this folder.
Size: 61 MB (65 MB with `embed-check/`).

## Embedding

```html
<iframe src="lab/?source=motion&match=shelton-coria&embed=1&camera=behind&footage=1&autoplay=1"
        width="400" height="560" loading="lazy" allow="autoplay"></iframe>
```

## URL parameters

| Parameter | Values | Effect |
|---|---|---|
| `source` | `motion`, `hawkeye`, `btc` | Scene family: video-to-body motion, Hawk-Eye tracking, Bruin shot records |
| `match` | scene id (below) | Which scene to open |
| `point` | e.g. `QS033-1-6-5`, `video-8` | Point inside a `hawkeye` / `btc` match |
| `embed` | `1` | Embed mode (added here): hides the "Jerry Shi" header, the "All demos" / "Share" bar, the collection tabs, the title block, the source/method text, the "Stack & files" panel, the footer and every outbound link; the viewer fills the iframe height; the 3D view opens without the "Open interactive court" click |
| `camera` | `behind`, `front`, `side`, `top`, `court`, `baseline`, `racket`, `free`, plus the app's own `broadcast`, `player`, `head`, `source` | Initial camera. `court` is an alias of the app's `broadcast`; `free` starts with "Rotate freely" enabled (drag to orbit) |
| `footage` | `1` or `0` | `1` opens the original footage excerpt beside the body; `0` keeps it closed (the "Show footage" button still works). Without the parameter the app's default applies (footage opens for motion scenes except the racket camera) |
| `autoplay` | `1` | Starts playback (body, ball and footage) on load |
| `pipeline=1&stage=0..3` | | Three-source test: the four reconstruction stages (Motion, Court, Racket, Skin + texture) |
| `appearance=1&head=none&outfit=…&racket=…` | outfit: `source`, `match`, `training`, `warmup`; racket: `ezone`, `aero`, `vcore`, `blade` | Clothes & rackets scene on the Shelton serve |

Layout in embed mode: the footage sits above the 3D view when the iframe is narrower
than 600 px and beside it from 600 px up. At 400 x 560 the 3D view is about 194 px tall
with footage open (152-166 px for scenes with an extra control row) and 318-390 px without.

## Scenes (from `data/motion.json`, `data/index.json` and `src/main.js` buildGallery)

Collection "Demos" (`collection=featured`)
- `shelton-serve` - Shelton · serve practice (Serve action) - motion
- `shelton-coria` - Shelton · serve and volley (Played practice point) - motion
- `shelton-serve` with `camera=racket` - EZONE — racket detail - motion

Collection "Footage tests" (`collection=footage`)
- `shelton-serve` - Shelton · serve practice
- `shelton-coria` - Shelton · serve and volley
- `ucla-point8` - Johnson · Stanford body and ball (Indexed UCLA footage; `replay`: body + estimated flight, Body+ball / Body only toggle)
- `shelton-atp` - Shelton · elevated ATP broadcast (High-camera benchmark)
- `shelton-long-rally` - Shelton · extended practice rally (14-second rally study)
- `shelton-rally` - Shelton · forehand and backhand (Groundstroke excerpt)
- `shelton-wide` - Shelton · wide-view movement (Movement excerpt)
- `jerry` - Jerry — original serve: a plain `<video>` of `media/jerry-original-serve.mp4` (`?source=original`), not a 3D scene; embed mode is not applied to it

Collection "Three-source test" (`collection=pipeline`, add `pipeline=1&stage=0`)
- `shelton-serve` - High-detail court-level
- `ucla-point8` - PlaySight college
- `shelton-atp` - ATP broadcast

Collection "Clothes & rackets" (`collection=appearance`, all on `match=shelton-serve&pipeline=1&stage=3&appearance=1&head=none`)
- `outfit-match` - Match knit (`outfit=match&racket=ezone&camera=front`)
- `outfit-training` - Training mesh (`outfit=training&racket=ezone&camera=front`)
- `outfit-warmup` - Warm-up weave (`outfit=warmup&racket=ezone&camera=front`)
- `racket-ezone` - Original EZONE (`outfit=match&racket=ezone&camera=racket`)
- `racket-aero` - Babolat Pure Aero 98 Gen9 (`outfit=match&racket=aero&camera=racket`)
- `racket-vcore` - Yonex VCORE 98 Ruby Red (`outfit=match&racket=vcore&camera=racket`)
- `racket-blade` - Wilson Blade 98 v10 (`outfit=match&racket=blade&camera=racket`)

Collection "Data studies" (`collection=data`)
- `QS033` - Quan–Gomez — Hawk-Eye data (`source=hawkeye&match=QS033&point=QS033-1-6-5`; 114 other Hawk-Eye/Bruin matches in `data/index.json` are also loadable)
- `btc-6f1044da7a51` - Johnson–Banerjee — shot diagram (`source=btc&match=btc-6f1044da7a51&point=video-8`)

## Source changes (worktree only, not committed anywhere)

Worktree: `/Users/jshi/Scratch/tennis-lab-vendor-20261030` (detached at c27ae1972).
- `src/main.js`: embed-mode block after the state declarations (reads `embed`, `camera`
  aliases `court`→`broadcast` and `free`, `footage`, `autoplay`; sets `activated=true` and
  adds `html.embed`); in `showRecord`, after the camera is set: enable rotation for `free`,
  honour `footage=0|1`, start playback for `autoplay=1`. The loop that fills the three
  appearance `<select>`s moved above `await loadCatalog()`: with auto-activation the
  appearance initialiser ran before the options existed, so the selects showed
  "Source colors / Original EZONE" while the 3D state was correct.
- `src/style.css`: `html.embed …` rules appended (hide chrome, flex layout that fills the
  iframe, compact control rows, footage above/beside the viewport).
- No absolute `/` asset or data URLs existed; everything goes through `import.meta.env.BASE_URL`,
  which `--base ./` turns into `./`.

## Exclusions from `dist/`

All `.blend` files in `downloads/` (optional editable Blender scenes) and any file over 15 MB:
aero-reference.blend 808K, blade-reference.blend 768K, equipment-options.blend 17M (also the
only file over 15 MB), pipeline-atp.blend 5.7M, pipeline-close.blend 5.4M, pipeline-college.blend
6.8M, quan-gomez-point.blend 208K, shelton-atp.blend 1.2M, shelton-coria.blend 3.8M,
shelton-long-rally.blend 2.0M, shelton-rally.blend 1.2M, shelton-serve.blend 2.0M,
shelton-wide.blend 1.2M, ucla-point8-combined.blend 1.5M, ucla-point8.blend 1.5M,
vcore-reference.blend 732K. The 13 GLBs in `downloads/` (20 MB), `data/` (24 MB), `models/`
(9.9 MB) and `media/` (6.2 MB) are kept. The "Stack & files" panel that linked to the
`.blend` files is hidden in embed mode; in the plain page those links would 404.

## Verification (2026-10-30)

Served with `python3 -m http.server 8470 -d video-to-motion-gallery`; Playwright 1.61.1 from
`shishi88/node_modules` driving `~/.cache/hyperframes/chrome/chrome-headless-shell/mac_arm-152.0.7977.30`
(the `ms-playwright` headless shell on this Mac is revision 1148, which Playwright 1.61.1 does
not accept) with `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`.
Each URL below was loaded with `&embed=1` at 400x560 and 430x560, screenshotted after 8 s
(`embed-check/<scene>-<w>x<h>.png`), and checked for console errors, page errors, responses
with status >= 400 and failed requests, `window.tennisLab.state.ready`, hidden chrome (header,
footer, detail nav, title block, library/tabs, technical panel, source text, no visible `http`
links), no page scroll, and a visible subject (the frame is rendered with and without the
body/racket/ball meshes and the differing pixels counted). Raw numbers: `embed-check/results.json`.

Result: 46 of 46 loads had zero console errors, zero 404/failed requests, ready viewer, hidden
chrome and no scroll. 40 passed the pixel check (2.0-2.5% of pixels for the body scenes).
The six below fell under the 0.3% automatic threshold but are correct on inspection:
- `btc-6f1044da7a51` (shot diagram: lines and markers only, no body by design)
- `alias-court` (`camera=court` on shelton-coria: full-court view, the body is small)
- `alias-top` (`camera=top`: top-down court, body small at the baseline)

Scenes checked (all with `footage=1&autoplay=1` unless noted; footage `readyState` 4 and the
clip was playing or had reached its end after 8 s): shelton-coria, shelton-serve, shelton-atp,
ucla-point8, shelton-long-rally, shelton-rally, shelton-wide (`camera=behind`);
EZONE racket detail (`camera=racket`, no footage); outfit-match, outfit-training, outfit-warmup
(`camera=front`); racket-ezone, racket-aero, racket-vcore, racket-blade (`camera=racket`);
pipeline shelton-serve, ucla-point8, shelton-atp (`pipeline=1&stage=0&camera=behind`);
Hawk-Eye QS033-1-6-5 (`camera=court`); btc-6f1044da7a51 video-8; and the aliases
`camera=court`, `camera=free` (Rotate freely active) and `camera=top` on shelton-coria.
Scenes where `playing` was false at 8 s had reached the clip end (clip 5.6-6.0 s); those
with longer clips were still playing.

Plain page: `lab/` (gallery, 21 cards) and `lab/?source=motion&match=shelton-coria` (cover,
then the 3D view after "Open interactive court") loaded at 1100x800 with no console errors and
no 404s (`embed-check/plain-*.png`).

Not verified: a real iframe in the gallery page, touch orbit, and widths of 600 px or more
(side-by-side layout) were not screenshotted.
