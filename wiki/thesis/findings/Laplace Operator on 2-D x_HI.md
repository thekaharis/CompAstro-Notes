---
type: finding
title: "Laplace Operator on 2-D x_HI"
created: 2026-09-15
updated: 2026-09-15
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - architecture/fno
  - concept/basis-choice
  - concept/discontinuities
  - concept/sharp-fronts
  - concept/architecture
  - finding/positive
status: active
verdict: partial
related:
  - "[[Laplace Neural Operator Port]]"
  - "[[Frequency-Mixing Operator]]"
  - "[[Learned Waveform Basis Operator]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[3-D Operator Matrix Final Results]]"
  - "[[LOS Bandwidth as the 3-D Bottleneck]]"
sources:
  - "`checkpoints/2d_xhi/fno_lap/xhi2d_fno_lap_p{2,4,8,16}_grid_s{0,1,2}` (jobs 4922105-10, 4931776-81)"
  - "`checkpoints/2d_xhi/{fno_fno,fno_fmix,fmix_fmix}/*` (control and mixing arms, jobs 4921861-69)"
  - "`figures/2d_xhi/eval/lap_p4_{s0_representative,ps_coherence*,edge}` (jobs 4934131, 4934109, 4934153)"
  - "`viz/edge_metrics_xhi2d.py`, `viz/seal_truncated_run.py`, `viz/compute_final_report.py` (added 2026-09-15)"
---

# Laplace Operator on 2-D x_HI

First architecture change in this campaign to clear the replicate floor
convincingly. The operator is the pole-residue layer of Cao et al. (2023),
ported and made tractable as described in [[Laplace Neural Operator Port]];
here it occupies the **global slot** with `fourier` local, against a
`fourier`/`fourier` control at matched seeds.

> **Scope.** 2-D $x_\text{HI}$ only, 3 seeds per arm, and **no run reached its
> 100-epoch budget** -- every Laplace job was killed by the 8 h Slurm wall.
> All headline numbers are scored at a **matched epoch 50**, which every arm
> except `p16` reached.

## 1. The result

Paired against the same-seed `fourier`/`fourier` control, best val_l2 within
epoch <= 50:

| arm | per-seed deltas | mean | sd |
| --- | --- | ---: | ---: |
| `fno_fmix` (frequency mixing) | -0.0001, -0.0003, -0.0036 | -0.0013 | 0.0019 |
| `fmix_fmix` | +0.0004, +0.0009, -0.0026 | -0.0004 | 0.0019 |
| **`lap p2`** | -0.0049, -0.0047, -0.0073 | **-0.0056** | 0.0015 |
| **`lap p4`** | -0.0052, -0.0047, -0.0072 | **-0.0057** | 0.0013 |
| **`lap p8`** | -0.0056, -0.0041, -0.0073 | **-0.0057** | 0.0016 |

Against the 2-D replicate floor of sd **0.0002-0.0009**
([[Learned Waveform Basis Operator]] §2) this is roughly **6x the floor**, with
**every seed of every Laplace arm negative**. Contrast the mixing arms, whose
means are driven by seed 2 alone and whose signs are mixed.

`p16` never reached epoch 50 (wall at 43). Scored at **its own** ceiling of
epoch 43 against the control at the same epoch it is **-0.0045** (sd 0.0021) --
also better, slightly less so.

**The pole budget is not the mechanism.** 2, 4 and 8 poles per axis give
-0.0056, -0.0057, -0.0057 -- differences far smaller than the per-seed spread.
Two poles buys the entire effect; 16 is mildly worse. Whatever this operator is
doing, it is **the pole-residue form itself**, not the resolution of many poles.

## 2. Confirmation on an independent metric family

`val_l2` is neuralop's absolute Lp. Running the trainer's own `final_report`
over the recorded held-out cone split (`viz/compute_final_report.py`) gives
RMSE-family metrics for `lap p4` seed 0, epoch-50 weights:

| metric | `lap p4` | control | change |
| --- | ---: | ---: | ---: |
| val_rmse | **0.1446** | 0.1741 | **-17%** |
| test_rmse | **0.1497** | 0.1789 | **-16%** |
| test_gradient_rmse | 0.1019 | 0.1038 | -2% |
| test_mean_xhi_mae | **0.0198** | 0.0254 | **-22%** |
| test_high_k_cross_correlation | 0.7115 | 0.7081 | +0.5% |
| test_high_k_power_ratio | 0.4956 | 0.5381 | *see §4* |

Same direction, large margin, different metric family, computed by the training
code rather than by an analysis script.

## 3. Where the error actually is

![[lap_p4_representative_slices.png]]

Bubble **positions and topology are right** -- every major ionized region in the
truth appears in the prediction, in the right place. The error panels are near
white in bubble interiors and in neutral gas, with structure confined to **thin
rings at every bubble wall**: red/blue dipoles, the signature of a displaced or
over-smoothed edge rather than a misplaced bubble. Interiors do not reach full
ionization; bubbles are soft dark blobs where the truth has hard-edged voids.

This is the campaign's standing [[Hedging Bias of Pointwise Losses]], not
something new to this operator -- but it is what the remaining error consists of.

## 4. Power spectrum -- and a metric that needs resolving

![[lap_p4_ps_coherence.png]]

