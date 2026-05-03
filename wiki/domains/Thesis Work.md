---
type: domain
title: "Thesis Work"
created: 2026-04-14
updated: 2026-04-16
tags:
  - domain/thesis
  - domain/planning
status: mature
related:
  - "[[Effective Field Theory]]"
  - "[[Simulation and Codes]]"
  - "[[Inference and ML]]"
  - "[[Simulator Dependence]]"
---

# Thesis Work

## Overview and Motivation

This master's thesis addresses a fundamental problem in 21 cm cosmology: **how to perform parameter inference when different reionization simulators produce different morphologies at the same global reionization history**, and when ML models trained on one code fail catastrophically on another.

The formal thesis proposal is archived at [[Thesis Proposal (EFT of Ionization Field)]].

The core insight is that the **Effective Field Theory (EFT) of the ionization field** provides a simulator-independent language for describing reionization. Different codes are different UV completions of the same EFT; they agree on the operator basis but disagree on coefficient values. By targeting **EFT coefficients** as inference observables instead of native simulator parameters ($\zeta$, $T_\text{vir}$), we expect to achieve cross-simulator generalization where standard approaches fail.

### Why This Matters

**Practical motivation:**
- Real SKA/HERA data will not come from any single simulator
- Any inference pipeline that learns simulator-specific features will fail on real data
- Current approaches (multi-simulator training, self-supervised learning) work empirically but lack physical grounding
- EFT provides a principled, physics-motivated solution

**Scientific motivation:**
- Understanding reionization (sources, feedback, topology) requires unbiased parameter inference
- Astrophysical parameters ($\zeta$, $T_\text{vir}$, $R_\text{mfp}$) set the ionizing photon budget and thus the star formation history at $z \sim 6$-$20$
- Precision constraints on these parameters require removing systematic biases from simulator dependence

**Methodological motivation:**
- Demonstrates that EFT is not just a theoretical tool, but a practical framework for unifying simulations
- Shows that physics-informed parameterizations (bias expansion) outperform purely data-driven alternatives for cross-simulator problems
- Opens new avenue for high-$z$ cosmology where theory-simulation mismatches are rampant

## Status and Context

**Program:** Master's in Computational Astrophysics (6 months)  
**Supervisor:** [Provided project proposal: EFT_of_ionization_fields_v2.pdf]  
**Phase:** Topic finalization and literature orientation  
**Background completed:** Reading of Choudhury 2022, Ferrara & Pandolfi, Trac & Gnedin 2009, Gnedin & Madau 2022

## The Two Work Packages

### P1: EFT Characterization of the Ionization Field (Core Deliverable)

**Objective:** Measure and validate the EFT description of $x_\text{HII}$ across ≥2 simulation codes; map regime of validity; quantify simulator variation in EFT space.

#### Detailed Steps

1. **Infrastructure Setup (~2 weeks)**
   - Get 21cmFAST and SCRIPT running on cluster
   - Verify both codes produce expected outputs for standard test cases
   - Implement matched initial condition pipeline: export density field $\delta_m(\mathbf{x}, z)$ from 21cmFAST, import into SCRIPT
   - Test: confirm both codes produce identical $\bar{x}_\text{HII}(z)$ for matched ICs at identical astrophysical parameters
   - Tools: `py21cmfast`, SCRIPT, Python (`numpy`, `scipy`, custom glue code)

