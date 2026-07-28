---
type: gap
title: "Square-Wave Basis for Ionization Fields"
created: 2026-07-24
updated: 2026-07-27
tags:
  - gap/open-question
  - gap/thesis-opportunity
  - gap/partially-answered
  - domain/operator-learning
status: partially-answered
domain: "[[Inference and ML]]"
related:
  - "[[Walsh-Hadamard Neural Operator]]"
  - "[[Pérez Cuadrado et al 2025 (WHNO)]]"
  - "[[Fourier Neural Operator]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[Ionization Morphology]]"
---

# Square-Wave Basis for Ionization Fields

## The question

Does a **step-function spectral basis** (Walsh–Hadamard) reconstruct the $x_\text{HI}$ bubble walls better than the sinusoidal FNO/U-FNO — and does a **WHNO + FNO ensemble** beat the U-FNO floor on the 3-D density → $x_\text{HI}$ lightcone map?

Origin: idea raised 2026-07-24; turns out to be almost exactly [[Pérez Cuadrado et al 2025 (WHNO)]], but demonstrated only on 2D toy PDEs. **3-D + realistic microstructure is named as open in their own future work.** Nobody has applied a Walsh/square-wave operator to 3-D ionization fields or 21 cm.

## Why it's promising here

- The whole lightcone program is a fight against **Gibbs-type bubble-wall blurring** ([[FNO Lightcone Experimental Findings]], [[SirenFNO Spectral Bias Investigation]]). $x_\text{HI}$ is near-binary with sharp walls — a piecewise-constant target, the ideal case for a rectangular basis.
- Every basis-side attack so far ([[Windowed Local-FNO U-Net Findings|Local-FNO]], [[SirenFNO Spectral Bias Investigation|SirenFNO]]) stayed **inside the Fourier basis** and did not beat the U-FNO floor. WHNO is the untried move: change the basis functions to step functions.
- Cheap and low-risk: fast WHT is $O(n\log n)$ with **no complex multiplies / no trig**; one cutoff knob; a one-transform swap in the existing FNO code. The FNO+WHNO ensemble needs no retraining — one cross-validated scalar $w^\*$.
- EFT synergy: the near-binary/step structure is the same feature the [[Bias Expansion]] treats as the ionization field; a basis matched to it is ideologically consistent with P1.

## Proposed experiment (minimal)

1. Swap $\mathcal{F}\to\mathcal{H}$ (fast WHT) in the existing 3-D FNO; truncate by sequency at matched $k$; matched params vs the U-FNO benchmark.
2. Evaluate in the **existing boundary-band + $P(k)$/$r(k)$ high-$k$** framework: 10–90% front width vs U-FNO (10.7 / truth 3.6 Mpc), boundary $H^1$, parity/hedging bias in nearly-ionized bins.
3. Fit the one-scalar **FNO + WHNO ensemble** on held-out cones; report whether it clears the U-FNO floor (test L² 0.0418 / H¹ 8.27).

## Risks / caveats to test (not assume)

- **Translation equivariance broken.** Walsh-domain pointwise multiply = **dyadic (XOR) convolution**, equivariant to dyadic shifts, not ordinary translation. Cosmological fields are statistically translation/rotation invariant → possible grid-aligned/blocky artifacts. This is the main theoretical objection; measure it (shift-consistency test), don't presume it fatal.
- **Anisotropy.** Tensor-product Walsh has preferred grid axes; bubble walls are curved/isotropic. Third comparison point: **Shearlet Neural Operator** (arXiv:2604.25181), a directional multiscale basis.
- **Local vs global.** The source paper's Haar-WNO control shows local step bases win on *locally determined* solutions, global Walsh wins on *long-range-dependent* ones. The lightcone has both (local walls + large-scale bubble topology) → this is exactly why the ensemble, not a single basis, may be the answer.

## Status — partially answered (2026-07-26)

**Run in 2-D, not yet in 3-D.** Six WHNO configs on the 2-D $x_\text{HI}$ slice task ([[Loss Objective and Operator Basis Sweep]], §2):

- ✅ **The basis does buy something.** `localop(fourier/hadamard)` — Walsh in the **global slot only** — reaches val RMSE **0.1453**, the first run to beat plain Local-FNO (0.1487) and ~9% ahead of U-FNO (0.1595).
- ❗ **The premise needs revising.** The gap was filed on the intuition that a step basis suits *sharp local walls*. The data say the opposite: **local-slot** Hadamard consistently *underperforms* Local-FNO (0.151–0.153), and the local→global move is worth ~5%, more than any other knob. LocalWNO (wavelet-local) landing merely level with Local-FNO says the same thing from the other family. **The payoff is in the global whole-field bottleneck.**
- ➖ **Ordering is nearly irrelevant**: sequency vs natural, 0.1520 vs 0.1533 at matched settings.
- ❌ **It does not solve the wall problem.** WHNO predictions are still 2–4× too wide, because the front-width defect is set by the objective, not the basis — see [[Hedging Bias of Pointwise Losses]] and [[Contrast Map Sharpening]]. A basis-side lever was never going to close that gap.

### Still open

1. **Does global-only WHNO transfer to 3-D and to $z_\text{re}$?** Untested. Standing warning: the same sweep retracted an earlier 2-D LocalWNO lead once the z-interpolation handicap on the 3-D baselines was removed — **a 2-D win is not a reliable predictor**.
2. **The FNO+WHNO ensemble** (the source paper's headline result) has not been fitted at all.
3. **The shift-consistency test** for the dyadic-convolution / translation-equivariance caveat has not been run.
4. Evaluation in the **boundary-band + $P(k)$/$r(k)$** framework against the U-FNO floor (0.0397 test RMSE in 3-D) is still pending.
