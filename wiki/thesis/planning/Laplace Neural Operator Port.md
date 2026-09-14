---
type: plan
title: "Laplace Neural Operator Port"
created: 2026-09-14
updated: 2026-09-14
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - architecture/fno
  - concept/basis-choice
  - concept/discontinuities
  - concept/sharp-fronts
  - concept/architecture
status: active
related:
  - "[[Frequency-Mixing Operator]]"
  - "[[Learned Waveform Basis Operator]]"
  - "[[LOS Bandwidth as the 3-D Bottleneck]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[3-D Operator Matrix Final Results]]"
sources:
  - "Cao, Goswami & Karniadakis 2023, *Laplace Neural Operator for Solving Differential Equations*, [arXiv:2303.10528](https://arxiv.org/abs/2303.10528)"
  - "`github.com/qianyingcao/Laplace-Neural-Operator`, cloned to `/pfs/10/work/hd_id260-fno_training/LNO`"
  - "`fno-21cm`: `laplace_operator.py`, `tests/check_laplace_equivalence.py`, registry entry in `operators.py`"
  - "jobs 4922105-4922110 (2-D, 2 pole counts x 3 seeds, queued 2026-09-14)"
---

# Laplace Neural Operator Port

> **No results yet.** Queued 2026-09-14 behind the
> [[Frequency-Mixing Operator]] batch. This page records the port, the
> verification, and what the test can and cannot show.

LNO replaces the Fourier multiplier with a **pole-residue** response: learned
poles and residues give a transient term plus a steady-state term, which lets it
represent **non-periodic signals and transients** that a truncated Fourier basis
handles badly. That is the reason to care here — the ionization front is a
non-periodic ramp, and front sharpness has been the campaign's standing defect
([[Hedging Bias of Pointwise Losses]], [[3-D Operator Matrix Final Results]] §4).

It is also the one basis that [[Learned Waveform Basis Operator]] could *not*
have found: that search was over dilations and phase shifts of a mother
waveform, which cannot produce a decaying exponential.

## Why the reference code could not simply be run

`PR2d.output_PR` materializes tensors of shape $(N\ldots, C, C, M\ldots)$ and
$(C, C, M\ldots, N\ldots)$ — $O(C^2 \prod M \prod N)$. The mode count
**multiplies** the grid rather than truncating it, and channels enter
quadratically, so the FNO spectral saving never happens.

| case | width | poles | grid | live memory |
| --- | ---: | ---: | ---: | ---: |
| their published `2D_Diffusion` | 16 | 4x4 | 50x50 | 0.23 GB |
| ours at their operator size | 16 | 4x4 | 140x140 | 1.8 GB |
| ours at our modes | 16 | 16x16 | 140x140 | 28.7 GB |
| **ours at our width + modes** | **32** | **16x16** | **140x140** | **115 GB** |

Forward only, complex64, before autograd saves, batch 1, one layer. Their README
notes the 2-D/3-D datasets were too big to upload, which fits: this code is
built for 50x50-class problems.

## The fix

Both tensors are **outer products over the mode axes**, so the pole sums can be
taken *before* the grid contraction and neither ever needs to exist. Per axis
$a$, with $\lambda_a$ the DFT frequencies:

$$ A_a[o,i,k,p] = \frac{1}{\lambda_a[o] - \text{pole}_a[i,k,p]}, \qquad
G[i,k,o\ldots] = \sum_{p\ldots} \text{residue}[i,k,p\ldots] \prod_a A_a[o_a,i,k,p_a] $$

contracting one axis at a time and chunking the output channel. Cost falls to
$O(C^2 \max(\prod N, \prod M))$. Measured at our 2-D size: **1 GB peak where the
reference needs 115 GB**; bottleneck forward 147 ms (4 poles) / 402 ms (16 poles)
on CPU.

## Verification — it is LNO, not something LNO-shaped

`tests/check_laplace_equivalence.py` transcribes `PR2d` **literally**, including
its index pairing (`output_residue2`'s output-channel axis contracts against the
poles' *input*-channel axis), evaluates it densely at sizes where its tensors
fit, and compares against our factorized operator.

| $C$ | poles | grid | relative error |
| ---: | --- | --- | ---: |
| 3 | 2x2 | 6x6 | **3.0e-16** |
| 4 | 3x2 | 8x5 | **6.3e-16** |
| 2 | 4x4 | 7x9 | **4.9e-16** |

Machine precision. Channel chunking is bit-identical; the 3-D path runs with
finite gradients on every parameter.

> Two precision traps surfaced here, both of which silently degrade results:
> `Module.double()` leaves **complex** parameters untouched (they are not
> `is_floating_point()`), and `torch.fft.fftfreq` returns **float32** by default,
> which capped the whole operator at single precision until the frequency vector
> was made to follow the parameter dtype.

## Two deliberate differences from the published code

1. **`modes` counts poles per axis, not a spectral cutoff.** Nothing is
   truncated — every DFT frequency reaches the output through $A_a$. Reusing
   `N_MODES=16` therefore means *256 poles per channel pair*, not a 16-mode
   band limit. Poles carry no grid size, so the operator is resolution-flexible.
2. **`stable_poles=True` by default**, mapping poles to $-|\mathrm{Re}| + i\,\mathrm{Im}$.
   The reference leaves the real part free, so $\exp(\text{pole}\cdot t)$ can
   grow; on a normalized domain with their initialization it stays bounded, but
   nothing stops training pushing it positive. `stable_poles=False` reproduces
   the published parameterization and is what the equivalence check uses.

Operator tag `lap`. Configuration: `LAPLACE_POLE_COUNT`, `LAPLACE_STABLE_POLES`,
`LAPLACE_CHANNEL_CHUNK`.

## Experiment in flight

`fourier` local / `laplace` global — bottleneck placement, as with frequency
mixing. 2 pole counts x 3 seeds, 100 epochs, batch 32, lr 3e-4,
`GRID_EMBEDDING=1`. Jobs 4922105-4922110.

| arm | poles | operator params |
| --- | ---: | ---: |
| `fno_lap` p4 | 4x4 | 49,152 |
| `fno_lap` p16 | 16x16 | 589,824 |

At 16 poles the operator is **smaller** than the Fourier global slot it replaces
(1,048,576 params), so capacity is not confounding the comparison. The control
is the `fno_fno` arm of the [[Frequency-Mixing Operator]] batch — same settings,
same seeds, so the contrast is paired.

## What this test can and cannot show

- **The 2-D task has no time-like axis.** LNO's transient term is built around
  $\exp(\text{pole}\cdot t)$ along a coordinate, and its published wins are on
  ODEs and transient PDE responses. On $x_\text{HI}$ slices both axes are
  transverse and periodic. This batch asks whether LNO is *competitive at all*
  on our target and whether the port trains stably — it is **not** a fair test of
  the method's actual claim.
- **The real target is the LOS axis of the 3-D task**, where the front is a
  genuine non-periodic ramp and where
  [[LOS Bandwidth as the 3-D Bottleneck]] locates the spectral headroom. If 2-D
  is merely neutral, that is still a reason to run 3-D rather than to stop.
- A null on 2-D would be the *fifth* consecutive architecture null on this task
  inside the replicate floor, which at some point is itself the finding: 2-D
  $x_\text{HI}$ may simply be saturated at this budget.
