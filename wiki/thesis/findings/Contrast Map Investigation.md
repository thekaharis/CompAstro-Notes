---
type: finding
title: "Contrast Map Investigation"
created: 2026-07-28
updated: 2026-07-28
tags:
  - domain/thesis
  - domain/ml
  - concept/loss-design
  - concept/sharp-fronts
  - finding/negative
status: closed
related:
  - "[[Hedged Edges vs Blurred Edges]]"
  - "[[Edge and Wall-Placement Losses]]"
  - "[[Structured-Transform Operator Findings]]"
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[Neutral Fraction]]"
  - "[[FNO Lightcone Experimental Findings]]"
sources:
  - "[[.raw/reports/NOTES-contrast-map.md]]"
  - "checkpoints/xhi2d_whno_glob_ctr* (7 runs)"
  - "tests/probe_contrast_from_truth.py, tests/probe_contrast_theta_on_truth.py"
---

# Contrast Map Investigation

> **Status: closed, negative, and explained** — with one narrow surviving regime.
>
> A two-parameter monotonic reshaping $g(x; \theta, \tau)$ of the $[0,1]$-valued prediction was proposed to recover the edge sharpness that pointwise losses destroy. It works as a **deblurrer** (−9.28% on a purely blurred field) and buys **0.00%** on the model at matched sharpness. That contrast is the whole result: the model's edges are not blurred, they are **hedged**, and no pointwise map moves an edge. See [[Hedged Edges vs Blurred Edges]] for the concept this established.

## 1. The map

$$g(x; \theta, \tau) = \frac{\tanh\!\big((x-\tau)/\theta\big) - \tanh(-\tau/\theta)}{\tanh\!\big((1-\tau)/\theta\big) - \tanh(-\tau/\theta)}$$

- $\tau$ — the **threshold**, the value the transition is centred on.
- $\theta$ — the **smoothness**. $\theta \to 0$ is a hard step at $\tau$; $\theta \to \infty$ recovers the identity. Slope at $\tau$ is $\approx 1/(2\theta)$, so $\theta$ reads directly as a transition width.

**The affine renormalisation is load-bearing.** The originally proposed form $\theta x + 2(1-\theta)\tanh(x/\theta)$ only behaves at $\theta = 1$: $\tanh(x/\theta)$ is centred at $x=0$, not $1/2$, so as $\theta \to 0$ it becomes a step at 0 of height 2 (measured: $f(0.5) = 1.925$, $f(1) = 1.950$ at $\theta = 0.05$). Subtracting the value at 0 and dividing by the span pins $g(0)=0$ and $g(1)=1$ for **every** $(\theta,\tau)$ — which is what lets $\tau$ move off $1/2$ without the prediction leaving $[0,1]$ or the mean level drifting.

![[contrast_map_examples.png]]

## 2. Post-hoc: an oracle gain that cannot be realized

