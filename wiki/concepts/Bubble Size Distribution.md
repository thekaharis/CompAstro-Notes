---
type: concept
title: "Bubble Size Distribution"
created: 2026-07-28
updated: 2026-07-28
tags:
  - domain/reionization
  - domain/ml
  - concept/morphology
  - concept/diagnostic
status: developing
complexity: intermediate
domain: Reionization Physics
aliases:
  - BSD
  - Mean free path bubble size
related:
  - "[[Ionization Morphology]]"
  - "[[Mean Free Path]]"
  - "[[Excursion Set Formalism]]"
  - "[[Bias Expansion]]"
  - "[[Structured-Transform Operator Findings]]"
  - "[[Neutral Fraction]]"
---

# Bubble Size Distribution

The distribution of characteristic ionized-region sizes at a given stage of reionization. It is the morphological statistic that a power spectrum compresses away, and it is the natural physical target for judging whether an emulator got the *topology* right rather than just the pixel values.

## Why it matters for this thesis

- In the [[Bias Expansion]], the characteristic bubble scale $R_\text{eff}$ is what the derivative operator's coefficient $b_{\nabla^2}^x$ encodes — the BSD is the real-space shadow of that EFT term.
- It is set jointly by the [[Excursion Set Formalism]] barrier and the [[Mean Free Path]] ceiling $R_\text{mfp}$, both of which differ between simulators — so BSD comparison is a direct probe of [[Simulator Dependence]].
- Unlike RMSE, it is insensitive to a globally displaced-but-correct morphology, so it separates "wrong field" from "right field, wrong place".

## Measurement: transverse periodic mean-free-path method

The estimator adopted in the `fno-21cm` diagnostics (`method: transverse_periodic_mean_free_path`):

- Threshold the field at $x_\text{HI} = 0.5$; cast 256 rays per slice from random ionized starting points in random transverse directions; record the distance to the first neutral cell, using periodic wrapping on the transverse axes.
- Box 200 Mpc, 24 log bins, max distance 200 Mpc. Rays that never terminate are recorded as **censored**, and the reported means are *restricted* means over the uncensored population — necessary because early in reionization a large fraction of rays (40%+ in the $\bar{x}_\text{HI} = 0.02$–$0.20$ stage) run the full box.
- Results are binned by global stage $\bar{x}_\text{HI} \in \{0.02\text{–}0.20, 0.20\text{–}0.40, 0.40\text{–}0.60, 0.60\text{–}0.80, 0.80\text{–}0.98\}$ plus an "active" $0.05$–$0.95$ pooling.

Reported per stage: restricted mean (Mpc), relative mean bias, restricted Wasserstein distance between the truth and prediction distributions, Jensen–Shannon divergence, and censored/underflow fractions.

## Measured on the best U-FNO (2026-07-22)

| stage $\bar{x}_\text{HI}$ | cones | truth mean (Mpc) | pred mean (Mpc) | rel. bias | $W_1$ (Mpc) | JS div |
|---|---|---|---|---|---|---|
| 0.02–0.20 | 72 | 130.4 | 137.0 | **+6.8%** | 15.52 | 0.0165 |
| 0.20–0.40 | 79 | 57.2 | 59.4 | **+9.3%** | 8.47 | 0.0147 |
| 0.40–0.60 | 91 | 25.5 | 27.9 | +6.0% | 3.25 | 0.0078 |
| 0.60–0.80 | 113 | 10.3 | 11.7 | +3.9% | 0.87 | 0.0046 |
| 0.80–0.98 | 168 | 3.15 | 3.05 | −2.6% | 0.22 | 0.0029 |
| active 0.05–0.95 | 153 | 10.4 | 13.4 | +2.4% | 1.54 | 0.0047 |

> [!key-insight]
> The bias is **systematically positive and grows toward early times**: the emulator makes bubbles too big while reionization is still sparse, and only crosses to slightly-too-small at the very end. This is the morphological signature of the same soft-front behaviour diagnosed in [[Hedging Bias of Pointwise Losses]] — an under-committed wall pushed outward reads as a larger bubble. JS divergences stay small (≤0.017) throughout, so the *shape* of the distribution is well recovered; it is the *scale* that drifts.

Figures: `wiki/thesis/findings/figures/bubble-size_20260722/`.

![[bubble_size_summary.png]]
