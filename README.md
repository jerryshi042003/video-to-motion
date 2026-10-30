# Video to Motion

How one YouTube clip of a tennis point becomes a 3D body, racket and ball on a court that a viewer can orbit. Live at https://video-to-motion.vercel.app and linked from the Notes row on jerrythegoat.com.

The page is one column in the jerrythegoat.com write-up style and reads in this order:

1. **Hero**: the Shelton serve-and-volley point in the gallery's own viewer (`scene/`): the original footage drives the 3D scene frame for frame, the camera starts where the footage camera was, one play control and a scrubber, drag to orbit, Wilson ball on the authored flights.
2. **The plan**: clip, body (FlowHMR on Modal), racket (RacketVision plus an arm solver), ball (authored to the motion's events), person (Rodin, Meshy), scene.
3. **Examples**: three more points, each with the footage frame beside the fit.
4. **Research**: Hawk-Eye SkeleTRACK, FlowHMR, RacketVision, Rodin 2.5, Meshy 7.1, and the honest score bars (body motion 8, ball 8, racket model 7, racket motion 6, Meshy skin 5, body shape 2, face 2).
5. **Where the videos come from**: one card per YouTube source (channel, camera, frame rate, what changed) with the live scene under it. Same model every time; the camera and the frame rate decide the result.
6. **Problems and fixes**, each measured on the same points before and after, drawn with D3: racket spin per point (free-wrist fit vs arm solve), face angle at 34 labelled contacts, racket detection at 30 vs 120 fps, the serve drift behind the baseline, the authored ball, and the likeness attempts.
7. **Scenes, cast, goat and films**, then the live environments (USTA, UCLA, LA Galaxy, LA Kings story pages embedded), the home-page thumbnails, and a timeline.

## Layout

```
index.html          the page (built)
build.py            builds index.html; sections, scores and chart data live here
charts.js           D3 charts: spinChart, contactChart, bars, trace
writeup.css         the jerrythegoat.com write-up contract
scene/              the viewer: ?m=<model id>&v=<footage>&cp=x,y,z&ct=x,y,z&fov=..&court=1&ball=auto|<json>&vs=<scene s per footage s>
vendor/             three.js r186 module build, OrbitControls, GLTFLoader, meshopt decoder
lab/, review/       the earlier vendored viewers; only their footage excerpts (lab/media/sources, review/data/*-source.mp4) and review/data poses are used now
media/data/         lab-cams.json and review-cams.json (source cameras per scene), racket-metrics.json, racket-trace.json
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
