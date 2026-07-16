---
type: plan
title: "Lightcone z_re Map Target"
created: 2026-07-16
updated: 2026-07-16
tags:
  - domain/thesis
  - domain/planning
  - domain/ml
  - domain/reionization
  - concept/target-reparametrization
  - concept/zre-field
status: implemented-training-pending
related:
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[Warped LOS Grid Plan]]"
  - "[[Neutral Fraction]]"
  - "[[P1 EFT Characterization]]"
---

# Lightcone z_re Map Target

> **What this is:** the concrete implementation of candidate 1 of the [[Smooth-Target Reparametrization Plan]], with one key change from the plan — instead of the native 21cmFAST `z_re_box` (a coeval box, which would force a re-simulation pass and a pipeline geometry change), the target is a **per-pixel 2-D map $z_\text{re}(x, y)$ fitted directly from the existing lightcone $x_\text{HI}(z)$ sightlines**. No re-simulation, no code surgery, and the learning problem becomes 2-D.

## Target definitions (`dataset/zre_target.py`)

Both are least-squares fits per sky pixel against the full native $x_\text{HI}(z)$ sightline:

- **`gompertz` (recommended)** — two-parameter front $x_\text{HI} = \exp(-e^{-(z - z_0)/\Delta z})$ over a $(z_0, \Delta z)$ grid ($z_0 \in [2.5, 18]$ step 0.1, $\Delta z \in$ geomspace(0.02, 4, 18)); the stored value is the fit's midpoint $z_\text{half} = z_0 - \ln(\ln 2)\,\Delta z$. Smoothest map; $z_0$ deliberately spans below the cone edge so partially started fronts can place their midpoint outside the volume.
- **`step`** — one-parameter step $x_\text{HI} = \Theta(z - z_\text{re})$ with the exact least-squares threshold (cumulative-sum trick, fully vectorized).

Pixels whose fitted transition lies outside the cone (midpoint below the low-z edge, or no transition at all) are stored as **NaN**. Maps cost a few seconds per cone and are cached in a sidecar HDF5 (`zre_targets.h5`, one dataset per cone, idempotent per file stem).

## Reconstruction sanity check (first pass of the plan's "ceiling check")

`figures/Z_RE reconstruction/` (2026-07-16), 12 sample cones:

- **Global $x_\text{HI}(z)$ round-trip** with step reconstruction $\hat{x}_\text{HI} = \Theta(z - z_\text{re}(x,y))$, comparing three step-crossing definitions: the **hi-z crossing is bad** (voxel MSE 0.13–0.32 per cone); the **lo-z crossing and the optimal (least-squares) step are good and nearly identical** (voxel MSE ≈ 0.008–0.05). Fully neutral cones reconstruct exactly (MSE 0.000).
- **Gompertz $z_\text{re}(x,y)$ maps**: mid/early-reionizing cones give smooth, well-behaved maps (medians 7.6–10.5); but **late reionizers have 79–99% of pixels with no front inside the cone** (fitted midpoint below z = 5 → NaN). The parent plan's "sentinel contamination" worry is confirmed as the dominant practical issue: many cones are mostly-NaN, and several are fully neutral throughout.

## Training pipeline (`fno_zre.py`, `dataset/dataset_zre.py`, `models_zre_2d.py`)

- **Mapping**: density lightcone → $z_\text{re}(x,y)$. The 3-D density cone is interpolated to `N_Z_IN = 64` LOS slices which enter a **2-D FNO as input channels** (the output map has no LOS axis, so LOS translation equivariance is not needed); the 11 sampled parameters are broadcast as constant channels, mirroring the 3-D pipeline's conditioning.
- **Target handling**: $z_\text{re}$ normalized to [0, 1] over $z \in [5, 25]$; NaN pixels clamped to the z_min edge (0) and flagged by a **mask channel**; a separate **masked MSE** metric reports error only where $z_\text{re}$ is genuinely defined, so the clamp never hides model error. Final report also gives RMSE in redshift units.
- **Models**: plain `FNO2d` (modes 32², hidden 64, 4 layers, grid pos-emb), `UFNO2d` (sigmoid output, batch/groupnorm), `LocalFNO2d` (windowed, with global bottleneck) — same three-way architecture comparison as the 3-D thread, selected via `MODEL_KIND`.
- **Loss**: `0.5·absL2 + 0.5·absH1` in 2-D — absolute norms deliberately, because the clamped target is ≈ 0 over most of a late-reionizing cone and a relative norm would divide by a near-zero target norm. H¹ is now well-posed (smooth target).
- **Training**: Adam + cosine, 200 epochs default, per-cone split (seed 42), single-A30 SLURM job `slurm/train_zre.sbatch`; per-model-kind checkpoint dirs; end-of-run truth/prediction/error figure for every test cone.

## Status & next steps (2026-07-16)

Implementation, target cache, and reconstruction sanity figures done; **no training results yet**. Next: first FNO2d run → U-FNO2d/LocalFNO2d comparison → the plan's decisive evaluation, always back in $x_\text{HI}$-space (reconstructed front width vs the U-FNO 10.7 Mpc / truth 3.6 Mpc benchmark). Open design questions: whether the lo-z-crossing step target beats the Gompertz midpoint as the training target (the reconstruction test says both reconstruct well), and how to keep mostly-NaN late reionizers from degrading training (mask-weighted loss vs cone filtering).

## Deviations from the parent plan worth remembering

1. **2-D map, not 3-D box** — LOS information enters as input channels; ==the output has no LOS axis at all.==
2. **Fitted from the lightcone, not read from the simulator** — $z_\text{re}$ here is a front-fit midpoint, not 21cmFAST's `z_re_box`; it inherits the lightcone's evolution-across-the-box geometry and needs no new simulation output.
3. **NaN + mask instead of a smooth sentinel transform** — the plan's $1/(1+z_\text{re})$ idea was not needed; the mask + edge-clamp keeps the target field flat (not discontinuous) at the clamp boundary.
