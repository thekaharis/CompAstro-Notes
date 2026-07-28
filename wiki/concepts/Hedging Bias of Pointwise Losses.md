---
type: concept
title: "Hedging Bias of Pointwise Losses"
created: 2026-07-27
updated: 2026-07-28
tags:
  - concept/ml
  - concept/loss-design
  - concept/boundary-sharpness
  - domain/operator-learning
  - domain/reionization
status: stable
complexity: intermediate
domain: "[[Inference and ML]]"
aliases:
  - "hedging bias"
  - "why L2 blurs edges"
  - "regression to the mean at edges"
related:
  - "[[Contrast Map]]"
  - "[[Contrast Map Sharpening]]"
  - "[[Loss Objective and Operator Basis Sweep]]"
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[Windowed Local-FNO U-Net Findings]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Ionization Morphology]]"
  - "[[Edge and Wall-Placement Losses]]"
  - "[[Sliced Wasserstein Edge Loss]]"
  - "[[Warped LOS Grid Evaluation]]"
sources:
  - "wiki/thesis/notes/NOTES-contrast-map.md §1"
  - "wiki/thesis/notes/FINDINGS-2026-07-26.md §3 (boundary band)"
---

# Hedging Bias of Pointwise Losses

## Statement

If a model is uncertain whether an edge sits at $x_0$ or $x_0\pm\delta$, the **L²-optimal prediction is the expectation over that uncertainty** — a ramp of width $\sim2\delta$. A sharp edge in the *wrong* place costs roughly twice the area of a soft ramp that hedges. So **L² actively rewards blurring**: the blurred front is not a failure of capacity, it is the optimum of the objective.

## Why H¹ does not rescue it

H¹ has the same pathology **one derivative up**. The L²-optimal *gradient* field is $\mathbb{E}[\nabla]$, which turns a tall narrow ridge into a **low wide bump**. Adding a gradient penalty therefore does not buy edge sharpness — it hedges the edge's derivative instead of its value.

This resolves a long-standing puzzle in the 3-D runs: fronts came out **12–14 Mpc against a 3.6 Mpc truth despite the loss being 99.4% H¹ by contribution** ([[Loss Objective and Operator Basis Sweep]]).

## The evidence that it is the objective, not the bandwidth

Measured on the 2-D $x_\text{HI}$ task (256 held-out slices, `whno_glob`):

- truth transitions ~**0.9 px**
- predictions ~**1.7–3.4 px** (2–4× too wide)
- the local branch (6 modes in a 16 px window) can represent ~**1.3–2.7 px** transitions

The models therefore **leave representable sharpness unused**. The binding constraint is the objective, not [[Spectral Mode Cutoff in FNOs|the retained mode count]].

Three independent confirmations, all in [[Contrast Map Sharpening]]:

1. **Post-hoc sharpening can never improve L² for a converged model** — the model already ends in a sigmoid and so spans every monotonic remap of its own logits. If one helped, training would have found it. (General result.)
2. **Given a free, differentiable sharpening dial, gradient descent leaves it at the identity** — learned θ moved 4.75 → 4.43, a map differing from the identity by ≤9e-4, ~130× less than truth-matched sharpness.
3. **The hedging bias is architecture-independent**: the earlier parity diagnostic found both U-FNO (+0.17) and Local-FNO (+0.21) over-predict in nearly-ionized bins ([[Windowed Local-FNO U-Net Findings]]).

## Consequences for the thesis programme

- **Basis-side attacks cannot fix it.** Local-FNO, SirenFNO and the Walsh–Hadamard operator all change *what the model can represent*; none change *what the loss prefers*. This is why none of them dissolved the front-width gap.
- **Output-side attacks cannot fix it.** [[Contrast Map]] is the direct test; closed negative.
- **The two routes that remain are both about changing what is being scored:**
  - **Target-side** — [[Smooth-Target Reparametrization Plan]]: learn a smooth surrogate ($z_\text{re}$) and threshold, so uncertainty becomes front **displacement** rather than front **blurring**.
  - **Loss-side, transport not steepness** — penalise **misplaced** edges rather than reward **steep** ones. Sliced-Wasserstein (SWD) is the live candidate: the only edge term tried that cost less than 1.2% L². Note the hard constraint from the `edgeonly` run (L² 0.9098, never beat epoch 0): **an L² anchor is not optional**, because neither SWD nor a high-k term constrains absolute level or position.

