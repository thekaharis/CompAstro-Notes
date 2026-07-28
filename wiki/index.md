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
- [[Pérez Cuadrado et al 2025 (WHNO)]] — replaces Fourier with the **Walsh–Hadamard transform** (global rectangular step-wave basis); no Gibbs on discontinuous fields; same $O(n\log n)$, no trig; **FNO+WHNO ensemble beats either alone** on all 7 configs; the untried step-function basis for bubble walls

### 21 cm Forecasts & Reionization (recent arXiv digest, May 2026)
- [[Worku et al 2026 (PMFs 21cm Forecasts)]] — `zeus21` extended with primordial magnetic field contribution to $P_\text{lin}(k)$; HERA/SKA forecasts; example of modular new-physics priors on the forward model
- [[Wang & Shan 2026 (JWST Reionization Degeneracy)]] — $f_\text{esc} \times f_{\star,0}$ degeneracy of global reionization observables; JWST UV LF *shape* breaks it; "early-galaxy crisis" excluded at 4.5σ; relevant to what 21 cm alone can constrain
- [[Byrne et al 2026 (Digital Whitening Systematic)]] — instrumentation; digital whitening + re-quantization induces a frequency-dependent gain distortion not removed by bandpass calibration; forecast-realism caveat

### Thesis Documents
- [[Thesis Proposal (EFT of Ionization Field)]] — Supervisor's project proposal; defines P1 + P2; EFT coefficients as simulator-independent inference targets; **thesis foundation document**
- [[Chronological Research Report]] — LaTeX report on regenerating 21cmFAST neutral-fraction lightcones from ground-truth density fields, including the FNO/U-FNO, SirenFNO, Local-FNO, smooth-target, and LOS-grid results

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
- [[Lightcone z_re Map Target]] — implementation of the smooth-target plan's candidate 1, modified: per-pixel $z_\text{re}(x,y)$ **fitted from existing lightcones** (Gompertz front / LS step per sightline) instead of the native `z_re_box` — no re-simulation, and the problem becomes 2-D (density LOS slices as channels → $z_\text{re}$ map, NaN pixels masked). Reconstruction sanity: lo-z/optimal step reconstruct global $x_\text{HI}(z)$ at voxel MSE ≈ 0.008–0.05; late reionizers are 79–99% no-front (the sentinel problem is real). **Trained — see [[z_re Map Training Results]] and [[Loss Objective and Operator Basis Sweep]]**
- [[Warped LOS Grid Plan]] — the cube cache's uniform-z LOS grid is **~37 Mpc at low z where the fronts live** (vs ~5 Mpc at saturated high z) — a hard, model-independent bound on wall fidelity. Candidate fix: **warped grid** (sampling density ∝ ensemble-mean $|d\langle x_\text{HI}\rangle/d\chi|$ + floor, CDF-inverted) + envelope/uniform-χ/crop variants; training-free round-trip evaluator with per-timing-class metrics; `build_cubes.py --target-z` + Δχ volume-weighted loss merged. **Evaluated on real cones — see [[Warped LOS Grid Evaluation]]**

## Findings