2. **EFT Coefficient Extraction (~4 weeks)**
   - Design parameter grid: $\zeta \in [10, 40]$, $T_\text{vir} \in [10^4, 5 \times 10^4]$ K, $R_\text{mfp} \in [10, 50]$ Mpc
   - Run 21cmFAST and SCRIPT at ~30-40 points on this grid (matched ICs)
   - For each (simulation, parameters) pair:
     - Compute the matter power spectrum $P_{mm}(k, z)$ from the density field
     - Compute the 21 cm power spectrum $P_{21}(k, z)$ from the simulation
     - Compute the ionization contrast $\delta_x = x_\text{HII} - \bar{x}_\text{HII}$
     - Fit the bias expansion $\delta_x(\mathbf{k}) = b_1^x \delta_m(\mathbf{k}) + \frac{b_2^x}{2} [\delta_m^2](\mathbf{k}) + b_{\nabla^2}^x (-k^2) \delta_m(\mathbf{k}) + \varepsilon(\mathbf{k})$ in Fourier space
     - Extract coefficients $\{b_1^x, b_2^x, b_{\nabla^2}^x\}$ via weighted least-squares regression in Fourier space
   - Tools: `powerbox` (power spectrum computation), `numpy.linalg.lstsq` (linear regression)
   - **Output:** Tables of $\{b_1^x(z), b_2^x(z), b_{\nabla^2}^x(z)\}$ for both codes across redshifts and parameters

3. **Stochastic Term Analysis (~2 weeks)**
   - After fitting the bias expansion, the residuals give the stochastic term $\varepsilon(\mathbf{k})$
   - Compute the stochastic power spectrum $P_{\varepsilon\varepsilon}(k, z)$ from residuals
   - Analyze scaling: is it scale-independent (white noise / shot noise)? Or power-law? How does it evolve with redshift?
   - Compare stochastic spectra between 21cmFAST and SCRIPT: do they differ? How much?
   - **Output:** Stochastic power evolution and code comparison plots

4. **Regime of Validity Analysis (~2 weeks)**
   - For each code and each (parameter, redshift) combination, compute $P_\text{err} / P_{21}$ as function of $k$
   - Find the $k_\text{max}(z)$ where error first exceeds 10% (standard choice)
   - Plot contours of regime validity in redshift-parameter space
   - **Output:** Maps of $k_\text{max}(z)$ for 21cmFAST vs. SCRIPT; demonstrates where EFT breaks down

5. **Interpretation: Coefficient Trajectories (~2 weeks)**
   - Plot $\{b_1^x(z), b_2^x(z), b_{\nabla^2}^x(z)\}$ evolution across reionization history for both codes
   - Compare trajectories: where do they agree? Where do they diverge?
   - Hypothesis: $b_1^x$ and $b_2^x$ should be more similar (both depend on source bias and global history), while $b_{\nabla^2}^x$ should differ more (depends on detailed bubble morphology)
   - Connect differences back to code-specific choices: Does SCRIPT's use of CLF lead to different $R_\text{eff}$ and thus different $b_{\nabla^2}^x$?
   - **Output:** Physical interpretation of simulator differences in EFT language

#### Expected Results

Based on McQuinn & D'Aloisio 2018 (which validated EFT on RT codes):
- **Large scales:** $b_1^x$ and $b_2^x$ should agree between codes to within ~10-20% (both controlled by large-scale physics)
- **Intermediate scales:** $b_{\nabla^2}^x$ should differ by ~20-50% between codes (depends on bubble morphology details)
- **Stochastic term:** $P_{\varepsilon\varepsilon}$ should show largest code dependence (discrete bubble shot noise is implementation-specific)
- **Regime of validity:** EFT should be valid to $k \sim 0.2-0.5 h/\text{Mpc}$ for both codes (typical bubble scale)

#### Timeline

- Weeks 1-2: Infrastructure, matched ICs
- Weeks 3-6: Simulation generation, coefficient extraction
- Weeks 7-8: Stochastic analysis, regime mapping
- Weeks 9-10: Interpretation and writeup

**Total: ~4-5 months**

### P2: EFT-Informed Cross-Simulator Inference (Stretch Goal / Secondary Focus)

**Objective:** Test whether inference targeting EFT coefficients generalizes better across simulators than native-parameter inference, demonstrating the practical value of the EFT framework.

#### Detailed Steps

