---
type: finding
title: "Native LOS Window Training"
created: 2026-09-24
updated: 2026-09-24
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - concept/architecture
  - concept/training-budget
  - finding/mixed
status: active
verdict: partial
related:
  - "[[Multi-Field 21cmFAST Data]]"
  - "[[3-D Operator Matrix Final Results]]"
  - "[[Warped LOS Grid Evaluation]]"
  - "[[Laplace Neural Operator Port]]"
  - "[[Excursion-Set Diagnostic]]"
  - "[[Global Reionization History Emulator]]"
  - "[[Transverse Symmetry Augmentation]]"
sources:
  - "`fno-21cm/notes/los-window-sampling.md`, `slurm/train_los_window.sbatch`"
  - "`checkpoints/3d_xhi/los_windows/*` (x_HI runs), `checkpoints/3d_xhi/mf_los_windows/*` (multi-field)"
  - "`experiments/los_windows/{contiguous_ep18,coarse_context_ep16}_test_metrics.json`, `predictions/*`"
  - "Jobs 4952130/4952131, 5096595 (first runs and r3), 5101369-72 and 5101442 (architecture set), 5145857-62 (multi-field), 5144031 (Laplace benchmark)"
---

# Native LOS Window Training

Training on the **native** line-of-sight grid (~2,100-2,900 cells at 1.43 Mpc)
instead of the 256-point cache, whose grid alone accounts for 60-98% of
end-to-end error ([[Multi-Field 21cmFAST Data]] §4). Full cones do not fit, so
the model trains on 256-cell windows with the full 140x140 transverse plane and
reassembles whole cones at evaluation from overlapping windows (32-cell halos,
192-cell cores). Task here: density -> $x_\text{HI}$, 2,000-cone subset
(1,600 / 200 / 200), `z_params` conditioning.

## 1. First runs: contiguous vs coarse context

Two `cnn/fno` runs, 4 windows per cone per epoch, 20-epoch schedule. Both were
killed by the 48 h wall before finishing; their best checkpoints were
evaluated on all 200 test cones:

| run | best full val | test MSE | test r |
|---|---:|---:|---:|
| **contiguous**, epoch 18 | 0.00613 | **0.00596** | 0.970 |
| coarse context (+4x-decimated 1,024-cell surroundings), epoch 16 | 0.00675 | 0.00606 | 0.970 |

**Coarse LOS context adds nothing.** This is consistent with the box tiling
found later: a 256-cell window already contains the whole 140-cell periodic box.

## 2. Where an epoch's time went

At 4 windows per cone with full 200-cone validation an epoch took **2.4-2.7 h**,
~60% of it validation:

- **Training is GPU-bound**: ~0.6 s forward+backward per window. Raw-file loading
  (1.3-2.1 s per sample) runs on DataLoader workers and hides behind it.
- **Validation is I/O-bound and serial**: each cone is walked through ~15
  overlapping windows at 12-15 s of reads per cone, because the raw gzip chunks
  make a window read cost as much as the whole field.

Two fixes were tried:

- **1 window per cone (run r3)**: epochs **4.4x cheaper**, but it learned ~4x less
  per epoch, so **no better per GPU hour** -- full val **0.0132**, test **0.0142**,
  about 2.3x worse than the 4-window runs. Comparison GIFs show why: r3 never
  reaches fully ionized and leaves a patchy x_HI ~ 0.05-0.2 haze in ionized
  regions. Reverted to 4 windows.
- **A fixed 40-cone validation subset**, chosen at evenly spaced quantiles of
  cone-mean $x_\text{HI}$, with the full 200 cones evaluated once at the end.
  This removed ~1.5 h per epoch of pure I/O and was kept.

**The subset is not a calibrated proxy for the full split.** At the same
checkpoint, full/subset was 0.82 for r3, **1.09** for `cnn/whno` and 0.88 for
`cnn/swhno`, so the offset changes sign between runs. Compare runs on the end-of-run full evaluation only.

The chunked native mirror ([[Multi-Field 21cmFAST Data]] §5) removes the read
bottleneck entirely (window reads 20x faster); the multi-field runs use it.

