---
type: concept
title: "Structured Transform Neural Operators"
created: 2026-07-28
updated: 2026-07-28
tags:
  - domain/ml
  - domain/operator-learning
  - architecture/wno
  - architecture/whno
  - concept/basis-choice
status: developing
complexity: advanced
domain: Inference and ML
aliases:
  - WNO
  - Wavelet Neural Operator
  - Walsh-Hadamard Neural Operator
  - WHNO
related:
  - "[[Fourier Neural Operator]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Structured-Transform Operator Findings]]"
  - "[[Hedged Edges vs Blurred Edges]]"
  - "[[Windowed Local-FNO U-Net Plan]]"
sources:
  - "[[.raw/reports/FINDINGS-2026-07-26.md]]"
---

# Structured Transform Neural Operators

Generalization of the [[Fourier Neural Operator]] in which the fixed FFT is replaced by any fast orthogonal transform. The operator block is unchanged in form — **transform → learned per-coefficient weight → inverse transform** — only the basis changes. This makes basis choice a *hyperparameter slot* rather than an architectural commitment.

## The families in use

| basis | transform | truncation | why it might suit ionization fields |
|---|---|---|---|
| **Fourier** | truncated rFFT over signed quadrants | `n_modes` per axis | smooth global structure; the baseline |
| **Wavelet (WNO)** | multilevel orthonormal **Haar** | all bands retained; depth = `LEVELS` | Haar atoms *are* step functions — a sharp bubble wall is sparse in this basis, unlike in Fourier where it needs all frequencies (Gibbs) |
| **Walsh–Hadamard (WHNO)** | Walsh–Hadamard in **sequency order** | truncate to lowest sequencies | square-wave basis: piecewise-constant fields are sparse; $O(N\log N)$, no complex arithmetic, power-of-two sizes only |
| **SIREN-Fourier** | rFFT with SIREN-generated per-mode weights | none (all modes) | removes the low-frequency weight collapse — see [[SirenFNO Spectral Bias Investigation]] |
| **CNN** | (identity; real-space convolution) | — | the U-FNO's local path, isolated as an operator |

**Sequency vs natural ordering** is the Walsh–Hadamard analogue of "keep the low modes": sequency order sorts basis functions by number of sign changes, so truncation is smoothest-first; natural (Kronecker / bit-reversed) order truncates arbitrarily. Measured difference on the 2-D $x_\text{HI}$ task is small (0.1520 vs 0.1533 RMSE).

## The two slots

In the windowed U-Net skeleton of [[Windowed Local-FNO U-Net Plan]] there are two independent places to put an operator:

- the **local slot** — the four overlap-add windowed encoder/decoder branches;
- the **global slot** — the two whole-field bottleneck blocks.

Naming them separately is what turned "which basis is best" into a testable question. The empirical answer on 21 cm slices is that **the global whole-field bottleneck is where a non-Fourier operator pays off, not the windowed local branches** — see [[Structured-Transform Operator Findings]].

## Engineering constraints the skeleton absorbs

- **Rank projection.** Spectral operators run inside a $1\times1$ projection down to a low channel rank and back; a CNN does not (a rank bottleneck would only throttle a convolution), so it runs at full width.
- **Windowing.** A CNN in the local slot defaults to whole-field operation — a convolution is already local, and windowing its input only modulates the signal it sees.
- **Padding.** The global slot's shape is data-dependent ($35\times35\times64$ on production cubes), so the block pads to what the operator accepts and crops back — *circular* on the periodic transverse axes, *replicate* on the finite line of sight. This is what lets a power-of-two-only Walsh–Hadamard transform run whole-volume.

Implementation: `operators.py` registry in the `fno-21cm` repo; `MODEL_KIND=localop` with `LOCAL_OPERATOR` / `GLOBAL_OPERATOR` pairs the slots freely, with the named kinds (`localfno`, `localwno`, `localwhno`, `localsirenfno`) as shorthands for fixed pairs.
