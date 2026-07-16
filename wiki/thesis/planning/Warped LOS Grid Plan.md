---
type: plan
title: "Warped LOS Grid Plan"
created: 2026-07-16
updated: 2026-07-16
tags:
  - domain/thesis
  - domain/planning
  - domain/ml
  - domain/reionization
  - concept/los-sampling
  - concept/data-representation
status: tooling-complete
related:
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[Windowed Local-FNO U-Net Findings]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
---

# Warped LOS Grid Plan

> **Decision:** Stop assuming the cube cache's LOS grid is harmless. The cache downsamples the native lightcone LOS axis (≈2340 slices, 1.43 Mpc uniform comoving) to 256 slices *uniform in redshift* — which is **coarsest (~37 Mpc) at low z, exactly where the reionization fronts live**, and finest (~5 Mpc) at high z where the field is saturated neutral. Any front structure destroyed at cache time is unlearnable for *every* model trained on the cache, so the grid choice is a hard bound on model quality — potentially a hidden contributor to the bubble-wall floor that all architecture attacks have been fighting.

## The tool: training-free round-trip evaluation

`viz/los_grid_evaluation.py` measures the bound directly, with no training: for each candidate grid it interpolates the native truth onto the grid and back (native → grid → native, both linear, matching `build_cubes.py`), then quantifies the damage where it matters:

- **transition RMSE** — error over voxels with native $x_\text{HI} \in (0.02, 0.98)$ (the fronts)
- **sharpness ratio** — per-ray max $|dx_\text{HI}/d\chi|$ after / before, front rays only (1.0 = fully preserved)
- **fronts missed %** — rays whose native 0.5-crossing disappears entirely
- **global RMSE** — whole volume (saturated-region dominated; context only)

Metrics are additionally broken down by **reionization-timing class** (early $z_{50} > 9.5$ / mid / late $z_{50} < 6.5$ from each cone's global $x_\text{HI}(z)$), because an ensemble-mean warp can look fine on average while badly mistreating the rare early reionizers.

## Candidate grids (same slice budget; 256 and 512)

- `uniform_z` — the current cache scheme (baseline)
- `uniform_chi` — uniform comoving distance
- **`warped` — the headline candidate**: sampling density ∝ ensemble-mean $|d\langle x_\text{HI}\rangle/d\chi|$ + a 20% uniform floor, CDF-inverted onto the slice budget — "sample where ionization changes"
- `envelope90` — like `warped` but using the 90th percentile of the per-cone $|dx/d\chi|$ across cones, so early *and* late reionizers are covered, not just the average one
- `crop15_chi` — uniform-χ over $z \in [5, 15]$ only; $z > 15$ reconstructed as constant

Grids are defined once in redshift via the **ensemble-mean** $\chi(z)$ (per-cone cosmology draws change both the native LOS length — e.g. 2340 vs 2178 slices — and $\chi(z)$), and applied per cone in $z$, matching how `build_cubes.py` works.

## Pipeline integration (already merged)

- `build_cubes.py --target-z <file> [--target-z-key warped_512]` builds the cube cache on any explicit grid (`.npz`/`.npy`/text, e.g. the `grids.npz` written by the evaluation script).
- `fno_21cm_3d.py` gains `LOSS_LOS_VOLUME_WEIGHTS=1`: on a non-uniform LOS grid, voxel count *is* loss weight, so densely sampled epochs would dominate the L²/H¹ terms; the flag applies Δχ quadrature weights along the LOS so the loss is volume-weighted regardless of grid (no-op-ish for uniform-χ, mildly reweights uniform-z).

## Status (2026-07-16)

Tooling complete with a passing synthetic self-test (warped must beat uniform_z transition RMSE by >2× and preserve gradients better; identity grid must round-trip losslessly). The evaluation on real cones runs on the cluster (`--n-cones 12`, CPU-only login node); **real-data numbers not yet produced/synced**. Next: run the evaluation → pick the winning grid → rebuild the cube cache → retrain the U-FNO benchmark on the warped cache with volume-weighted loss.

## How it fits the thread

This is a *data-representation* attack on the same bubble-wall problem as the basis-side ([[SirenFNO Spectral Bias Investigation]], [[Windowed Local-FNO U-Net Findings]]) and target-side ([[Smooth-Target Reparametrization Plan]]) attacks — and it is logically prior to both: if the cache grid itself destroys front structure, no architecture or target choice downstream can recover it. It also composes with them (a warped cache helps any model trained on it).
