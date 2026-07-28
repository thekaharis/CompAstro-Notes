---
type: meta
title: Wiki Index
updated: 2026-07-28
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
- [[Shi et al 2025 (SirenFNO)]] — SIREN hypernetwork *generates* the Fourier kernel for all modes (no truncation); constant, resolution-independent parameter count; directly targets the FNO low-frequency bias; CP/TT/Tucker kernel decompositions

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
- [[Siren3D Residual Refinement Plan]] — Frozen-U-FNO + coordinate-conditioned sinusoidal residual head for bubble-wall refinement; boundary sampling, controls, and stop criteria
- [[Windowed Local-FNO U-Net Plan]] — U-FNO with **windowed** spectral mixing (overlapping Hann patches, shifted grids) + one global Fourier bottleneck; a low mode inside a small window = a high effective frequency on the full grid; targets the measured low-frequency collapse at the bubble walls; ~10.2 M params
- [[Smooth-Target Reparametrization Plan]] — stop learning $x_\text{HI}$; learn a **smooth surrogate** (primary: $z_\text{re}(\mathbf{x})$, native 21cmFAST output; secondary: signed distance to front) and reconstruct $x_\text{HI}$ by deterministic thresholding — uncertainty becomes front *displacement* instead of front *blurring*; orthogonal to all basis-side attacks; cheapest remaining lever + best EFT synergy
- [[Lightcone z_re Map Target]] — implementation of the smooth-target plan's candidate 1, modified: per-pixel $z_\text{re}(x,y)$ **fitted from existing lightcones** (Gompertz front / LS step per sightline) instead of the native `z_re_box` — no re-simulation, and the problem becomes 2-D (density LOS slices as channels → $z_\text{re}$ map, NaN pixels masked). Reconstruction sanity: lo-z/optimal step reconstruct global $x_\text{HI}(z)$ at voxel MSE ≈ 0.008–0.05; late reionizers are 79–99% no-front (the sentinel problem is real). **Trained — results in [[z_re Map Training Results]]**
- [[Warped LOS Grid Plan]] — the cube cache's uniform-z LOS grid is **~37 Mpc at low z where the fronts live** (vs ~5 Mpc at saturated high z) — a hard, model-independent bound on wall fidelity. Candidate fix: **warped grid** (sampling density ∝ ensemble-mean $|d\langle x_\text{HI}\rangle/d\chi|$ + floor, CDF-inverted) + envelope/uniform-χ/crop variants; training-free round-trip evaluator with per-timing-class metrics; `build_cubes.py --target-z` + Δχ volume-weighted loss merged. **Evaluated on real cones — results in [[Warped LOS Grid Evaluation]]**

## Findings

