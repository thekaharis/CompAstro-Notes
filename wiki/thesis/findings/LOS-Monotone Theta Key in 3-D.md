---
type: finding
title: "LOS-Monotone Theta Key in 3-D"
created: 2026-08-06
updated: 2026-08-06
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

## Result

Both architectures, epoch 1, `CONTRAST_KEY=monotone`:

| run | `key_jitter` | `frac_band` | train gain | bins floored |
| --- | --- | --- | --- | --- |
| ufno (groupnorm) | **0.0000** | 0.5% | -1.87% | 7/14 |
| fno_whno | **0.0005** | 1.0% | -0.89% | 4/14 |

ufno at epoch 2: `key_jitter` 0.0004, `frac_band` **0.1%**, train gain
**-24.52%**, 8/14 bins seen.

The stop condition fired on both architectures independently. `key_jitter` of
0.0000-0.0005 is 2 orders of magnitude below the ~0.05 error scale the §8.1
table was built around: the raw per-slice means are **already monotone**, so the
isotonic fit is the identity and has no jitter to remove. By §8.1's own logic the
key error is therefore **bias, not jitter**, and this is the case smoothing
cannot reach.

## The binding constraint is `frac_band`, not the key

`frac_band` did not grow as predictions sharpened — it *fell*, 0.5% -> 0.1%.
With `CONTRAST_REFIT_SAMPLES = 2048` that is:

- epoch 1: 0.5% x 2048 ~= **10 slices** in the responsive band
- epoch 2: 0.1% x 2048 ~= **2 slices**

The ~4 bins that span 0.005-0.05 are being fitted on 2-10 LOS slices. That, not
bin resolution, is why half the schedule floors (see below) and why the train
gain went sharply negative.

A cone spanning z = 5-25 should physically have far more than 0.1% of its 256
slices in transition, so the key appears to place slices outside the band even
when the truth is inside it — the bias diagnosis arriving from a second
direction.

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

## Status

Left running at the owner's request to inspect predictions qualitatively, since
the refit diagnostics say nothing about what the output cubes look like. The
quantitative question is answered: **in 3-D the theta schedule is
sample-starved in the band that matters**, and LOS-monotone smoothing addresses
a jitter component that is not present.

This is a pre-registered negative result, not a failed run — §8 specified the
diagnostics and the stop rule before the data existed.
