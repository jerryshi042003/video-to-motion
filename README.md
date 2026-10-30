# Video to Motion

How one YouTube clip of a tennis point becomes a 3D body, racket and ball on a court that a viewer can orbit. Live at https://video-to-motion.vercel.app and linked from the Notes row on jerrythegoat.com.

The page is one column in the jerrythegoat.com write-up style and reads in this order:

1. **Hero**: the Shelton serve-and-volley point with the original footage, body, racket and Wilson ball, orbitable, with Front, Side, Top and Court cameras.
2. **The plan**: clip, body (FlowHMR on Modal), racket (RacketVision plus an arm solver), ball (authored to the motion's events), person (Rodin, Meshy), scene.
3. **Examples**: three more points, each with the footage frame beside the fit.
4. **Research**: Hawk-Eye SkeleTRACK, FlowHMR, RacketVision, Rodin 2.5, Meshy 7.1, and the honest score bars (body motion 8, ball 8, racket model 7, racket motion 6, Meshy skin 5, body shape 2, face 2).
5. **Where the videos come from**: one card per YouTube source (channel, camera, frame rate, what changed) with the live scene under it. Same model every time; the camera and the frame rate decide the result.
6. **Problems and fixes**, each measured on the same points before and after, drawn with D3: racket spin per point (free-wrist fit vs arm solve), face angle at 34 labelled contacts, racket detection at 30 vs 120 fps, the serve drift behind the baseline, the authored ball, and the likeness attempts.
7. **Scenes, cast, goat and films**, then a timeline.

## Layout

```
index.html          the page (built)
build.py            builds index.html; sections, scores and chart data live here
charts.js           D3 charts: spinChart, contactChart, bars, trace
writeup.css         the jerrythegoat.com write-up contract
lab/                Tennis Lab viewer (Vite build) in embed mode: ?source=motion&match=<id>&embed=1&camera=behind&footage=1&autoplay=1
review/             16-point review viewer in embed mode: ?point=<id>&embed=1&camera=behind&footage=1&autoplay=1 (data/ holds poses, racket matrices, source excerpts)
media/models/       GLBs with posters and manifest.json (model-viewer, meshopt)
media/data/         racket-metrics.json, racket-trace.json (per-frame racket angular speed)
media/refs/         research and channel images, footage posters, SOURCES.txt
media/racket, bodies, venues, hyperframes, web, cast, logos
```

Rebuild after editing `build.py` or the data:

```bash
python3 build.py
```

Deploy with `vercel deploy --prod` from this folder (project `video-to-motion`).

## Sources and limits

Footage: Court Level Tennis, Slow-Mo Tennis, FocusedTennis, Court Level TV, Tennis TV and UCLA Tennis Consulting on YouTube; short excerpts for analysis, each card links to its source. Body depth is monocular and no physics was simulated. The racket face angle at contact is set by rule, not measured. Faces are generated, not likenesses.
