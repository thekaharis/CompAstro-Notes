---
type: finding
title: "Excursion-Set Diagnostic"
created: 2026-09-24
updated: 2026-09-24
tags:
  - domain/thesis
  - domain/reionization
  - domain/ml
  - concept/physics-informed
  - concept/architecture
  - finding/positive
status: active
verdict: partial
related:
  - "[[Excursion Set Formalism]]"
  - "[[Excursion-Set Input Layer]]"
  - "[[Native LOS Window Training]]"
  - "[[Multi-Field 21cmFAST Data]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[Phase Coherence and Bubble Size Bias]]"
sources:
  - "`fno-21cm/tools_excursion_set_diagnostic.py`, `slurm/excursion_set_diagnostic.sbatch` (job 5148078)"
  - "`fno-21cm/experiments/excursion_set/{summary,slabs}.json`, `excursion_set_diagnostic.png`"
  - "Network predictions: `experiments/los_windows/predictions/contiguous_ep18/` (12 test cones)"
---

# Excursion-Set Diagnostic

**Question:** 21cmFAST (`hii_filter = sharp-k`) ionizes a cell if the density
smoothed by a sharp-k filter of radius R exceeds a barrier at **any** R. How
much of the true $x_\text{HI}$ morphology does that rule explain, applied
directly to the true density -- and where does it beat the trained network?
Answering this needs no training, and decides whether the rule is worth
building into the model ([[Excursion-Set Input Layer]]).

## Method

- **Data**: the 12 test cones with saved `contiguous_ep18` predictions (the best
  native-window run, test MSE 0.00596). 237 slabs of 28 LOS cells (40 Mpc,
  $\Delta z \approx 0.1$) with slab-mean $x_\text{HI}$ in 0.05-0.95.
- **Filtering**: periodic 3-D FFT over a **140-cell LOS chunk** around each slab.
  Box tiling ([[Multi-Field 21cmFAST Data]] §2) makes any 140 consecutive cells a
  full shifted box, so this reproduces coeval filtering up to growth across the
  chunk. Radii 0.9-31 Mpc, keeping $|k|R \le 1$.
- **Barrier, fitted per slab on the truth (an oracle):**
  - *EPS shape*: $B(R) = a - b\,s_R$, $s_R = \sqrt{\sigma^2_\text{min} - \sigma^2_R}$,
    the extended Press-Schechter form -- **two numbers per slab**;
  - *free*: one threshold per radius, fitted by exact coordinate descent on MSE.
- **Baselines**: threshold on the unsmoothed density; best single radius.
- **Metric**: ionized-region IoU with **every method thresholded to the true
  ionized fraction**, so only morphology is compared and the global level is
  given to all. Also within-slab $R^2$.

## Result

| stage (slab mean $x_\text{HI}$) | slabs | network | raw density | best single R | EPS barrier | free barrier |
|---|---:|---:|---:|---:|---:|---:|
| late (0.05-0.35) | 33 | 0.879 | 0.738 | 0.799 | **0.910** | **0.920** |
| mid (0.35-0.65) | 50 | **0.831** | 0.617 | 0.672 | 0.808 | **0.830** |
| early (0.65-0.95) | 154 | **0.801** | 0.586 | 0.580 | 0.694 | 0.719 |

Within-slab $R^2$, late stage: network **0.41**, EPS 0.68, free 0.73.

- **Late reionization: the excursion set wins** (82% of slabs), exactly where the
  network is weakest: its within-slab $R^2$ falls from 0.83 early to **0.41**
  late. The network blurs bubble edges that the rule places sharply (the familiar
  [[Hedging Bias of Pointwise Losses]]).
- **Mid: a tie. Early: the network wins**, 0.80 vs 0.72. With sparse, small
  bubbles, density thresholds alone do not place them. Possible causes (source
  model details, node-box interpolation, which shows up as intermediate-value
  patches in the truth) are not separated.
- **The multi-scale maximum is what matters.** Raw density and any single radius
  are far worse (0.58-0.80). The max over R is a hard, long-range nonlinearity
  that spectral + pointwise layers do not naturally represent.
- **The barrier is simple and smooth.** The 2-number EPS shape reaches ~97% of
  the free barrier. Within a cone the fitted offset $a$ varies smoothly with z
  (0.105 spread, **0.017 residual** after a quadratic), and $b$ is small (median
  0.2). A small network of $(z, \theta)$ should be able to predict it.
- **Ionizing scales** span ~1-20 Mpc roughly evenly (4.6-9.2% of ionized cells per radius) and drop to ~1% per radius above 20 Mpc.

## Caveats

- **The barrier is fitted on the truth**, so the excursion-set columns are
  ceilings for the rule's shape, not achievable scores. A layer must predict
  the barrier from $(z,\theta)$.
- Radii above $L/2\pi = 31.8$ Mpc have a sharp-k cutoff below the fundamental
  mode and leave a constant field; an early version fitted thresholds to its
  round-off. Radii are capped at 31 Mpc.
- 12 cones, one network (`cnn/fno` contiguous). Truth ionized = $x_\text{HI} < 0.5$.

## Consequence

Add the excursion set as **extra input channels, not a replacement**, so the
network keeps its early-reionization advantage: [[Excursion-Set Input Layer]].
Before any training, that layer at initialization already reproduces this
diagnostic's overlaps on real windows (0.915 / 0.852 / 0.777 vs 0.906 / 0.869 /
0.800 across late / mid / early slabs).
