---
type: concept
title: "Contrast Map"
created: 2026-07-27
updated: 2026-07-27
tags:
  - concept/ml
  - concept/loss-design
  - concept/boundary-sharpness
  - domain/operator-learning
status: stable
complexity: intermediate
domain: "[[Inference and ML]]"
aliases:
  - "(theta, tau) contrast map"
  - "contrast head"
  - "tanh contrast reshaping"
related:
  - "[[Contrast Map Sharpening]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[Ionization Morphology]]"
  - "[[Neutral Fraction]]"
  - "[[Fourier Neural Operator]]"
sources:
  - "wiki/thesis/notes/NOTES-contrast-map.md"
  - "implementation: `contrast.py`"
---

# Contrast Map

## Definition

A **two-parameter monotonic reshaping** of a $[0,1]$-valued prediction, designed to recover edge sharpness that pointwise losses destroy (see [[Hedging Bias of Pointwise Losses]]):

$$
g(x;\theta,\tau)=\frac{\tanh\!\big((x-\tau)/\theta\big)-\tanh(-\tau/\theta)}{\tanh\!\big((1-\tau)/\theta\big)-\tanh(-\tau/\theta)}
$$

- $\tau$ — the **threshold**: the value the transition is centred on.
- $\theta$ — the **smoothness**: $\theta\to0$ is a hard step at $\tau$; $\theta\to\infty$ recovers the identity. Slope at $\tau$ is $\approx 1/(2\theta)$, so **θ reads directly as a transition width**.

## The affine renormalisation is load-bearing

The naive form $\theta x + 2(1-\theta)\tanh(x/\theta)$ only behaves at $\theta=1$ (where it is the identity). $\tanh(x/\theta)$ is centred at $x=0$, not at $1/2$, so as $\theta\to0$ it becomes a step at 0 **of height 2**:

| θ | f(0) | f(0.5) | f(1) |
|---|---|---|---|
| 1.00 | 0.0000 | 0.5000 | 1.0000 |
| 0.50 | 0.0000 | 1.0116 | 1.4640 |
| 0.05 | 0.0000 | 1.9250 | 1.9500 |

Subtracting the value at 0 and dividing by the span pins $g(0)=0$ and $g(1)=1$ for **every** $(\theta,\tau)$ — which is exactly what lets $\tau$ move off $1/2$ without the prediction leaving $[0,1]$ or the mean level drifting.

Verified: endpoints exact and monotonicity holds across $\theta\in\{0.05,0.2,0.5,2\}\times\tau\in\{0.3,0.5,0.7\}$; $\theta=\texttt{THETA\_MAX}$ reproduces the identity to 6e-4.

## Modes of use

| mode | what is learned | outcome |
|---|---|---|
| post-hoc, global θ | swept, not learned | strictly worse than identity |
| post-hoc, per-sample $(\theta,\tau)$ | oracle-fitted per slice | −6.2%, **unrealizable** (τ unpredictable) |
| end-to-end `global` | two scalars by SGD | no effect; parameters stay at identity |
| end-to-end `head` | small MLP → $(\theta,\tau)$ | collapsed to a constant (zero-init pathology) |

Implementation: `contrast.py` (`apply_contrast`, `ContrastHead`, `ContrastOutput`, `ContrastComposed`), enabled via `CONTRAST_MODE=off|global|head` in `fno_21cm.py`.

## Status

**Closed, negative** — full evidence in [[Contrast Map Sharpening]]. The functional form is sound; the objective simply does not want sharpening. The map's surviving use is as an **explicit, reported post-processing dial**: $\theta\approx0.30$ buys truth-matched sharpness statistics for ~5% RMSE.

## Connections

- Results and verdict: [[Contrast Map Sharpening]]
- The mechanism it failed to defeat: [[Hedging Bias of Pointwise Losses]]
- The target it was aimed at: [[Ionization Morphology]] (near-binary $x_\text{HI}$, sharp bubble walls)
- Contrast with the target-side fix that *does* address displacement: [[Smooth-Target Reparametrization Plan]]
