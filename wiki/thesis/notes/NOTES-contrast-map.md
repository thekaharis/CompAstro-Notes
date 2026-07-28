# The (theta, tau) contrast map

A two-parameter monotonic reshaping of a `[0, 1]`-valued prediction, intended
to recover the edge sharpness that pointwise losses systematically destroy.

Status as of 2026-07-27: **closed, negative.** The post-hoc form has a real but
unrealizable 6.2% ceiling; the end-to-end form has now run, and gradient
descent declined to use the map at all (section 4).

---

## 1. Motivation: why pointwise losses blur

If the model is uncertain whether an edge sits at `x0` or `x0 +- delta`, the
L2-optimal prediction is the expectation over that uncertainty -- a ramp of
width `~2*delta`. A sharp edge in the wrong place costs roughly twice the area
of a soft ramp that hedges, so **L2 actively rewards blurring**.

H1 has the same pathology one derivative up: the L2-optimal *gradient* field is
`E[grad]`, which turns a tall narrow ridge into a low wide bump. This explains a
long-standing puzzle in the 3-D runs -- fronts came out 12-14 Mpc against a
3.6 Mpc truth *despite* the loss being 99.4% H1 by contribution.

Measured on the 2-D x_HI task (256 held-out slices, `whno_glob`), truth
transitions are ~0.9 px wide and predictions ~1.7-3.4 px, i.e. ~2-4x too wide.
The local branch (6 modes in a 16 px window) can represent ~1.3-2.7 px
transitions, so the models leave representable sharpness unused: the binding
constraint is the objective, not the bandwidth.

## 2. The map

```
g(x; theta, tau) = [tanh((x - tau)/theta) - tanh(-tau/theta)]
                   / [tanh((1 - tau)/theta) - tanh(-tau/theta)]
```

* `tau` -- the **threshold**, the value the transition is centred on.
* `theta` -- the **smoothness**. `theta -> 0` is a hard step at `tau`;
  `theta -> inf` recovers the identity. Slope at `tau` is `~1/(2*theta)`, so
  `theta` reads directly as a transition width.

**The affine renormalisation is load-bearing.** The originally proposed form,
`theta*x + 2*(1-theta)*tanh(x/theta)`, only behaves at `theta = 1` (where it is
the identity): `tanh(x/theta)` is centred at `x = 0`, not at `1/2`, so as
`theta -> 0` it becomes a step at 0 of height 2. Measured values:

| theta | f(0) | f(0.5) | f(1) |
| --- | --- | --- | --- |
| 1.00 | 0.0000 | 0.5000 | 1.0000 |
| 0.50 | 0.0000 | 1.0116 | 1.4640 |
| 0.05 | 0.0000 | 1.9250 | 1.9500 |

Subtracting the value at 0 and dividing by the span pins `g(0) = 0` and
`g(1) = 1` for **every** `(theta, tau)`, which is what allows `tau` to move off
`1/2` without the prediction leaving `[0, 1]` or the mean level drifting.
Verified: endpoints exact and monotonicity holds across
`theta in {0.05, 0.2, 0.5, 2}` x `tau in {0.3, 0.5, 0.7}`; `theta = THETA_MAX`
reproduces the identity to `6e-4`.

Implementation: `contrast.py` (`apply_contrast`, `ContrastHead`,
`ContrastOutput`, `ContrastComposed`).

## 3. Post-hoc results (closed)

All on the trained `whno_glob` (`xhi2d_whno_glob_lr3e4`, the 2-D x_HI leader:
val L2 0.1060 / test L2 0.1107 at epoch 25). Note the tables below report
**pixel RMSE** on held-out slices, which is a different quantity from the
trainer's `val_l2`, and the slice sets differ between subsections -- compare
within a table, never across.

### 3.1 A global (theta, tau) is worthless

Sweeping a single `theta` shared by all slices, RMSE degrades monotonically;
no value beats the identity.

| theta | RMSE | vs identity | blur_frac | width_px |
| --- | --- | --- | --- | --- |
| TRUTH | -- | -- | 0.1073 | 1.505 |
| identity | **0.14866** | -- | 0.2125 | 3.433 |
| 0.40 | 0.15213 | +2.3% | 0.1385 | 2.260 |
| 0.30 | 0.15595 | +4.9% | 0.1112 | 1.822 |
| 0.20 | 0.16449 | +10.6% | 0.0755 | 1.242 |

This *had* to come out this way: the model already ends in a sigmoid, so it can
represent any monotonic remap of its own logits. If some `g_theta` improved L2,
training would have found it. **Post-hoc pointwise sharpening can never improve
L2 for a converged model** -- a general result, not specific to this
architecture.

