---
type: meta
title: Wiki Index
updated: 2026-06-06
---

# Wiki Index

## Domains

- [[21cm Cosmology]] — Signal physics, brightness temperature, HERA/SKA observational context
- [[Reionization Physics]] — EoR history, bubble morphology, ionization sources and sinks
- [[Effective Field Theory]] — Bias expansion, perturbation theory, EFT operators and coefficients
- [[Simulation and Codes]] — 21cmFAST, SCRIPT, THESAN, radiative transfer codes
- [[Inference and ML]] — SBI, neural networks, EoRFlow, SKATR, parameter estimation pipelines
- [[Thesis Work]] — Research log, methodology, P1/P2 tasks, timeline, deliverables

## Papers

### Reionization Physics (Background)
- [[Choudhury 2022 (Reionization Intro)]] — Pedagogical review; halo mass functions, photon budget, global reionization equation; **foundational background**
- [[Ferrara & Pandolfi (IGM Reionization)]] — Two-lecture overview; IGM physics, Lyman-alpha forest, GP effect, ionization topology
- [[Mesinger 2016]] — EoR review book (ed. Mesinger); Furlanetto ch. 9 = 21cm pedagogy

### Reionization Simulations (Background)
- [[Trac & Gnedin 2009 (Reionization Simulations)]] — Review of RT simulation methods; RT algorithm taxonomy; sources vs sinks
- [[Gnedin & Madau 2022 (Modeling Reionization)]] — Comprehensive code taxonomy; 21cmFAST, ARTIST, ASTRAEUS, fully coupled RT; **the field map**
- [[Mesinger et al 2010 (21cmFAST)]] — Original 21cmFAST paper; FFRT excursion-set ionization; Zel'dovich density; ~10% PS agreement with full RT; **code foundation**

