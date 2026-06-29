---
type: concept
title: "Spectral Mode Cutoff in FNOs"
created: 2026-06-20
updated: 2026-06-21
tags:
  - domain/ml
  - domain/operator-learning
  - concept/spectral-truncation
  - concept/spectral-bias
  - finding/negative
status: developing
complexity: advanced
domain: "Inference and ML"
aliases:
  - FNO mode cutoff
  - spectral cutoff
  - n_modes cutoff
  - low-frequency bias
related:
  - "[[Fourier Neural Operator]]"
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[Siren3D Residual Refinement Plan]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
  - "[[Shi et al 2025 (SirenFNO)]]"
  - "[[Windowed Local-FNO U-Net Plan]]"
---

# Spectral Mode Cutoff in FNOs

## Core distinction

The `n_modes` parameter in an FNO is **not a hard band-limit on the model output**. It limits the Fourier modes used by the learned non-local spectral convolution:

$$
\mathcal{K}_\ell v
=
\mathcal{F}^{-1}
\left[
R_\ell(\mathbf{k})\,\mathcal{F}(v)(\mathbf{k})
\right]_{|\mathbf{k}_i|<m_i}.
$$

A complete FNO block also contains a full-resolution pointwise path, a nonlinearity, and—in U-FNO—a local U-Net path:

$$
v_{\ell+1}
=
\sigma\!\left(
\mathcal{K}_\ell v_\ell
+ W_\ell v_\ell
+ U_\ell v_\ell
\right).
$$

The $W_\ell$ path acts at every voxel and therefore is not spectrally truncated. Nonlinear activations can mix frequencies, and the U-Net path can construct sharp local structure directly in real space. Consequently, predictions can contain power above the spectral branch's nominal cutoff.

The safe interpretation is:

> `n_modes` controls the bandwidth and capacity of learned **global communication**, not the maximum frequency present in the prediction.

## Why mode count is not one physical cutoff on a lightcone

For a periodic axis of length $L_i$, a nominal retained-mode edge is

$$
k_{\mathrm{cut},i}\approx \frac{2\pi m_i}{L_i}.
$$

For the current $140\times140\times256$ lightcones, with approximately 200 Mpc transverse extent and 3340 Mpc LOS extent:

| `n_modes` | nominal transverse edge | nominal LOS edge |
|---|---:|---:|
| $(16,16,16)$ | $\sim0.50\ \mathrm{Mpc}^{-1}$ | $\sim0.030\ \mathrm{Mpc}^{-1}$ |
| $(16,16,32)$ | $\sim0.50\ \mathrm{Mpc}^{-1}$ | $\sim0.060\ \mathrm{Mpc}^{-1}$ |
| $(24,24,24)$ | $\sim0.75\ \mathrm{Mpc}^{-1}$ | $\sim0.045\ \mathrm{Mpc}^{-1}$ |

These are orientation-dependent nominal edges, not a single radial $k_{\max}$. The LOS is also an evolving lightcone rather than a stationary periodic volume, so its Fourier index should not be read as a clean cosmological wavenumber without a windowed/coeval analysis.

## Experimental findings

The lightcone campaign in [[FNO Lightcone Experimental Findings]] tested the mode-capacity hypothesis repeatedly:

1. **Pure FNO: $(16,16,16)\to(24,24,24)$** produced overlapping validation trajectories and no qualitative improvement.
2. **U-FNO: $m_z=16\to32$**, bundled with GroupNorm and stronger H¹ weighting, tied the original U-FNO floor and was slightly worse in H¹.
3. **Anisotropic U-Net LOS stride** doubled the bottleneck's LOS receptive field but converged to the same floor.

Together these results rule out a shortage of retained LOS modes—and, more broadly, LOS receptive field—as the active bottleneck at the tested width and dataset size. They do **not** prove that high-frequency boundary structure is irrelevant. They show that supplying more global Fourier bandwidth does not make the network usefully reconstruct it.

## Practical consequence

Future experiments should not be justified as “raising the output cutoff.” They must name which route produces the missing detail:

- more non-local bandwidth through the spectral branch;
- local real-space features through convolution;
- coordinate-conditioned detail through an implicit decoder such as [[Siren3D Residual Refinement Plan]];
- or a loss/sampling scheme that concentrates supervision on ionization boundaries.

The current evidence favours the latter two. U-FNO already demonstrated that changing basis from global Fourier to local convolution matters; further mode increases did not.

## Direct measurement: the learned weights collapse onto low modes

The mode-count nulls above are an *inference* about how the model uses its bandwidth. The mode-weight diagnostic in [[SirenFNO Spectral Bias Investigation]] turns it into a *measurement*. Logging the per-mode RMS of the learned spectral weights $R_\phi(k)$ per epoch shows the U-FNO **collapses onto the lowest modes within the first epoch and stays there**:

- 32-LOS-mode U-FNO: the lowest 8 of 32 modes hold **52%** of the spectral weight at convergence (uniform = 25%); half the spectral energy is reached by mode 7/31; the per-layer high/low cutoff ratio falls from 1.0 at init to 0.1–0.45.
- 64-LOS-mode U-FNO: same qualitative collapse, spread over more modes (low-quarter fraction 0.36, half-energy at mode 27/63).

This is the concrete mechanism behind the null results: **extra modes are learned but then down-weighted**, so adding bandwidth cannot help. It is the well-known FNO *low-frequency (spectral) bias*, now quantified on the 21cmFAST lightcone.

[[Shi et al 2025 (SirenFNO)]] attacks the bias at its source: a SIREN hypernetwork generates the kernel for *all* modes, and the measured spectrum then stays flat (low-quarter fraction pinned at 0.25, cutoff ratio ≈1.0) across training — confirming the collapse is specific to the per-mode learnable-table parameterization, not inevitable. Whether removing the bias improves bubble-wall fidelity is still open; see [[SirenFNO Spectral Bias Investigation]] §4.
