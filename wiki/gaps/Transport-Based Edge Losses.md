---
type: gap
title: "Transport-Based Edge Losses"
created: 2026-07-27
updated: 2026-07-27
tags:
  - gap/open-question
  - gap/thesis-opportunity
  - domain/operator-learning
  - concept/loss-design
  - concept/boundary-sharpness
status: open
priority: high
domain: "[[Inference and ML]]"
related:
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[Contrast Map Sharpening]]"
  - "[[Contrast Map]]"
  - "[[Loss Objective and Operator Basis Sweep]]"
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[Ionization Morphology]]"
---

# Transport-Based Edge Losses

## The question

Can a **transport-based** loss term — sliced-Wasserstein (SWD) or similar — recover bubble-wall sharpness where every pointwise and basis-side attack has failed?

The framing that emerged from the closed contrast-map work: **the loss must penalise *misplaced* edges rather than reward *steep* ones.** Pointwise losses are indifferent to where an edge is beyond the per-pixel cost, so they hedge; a transport metric is by construction sensitive to displacement.

## Why this is now the live lead

The elimination is fairly complete ([[Hedging Bias of Pointwise Losses]]):

- **Basis-side** — Local-FNO, SirenFNO, Walsh–Hadamard all change what the model can represent, not what the loss prefers. None dissolved the front-width gap.
- **Output-side** — [[Contrast Map]] tested directly: post-hoc sharpening provably cannot improve L² for a converged model, and given a free differentiable sharpening dial, gradient descent left it at the identity.
- **Gradient penalties** — H¹ hedges one derivative up. Fronts came out 12–14 Mpc against 3.6 Mpc truth *despite* a 99.4%-H¹ loss.

SWD is the **only edge term tried so far that cost less than 1.2% L²** (0.1072 vs baseline 0.1060 at epoch 25).

## Hard constraints already established

1. **An L² anchor is not optional.** The `edgeonly` run (no L²) failed outright at L² 0.9098, never beating its epoch-0 value — neither SWD nor a high-k term constrains absolute level or position.
2. **highK + contrast is unstable** (NaN by epoch 10, CUDA assert in `HighKPowerRatio._binned_power`); highK alone and contrast alone were each fine. Plausible mechanism: highK's $\log(P_\text{pred}/P_\text{true})$ gradient grows without bound as predicted band power falls. Any new edge term should be stability-tested in combination, not just alone.
3. **Sharpness must be measured, not assumed.** Every edge variant costs L², so their case rests entirely on sharpness — which is *not yet measured at matched final epoch* (see open item in [[Contrast Map Sharpening]]).

## Proposed next steps

1. Finish the **sharpness table at matched epoch 29** for the existing edge-loss runs (baseline / swd / highk / swd+highk). Without it the whole comparison is unresolved.
2. If SWD holds up in 2-D, test **transfer to 3-D**, where the defect is worse (~3.5× vs ~2–4×).
3. Compare head-to-head against the **target-side** route ([[Smooth-Target Reparametrization Plan]]), which achieves the same goal by construction — converting front blurring into front displacement — rather than by a loss term. These are the two surviving strategies and they are substitutes, so the comparison should be explicit.