1. **Build the Mapping: Parameters → EFT Coefficients (~2 weeks)**
   - Use P1 results to train a **mapping function** from astrophysical parameters $(\zeta, T_\text{vir}, R_\text{mfp})$ to EFT coefficients $\{b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon}\}$
   - Method: 
     - Use the ~30-40 P1 simulations as training data
     - Fit polynomial interpolators or neural network emulators to the coefficient data
     - Test: verify that mapping reproduces P1 coefficients at all sampled points
   - **Output:** Python function `eft_coeffs = f_map(zeta, T_vir, R_mfp, z)`

2. **Generate Large Training Set (~3 weeks)**
   - Run 21cmFAST at ~500 diverse parameter combinations to generate training set for SBI
   - Cover parameter ranges: $\zeta \in [10, 40]$, $T_\text{vir} \in [10^4, 5 \times 10^4]$ K, $R_\text{mfp} \in [10, 50]$ Mpc
   - For each simulation:
     - Extract EFT coefficients (using the mapping from step 1)
     - Compute summary statistics: 1D power spectrum $P_{21}(k_i, z_j)$ or 2D power spectrum
   - **Output:** Dataset $\{(\mathbf{s}_i, \mathbf{b}_i)\}$ where $\mathbf{s}_i$ is summary stats and $\mathbf{b}_i = [b_1^x, b_2^x, b_{\nabla^2}^x, \ldots]$ are EFT coefficients
   - **Computational cost:** ~500 × 5 sec = 40 min on cluster (extremely fast)

3. **Train Inference Models (~2 weeks)**
   - **Model A (Baseline):** Train TMNRE/swyft on native parameters $(\zeta, T_\text{vir}, R_\text{mfp})$ from power spectrum summaries
   - **Model B (EFT-informed):** Train TMNRE/swyft on EFT coefficients from power spectrum summaries
   - For each model:
     - Use swyft package (Python; standard in cosmology)
     - Architecture: masked autoregressive flow (MAF) density model
     - Training: 100 GPU-hours per model (feasible on university cluster with 1 A100)
   - **Output:** Two trained neural networks

4. **Test Cross-Simulator Generalization (~1-2 weeks)**
   - Generate a **test set** from SCRIPT (not seen during training):
     - Run SCRIPT at ~50 test parameter combinations (matched ICs to ensure fair comparison)
     - Compute same summary statistics
   - For each test case:
     - Apply Model A (baseline) → infer $(\zeta, T_\text{vir}, R_\text{mfp})$ on SCRIPT data
     - Apply Model B (EFT) → infer $\{b_1^x, b_2^x, b_{\nabla^2}^x\}$ on SCRIPT data, then use mapping to infer $(\zeta, T_\text{vir}, R_\text{mfp})$
   - Compute metrics:
     - **R² (coefficient of determination):** How well do inferred parameters match true values?
     - **Bias:** $\mathbb{E}[\hat{\theta} - \theta]$ — systematic error in inferred parameters
     - **Coverage:** What fraction of true parameters fall within 68% credible interval?
   - **Expected result (hypothesis):** Model B should achieve R² > 0.70-0.75 cross-simulator, vs. Model A at R² ~ 0.40-0.50

5. **Detailed Analysis of Failures and Successes (~1-2 weeks)**
   - For which parameter combinations does Model B outperform Model A? Identify patterns.
   - Are there specific EFT coefficients (e.g., $b_{\nabla^2}^x$) that are harder to generalize?
   - Does the failure come from the EFT coefficient extraction, or from the inference model?
   - Comparison to baseline: [[Solt et al 2026 (Multi-Simulator Training)]] achieves ~R² = 0.60-0.70 on $\Delta z$ targets; our goal is to achieve similar or better with physical targets.

#### Expected Computational Requirements

- **Simulation generation:** ~8 GPU-hours total (500 runs × 10 sec each = 1.4 hours CPU, scaled for cluster overhead)
- **Neural network training:** ~200 GPU-hours total (100 per model on 1 A100)
- **Testing and analysis:** ~10 GPU-hours

**Total: ~200-300 GPU-hours**

At typical cluster rates (~10 A100s running 8 hours/day), this is doable in 2-3 days of cluster time. Realistic timeline: 4-5 weeks for the full P2 pipeline.

