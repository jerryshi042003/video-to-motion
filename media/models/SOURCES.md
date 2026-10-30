# Model sources

Gathered 2026-10-30 from Jerry Shi's October 2026 work. Each GLB was re-packed with `gltf-transform optimize` (meshopt, webp textures at 1024 px max; `optimize` also welds, simplifies and prunes, so delivered triangle counts are below the originals). Posters rendered with Blender 5.2 (EEVEE), three-quarter view, first animation frame.

## License and generator notes

- **FlowHMR**: FlowHMR body estimate from video (research model output; generic SMPL-family body, not a likeness). Jerry Shi, Oct 2026.
- **Blender**: Authored in Blender by Jerry Shi (Oct 2026) unless noted.
- **Meshy**: Generated with Meshy (Jerry Shi account, Oct 2026). Ownership/commercial use per Meshy plan terms (not verified here). Named-player models are approximate likenesses.
- **Rodin**: Generated with Hyper3D Rodin via fal.ai from reference photos (Oct 2026). Use per fal.ai / Hyper3D terms (not verified here). Real-player likenesses: treat as private reference, not for redistribution without review.
- **Tripo**: Generated with Tripo via fal.ai from an authored concept image (Oct 2026). Use per fal.ai / Tripo terms (not verified here).
- **Hunyuan3D**: Generated with Hunyuan3D via fal.ai from an authored concept image (Oct 2026). Use per fal.ai / Tencent Hunyuan terms (not verified here).
- **authored**: See per-file note.

## Files