- [[FNO Lightcone Experimental Findings]] — 3-D FNO $\delta_m \to x_\text{HI}$ on full lightcones (4× H200 DDP, 6600 cones). **Two breakthroughs**: parameter conditioning drops val L² 0.20 → 0.06; U-FNO + SyncBN reaches **val L² = 0.0418, val H¹ = 8.27**. **Nulls**: more isotropic/LOS modes, BCE, GroupNorm, stronger H¹ weighting, and doubled LOS U-Net receptive field do not improve the relevant architecture's floor. The active bottleneck is not retained mode count or LOS receptive field.
- [[SirenFNO Spectral Bias Investigation]] — new mode-weight diagnostic **measures** the FNO/U-FNO low-frequency collapse (32-mode U-FNO: low 8/32 modes hold 52% of spectral weight). A 3-D **SirenFNO** keeps the learned spectrum flat (no collapse), beats the plain FNO (test L² 0.057→0.050, H¹ 11.6→9.8) but does **not** yet beat the U-FNO floor (0.040) — plausibly because it lacks the local U-Net path. Next: boundary-band/$P(k)$ diagnostics + SirenFNO×U-Net hybrid.
- [[Windowed Local-FNO U-Net Findings]] — first run of the windowed Local-FNO (local modes `(6,6,12)`, 21 epochs, ~10.2 M params). **Negative result on the design hypothesis**: at epoch 20 the boundary diagnostic is *worse* than the U-FNO benchmark — 10–90% front width **32.2 Mpc vs U-FNO 10.7 Mpc** (truth 3.6), higher peak RMSE (0.32 vs 0.28) and gradient error (0.19 vs 0.16) at the wall. Whole-volume (test L² 0.057 / H¹ 10.2) sits at the plain-FNO level, but the run is **undertrained and still descending**. No patch seams. Windowed-Fourier ≠ the U-FNO's real-space conv path for wall sharpness. Next: finish to 70 ep, widen local modes, boundary-aware loss, conv-path hybrid.
- [[z_re Map Training Results]] — 26 runs, 5 architectures, 660 held-out cones on the 2-D $z_\text{re}$ map task. **Pure L² beats L²+H¹ by ~35%** on every architecture (and improves the H¹ metric itself); **SIREN weights take the Local-FNO from worst to second best** (RMSE 0.305 → 0.123, gap 3.0× → 1.2×) with 54× fewer params than the U-FNO; **the nominal loss weights were misleading** — H¹ supplied **99.4%** of the 3-D training loss. Per-branch mode weights say the **LOS axis** is the only place bandwidth still binds. *Caveat: measured in $z_\text{re}$-space; the reconstructed-$x_\text{HI}$ front-width test is still unrun.*
- [[Structured-Transform Operator Findings]] — the operator basis made a slot. Best 2-D $x_\text{HI}$ model is **Walsh–Hadamard in the global bottleneck only** (val RMSE 0.1453 vs LocalFNO 0.1487, U-FNO 0.1595). **Which slot matters more than which basis** (~5% vs ~1%); local models are **20–60× smaller** than the U-FNO at better accuracy. Retracts the earlier inflated LocalWNO-vs-3-D comparison (z-interpolation handicap).
- [[Edge and Wall-Placement Losses]] — four new loss terms attacking front placement. **`ExponentialWallDistance` reaches truth-like front width (1.16 px vs truth 1.46)** where every RMSE-optimal model sits at ~2.9, at ~22% RMSE cost — the first training-time sharpness knob in the campaign. Establishes that H¹ seminorm and H² are **exactly blind** to misplacement (1.00× over 4→48 px) while a signed-distance loss changes 144×.
- [[Contrast Map Investigation]] — **closed, negative, explained.** A learned $(\theta,\tau)$ output remap is a working deblurrer (−9.28% on a purely blurred field) that buys **0.00%** on the model at matched sharpness; given the dial and 30 epochs, gradient descent left it at the identity. One surviving regime: at $\bar{x}_\text{HI} \approx 0.005$–$0.05$ a per-band $\theta$ buys a real held-out 2–9%.
- [[Warped LOS Grid Evaluation]] — real-cone round trip, 926,903 front rays. The production cache recovers only **12.7% of true front sharpness and misses 11.7% of fronts**; `warped_256` gets to 33.2% / 4.9% at the same budget and **beats uniform-$z$ at 512 slices**. Sample placement dominates sample count. Warped-cache training runs exist but are not yet comparable (different target grid).

## Concepts

### EFT / Theory
- [[Bias Expansion]], [[Stochastic Term]], [[Renormalization]], [[Regime of Validity]]
- [[Matter Overdensity Field]], [[Linear Growth Factor]]

### Reionization
- [[Neutral Fraction]], [[Ionization Morphology]], [[Bubble Size Distribution]] ✓
- [[Mean Free Path]], [[Spin Temperature]], [[Excursion Set Formalism]], [[Clumping Factor]]

### Signal / Observation
- [[Power Spectrum as Summary Statistic]], [[2D Power Spectrum]], [[Cross-Power Spectrum]]
- [[Lyman Alpha Forest]], [[Foreground Wedge]], [[Redshift Space Distortions]]

### Inference / ML
- [[Simulation-Based Inference]], [[Neural Posterior Estimation]], [[Simulator Dependence]]
- [[Cross-Simulator Generalization]], [[Self-Supervised Learning]]
- [[Vision Transformer]], [[Fourier Neural Operator]], [[FiLM Conditioning]]
- [[Spectral Mode Cutoff in FNOs]], [[Structured Transform Neural Operators]]
- [[Hedged Edges vs Blurred Edges]], [[Sliced Wasserstein Edge Loss]]
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
