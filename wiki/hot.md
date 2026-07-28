---
type: meta
title: "Hot Cache"
updated: 2026-07-28T00:00:00
---

# Recent Context

## Last Updated

2026-07-28 — Merged two parallel ingests of the same period. The 07-26/27 branch filed [[Loss Objective and Operator Basis Sweep]], [[Contrast Map Sharpening]], [[Hedging Bias of Pointwise Losses]], [[Contrast Map]], [[Walsh-Hadamard Neural Operator]] and three gaps; the 07-28 branch added [[Edge and Wall-Placement Losses]], [[Warped LOS Grid Evaluation]], [[Bubble Size Distribution]], [[Sliced Wasserstein Edge Loss]], [[Structured Transform Neural Operators]] and two detailed companions ([[z_re Map Training Results]], [[Structured-Transform Operator Findings]]). Duplicate pairs were reconciled onto the earlier names.

## Key Recent Facts

- **The diagnosis is settled and now acted on.** [[Hedging Bias of Pointwise Losses]]: L² is *minimised* by a hedged ramp when edge position is uncertain, and H¹ repeats it one derivative up. The discriminating measurement: the same sharpening map fixes band-limited truth (**−9.28%**) and does **exactly nothing** to the model (**+0.00%**) at matched width — so the softness is not blur. ~86% of the model's error is not blur.
- **And there is finally a lever that moves front width.** [[Edge and Wall-Placement Losses]]: `ExponentialWallDistance` reaches **1.16 px against truth 1.46**, where every RMSE-optimal model sits at ~2.9, for ~22% RMSE and high-$k$ power ratio 0.51 → 0.82. **Amendment to the 07-27 lead: SWD was not the winner.** The decisive property is *absolute* rather than *squared* error — a weighted conditional **median**, which on a binary field is binary, so the loss picks a side instead of averaging. Hedging is a property of pointwise **squared** losses, not pointwise losses in general.
- **Displacement blindness, quantified.** Over 4 → 48 px of wall misplacement: L² 3.5×, H¹ 2.9×, **H¹ seminorm 1.00×, H² 1.00×**, signed-distance 144×. H¹'s entire placement sensitivity is the L² term inside it.
- **The loss weights were a fiction.** Nominal 0.5/0.5 absolute-mode → **H¹ supplies 99.4%** of the 3-D loss; every archived "L²+H¹" 3-D run was H¹-dominated. On $z_\text{re}$, **pure L² beats L²+H¹ by ~35% for every architecture — and improves the H¹ metric itself.**
- **Best 2-D model is Walsh–Hadamard in the *global* slot only** (0.1453 vs LocalFNO 0.1487, U-FNO 0.1595); the local/global split matters more than the basis. Local models are **20–60× smaller than the U-FNO** at better accuracy and ~40% less peak memory ([[Structured-Transform Operator Findings]]).
- **SIREN weights rescue the Local-FNO** on $z_\text{re}$ (0.305 → 0.123, gap 3.0× → 1.2×) at 54× fewer params than the U-FNO.
- **The cube cache discards most of the fronts before training sees them.** [[Warped LOS Grid Evaluation]]: `uniform_z_256` recovers **12.7%** of true front sharpness and misses **11.7%** of fronts; `warped_256` gets 33.2% / 4.9% at the same budget and **beats uniform-$z$ at 512 slices**. This bound is independent of the objective problem — both are real.
- **Morphology check added.** [[Bubble Size Distribution]]: the best U-FNO makes bubbles **+6.8% / +9.3% too large** at $\bar{x}_\text{HI}$ 0.02–0.20 / 0.20–0.40, crossing to −2.6% at the end; JS ≤ 0.017 throughout — shape right, scale drifts.
- **LOS is the one axis where bandwidth may still bind**: edge/peak mode weight 0.60–0.78 on $z$ vs 0.03–0.20 transverse ([[LOS Bandwidth as the 3-D Bottleneck]]).

## Active Threads

**Resolved this cycle** — the epoch-29 sharpness table is in (the 29-run shared-slice leaderboard with `width`/`blur`); the transport-vs-steepness lead is settled (expwall, not SWD); the warped-grid real-cone evaluation is done; the first $z_\text{re}$ training runs are in.

- **Run expwall in 3-D.** Top priority. Merged for cubes (chamfer via `max_pool3d`); the front-width defect is worse there (~3.5×); the anisotropic-voxel caveat (transverse vs LOS Mpc) needs measuring, not arguing.
- **Run the $z_\text{re}$ reconstruction evaluation.** All 26 runs are scored in $z_\text{re}$-space; [[Smooth-Target Reparametrization Plan]]'s actual criterion — reconstructed front width vs U-FNO 10.7 / truth 3.6 Mpc — is still unrun. **The target-side thread is unresolved, not successful.**
- **Pick the LOS grid and rebuild the cache** (`crop15_chi_256` for simplicity, `warped_256` for low-$z$ fidelity), then the **common-grid re-evaluation** that makes warped-cache training numbers comparable, then the U-FNO benchmark with `LOSS_LOS_VOLUME_WEIGHTS=1`.
- **LOS mode count** ([[LOS Bandwidth as the 3-D Bottleneck]]): single-variable runs at `LOCALFNO_MODES_Z` 12 → 17 and bottleneck z 16 → 24/33 with the diagnostic re-run — but interpret with [[Warped LOS Grid Evaluation]]: extra modes resolve nothing if the cache is the limit.
- **3-D confirmations queued**: pure L² (`checkpoints_3d_localsirenfno` vs `_l2only`), width bw32/bw48 at ω=60, and the first genuinely balanced 3-D L²+H¹ (`_bw32om60_relbal`, 0.5/0.07).
- **Does global-slot WHNO transfer to 3-D / $z_\text{re}$?** Plus the unfitted FNO+WHNO ensemble and the shift-consistency test for the dyadic-convolution caveat ([[Square-Wave Basis for Ionization Fields]]).
- Untried and cheap: `WallPlacementLoss` + BCE (the designed pairing), the `cnn` operator as a converged baseline, Local-FNO transverse-roll/D4 augmentation and AdamW.
- Re-check [[Bubble Size Distribution]] on an expwall model — does truth-like front width fix the too-large bubbles?
- Boundary-band + $P(k)$/$r(k)$ on the SirenFNO checkpoint; the SirenFNO × U-Net hybrid; the global-pooling residual.
- **The campaign now has an explicit accuracy-vs-sharpness frontier** (RMSE 0.1448 at width 2.89, or 0.1767 at 1.16). For a forward model feeding SBI on summary statistics, truth-like $P(k)$ and BSD plausibly beat per-pixel RMSE — the thesis has to pick a point deliberately rather than inherit the loss default.
- P1 remains focused on renormalized EFT coefficient extraction and cross-simulator validity.
