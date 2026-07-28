---
type: concept
title: "Walsh-Hadamard Neural Operator"
created: 2026-07-24
updated: 2026-07-27
tags:
  - concept/ml
  - domain/inference
  - domain/operator-learning
  - architecture/whno
status: active
complexity: advanced
domain: "[[Inference and ML]]"
aliases:
  - "WHNO"
  - "Walsh Neural Operator"
  - "Walsh-Hadamard transform"
related:
  - "[[Fourier Neural Operator]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Wavelet Neural Operator]]"
  - "[[Ionization Morphology]]"
  - "[[Square-Wave Basis for Ionization Fields]]"
  - "[[Loss Objective and Operator Basis Sweep]]"
  - "[[Hedging Bias of Pointwise Losses]]"
sources:
  - "[[Pérez Cuadrado et al 2025 (WHNO)]]"
  - "wiki/thesis/notes/FINDINGS-2026-07-26.md §2 (first 2-D results)"
---

# Walsh-Hadamard Neural Operator

## Definition

A neural operator identical in structure to the [[Fourier Neural Operator]] but with the Fourier transform replaced by the **Walsh–Hadamard transform (WHT)** — a complete orthonormal basis of **rectangular ($\pm1$) step waves** indexed by *sequency* (the square-wave analog of frequency) — so that discontinuous, piecewise-constant fields are represented without Gibbs ringing.

## Physical Intuition

The FNO expands a field in smooth sinusoids. To represent a **sharp edge** with sinusoids you need infinitely many modes, and any truncation overshoots and rings (Gibbs). The ionization field is the pathological case: near-binary $x_\text{HI}$ with sharp bubble walls (see [[Ionization Morphology]]) — closer to a segmentation mask than a smooth field.

Walsh functions are themselves **step functions**, so a step edge is a *natural, sparse* object in this basis rather than a hard one. Crucially, unlike wavelets, the Walsh basis has **global support** (like Fourier): each basis function spans the whole domain but is square-shaped. That combination — global reach + square shape — is the "best of both" intuition:

- Fourier: global, smooth → good global statistics, blurs edges.
- Wavelets: local, step-like → sharp edges, but short support can't encode long-range / large-scale dependence (this is the late-z-only limitation).
- **Walsh: global, step-like** → sharp edges *and* long-range coupling.

## Mathematical Form

One WHNO layer, differing from the FNO layer only in the transform $\mathcal{H}$:

$$
v^{(l+1)}(\mathbf{x})=\sigma\!\Big(W^{(l)}v^{(l)}(\mathbf{x})+\mathcal{H}^{-1}\big[\,\mathcal{P}_k\big(\mathcal{W}^{(l)}\odot\mathcal{H}[v^{(l)}]\big)\big](\mathbf{x})\Big)
$$

where:
- $\mathcal{H}$ — the (fast) Walsh–Hadamard transform, $O(n\log n)$;
- $\mathcal{H}[v^{(l)}]$ — Walsh coefficients, ordered by **sequency** (number of sign changes);
- $\mathcal{P}_k$ — truncation to the lowest-$k$ sequencies (analog of the FNO mode cutoff, see [[Spectral Mode Cutoff in FNOs]]);
- $\mathcal{W}^{(l)}$ — learnable per-sequency channel-mixing weights;
- $W^{(l)}v^{(l)}$ — the pointwise local bypass, exactly as in FNO.

The WHT can be written as repeated application of the $2\times2$ Hadamard matrix $H_2=\begin{psmallmatrix}1&1\\1&-1\end{psmallmatrix}$ via a Cooley–Tukey-style butterfly — **additions and subtractions only**, no complex multiplies, no trig.

## Why It Matters for This Thesis

The entire lightcone-regeneration program is a fight against **Gibbs-type bubble-wall blurring** in FNO/U-FNO ([[FNO Lightcone Experimental Findings]], [[SirenFNO Spectral Bias Investigation]]). Every attack tried so far stayed inside the Fourier basis:

- [[Windowed Local-FNO U-Net Findings|Local-FNO]] — apply Fourier in small windows (still Gibbs within each window).
- [[SirenFNO Spectral Bias Investigation|SirenFNO]] — learn a weight for every Fourier mode (removes low-mode collapse, still sinusoidal).
- [[Smooth-Target Reparametrization Plan|smooth-target]] — sidestep the discontinuity by learning a smooth surrogate ($z_\text{re}$).

