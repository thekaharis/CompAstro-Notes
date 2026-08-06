---
type: finding
title: "U-FNO BatchNorm Train-Eval Mismatch"
created: 2026-08-06
updated: 2026-08-06
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - concept/normalization
  - concept/train-eval-gap
  - architecture/ufno
  - finding/positive
  - finding/closed
status: closed
verdict: positive
related:
  - "[[U-FNO]]"
  - "[[Fourier Neural Operator]]"
  - "[[3-D Architecture x Loss Matrix]]"
sources:
  - "runs 4425989 / 4425990 (batchnorm), 4447576 (groupnorm)"
  - "implementation: `models_ufno.py`, `modeling.py:297`"
  - "`checkpoints_3d_ufno_hybrid/best_model_state_dict.pt` (epoch 3)"
---

# U-FNO BatchNorm Train-Eval Mismatch

## Claim

U-FNO's default `ufno_norm=batchnorm` is **unusable at batch size 1** on 3-D
lightcone cubes. It cost a factor of ~4.6 in `val_l2` and made the architecture
look like the worst cell of the [[3-D Architecture x Loss Matrix]] when it is in
fact the best.

## Evidence

Same architecture, same data, same loss, epoch 0:

| | groupnorm | batchnorm | fno_whno (reference) |
| --- | --- | --- | --- |
| train L2 | 0.1224 | 0.1162 | 0.1805 |
| val_l2 | **0.1049** | 0.4829 | 0.1279 |
| val_l2 / train L2 | **0.86x** | 4.16x | 0.71x |
| `val_pred_sat_low` | **0.0000** | 0.3347 | 0.0000 |
| `val_pred_std` | 0.2230 | 0.4889 | 0.1927 |

The diagnostic signature: **training loss is essentially identical** (0.1224 vs
0.1162) while validation differs 4.6x. The model was always fitting the data;
only the `model.eval()` path was broken. Under batchnorm the gap widened over
training (4.2x -> 6.4x -> 6.1x -> 8.1x by epoch 3) while `val_h1_rel` stayed
pinned at ~0.95 and then rose above 1.0 — i.e. worse than the trivial baseline.

## Mechanism

Confirmed by inspecting the saved batchnorm checkpoint directly rather than by
ablation alone. 15 `BatchNorm3d` layers, `num_batches_tracked = 15840` = 3
epochs x 5280 samples, confirming statistics accumulated one sample at a time.

**38 of 480 channels have `running_var` below the default `eps = 1e-5`**,
concentrated in one layer:

| layer | degenerate channels | var median |
| --- | --- | --- |
| `fno.body.unet3.conv3_1` | **31/32** | 9.5e-09 (min 4.7e-15) |
| `fno.body.unet3.conv3` | 6/32 | 6.9e-04 |
| `fno.body.unet4.conv3_1` | 1/32 | 4.4e-03 |

For `unet3.conv3_1` the eval-time normalizer is `1/sqrt(var + eps) ~= 316`
because eps dominates, while training at batch size 1 divides by the actual
per-sample `1/sqrt(var) ~= 9032` — a **28.6x scale discrepancy** between the two
modes in that layer. Healthy layers show ratios of 1.000 and 1.007, so this is
not a global artifact.

Two mechanisms compound:

1. **Batch size 1 makes BatchNorm behave as instance norm during training** (each
   sample normalized by its own spatial statistics) while eval uses running
   averages pooled over very dissimilar cubes.
2. **`momentum=0.1` at batch size 1** (constructed with defaults,
   `models_ufno.py:112` and `:240`) makes the running statistics an EMA over
   roughly the **last 10 cubes**, not the dataset — which is also how a variance
   collapses to 1e-15 in the first place.

## Resolution

`UFNO_NORM=groupnorm`, already implemented at `models_ufno.py:49`
(`_replace_bn_with_groupnorm`). GroupNorm has no batch statistics, so it is
identical in train and eval; the docstring at `:60` also notes the
SyncBatchNorm conversion becomes a no-op, so the DDP path is unaffected.

Only `batchnorm` and `groupnorm` are valid values (`modeling.py:297`) —
`instance` is **not** accepted.

## Consequence for the matrix

With GroupNorm, U-FNO went from the worst cell to the best completed run:

| completed run | val_l2 | val_h1 | wall-clock |
| --- | --- | --- | --- |
| **ufno-plain (groupnorm)** | **0.0471** | **9.15** | 23.6 h |
| fno_whno-plain | 0.0611 | 10.97 | 53.1 h |
| fno_whno-hybrid | 0.0650 | 11.63 | 53.8 h |

23% better `val_l2` and 17% better `val_h1` in 45% of the wall clock. The lead
was established by epoch 2 and held to completion.

## Generalization

Any batch-size-1 3-D operator model with a BatchNorm-bearing CNN path is
exposed to this. The cheap detector is the ratio `val_<term> / train_<term>_term`
compared against its own training term — not against `train_err`, which is a
weighted blend once multiple loss terms are active.
