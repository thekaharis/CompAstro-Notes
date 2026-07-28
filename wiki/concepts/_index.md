---
type: meta
title: "Concepts Index"
updated: 2026-07-28
---

# Concepts

## EFT / Theory
- [[Bias Expansion]] — operator expansion of $\delta_x$ in terms of $\delta_m$ and its derivatives
- [[Stochastic Term]] — $P_{\varepsilon\varepsilon}$: residual power after EFT fit; most novel cross-simulator diagnostic
- [[Renormalization]] — UV subtraction in quadratic operator; $\frac{68}{21}\sigma^2_L$ coefficient
- [[Regime of Validity]] — $k$ range where EFT holds; $P_\text{err}/P_{21} < 10\%$ criterion
- [[Matter Overdensity Field]] — $\delta_m = (\rho - \bar{\rho})/\bar{\rho}$; linear $\delta^{(1)}$ vs second-order $\delta^{(2)}$
- [[Linear Growth Factor]] — $D(z)$; amplitude scaling of linear modes

## Reionization
- [[Neutral Fraction]] ✓ — $\bar{x}_\text{HI}(z)$; global history; GP trough saturation; EoRFlow target
- [[Ionization Morphology]] ✓ — inside-out topology; bubble size stages; simulator dependence of morphology
- [[Bubble Size Distribution]] ✓ — characteristic size $R_\text{eff}$; enters $b_{\nabla^2}^x$; measured via transverse periodic mean-free-path rays; U-FNO bubbles run **+6–9% too large** at early stages
- [[Mean Free Path]] ✓ — $R_\text{mfp}$; sets max bubble size in excursion-set; enters $b_{\nabla^2}^x$
- [[Spin Temperature]] ✓ — $T_S$; Wouthuysen-Field coupling; saturated limit assumed in thesis
- [[Excursion Set Formalism]] ✓ — Press-Schechter/Sheth-Tormen; ionized bubble criterion; core of 21cmFAST
- [[Clumping Factor]] ✓ — $C = \langle n^2 \rangle / \langle n \rangle^2$; recombination sink; source of simulator divergence

## Observation / Signal
- [[Power Spectrum as Summary Statistic]] — $P_{21}(k,z)$; spherically averaged; compact SBI input
- [[2D Power Spectrum]] ✓ — $P_{21}(k_\perp, k_\parallel)$; separates sky/LOS modes; enables foreground wedge excision; used by EoRFlow
- [[Cross-Power Spectrum]] ✓ — 21cm $\times$ galaxy; reduces foreground sensitivity; constrains $f_\text{esc}$, $f_*$
- [[Lyman Alpha Forest]] ✓ — GP trough; saturation at $\bar{x}_\text{HI} \sim 10^{-3}$; observational endpoint constraint

## Inference / ML
- [[Simulation-Based Inference]] — likelihood-free inference from (sim, params) pairs
- [[Neural Posterior Estimation]] — normalizing flow learns $P(\theta \mid x)$ directly
- [[Simulator Dependence]] — ML models failing cross-simulator; core problem this thesis addresses
- [[Cross-Simulator Generalization]] — whether EFT targets improve inference portability
- [[Self-Supervised Learning]] ✓ — pre-training without labels; SKATR achieves cross-simulator generalization this way
- [[Vision Transformer]] ✓ — ViT; global attention over patches; outperforms CNN on 21cm data (SKATR, Starobinsky)
- [[Fourier Neural Operator]] ✓ — FNO; learns function-to-function maps in Fourier space; resolution-invariant; potential emulator
- [[Spectral Mode Cutoff in FNOs]] ✓ — `n_modes` limits learned global spectral communication, not the output bandwidth; records the *measured* low-frequency weight collapse and the per-branch result that the **LOS axis is the only place bandwidth still binds**
- [[Structured Transform Neural Operators]] ✓ — the operator basis as a hyperparameter slot: Haar wavelet (WNO), Walsh–Hadamard (WHNO), SIREN-Fourier, CNN; local vs global slot
- [[Hedged Edges vs Blurred Edges]] ✓ — a soft front is either band-limited (fixable by sharpening) or position-hedged (not); the FNO family's deficit is measured to be **hedging**; ~86% of the model error is not blur
- [[Sliced Wasserstein Edge Loss]] ✓ — optimal-transport distance between edge measures; the Wasserstein barycenter of shifted sharp edges is still sharp, so it penalises displacement instead of rewarding it
- [[Training Set Generation]] — ~500 21cmFAST runs for P2 SBI training
- [[Radiative Transfer]] ✓ — three RT algorithm families; moments/MC/ray-tracing; photon conservation
- [[Initial Conditions]] — matched $\delta_m(\mathbf{x})$ grid across codes required for P1

*(✓ = concept file exists)*
