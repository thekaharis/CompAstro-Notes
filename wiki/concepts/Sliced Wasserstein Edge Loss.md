---
type: concept
title: "Sliced Wasserstein Edge Loss"
created: 2026-07-28
updated: 2026-07-28
tags:
  - domain/ml
  - domain/operator-learning
  - concept/loss-design
  - concept/optimal-transport
status: developing
complexity: advanced
domain: Inference and ML
aliases:
  - SWD edge loss
  - Sliced Wasserstein distance
related:
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[Edge and Wall-Placement Losses]]"
  - "[[Ionization Morphology]]"
  - "[[Fourier Neural Operator]]"
---

# Sliced Wasserstein Edge Loss

A transport-based loss term that scores **where** a field's transitions sit, designed as the direct answer to the hedging pathology of pointwise losses ([[Hedging Bias of Pointwise Losses]]).

## Construction

1. **Edge measure.** $m = |\nabla x_\text{HI}|$ on the periodic transverse axes, normalized to unit mass per sample. This turns the field into a probability distribution over transition locations. Normalizing to unit mass is deliberate: the term scores *position* and leaves *amount* of edge to a spectral term such as [[Edge and Wall-Placement Losses|HighKPowerRatio]].
2. **Slicing.** The exact 2-D optimal transport is replaced by the standard sliced approximation (Bonneel et al.): project pixel coordinates onto $N$ random unit directions (default 48) and compare 1-D CDFs, which is the exact 1-D Wasserstein-1 distance along each direction.
3. **Fixed-grid trick.** On a fixed grid the projected coordinates are constant, so the per-direction sort order is precomputed once per spatial shape. Each call is then a gather, a cumsum, and an L1 difference — **no sorting in the training loop**. Directions are seeded, so every DDP rank and every restart slices along the same set.
4. **Units.** Projections are scaled to unit extent, so the value is a mean transport distance in units of the box width — comparable across resolutions.

## Why transport rather than a pointwise gradient term

A pointwise gradient loss (H¹) is minimized by $\mathbb{E}[\nabla u]$, which turns a tall narrow ridge into a low wide bump whenever edge position is uncertain — it rewards exactly the blurring one is trying to remove. The **Wasserstein barycenter of shifted sharp edges is still a sharp edge**, so the cost grows with *displacement* while smearing mass away from the true boundary increases it.

## Limitations measured in practice

- **It constrains neither level nor position absolutely.** Run without an L² (or BCE) anchor, the `edgeonly` variant failed outright — RMSE 0.92, never beating its epoch-0 value.
- **It is cheap in accuracy but did not deliver sharpness on its own.** At weight 140 alongside L², it cost only ~1.1% val L² — the least damaging of the edge terms tried — but front width moved from 2.89 → 2.66 px against a truth of 1.46. Compare [[Edge and Wall-Placement Losses|ExponentialWallDistance]], which reached 1.16 px.
- It is the only edge term tested that can, in principle, **move** an edge rather than steepen it in place, which is why it remains in the mix despite the modest gain.

Implementation: `losses.py::SlicedWassersteinEdges` in the `fno-21cm` repo.
