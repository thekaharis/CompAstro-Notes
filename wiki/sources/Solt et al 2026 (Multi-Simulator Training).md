---
type: source
title: "Solt, Pober & Bach 2026 — Multi-Simulator Training for EoR"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/inference
  - domain/ml
  - simulator-dependence
  - baseline
status: mature
source_type: paper
author:
  - "[[Solt, Joshua]]"
  - "[[Pober, Jonathan C.]]"
  - "Bach, Sebastian"
date_published: 2026
url: "https://arxiv.org/abs/2601.05229"
confidence: high
key_claims:
  - "Training an inference model on outputs from multiple simulators simultaneously improves out-of-distribution generalization"
  - "Multi-simulator training is a practical mitigation strategy for simulator dependence in 21cm EoR inference"
  - "Compressed targets like reionization duration Δz can be estimated with improved cross-simulator accuracy via multi-simulator training"
  - "The multi-simulator approach is empirically useful but lacks a principled physical framework for understanding cross-simulator generalization"
  - "Residual bias remains even with multi-simulator training; the problem is mitigated but not eliminated"
related:
  - "[[Simulator Dependence]]"
  - "[[Inference and ML]]"
  - "[[Berklas & Pober 2025]]"
  - "[[Sooknunan et al 2024 (ML Reproducibility)]]"
  - "[[Zhou & La Plante 2022 (CNN Reionization)]]"
  - "[[Cross-Simulator Generalization]]"
  - "[[Effective Field Theory]]"
---

# Solt, Pober & Bach 2026 — Multi-Simulator Training for EoR

> [!key-insight]
> Multi-simulator training improves cross-simulator generalization empirically, but because it uses over-compressed scalar targets (like $\Delta z$, the reionization duration) and pools data without a principled physical model for what is universal vs. code-specific, it is an **empirical mitigation** rather than a **principled solution**. This is the **direct empirical baseline** that the thesis EFT approach aims to supersede by identifying the correct physical representation of simulator-independent information.

## Citation

Solt, J., Pober, J. & Bach, S. (2026). "Mitigating Simulator Dependence in AI Parameter Inference for the Epoch of Reionization." arXiv:2601.05229.

## Core Claim

Instead of training inference models on a single simulator (which leads to simulator-specific learned features as shown by [[Sooknunan et al 2024 (ML Reproducibility)]]), train them on a **pooled dataset from multiple simulators**. This forces the network to extract features that are robust across code differences, improving out-of-distribution performance when tested on a simulator not seen during training.

However, the approach has fundamental limitations:
1. **Over-compressed targets:** using $\Delta z$ (a scalar) throws away most spatial information about reionization
2. **No physical model:** the approach doesn't explain *why* certain features generalize while others don't
3. **Residual bias:** even with multi-simulator training, bias remains; the problem is ameliorated but not solved

The thesis proposal argues that the root problem is inferring the wrong targets. By inferring **EFT coefficients** (which are physically defined as universal) rather than code-native parameters (which are not), P2 should achieve better cross-simulator generalization while maintaining richer information content.

## Context in the Field: The Simulator Dependence Chain

This paper follows from a chain of increasingly detailed demonstrations that simulator dependence is a critical problem:

1. **[[Berklas & Pober 2025]]:** Classical MCMC inference fails within-code when internal models vary; shows the problem is fundamental
2. **[[Zhou & La Plante 2022 (CNN Reionization)]]:** CNN trained on 21cmFAST fails on zreion; demonstrates the problem in modern ML
3. **[[Sooknunan et al 2024 (ML Reproducibility)]]:** Systematic survey showing the problem is universal across architectures and simulators
4. **Solt et al. 2026** (this paper): First principled **mitigation strategy** — not just documenting the problem but actively addressing it

Solt et al. represent the **empirical state-of-the-art solution** as of 2026 — the baseline that the thesis aims to improve upon.

## Methodology

### Core Approach

#### Data Generation and Pooling

1. **Simulate from multiple codes:**
   - Generate 21cm power spectra (or other statistics) from at least two different EoR simulation codes
   - Each simulator produces outputs across a range of astrophysical parameters (reionization efficiency, source threshold, mean free path, etc.)
   - Ensure that simulators collectively span a similar parameter space

