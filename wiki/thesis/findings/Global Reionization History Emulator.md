---
type: finding
title: "Global Reionization History Emulator"
created: 2026-09-24
updated: 2026-09-24
tags:
  - domain/thesis
  - domain/reionization
  - domain/ml
  - concept/emulator
  - concept/conditioning
  - finding/positive
status: active
verdict: partial
related:
  - "[[Native LOS Window Training]]"
  - "[[Multi-Field 21cmFAST Data]]"
  - "[[Neutral Fraction]]"
  - "[[Excursion-Set Input Layer]]"
  - "[[Contrast Map Sharpening]]"
sources:
  - "`fno-21cm/tools_global_history_emulator.py`, `slurm/global_history_emulator.sbatch` (job 5158645)"
  - "`fno-21cm/dataset/global_history.py`; `--history-emulator` in `fno_multifield.py`"
  - "`experiments/global_history/{evaluation,relevel}.json`, `histories_vs_field_model.png`"
  - "commit 57a9d26 on `codex/frequency-mixing-transform`; test run job 5161264"
---

# Global Reionization History Emulator

## Problem: timing regresses to the mean

On cone 27 every native-window run reionizes **dz ~ 0.6-1.3 too late**
([[Native LOS Window Training]] §4). It is not a spatial error: cross-correlating
prediction and truth over LOS offsets of -12 to +12 cells peaks at **lag 0 on
every cone of every run**. It is a timing error:

- cone 27 reaches $\bar x_\text{HI} = 0.5$ at z = 15.8; only **3 of 1,600
  training cones** reionize that early (99.8th percentile; ~half the training
  cones are still >50% neutral at z = 4);
- its parameters sit in a corner of the prior (F_STAR10 93rd percentile, F_ESC10
  84th, M_TURN 11th, ALPHA_STAR 10th), and even its five nearest training
  neighbours reionize at z = 11.5-14.6;
- the error grows with distance from the typical history and points back toward
  it: cone 1275 (89th percentile) -0.8, the late reionizer 1031 **+0.49**,
  typical cones within 0.03.

Density carries almost no timing information, so the field model learns
parameters -> timing from 1,600 examples and shrinks toward the typical history
at the edges. For inference, that is a bias concentrated at the prior's edges.

## Emulator

Every raw file stores the **box-averaged** $x_\text{HI}$ at 101 node redshifts
(z = 4-35.2, shared by all simulations), for all 6,600 simulations -- not only
the 2,000-cone field subset.

- 5-member ensemble of MLPs, 11 parameters -> 101-point history, **monotone in
  z by construction**: $\sigma(b + \text{cumsum}\,\text{softplus}(d) - 10)$ over
  increasing z. Monotonicity holds in the data for 6,599/6,600 histories.
- Trained on **5,322** simulations (591 for early stopping), holding out the
  validation and test cones of **both** the $x_\text{HI}$ and multi-field studies
  (687), so it can feed either field model without leakage. 9 min on CPU.
- Held-out $x_\text{HI}$ test (200 cones): history RMSE **0.009**, median midpoint
  error $|\Delta z|$ **0.044**, 90th percentile 0.094.

| cone | $z_\text{mid}$ box truth | emulator | field model contiguous | field model coarse |
|---|---:|---:|---:|---:|
| 27 | 15.84 | **15.90** | 15.35 | 14.65 |
| 1275 | 10.62 | **10.69** | 9.68 | 9.66 |
| 1031 | 6.08 | **6.00** | 6.46 | 5.93 |

## What it cannot do

The truth a field model is scored against is the mean of each **thin lightcone
slice**, which scatters around the box history by 0.02-0.08 RMS -- real
slice-to-slice density variation, plus interpolation between node boxes. The
field model sees each slice's density and tracks those fluctuations closely on
typical cones; the emulator knows only the parameters. Each gets right what the
other gets wrong.

## Post-hoc test: re-level existing predictions

Shift each predicted slice in logit space so its mean equals the emulator's
$x_\text{HI}(z)$; no retraining. Mean MSE over the 12 saved test cones:

| run | as trained | re-levelled to emulator | re-levelled to true slice mean (ceiling) |
|---|---:|---:|---:|
| contiguous | 0.00893 | **0.00725** (-19%) | 0.00577 |
| coarse context | 0.01054 | **0.00717** (-32%) | 0.00571 |

Large gains on the mistimed cones (27: 0.0108 -> 0.0057; 1275: 0.0228 ->
0.0085), losses on typical ones (1956: 0.0114 -> 0.0163): forcing every slice to
the smooth box history erases the slice-level variation the field model had
right. **Hard re-levelling is too blunt.**

## Integration: history as an input channel (run in flight)

`dataset/global_history.py` holds the frozen emulator; `--history-emulator`
(`HISTORY_EMULATOR=` in `train_los_window.sbatch`) appends
`x_HI_global_emulated(z)` as the **last** input channel -- constant across the
sky plane, one value per LOS slice -- so existing channel indices (including the
[[Excursion-Set Input Layer]]'s) do not move. The field model gets reliable
timing and can still deviate slice by slice from the density it sees.

Run metadata records the emulator's path and sha256; restore reinstalls it and
refuses a changed file or mismatched channels. Verified on cone 27 (channel
crosses 0.5 at z = 15.896, identical to the emulator) and by an end-to-end CPU
train -> checkpoint -> restore -> evaluate cycle. `emulator.pt` is gitignored
(`*.pt`); rebuilding it changes the hash.

**Test (job 5161264)**: `cnn/whno` + history channel, identical seed and windows
to the baseline. Check: full test MSE, and $z_\text{mid}$ on cones 27, 1275, 1031.
