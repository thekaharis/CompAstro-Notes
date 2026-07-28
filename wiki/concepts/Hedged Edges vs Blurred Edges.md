---
type: concept
title: "Hedged Edges vs Blurred Edges"
created: 2026-07-28
updated: 2026-07-28
tags:
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - concept/loss-design
  - concept/sharp-fronts
status: mature
complexity: intermediate
domain: Inference and ML
aliases:
  - Hedging
  - L2-optimal blurring
  - Edge hedging
related:
  - "[[Contrast Map Investigation]]"
  - "[[Edge and Wall-Placement Losses]]"
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[Sliced Wasserstein Edge Loss]]"
  - "[[Ionization Morphology]]"
sources:
  - "[[.raw/reports/NOTES-contrast-map.md]]"
---

# Hedged Edges vs Blurred Edges

> **The distinction:** a soft ionization front in a prediction can be soft for two completely different reasons, and they demand opposite fixes. A **blurred** edge is a sharp edge whose high-$k$ content was removed — it is repaired by sharpening. A **hedged** edge is a sharp edge whose *position* is uncertain, so the loss-optimal prediction averages over the possible positions — it is not repaired by sharpening at all, only by a loss that penalises misplacement. The FNO family's front-width deficit on 21 cm lightcones is measured to be **hedging, not blur**.

## Why pointwise losses hedge

If a model is uncertain whether a front sits at $x_0$ or $x_0 \pm \delta$, the L²-optimal prediction is the expectation over that uncertainty — a ramp of width $\sim 2\delta$. A sharp edge in the *wrong* place costs roughly twice the area of a soft ramp that splits the difference, so **L² actively rewards blurring**.

H¹ has the same pathology one derivative up: the L²-optimal *gradient* field is $\mathbb{E}[\nabla u]$, which turns a tall narrow ridge into a low wide bump. This resolves a long-standing puzzle in the 3-D runs of [[FNO Lightcone Experimental Findings]] — predicted fronts come out 12–14 Mpc against a 3.6 Mpc truth *despite* the loss being 99.4% H¹ by contribution (see [[Edge and Wall-Placement Losses]]).

BCE is no better: the minimiser of any weighted **squared** error (or of BCE) is a weighted conditional **mean**, which is exactly the blurred compromise. Only a weighted **absolute** error has a conditional **median** minimiser, and the median of a binary field is binary — under uncertainty it picks a side instead of averaging.

## The measurement that separates the two

The decisive experiment (2026-07-27, 2-D $x_\text{HI}$ task, 512 held-out slices) applies the same monotone sharpening map to two fields of near-identical sharpness:

| field | transition width (px) | RMSE before | RMSE after sharpening | change |
|---|---|---|---|---|
| **band-limited truth** (blur only, $k_\text{cut}=0.20$) | 3.40 | 0.07734 | 0.07017 | **−9.28%** |
| **model prediction** | 3.21 | 0.15263 | 0.15263 | **+0.00%** |
| truth | 1.47 | — | — | — |

Same operation, same parameter grid, matched starting sharpness — it fixes one and not the other. Supporting numbers: over the sharpening range, the correlation between the model's degradation and the map's pure distortion cost is **+0.982**, i.e. the map does nothing model-specific; and subtracting the distortion in quadrature still leaves every value above identity, so no benefit hides underneath the cost.

A second quadrature estimate says the same thing from the other side: at equal sharpness pure band-limiting costs 0.077 RMSE while the model costs 0.153, so $\sqrt{0.153^2 - 0.077^2} \approx 0.132$ — roughly **86% of the model's error is not blur**.

## Consequences

1. **Post-processing is a dead end.** Any pointwise remap of a converged model's output is something the model's own output sigmoid could already have applied; if it improved L², training would have found it. Confirmed both post-hoc and end-to-end in [[Contrast Map Investigation]].
2. **Bandwidth is not the binding constraint.** The local branch of the windowed operator can represent ~1.3–2.7 px transitions and the model leaves that representable sharpness unused. The objective is the constraint, not the basis — which reframes the whole basis-side attack line ([[SirenFNO Spectral Bias Investigation]], [[Windowed Local-FNO U-Net Findings]]).
3. **The loss must penalise *misplacement*, not reward *steepness*.** Every pointwise-difference loss saturates with displacement: once a predicted wall no longer overlaps the true one, moving it further costs nothing more. Measured on a displaced step edge, going from 4 px to 48 px of error changes L² by 3.5×, H¹ by 2.9×, and the H¹ *seminorm* and H² by exactly **1.00×** — gradient-only losses are completely blind to misplacement. A signed-distance-weighted loss changes by **144×** over the same range. See [[Edge and Wall-Placement Losses]].
4. **Or dissolve the problem in the target.** This is the independent motivation for [[Smooth-Target Reparametrization Plan]] / [[Lightcone z_re Map Target]]: on a smooth surrogate target, uncertainty shows up as front *displacement* by construction, and the reconstructed front stays step-sharp.

> [!key-insight]
> "Sharper" and "better placed" are different objectives, and only one of them is what the physics diagnostics ([[Bubble Size Distribution]], $P(k)$, $r(k)$) actually reward. Reporting a sharpening dial as a model improvement is a category error — it is post-processing.

## Where hedging is *not* the whole story

Resolved against ionization state, there is one regime where the field really is under-committed rather than misplaced: at $\bar{x}_\text{HI} \approx 0.005$–$0.05$ (very late reionization) the field is a handful of isolated neutral islands that the model renders as correctly-located low-contrast blobs. There a pointwise sharpening map buys a genuine held-out **2–9%** ([[Contrast Map Investigation]] §band analysis). Above $\bar{x}_\text{HI} \approx 0.1$, where the field is a dense bubble network, it buys exactly 0.00%.