## 3. Architecture set on native windows

The top five basis combinations from the 3-D matrix ([[3-D Operator Matrix Final Results]])
plus a Laplace variant, with configs copied from the 3-D winners: 4 windows per
cone, 30 epochs, 40-cone subset, walltime per model (48-132 h).

| model | params (`numel`) | test MSE | full val | status |
|---|---:|---:|---:|---|
| `cnn/whno` | 3.47 M | **0.00716** (r 0.964) | 0.00717 | done |
| `cnn/swhno` | 1.41 M | **0.00714** (r 0.964) | 0.00777 | done |
| `cnn/fno` bw48 | 20.7 M | -- | -- | epoch 16/30, subset best 0.0106 |
| `cnn/sfno` bw48om60 | 12.4 M | -- | -- | epoch 14/30, subset best 0.0121 |
| `sfno/swhno` bw48om60 | 0.75 M | -- | -- | epoch 6/30, 3.9 h/epoch |
| `cnn/lap4` bw48 | -- | -- | -- | **not viable**: out of memory |

Parameter counts are PyTorch `numel`, which counts a complex weight once, so the
Fourier-family counts are understated (see [[3-D Operator Matrix Final Results]]).

**Both finished Walsh models are ~20% worse on test than the old contiguous
`cnn/fno` (0.00596)**, despite a 30-epoch rather than 20-epoch schedule.

*Correction:* mid-run I concluded that `cnn/whno` "matches the old run, if
anything slightly ahead". That rested on matched-schedule-fraction comparisons
of train loss and **subset** validation, where the two curves were nearly
identical (0.0077 / 0.0075 at 77% of schedule). Train loss did match; the
validation match was a subset artifact, because for this run the subset scores
easier than the full split. The full evaluation shows the gap.

Confounds between the old `cnn/fno` and the new configs: the new configs
disable `grid_embedding` (on in the old run) and use width 48 instead of 32 for
the FNO family. The dataset still supplies relative LOS position as a channel,
so the grid-embedding effect is probably small but unmeasured.

**Laplace does not fit in 3-D at this window size.** A clean benchmark (job
5144031) ran out of memory on one 140x140x256 window at batch 1, at 77.9 of
79.3 GB. On CPU its forward pass took 502.7 s against 73.1 s for `cnn/fno`.
Options (smaller width, smaller channel chunks, gradient checkpointing) are
untried. See [[Laplace Neural Operator Port]].

## 4. Reionization timing at the prior's edges

On cone 27 every windowed run reionizes **dz ~ 0.6-1.3 too late**, with zero LOS
misalignment (cross-correlation peaks at lag 0 on every cone). Cone 27
reionizes at $z_\text{mid}$ = 15.8, the 99.8th percentile of training cones.
The error grows with distance from the typical history and points back toward
it (cone 1275: -0.8; the late reionizer 1031: +0.49). Timing comes almost
entirely from the parameters, so this is regression to the mean. Diagnosis and
fix: [[Global Reionization History Emulator]].

## 5. Multi-field windows

The same five architectures on density + LOS velocity -> $x_\text{HI}$ +
$T_b$, from the native mirror, all other settings matched (jobs 5145857-62).
The loss weights both fields' normalized MSE equally, with a sigmoid only on
$x_\text{HI}$. The mirror makes the loader cheap: **0.34 s per training window**
and **0.84 h per epoch** including validation, against 0.87 h for the
single-field runs on raw files.

`cnn/whno` at epoch 6: $x_\text{HI}$ normalized MSE 0.035 (r 0.855), $T_b$
0.46 (r 0.645). Early, and not comparable to the single-field numbers because the
combined loss is dominated by $T_b$, which is scaled to unit variance.

## 6. Single-change variants in flight

Each is `cnn/whno`, same seed and **identical training windows** as the
finished baseline, differing in one thing:

- [[Transverse Symmetry Augmentation]] (job 5148158)
- Excursion-set input channels (job 5149043), see [[Excursion-Set Diagnostic]]
- Emulated global history channel (job 5161264), see [[Global Reionization History Emulator]]
