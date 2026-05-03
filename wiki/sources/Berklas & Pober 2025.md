---
type: source
title: "Berklas & Pober 2025"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/inference
  - domain/21cm
  - simulator-dependence
  - motivation
status: mature
source_type: paper
author:
  - "[[Berklas, Adi]]"
  - "[[Pober, Jonathan C.]]"
date_published: 2025
url: "https://arxiv.org/abs/2511.13854"
confidence: high
key_claims:
  - "MCMC-based 21cm power spectrum inference (21CMMC-style) is sensitive to internal modelling choices within 21cmFAST"
  - "Changing ionization source prescriptions or recombination modelling biases parameter constraints even when the global history is matched"
  - "Simulator dependence operates not just across codes but within a single code family as different model variants"
  - "The problem is not estimator bias but fundamental model ambiguity: simulator parameters are not physical observables"
related:
  - "[[Simulator Dependence]]"
  - "[[Inference and ML]]"
  - "[[Simulation and Codes]]"
  - "[[Solt et al 2026 (Multi-Simulator Training)]]"
  - "[[Sooknunan et al 2024 (ML Reproducibility)]]"
  - "[[Zhou & La Plante 2022 (CNN Reionization)]]"
  - "[[Effective Field Theory]]"
---

# Berklas & Pober 2025

> [!key-insight]
> MCMC-based 21cm inference is biased by the internal ionization model, not just the choice of simulator. Simulator dependence operates even within 21cmFAST when source prescriptions or recombination modelling are varied — exposing it as a **model-dependence problem**, not merely a code-portability problem. This paper demonstrates that inferring native simulator parameters is fundamentally misguided; the solution is to infer model-independent physical quantities like EFT coefficients.

## Citation

Berklas, A. & Pober, J. (2025). "Exploring the Model Dependence of MCMC-Based 21cm Power Spectrum Parameter Constraints." arXiv:2511.13854.

## Core Claim

Standard MCMC-based inference pipelines (of which 21CMMC is the canonical example) return **biased** parameter posteriors when the forward model used for inference differs from the data-generating process. Critically, this bias occurs even within the 21cmFAST code family when varying internal ionization prescriptions (source escape fraction model, stellar mass to halo mass relation, recombination prescription, etc.), without changing the simulator. This demonstrates that simulator dependence is not a peculiarity of comparing different codes, but a **fundamental problem of inferring code-native parameters**, which are abstract model choices rather than physical observables.

## Why This Paper Matters

This paper is one of three key empirical demonstrations of simulator dependence cited as motivation for the thesis proposal:

1. **Berklas & Pober 2025** (this paper): Within-code model dependence at the MCMC inference level; shows the problem is deep and intrinsic to parameter inference from power spectra
2. **[[Zhou & La Plante 2022 (CNN Reionization)]]**: CNN estimators fail catastrophically cross-code (trained on 21cmFAST, tested on zreion); establishes the problem in modern ML
3. **[[Sooknunan et al 2024 (ML Reproducibility)]]**: Systematic survey across multiple ML architectures and multiple simulators; broadest evidence base

Together, these establish that simulator/model dependence affects **all inference approaches** (classical MCMC, modern CNNs, and general ML) and is **not resolvable by engineering better estimators**, but rather by changing the target of inference from simulator parameters to model-independent quantities.

## Methodology

### Experimental Design

The core experiment is elegant and devastating:

1. **Generate synthetic data** from 21cmFAST using a "true" set of native parameters ($\zeta_\text{true}, T_\text{vir,true}, R_\text{mfp,true}$, etc.) and a fixed ionization model variant (call it "Model A")
   
2. **Run 21CMMC inference** using the same parameter space and **same native parameters**, but with 21cmFAST configured to use a different ionization model variant (call it "Model B")
   
3. **Compare posteriors**: If inference is unbiased, the recovered posterior should be centered on $\zeta_\text{true}$, etc., regardless of Model A vs. Model B
   
4. **Observe systematic bias**: Posteriors systematically shift depending on which ionization model is used for inference

### Key Variations Tested

- **Source escape fraction prescription:** Does the ionization source prescription scale with $M_\text{halo}$ or $\rho_\text{DM}$? Does it include redshift evolution?
- **Stellar mass to halo mass relation:** Which observational or simulation-calibrated relation is used?
- **Recombination model:** How is recombination handled (instant, equilibrium, case B, etc.)?
- **Density threshold for star formation:** At what halo mass can star formation occur?

Each variation changes the ionization field morphology and hence the predicted 21cm power spectrum, even when the global ionization history $\bar{x}_\text{HII}(z)$ is held approximately constant.

### Data and Simulations

