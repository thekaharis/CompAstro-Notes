---
type: finding
title: "Contrast Map Sharpening"
created: 2026-07-27
updated: 2026-07-27
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - concept/loss-design
  - concept/boundary-sharpness
  - architecture/whno
  - finding/negative
  - finding/closed
status: closed
verdict: negative
related:
  - "[[Contrast Map]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[Loss Objective and Operator Basis Sweep]]"
  - "[[Walsh-Hadamard Neural Operator]]"
  - "[[Windowed Local-FNO U-Net Findings]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[Ionization Morphology]]"
  - "[[Inference and ML]]"
sources:
  - "wiki/thesis/notes/NOTES-contrast-map.md"
  - "implementation: `contrast.py` (`apply_contrast`, `ContrastHead`, `ContrastOutput`, `ContrastComposed`); `CONTRAST_MODE=off|global|head` in `fno_21cm.py`"
  - "runs: jobs 4358634 / 4358635 / 4358636, all `whno_glob`, 30 epochs, pure L2"
---

# Contrast Map Sharpening

**Status as of 2026-07-27: closed, negative.** Both routes are dead. The post-hoc form has a real but **unrealizable** 6.2% ceiling; the end-to-end form ran, and gradient descent **declined to use the map at all**.

The object under test is the two-parameter monotonic reshaping defined in [[Contrast Map]]; this page records what it bought (nothing) and, more usefully, *why*.

## Why it was tried

Fronts come out 12–14 Mpc against a 3.6 Mpc truth in 3-D, and 1.7–3.4 px against ~0.9 px truth on the 2-D $x_\text{HI}$ task (256 held-out slices, `whno_glob`) — i.e. **2–4× too wide**. The local branch (6 modes in a 16 px window) can represent ~1.3–2.7 px transitions, so **the models leave representable sharpness unused**: the binding constraint is the objective, not the bandwidth. See [[Hedging Bias of Pointwise Losses]] for the mechanism, including why the H¹-dominated 3-D loss did not prevent this.

## 1. Post-hoc route — closed

All on the trained `whno_glob` (`xhi2d_whno_glob_lr3e4`, the 2-D $x_\text{HI}$ leader: val L² 0.1060 / test L² 0.1107 at epoch 25).

> **Metric warning.** The tables below report **pixel RMSE** on held-out slices — a different quantity from the trainer's `val_l2` — and the slice sets differ between subsections. **Compare within a table, never across.**

### 1.1 A global $(\theta,\tau)$ is worthless

| θ | RMSE | vs identity | blur_frac | width_px |
|---|---|---|---|---|
| TRUTH | – | – | 0.1073 | 1.505 |
| identity | **0.14866** | – | 0.2125 | 3.433 |
| 0.40 | 0.15213 | +2.3% | 0.1385 | 2.260 |
| 0.30 | 0.15595 | +4.9% | 0.1112 | 1.822 |
| 0.20 | 0.16449 | +10.6% | 0.0755 | 1.242 |

This **had** to come out this way, and the argument is general: the model already ends in a sigmoid, so it can represent any monotonic remap of its own logits. If some $g_\theta$ improved L², training would already have found it. → **Post-hoc pointwise sharpening can never improve L² for a converged model.** Not architecture-specific.

The map survives as an explicit **tradeoff dial**: θ ≈ 0.30 lands sharpness statistics on truth (blur 0.1112 vs 0.1073) for ~5% RMSE. Legitimate if the deliverable is summary statistics — but **must be reported as post-processing, not as a better model**.

### 1.2 Per-sample $(\theta,\tau)$ has real headroom — and needs both

Fitted per slice, **cross-validated across pixels** (fit on a random half of each slice, score on the other half — so not selection bias):

| variant | RMSE | gain |
|---|---|---|
| identity | 0.15328 | – |
| per-slice θ only (τ = 0.5) | 0.15267 | −0.40% |
| per-slice τ only (θ = global best) | 0.15277 | −0.33% |
| **per-slice both** | **0.14382** | **−6.17%** |