### EFT Theory (Thesis-Core)
- [[McQuinn & D'Aloisio 2018]] — EFT bias expansion for 21cm; Minimal Model; P_err/P₂₁ < 10%; **foundational**
- [[Qin et al 2022 (EFT Redshift Space)]] — RSD extension; renormalized coefficients; THESAN validation; k ≲ 0.8 h/Mpc
- [[Sailer et al 2022 (Optical Depth EFT)]] — τ forecasts from perturbative 21cm; large-scale EFT + CMB lensing
- [[Baradaran et al 2024 (Hybrid EFT)]] — hybrid EFT: N-body density + EFT ionization painting; best accuracy

### Simulator Dependence (Core Problem)
- [[Berklas & Pober 2025]] — MCMC model dependence within 21cmFAST; biased posteriors from internal model variation
- [[Sooknunan et al 2024 (ML Reproducibility)]] — systematic ML reproducibility failures across simulators; networks learn code-specific features
- [[Zhou & La Plante 2022 (CNN Reionization)]] — CNN failure 21cmFAST→zreion; canonical cross-code demonstration
- [[Solt et al 2026 (Multi-Simulator Training)]] — multi-simulator training mitigates but doesn't solve; **empirical baseline for P2**

### SBI Pipelines & ML Methods
- [[Pietschke et al 2025 (EoRFlow)]] — EoRFlow SBI; $x_\text{HI}(z)$ from 2DPS; SKA-Low validated
- [[Pietschke et al 2026 (cross-correlation)]] — EoRFlow + 21cm×galaxy; constrains $f_\text{esc}$, $f_*$
- [[Ore et al 2025 (SKATR)]] — SKATR self-supervised ViT; **cross-simulator generalization**
- [[Schosser et al 2025 (Starobinsky)]] — SKA+CMB joint SBI; Starobinsky inflation constraints
- [[Duruisseaux et al 2026 (FNO)]] — FNO guide; resolution-invariant operator learning
- [[Deistler et al 2025 (SBI Guide)]] — Comprehensive SBI methods tutorial; NPE/NLE/NRE workflow; diagnostics (SBC, TARP); **methods reference for P2**

### Neural Operator Architectures
- [[Lu et al 2020 (DeepONet)]] — DeepONet; branch-trunk architecture; universal approximation theorem for operators; arbitrary output locations; high-order convergence
- [[Rahman et al 2023 (U-NO)]] — U-shaped Neural Operator; encoder-decoder with skip connections; 3D spatiotemporal native; 26–44% better than FNO on PDE benchmarks; memory-efficient via domain contraction
- [[Staddon 2026 (Isotropic FNO)]] — radially-binned spectral kernel $R(|\mathbf{k}|)$; SO(d)-equivariant FNO; ~16x (2D) / ~96x (3D) parameter reduction; right symmetry for the comoving real-space surrogate

### 21 cm Forecasts & Reionization (recent arXiv digest, May 2026)
- [[Worku et al 2026 (PMFs 21cm Forecasts)]] — `zeus21` extended with primordial magnetic field contribution to $P_\text{lin}(k)$; HERA/SKA forecasts; example of modular new-physics priors on the forward model
- [[Wang & Shan 2026 (JWST Reionization Degeneracy)]] — $f_\text{esc} \times f_{\star,0}$ degeneracy of global reionization observables; JWST UV LF *shape* breaks it; "early-galaxy crisis" excluded at 4.5σ; relevant to what 21 cm alone can constrain
- [[Byrne et al 2026 (Digital Whitening Systematic)]] — instrumentation; digital whitening + re-quantization induces a frequency-dependent gain distortion not removed by bandpass calibration; forecast-realism caveat

### Thesis Documents
- [[Thesis Proposal (EFT of Ionization Field)]] — Supervisor's project proposal; defines P1 + P2; EFT coefficients as simulator-independent inference targets; **thesis foundation document**

## Entities

### People
- [[McQuinn, Matthew]] — UW; foundational EFT paper
- [[D'Aloisio, Anson]] — UC Riverside; foundational EFT paper
- [[Heneka, Caroline]] — Heidelberg ITP; EoRFlow + SKATR group
- [[Pietschke, Yannic]] — Heidelberg/Vienna; EoRFlow lead
- [[Ore, Ayodele]] — Heidelberg; SKATR lead
- [[Schosser, Benedikt]] — Heidelberg ARI; Starobinsky SBI
- [[Mesinger, Andrei]] — SNS Pisa; 21cmFAST developer; book editor
- [[Mason, Charlotte]] — SCRIPT developer
- [[Qin, Yuxiang]] — Qin et al. 2022; EFT on THESAN
- [[Pober, Jonathan C.]] — Brown; Berklas & Pober 2025 + Solt et al. 2026; simulator dependence expert
- [[Sailer, Neha]] — Berkeley; Sailer et al. 2022 + Baradaran et al. 2024; EFT forecasting
- [[Pritchard, Jonathan R.]] — Imperial; Sooknunan et al. 2024; 21cm community leader

### Codes & Tools
- [[py21cmfast]] — primary simulation code
- [[SCRIPT]] — second code for P1
- [[EoRFlow]] — Heidelberg SBI pipeline
- [[SKATR]] — self-supervised ViT; cross-simulator generalization
- [[swyft]] — TMNRE SBI framework for P2
- [[THESAN]] — RT hydrodynamical simulation suite
- [[powerbox]] — power spectrum utilities

### Telescopes & Experiments
- [[HERA]] — primary near-future 21cm array
- [[SKA]] — next-generation; full imaging capability
- [[LOFAR]] — current upper limits
- [[MWA]] — Australian precursor

## Planning Notes

- [[P1 EFT Characterization]] — Step-by-step P1 plan: EFT coefficient extraction across 21cmFAST and BEoRN
- [[P2 Cross-Simulator Inference]] — P2 plan: EFT-targeted SBI; cross-simulator posterior comparison
- [[FNO Approach for 21cm Emulation]] — FNO/U-NO emulation of $T_b$ and $x_\text{HI}$; EFT–FNO connection; suggested timeline

## Findings

- [[FNO Lightcone Experimental Findings]] — 3-D FNO $\delta_m \to x_\text{HI}$ on full lightcones (4× H200 DDP, 6600 cones). **Breakthrough**: 11-param astrophysical conditioning drops val L² 0.20 → 0.06 and recovers bubble morphology. **Negative findings**: modes 16 → 24 and BCE regulariser both ineffective — the ceiling is input information, not capacity or loss formulation.

## Concepts

### EFT / Theory
- [[Bias Expansion]], [[Stochastic Term]], [[Renormalization]], [[Regime of Validity]]
- [[Matter Overdensity Field]], [[Linear Growth Factor]]

### Reionization
- [[Neutral Fraction]], [[Ionization Morphology]], [[Bubble Size Distribution]]
- [[Mean Free Path]], [[Spin Temperature]], [[Excursion Set Formalism]], [[Clumping Factor]]

### Signal / Observation
- [[Power Spectrum as Summary Statistic]], [[2D Power Spectrum]], [[Cross-Power Spectrum]]
- [[Lyman Alpha Forest]], [[Foreground Wedge]], [[Redshift Space Distortions]]

### Inference / ML
- [[Simulation-Based Inference]], [[Neural Posterior Estimation]], [[Simulator Dependence]]
- [[Cross-Simulator Generalization]], [[Self-Supervised Learning]]
- [[Vision Transformer]], [[Fourier Neural Operator]], [[FiLM Conditioning]]
- [[Training Set Generation]], [[Initial Conditions]]

### Concepts
- [[Simulator Dependence]] — **NEW** — now has a full concept note with evidence chain and mitigation map

## Sources

*(full catalog in wiki/sources/ — 24 papers ingested)*

## Comparisons

*(populate as needed — suggested: EoRFlow vs SKATR vs P2 on simulator dependence)*

## Questions

*(populate as questions are filed)*

## Gaps

- Has EoRFlow been tested cross-simulator? (motivates P2)
- Does SKATR's cross-simulator generalization extend to coefficient-level interpretability?
- Which second simulator (SCRIPT vs SimFast21) for P1?
- How to match ICs between 21cmFAST and SCRIPT?
- Do EFT coefficients stay stable when 21cmFAST *internal* model is varied (per Berklas & Pober 2025)?
- What exactly are the simulator-specific morphological features that ML networks learn (per Sooknunan et al.)?