- [[Loss Objective and Operator Basis Sweep]] — **2026-07-26 consolidated report** across all three tasks. **Pure L² beats L²+H¹ by ~35% on $z_\text{re}$ for every architecture**, and the nominal 0.5/0.5 weights were a fiction: H¹ supplied **99.4%** of the 3-D loss, so every archived "L²+H¹" 3-D run was H¹-dominated. SIREN weights rescue Local-FNO on $z_\text{re}$ (0.305 → 0.123); width saturates at 32; mid-run LR comparisons are unreliable. On 2-D $x_\text{HI}$, **Walsh–Hadamard in the GLOBAL slot only** is the new best model (0.1453 vs Local-FNO 0.1487, U-FNO +9%) — the local/global slot matters more than the basis. U-FNO floor still holds in 3-D (0.0397). Retracts the earlier LocalWNO lead as a z-interpolation artifact.
- [[Edge and Wall-Placement Losses]] — **the constructive answer to the hedging diagnosis, and the first training-time sharpness result in the campaign.** `ExponentialWallDistance` (exponential-in-distance **absolute** error — a conditional *median*, which is binary on a binary field) reaches front width **1.16 px against truth 1.46**, where every RMSE-optimal model sits at ~2.9, for ~22% RMSE and high-$k$ power ratio 0.51 → 0.82. Establishes that H¹ seminorm and H² are **exactly blind** to misplacement (1.00× over 4→48 px) while a signed-distance loss changes 144×. Amends [[Transport-Based Edge Losses]]: SWD was not the winner; *absolute vs squared* is the decisive property. An L² or BCE anchor is not optional.
- [[Warped LOS Grid Evaluation]] — real-cone round trip, 926,903 front rays. The production cache recovers only **12.7% of true front sharpness and misses 11.7% of fronts**; `warped_256` reaches 33.2% / 4.9% at the same budget and **beats uniform-$z$ at 512 slices** — sample placement dominates sample count. `crop15_chi_256` nearly ties it with no ensemble-derived warp. Warped-cache training runs exist but are **not yet comparable** (different target grid).
- [[z_re Map Training Results]] — detailed companion to [[Loss Objective and Operator Basis Sweep]]: the 26-run per-model table, the Local-SirenFNO sweep conclusions, both training-failure root causes, the z_re infrastructure, and the **per-branch mode-weight diagnostic showing the LOS axis is the only place bandwidth still binds** (edge/peak 0.60–0.78 vs 0.03–0.20 transverse).
- [[Structured-Transform Operator Findings]] — detailed companion on the operator side: the **29-run shared-slice leaderboard** with `width`/`blur` columns against a TRUTH row, the local/global slot sweep, and the A30 benchmark — local models are **20–60× smaller than the U-FNO** at better accuracy and ~40% less peak memory, WHNO costs ~5% throughput, local-slot wavelet ~53%.
- [[Contrast Map Sharpening]] — **closed, negative.** Two-parameter $(\theta,\tau)$ output reshaping to recover edge sharpness. Post-hoc: a real **6.2% oracle gain** that is **unrealizable** because τ is unpredictable from anything available at inference ($R^2\approx0$ even given z + 11 cosmological params). End-to-end: given a free differentiable sharpening dial, **gradient descent left it at the identity** (θ 4.75 → 4.43, ~130× less than truth-matched sharpness). Also documents a reusable zero-init/weight-decay collapse pathology and a highK+contrast instability.
- [[FNO Lightcone Experimental Findings]] — 3-D FNO $\delta_m \to x_\text{HI}$ on full lightcones (4× H200 DDP, 6600 cones). **Two breakthroughs**: parameter conditioning drops val L² 0.20 → 0.06; U-FNO + SyncBN reaches **val L² = 0.0418, val H¹ = 8.27**. **Nulls**: more isotropic/LOS modes, BCE, GroupNorm, stronger H¹ weighting, and doubled LOS U-Net receptive field do not improve the relevant architecture's floor. The active bottleneck is not retained mode count or LOS receptive field.
- [[SirenFNO Spectral Bias Investigation]] — new mode-weight diagnostic **measures** the FNO/U-FNO low-frequency collapse (32-mode U-FNO: low 8/32 modes hold 52% of spectral weight). A 3-D **SirenFNO** keeps the learned spectrum flat (no collapse), beats the plain FNO (test L² 0.057→0.050, H¹ 11.6→9.8) but does **not** yet beat the U-FNO floor (0.040) — plausibly because it lacks the local U-Net path. Next: boundary-band/$P(k)$ diagnostics + SirenFNO×U-Net hybrid.
- [[Windowed Local-FNO U-Net Findings]] — first run of the windowed Local-FNO (local modes `(6,6,12)`, 21 epochs, ~10.2 M params). **Negative result on the design hypothesis**: at epoch 20 the boundary diagnostic is *worse* than the U-FNO benchmark — 10–90% front width **32.2 Mpc vs U-FNO 10.7 Mpc** (truth 3.6), higher peak RMSE (0.32 vs 0.28) and gradient error (0.19 vs 0.16) at the wall. Whole-volume (test L² 0.057 / H¹ 10.2) sits at the plain-FNO level, but the run is **undertrained and still descending**. No patch seams. Windowed-Fourier ≠ the U-FNO's real-space conv path for wall sharpness. **Update (ep 38)**: front width 18.5 vs U-FNO 13.9 Mpc, boundary-H¹ margin shrank ~8× but U-FNO still significantly ahead; ionized-wall loss experiment failed; new parity diagnostic shows the hedging bias (+0.17/+0.21 in nearly-ionized bins) is common to both architectures → target-side attacks now prioritized.

