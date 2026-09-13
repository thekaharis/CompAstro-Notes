---
type: finding
title: "Learned Waveform Basis Operator"
created: 2026-09-13
updated: 2026-09-13
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - architecture/fno
  - architecture/local-fno
  - concept/basis-choice
  - concept/spectral-truncation
  - concept/discontinuities
  - concept/architecture
  - finding/negative
status: active
verdict: complete
related:
  - "[[Square-Wave Basis for Ionization Fields]]"
  - "[[Walsh-Hadamard Neural Operator]]"
  - "[[Structured-Transform Operator Findings]]"
  - "[[3-D Operator Matrix Final Results]]"
  - "[[Loss Objective and Operator Basis Sweep]]"
  - "[[Windowed Local-FNO U-Net Findings]]"
  - "[[Hedging Bias of Pointwise Losses]]"
sources:
  - "`checkpoints/2d_xhi/lwf_lwf/xhi2d_lwf_both_ph_*` (init sweep, LR sweep, 21-run seeded control matrix, 6 separate-transform runs)"
  - "`checkpoints/2d_xhi/id_lwf/xhi2d_id_lwf_grid_{sine,square,sawtooth,random}_s0`, `checkpoints/2d_xhi/id_fno/xhi2d_id_fno_grid_s0` (identity ablation, jobs 4902218/19/21, 4905501/02)"
  - "`figures/shared/diagnostics/waveforms/`, `figures/shared/diagnostics/waveform_seed_controls/`"
  - "`learned_waveform_operator.py`, `operators.py` (IdentityOperator), `viz/learned_waveforms.py`, `viz/waveform_seed_controls_report.py`"
---

# Learned Waveform Basis Operator

The adaptive-basis experiment on the **2-D task** ($x_\text{HI}$ slices, 140x140,
100-epoch budget, batch 32, lr 3e-4). The question behind it: the Walsh results
([[Square-Wave Basis for Ionization Fields]]) suggested a square-wave basis
should suit a two-phase ionization field better than Fourier, so rather than
choose a basis, **learn one**.

The answer, established four independent ways below, is that **on this task the
basis is not a free parameter — every configuration converges to Fourier and
scores like Fourier.** That is a positive mechanistic result about the problem
and a negative result for the adaptive-basis idea, and both halves matter.

## 1. What the operator is

Per axis, a learned **mother bin table** (15 bins local, 31 global) is expanded
into a candidate set by **dilation** ($k = 1,2,3$) and **phase shift**
($0, 0.25$), resampled through a **truncated Fourier series** that acts purely as
a fixed anti-aliasing filter, then **reduced-QR orthonormalized with DC first**.
The learned parameters are real bin amplitudes; the Fourier machinery is a
resampler, not the representation.

Key structural facts:

- **A sine mother waveform generates exactly the Fourier basis.** Its candidates
  are already orthonormal (condition number 1.000), so the operator degenerates
  to a truncated FNO. Fourier is inside the search space as an exact point.
- `sampled_candidates` normalizes each column to unit norm, so the **overall
  table scale is a gauge direction** the loss cannot see.
- Waveform parameters get their own optimizer group (`waveform_parameter_groups`):
  0.1x LR by default, zero weight decay.
- **Phase mixing** (real phase-pair blocks, `phase_weight` zero-initialized) adds
  395,264 parameters, 823,959 total for the `lwf/lwf` 2-D model.

Six initializations were used throughout: random, smooth_random, sine, triangle,
square, sawtooth.

## 2. Seeded control matrix — 7 conditions x 3 seeds

The training-schedule axis (`WAVEFORM_TRAINING_MODE` = joint / frozen /
adapt25 / alternating), run as 21 matched runs with `RUN_SEED` controlling both
initialization and loader order, so pairing across conditions is bit-identical.

| arm | joint | frozen | adapt25 |
| --- | ---: | ---: | ---: |
| square | 0.1107 +/- 0.0002 | 0.1108 +/- 0.0003 | 0.1108 +/- 0.0006 |
| sawtooth | 0.1101 +/- 0.0009 | 0.1108 +/- 0.0004 | 0.1100 +/- 0.0009 |
| sine (frozen) | — | 0.1109, 0.1109, 0.1109 | — |