All on the trained `whno_glob` 2-D leader. *(Tables report pixel RMSE on held-out slices, a different quantity from the trainer's `val_l2`, and slice sets differ between subsections — compare within a table, never across.)*

**A global $(\theta,\tau)$ is worthless.** Sweeping one shared $\theta$, RMSE degrades monotonically; no value beats the identity ($\theta = 0.40$: +2.3%; $\theta = 0.20$: +10.6%). This *had* to come out this way — the model already ends in a sigmoid, so it can represent any monotone remap of its own logits. **Post-hoc pointwise sharpening can never improve L² for a converged model.**

**Per-sample $(\theta,\tau)$ has real headroom — and needs both.** Cross-validated across pixels (fit on a random half of each slice, score on the other):

| variant | RMSE | gain |
|---|---|---|
| identity | 0.15328 | — |
| per-slice $\theta$ only ($\tau = 0.5$) | 0.15267 | −0.40% |
| per-slice $\tau$ only ($\theta$ = global best) | 0.15277 | −0.33% |
| **per-slice both** | **0.14382** | **−6.17%** |

Strongly **superadditive** — ~8× the sum of the parts. The beneficial operation is *a sharp map placed at a per-slice-specific threshold*: with $\tau$ pinned at $1/2$ you only steepen in the wrong place; with $\theta$ near identity a near-linear map barely notices its pivot.

**But $\tau$ is not predictable at inference.** $R^2$ for predicting the fitted parameters (held-out 30%, linear / small MLP):

| features | $\theta$ | $\tau$ |
|---|---|---|
| pooled prediction stats (6) | 0.26 / 0.28 | 0.01 / −0.06 |
| + value histogram (16) | 0.27 / 0.10 | −0.01 / −0.31 |
| + conditioning ($z$, 11 params) | 0.35 / −0.58 | **−0.01 / −1.10** |

Not the prediction, not its histogram, not even redshift and the cosmological parameters. Since the gain needs both jointly and is superadditive, a head with poor $\tau$ accuracy gets no partial credit — it applies sharp maps at wrong thresholds, the actively harmful regime. **The 6.2% is an oracle ceiling, not an achievable target.**

## 3. End-to-end: the network declined the map

`CONTRAST_MODE=off|global|head`, initialised at the identity, gradients verified to reach the contrast parameters *and* all 84 base tensors. 30 epochs, pure L², against the matched baseline.

| run | contrast | val L² | test L² | vs baseline |
|---|---|---|---|---|
| `whno_glob_lr3e4` | none | **0.1060** | **0.1107** | — |
| `whno_glob_ctrglobal` | global | 0.1062 | 0.1112 | +0.2% / +0.5% |
| `whno_glob_ctrhead` | head | 0.1055 | 0.1117 | −0.5% / +0.9% |
| `whno_glob_ctrglobal_hk` | global + highK | NaN at ~ep 6–10 | — | crashed |

Val and test disagree in sign; the spread is tenths of a percent. **No effect.** But the decisive number is not the RMSE — it is the learned parameters:

| run | learned $\theta$ | learned $\tau$ | max $|g(x)-x|$ |
|---|---|---|---|
| initialisation | 4.750 | 0.500 | 0.0007 |
| `ctrglobal` | 4.431 | 0.5044 | **0.0009** |
| *(for scale)* sharpness-matched | 0.30 | 0.5 | 0.117 |

$\theta$ was free to move anywhere in $[0.02, 5.0]$ and moved from 4.75 to 4.43 — i.e. **nowhere**. The learned map differs from the identity by at most $9\times10^{-4}$, ~130× less than the setting that matches truth sharpness. **Given a differentiable sharpening dial and 30 epochs, gradient descent left it at zero.**

This also settles the pre-registered "band-limited" argument for the approach (a pointwise nonlinearity after spectral synthesis creates high-frequency content the operator cannot represent — genuine added expressiveness). **That argument does not hold in practice**: whatever extra high-$k$ content the map could create, L² does not want it.

### Two methodological gotchas worth remembering

- **The `head` run did not test what it was meant to.** Its input-layer weights decayed to ~5e-28, so `net.0` outputs zero regardless of input and the MLP degenerates to a bias chain — probing with random, binarised, all-0.1 and all-0.9 fields returns the identical $(\theta, \tau) = (4.441, 0.5051)$. Cause: the identity initialisation `nn.init.zeros_(net[-1].weight)` is the standard trick for starting at the identity, but here it zeros the **only** backward path to the earlier layers; layer 0's gradient scales as $W_2 W_4$, so with $W_4 = 0$ the early layers get no gradient while weight decay keeps acting. A collapse cascade. **Fix: nonzero (small) last-layer init, or no weight decay on the head.**
- **highK + contrast is unstable.** Healthy at epoch 5 (best highK value of any run), `avg_loss=nan` by epoch 10. Plausible mechanism: highK's $\log(P_\text{pred}/P_\text{true})$ gradient grows without bound as predicted band power falls, and $\partial g/\partial\theta \sim 1/\theta^2$ — the two drive each other. The reported CUDA assert location is a red herring (errors surface at the next synchronisation point).

## 4. Deriving the parameters from the truth — why the useful $\tau$ is unphysical

Instead of fitting by minimising RMSE, read $(\theta,\tau)$ off the truth's edge geometry: $\tau_\text{geom}$ = median prediction value *at the true boundary*, $\theta_\text{geom}$ = the $\theta$ matching the prediction's transition width to the truth's. 512 held-out slices:

| variant | RMSE | vs identity |
|---|---|---|
| identity | 0.15263 | — |
| per-slice **geometric** | 0.18853 | **+23.52%** |
| per-slice **blind** fit (RMSE oracle) | 0.14511 | −4.93% |
| blind $\theta$ + geometric $\tau$ | 0.15390 | +0.83% |
| geometric $\theta$ + blind $\tau$ | 0.18278 | +19.75% |

$\tau_\text{geom}$ **is** predictable from what the model sees (corr with mean prediction +0.475). But it yields no gain, and the split shows why: geometric $\tau$ is nearly harmless (+0.83%); geometric $\theta$ is what destroys it. Decisively, corr($\tau_\text{geom}$, $\tau_\text{blind}$) = only **+0.309**.

> [!key-insight]
> **The $\tau$ carrying the gain is not the edge-location threshold.** It is a per-slice bias/calibration nuisance — which a converged model leaves unpredictable almost by definition: any bias inferable from the input would already have been removed. *The physical threshold is predictable and useless; the useful one is unpredictable and unphysical.* This closes the §2 open question rather than reopening it.

## 5. The one regime where it works: $\theta$ resolved against $\bar{x}_\text{HI}$

The pooled sweeps hide a real effect. $\theta$ was expected to depend on ionization state — early on a few small bubbles in a neutral sea, late on a few neutral islands in an ionized sea. Resolving it needed more statistics than the training cache holds (its sampler down-weights the tails ~50×), so `dataset/build_xhi_band.py` builds a band-saturating cache from **val + test cones only**: 6292 slices, 566 cones, ~700–1100 per 0.05 bin against 34–68 before.

$\theta$ fitted per bin on one set of cones, scored on disjoint cones, CI from a cone-level bootstrap. `edge_t` is truth edge density — the control saying whether a bin contains any boundaries to sharpen.

| $\bar{x}_\text{HI}$ | n | edge_t | $\theta_\text{pred}$ | identity | +$\theta$ | gain | 95% CI |
|---|---|---|---|---|---|---|---|
| *0.000–0.005* | *497* | *0.0001* | *0.161* | *0.06017* | *0.05247* | *−12.79%* | *[−26.4, −4.7]* |
| **0.005–0.010** | 60 | 0.0038 | 0.289 | 0.13323 | 0.12103 | **−9.16%** | [−15.7, −4.4] |
| **0.010–0.020** | 117 | 0.0076 | 0.311 | 0.13361 | 0.12321 | **−7.78%** | [−11.6, −4.7] |
| **0.020–0.030** | 133 | 0.0108 | 0.482 | 0.18623 | 0.18246 | **−2.02%** | [−3.3, −0.9] |
| **0.030–0.050** | 263 | 0.0162 | 0.482 | 0.17660 | 0.17293 | **−2.08%** | [−3.3, −1.1] |
| 0.050–0.100 | 785 | 0.0279 | 0.804 | 0.21602 | 0.21565 | −0.17% | [−0.32, −0.02] |
| 0.100–0.200 | 1612 | 0.0501 | 5.000 | 0.25824 | 0.25825 | +0.00% | [+0.00, +0.01] |
| 0.200–0.360 | 2189 | 0.0856 | 5.000 | 0.28232 | 0.28235 | +0.01% | [+0.01, +0.01] |

**Genuine, realizable, and narrow.** At $\bar{x}_\text{HI} \approx 0.005$–$0.05$ the held-out gain is 2–9% with every CI clear of zero, and $\theta$ there depends only on $\bar{x}_\text{HI}$, which the model estimates from its own mean output — so unlike $\tau$, it *is* available at inference.

- The **first row is excluded from every headline**: at `edge_t = 0.0001` the truth has essentially no boundaries, the model emits faint spurious structure, and a small $\theta$ squashes it. That is thresholding noise off a blank field, the same artefact as the $\bar{x}_\text{HI} = 1.000$ bin's −42% at the opposite end. **Any bin whose gain is not accompanied by real `edge_t` should be read this way.**
- $\theta_\text{pred}$ rises monotonically with $\bar{x}_\text{HI}$ — sharp → blurred, the predicted direction. Spearman = **+0.448** over 0–0.36 and **+0.721** over 0–0.10. Over the full test set it was **+0.003**: decile binning averaged it away entirely.
- **Size of the prize:** pooled over 0.005–0.36 the gain is only **−0.16%**, and it is confined to $\bar{x}_\text{HI} < 0.05$. A targeted correction for very-late-reionization maps, not a general improvement.

Why here and nowhere else: at $\bar{x}_\text{HI} \sim 0.01$ the field is a handful of isolated neutral islands the model renders as low-contrast blobs — **correctly located, just under-committed**, exactly the defect a pointwise map fixes. By $\bar{x}_\text{HI} > 0.1$ the field is a dense bubble network where the errors are *positional*, and sharpening does nothing at all (+0.00%, CI width 0.01%, ~1900 held-out slices).

### End-to-end schedule runs

A per-$\bar{x}_\text{HI}$-bin $\theta$ schedule was then trained in the loop (`CONTRAST_MODE=xhi`, alternating per-epoch refit, minibatched, floored, gradient-clipped, refit under the run's own loss rather than hardcoded MSE, drawing from a band-enriched train-only slice pool). On the shared-slice leaderboard the scheduled variants land at 0.1452–0.1455 RMSE against the baseline's 0.1448 — i.e. **the in-loop schedule reproduces the baseline and does not add to it**, consistent with the pooled −0.16%. Logged `contrast_train_gain_pct` hovers at −0.2 to −0.4% on the L² runs.

## 6. Verdict

The map is **not useless — it has one real regime** ($\bar{x}_\text{HI} \approx 0.005$–$0.05$, held-out 2–9%, realizable). Everywhere else the original verdict stands: a working deblurrer that buys 0.00% on the model at matched sharpness, because the model's edges are hedged, not blurred.

It remains usable as an **explicit, reported post-processing dial** — $\theta \approx 0.30$ lands the sharpness statistics on truth (blur 0.1112 vs truth 0.1073) for ~5% RMSE. **That is a presentation choice, not a better model, and must be reported as post-processing.**

Incidental but physical: driving $\theta \to 0.02$ hard-binarises even the *truth* and costs 0.0879 RMSE. The partial ionization in the transition band is real information worth ~58% of the model's entire error — **binarising is not free**.

## 7. Where the effort should go instead

Section 4–5 point one way: the loss must penalise **misplaced** edges, not reward **steep** ones. Sharpening is measurably the wrong tool — it fixes blur, and ~86% of the error is not blur. That is the brief taken up in [[Edge and Wall-Placement Losses]].

Still open: whether any of this transfers to 3-D, where the front-width defect is worse (~3.5× vs ~2–4× in 2-D).