#### Timeline

- Weeks 1-2: Build parameter → EFT mapping (using P1 results)
- Weeks 3-4: Generate training set (21cmFAST + EFT coefficients)
- Weeks 5-6: Train baseline and EFT inference models
- Weeks 7-8: SCRIPT test set, cross-simulator evaluation
- Weeks 9-10: Analysis and writeup

**Total: ~5-6 months** (can run in parallel with P1 writeup)

#### Alternative (If P2 Fails or Time Is Short)

If cross-simulator inference is too ambitious or doesn't show improvement:
- **Fallback:** Demonstrate that EFT coefficients extracted from THESAN (if available) match those from 21cmFAST + SCRIPT
- This would still validate the EFT framework, even if inference benefits are unclear

## Background Reading (Status: Completed)

Four foundational reviews have been absorbed into the wiki:

| Paper | What it provides | Status |
|-------|-----------------|--------|
| [[Choudhury 2022 (Reionization Intro)]] | Complete derivation of photon budget, halo mass functions, global reionization equation, minimum halo mass for star formation | Read & synthesized |
| [[Ferrara & Pandolfi (IGM Reionization)]] | IGM physics, Lyman-alpha forest, inside-out topology, observational context | Read & synthesized |
| [[Trac & Gnedin 2009 (Reionization Simulations)]] | Radiative transfer algorithm taxonomy, convergence of full RT codes, sources vs. sinks, why quasars cannot reionize | Read & synthesized |
| [[Gnedin & Madau 2022 (Modeling Reionization)]] | Complete code taxonomy, speed/fidelity trade-offs, description of 21cmFAST in detail | Read & synthesized |