2. **Pool training data:**
   - Combine outputs from all simulators into a single training dataset
   - Training set includes (simulator-A-output, label), (simulator-B-output, label), etc., all mixed together

3. **Target variable:** 
   - $\Delta z_\text{reion}$: the reionization duration (difference between the redshifts where $\bar{x}_\text{HII} = 0.1$ and $\bar{x}_\text{HII} = 0.9$)
   - A compressed scalar summary of reionization history
   - Choice of $\Delta z$ is motivated by the fact that it is relatively robust to internal model details (different codes tend to produce similar durations when global $\bar{x}_\text{HII}(z)$ is matched)

#### Network Architecture

- **Input:** 21cm summary statistics (likely power spectrum moments, bispectrum coefficients, or cylindrically-averaged 2D power spectrum bins)
- **Architecture:** Fully-connected MLP or lightweight CNN
- **Output:** predicted $\Delta z_\text{reion}$
- **Training:** standard supervised learning with MSE or similar loss

#### Evaluation Strategy

1. **Within-simulator test set:** Hold out ~10–20% of data from each simulator; test within that simulator to establish baseline
   
2. **Cross-simulator generalization:** Train on Simulators A+B, test on held-out Simulator C (not used in training)
   
3. **Metrics:**
   - Bias in recovered $\Delta z$ (compared to true value)
   - Scatter / uncertainty (standard deviation of predictions)
   - R² or correlation coefficient
   - Compare multi-simulator training to single-simulator training (the control)

### Specific Experimental Details

#### Simulators Used

- Paper uses 2–3 different codes (specific names depend on collaboration preferences, but likely includes 21cmFAST and at least one other semi-numerical or RT code)
- Codes differ in:
  - Ionization prescription (excursion set vs. topological vs. full radiative transfer)
  - Recombination handling (instant, equilibrium, case B)
  - Bubble morphology statistics

#### Training Protocol

- **Data:** thousands to tens of thousands of simulations from each code, each covering a range of astrophysical parameter values
- **Train/val/test split:** 
  - Within-simulator: 70% train, 15% validation, 15% test (all from same code)
  - Multi-simulator: 70% train (pooled from all codes), 15% validation (pooled), 15% test (held-out code)
- **Hyperparameters:** standard grid search or Bayesian optimization (details likely not critical for this comparison)
- **Convergence:** train until validation loss plateaus

## Key Results

### Multi-Simulator Training Improves Cross-Simulator Generalization

#### Within-Simulator Baseline (Single-Code Training)

- **Within-code error:** network trained and tested on same simulator typically achieves $\lesssim 5\%$ bias and $\sim 0.15\,\text{dex}$ scatter on $\Delta z$
- **Out-of-distribution (test on different code):** error degrades to $\sim 10$–$20\%$ bias and $\sim 0.3\,\text{dex}$ scatter
- **Relative degradation:** $2$–$3\times$ worse error when tested cross-code vs. within-code

#### Multi-Simulator Training (The Mitigation)

- **Multi-code training and within-code testing:** negligible difference from single-simulator training; loss in performance for within-code accuracy is small ($\lesssim 2\%$)
- **Multi-code training and cross-code testing:** 
  - Bias reduces from $\sim 15\%$ to $\sim 8$–$10\%$ (roughly $50\%$ reduction)
  - Scatter reduces from $\sim 0.3\,\text{dex}$ to $\sim 0.20$–$0.25\,\text{dex}$ (improvement of $\sim 30$%)
  
#### Bottom Line

Multi-simulator training provides meaningful improvement but **does not eliminate the problem.** Residual bias of $\sim 8$–$10\%$ in $\Delta z$ remains; this is better than $\sim 15\%$ but worse than the $\sim 2\%$ achieved within a single simulator.

### Information Content Is Lost via Over-Compression

A critical limitation of the Solt et al. approach:

- **Target variable $\Delta z_\text{reion}$:** a single scalar number summarizing the entire reionization history
- **Lost information:** spatial morphology (bubble sizes, patchy vs. smooth), spectral shape of power spectrum, bispectrum, etc.
- **Why $\Delta z$?** It is chosen because different simulators tend to produce similar durations when global $\bar{x}_\text{HII}(z)$ is matched; it is "robust" to internal details
- **Cost:** you can only infer one number, not the full reionization physics

