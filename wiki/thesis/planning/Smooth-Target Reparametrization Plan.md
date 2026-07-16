---
type: plan
title: "Smooth-Target Reparametrization Plan"
created: 2026-07-15
updated: 2026-07-16
tags:
  - domain/thesis
  - domain/planning
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - concept/spectral-bias
  - concept/target-reparametrization
status: draft
related:
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[Windowed Local-FNO U-Net Findings]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Siren3D Residual Refinement Plan]]"
  - "[[Windowed Local-FNO U-Net Plan]]"
  - "[[Excursion Set Formalism]]"
  - "[[Neutral Fraction]]"
  - "[[P1 EFT Characterization]]"
  - "[[Ionization Morphology]]"
---

# Smooth-Target Reparametrization Plan

> **Status update (2026-07-16):** candidate 1 is now implemented — with a modification — as a per-pixel $z_\text{re}(x,y)$ map *fitted from the existing lightcones* (Gompertz/step least squares) rather than the native `z_re_box`, trained by a 2-D FNO. Reconstruction sanity checks pass; training pending. See [[Lightcone z_re Map Target]]. A complementary data-side attack on the same wall problem is also filed: [[Warped LOS Grid Plan]].

> **Decision:** Stop learning $x_\text{HI}$ directly. Learn a **smooth surrogate field** that is compatible with the FNO/U-FNO inductive bias, and reconstruct $x_\text{HI}$ from it deterministically. Primary candidate: the **reionization redshift field $z_\text{re}(\mathbf{x})$**, which 21cmFAST outputs natively.

## Why change the target, not the architecture

Every attack so far has changed the *basis* while keeping the discontinuous target:

- More global modes / channels / BCE — null ([[FNO Lightcone Experimental Findings]] Acts 3–4, 6).
- SirenFNO (hypernetwork kernel, no spectral bias) — beats plain FNO, trails U-FNO ([[SirenFNO Spectral Bias Investigation]]).
- Windowed Local-FNO (localized transform) — *broadens* fronts 3× vs U-FNO ([[Windowed Local-FNO U-Net Findings]]).

The persistent failure mode is that L²-optimal behavior under uncertainty in $x_\text{HI}$-space is **diffusion**: the model hedges with ≈0.3 interiors and blurred walls (the H¹ ceiling). The reparametrization idea inverts this: choose a target where model uncertainty manifests as **front displacement** instead of front blurring. A regression error in a smooth surrogate moves a wall that stays step-sharp by construction; it cannot blur it. The Gibbs/spectral-bias problem is dissolved rather than fought, because the field the network must represent has no step discontinuities.

The deeper physics justification: 21cmFAST's $x_\text{HI}$ *is* a threshold of a smooth latent (the excursion-set smoothed $\zeta f_\text{coll}$ field — [[Excursion Set Formalism]]). The sharpness is manufactured by the simulator's final nonlinearity; it is not present in the latent physics. Learning the smooth part and hardcoding the sharp part matches the generative structure of the simulator.

## Candidate targets (priority order)

### 1. Reionization redshift field $z_\text{re}(\mathbf{x})$ — primary

For each comoving position, the redshift at which it ionizes.

- **Smooth**: spatially correlated with large-scale density — exactly what the Fourier basis represents well ([[Spectral Mode Cutoff in FNOs]] collapse becomes harmless).
- **Free targets**: 21cmFAST outputs `z_re_box` natively; no code surgery.
- **Deterministic reconstruction**: $x_\text{HI}(\mathbf{x}, z) = \mathbb{1}[z > z_\text{re}(\mathbf{x})]$, then the existing lightcone interpolation onto the 256-cell LOS grid recovers partial-ionization cells at fronts.
- **Well-conditioned error**: L² in $z_\text{re}$-space = front-*timing* error. Hedging moves the front; it cannot diffuse it.
- **Dimensional simplification**: one coeval 3-D scalar box replaces the full lightcone step structure along the LOS.
- **Literature cover**: Battaglia et al. 2013 established $z_\text{re}$ as the natural smooth parameterization of patchy reionization (semi-numeric $z_\text{re}$–$\delta$ mapping); `zreion` is built on it. Also connects to [[P1 EFT Characterization]] — the $z_\text{re}$ field admits a bias-expansion description.

**Caveats**
- Assumes monotonic ionization (no re-neutralization). Holds for the current 21cmFAST configuration; breaks if inhomogeneous recombinations are enabled later. Check the flag before generating targets.
- Cells never ionized within the simulated range need a sentinel value (e.g. $z_\text{re} < 5$ floor) — choose one that keeps the target field smooth at the sentinel boundary, or regress a transformed variable like $1/(1+z_\text{re})$.
- Input/output geometry changes: the natural target is a coeval box while the current pipeline conditions on the density *lightcone*. Options: (a) keep the lightcone input, output the transverse $z_\text{re}$ map (140×140) or the full coeval box; (b) condition on the IC/early density box + $\theta_{11}$, output the $z_\text{re}$ box — cleaner, and closer to how `zreion` frames it. Decide at pipeline-design time; (b) is the recommended default.

### 2. Signed distance to the ionization front — secondary

$\phi(\mathbf{x}, z)$ = signed Euclidean distance to the nearest front in the lightcone; reconstruct via $x_\text{HI} = \mathbb{1}[\phi > 0]$.