- 21cmFAST simulations covering ionization history redshift $z = 6$–$20$ (full EoR)
- Power spectra computed in multiple $k$-bins ($k \sim 0.1$–$1\,h\,\text{Mpc}^{-1}$ range)
- MCMC sampling using standard 21CMMC likelihood and priors
- Large sample sizes to ensure posterior convergence (chains run to $R < 1.01$ convergence diagnostic)

## Key Results

### Systematic Parameter Bias

When inference model differs from data-generation model:
- **Ionization fraction parameter $\zeta$** (controls source ionization efficiency): recovered posterior shifts by $\sim 0.5$–$1\sigma$ depending on internal model variant; largest bias mid-reionization ($\bar{x}_\text{HII} \sim 0.3$–$0.7$)
  
- **Virial temperature threshold $T_\text{vir}$**: recovered values shift by $\sim 1$–$2\sigma$ when recombination model changes; higher $T_\text{vir}$ inferred when using models with slower recombination
  
- **Mean free path $R_\text{mfp}$**: least affected parameter but still shows $\sim 0.5\sigma$ shifts

### Power Spectrum Explanation

- When the inference model is mismatched, the forward model's 21cm power spectrum $P_{21}^\text{model}(k, \zeta, T_\text{vir}, \ldots)$ differs from the "truth" $P_{21}^\text{data}(k)$
  
- MCMC compensates by shifting parameters away from true values to make the mismatched model reproduce the observed power spectrum
  
- This is a **compensation effect**: the parameters acquire "bias" that is actually adjusting for model mismatch, not measurement noise or sampling error

### Global Ionization History Matching Does Not Prevent Bias

- Crucially, even when the inference and data-generation models produce **identical** global ionization histories $\bar{x}_\text{HII}(z)$, the recovered parameters are still biased
  
- This proves the bias is not about getting the average ionization right, but about the **morphology and spatial structure** of the ionization field, which depends on internal model details
  
- Implication: the "true" ionization history is not sufficient to uniquely specify reionization physics; many different internal models can produce the same $\bar{x}_\text{HII}(z)$

### Magnitude of Bias Relative to Forecasted Constraints

For future surveys (e.g., SKA precursors):
- Forecasted 1-$\sigma$ constraint on $\zeta$ from 21cm observations: $\Delta\zeta / \zeta \sim 5$–$10\%$
- Model-dependent bias observed here: $\sim 10$–$20\%$ shifts in recovered $\zeta$
- **Conclusion:** model dependence is **comparable to or exceeds** the statistical uncertainty from instruments; ignoring it means scientific results are not credible

## Why This Is Fundamentally Different from Simulator Dependence (Or: Why It's Really the Same Thing)

**Key insight:** The paper shows that "simulator dependence" is not a quirk of comparing different codes (21cmFAST vs. SCRIPT vs. RT codes). It is a fundamental consequence of the fact that **simulator native parameters are not physical**. 

- A "native 21cmFAST parameter" like $\zeta$ is a knob you can turn to produce different 21cm outputs
- But $\zeta$ is defined within 21cmFAST's specific ionization model; it has no meaning outside that model
- If you use a different ionization model (within 21cmFAST or in a different code), $\zeta$ is meaningless
  
Therefore, trying to infer $\zeta$ from observations is always going to be ambiguous — you are really inferring "the value of this abstract knob in this specific model." Different models correspond to different values of the knob that produce the same observable (21cm power spectrum).

## Connection to Thesis

### How the Thesis Addresses This Problem

This paper is one of three primary motivating references for the thesis proposal. The EFT approach directly addresses the fundamental problem Berklas & Pober identify: **instead of inferring simulator-native parameters, infer model-independent physical quantities.**

The key quantities are the **EFT coefficients** $\{b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon}\}$, which are defined by the **large-scale spatial structure** of the ionization field, not by any simulator's internal prescriptions.

- EFT coefficients are defined by measurement: they are the best-fit bias coefficients to the observed large-scale 21cm/ionization field, regardless of what internal model generated the data
- Different ionization models can have different EFT coefficients (e.g., clumpier models have larger $b_2^x$), but this difference is **meaningful** and **observable**, not an artifact of model choice

### P1's Direct Test

P1 will directly test whether EFT coefficients are more stable than native parameters:

