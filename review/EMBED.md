# Embedding a point from the racket-motion review

Static copy of the private player-motion review viewer (`tools/tennis-racket-motion/index.html` + `viewer.js`, three.js vendored in `vendor/`). All point data lives in `data/`. The original tools and the review root were not modified.

## URL

```
review/?point=<id>&embed=1&camera=<name>&footage=1&autoplay=1
```

| Parameter | Values | Effect |
|---|---|---|
| `point` | one of the 17 ids below (`clip` still works as an alias) | point to open; unknown ids fall back to `djokovic-iw-a` |
| `embed` | `1` | hides the page chrome; keeps the 3D view, the footage panel, the camera row and the play/scrub row, filling the iframe |
| `camera` | `behind` `front` `side` `top` `free`, or the viewer's own `rear` `front` `side` `top` `oblique` `grip` `impact` `source` (`view` still works) | initial camera. `behind` → `rear`; `free` → `oblique` (orbit is enabled on every preset except `source`). `top` is a new straight-down preset added to the copied viewer |
| `footage` | `1` / `0` | show or hide the source-footage panel above the 3D view |
| `autoplay` | `1` | starts playback on load and loops the point (only in embed mode) |
| `frame` | number | start frame (unchanged from the original viewer) |

Example:

```html
<iframe src="review/?point=shelton-serve-d&embed=1&camera=behind&footage=1&autoplay=1"
        width="400" height="560" loading="lazy" allow="autoplay" style="border:0"></iframe>
```

Phone: 400×560. Desktop: 430×560. Served from the gallery root with any static server (plain `python3 -m http.server` is enough; byte-range support is only needed for faster seeking of long clips).

Without `embed=1` the page is the full review viewer (point list, previous/new fit toggle, ghost, status, contact buttons, evidence text).

## Points (17)

shelton-serve-b, shelton-serve-d, shelton-serve-f, shelton-serve-g2, alcaraz-serve, sinner-return, djokovic-turin-return, cabolli-return, alcaraz-a, alcaraz-b, djokovic-iw-a, djokovic-iw-c, cobolli-b1, cobolli-b2, cobolli-c1, cobolli-c2, alcaraz-hfr

Per point in `data/`: `<id>.json` (metadata, layout, audit, balls), `<id>.bin` (poses, mesh, weights, camera; unchanged), `<id>-source.mp4` (source footage). Shared: `manifest.json`, `racket.glb` (13.2 MB), `racket-previous.glb` (1.2 MB, only used by the racket inspector page, kept for completeness).

## Sizes

- `review/` total: 119.5 MB (119,479,696 bytes; 114.0 MiB) including the 7 verification screenshots (0.9 MB) and this file; 118.6 MB without them
- `.bin` motion files: 83.8 MB (unchanged)
- `racket.glb` + `racket-previous.glb`: 14.4 MB (unchanged)
- `vendor/` three.js modules: 2.2 MB (only the modules the viewer imports)
- source footage: 17 files, 19.8 MB total (0.63–1.62 MB each). Originals were 1920 px H.264, 230 MB in total. Re-encoded with `ffmpeg -an -vf scale=960:-2 -c:v libx264 -preset slow -crf 29 -pix_fmt yuv420p -g 30 -movflags +faststart`. CRF 26 as first tried gave 25.3 MB and a 126.7 MB total, over the 120 MB target, so CRF 29 was used. Frame counts and frame rates were verified identical to the originals with `ffprobe -count_frames` for all 17 files, so the viewer's frame-exact seeking is unchanged. Audio was dropped (the viewer plays the video muted).

## Changes made in the copied viewer (not in the original tools)

`viewer.js`: `DATA='data/'` prefix on every fetch (`manifest.json`, `<id>.json`, `<id>.bin`, `-source.mp4`, `racket.glb`); `point`/`camera`/`embed`/`footage`/`autoplay` query handling with camera aliases; `top` camera preset; loop-on-end when autoplaying in embed mode; source canvas switched to 960×436 in embed mode so the footage panel is 2.2:1.
`index.html`: `Top` camera button; seek slider moved into the transport row; `html.embed` CSS (hides header, intro, status, contact buttons, evidence, references, frame-number input, speed select, frame step buttons, full-source and ball checkboxes; camera row scrolls horizontally); blank favicon link so no `favicon.ico` 404.

## Verification (2026-10-30)

Server: `python3 -m http.server 8471 -d /Users/jshi/Personal/playground/video-to-motion-gallery`. Playwright 1.61.1 from `shishi88/node_modules`, viewport 400×560, flags `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`, screenshot after 8 s, then a further 1.5 s to confirm the video clock advances. Screenshots in `embed-check/`.

Browser note: the installed Playwright headless shell (`chromium_headless_shell-1148`, Chromium 131) has no H.264 decoder, so with it every `-source.mp4` failed with `NotSupportedError: The element has no supported sources` (3D scene, body and racket still rendered). The footage check was therefore run with the installed Google Chrome 156 through Playwright's `channel: 'chrome'` in headless mode with the same GL flags. Real browsers (Chrome, Safari, Firefox, iOS) decode H.264.

| point | loaded | console errors | HTTP ≥400 | body + racket rendered | footage playing | autoplay/loop |
|---|---|---|---|---|---|---|
| shelton-serve-d | yes | 0 | 0 | yes (screenshot) | yes, 960 px, readyState 4, clock 4.58→6.09 s | playing; 192-frame clip had wrapped once by 8 s |
| alcaraz-hfr | yes | 0 | 0 | yes | yes, clock 5.52→8.52 s (120 fps motion on 60 fps source, rate 2×) | playing, loops |
| sinner-return | yes | 0 | 0 | yes | yes, clock 6.57→8.07 s | playing, loops |
| cobolli-c1 | yes | 0 | 0 | yes | yes, clock 5.19→6.69 s | playing, loops |

Extra checks (same run): 430×560 desktop with `camera=top` (shelton-serve-d) renders and selects the Top preset; `footage=0` hides the footage panel and the 3D view takes 462 px of height; the full non-embed page (`?point=djokovic-iw-a&camera=side`) loads with no console errors and no failed requests. Pixel checks on the WebGL canvas counted 2,800–5,400 light-grey body pixels and 13,000–15,000 other foreground (racket, grid) pixels per point at 382×280. The single `favicon.ico` 404 seen in the first run was removed by the blank favicon link; the final runs had none.

Not verified: real phone browsers, touch orbit inside an iframe, and byte-range seeking behaviour on the eventual hosting server.
