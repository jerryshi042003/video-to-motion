# Video to Motion

What each generator actually produced, October 2026. One section per process: the stack and the pipeline first, then the results, with the input beside the output wherever both were kept.

- **Video to motion**: Modal running [FlowHMR](https://github.com/flowhmr/flowhmr) for body motion and [RacketVision](https://arxiv.org/abs/2511.17045) for racket points, a local arm solver, Blender for the racket and the renders
- **Bodies from photos**: Hyper3D Rodin 2.5 through fal.ai
- **HyperFrames films**: HTML and a paused timeline rendered frame by frame to video
- **Home-page thumbnails**: four generations in one day and a 140-option review
- **Meshy**: characters, crowds, props and scenes for the court-stories pages

Open `index.html`, or the GitHub Pages site once enabled. Videos play on their own as they scroll into view. The small `i` on every card opens the back: source, what ran, the result, what is specific to that item, and cost.

![Ben Shelton serve: source, front, side, back](media/library/shelton-serve-b-poster.jpg)

## Where it stands

| Area | Score | Why |
| --- | --- | --- |
| Body motion | 8/10 | FlowHMR on court-level footage, accepted across 16 points |
| Ball | 8/10 | ball audit and estimated arcs; hidden where unsupported |
| Racket model design | 7/10 | traced outline, woven strings, drilled grommets; depth approximate |
| Racket motion | 6/10 | solved through the arm; face at contact set by rule; blurred at 30 fps |
| Skin and face texture, Meshy | 5/10 | stylised characters; heads rejected as likeness |
| Body shape specific to the person | 2/10 | every player shares the FlowHMR body; Rodin bodies paused |
| Skin and face texture, FlowHMR with a rig | 2/10 | plain grey body |
| Face likeness | 2/10 | Rodin, UP2You and Meshy all generated a face, none a likeness |

## Video to motion

The recipe that worked: court-level footage from behind the player, 30 fps, 1080p cut from 4K. FlowHMR gives the body and shape. RacketVision gives five racket points per frame where the racket is visible. The racket is solved through the forearm and wrist inside anatomical limits, with spin capped, instead of being placed freely at the wrist. Contact frames are labelled by eye and the face angle is pinned there. Blender renders source, front, side and back in sync.

Sixteen points across six players, grouped by shot: serves, returns, and served points with groundstrokes. Same steps on every point; the back of each card lists what is specific to it (handedness, contacts, how much of the swing the detector saw, arm-limit frames).

Other cameras and frame rates show where quality changes:

- 120 fps, 4K, court level (Alcaraz forehand): the detector keeps the racket through contact; 81 percent of frames found against 32 to 40 percent at 30 fps. The best racket result of the project.
- High diagonal seat, 4K crop (Djokovic): body fit improved, racket detection got worse; this camera is the ceiling for groundstrokes.
- Elevated broadcast, 1080p50 (Shelton, ATP): full-court context, no usable wrist or face.
- Fixed club camera (college match): body plus charted ball arcs, no racket.
- 14-second rally and a two-player played point: drift over time, hidden hands, cropped serve contact. Both remain viewable as test scenes on the Tennis Lab site.

![Alcaraz forehand at 120 fps through contact](media/racket/hfr-contact.jpg)

## The racket

A model built in Blender from reference contours, with the frame, throat bridge, individual grommets, a woven string bed and a wrapped handle as separate closed meshes. The arm solve stopped the face flipping between frames. The contact rule fixed 34 labelled contacts from 7 plausible face angles to 34. Grip registration is one hand-to-handle transform per stroke family.

![Racket model](media/racket/racket-full.jpg)

## Bodies from photos

Two or three frames of the player's own video to Rodin 2.5 give a whole clothed person whose outfit matches the footage. The face is generated, the hand stays open under the grip, and loose clothing bulges because the shirt is part of the body mesh. Eight bodies were built and paused.

![Shelton serve with his own Rodin body](media/bodies/compare-serve.jpg)

## HyperFrames films

HyperFrames renders HTML to video by seeking a paused GSAP timeline frame by frame in headless Chrome, so every render is deterministic. Scaffold, timeline, check, preview, render, encode. The hub clips for jerrythegoat.com (Shield, AEG, USTA, UCLA, Match Viewer, radio captions, cycling), the 17-second cycling film, the 31-second sports data reel and the Hawk-Eye 3D match films all came from it.

## Home-page thumbnails

HyperFrames camera-template clips on Oct 21 to 24; hand-authored HTML/CSS versions on Oct 27 at 02:00, rejected the same day; the seven original clips restored at 04:40; a review page of 140 de-duplicated options at 05:00; one selection per project with edits; a final refinement at 12:53. The gallery shows the process images and the eight live cards.

## Meshy

Stylised characters, crowds and props from one reference image: fast and consistent, not a likeness. The tennis likeness attempts (heads, multi-view body, first figure) were rejected; the court-stories cast and scenes are in the Meshy section.

## Repository layout

```
index.html         the gallery (built)
gallery.json       every process: stack, pipeline, groups, cards with front and back
build.py           regenerates index.html from gallery.json
media/library/     16 library clips (mp4 + poster): source | front | side | back
media/racket/      racket renders, overlays, 120 fps proof, contact checks
media/bodies/      Rodin body comparison
media/scenes/      stills of the live Tennis Lab scenes for the other cameras
media/hyperframes/ hub clips and films, 960 px encodes
media/thumbs/      thumbnail process images and the eight live cards
media/calls/       input and output images for each service call
media/logos/       vendor marks (sources in SOURCES.txt)
```

Rebuild after editing `gallery.json`:

```bash
python3 build.py
```

## Sources and limits

Footage: Court Level Tennis, Slow-Mo Tennis and TennisTV on YouTube, plus a college PlaySight camera; each clip links to its source and time range. Short excerpts for analysis.

Body depth is monocular and no physics was simulated. The racket face angle at contact is set by rule, not measured. Hawk-Eye SkeleTRACK and mocap-suit capture remain the gold standard; this is what one camera and public footage can do.