**This matrix is where the replicate noise floor comes from**: identical-config
seeds spread by **sd 0.0002-0.0009 in val_l2**. Every number elsewhere on this
page is judged against that band. Only two contrasts cleared it — sawtooth
frozen-minus-joint and adapt25-minus-frozen — and both are single-arm effects of
about one floor width.

> An earlier attempt at this matrix was invalid: `WAVEFORM_KERNEL_SCOPE=spectral`
> silently froze ~260 k parameters (lifting, projection, U-Net shell, norms) in
> the kernel-only phases, giving val_l2 0.387. Re-run with `scope=all`.

## 3. Separate analysis/synthesis transforms — null, but informative

`WAVEFORM_TRANSFORM=separate` gives the operator independent analysis and
synthesis banks (+182 parameters). Six runs, square and sawtooth x 3 seeds,
100 epochs, paired against their tied counterparts:

| init | s0 | s1 | s2 | mean | sd |
| --- | ---: | ---: | ---: | ---: | ---: |
| square | +0.0008 | -0.0003 | +0.0001 | **+0.0002** | 0.0006 |
| sawtooth | +0.0002 | -0.0007 | -0.0009 | **-0.0005** | 0.0006 |

Mixed signs, both means inside the floor. **But the two banks genuinely diverged**,
so this is a real null rather than dead plumbing — correlation between the
analysis and synthesis mother tables at epoch 99:

| slot | square | sawtooth |
| --- | --- | --- |
| encoder0 | 0.94-0.97 | **0.67-0.80** |
| encoder1 | 0.98-1.00 | 0.93-0.97 |
| bottleneck | 0.99-1.00 | 0.98-0.99 |
| decoder1 | 0.95-0.99 | 0.84-0.97 |
| decoder0 | 0.97-0.99 | 0.91-0.96 |

The freedom is used at the **shallowest** slots and ignored at the **bottleneck**.
Sawtooth splits hardest, consistent with it being the init furthest from where
the model wants to be. The optimizer pulls the banks apart and the loss does not
care.

## 4. Identity ablation — deleting the local branch

Replacing the windowed local operator with `IdentityOperator` (added to
`operators.py`, tag `id`) leaves the **global slot as the only operator in the
model**, and isolates the basis question from the local branch entirely. Run
with the new positional grid embedding (`GRID_EMBEDDING=1`), otherwise matched
to the `lwf/lwf` reference.

| run | params | best val_l2 | @ep | test | wall clock |
| --- | ---: | ---: | ---: | ---: | ---: |
| identity / fourier (plain FNO) | 778,785 | **0.1113** | 46 | 0.1173 | 1:20 |
| identity / lwf, sine init | 715,359 | 0.1116 | 38 | 0.1170 | 1:33 |
| identity / lwf, square init | 715,359 | 0.1116 | 34 | 0.1157 | 1:33 |
| identity / lwf, sawtooth init | 715,359 | 0.1118 | 34 | 0.1175 | ~1:30 |
| identity / lwf, random init | 715,359 | 0.1126 | 36 | 0.1163 | ~1:30 |
| cnn-local / lwf, sine (reference) | 823,959 | 0.1109 | 38 | 0.1163 | 5:54-6:18 |
| cnn-local / lwf, square (reference) | 823,959 | 0.1107 | 47 | 0.1158 | 5:54-6:18 |

**Deleting the local branch costs +0.0007 to +0.0009 val_l2** — the top edge of
the replicate floor — while removing **108,600 parameters (13%)** and running
**~4x faster**. The windowed local operator is not earning its cost. This is the
second time the **window loop**, not the weight count, has turned out to be where
the compute goes; see [[3-D Operator Matrix Final Results]] §2.1, where parameter
count and inference cost correlate at 0.011.

## 5. Fourier is an attractor — four inits, one destination

With the local branch gone, the bottleneck mother table was tracked from four
starting shapes. Correlations are magnitudes (table polarity is arbitrary):

| init | \|vs sine\| (x, y) | \|vs init\| | distance travelled |
| --- | --- | ---: | --- |
| sine | 0.9997, 0.9997 | 0.9997 | none (fixed point) |
| square | 0.9997, 0.9994 | 0.913 | 0.914 -> 0.9997 |
| sawtooth | 0.9995, 0.9995 | 0.787 | 0.781 -> 0.9995 |
| random | 0.767, 0.9972 | 0.449 / 0.307 | partial, see below |