- Smooth by construction ($|\nabla\phi| \approx 1$ away from the skeleton), level-set / DeepSDF trick.
- No monotonicity assumption — survives recombinations.
- Targets computed offline via `scipy.ndimage.distance_transform_edt` on the binarized cache (one extra precompute pass, same HDF5 pattern as `build_cubes.py`).
- **Free parameters to fix**: truncation radius (clamp $|\phi| \le \phi_\text{max}$ so the target stays informative near fronts and constant far away), anisotropic voxel scaling (transverse ~1.43 Mpc vs LOS ~13 Mpc cells), and handling of fully-neutral / fully-ionized cones (no front exists → clamp everywhere).

### 3. Pre-threshold excursion-set field — most principled, most friction

Learn the smoothed $\zeta f_\text{coll}$ (or $n_\text{ion}$) field; apply the excursion-set max-over-scales + threshold as a **fixed, non-learned physics layer**.

- Matches the simulator's generative structure exactly; the network only learns the smooth latent it is good at.
- Best EFT connection: the latent is far closer to something with a controlled bias expansion than binary $x_\text{HI}$.
- **Friction**: 21cmFAST does not cheaply expose this field — requires code surgery to dump it. Park for now; revisit if 1–2 succeed and the EFT thread wants the latent.

## Experimental design (Phase 1: $z_\text{re}$)

1. **Target generation**: re-run or post-process the LHS design to cache `z_re_box` per cone. If re-simulation is needed, verify seeds/parameters reproduce the existing cache (spot-check a few cones' $x_\text{HI}$ against the current HDF5).
2. **Transform**: z-score $z_\text{re}$ (or $1/(1+z_\text{re})$) against the cache distribution; document the sentinel convention.
3. **Model**: reuse the U-FNO (current best) *and* the plain FNO. Prediction: on a smooth target, the plain FNO's disadvantage should shrink dramatically — this is itself a diagnostic of the reparametrization claim.
4. **Loss**: L² + H¹ on the $z_\text{re}$ field (H¹ is now well-posed — the target has no steps).
5. **Reconstruction**: threshold + lightcone interpolation, fixed and non-learned. No gradients through it in Phase 1 (train purely in target space; avoids the dead-gradient problem entirely).
6. **Evaluation — in $x_\text{HI}$-space, always**: reconstructed test L² / H¹, boundary-band RMSE + gradient error, **10–90% front width** (truth 3.6 Mpc; U-FNO 10.7; Local-FNO 32.2), $P(k)$, $r(k)$ high-$k$, global $\bar{x}_\text{HI}(z)$. A $z_\text{re}$ model can look excellent in its own space while systematically misplacing fronts — target-space metrics are never the verdict.
7. **Extra diagnostic unique to this approach**: the front-displacement error distribution, $\Delta z_\text{re}(\mathbf{x}) = \hat{z}_\text{re} - z_\text{re}$ — its spatial power spectrum says *where* timing errors live (large-scale timing bias vs small-scale jitter), which is more interpretable than any $x_\text{HI}$ residual map.

## Success criteria

> Reconstructed-field **front width < 10.7 Mpc** (beat U-FNO) with test L² within 10% of the U-FNO floor (0.0408) and no degradation in $P(k)$ / $r(k)$ / $\bar{x}_\text{HI}(z)$. Front width is the primary axis — this plan exists to fix walls, not whole-volume L².

Secondary claims worth recording even on partial success: (a) plain-FNO vs U-FNO gap shrinking on the smooth target (evidence the U-Net path was compensating for the target, not the physics); (b) front-displacement spectrum characterization.

## Failure modes to watch

- **Threshold amplification**: where $|\nabla z_\text{re}|$ is small (slowly ionizing regions), a small $z_\text{re}$ error displaces the front a long way. The reconstructed-field metrics catch this; the displacement diagnostic localizes it.
- **Sentinel contamination**: never-ionized cones (e.g. cone 1982-like) put a large sentinel mass in the target distribution; check they don't dominate the loss.
- **Partial ionization**: 21cmFAST cells at fronts can be genuinely fractional; pure thresholding loses this. The lightcone interpolation recovers most of it; quantify the residual on truth data *before* training (reconstruct truth $x_\text{HI}$ from truth $z_\text{re}$ — this bounds the ceiling of the whole approach and costs one afternoon).
- **End-to-end temptation**: if target-space training plateaus, a temperature-annealed sigmoid threshold (or straight-through estimator) allows fine-tuning through the reconstruction — but this reintroduces the hedging incentive. Only as a Phase-2 escalation.

## Run order

1. **Ceiling check (cheap, do first)**: reconstruct truth $x_\text{HI}$ lightcones from truth `z_re_box` + interpolation; measure reconstruction-only L²/H¹/front width vs the cached truth. If this ceiling is already worse than the U-FNO floor, stop.
2. Target cache build (extend `build_cubes.py` pattern).
3. U-FNO on $z_\text{re}$, 30 epochs, standard DDP setup → reconstruct → full diagnostic suite vs U-FNO benchmark.
4. Plain-FNO on $z_\text{re}$ (the "does the smooth target rescue the weak architecture" test).
5. Decision point: escalate to signed-distance (target 2) only if $z_\text{re}$ fails for reasons the SDF fixes (non-monotonicity, geometry); escalate to end-to-end fine-tuning only if fronts are sharp but misplaced with a learnable pattern.

## How it fits the thread

The basis-side attacks ([[SirenFNO Spectral Bias Investigation]], [[Windowed Local-FNO U-Net Plan]], [[Siren3D Residual Refinement Plan]]) all fight the mismatch between a Fourier-dominated representation and a step-function target. This plan is the orthogonal axis: keep the winning architecture, change the target so the mismatch never arises. It is also the cheapest remaining lever — same pipeline, same conditioning, one new cache field — and the one with the best EFT synergy, since $z_\text{re}$ (and the excursion-set latent behind it) is the object with a natural perturbative description.