**Next reading:**
- [[McQuinn & D'Aloisio 2018]] — foundational EFT theory (already read; will re-read for details)
- [[Qin et al 2022 (EFT Redshift Space)]] — redshift-space EFT and renormalization tricks
- [[Solt et al 2026 (Multi-Simulator Training)]] — understanding the empirical baseline
- [[Berklas & Pober 2025]] — understanding within-code dependence failures

## Technical Implementation Plan for P1

### Software Stack

- **Language:** Python 3.8+
- **Core packages:** 
  - `py21cmfast` — 21cmFAST interface
  - `SCRIPT` — compiled C/Python interface (from github)
  - `numpy` — array operations, linear algebra (`lstsq`)
  - `scipy` — interpolation, special functions
  - `powerbox` — Fourier transform and power spectrum utilities
  - `matplotlib`, `seaborn` — plotting

### Key Computational Patterns

**Computing power spectra from simulations:**
```
P_{21}(k) = (1/V) * |FFT(delta_T_b)|^2
P_{mm}(k) = (1/V) * |FFT(delta_m)|^2
```
Tools: `powerbox`, `numpy.fft`

**Linear regression in Fourier space (extracting bias coefficients):**
$$
\delta_x(\mathbf{k}) = b_1 \delta_m(\mathbf{k}) + \frac{b_2}{2} [\delta_m^2](\mathbf{k}) + b_{\nabla^2} (-k^2) \delta_m(\mathbf{k})
$$
- Construct design matrix: columns are the basis functions $\{\delta_m, [\delta_m^2], -k^2 \delta_m\}$
- Use `numpy.linalg.lstsq(design_matrix, delta_x_field)` to find coefficients
- Weight by mode count or inverse variance

### Expected Bottlenecks

1. **Simulation generation:** ~500 21cmFAST runs × 5 sec each = 2500 CPU-sec = ~0.7 CPU-hours. Not a bottleneck if cluster access is available.

2. **Power spectrum computation:** FFT of 1024³-2048³ grids can be slow. Parallelize over redshifts or use GPU FFT (`CuPy`) if available.

3. **Cross-simulator comparison:** Ensuring 21cmFAST and SCRIPT have **identical initial conditions** is critical. Testing/debugging this pipeline may take time.

## Expected Scientific Results

### For P1

Based on McQuinn & D'Aloisio 2018 (EFT validation on 3 full RT codes) and intuition about code differences:

**Large-scale coefficients ($b_1^x, b_2^x$):**
- Should show *moderate* code variation: 10-20% difference between 21cmFAST and SCRIPT
- Variation driven by differences in how source clustering and global history are captured
- Should be smoothly varying functions of redshift

**Derivative bias ($b_{\nabla^2}^x$):**
- Expected to show *substantial* code variation: 20-50% difference
- Directly encodes the effective ionized bubble size $R_\text{eff}$
- Different bubble-growth algorithms (excursion-set in 21cmFAST vs. CLF in SCRIPT) produce different morphologies
- Signature: $b_{\nabla^2}^x \propto -R_\text{eff}^2(z)$; the coefficient magnitude should track bubble growth

**Stochastic term ($P_{\varepsilon\varepsilon}$):**
- Expected to show *large* code variation: factor of 2-3 difference or more
- Encodes discrete bubble shot noise; implementation-specific
- Should fall as reionization progresses (fewer, larger bubbles = less shot noise)

**EFT validity:**
- Expect $P_\text{err} / P_{21} < 10\%$ for $k < 0.2-0.5 h/\text{Mpc}$ (typical for reionization)
- Validity breaks down at $k \sim 1/R_\text{eff}$ as expected from theory

### For P2

**Baseline (native parameters):**
- In-code generalization (21cmFAST → 21cmFAST test set): R² ~ 0.90-0.95
- Cross-code generalization (21cmFAST → SCRIPT): R² ~ 0.40-0.50 (from literature)

**EFT-informed:**
- Hypothesis: In-code R² ~ 0.85-0.90 (slight degradation due to indirect targets, but acceptable)
- Cross-code R² ~ 0.70-0.80 (improvement of factor ~1.5-2 vs. baseline)
- Success criterion: cross-code R² > 0.65 (indicating genuine improvement over baseline)

**If successful:**
- P2 would provide the first demonstration that EFT coefficients are more stable across simulators than native parameters
- Would validate the EFT framework as a practical tool for simulation unification
- Would open path for SKA-era analyses using EFT-parameterized inference

## Comparison to Prior Work

### vs. McQuinn & D'Aloisio 2018

**Their work:**
- Validated EFT on 3 **full radiative transfer codes** (THESAN, C²-Ray, SPHINX)
- Showed EFT works well ($P_\text{err}/P_{21} < 10\%$) at large scales
- Measured EFT coefficients and their redshift evolution

**This thesis:**
- Compare **two semi-numerical codes** (21cmFAST, SCRIPT) — tractable for large parameter grids
- Focus on **simulator dependence problem**: how much do coefficients vary between codes?
- Investigate whether EFT coefficients are more stable than native parameters for inference
- Novel: direct application to ML inference and cross-simulator generalization

### vs. Solt et al. 2026 (Multi-Simulator Training)

**Their work:**
- Pool training data from 3+ simulators
- Infer scalar **$\Delta z$** targets (compressed reionization history)
- Show empirical improvement in cross-simulator generalization

**This thesis (P2 if completed):**
- Use physically-motivated **EFT coefficient targets** instead of scalar compression
- More interpretable (each coefficient has physical meaning)
- Fewer parameters (4 EFT coefficients vs. many $\Delta z$ samples)
- Explicitly tests whether physics-informed parameterization helps

### vs. Ore et al. 2025 (SKATR)

**Their work:**
- Self-supervised Vision Transformer learns simulator-agnostic representations
- Data-driven; no theoretical assumptions
- Demonstrated cross-simulator generalization

**This thesis (P2):**
- Physics-informed (EFT) approach; complementary to SKATR
- Interpretable targets (vs. ViT embeddings)
- Fewer required training simulations (physics constrains the space)
- Could combine: SKATR features as input to EFT coefficient inference

## Publishability Assessment

### P1 (EFT Characterization of Ionization Field Across Codes)

**Suitable for:** JCAP (Journal of Cosmology and Astroparticle Physics), MNRAS (Monthly Notices of the Royal Astronomical Society)

**Novel contributions:**
- First systematic cross-code comparison of EFT coefficients for semi-numerical codes
- Quantitative assessment of simulator dependence in EFT language
- Maps of regime of validity for EFT as function of parameters and redshift
- Direct physical interpretation of code differences via bias coefficients

**Strength:** Clean, well-defined problem; clear methodology; no reliance on speculative outcomes

**Expected impact:** 10-20 citations in 2-3 years (moderate; niche audience of 21cm simulators and EFT community)

### P2 (EFT-Informed Inference and Cross-Simulator Generalization)

**Suitable for:** MNRAS, ApJ (if results are strong); or JCAP if combined with P1

**Novel contributions:**
- First demonstration (if successful) that EFT coefficients improve cross-simulator generalization
- Validates EFT framework as practical tool for multi-code inference
- Opens new avenue for handling simulator uncertainty in high-$z$ cosmology

**Strength (if successful):** Directly addresses major systematic in the field; methodologically clean

**Risk:** If cross-simulator generalization doesn't improve dramatically (e.g., only 10-20% better), the practical impact is less clear

**Contingency:** If P2 results are weak, focus the paper on P1 + THESAN cross-validation (if possible). P1 alone is publishable.

## Timeline (6-Month Master's Program)

| Month | Focus | Milestones |
|-------|-------|-----------|
| **Month 1** | Literature review; code setup; reproduce McQuinn & D'Aloisio Fig. 2 | 21cmFAST + SCRIPT running; confirmed output validation |
| **Month 2** | Matched ICs pipeline; EFT coefficient extraction methodology | 30-40 P1 simulations completed; first coefficient trajectories |
| **Month 3** | Full P1 parameter grid; coefficient extraction; regime mapping | Complete P1 simulation + analysis suite |
| **Month 4** | P1 interpretation + writing; begin P2 training set generation | P1 draft writeup; 500 21cmFAST runs for training set |
| **Month 5** | P2 inference model training; SCRIPT test set evaluation | Baseline and EFT models trained; cross-simulator test results |
| **Month 6** | P2 analysis; thesis writing; final figures and tables | Thesis submitted |

## Deliverables (Thesis Checklist)

### P1 (Required)
- [x] Code infrastructure: 21cmFAST + SCRIPT matched ICs working
- [ ] EFT coefficient trajectories $\{b_1^x, b_2^x, b_{\nabla^2}^x\}$ for 21cmFAST across $z$ and parameters
- [ ] Same for SCRIPT with matched ICs
- [ ] $P_\text{err}/P_{21}$ error maps for both codes as function of $k, z$, and parameters
- [ ] Physical interpretation section: what code differences does EFT reveal?
- [ ] Publication-ready figures and tables
- [ ] ~6000-8000 word P1 writeup (methods, results, discussion)

### P2 (Stretch Goal)
- [ ] Parameter → EFT mapping function trained
- [ ] 500-simulation training set (21cmFAST with EFT coefficients)
- [ ] Baseline neural network trained (native parameter targets)
- [ ] EFT-informed neural network trained (EFT coefficient targets)
- [ ] Cross-simulator generalization test on SCRIPT data
- [ ] R² comparison: baseline vs. EFT-informed
- [ ] ~4000-5000 word P2 writeup (or included as P1 extension)

### Overall Thesis
- [ ] Full written thesis (~12,000-15,000 words for master's)
- [ ] Literature review (2000-3000 words)
- [ ] Methods (3000-4000 words)
- [ ] Results (3000-5000 words)
- [ ] Discussion & Conclusions (2000-3000 words)
- [ ] Code repository (github) with documentation and reproducibility
- [ ] Public data release (EFT coefficient tables, power spectra) if space permits

## Key Resources and Contacts

**Supervisors & collaborators:**
- [Thesis supervisor] — primary advisor; provided project proposal
- [Co-advisors/mentors] — if any

**Code documentation:**
- py21cmfast: https://github.com/21cmfast/21cmFAST (excellent docs)
- SCRIPT: https://github.com/charlottenosam/SCRIPT (good documentation)
- swyft: https://github.com/undark-lab/swyft (for P2 if pursued)

**Key papers to have at hand:**
- [[McQuinn & D'Aloisio 2018]] — EFT foundational
- [[Qin et al 2022 (EFT Redshift Space)]] — redshift-space + renormalization
- [[Baldauf et al 2016]] — perturbation theory density fields (for 2LPT understanding)
- [[Choudhury 2022 (Reionization Intro)]] — physics background

## Open Questions and Decisions

1. **Which second simulator for P1?** SCRIPT is most tractable; SimFast21 also possible. **Decision:** SCRIPT (publicly available, CLF approach is clearly different from 21cmFAST).

2. **How to handle matched initial conditions?** Exactly which redshift should ICs be exported from 21cmFAST? **Decision:** Generate at $z=0$ (earliest time in 21cmFAST runs), export $\delta_m(\mathbf{x})$; both codes evolve from there.

3. **What astrophysical parameter grid for P1?** Fine grid (50+ points) or coarse grid (20-30 points)? **Decision:** Start with ~30-40 points for feasibility; expand to 50-100 if time permits.

4. **For P2, should we use power spectrum or 2D power spectrum summaries?** 1D power spectrum is simpler; 2D allows foreground mitigation. **Decision:** Start with 1D for speed; 2D as robustness check if time permits.

5. **How to handle the $T_S$ assumption in practice?** The thesis assumes $T_S \gg T_\text{CMB}$ for $z < 15$. Should we validate this? **Decision:** Check using 21cmFAST's thermal outputs; document the redshift range where assumption is valid.

6. **Is the EFT approach actually better for inference?** What if P2 shows no improvement? **Decision:** P1 is publishable independently. P2 is a test of the hypothesis; even null results (EFT coefficients don't help) are scientifically interesting and publishable.

## Risk Assessment and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Matched ICs pipeline doesn't work | Medium | High | Start debugging early (month 1); have backup: use same random seed, hope for similar ICs |
| Simulator differences in EFT space are too small to measure | Low | Medium | Use large ensemble (~100+ sims per code); publish as "EFT coefficients are robust across codes" |
| P2 inference doesn't show improvement | Medium | Low | P1 is publishable independently; P2 failure is still interesting result |
| Cluster computing issues | Low | Medium | Have local laptop implementation for small tests; contact sys admins early |
| Time pressure in final month | Medium | Medium | Prioritize P1 completion; P2 is optional; have clear fallback positions |

## Expected Outputs and Impact

### Immediate (6-month thesis)
- **1-2 publications:** P1 (±P2 if successful) in JCAP/MNRAS
- **Code release:** Python package for EFT coefficient extraction from 21cm simulations
- **Data release:** Tables of EFT coefficients from 21cmFAST and SCRIPT
- **Training materials:** Wiki documentation (this file and related entries) suitable for teaching

### Longer term (2-3 years post-thesis)
- **Extensions:** Apply same methodology to THESAN, other codes, AGN-inclusive models
- **Observational applications:** Measure EFT coefficients from HERA data (if early detections), test predictions
- **Inference applications:** Integrate EFT-based inference into standard 21cm analysis pipelines (EoRFlow, etc.)
- **Cross-field applications:** Methodology transfers to galaxy clustering (where EFT bias expansion already standard)

### Impact on the field
- **Simulator unification:** Provides principled language for understanding code differences
- **Systematic reduction:** Demonstrates that EFT reduces (potential) cross-simulator bias in inference
- **SKA readiness:** Positions the community to handle simulator uncertainty when real 21cm detections arrive
- **ML + Physics:** Shows practical value of physics-informed parameterization vs. pure data-driven approaches