## Concepts

### EFT / Theory
- [[Bias Expansion]], [[Stochastic Term]], [[Renormalization]], [[Regime of Validity]]
- [[Matter Overdensity Field]], [[Linear Growth Factor]]

### Reionization
- [[Neutral Fraction]], [[Ionization Morphology]], [[Bubble Size Distribution]] ✓ — **NEW note** — mean-free-path estimator; U-FNO bubbles run **+6–9% too large** at early stages
- [[Mean Free Path]], [[Spin Temperature]], [[Excursion Set Formalism]], [[Clumping Factor]]

### Signal / Observation
- [[Power Spectrum as Summary Statistic]], [[2D Power Spectrum]], [[Cross-Power Spectrum]]
- [[Lyman Alpha Forest]], [[Foreground Wedge]], [[Redshift Space Distortions]]

### Inference / ML
- [[Simulation-Based Inference]], [[Neural Posterior Estimation]], [[Simulator Dependence]]
- [[Cross-Simulator Generalization]], [[Self-Supervised Learning]]
- [[Vision Transformer]], [[Fourier Neural Operator]], [[FiLM Conditioning]]
- [[Spectral Mode Cutoff in FNOs]], [[Structured Transform Neural Operators]], [[Walsh-Hadamard Neural Operator]]
- [[Training Set Generation]], [[Initial Conditions]]

### Loss Design / Boundary Sharpness
- [[Hedging Bias of Pointwise Losses]] — **NEW** — why L² (and H¹ one derivative up) provably prefer blurred fronts; the mechanism behind every front-width null
- [[Contrast Map]] — **NEW** — the $(\theta,\tau)$ monotonic output reshaping; definition, why the affine renormalisation is load-bearing, and its closed-negative status
- [[Sliced Wasserstein Edge Loss]] — **NEW** — optimal-transport distance between unit-mass edge measures; the Wasserstein barycenter of shifted sharp edges is still sharp, so it penalises *displacement* instead of rewarding *steepness*

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
- [[Square-Wave Basis for Ionization Fields]] — **partially answered (2026-07-26)**: global-slot WHNO is the new 2-D $x_\text{HI}$ leader, but the premise was wrong (the payoff is in the *global* bottleneck, not the local walls) and it does not fix front width. 3-D, $z_\text{re}$, the FNO+WHNO ensemble and the shift-consistency test remain open
- [[Transport-Based Edge Losses]] — **NEW, high priority**: can a transport metric (SWD) recover wall sharpness by penalising *misplaced* edges rather than rewarding *steep* ones? The last loss-side lever standing; SWD is the only edge term costing <1.2% L²
- [[LOS Bandwidth as the 3-D Bottleneck]] — **NEW**: mode-weight diagnostics put the binding truncation on the LOS axis (edge/peak 0.60–0.78 vs 0.03–0.20 transverse), with headroom in both knobs — untestable from the 2-D $z_\text{re}$ sweep and so far untested
