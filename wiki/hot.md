---
type: meta
title: "Hot Cache"
updated: 2026-07-28T00:00:00
---

# Recent Context

## Last Updated

2026-07-28 — Filed twelve days of 2-D / $z_\text{re}$ work: five findings ([[z_re Map Training Results]], [[Structured-Transform Operator Findings]], [[Edge and Wall-Placement Losses]], [[Contrast Map Investigation]], [[Warped LOS Grid Evaluation]]) and four concepts ([[Hedged Edges vs Blurred Edges]], [[Structured Transform Neural Operators]], [[Sliced Wasserstein Edge Loss]], [[Bubble Size Distribution]]).

## Key Recent Facts

- **The front-width problem is a *loss* problem, not a basis problem.** [[Hedged Edges vs Blurred Edges]]: the same sharpening map fixes band-limited truth (−9.28%) and does **exactly nothing** to the model (+0.00%) at matched width. ~86% of the model's error is not blur. The model's edges are soft because their *position* is uncertain and L² hedges — a category the whole campaign had been treating as blur.
- **And there is now a knob that moves it.** [[Edge and Wall-Placement Losses]]: `ExponentialWallDistance` (exponential-in-distance **absolute** error — a weighted *median*, which is binary on a binary field) reaches front width **1.16 px against truth 1.46**, where every RMSE-optimal model sits at ~2.9, for ~22% RMSE and high-$k$ power ratio 0.51 → 0.82. First training-time sharpness result in the campaign. Measured premise: H¹ seminorm and H² change by **exactly 1.00×** over 4→48 px of misplacement; the signed-distance loss changes 144×.
- **The loss weights were lying.** [[z_re Map Training Results]]: with nominal 0.5/0.5 absolute-mode losses, **H¹ supplies 99.4% of the 3-D training loss**. Every archived "L²+H¹" 3-D run is H¹-dominated, and a balanced weighting has never been tested. On $z_\text{re}$, **pure L² beats L²+H¹ by ~35% for every architecture — and improves the H¹ metric itself.**
- **SIREN weights rescue the Local-FNO.** Same note: LocalFNO goes worst → second best (RMSE 0.305 → 0.123, train→test gap 3.0× → 1.2×) at 54× fewer params than the U-FNO. This substantially softens the negative verdict in [[Windowed Local-FNO U-Net Findings]] — the problem was the spectral-weight collapse inherited inside each window, not locality.
- **Best 2-D model: Walsh–Hadamard in the *global* bottleneck only.** [[Structured-Transform Operator Findings]]: val RMSE 0.1453 vs LocalFNO 0.1487, U-FNO 0.1595. **Which slot matters more than which basis** (~5% vs ~1%). Local models are 20–60× smaller than the U-FNO at better accuracy. Also retracts the earlier inflated LocalWNO-vs-3-D comparison (z-interpolation handicap on the 3-D models).
- **The cube cache throws away most of the fronts.** [[Warped LOS Grid Evaluation]] on real cones (926,903 front rays): `uniform_z_256` recovers **12.7%** of true front sharpness and misses **11.7%** of fronts; `warped_256` gets 33.2% / 4.9% at the same budget and **beats uniform-$z$ at 512 slices**. Warped-cache training runs exist but are **not yet interpretable** (different target grid).
- **The contrast-map thread is closed.** [[Contrast Map Investigation]]: given a free sharpening dial and 30 epochs, gradient descent left it at the identity (θ 4.750 → 4.431). The 6.2% post-hoc gain is an oracle ceiling — its τ is a bias nuisance, not the physical threshold. One narrow survivor: per-band θ buys a real held-out 2–9% at $\bar{x}_\text{HI}$ 0.005–0.05.
- **LOS is the only axis where bandwidth still binds.** Per-branch mode weights: edge/peak 0.60–0.78 on $z$ vs 0.03–0.20 transverse. `LOCALFNO_MODES_Z` has never been spent. See [[Spectral Mode Cutoff in FNOs]].
- **Physics diagnostic added:** [[Bubble Size Distribution]] via transverse mean-free-path rays — the best U-FNO makes bubbles **+6.8% / +9.3% too large** early on, crossing to −2.6% at the end; distribution *shape* is fine (JS ≤ 0.017), *scale* drifts.

## Active Threads

- **Run expwall in 3-D.** Top priority. The loss is merged for cubes (chamfer via `max_pool3d`), the front-width defect is worse there (~3.5×), and the voxel-anisotropy caveat (transverse vs LOS Mpc per voxel) needs measuring rather than arguing about.
- **Run the $z_\text{re}$ reconstruction evaluation.** All 26 z_re runs are scored in $z_\text{re}$-space; [[Smooth-Target Reparametrization Plan]]'s actual criterion — reconstructed 10–90% front width vs U-FNO 10.7 / truth 3.6 Mpc — is still unrun. The smooth-target thread is unresolved, not successful.
- **Pick the LOS grid and rebuild the cache.** `crop15_chi_256` for simplicity, `warped_256` for maximum low-$z$ fidelity; then the **common-grid re-evaluation** that makes warped-cache training numbers comparable, then the U-FNO benchmark with `LOSS_LOS_VOLUME_WEIGHTS=1`.
- **Spend the LOS bandwidth headroom** (`LOCALFNO_MODES_Z` 12 → cap 17; bottleneck z 16 → cap 33). The one asymmetric-LOS test ever run stopped at 16 epochs.
- **3-D transfers being measured now**: pure L² (`checkpoints_3d_localsirenfno` vs `_l2only`), width bw32/bw48 at ω=60, and a genuinely balanced L²+H¹ (`_bw32om60_relbal`, relative mode, 0.5/0.07).
- Does global-only Walsh–Hadamard transfer to 3-D / $z_\text{re}$? Untested — and §1.3 of [[Structured-Transform Operator Findings]] warns a 2-D win is not a reliable predictor.
- Untried and cheap: `WallPlacementLoss` + BCE (the designed pairing), the `cnn` operator as a converged baseline, LocalFNO augmentation (transverse rolls + D4) and AdamW.
- Re-check [[Bubble Size Distribution]] on an expwall model — does truth-like front width fix the too-large bubbles?
- Any sharpness win must still be checked against $P(k)$, $r(k)$, and $\bar{x}_\text{HI}(z)$. The campaign now has an explicit **accuracy-vs-sharpness frontier** and the thesis has to choose a point on it deliberately.
- P1 remains focused on renormalized EFT coefficient extraction and cross-simulator validity.
