---
type: plan
title: "Siren3D Residual Refinement Plan"
created: 2026-06-20
updated: 2026-06-20
tags:
  - domain/thesis
  - domain/planning
  - domain/ml
  - domain/operator-learning
  - architecture/siren
status: draft
related:
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[FNO Approach for 21cm Emulation]]"
  - "[[FiLM Conditioning]]"
---

# Siren3D Residual Refinement Plan

> **Decision:** Test Siren3D as a coordinate-conditioned refinement module on top of the converged U-FNO, not as a standalone replacement for the density-to-ionization operator.

## Motivation

The U-FNO floor is stable at approximately

$$
\mathrm{val}\ L^2=0.0418,\qquad \mathrm{val}\ H^1=8.27.
$$

More Fourier modes, stronger H¹ weighting, alternative normalisation, and a larger LOS receptive field did not improve it. The remaining error is concentrated around ionization fronts. A SIREN—an MLP with sinusoidal activations—offers a different representation for coordinate-dependent, high-frequency detail and has well-behaved analytic spatial derivatives.

However, a standalone coordinate MLP does not naturally see the full non-local density field that determines bubble placement. The experiment should preserve U-FNO as the global operator and ask a narrower question:

> Given the U-FNO prediction and context, can a sinusoidal coordinate decoder correct boundary geometry below the U-FNO floor?

## Proposed model

For each queried voxel coordinate $\mathbf{r}=(x,y,z)$, trilinearly sample a context vector from the frozen or jointly trained U-FNO:

$$
c(\mathbf{r})=
\left[
h_{\mathrm{UFNO}}(\mathbf{r}),
\hat{x}_{\mathrm{HI}}^{\,\mathrm{UFNO}}(\mathbf{r}),
\delta_m(\mathbf{r}),
z(\mathbf{r}),
\theta_{11}
\right].
$$

The Siren3D head predicts a **logit residual**:

$$
\hat{x}_{\mathrm{HI}}(\mathbf{r})
=
\sigma\!\left(
\operatorname{logit}\hat{x}_{\mathrm{HI}}^{\,\mathrm{UFNO}}(\mathbf{r})
+ \alpha\,f_{\mathrm{SIREN}}(\mathbf{r},c(\mathbf{r}))
\right),
$$

where $\alpha$ is zero-initialized or learned from zero. This makes the initial model exactly reproduce the U-FNO baseline and prevents the new head from destroying already-correct neutral/ionized regions.

In implementation, clamp the baseline prediction to $[\varepsilon,1-\varepsilon]$ before applying `logit` so saturated voxels remain numerically finite.

### Minimum architecture

- 5–6 hidden layers, width 128–256
- sine activation in hidden layers
- SIREN initialization; tune first-layer frequency $\omega_0$ rather than using ordinary Xavier initialization
- normalized coordinates in $[-1,1]^3$
- U-FNO context projected to a compact conditioning vector before concatenation or FiLM modulation
- residual logit output with a zero-initialized gate

## Training ladder

### Stage 0 — boundary diagnostic

Before training, quantify where the baseline error lives:

- distance-to-boundary histogram of squared error;
- L² and H¹ inside a narrow boundary band;
- power-spectrum ratio and cross-correlation as functions of $k$ and redshift;
- calibration of predicted $x_{\mathrm{HI}}$ near 0 and 1.

This establishes whether a boundary refiner is targeting enough of the total error to matter.

### Stage 1 — frozen U-FNO, residual-only Siren3D

- Freeze the converged v1 U-FNO.
- Train only the Siren3D head.
- Sample all easy voxels sparsely, but oversample truth/prediction boundary bands and hard redshift slices.
- Keep a non-zero uniform sample fraction so global calibration cannot drift.

Recommended loss:

$$
\mathcal{L}
=
\lambda_2\mathcal{L}_{L^2}
+\lambda_\nabla\mathcal{L}_{\nabla}
+\lambda_b\mathcal{L}_{\mathrm{boundary}}
+\lambda_{\mathrm{PS}}\mathcal{L}_{P(k)}.
$$

Start without the power-spectrum term; add it only if boundary gains damage large-scale statistics.

### Stage 2 — limited joint fine-tuning

If Stage 1 improves held-out H¹ without degrading L² or $P(k)$:

- unfreeze only the U-FNO projection and final U-Fourier block;
- use a 10–100× smaller learning rate for U-FNO than for Siren3D;
- retain the residual gate and baseline-preservation check.

Do not immediately fine-tune the whole 28 M-parameter U-FNO; that would obscure whether the gain came from the SIREN representation or ordinary retraining.

### Stage 3 — ablations

Compare against parameter-matched alternatives:

1. ReLU/GELU coordinate MLP residual
2. Fourier-feature MLP residual
3. small 3-D convolutional residual head
4. Siren3D without latent U-FNO context
5. Siren3D without boundary-aware sampling

The key causal claim requires SIREN to beat these controls, not merely beat the frozen baseline.

## Success and stop criteria

### Success

- at least 5% relative reduction in held-out H¹ from 8.27;
- no statistically meaningful degradation in held-out L²;
- large-scale $P(k)$ and $r(k)$ remain within the existing U-FNO error envelope;
- gains repeat across multiple seeds and are concentrated near true bubble boundaries;
- improvement survives evaluation on both validation and test cones.

### Stop

Stop the Siren3D branch if:

- it only improves training metrics;
- gains vanish against a parameter-matched non-sinusoidal MLP;
- sharper-looking fronts worsen power spectra or ionization history;
- or boundary-band correction is too small to move whole-volume metrics.

## Risks

- SIRENs represent high frequencies well but do not make discontinuities easy by magic; ringing remains possible.
- Coordinate networks can memorize spatial coordinates if cone identity or positional leakage is present.
- Uniform voxel sampling will be dominated by trivial all-neutral/all-ionized regions.
- Full-cube coordinate evaluation is expensive; chunked query evaluation and sampled training are required.
- The LOS coordinate mixes position and cosmic evolution. Redshift/context must remain explicit so the head does not interpret the lightcone as a stationary spatial axis.

## Recommended execution order

1. Complete the cheap global-pooling residual experiment already motivated by Act 7.
2. Run the Stage-0 boundary diagnostic.
3. If boundary error is dominant, run frozen-U-FNO Siren3D and the Fourier-feature/ReLU controls.
4. Jointly fine-tune only after a clean residual-only win.

This ordering keeps the scientific claim legible: first test missing global context, then test whether a coordinate-based local representation adds something genuinely different.