WHNO is the **missing basis-side move**: change the basis functions themselves from sinusoids to step functions, matched to what $x_\text{HI}$ is. It is cheap (same $O(n\log n)$, no trig), single-knob, and drops into the existing FNO code with one transform swap. The proposed experiment and its caveats live in [[Square-Wave Basis for Ionization Fields]].

## Key subtleties (do not skip)

1. **Convolution theorem breaks.** FNO's physical justification is that pointwise multiply in Fourier space = a **translation-equivariant** global convolution (a learned Green's-function filter), which suits statistically homogeneous fields. Pointwise multiply in the Walsh domain corresponds instead to **dyadic (bitwise-XOR) convolution** — equivariant to dyadic shifts, *not* ordinary translation. For a field whose statistics are translation/rotation invariant this is a real theoretical wrinkle; may surface as grid-aligned/blocky artifacts. Empirical question, not necessarily fatal.
2. **Anisotropy.** Multi-D Walsh is a tensor product with grid-preferred axes; bubble walls are curved and isotropic. The **Shearlet Neural Operator** (directional, multiscale) is the natural third comparison for curved edges.
3. **Ensemble, not replacement.** The source paper's strongest result is not WHNO-alone but a one-scalar **WHNO + FNO ensemble** beating both — mirrors the thesis pattern that no single basis has won outright.

## First results on 21 cm data (2026-07-26)

Tested on the **2-D $x_\text{HI}$ slice task** inside the Local-FNO U-Net, where the operator can occupy either the *windowed local* branches, the *global* whole-field bottleneck, or both. Six configs varied slot, local mode count (6 vs 12), width (32 vs 48) and coefficient ordering (sequency vs natural). Full tables in [[Loss Objective and Operator Basis Sweep]].

| config | val RMSE | vs Local-FNO |
|---|---|---|
| `localop(fourier/hadamard)` — **global slot only** | **0.1453** | **−2.3%** |
| `localop(hadamard/hadamard)` — both slots | 0.1501 | +0.9% |
| Local-FNO (all-Fourier reference) | 0.1487 | – |
| `localop(hadamard/fourier)` — local slot only | 0.1515–0.1533 | +1.9…+3.1% |
| U-FNO | 0.1595 | +7.3% |

Three things this establishes:

1. **The Walsh basis does buy something real** — global-slot WHNO is the first run to beat plain Local-FNO on this task, and beats U-FNO by ~9%.
2. **Where it goes matters more than which basis it is.** Moving the operator from local-only to global-only changed the result by ~5%, more than any other knob in the sweep; sequency vs natural ordering changed it by <1%. Combined with LocalWNO (wavelet-local, Fourier-global) landing merely *level* with Local-FNO, the pattern across **both** structured-transform families is that **the global whole-field bottleneck is where a non-Fourier operator pays off** — not the windowed local branches. This is the opposite of the naive "step basis for sharp local walls" intuition in the section above, and refines the source paper's global-vs-local-support framing.
3. **It does not dissolve the front-width problem.** WHNO's own predictions are still 2–4× too wide, because that defect is set by the objective, not the basis — see [[Hedging Bias of Pointwise Losses]]. `whno_glob` was in fact the *base model* for the [[Contrast Map Sharpening]] experiments.

Still untested: 3-D, $z_\text{re}$, the FNO+WHNO ensemble, and the shift-consistency check for the dyadic-convolution caveat below. Tracked in [[Square-Wave Basis for Ionization Fields]].

## Connections

- Drop-in variant of: [[Fourier Neural Operator]]
- Shares the truncation knob with: [[Spectral Mode Cutoff in FNOs]]
- Local step-basis cousin: [[Wavelet Neural Operator]] (Haar) — global vs local support is the decisive difference
- Target it suits: [[Ionization Morphology]] (near-binary field, sharp bubble walls)
- Complements/contrasts the Fourier-basis attacks: [[SirenFNO Spectral Bias Investigation]], [[Windowed Local-FNO U-Net Findings]]
- Alternative to the target-side attack: [[Smooth-Target Reparametrization Plan]]

## Sources

- [[Pérez Cuadrado et al 2025 (WHNO)]] — arXiv:2511.07347 / J. Comp. Phys. 2026
