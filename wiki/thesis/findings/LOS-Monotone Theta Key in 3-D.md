---
type: finding
title: "LOS-Monotone Theta Key in 3-D"
created: 2026-08-06
updated: 2026-08-07
tags:
  - domain/thesis
  - domain/ml
  - domain/reionization
  - concept/loss-design
  - concept/boundary-sharpness
  - architecture/ufno
  - architecture/whno
  - finding/negative
  - finding/open
status: open
verdict: negative-so-far
related:
  - "[[Contrast Map]]"
  - "[[Contrast Map Sharpening]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[U-FNO BatchNorm Train-Eval Mismatch]]"
sources:
  - "wiki/thesis/notes/NOTES-contrast-map.md §8 (pre-registration)"
  - "runs 4457033 (fno_whno), 4457034 (ufno, groupnorm)"
  - "implementation: `contrast.py:118` `los_key`, `util/contrast_refit.py`"
  - "diagnostic: `viz/theta_z_profile.py` (added 2026-08-07)"
---

# LOS-Monotone Theta Key in 3-D

## The pre-registration

`NOTES-contrast-map.md` §8.1 registered the prediction in advance: the 2-D
contrast-map gain pooled to -0.16% because the **key** (per-slice mean
prediction, MAE ~0.055) is noisier than the **band** it must resolve (x_HI
0.005-0.05, width 0.045). A lightcone's 256 per-slice means are noisy samples of
one monotone curve, so an isotonic (PAV) fit along the LOS axis should remove
jitter using no truth.

The same note registered the stop condition explicitly:

> A `key_jitter` near zero at epoch 1 means stop.

and the reason: isotonic smoothing is "exactly powerless" against bias (+0% in
both bias rows of the §8.1 table), and `frac_band` caps the achievable gain
because every slice outside the band gets the identity.

## Reading `train gain` -- the sign is inverted

`train_gain_pct = 100 * (mapped_loss / unmapped_loss - 1)`
(`util/contrast_refit.py:315`), so **negative means the map REDUCED the loss**.
"Gain" reads like "benefit", and an earlier version of this note took the large
negative values as evidence the map was harmful. It is the opposite: on the
2048 refit slices the map achieves a real, sometimes large improvement. What it
never does is reach the epoch metrics, because it only touches the <1% of
slices inside the responsive band.

## Result: ufno completed, 20 epochs

`3d-ufno-expwall_theta-gnorm` (4457034), 22.4 h:

| | val_l2 | val_h1 | `key_jitter` | `frac_band` | train gain |
| --- | --- | --- | --- | --- | --- |
| ep1 | 0.1115 | 18.37 | 0.0000 | 0.5% | -1.87% |
| ep2 | 0.1104 | 18.29 | 0.0004 | 0.1% | -24.52% |
| ep7 | 0.0745 | 14.26 | 0.0032 | **0.0%** | -48.20% |
| ep14 | 0.0640 | 12.59 | -- | -- | -- |
| **ep18 (best)** | **0.0616** | **12.235** | -- | -- | -- |
| ep19 (final) | 0.0616 | 12.257 | 0.0043 | 0.6% | -31.36% |

`fno_whno-expwall_theta` (4457033) is still running; at epoch 9 it sits at
val_l2 0.0769 / val_h1 13.71, `key_jitter` 0.0066, `frac_band` 0.4%.

**The decisive comparison is ufno against itself.** Same architecture, same
groupnorm fix, 20 epochs each:

| ufno run | loss | val_l2 | val_h1 |
| --- | --- | --- | --- |
| **ufno-plain-gnorm** | plain L2 | **0.0471** | **9.15** |
| ufno-expwall_theta-gnorm | expwall + theta | 0.0616 | 12.26 |

Adding expwall+theta costs **31% on val_l2 and 34% on val_h1** against simply
training on L2. It is the best expwall-family cell in the matrix (whno_whno
0.0704, fno_whno 0.0721) -- but that is the architecture, not the map.

## The binding constraint is `frac_band`, not the key

`frac_band` never grew. Over 20 epochs it oscillated between **0.0% and 1.2%**,
ending at 0.6% -- no better than epoch 1's 0.5%. With
`CONTRAST_REFIT_SAMPLES = 2048` that is **0 to 25 slices** in the responsive
band, and the ~4 bins spanning 0.005-0.05 are fitted on that handful.

The sharpest single observation: at **epoch 7 `frac_band` was 0.0%** -- not one
slice of 2048 in the band -- and the run posted its largest improvement of the
campaign (val_l2 -13.3%). The gains come from the expwall objective, not the map.