Strongly **superadditive — ~8× the sum of the parts**. The beneficial operation is *a sharp map placed at a per-slice-specific threshold*: with τ pinned at 1/2 you can only steepen in the wrong place, and with θ near-identity a near-linear map barely notices its pivot. Fitted values spread widely (θ 0.28–3.21, τ 0.10–0.90 at 10–90%) — genuine per-sample heterogeneity. Held-out (−5.33%) matched or beat in-sample (−5.03%) on a separate 600-slice run.

### 1.3 …but it cannot be realized at inference

$R^2$ for predicting the fitted parameters, held-out 30%, linear / small MLP:

| features | θ | τ |
|---|---|---|
| pooled prediction stats (6) | 0.26 / 0.28 | 0.01 / −0.06 |
| + value histogram (16) | 0.27 / 0.10 | −0.01 / −0.31 |
| + conditioning (z, 11 params) | 0.35 / −0.58 | **−0.01 / −1.10** |

θ is moderately predictable; **τ is not predictable from anything available at inference** — not the prediction, not its histogram, not even redshift and the cosmological parameters. Since the gain needs both jointly, **the 6.2% is an oracle ceiling, not an achievable target**.

Confirmed empirically by a trained `ContrastHead`: test RMSE 0.13782 vs 0.13774 identity (+0.05%, slightly *worse*), training loss **rising** 0.0171 → 0.0203, τ pinned at its upper bound. Because the gain is superadditive, a head with poor τ accuracy gets **no partial credit** — it applies sharp maps at wrong thresholds, which is the actively harmful regime.

**Verdict:** report 6.2% as a measured upper bound on per-sample output correction, and note the limitation is **information, not functional form**.

## 2. End-to-end route — done, negative

The pre-registered rationale (stated before the runs, and distinct from §1):

- With a **global** learned $(\theta,\tau)$ there is no prediction problem — two scalars trained by gradient descent.
- The network can **co-adapt**, shaping its pre-map output to suit the map rather than having a finished prediction reshaped afterwards.
- The spectral operators synthesise a **band-limited** field; a pointwise nonlinearity applied *after* synthesis creates high-frequency content the operator cannot represent — genuine added expressiveness.

Initialised at the identity, so a run starts from exactly the baseline; gradients verified to reach the contrast parameters *and* all 84 base tensors.

### 2.1 Results — no effect

All `whno_glob`, 30 epochs, pure L², against the **matched** no-contrast baseline. (Metrics logged every 5 epochs → all figures are epoch 25.)

| job | run | contrast | val L² | test L² | vs baseline |
|---|---|---|---|---|---|
| – | `whno_glob_lr3e4` | none | **0.1060** | **0.1107** | – |
| 4358634 | `whno_glob_ctrglobal` | global | 0.1062 | 0.1112 | +0.2% / +0.5% |
| 4358635 | `whno_glob_ctrhead` | head | 0.1055 | 0.1117 | −0.5% / +0.9% |
| 4358636 | `whno_glob_ctrglobal_hk` | global + highK | NaN at ~ep 6–10 | – | crashed |

Val and test disagree in sign for both variants; the spread is a few tenths of a percent.

### 2.2 The decisive number is the learned parameters, not the RMSE

| run | learned θ | learned τ | max abs g(x) − x |
|---|---|---|---|
| initialisation | 4.750 | 0.500 | 0.0007 |
| `ctrglobal` | 4.431 | 0.5044 | **0.0009** |
| `ctrhead` (see §2.3) | 4.441 | 0.5051 | **0.0009** |
| *(for scale)* sharpness-matched | 0.30 | 0.5 | 0.117 |

θ was free anywhere in [0.02, 5.0] and the gradient was verified to reach it. It moved from 4.75 to 4.43 — **nowhere**. The learned map differs from the identity by at most 9e-4, **~130× less** than the setting that matches truth sharpness. **Given a differentiable sharpening dial and 30 epochs, gradient descent left it at zero.**

