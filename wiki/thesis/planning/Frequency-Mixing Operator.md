---
type: plan
title: "Frequency-Mixing Operator"
created: 2026-09-14
updated: 2026-09-14
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - architecture/fno
  - concept/basis-choice
  - concept/spectral-truncation
  - concept/architecture
status: active
related:
  - "[[Laplace Neural Operator Port]]"
  - "[[Learned Waveform Basis Operator]]"
  - "[[3-D Operator Matrix Final Results]]"
  - "[[Structured-Transform Operator Findings]]"
sources:
  - "`fno-21cm` branch `codex/frequency-mixing-transform`, commit 153798a"
  - "`spectral_mixing_operator.py`, `notes/frequency-mixing.md`, `notes/PLAN-frequency-mixing-transform.md`"
  - "`tests/test_frequency_mixing.py`, `util/frequency_mixing_checkpoint.py`, `viz/frequency_mixing.py`"
  - "jobs 4921861-4921869 (2-D, 3 conditions x 3 seeds, in flight 2026-09-14)"
---

# Frequency-Mixing Operator

> **No results yet.** The runs below were queued 2026-09-14 and are at epoch ~11
> of 100. This page records the method, the verification, and the
> pre-registered expectations. Results will move to a finding page.

A plain FNO spectral layer is **diagonal in frequency**: mode $k$ of the output
depends only on mode $k$ of the input. Every operator in
[[3-D Operator Matrix Final Results]] shares that restriction, differing only in
*which* basis is diagonalized. This operator breaks it.

## Method

$$ y = \text{FourierMultiplier}(x) + U A_\theta P_\theta U^\top x $$

The first term is the existing signed-quadrant Fourier multiplier, computed with
FFTs. The second is a **cross-frequency residual**: $U^\top$ takes real Fourier
coefficients, $P_\theta$ and $A_\theta$ are factors emitted by two small MLPs
over the *mode coordinates*, and $U$ synthesizes back. Every retained
coefficient can therefore affect every other, including DC.

The factors are generated once per block forward and shared across the batch.
This is **linear mixing, not attention** — nothing is conditioned on the input.
Physical-space nonlinearity stays in the surrounding blocks.

Three backends: `factorized` (production), `dense` (a full learned matrix, for
small-grid correctness studies) and `pairwise` (generates that matrix from both
coefficients' coordinates). The latter two cost quadratically in modes and exist
as references.

## The property that makes the experiment clean

**The synthesis network's final layer is zero-initialized, so at step 0 the
operator is exactly a plain FNO.** Verified rather than assumed, in float64:

| check | result |
| --- | --- |
| `max abs(mixing - fourier)` at init | **0.000e+00** |
| residual Frobenius norm at init | **0.0** |
| after perturbing synthesis | 1.2e-01 |
| gradients reach analysis / synthesis nets | 2.6e+00 / 1.9e+00 |

A mixing run and a Fourier control started from the same seed are therefore the
*same function* at step 0. The paired contrast carries no initialization noise —
a better-controlled comparison than anything else in the campaign, where arms
normally differ from the first step.

## Mode convention — a real trap

`N_MODES_*` keeps the **signed-quadrant FNO cutoff** convention, *not* a count of
real columns as in `learned_waveform`. For cutoffs $(m_x,m_y)$ the residual
retains $(2m_x+1,\ 2m_y-1)$ real columns in 2-D, and each must fit its axis
excluding the even-grid Nyquist bin. Our 2-D settings:

| slot | grid | modes | real columns | fits |
| --- | --- | --- | --- | --- |
| global bottleneck | 35x35 | 16x16 | 33 x 31 | yes |
| local window | 16x16 | 6x6 | 13 x 11 | yes |

Invalid shapes fail explicitly rather than silently truncating.

## Cost, measured

Steady-state epoch train time on one A100, 2-D task, batch 32:

| condition | s / epoch | vs control |
| --- | ---: | ---: |
| `fourier` / `fourier` (control) | 149 | — |
| `fourier` / `frequency_mixing` | 152 | **+2%** |
| `frequency_mixing` / `frequency_mixing` | 181 | **+22%** |

Mixing at the bottleneck is nearly free. In the windowed local branch it costs
22%, because factors are regenerated per block forward and reused only across
that block's patch chunks — the same window-loop cost that dominates elsewhere
([[Learned Waveform Basis Operator]] §4, [[3-D Operator Matrix Final Results]] §2.1).

## Configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| `FREQUENCY_MIXING_BACKEND` | `factorized` | `dense`/`pairwise` are small references |
| `FREQUENCY_MIXING_RANK` | 32 | Rank of the additional coefficient mapping |
| `FREQUENCY_MIXING_HIDDEN_DIM` | 64 | Coordinate-network width |
| `FREQUENCY_MIXING_CHUNK_SIZE` | 1024 | Coordinate generation chunk |
| `FREQUENCY_MIXING_DENSE_LIMIT` | 4e6 | Cap on requested dense matrix entries |

Operator tag `fmix`. Legacy Fourier checkpoints must be migrated explicitly with
`util.frequency_mixing_checkpoint`; `load_checkpoint` **rejects** a partial match
rather than leaving the new multiplier random.

## Experiment in flight

3 conditions x 3 seeds, 100 epochs, batch 32, lr 3e-4, `GRID_EMBEDDING=1`,
rank 32, hidden 64. Jobs 4921861-4921869.

| condition | local / global |
| --- | --- |
| `fno_fno` | fourier / fourier — **the control** |
| `fno_fmix` | fourier / frequency_mixing |
| `fmix_fmix` | frequency_mixing / frequency_mixing |

The control had to be run: **no `fourier`/`fourier` 2-D run existed** at these
settings. Three seeds because the 2-D replicate floor is sd 0.0002-0.0009 in
val_l2 ([[Learned Waveform Basis Operator]] §2) and four consecutive
architecture tests on this task have come back null inside it.

## What would count as a result

- **Clearing the floor.** A paired mean below about $-0.001$ val_l2 against
  `fno_fno`. Anything smaller is not distinguishable from seed noise.
- **The prior is not favourable.** [[Learned Waveform Basis Operator]] showed
  that given freedom over the *basis*, this task converges to Fourier and gains
  nothing. Frequency mixing attacks a different axis — coupling *between* modes
  rather than the choice of modes — so it is not refuted by that result, but the
  task has so far rewarded no added spectral machinery.
- If `fmix_fmix` beats `fno_fmix`, the local branch matters and the 22% is worth
  paying; if they tie, bottleneck-only placement is the recommendation.

## Caveats to carry into the write-up

- **The rank-32 latent is global.** Every output coefficient is an affine
  function of the same 32 scalars, summarizing all 1023 modes x 16 channels =
  16,368 coefficients. "Every coefficient can affect every other" is true but
  routed through a far tighter bottleneck than it suggests. If the result is a
  null, **rank is the first thing to sweep**, not the conclusion.
- **Full mixing breaks translation equivariance**, transverse included. No axis
  restriction is applied silently. For a periodic transverse box this is a real
  loss of inductive bias, and it is not obviously the right trade.
- Mixing cannot recover dependence on frequencies the analysis step discarded;
  identity mixing is projection onto the retained subspace.
- The profiling in `notes/frequency-mixing.md` is small-CPU, not GPU throughput.
  The per-epoch numbers above are ours, measured on the actual A100 runs.