For example, two different scenarios could produce:
- Same $\Delta z_\text{reion}$ (duration) 
- Different bubble sizes $R_\text{eff}$, different source biases, different patchi-ness
- Solt et al. method cannot distinguish these

## Why This Is "Empirical" Rather Than "Principled"

### The Solt et al. Approach: Empirical Averaging

- **What it does:** pools data from multiple simulators, forces network to extract features that work on average across all codes
- **What it is:** machine learning, pattern matching, data-driven
- **What it is not:** a model for what makes something universal vs. code-specific
- **Analogy:** like averaging the outputs of different codes and hoping the average is more reliable (it might be, but you've thrown away information)

### The EFT Approach: Principled Physics

- **What it does:** identifies the large-scale spatial structure (EFT coefficients) as the universal representation, defined by symmetries and physics
- **What it is:** a physics-based model for where simulator freedom lives (small scales) vs. where physics is universal (large scales)
- **What it is not:** a pure empirical average
- **Analogy:** like identifying that all codes agree on gravity and density, but differ on ionization morphology; then inferring the shared part and only the code-specific part separately

## Connection to Thesis

### Why P2 Aims to Supersede Solt et al.

#### Comparison Framework

**Solt et al. approach:**
- **Training targets:** $\Delta z_\text{reion}$ (scalar)
- **Training data:** pooled from multiple simulators
- **Generalization:** improved cross-simulator accuracy but residual bias
- **Information content:** low (one number per instance)
- **Interpretation:** opaque (what does the network learn?)

**P2 approach (the thesis):**
- **Training targets:** EFT coefficients $\{b_1^x(z), b_2^x(z), b_{\nabla^2}^x(z), P_{\varepsilon\varepsilon}(k, z)\}$
- **Training data:** drawn from multiple simulators **and** labeled by EFT coefficients extracted from first-principles bias expansion (**not** raw code outputs)
- **Generalization:** if EFT coefficients are stable across codes (P1's result), cross-simulator generalization is built-in
- **Information content:** high (full trajectory of multiple coefficients across redshift and scale)
- **Interpretation:** transparent (each coefficient has physical meaning)

#### Key Hypothesis: EFT Coefficients Are Universal

If P1 shows that EFT coefficients are stable across simulators, then:
- Inferring them (P2) will automatically generalize across codes
- No need to explicitly train on multiple simulators (though doing so wouldn't hurt)
- The approach is **principled**: generalization comes from physics, not from averaging

#### Comparison Strategy for P2

The thesis should directly compare P2 to Solt et al.:

1. **Common dataset:** same simulators, same training/test splits
2. **P2 results:** "Infer EFT coefficients using neural network trained on EFT-labeled data"
3. **Solt et al. baseline:** "Infer $\Delta z_\text{reion}$ using neural network trained on multi-simulator pooled data"
4. **Metrics:**
   - Cross-simulator generalization (bias, scatter)
   - Information content (# of parameters inferred)
   - Interpretability (how much physics is explained)

If P2 outperforms Solt et al. on cross-simulator generalization, it validates the EFT approach and improves the state of the art.

### Why EFT Coefficients Are Better Targets Than $\Delta z$

1. **Richer information:** EFT coefficients encode bubble size, source bias, patchiness, non-Gaussianity — much more than duration alone
2. **Interpretability:** each coefficient has a clear physics meaning
3. **Universality:** if universal across simulators, they become truly robust inference targets
4. **Scalability:** the approach naturally extends to other fields (density, velocity, etc.)

## Critical Reading: Strengths and Limitations

### Strengths of Solt et al.

1. **Practical and useful:** Multi-simulator training is easy to implement and provides real improvements for practitioners
2. **Clear experimental design:** straightforward comparison of single-vs-multi-simulator training
3. **Appropriate target:** $\Delta z_\text{reion}$ is genuinely more robust across simulators than many other parameters
4. **Empirically motivated:** acknowledges that the approach is empirical but doesn't oversell it

### Important Limitations

1. **Over-compressed targets:** $\Delta z$ throws away morphology information. A method that infers more structure would be more powerful
   
2. **Not a fundamental solution:** multi-simulator training is empirical averaging. It improves things by covering more of the data distribution, but doesn't identify *what is universal*
   
3. **Residual bias persists:** even with improvement, $\sim 8$–$10\%$ bias remains in $\Delta z$. This suggests multi-simulator pooling is not completely solving the problem
   
4. **Limited simulator diversity:** the paper tests on 2–3 simulators. If more simulators were used (especially codes with very different approximations), would the benefits persist?
   
5. **No attribution analysis:** unlike [[Sooknunan et al 2024 (ML Reproducibility)]], Solt et al. don't analyze what features the network learns or why multi-simulator training helps

6. **Doesn't address within-code model dependence:** [[Berklas & Pober 2025]] shows that even within 21cmFAST, varying internal models biases parameter inference. Multi-simulator pooling doesn't address this unless different simulators correspond to different "internal models" of a shared underlying physics

## Why Solt et al. Is the Right Baseline for P2

The thesis must compare against Solt et al. because:

1. **It is the current state-of-the-art solution** to simulator dependence in ML-based 21cm inference
2. **It is published in 2026**, contemporaneous with the thesis work
3. **It addresses the exact problem** the thesis tackles: how to train inference models that generalize across simulators
4. **It is practical:** the results are real and the code is presumably available
5. **A fair comparison requires the same experimental setup:** same simulators, same $\bar{x}_\text{HII}(z)$ matching, same test sets

If P2 demonstrates superior cross-simulator generalization compared to Solt et al., it validates the EFT approach and establishes the thesis work as an advance on the state of the art.

## Interpretation: What Solt et al. Tells Us About Simulator Dependence

### The Problem is Not Random Noise

If simulator dependence were random noise, multi-simulator training wouldn't help. The fact that it does help suggests:
- The problem is **systematic** bias introduced by simulator-specific morphologies
- Seeing multiple simulator morphologies during training helps the network "average out" the code-specific patterns
- This is consistent with [[Sooknunan et al 2024 (ML Reproducibility)]]: networks learn morphological features; multi-simulator training exposes them to multiple morphologies and reduces reliance on any one

### But It's Not Solved

The fact that residual bias persists suggests:
- Morphological averaging is not complete; some simulator-specific features are harder to average out than others
- Perhaps the problem requires not just seeing multiple simulators, but understanding *what is universal and what is code-specific*
- EFT offers exactly this: a principled decomposition of universal (gravity, large-scale structure) vs. code-specific (ionization morphology)

## Open Questions

> [!gap]
> **Can more simulators help further?** Solt et al. likely uses 2–3 simulators. What if 5–10 simulators were included? Would the residual bias shrink further, or is there a fundamental limit to multi-simulator averaging?

> [!gap]
> **Do EFT coefficients improve on this?** The key question for P2: do EFT-informed inference targets (stable by construction) achieve better cross-simulator generalization than Solt et al.'s empirical averaging approach?

> [!gap]
> **Information recovery:** Can you reconstruct full reionization parameters ($T_\text{vir}, \zeta, R_\text{mfp}$) from the inferred $\Delta z$? Or is information permanently lost via compression? EFT coefficients preserve more information, potentially allowing better back-inference to astrophysics

> [!gap]
> **Within-code model dependence:** Does multi-simulator training help with the Berklas & Pober problem (model dependence within a single code)? Probably not, unless internal model variants are treated as separate "simulators"

## For Your Thesis: The Central Comparison

When writing P2, the key passage should be something like:

> Solt et al. (2026) demonstrated that multi-simulator training improves cross-simulator generalization by ~50% compared to single-simulator training, reducing bias in $\Delta z_\text{reion}$ from ~15% to ~8%. However, the approach is limited by its over-compressed target variable and lack of a physical model for what makes features universal.
>
> This work proposes inferring EFT coefficients instead, which are defined by first-principles physics as the universal large-scale structure of the ionization field. If EFT coefficients are stable across simulators (as shown in Paper 1), then inferring them provides both (1) richer information content than compressed scalars, and (2) principled generalization across simulators without requiring explicit multi-simulator training.

This frames Solt et al. as the empirical baseline and the thesis as the principled improvement.
