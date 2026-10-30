# Tennis source → observations → 3D → website

Keep one immutable source record per input: URL/file, hash, player identity, time range, frame count, camera view, rights and known limitations.

## Ingest

- Hawk-Eye: retain event times, source cubic coefficients, both ground-position tracks, faults, lets and missing point endings. No skeleton is supplied.
- SwingVision: retain exact contact/bounce coordinates, player labels, timestamp nulls and scoring metadata. Do not replace missing times with made-up real time. Links between contacts and bounces are schematic, not measured ball flight.
- Video: decode the selected full action. Detect cuts and slowdown. Keep both players, racket, ball and camera calibration on one frame clock.

## Reconstruct

FlowHMR estimates body motion. RacketVision supplies racket and ball detections. OpenCV stabilizes the camera and measures the court. An independent landmark detector can check visibility and gross disagreement. No one library guarantees physics or exact body dimensions.

Fit a fixed shape per player. Apply temporal observation smoothing, then solve contact and the rig. Keep hidden observations missing. Do not deform the body just to make a generated head fit.

## Accept

Inspect the full action plus front/side/back views in Blender and browser. Check shoulders, spine, grip, foot contacts, racket contact and occlusion. Preserve source and failed candidates. Numeric checks support visual review; they do not replace it.

## Deliver

One small poster on the portfolio, optional short MP4 preview, explicit link to this page. Download only the selected match/point and animation. Share the Blender scene separately. A GLB is an optional on-demand model; do not preload every scene on the homepage.

## Reproduce this catalog

Run `/usr/bin/python3 scripts/ingest.py`, then `npm run verify` and `npm run build` from the tennis-lab application directory. The source adapters read local source repositories and write only the lab's public data directory. Source files and generation credentials are not part of the web build.