| | `lap p4` | control |
| --- | ---: | ---: |
| $r(k \ge 0.2)$ | **0.7375** | 0.7303 |
| high-k power ratio (active slices) | **1.535** | 1.062 |

Coherence is marginally better. The power ratio says Laplace **overshoots**
small-scale power by 53% where the control is within 6% of unity -- the reverse
of the campaign's usual under-production, and consistent with §3: soft walls
with the wrong profile shape put power in roughly the right places.

> **Unresolved.** This high-k ratio (1.535 vs 1.062, ideal 1.0) and
> `test_high_k_power_ratio` in §2 (0.496 vs 0.538, ideal 1.0) **disagree in
> sign** about which model is closer to the truth. They normalize differently.
> Neither should be quoted until that is settled.

## 5. Boundary-band edge metrics

![[lap_p4_edge_band_overlay.png]]

547 contributing cones, 3960 held-out slices, 2-D transverse `mode="slice"`:

| metric | `lap p4` | control |
| --- | ---: | ---: |
| total squared error | **1.728e6** | 2.447e6 |
| L2 within 2 Mpc of a front | **0.2739** | 0.2893 |
| L2 within 5 Mpc | **0.2100** | 0.2298 |
| H1 within 2 Mpc | 0.1757 | 0.1758 |
| error fraction within 5 Mpc | 0.815 | 0.785 |

Total squared error is **29% lower**. The gain is broad rather than
wall-specific: L2 improves by only 5-9% in the near-front bands and the H1
(gradient) bands are identical to 4 decimals, while the **error fraction inside
5 Mpc is higher** for Laplace (0.815 vs 0.785). Laplace reduces error mostly
away from fronts and concentrates what remains at the walls.

**Front width is not usable here.** `front_width` needs the mean predicted
profile to cross both the 0.1 and 0.9 levels; the control's never does, so it
returns NaN -- a direct expression of hedging bias, not a bug. Laplace does span
those levels (hence a finite 31.35 Mpc against a 2.74 Mpc truth) but the value
sits at the edge of the +/-30 Mpc window and is not a calibrated width. The
qualitative statement -- Laplace reaches the extremes, the control does not --
is what this supports.

## 6. Cost

Median epoch train time, seed 0:

| arm | s/epoch | vs control |
| --- | ---: | ---: |
| `fno_fno` | 147.8 | 1.0x |
| `lap p4` | 394.8 | 2.7x |
| `lap p8` | 459.5 | 3.1x |
| `lap p2` | 476.7 | 3.2x |
| `lap p16` | 606.1 | 4.1x |

**These are not clean measurements**: `p2` should be the cheapest arm and
measures as the second most expensive, so node contention dominates the
ordering. What is safe to say is that Laplace costs roughly **3-4x** a Fourier
epoch. A per-channel Python loop in `_steady_field` (one iteration per channel,
small kernels) is the obvious suspect and is an implementation cost, not
intrinsic to the method. **Worth optimizing before the 3-D follow-up.**

## 7. What this establishes, and what it does not

1. **A real, reproducible gain.** ~6x the replicate floor, every seed of every
   arm, confirmed on a second metric family, at a matched budget.
2. **The pole budget is irrelevant between 2 and 8.** The cheapest configuration
   is as good as any.
3. **The mechanism is unexplained, and it contradicts the stated motivation.**
   LNO's pole-residue form is built for non-periodic signals and transient
   responses. 2-D $x_\text{HI}$ slices have **no time-like axis** -- both axes
   are transverse and periodic. The reason to try it here was that it is a basis
   [[Learned Waveform Basis Operator]] could not reach, not that its physics
   applied. It works anyway. Until we know why, this is an empirical result.
4. **It is not a front-sharpness fix.** §3 and §5 agree that the residual error
   is still concentrated at bubble walls, and the gradient metrics barely move.

## Caveats

- **No run completed its budget.** All Laplace jobs hit the 8 h wall; the
  100-epoch numbers do not exist. Since best-val is a running minimum,
  truncation can only understate the arms -- but it also means the matched-epoch
  comparison is the only defensible one.
- **§2-§5 use epoch-50 weights, not best.** The run's best was epoch 63
  (val_l2 0.1025 vs 0.1040). Periodic checkpoints land every 25 epochs and the
  run died at 66, so no later weights exist. Every diagnostic is therefore of a
  model 0.0015 worse than the arm's own best.
- Three seeds per arm; the diagnostics in §2-§5 are **seed 0 only**.
- The two high-k power metrics disagree (§4).

## Open

- **Why does it work?** The transient term is the part with no 2-D motivation.
  An ablation that zeroes it, leaving only the steady-state term, would say
  whether the gain is the pole-residue response or merely the extra
  parameterization.
- **3-D $x_\text{HI}$**, where the LOS axis is a genuine non-periodic ramp and
  [[LOS Bandwidth as the 3-D Bottleneck]] locates the spectral headroom. This is
  where the method's own claim can finally be tested.
- **Optimize `_steady_field`** before that: 3-4x per epoch is the binding
  constraint on a 3-D run.
- Re-run the diagnostics on best-epoch weights, which requires best-checkpoint
  saving rather than periodic-only.
- Reconcile the two high-k power-ratio definitions.