![[lwf_identity_bottleneck_square.png]]

![[lwf_identity_bottleneck_sawtooth.png]]

**Three checks rule out the trivial explanations.**

1. **Not a bandlimiting artifact.** The resampler keeps
   `min((bins-1)//2, (size-1)//(2k))` harmonics; at the bottleneck (31 bins,
   size 35) that is **15 harmonics at k=1** — the entire Nyquist budget for a
   31-bin table. A 15-harmonic square is still a square. The inits had full
   capacity to hold their shape for 100 epochs and did not.
2. **Not decay toward something degenerate.** The table norm is conserved to
   1.5-5% while the shape changes completely; the square's peak goes
   1.0 -> **1.42 $\approx \sqrt{2}$**, exactly the equal-RMS sine. The trajectory
   runs along the sphere, which is what the gauge-invariance in §1 predicts.
3. **Not one lucky trajectory.** The x and y axes are independent parameters and
   land on the same answer to four decimals in every structured arm.

**Random is the informative exception.** Axis y reached 0.9972; axis x sits at
0.767 — but it is a clean single sine cycle **plus a one-bin spike at the wrap
point** that never annealed out, not a different basis. It is also the only arm
outside the replicate floor (0.1126, +0.0013 over plain FNO). The defect and the
loss penalty are the same fact: the arm that did not finish arriving is the arm
that pays.

![[lwf_identity_bottleneck_random.png]]

## 6. What this establishes

1. **Fourier is the optimum within this candidate family on 2-D $x_\text{HI}$,
   demonstrated by convergence from four directions** rather than asserted. Sine
   is a fixed point, and square, sawtooth and (nearly) random all walk to it with
   full capacity to do otherwise.
2. **The square-wave intuition does not survive contact with a learned basis.**
   [[Square-Wave Basis for Ionization Fields]] motivated a two-phase basis for a
   two-phase field; given the freedom to build one, the model discards it. The
   Walsh models' wins elsewhere are therefore **not** evidence that a square
   basis is the right representation — see [[Phase Coherence and Bubble Size Bias]],
   where their small-scale power turns out to be wrong-phase power.
3. **A discontinuous mother waveform is not a barrier.** The sawtooth travelled
   furthest (init correlation 0.787) and still arrived. The barrier to
   convergence was the **local branch**, not the jump: with a windowed local
   operator present the same sawtooth stalls at ~0.89 against sine across three
   seeds, because the local branch supplies the short-range corrections that
   would otherwise force the global slot to be an efficient global basis.
4. **The adaptive basis has no headroom on this task.** Every arm scores within
   0.0013 of a plain FNO, most within the replicate floor, at 715 k parameters
   against 779 k. It costs nothing and buys nothing.
5. **The windowed local branch costs 4x wall clock for at most one floor width.**

## Caveats

- **Single seed per identity arm.** The §5 losses are one draw each against a
  floor estimated in §2. "No effect detectable at n = 1" is the honest reading,
  not "no effect".
- **2-D only, bottleneck only.** The mother tables analysed in §5 are the
  bottleneck bank. Nothing here is evidence about 3-D $x_\text{HI}$ or
  $z_\text{re}$, where the basis-ranking comparison already showed the preferred
  bases differ by target.
- The divergence measured in §3 is on mother tables, not on the **effective**
  bases after dilation, phase and QR, which may differ by more or less.
- No **sine arm** was run for the separate transform — the case where untying
  could most plausibly matter, since sine is already the exact Fourier basis.

## Open

- **Seed replication of the sawtooth identity arm** (~1.5 h per seed now that the
  local branch is gone). The strongest single result on the page rests on n = 1.
- **Repeat the identity ablation on $z_\text{re}$ or 3-D $x_\text{HI}$** to test
  whether the Fourier attractor is task-specific or general.
- **Why the local branch blocks convergence** (§6.3) is inferred from the stall at
  ~0.89, not demonstrated. Ablating the local branch's window size rather than
  the branch itself would separate "short-range corrections" from "windowing".
- The grid-embedding confound: identity arms carry positional grid channels and
  the `cnn`-local references do not, so the §4 cost is really "local branch minus
  grid embedding". One `GRID_EMBEDDING=0` identity/fourier run separates them.