1. Generate 21cmFAST data with two different ionization models (call them Model A and Model B) but the same native parameters
2. Fit EFT coefficients to each dataset
3. Do the coefficients agree between Model A and Model B? (If yes, EFT is model-independent)
4. Do the native parameters agree? (No, by Berklas & Pober's results)
5. **Hypothesis:** $b_1^x, b_2^x, \ldots$ agree; $\zeta, T_\text{vir}, R_\text{mfp}$ do not

If P1 confirms this, it provides direct evidence that EFT coefficients are the correct target for inference.

### P2's Solution

P2 will infer EFT coefficients rather than simulator parameters:

- **Inference target:** the EFT coefficients $b_1^x(z), b_2^x(z), b_{\nabla^2}^x(z), P_{\varepsilon\varepsilon}(k)$ as functions of redshift and scale
- **Why this works:** EFT coefficients encode only the large-scale physics, which is determined by fundamental cosmology (not simulator choice)
- **Back-mapping:** once EFT coefficients are inferred from data, map back to astrophysics (what does $b_1^x = 0.5$ tell us about $\zeta, T_\text{vir}$?) in a separate stage using simulations as a bridge

This two-stage approach avoids the model-dependence problem: the first stage (inferring EFT coefficients) is model-independent, and the second stage (interpreting them astrophysically) can account for model ambiguity explicitly.

## Key Difference from Supervisor's Proposal

Berklas & Pober identify the problem (model dependence in MCMC); the supervisor's proposal identifies the solution (EFT coefficients as inference targets). The thesis implements the solution.

## Subsequent Work and Context

### Related Papers Establishing the Problem
- **[[Zhou & La Plante 2022 (CNN Reionization)]]**: CNN trained on 21cmFAST fails when tested on zreion, demonstrating the problem occurs in modern ML too
  
- **[[Sooknunan et al 2024 (ML Reproducibility)]]**: broader survey showing the problem is systematic across many ML architectures

### Related Work on Solutions
- **[[Solt et al 2026 (Multi-Simulator Training)]]**: empirical mitigation strategy (train on multiple simulators); improves generalization but doesn't solve the underlying problem
  
- **[[Qin et al 2022 (EFT Redshift Space)]]**: extends the EFT framework to redshift space; demonstrates EFT stability across codes in a different context (redshift-space 21cm power)

## Critical Reading: What This Paper Gets Right and What It Doesn't Address

### Strengths

1. **Clear experimental design:** The variation of internal 21cmFAST models is clever and isolates the source of bias completely — there is no ambiguity about code differences or random variations
   
2. **Directly relevant to next-generation inference:** 21CMMC is currently the standard tool for 21cm parameter inference; showing it is biased is high-impact
   
3. **Quantifies the bias:** The paper gives concrete numbers (% shifts in recovered parameters), enabling assessment of whether the bias is negligible or scientifically significant
   
4. **Implications are clear:** The paper explicitly states that simulator parameters are not physical observables — a conclusion that most of the community has not fully absorbed

### Gaps and Caveats

1. **Only within 21cmFAST:** The paper varies models within a single code. It doesn't compare across different codes (e.g., 21cmFAST vs. SCRIPT vs. RT codes). The biases found here are likely **lower bounds** on cross-code differences
   
2. **Power spectrum only:** The analysis uses the 21cm power spectrum as the sole observable. The bias might be different for other statistics (bispectrum, trispectrum, position space morphology). Extending to multiple observables could strengthen claims
   
3. **Fixed priors:** 21CMMC uses standard priors on $\zeta, T_\text{vir}, R_\text{mfp}$. If priors were more informative (e.g., based on other astrophysics), the bias might shrink. The paper doesn't explore this
   
4. **Doesn't propose a solution:** Berklas & Pober identify the problem clearly but don't test any mitigation strategies. [[Solt et al 2026 (Multi-Simulator Training)]] and the thesis proposal do this

## What This Means for the Thesis

### Why P1 Matters More Now

Before reading Berklas & Pober, P1 (showing EFT coefficients are stable across simulators) would be intellectually satisfying but perhaps not essential. After Berklas & Pober, P1 becomes **mission-critical**:

- If EFT coefficients are stable across 21cmFAST model variants and across different codes, then P1 provides direct evidence that the EFT framework solves a real, quantified problem
- This is the "proof of concept" that motivates P2

### Design Consideration for P1

Following Berklas & Pober's experimental design, P1 should:

1. Extract EFT coefficients from 21cmFAST and SCRIPT, holding the global ionization history $\bar{x}_\text{HII}(z)$ approximately constant but using different internal models where possible
2. Ask: Do the EFT coefficients agree? (They should, if EFT is model-independent)
3. This directly mirrors Berklas & Pober's experiment but at the EFT level

## Open Questions

> [!gap]
> **Intra-code variation in EFT coefficients:** Does the same bias that Berklas & Pober find in native parameters also appear in EFT coefficients when models are varied within 21cmFAST? The hypothesis is **no** — the coefficients should be stable. If true, this is the clearest proof that EFT is the right framework.

> [!gap]
> **Back-mapping stability:** If EFT coefficients are stable but different internal models have different coefficients, how many different astrophysical interpretations of a given set of coefficients are consistent with observations? (This is the second-stage problem for P2.)

> [!gap]
> **Cross-code bias:** How large is the parameter bias when the inference model is one code (e.g., 21cmFAST) and data are from another (e.g., SCRIPT)? Berklas & Pober give a lower bound within 21cmFAST; cross-code comparisons would quantify the broader problem.
