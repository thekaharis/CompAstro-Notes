---
type: concept
title: "Hedging Bias of Pointwise Losses"
created: 2026-07-27
updated: 2026-07-27
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