| id | group | generator | source | note |
|---|---|---|---|---|
| tennis-lab-equipment-aero-motion | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/equipment-aero-motion.glb` |  |
| tennis-lab-pipeline-atp | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/pipeline-atp.glb` |  |
| tennis-lab-pipeline-close | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/pipeline-close.glb` |  |
| tennis-lab-pipeline-college | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/pipeline-college.glb` |  |
| tennis-lab-quan-gomez-point | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/quan-gomez-point.glb` |  |
| tennis-lab-shelton-atp | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/shelton-atp.glb` |  |
| tennis-lab-shelton-coria | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/shelton-coria.glb` |  |
| tennis-lab-shelton-long-rally | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/shelton-long-rally.glb` |  |
| tennis-lab-shelton-rally | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/shelton-rally.glb` |  |
| tennis-lab-shelton-serve | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/shelton-serve.glb` |  |
| tennis-lab-shelton-wide | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/shelton-wide.glb` |  |
| tennis-lab-ucla-point8-combined | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/ucla-point8-combined.glb` |  |
| tennis-lab-ucla-point8 | tennis-lab-demo | FlowHMR | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/downloads/ucla-point8.glb` |  |
| racket-ezone | racket | Blender | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/models/ezone.glb` | Yonex EZONE 98 (2025) retail visual reference, photo-projected frame; originally /Users/jshi/Scratch/tennis-motion-sota-20261021/racket/yonex_ezone98_2025_photo.glb (byte-identical). Not manufacturer CAD. |
| racket-aero | racket | Blender | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/models/rackets/aero.glb` | Babolat Pure Aero 98 Gen9 retail visual reference: photo-traced frame, authored beam/strings/grip (tennis-lab scripts/rackets/make_racket_reference.py). Product photo from babolat.com used as tracing source only. Not manufacturer CAD. |
| racket-blade | racket | Blender | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/models/rackets/blade.glb` | Wilson Blade 98 v10 retail visual reference, same method as aero; beam measurements approximate. |
| racket-vcore | racket | Blender | `/Users/jshi/Personal/playground/shishi88 @ codex/tennis-lab-release : apps/tennis-lab/public/models/rackets/vcore.glb` | Yonex VCORE 98 retail visual reference, same method as aero. |
| racket-arm-solved | racket | Blender | `/Users/jshi/Scratch/tennis-racket-motion-20261028/racket-rebuild/racket-final.glb` | Rebuilt racket used by the Oct 28 arm-solved 16-point library (review/racket.glb is byte-identical). optimize simplified 561k -> 62k triangles. |
| racket-finished-v18 | racket | Blender | `/Users/jshi/Scratch/tennis-racket-motion-20261028/finish-rebuild/racket-finished-v18.glb` | Finished racket build v18 (= full-redo/staged/racket-rebuild/racket-final.glb, byte-identical). Raw 107.7 MB; optimize simplified 2.29M -> 389k triangles. |
| shelton-coria-point | usta-scene | FlowHMR | `/Users/jshi/Scratch/usta-drift-20261030/apps/court-stories/public/models/shelton-coria-point.glb` | FlowHMR two-player point packed for court-stories (scripts/blender/pack_player.py) from the usta-drift-20261030 scratch checkout. |
| ball-usopen | usta-scene | Blender | `/Users/jshi/Scratch/usta-drift-20261030/apps/court-stories/public/models/ball-usopen.glb` | Wilson US Open ball, 6.7 cm, authored in Blender (court-stories scripts usopen_ball.py: UV sphere + painted texture). |
| shelton | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/shelton.glb` |  |
| shelton-2 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/shelton2.glb` |  |
| gauff | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/gauff.glb` |  |
| gauff-2 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/gauff2.glb` |  |
| gilbert | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/gilbert.glb` |  |
| martin | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/martin.glb` |  |
| quan-iw | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/quanIW.glb` |  |
| quan-ucla | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/quanUCLA.glb` |  |
| jerry | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/jerry.glb` |  |
| jerry-serve | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/jerry-serve.glb` |  |
| umpire | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/umpire.glb` |  |
| ballkid | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/ballkid.glb` |  |
| analyst | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/analyst.glb` |  |
| coach | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/coach.glb` |  |
| stu-1 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/stu1.glb` |  |
| stu-2 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/stu2.glb` |  |
| stu-3 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/stu3.glb` |  |
| stu-4 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/stu4.glb` |  |
| sp-1 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/sp1.glb` |  |
| sp-2 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/sp2.glb` |  |
| sp-3 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/sp3.glb` |  |
| sp-4 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/sp4.glb` |  |
| fan-1 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/fan1.glb` |  |
| fan-2 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/fan2.glb` |  |
| fan-3 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/fan3.glb` |  |
| fan-4 | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/fan4.glb` |  |
| pro-a | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/proA.glb` |  |
| pro-b | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/proB.glb` |  |
| rival | meshy-cast | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/rival.glb` |  |
| palm | prop | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/palm.glb` |  |
| bruin | prop | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/models/bruin.glb` |  |
| crowd-fan-1 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/fan1.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-fan-2 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/fan2.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-fan-3 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/fan3.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-fan-4 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/fan4.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-sp-1 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/sp1.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-sp-2 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/sp2.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-sp-3 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/sp3.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-sp-4 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/sp4.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-sp-5 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/sp5.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-sp-6 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/sp6.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-sp-7 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/sp7.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| crowd-sp-8 | crowd | Meshy | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/crowd/sp8.glb` | Baked low-poly crowd kit person derived from the Meshy cast for seated-crowd impostors. |
| straus-stands | other | Blender | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/venues/straus-stands.glb` | Straus Stadium stands, authored low-poly venue geometry for court-stories (9 webp textures). |
| prop-sofa-03 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/sofa_03.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-sofa-02 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/sofa_02.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-coffee-table-01 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/coffee_table_01.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-modern-coffee-table-01 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/modern_coffee_table_01.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-modern-arm-chair-01 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/modern_arm_chair_01.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-mid-century-lounge-chair | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/mid_century_lounge_chair.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-side-table-01 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/side_table_01.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-potted-plant-01 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/potted_plant_01.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-metal-office-desk | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/metal_office_desk.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-drawer-cabinet | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/drawer_cabinet.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-desk-lamp-arm-01 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/desk_lamp_arm_01.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-painted-wooden-bench | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/painted_wooden_bench.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-metal-trash-can | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/metal_trash_can.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-steel-frame-shelves-01 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/steel_frame_shelves_01.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| prop-shelf-01 | prop | authored | `/Users/jshi/Personal/playground/shishi88/apps/court-stories/public/props/shelf_01.glb` | Poly Haven furniture, CC0 (https://polyhaven.com/license); see apps/court-stories/public/props/SOURCES.md for asset id and authors. Already meshopt/webp-packed by court-stories scripts/fetch-props.mjs. |
| goat-loader | loader | Blender | `/Users/jshi/Scratch/court-goat-smooth/apps/court-stories/src/jerry-thinking/assets/goat-loader.glb` | Goat by Copabrangorandel, OpenGameArt, CC0 (https://opengameart.org/content/goat), reshaped toward an ibex with authored horns/beard and an original 16-bone rig (scripts/prepare-goat-loader.py). |
| boulder-loader | loader | Blender | `/Users/jshi/Scratch/court-goat-smooth/apps/court-stories/src/jerry-thinking/assets/boulder-loader.glb` | Boulder 01, Rico Cilliers / Poly Haven, CC0 (https://polyhaven.com/a/boulder_01), welded and decimated to 5,950 triangles; textures stripped in this GLB (the app loads separate webp diffuse/normal). |
| mountainside-loader | loader | Blender | `/Users/jshi/Scratch/goat-ibex-release-20261027/release-prev-232836/.vercel/output/static/assets/mountainside-loader-BBejPAux.glb` | Recovered from a previous release build (hashed Vite asset). Its build script was not located in the checked-out sources; provenance unverified beyond the file itself. |
| toy-ibex | loader | Tripo | `/Users/jshi/Scratch/toy-ibex-20261027/rig/toy-ibex.glb` | Rigged web version of the Tripo toy ibex (rig/rig.py); one webp texture. |
| toy-ibex-normalized | loader | Tripo | `/Users/jshi/Scratch/toy-ibex-20261027/rig/norm.glb` | Normalized Tripo mesh before rigging (rig/normalize.py). |
| toy-ibex-tripo-raw | loader | Tripo | `/Users/jshi/Scratch/toy-ibex-20261027/models/tripo.glb` | Raw Tripo image-to-3D output (fal.ai) from an authored concept image. |
| toy-ibex-hunyuan-raw | loader | Hunyuan3D | `/Users/jshi/Scratch/toy-ibex-20261027/models/hy.glb` | Raw Hunyuan3D image-to-3D output (fal.ai) from the same concept image. Its embedded texture has a zero-width image, so texture compression was skipped (meshopt only). |
| toy-mountain | loader | Tripo | `/Users/jshi/Scratch/toy-ibex-20261027/mountain/mountain-web.glb` | Slimmed web version of the Tripo toy mountain (mountain/slim.py). |
| toy-mountain-raw | loader | Tripo | `/Users/jshi/Scratch/toy-ibex-20261027/mountain/mountain.glb` | Raw Tripo image-to-3D output (fal.ai) from an authored diorama concept image. |
| rodin-shelton | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-shelton-recipe-20261027/fal-shelton/base_basic_pbr.glb` |  |
| rodin-cobolli | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-rear-recipe-20261027/fal-cobolli/base_basic_pbr.glb` |  |
| rodin-alcaraz | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-rear-recipe-20261027/fal-alcaraz/base_basic_pbr.glb` |  |
| rodin-perricard | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-rear-recipe-20261027/fal-perricard/base_basic_pbr.glb` |  |
| rodin-djokovic | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-rear-recipe-20261027/fal-djokovic/base_basic_pbr.glb` |  |
| rodin-djokovic-2 | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-rear-recipe-20261027/fal-djokovic2/base_basic_pbr.glb` |  |
| rodin-shelton-rigged | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-shelton-recipe-20261027/shelton-rig/shelton-rodin-clean.glb` |  |
| rodin-cobolli-rigged | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-rear-recipe-20261027/cobolli-rig/cobolli-rodin-clean.glb` |  |
| rodin-alcaraz-rigged | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-rear-recipe-20261027/alcaraz-rig/alcaraz-rodin-clean.glb` |  |
| rodin-perricard-rigged | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-rear-recipe-20261027/perricard-rig/perricard-rodin-clean.glb` |  |
| rodin-djokovic-2-rigged | rodin-body | Rodin | `/Users/jshi/Scratch/tennis-rear-recipe-20261027/djokovic2-rig/djokovic2-rodin-clean.glb` |  |

## Not found / not exported as GLB

- 16-point rear-court library (shelton-serve-b/d/f/g2, alcaraz-a/b, alcaraz-serve, alcaraz-hfr, djokovic-iw-a/c, djokovic-turin-return, sinner-return, cabolli-return, cobolli-b1/b2/c1/c2): no per-point GLB exists under /Users/jshi/Scratch/tennis-racket-motion-20261028/candidate/<point>/ (audit.json, ball.json, motion.npz only), full-redo/ or review/. The review export stores each point as `<point>.json` + `<point>.bin` (custom layout: rest mesh, faces, weights, per-frame bones, racket transforms) for the browser viewer; only review/racket.glb (= racket-arm-solved) and racket-previous.glb (= racket-ezone) are GLBs there.
- /Users/jshi/Scratch/real-ibex-20261028/ does not exist; no real-ibex.glb, dam/ibex.glb or toy-mountain.glb under court-goat-smooth jerry-thinking/assets (only goat-loader.glb and boulder-loader.glb).
- /Users/jshi/Personal/playground/shishi88/apps/hawkeye-3d/public holds examples/ and videos/ only; no GLB.
- Rodin: no shelton body under tennis-rear-recipe-20261027 (fal-shelton lives in tennis-shelton-recipe-20261027); tennis-rear-point-batch-20261027 holds only deploy copies of candidate-web/candidate-own-motion/djokovic-own-motion GLBs (FlowHMR candidates, not Rodin).

## Skipped duplicates / not collected

- review/racket.glb, review/racket-previous.glb, repair-preview/review/*, full-redo/staged/review/racket.glb: byte-identical to racket-arm-solved / racket-ezone / racket-finished-v18.
- finish-rebuild/racket-finished-v2..v19, racket-analytic*, racket-geometry, racket-rebuild/racket-v2..v6: intermediate racket builds (35-108 MB each), not collected.
- tennis-rear-recipe-20261027/*-rig/*-rodin.glb: byte-identical to the fal base_basic_pbr.glb files; djokovic-rig/djokovic-rodin.glb (take 1) has no -clean counterpart.
- tennis-connected-appearance-20261026 (fal-rodin single/multiview, connected-candidate, retired-gallery heads, MICA face), tennis-head-rebuild-20261027, tennis-body-repair-20261022, tennis-flowhmr-liam-20261022 model-guide/player-benchmark, tennis-motion-sota-20261021 gpu/rigged and fingers rigs: earlier appearance/body experiments, outside the brief; listed here so they are known to survive.
- goat-ibex-20261027/base.glb, v1-v8, repro.glb: goat reshaping iterations behind goat-loader; toy-ibex-20261027/concepts: images only.
