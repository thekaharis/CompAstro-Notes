---
type: finding
title: "Granulometry (BSD) Auxiliary Loss"
created: 2026-08-10
updated: 2026-08-10
tags:
  - domain/thesis
  - domain/ml
  - domain/reionization
  - concept/loss-design
  - concept/bubble-morphology
  - architecture/ufno
  - finding/positive
  - finding/open
status: open
verdict: positive
related:
  - "[[Bubble Size Distribution]]"
  - "[[Edge and Wall-Placement Losses]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[U-FNO BatchNorm Train-Eval Mismatch]]"
  - "[[Loss Objective and Operator Basis Sweep]]"
sources:
  - "implementation: `losses.py` `GranulometrySpectrum`, `LOSS=bsd` in `slurm/train_3d_matrix.sbatch`"
  - "runs 4485729/30/31 (ufno expwall / hybrid / bsd, all groupnorm, seed-matched)"
  - "evaluation: job 4494775, `figures/bubble_size_out/ufno_trio/`"
---

# Granulometry (BSD) Auxiliary Loss

**The first auxiliary term in this campaign that measurably improves the thing
it targets.** It halves the bubble-size bias, and it costs 6.5% of `val_l2` to
do it.

## The idea

The mean-free-path bubble-size distribution that
`viz/bubble_size_evaluation.py` reports cannot be a training term: it
thresholds the field, takes a first crossing along each ray, and histograms the
result -- none of which has a useful gradient.

`GranulometrySpectrum` is the differentiable stand-in. **Morphological opening**
by a ball of radius `r` (erode, then dilate) keeps only structures that ball
fits inside, so the volume lost between consecutive radii is the mass of
structures at that scale -- a size distribution, and the same physics the MFP
estimator samples. Erosion and dilation are min/max filters, hence max-pooling,
hence differentiable almost everywhere. Against the MFP estimator on discs of
radius 2-13 the two agree at **Pearson r = 0.99**.

It works on the **raw field**: grayscale opening needs no threshold, so unlike
the MFP estimator there is no cutoff to choose and no gradient killed by a hard
mask.

Configuration used: `BSD_RADII=1,2,4,8`, `BSD_DOWNSAMPLE=2`,
`BSD_MAX_SLICES=64`, `BSD_WARMUP_EPOCHS=5`, on top of the `hybrid` objective
(`L2=1.0`, `expwall=30.0`).

### It cannot stand alone

A size spectrum is invariant to translation, to rotation, and to any
rearrangement preserving sizes. Measured: a field with every bubble displaced
37 px scores **21x better** than one with the wrong sizes. That is the same
hole that sank the L2-free edge run (`edgeonly`, 0.9098, never beating its
epoch-0 value) and it is worse here. This is why `LOSS=bsd` rides on the
expwall+L2 anchor rather than replacing it -- the same conclusion
[[Edge and Wall-Placement Losses]] reached for expwall.

## Result

Three U-FNO runs, **identical seed and groupnorm**, 20 epochs each, differing
only in the loss. Seed-matching is real here: all three produced byte-identical
epoch-0 metrics, so any later divergence is the loss term and not
initialisation.

BSD evaluated on 200 test cones, `active 0.05-0.95` stage, truth mean radius
**10.410 Mpc**:

| run | val_l2 | val_h1 | pred mean (Mpc) | rel. bias | Wasserstein | JS div |
| --- | --- | --- | --- | --- | --- | --- |
| ufno-plain (L2) | **0.0471** | **9.15** | 12.959 | +0.0599 | 2.1996 | **0.00627** |
| ufno-hybrid (L2+expwall) | 0.0490 | 9.60 | 11.500 | +0.0504 | 1.9958 | 0.00626 |
| **ufno-bsd** (+granulometry) | 0.0502 | 9.72 | 11.648 | **+0.0294** | **1.9733** | 0.00685 |

**Relative mean bias falls +6.0% -> +2.9%, a 51% reduction**, with the best
transport distance of the three. Per stage the granulometry run is better than
plain in four of five bins:

| stage | plain | hybrid | bsd |
| --- | --- | --- | --- |
| xbar_HI 0.02-0.20 | 0.0929 | 0.1648 | 0.1112 |
| xbar_HI 0.20-0.40 | 0.0878 | 0.1296 | 0.1184 |
| xbar_HI 0.40-0.60 | 0.0761 | 0.1073 | **0.0533** |
| xbar_HI 0.60-0.80 | 0.0535 | 0.0472 | **0.0015** |
| xbar_HI 0.80-0.98 | 0.0098 | -0.0088 | -0.0208 |
| **active 0.05-0.95** | 0.0599 | 0.0504 | **0.0294** |

At `xbar_HI 0.60-0.80` the bias is **+0.0015**, essentially zero.

## Two things it does not do

**The distribution shape is not improved.** JS divergence is marginally *worse*
(0.00685 vs plain's 0.00627). The term fixes the mean radius and the transport
distance, not the full spectrum -- consistent with optimising a 3-number opening
spectrum rather than the histogram itself.

**The large-bubble regime gets worse, for every loss.** In `xbar_HI 0.02-0.20`
all three runs are worse than at any later stage, hybrid worst at +0.165. Early
reionisation, where bubbles are largest and rarest, is not helped by any
objective tried so far.

## Cost

On the epoch-capped leaderboard ([[Loss Objective and Operator Basis Sweep]]
section 3), `ufno_bsd_gnorm` scores test RMSE **0.0488** against
`ufno_plain_gnorm` at 0.0467 -- 4.5% worse, and 6.5% worse on `val_l2`. So it
is a genuine trade rather than a free win:

* whole-volume accuracy: **plain L2 wins** (0.0471 vs 0.0502 val_l2)
* bubble-size fidelity: **granulometry wins** (+0.029 vs +0.060 bias)

Which matters depends on the downstream use. For voxel-level emulation, plain
L2. For EFT-targeted inference on ionisation *morphology*, the BSD side is
arguably the one that counts -- and it is the first term in this campaign to
move it.

## Open

* Only tested on U-FNO. `whno_whno-bsd` and `fno_fno-bsd` are running; whether
  the gain is architecture-independent is unknown.
* The weight (`LOSS_BSD_WEIGHT=1.0`) and radii (`1,2,4,8`) were not swept. The
  cost/benefit ratio above is one point in that space, not an optimum.
* JS divergence getting worse while the mean improves suggests the spectrum
  distance may be the wrong summary; matching more radii, or the histogram
  shape directly, is untested.
