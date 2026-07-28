---
type: paper
title: "Pérez Cuadrado et al 2025 (WHNO)"
created: 2026-07-24
updated: 2026-07-24
tags:
  - domain/ml
  - domain/operator-learning
  - architecture/whno
  - architecture/fno
  - concept/discontinuities
  - concept/gibbs
status: summarized
domain: "Inference and ML"
aliases:
  - WHNO
  - "Walsh-Hadamard Neural Operator"
  - "Pérez Cuadrado 2025"
  - "Walsh-Hadamard Neural Operators for Solving PDEs with Discontinuous Coefficients"
related:
  - "[[Walsh-Hadamard Neural Operator]]"
  - "[[Fourier Neural Operator]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Square-Wave Basis for Ionization Fields]]"
  - "[[Wavelet Neural Operator]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
authors: "M. Pérez Cuadrado et al."
year: 2025
venue: "arXiv:2511.07347 → J. Comp. Phys. (2026)"
---

# Pérez Cuadrado et al 2025 (WHNO)

> **One line:** Replace the FNO's Fourier transform with the **Walsh–Hadamard transform** — a global basis of rectangular (±1) step waves — so that discontinuous, piecewise-constant fields are represented without Gibbs ringing, at identical $O(n\log n)$ cost. Headline: a one-scalar **WHNO + FNO ensemble** strictly beats either alone on every configuration tested.

## Coordinates

- arXiv:2511.07347 (Nov 2025); published in *Journal of Computational Physics* (2026), S0021999126004766.
- The square-wave-basis idea I sketched (2026-07-24) is essentially this paper. Filed here as prior art + a live basis-side attack for the lightcone program.

## The problem it targets

Spectral neural operators expand fields in a fixed basis and learn weights on the low-order coefficients. The [[Fourier Neural Operator]] uses sines/cosines. Smooth trigonometric bases represent **discontinuities** poorly: a truncated Fourier expansion of a step function oscillates (Gibbs phenomenon), so sharp interfaces get blurred and ringing appears — exactly the [[SirenFNO Spectral Bias Investigation|low-frequency-collapse]] / bubble-wall failure mode measured across the lightcone experiments.

## Method

Same architecture skeleton as FNO, one substitution — the transform $\mathcal{F}$:

$$
v^{(l+1)}(\mathbf{x})=\sigma\!\Big(W^{(l)}v^{(l)}(\mathbf{x})+\mathcal{H}^{-1}\big[\,\mathcal{P}_k\,\mathcal{W}\,\odot\,\mathcal{H}[v^{(l)}]\,\big](\mathbf{x})\Big)
$$

where $\mathcal{H}$ is the **Walsh–Hadamard transform** (fast WHT, $O(n\log n)$), $\mathcal{P}_k$ truncates to the lowest-$k$ **sequency** coefficients (the square-wave analog of "lowest wavenumbers"), and $\mathcal{W}$ is a learnable channel-mixing weight applied per retained sequency.

Key properties they invoke:

- **Rectangular basis** — Walsh functions take values $\pm1$; naturally suited to **piecewise-constant** fields (their coefficients decay rapidly, so aggressive truncation is cheap and lossless-ish).
- **No Gibbs** — step edges are represented without oscillatory overshoot.
- **Cost = FFT** — the fast WHT is $O(n\log n)$, and the butterfly uses only additions/subtractions (no complex multiplies, no trig tables) → same asymptotics, smaller constant, real-valued throughout.
- **One knob** — truncation cutoff $k$, structurally identical to FNO's mode count.

## Results

- **Heat conduction, discontinuous conductivity:** WHNO MAE 0.0153 vs FNO 0.0166 (100 test samples), lower $H^1$ too.
- **2D Burgers, discontinuous ICs:** WHNO MAE 0.0064 vs FNO 0.0084, lower $H^1$.
- **Error geometry:** FNO error concentrates *at* the discontinuities (Gibbs-like); WHNO error spreads evenly across the domain — the same signature the boundary-band diagnostic looks for in [[Windowed Local-FNO U-Net Findings]].
- **Ensemble is the real headline:** train WHNO and FNO independently, fit one scalar $w^\*\in[0,1]$ on held-out data to minimise $\mathbb{E}[(w\,u_\text{WHNO}+(1-w)\,u_\text{FNO}-u_\text{true})^2]$. Result: **strictly lower** test MSE **and** $H^1$ than either single model on **all seven** (problem, geometry/IC) configurations. $w^\*=0.572\pm0.016$ (heat), $0.648\pm0.020$ (Burgers) — both keep a non-trivial FNO contribution. Doubles inference cost, no extra training.

## WHNO vs the wavelet operator (their controlled experiment)

This is the part most relevant to the "why not wavelets" question. They run a **single-level Haar** [[Wavelet Neural Operator|WNO]] (Haar = the local, multiscale cousin of Walsh; both are built from rectangular steps) at matched $k=32$, identical encoder/decoder, identical params (1,555,153):

- **Local Haar wins on heat conduction** (−15% to −27% MAE): the solution is determined *locally* by the conductivity neighbourhood → short wavelet support suffices.
- **Global Walsh wins on Burgers** (Haar +27% to +67% MAE): after 500 advection steps the solution depends on IC information from a *growing radius*; the **global support** of Walsh encodes that long-range dependence in low-sequency coefficients that a single-scale local wavelet has no mechanism to express.

Structural point they stress: WNO carries free knobs (wavelet family, #levels, boundary handling, filter length) whose right setting depends on unknown target regularity; WHT has **none** — one canonical basis, one cutoff.

## Why it matters for this thesis

Every basis-side attack so far ([[Windowed Local-FNO U-Net Findings|Local-FNO]], [[SirenFNO Spectral Bias Investigation|SirenFNO]]) stayed inside the **Fourier** basis and failed to beat the U-FNO floor. WHNO is the first attack that **changes the basis to a step-function basis** — which is what the near-binary $x_\text{HI}$ field with sharp bubble walls actually is. See [[Walsh-Hadamard Neural Operator]] for the concept and [[Square-Wave Basis for Ionization Fields]] for the proposed 3-D lightcone experiment and the caveats (dyadic-convolution / translation-equivariance, grid-axis anisotropy).

## Caveats to carry forward

- Demonstrated only on **2D** toy PDEs; **3D + realistic microstructure** is named as open in their future work — precisely the untouched niche.
- Pointwise multiply in the Walsh domain = **dyadic (XOR) convolution** in real space, i.e. equivariant to dyadic shifts, **not** ordinary translations — a genuine wrinkle for statistically homogeneous/isotropic cosmological fields. See [[Square-Wave Basis for Ionization Fields]].

## Sources

- [Walsh-Hadamard Neural Operators for Solving PDEs with Discontinuous Coefficients — arXiv:2511.07347](https://arxiv.org/abs/2511.07347)
- [Published version, J. Comp. Phys.](https://www.sciencedirect.com/science/article/pii/S0021999126004766)
- Related: [Shearlet Neural Operator — arXiv:2604.25181](https://arxiv.org/abs/2604.25181) (directional/anisotropic-edge basis; third comparison point)