The map is still usable as an explicit tradeoff dial: `theta ~ 0.30` lands the
sharpness statistics on truth (blur 0.1112 vs 0.1073) for ~5% RMSE. Legitimate
if the deliverable is summary statistics rather than per-pixel accuracy, but it
must be reported as post-processing, not as a better model.

### 3.2 Per-sample (theta, tau) has real headroom -- and needs both

Fitting parameters per slice, **cross-validated across pixels** (fit on a random
half of each slice, score on the other half, so this is not selection bias):

| variant | RMSE | gain |
| --- | --- | --- |
| identity | 0.15328 | -- |
| per-slice `theta` only (`tau` = 0.5) | 0.15267 | -0.40% |
| per-slice `tau` only (`theta` = global best) | 0.15277 | -0.33% |
| **per-slice both** | **0.14382** | **-6.17%** |

Strongly **superadditive**: ~8x the sum of the parts. The beneficial operation
is *a sharp map placed at a per-slice-specific threshold* -- with `tau` pinned
at 1/2 you can only steepen in the wrong place, and with `theta` near-identity
a near-linear map barely notices its pivot. Fitted values spread widely
(`theta` 0.28-3.21, `tau` 0.10-0.90 at 10-90%), confirming genuine
per-sample heterogeneity.

Held-out (-5.33%) matched or beat in-sample (-5.03%) on a separate 600-slice
run, so selection bias is negligible.

### 3.3 ...but it cannot be realized at inference

R^2 for predicting the fitted parameters, held-out 30%, linear and small MLP:

| features | theta | tau |
| --- | --- | --- |
| pooled prediction stats (6) | 0.26 / 0.28 | 0.01 / -0.06 |
| + value histogram (16) | 0.27 / 0.10 | -0.01 / -0.31 |
| + conditioning (z, 11 params) | 0.35 / -0.58 | **-0.01 / -1.10** |

`theta` is moderately predictable; **`tau` is not predictable from anything
available at inference** -- not the prediction, not its histogram, not even
redshift and the cosmological parameters. Since the gain needs both jointly,
the 6.2% is an **oracle ceiling, not an achievable target**.

A trained `ContrastHead` confirmed this empirically: test RMSE 0.13782 vs
0.13774 identity (+0.05%, i.e. slightly *worse*), with training loss *rising*
0.0171 -> 0.0203 and `tau` pinned at its upper bound. Because the gain is
superadditive, a head with poor `tau` accuracy does not get partial credit --
it applies sharp maps at wrong thresholds, which is the actively harmful
regime.

**Conclusion for the post-hoc route: closed.** Report 6.2% as a measured upper
bound on per-sample output correction, and note the limitation is *information*,
not the functional form.

## 4. End-to-end (done -- negative)

The rationale, stated before the runs, was that this is distinct from the above
and not refuted by it:

* With a **global** learned `(theta, tau)` there is no prediction problem --
  two scalars trained by gradient descent.
* The network can **co-adapt**, shaping its pre-map output to suit the map
  rather than having a finished prediction reshaped afterwards.
* The spectral operators synthesise a **band-limited** field; a pointwise
  nonlinearity applied *after* synthesis creates high-frequency content the
  operator cannot represent. This is genuine added expressiveness relative to
  the linear operator plus a fixed mild sigmoid.

Enabled with `CONTRAST_MODE=off|global|head` in `fno_21cm.py`; initialised at
the identity so a run starts from exactly the baseline. Verified that gradients
reach the contrast parameters *and* all 84 base tensors.

### 4.1 Results

All `whno_glob`, 30 epochs, pure L2, against the **matched** no-contrast pure-L2
baseline `xhi2d_whno_glob_lr3e4`. (Metrics are logged every 5 epochs, so all
figures are epoch 25.)

| job | run | contrast | val L2 | test L2 | vs baseline |
| --- | --- | --- | --- | --- | --- |
| -- | `whno_glob_lr3e4` | none | **0.1060** | **0.1107** | -- |
| 4358634 | `whno_glob_ctrglobal` | global | 0.1062 | 0.1112 | +0.2% / +0.5% |
| 4358635 | `whno_glob_ctrhead` | head | 0.1055 | 0.1117 | -0.5% / +0.9% |
| 4358636 | `whno_glob_ctrglobal_hk` | global + highK | NaN at ~ep 6-10 | -- | crashed |

Val and test disagree in sign for both variants and the spread is a few tenths
of a percent. **No effect.**

### 4.2 The network chose not to use the map

The decisive number is not the RMSE, it is the learned parameters:

| run | learned theta | learned tau | max abs g(x) - x |
| --- | --- | --- | --- |
| initialisation | 4.750 | 0.500 | 0.0007 |
| `ctrglobal` | 4.431 | 0.5044 | **0.0009** |
| `ctrhead` (see 4.3) | 4.441 | 0.5051 | **0.0009** |
| *(for scale)* sharpness-matched | 0.30 | 0.5 | 0.117 |

`theta` was free to move anywhere in `[0.02, 5.0]` and the gradient was verified
to reach it. It moved from 4.75 to 4.43 -- i.e. **nowhere**. The learned map
differs from the identity by at most 9e-4, ~130x less than the setting that
matches truth sharpness. Given a differentiable sharpening dial and 30 epochs,
gradient descent left it at zero.

This is the prediction in the pre-registered version of this note coming true,
and it settles the band-limited argument in section 4's rationale: **that
argument does not hold in practice.** Whatever extra high-k content the
post-synthesis nonlinearity could create, L2 does not want it -- consistent with
section 1 (L2 rewards hedging) and section 3.1 (the model's own sigmoid already
spans these remaps). The map is not a way around the objective; the objective
was always the thing selecting against sharpness.

### 4.3 The `head` run did not test what it was meant to

Caveat, found on inspection of the trained weights: the head **collapsed to a
constant**. Its input-layer weights decayed to ~5e-28 (from ~0.4 at init), so
`net.0` outputs zero regardless of input and the whole MLP degenerates to a bias
chain. Probing it with random, binarised, all-0.1 and all-0.9 fields returns
identical `(theta, tau) = (4.441, 0.5051)` in every case -- the same point the
*global* run reached independently, to three decimals.

The cause is the identity initialisation: `nn.init.zeros_(self.net[-1].weight)`
is the standard trick for starting a module at the identity, but here it zeros
the **only** backward path to the earlier layers. Layer 0's gradient scales as
`W2 * W4`, layer 2's as `W4`, so with `W4` starting at zero the early layers get
essentially no gradient while weight decay keeps acting -- a collapse cascade,
visible in the final magnitudes (`W0` 5e-28 < `W2` 1e-27 << `W4` 5e-2).

So the head run is **not** independent evidence about input-dependent contrast;
it is a second, slower measurement of the global case. It is consistent with
section 3.3 but does not confirm it. Rerunning would need a nonzero (small)
last-layer init, or no weight decay on the head. Given 4.2 -- the global map,
which had no such handicap, also went nowhere -- this is not worth the GPU time
unless the whole approach is revisited under a different loss.

### 4.4 The highK combination is unstable

`ctrglobal_hk` (L2 + 0.12*highK, warmup 5) was healthy at epoch 5
(val_l2 0.1219, val_highk 0.0825 -- the best highK value of any run) and
`avg_loss=nan` by epoch 10; it then died in eval with a CUDA device-side assert
inside `HighKPowerRatio._binned_power`. The saved epoch-9 checkpoint is entirely
finite, so the blowup is after it.

Not isolated. Note that highK alone and contrast alone each trained to epoch 29
without incident, so it is the combination. Plausible mechanism: highK's
`log(P_pred/P_true)` gradient grows without bound as predicted band power falls,
and `d g/d theta ~ 1/theta^2`, so the two can drive each other. The reported
assert location is a red herring -- CUDA errors surface at the next
synchronisation point, and `index[keep]` indexes a validated cached tensor.

## 5. Verdict and open items

**Verdict.** Both routes are closed. Post-hoc: a genuine 6.2% oracle gain that
cannot be realised because `tau` is not predictable from anything available at
inference (3.3). End-to-end: the network declines the map when free to use it
(4.2). The functional form is fine; sharpening the output is simply not what a
pointwise loss wants, and adding a knob for it does not change that.

The map remains useful as an **explicit, reported post-processing dial**
(`theta ~ 0.30` buys truth-matched sharpness statistics for ~5% RMSE, section
3.1) -- but that is a presentation choice, not a better model.

Open:

* Sharpness table for the finished edge-loss runs at matched epoch 29. Ranking
  on L2 at epoch 25: baseline 0.1060 < swd 0.1072 < highk 0.1083 < swd+highk
  0.1089; `edgeonly` (no L2) failed outright at **0.9098**, never beating its
  epoch-0 value -- neither SWD nor highK constrains absolute level or position,
  so an L2 anchor is not optional. All edge variants cost L2, so their case
  rests entirely on sharpness, which is not yet measured at the final epoch.
* Whether any of this transfers to 3-D, where the front-width defect is worse
  (~3.5x vs ~2-4x here).
* If sharpness is still wanted in-loss, the live lead is that the loss must
  penalise *misplaced* edges rather than reward *steep* ones -- i.e. the
  transport-based direction (SWD), not a pointwise reshaping. It is the only
  edge term here that cost less than 1.2% L2.