## Connections

- Direct test and refutation of the output-side fix: [[Contrast Map]] / [[Contrast Map Sharpening]]
- Quantified in 3-D and 2-D: [[Loss Objective and Operator Basis Sweep]]
- The failure mode it explains: [[Ionization Morphology]] bubble-wall blurring
- The surviving fix: [[Smooth-Target Reparametrization Plan]]

## The measurement that separates hedging from blur (2026-07-28)

The sections above establish hedging as the *mechanism*. A later probe makes it a **discriminating measurement**, by applying the same monotone sharpening map to two fields of near-identical sharpness (512 held-out slices):

| field | transition width (px) | RMSE before | after sharpening | change |
|---|---|---|---|---|
| **band-limited truth** (blur only, $k_\text{cut}=0.20$) | 3.40 | 0.07734 | 0.07017 | **−9.28%** |
| **model prediction** | 3.21 | 0.15263 | 0.15263 | **+0.00%** |
| truth | 1.47 | — | — | — |

Same operation, same grid, matched starting sharpness — **it repairs one and not the other**. So the model's softness is not band-limiting: a field that is blurry *because it was blurred* is fixed by sharpening; the model's is not.

Two supporting numbers: over the sharpening range, corr(model degradation, the map's pure distortion cost) = **+0.982** — the map does nothing model-specific; and at equal sharpness pure band-limiting costs 0.077 RMSE against the model's 0.153, so in quadrature roughly **86% of the model's error is not blur**.

## Why gradient losses cannot see the problem

Every pointwise-difference loss **saturates with displacement**: once a predicted wall no longer overlaps the true one, moving it further costs nothing more. Measured on a displaced step edge, going from 4 px to 48 px of error changes:

| loss | change |
|---|---|
| L² | 3.5× |
| H¹ | 2.9× |
| **H¹ seminorm** | **1.00×** |
| **H²** | **1.00×** |
| signed-distance wall loss | **144×** |

H¹'s entire sensitivity to placement comes from the L² term inside it. This is the quantitative form of "H¹ does not rescue it" above.

## Resolution of the open lever (2026-07-28)

The "loss-side, transport not steepness" route above has now been tested, and the conclusion needs one amendment: **SWD was not the winner.** SWD is indeed the cheapest edge term (~1.1% L²) but moved front width only 2.89 → 2.66 px. The term that worked is an **exponential-in-distance absolute error** ([[Edge and Wall-Placement Losses]]), reaching **1.16 px against truth 1.46** for ~22% RMSE.

The reason is a sharper version of the hedging statement: the minimiser of a weighted **squared** error (or of BCE) is a weighted conditional **mean** — the blurred compromise. The minimiser of a weighted **absolute** error is a weighted conditional **median**, and *the median of a binary field is binary*. Under uncertainty an absolute-error loss **picks a side instead of averaging**. Hedging is therefore not a property of pointwise losses in general, but of pointwise **squared** losses.

One regime survives as genuine under-commitment rather than misplacement: at $\bar{x}_\text{HI}\approx0.005$–$0.05$ the field is a few isolated neutral islands rendered as correctly-located low-contrast blobs, where a pointwise map does buy a real held-out 2–9% ([[Contrast Map Sharpening]] §band analysis).

> [!info] Independent of all of this, the LOS cache grid discards most of the front structure before training ever sees it — see [[Warped LOS Grid Evaluation]]. The cache bounds what is achievable; the objective determines whether a model reaches that bound. Both are real and they are not the same problem.