This settles the band-limited argument in the §2 rationale: **that argument does not hold in practice.** Whatever extra high-k content the post-synthesis nonlinearity could create, **L² does not want it** — consistent with the hedging mechanism and with §1.1 (the model's own sigmoid already spans these remaps). The map is not a way around the objective; **the objective was always the thing selecting against sharpness.**

### 2.3 Caveat: the `head` run did not test what it was meant to

Found on inspection of the trained weights: the head **collapsed to a constant**. Input-layer weights decayed to ~5e-28 (from ~0.4 at init), so `net.0` outputs zero regardless of input and the MLP degenerates to a bias chain. Probing with random, binarised, all-0.1 and all-0.9 fields returns identical $(\theta,\tau) = (4.441, 0.5051)$ — the same point the *global* run reached independently, to three decimals.

**Cause: the identity initialisation.** `nn.init.zeros_(self.net[-1].weight)` is the standard trick for starting a module at the identity, but here it zeros the **only** backward path to the earlier layers. Layer 0's gradient scales as $W_2 W_4$, layer 2's as $W_4$; with $W_4$ starting at zero the early layers get essentially no gradient while weight decay keeps acting — a collapse cascade, visible in the final magnitudes ($W_0$ 5e-28 < $W_2$ 1e-27 ≪ $W_4$ 5e-2).

So the head run is **not independent evidence** about input-dependent contrast; it is a second, slower measurement of the global case. Consistent with §1.3 but does not confirm it. A rerun needs a nonzero (small) last-layer init, or no weight decay on the head — **not worth the GPU time** given that the global map, which had no such handicap, also went nowhere.

> **Reusable lesson:** zero-init of the last layer for identity initialisation is unsafe whenever that layer is the sole gradient path to earlier layers. Pair it with a small nonzero init or disable weight decay on the module.

### 2.4 The highK combination is unstable

`ctrglobal_hk` (L² + 0.12·highK, warmup 5) was healthy at epoch 5 (val_l2 0.1219, val_highk 0.0825 — **the best highK value of any run**) and `avg_loss=nan` by epoch 10, then died in eval with a CUDA device-side assert inside `HighKPowerRatio._binned_power`. The epoch-9 checkpoint is entirely finite, so the blowup is after it.

Not isolated: highK alone and contrast alone each trained to epoch 29 without incident — **it is the combination.** Plausible mechanism: highK's $\log(P_\text{pred}/P_\text{true})$ gradient grows without bound as predicted band power falls, and $\partial g/\partial\theta \sim 1/\theta^2$, so the two drive each other. The reported assert location is a **red herring** — CUDA errors surface at the next synchronisation point, and `index[keep]` indexes a validated cached tensor.

## 3. Verdict and what survives

**Both routes closed.** Post-hoc: a genuine 6.2% oracle gain that cannot be realised because τ is unpredictable at inference (§1.3). End-to-end: the network declines the map when free to use it (§2.2). The functional form is fine — **sharpening the output is simply not what a pointwise loss wants, and adding a knob for it does not change that.**

What survives: the map as an **explicit, reported post-processing dial** (θ ≈ 0.30 buys truth-matched sharpness statistics for ~5% RMSE, §1.1). That is a presentation choice, not a better model.

## 4. Open items

- **Sharpness table for the finished edge-loss runs at matched epoch 29.** Ranking on L² at epoch 25: baseline 0.1060 < swd 0.1072 < highk 0.1083 < swd+highk 0.1089. `edgeonly` (no L²) **failed outright at 0.9098**, never beating its epoch-0 value — neither SWD nor highK constrains absolute level or position, so **an L² anchor is not optional**. All edge variants cost L², so their case rests entirely on sharpness, not yet measured at the final epoch.
- Whether any of this **transfers to 3-D**, where the front-width defect is worse (~3.5× vs ~2–4× here).
- **The live lead:** if sharpness is wanted in-loss, the loss must penalise **misplaced** edges rather than reward **steep** ones — i.e. the **transport-based direction (SWD)**, the only edge term here that cost less than 1.2% L². This is the natural sibling of the target-side [[Smooth-Target Reparametrization Plan]], which converts front *blurring* into front *displacement* by construction.
