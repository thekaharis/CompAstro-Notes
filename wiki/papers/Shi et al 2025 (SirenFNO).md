---
type: paper
title: "Shi et al 2025 (SirenFNO)"
created: 2026-06-21
updated: 2026-06-21
tags:
  - domain/ml
  - domain/operator-learning
  - architecture/siren
  - architecture/fno
  - concept/spectral-bias
status: summarized
domain: "Inference and ML"
aliases:
  - SirenFNO
  - Shi 2025
  - "SirenFNO: Efficient and Full Frequency Learning of Fourier Neural Operators"
related:
  - "[[Fourier Neural Operator]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Wen et al 2022 (U-FNO)]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
  - "[[Siren3D Residual Refinement Plan]]"
authors: "Pengqing Shi, Jie Yin, Stephen Tierney, Junbin Gao (University of Sydney)"
year: 2025
---

# Shi et al 2025 (SirenFNO)

> **One line:** Replace the FNO's frequency-truncated, per-mode learnable spectral weights with a SIREN hypernetwork that *generates* a kernel weight for **every** Fourier mode — eliminating truncation, removing the low-frequency bias, and keeping a constant, discretization-independent parameter count.

## The problem it targets

A standard [[Fourier Neural Operator]] does not learn a weight for every frequency. To stay efficient it applies **frequency truncation**: it keeps only the lowest `n_modes` modes of the learned spectral convolution $R_\phi(k)$ and discards the rest (see [[Spectral Mode Cutoff in FNOs]]). The paper's framing of the consequences:

1. **Spectral / low-frequency bias.** Empirically FNOs preferentially fit low-frequency content; truncation hard-codes this by removing the high modes from the learned global path entirely. This hurts PDEs with strong high-frequency oscillations.
2. **Broken continuous↔discrete equivalence.** Truncation can break the equivalence between the continuous operator and its discrete representation (cites Gao et al. 2025), undermining the "discretization-invariant" promise.

Prior fixes cited: **U-FNO** (Wen et al. 2022) bolts a local U-Net path onto each Fourier layer to recover high frequencies; **AM-FNO** (Xiao et al. 2024) uses an amortized kernel parameterization without explicit truncation. SirenFNO is in the second family.

## Method

Standard FNO layer:

$$
v^{(l+1)}(x)=\sigma\!\Big(W^{(l)}v^{(l)}(x)+\mathcal{F}^{-1}\big(R^{l}_\phi(k)\cdot \mathcal{F}(v^{(l)})(k)\big)(x)+b^{(l)}\Big).
$$

In the vanilla FNO, $R_\phi(k)$ is a **table of independently learnable complex weights, one per retained mode**, and modes above the cutoff are simply dropped.

SirenFNO instead **parameterizes the whole spectrum with a small sinusoidal MLP (SIREN) hypernetwork**. The mode index/coordinate $k$ is mapped through random Fourier features (RFF) and a SIREN to *produce* the kernel weight $R_\phi(k)$ **mode-wise, for all modes on the full grid** — no truncation:

- The SIREN is an implicit neural representation of the kernel spectrum $k \mapsto R_\phi(k)$.
- Because the kernel is a *function of $k$* rather than a stored table, the **parameter count is constant and independent of resolution / number of modes** — you can query the same SIREN on a finer grid at test time (zero-shot super-resolution, their Fig. 1: train on 32³, test on 64³).
- They further compress the generated kernel with **functional tensor decompositions** — Canonical Polyadic (CP), Tensor-Train (TT), and Tucker — for parameter efficiency.

## Headline claims (their experiments)

- **Full-frequency learning:** the SIREN-generated spectrum spreads representational weight across *all* modes rather than collapsing to low frequencies.
- **Resolution-agnostic:** constant parameter count; demonstrated zero-shot super-resolution on Darcy Flow and other PDE benchmarks.
- **Competitive or better accuracy** vs. vanilla FNO and efficiency-oriented variants on standard PDE benchmarks, at comparable/fewer parameters.

## Why it matters for this thesis

This is the paper behind my **3-D SirenFNO** experiment on the density → $x_\text{HI}$ lightcone map. The motivation is exactly the failure mode I observed: the FNO/U-FNO learnable spectral weights **collapse onto low modes during training** (quantified in [[SirenFNO Spectral Bias Investigation]]). SirenFNO is a principled, full-architecture answer to that bias — distinct from the [[Siren3D Residual Refinement Plan]], which keeps U-FNO and only adds a coordinate-conditioned SIREN *residual head*. SirenFNO replaces the operator's kernel parameterization itself.

Key distinction to keep straight:

| | parameterizes | role of SIREN | bias it attacks |
|---|---|---|---|
| **SirenFNO** (this paper) | the Fourier **kernel** $R_\phi(k)$, full-grid | hypernetwork generating per-mode weights | low-frequency spectral bias at its source |
| **[[Siren3D Residual Refinement Plan]]** | a real-space **residual** on top of frozen U-FNO | coordinate decoder for boundary detail | boundary/Gibbs error in the output field |

## Open questions for the thesis

- Does removing the spectral bias translate into sharper ionization-front (bubble-wall) reconstruction, i.e. lower held-out H¹ and better $P(k)$/$r(k)$ at high $k$? — Not yet, on aggregate metrics (see [[SirenFNO Spectral Bias Investigation]]).
- SirenFNO has no local U-Net path; can a **SirenFNO + U-Net hybrid** combine full-frequency global learning with local Gibbs-free features?
- Tensor-decomposed kernels (CP/TT/Tucker) for the 3-D anisotropic lightcone are untested here and could cut the 64-mode cost.

## Sources

- `Thesis/FNOs/SirenFNO.pdf` — Shi, Yin, Tierney & Gao, *SirenFNO: Efficient and Full Frequency Learning of Fourier Neural Operators*, University of Sydney (2025).
