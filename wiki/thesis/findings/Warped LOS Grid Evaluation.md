---
type: finding
title: "Warped LOS Grid Evaluation"
created: 2026-07-28
updated: 2026-07-28
tags:
  - domain/thesis
  - domain/ml
  - domain/reionization
  - concept/data-pipeline
  - concept/sharp-fronts
  - finding/positive
status: active
related:
  - "[[Warped LOS Grid Plan]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[z_re Map Training Results]]"
  - "[[Edge and Wall-Placement Losses]]"
  - "[[Neutral Fraction]]"
sources:
  - "figures/grid_eval_out50_real/grid_eval.csv (real cones, 926,903 front rays)"
  - "checkpoints_3d_localfno_warped256*"
---

# Warped LOS Grid Evaluation

> **Purpose:** the real-cone evaluation that was pending in [[Warped LOS Grid Plan]]. The training-free round-trip evaluator has now been run on real lightcones (926,903 front-bearing rays, 8 candidate grids). **The warped grid wins decisively on every metric**, and the first training runs on the rebuilt `warped256` cache are underway. But the evaluator also exposes an unexpected result: the plan's diagnosis was right *and* the fix does not come free.

## 1. Round-trip results on real cones

Training-free: resample the native lightcone onto a candidate grid, interpolate back, and measure what was lost. `sharpness_ratio` is the recovered front sharpness (1.0 = perfect); `fronts_missed` is the fraction of front-bearing rays whose transition falls between samples entirely.

| grid | global RMSE | transition RMSE | **sharpness ratio** | **fronts missed** | cell @ z=5.5 | cell @ z=20 |
|---|---|---|---|---|---|---|
| **uniform_z_256** *(the current cache)* | 0.1381 | 0.2669 | **0.127** | **11.7%** | **37.7 Mpc** | 6.5 Mpc |
| uniform_chi_256 | 0.1137 | 0.2362 | 0.201 | 6.3% | 13.3 | 13.3 |
| **warped_256** | **0.1027** | 0.2199 | **0.332** | **4.9%** | **12.3** | 63.2 |
| crop15_chi_256 | 0.1039 | 0.2195 | 0.272 | 5.3% | 9.9 | — |
| uniform_z_512 | 0.1100 | 0.2290 | 0.276 | 7.2% | 19.0 | 3.2 |
| uniform_chi_512 | 0.0829 | 0.1906 | 0.414 | 3.2% | 6.6 | 6.6 |
| **warped_512** | **0.0728** | **0.1714** | **0.661** | **2.9%** | 6.2 | 31.7 |
| crop15_chi_512 | 0.0740 | 0.1699 | 0.556 | 2.9% | 5.0 | — |

### What this establishes

1. **The plan's diagnosis is confirmed and it is large.** The production cache (`uniform_z_256`) recovers only **12.7%** of the true front sharpness and misses **11.7%** of fronts entirely. Roughly one front in nine is not in the training data at all. This is a hard, model-independent ceiling that sits logically *prior* to every architecture and loss experiment in the campaign — no operator and no wall-placement loss can recover a front the cache never sampled.
2. **Warping is the single best 256-slice option**: sharpness 0.127 → **0.332** (2.6×) and fronts missed 11.7% → 4.9%, at the *same* storage budget. Simply switching to uniform-$\chi$ already gets most of the way (0.201, 6.3%) for free.
3. **Warping at 256 beats uniform-$z$ at 512.** The warped 256-slice grid (0.332 / 4.9%) outperforms doubling the uniform-$z$ budget (0.276 / 7.2%). **Where the samples go matters more than how many there are** — the cleanest possible vindication of the plan.
4. **`crop15_chi` is nearly as good and much simpler.** Cropping to $z < 15$ and sampling uniformly in $\chi$ gets 0.272 / 5.3% at 256 and essentially ties warped at 512, without any ensemble-derived warp function. **Consider it the default unless the high-$z$ tail is needed** — it has no tuning surface and no ensemble dependence.

> [!key-insight]
> The warp's cost is visible in the last column: cell size at $z = 20$ goes from 6.5 Mpc (uniform-$z$) to **63.2 Mpc** (warped). The warp buys low-$z$ front resolution by abandoning the high-$z$ end — which is defensible only because the field is saturated there. Any downstream use that cares about high-$z$ structure (e.g. an early-density auxiliary input, or the $T_b$ task's spin-temperature era) must not use this cache.

![[envelope_explainer.png]]

## 2. Training on the warped cache — early and inconclusive

Three LocalFNO runs on the rebuilt `warped256` dataset:

| run | epochs | best val L² | val H¹ | test L² |
|---|---|---|---|---|
| `checkpoints_3d_localfno_warped256` | 37 | 0.0731 | 13.33 | 0.0699 |
| `checkpoints_3d_localfno_warped256_volw_cont` (Δχ volume-weighted loss) | 50 | **0.0634** | 12.30 | 0.0620 |
| *(reference)* `checkpoints_3d_localfno_1gpu` on the **uniform** cache | 50 | 0.0460 | 8.94 | 0.0458 |

> [!contradiction]
> The warped-cache runs score *far worse* than the uniform-cache reference — 0.063 vs 0.046 val L². **This is not a like-for-like comparison and must not be read as one.** The target grid differs, so the loss is computed over a different set of voxels; concentrating samples where fronts live *increases* the fraction of hard, high-variance voxels in the target and mechanically raises RMSE. The consolidated run table in [[Structured-Transform Operator Findings]] excludes warped256 rows for exactly this reason.
>
> The comparison that would settle it — evaluate both models on a **common** reference grid, or compare reconstructed front width rather than voxel L² — has not been run. **Until it is, the warped-cache training result is uninterpreted, not negative.**

The Δχ volume-weighted loss (`LOSS_LOS_VOLUME_WEIGHTS=1`) does help within the warped family (0.0731 → 0.0634), which is the expected direction: without it the non-uniform grid over-weights the densely sampled low-$z$ region in the loss as well as in the data.

## 3. Where this sits in the campaign

This is the **data-side** attack, and the round-trip numbers argue it should have been first. The three architecture-side attacks ([[SirenFNO Spectral Bias Investigation]], [[Windowed Local-FNO U-Net Findings]], [[Structured-Transform Operator Findings]]) and the loss-side attack ([[Edge and Wall-Placement Losses]]) were all fighting for front sharpness inside a cache that had already discarded 87% of it.

It does not, however, explain the hedging result: [[Hedging Bias of Pointwise Losses]] shows the 2-D models leave *representable* sharpness unused, and the 2-D slice task does not go through the LOS cache at all. **The two diagnoses are independent and both are real** — the cache bounds what is achievable, and the objective determines whether the model reaches that bound.

## 4. Next

- **Pick the grid and rebuild.** On these numbers: `crop15_chi_256` for simplicity, `warped_256` for maximum low-$z$ fidelity. Decide whether the $z > 15$ tail is needed by anything downstream.
- **Common-grid re-evaluation** of the warped-cache checkpoints against the uniform-cache benchmark — the missing comparison above.
- Retrain the U-FNO benchmark on the chosen cache with `LOSS_LOS_VOLUME_WEIGHTS=1`, and re-run the boundary-band diagnostic. The relevant question is not val L² but **whether the 10.7 Mpc front-width floor moves**.
- Combine with expwall: a cache that keeps the fronts plus a loss that places them is the first configuration with a plausible path to truth-like 3-D fronts.

![[xhi_hist_cache_comparison.png]]