`key_jitter` did rise over training, 0.0000 -> ~0.0050, as predictions sharpened
and the per-slice means stopped being trivially monotone, so the epoch-1 reading
("pure bias, smoothing is powerless") was true then and softened later. It never
mattered: 0.005 is still an order of magnitude below the ~0.05 error scale §8.1
was built around, against a band 0.045 wide.

A cone spanning z = 5-25 should physically have far more than 1% of its 256
slices in transition, so the key places slices outside the band even when the
truth is inside it -- the bias diagnosis arriving from a second direction.

## Why increasing `CONTRAST_BINS` does not help

Bins are log-spaced, `geomspace(1e-3, 1.0, n_bins - 1)` with a `0.0` edge
prepended (`contrast.py:295`), so ~4 of 14 bins already span the responsive
band and only ~4 cover everything above 0.1. At epoch 2 only **8 of 14 bins were
occupied**, with 5 floored; empty bins keep their previous value by design, so
more bins produce more frozen bins, and split the same 2-10 in-band slices more
thinly. The lever is `CONTRAST_REFIT_SAMPLES`, but the arithmetic is
discouraging: 50 slices in each of 4 band bins at `frac_band` = 0.1% needs
~200,000 refit slices, a 100x increase.

## Flooring

`theta_floor = 0.25` (`CONTRAST_THETA_FLOOR`, applied at
`util/contrast_refit.py:359`) clamps up any bin the fit wanted steeper. It is a
stability guard, not a modelling choice: the map amplifies gradients by
~1/(2*theta), and a previously fitted 0.031 amplified 16x and produced NaN
weights within one epoch. `THETA_MIN` is 0.02, so the schedule *can* represent
values 10x steeper than the floor.

Both runs report `median = 0.250`, i.e. **at least half the occupied bins sit on
the clamp rather than at a fitted value**. Lowering the floor would mostly
amplify an estimate driven by 2-10 slices.

## The schedule applies contrast everywhere, including where it cannot help

`viz/theta_z_profile.py` walks 60 real cones through each fitted table and bins
the applied theta by redshift (truth-keyed, so it shows the schedule's intent
rather than what the biased key selects).

| z | mean x_HI | ufno theta | fno_whno theta | floored |
| --- | --- | --- | --- | --- |
| 5.3 | 0.494 | 0.281 | 0.980 | 31-41% |
| 7.8 | 0.731 | 0.287 | 0.436 | 18-19% |
| 10.3 | 0.913 | 0.292 | 0.461 | 1-4% |
| 12.8-22.8 | 0.989-1.000 | **0.292** | **0.304** | 0% |

**`frac_identity` is 0.00 at every redshift** -- no slice anywhere receives
theta = THETA_MAX. This corrects a natural assumption (and an earlier claim in
this note): outside the responsive band the map is *not* the identity. Above
z ~ 12, where x_HI is 0.99-1.00 and there is no structure to sharpen, both runs
apply theta ~ 0.29-0.30, sitting on the 0.25 floor -- the most aggressive
contrast in the schedule, applied to the most saturated ~60% of every cone.

Likely mechanism: in a saturated region the objective is nearly insensitive to
theta, so the fit gets almost no gradient there and stays near its
initialisation, which is close to the floor. Since the map amplifies gradients
by ~1/(2*theta), that is a ~1.7x amplification over the majority of the volume
for no modelling benefit -- exactly the regime the floor exists to guard.

The two architectures also disagree completely inside the band: fno_whno fits
theta ~ 4.9 (near identity, "do not sharpen") where ufno fits 0.25 (the floor,
"sharpen as hard as allowed"). Same data, same objective, opposite conclusions
-- a strong hint the fit is unconstrained rather than finding signal.

## Status

`ufno-expwall_theta-gnorm` completed 20 epochs (best val_l2 0.0616 at ep18).
`fno_whno-expwall_theta` continues at the owner's request, to inspect
predictions qualitatively -- the refit diagnostics say nothing about what the
output cubes look like, and detailed visualisations exist
(`figures/fno_whno-expwall_theta-detailed_*`).

The quantitative question is answered: **in 3-D the theta schedule is
sample-starved in the band that matters** (0-25 of 2048 refit slices across all
20 epochs), LOS-monotone smoothing addresses a jitter component an order of
magnitude too small to matter, and on matched architecture the configuration
costs 31% val_l2 against plain L2.

This is a pre-registered negative result, not a failed run -- §8 specified the
diagnostics and the stop rule before the data existed.
