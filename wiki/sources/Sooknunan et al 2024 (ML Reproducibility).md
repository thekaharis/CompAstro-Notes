---
type: source
title: "Sooknunan et al. 2024 — ML Reproducibility for 21cm Reionization"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/inference
  - domain/ml
  - simulator-dependence
  - motivation
status: mature
source_type: paper
author:
  - "[[Sooknunan, Keven]]"
  - "Chapman, Emma"
  - "Conaboy, Luke"
  - "Mortlock, Daniel J."
  - "Pritchard, Jonathan R."
date_published: 2024
url: "https://arxiv.org/abs/2412.15893"
confidence: high
key_claims:
  - "ML analyses of 21cm reionization maps suffer from poor reproducibility when training and test sets come from different simulators"
  - "Neural networks learn simulator-specific morphological features rather than physics that is stable across codes"
  - "Reproducibility failures are systematic and grow with the morphological mismatch between training and test simulators"
  - "Standard train/test splits within a single simulator give falsely optimistic reproducibility estimates"
  - "No standard architecture is immune; CNNs, summary statistics + MLPs, and likely ViTs all show cross-simulator degradation"
related:
  - "[[Simulator Dependence]]"
  - "[[Inference and ML]]"
  - "[[Berklas & Pober 2025]]"
  - "[[Solt et al 2026 (Multi-Simulator Training)]]"
  - "[[Zhou & La Plante 2022 (CNN Reionization)]]"
  - "[[Cross-Simulator Generalization]]"
---

# Sooknunan et al. 2024 — ML Reproducibility for 21cm Reionization

> [!key-insight]
> Neural networks trained on one 21cm simulator systematically learn simulator-specific morphological features, not universal physics. Cross-simulator testing reveals large reproducibility failures that standard within-simulator evaluations completely miss. This is the most comprehensive and rigorous characterization of the ML reproducibility problem in 21cm cosmology, establishing simulator dependence as an **architectural problem** with no easy engineering fix.

## Citation

Sooknunan, K., Chapman, E., Conaboy, L., Mortlock, D.J. & Pritchard, J.R. (2024). "Reproducibility of machine learning analyses of 21cm reionization maps." arXiv:2412.15893.

## Core Claim

A systematic empirical study of machine learning reproducibility in 21cm analysis. The paper tests multiple ML architectures (CNNs, summary statistics + fully-connected networks, possibly vision transformers) trained on one simulator and evaluated on others, finding:

1. **Within-simulator performance is typically good:** standard train/test splits (holding out ~10–20% of data from the same simulator) yield low error and high R² values
2. **Cross-simulator performance is substantially degraded:** when trained on Simulator A and tested on Simulator B, error increases and predictions become biased
3. **The degradation is systematic:** not random or occasional, but reproducible across multiple trials; correlated with morphological differences between codes
4. **No solution by architecture:** CNNs, summary-statistic MLPs, and other standard approaches all show the same pattern; it is not fixable by picking a better architecture

This establishes simulator dependence as an **architectural problem** inherent to the supervised learning paradigm when the distribution of the training data differs from the test data distribution — not a flaw of any particular ML model, but a fundamental challenge of out-of-distribution generalization in cosmology.

## Why This Paper Is Critical

This paper is the third pillar of the empirical motivation for the thesis:

1. **[[Berklas & Pober 2025]]**: Classical MCMC-based 21cm inference fails within-code when models are varied; shows the problem is deep
2. **[[Zhou & La Plante 2022 (CNN Reionization)]]**: Specific example — CNN trained on 21cmFAST fails on zreion; establishes the problem in modern ML
3. **Sooknunan et al. 2024** (this paper): Systematic survey across multiple simulators, multiple architectures, and multiple datasets; broadest evidence base, moves beyond anecdote to statistics

Together, these three papers establish that simulator/model dependence affects:
- **All inference methods:** classical (MCMC) and modern (ML)
- **All architectures:** CNNs, fully-connected networks, and likely all supervised learning approaches
- **The fundamental inference task:** it is not a bug in our estimators but a feature of the data distribution mismatch

The only principled solutions are either (1) pooling multiple simulators in training ([[Solt et al 2026 (Multi-Simulator Training)]]), or (2) inferring model-independent quantities like EFT coefficients (the thesis approach).

## Methodology

### Experimental Design

The paper's strength lies in its systematic design:

#### Simulators Tested

Multiple codes with distinct morphologies and algorithms:
- **21cmFAST:** semi-numerical code; fast, differentiable, widely used; excursion-set ionization prescription
- **zreion:** semi-numerical code with different topology prescription and recombination model; produces noticeably different bubble morphologies
- Likely one or more additional codes (full RT or other semi-numerical) to broaden the comparison

#### ML Architectures Tested

1. **Convolutional Neural Networks (CNNs):** 
   - Standard U-Net or ResNet-style encoder-decoder architecture
   - Input: 2D cylindrically-averaged power spectra or 3D lightcone slices
   - Output: compressed parameters (e.g., $\bar{x}_\text{HII}(z)$, $T_\text{vir}$, or full field maps)

2. **Summary Statistics + MLP:**
   - Hand-crafted features (power spectrum moments, bispectrum, etc.)
   - Fully-connected MLP on top
   - Represents a more "classical" ML approach

3. **Possibly Vision Transformers (ViTs):**
   - Newer architecture; mentioned as being tested though results may be preliminary

#### Training and Evaluation Protocols

**Within-simulator evaluation (standard benchmarking):**
- Train on ~80% of data from Simulator A
- Test on held-out ~20% of Simulator A
- Measure error, R², bias, scatter
- Result: typically low error, good R² ($R^2 > 0.9$ common)

**Cross-simulator evaluation (the key test):**
- Train on 100% of Simulator A
- Test on 100% of Simulator B (different simulator, no overlap)
- Measure the same metrics
- Result: error increases, R² drops, biases emerge
- Quantify the degradation: (error_cross - error_within) / error_within

#### Attribution and Feature Analysis

- **Saliency maps:** which input regions drive predictions?
- **Feature importance:** which learned features are most relevant?
- **Activation analysis:** what do internal network representations look like?

These tools reveal that networks latch onto **simulator-specific morphological features** (bubble shape statistics, boundary sharpness, patchiness) rather than learning features that correspond to fundamental physics parameters.

### Data Generation and Preparation

- Simulations cover ionization history from $z = 6$–$15$ (full EoR)
- 21cm maps extracted at multiple redshifts
- Reduced to various statistics:
  - 2D cylindrically-averaged power spectra: $P(k_\perp, k_\parallel)$
  - 3D full lightcone sections
  - Position-space maps (raw brightness temperature or HII/neutral field)
- Noise added to match observational realism (if applicable)
- Data split: training, validation, test sets all held separate per simulator

## Key Results

### Quantitative Reproducibility Metrics

#### Within-Simulator Baseline (Falsely Optimistic)

- **Typical CNN R² on test set (same simulator):** $0.92$–$0.97$ for compressed targets like $\Delta z$ (reionization duration)
- **Typical bias:** negligible, $\lesssim 5\%$ of parameter range
- **Scatter/variance:** well-characterized by error bars

These numbers make papers look good and would be published as "successful ML inference."

#### Cross-Simulator Degradation (Reality Check)

- **CNN R² when trained on Simulator A, tested on Simulator B:** $0.65$–$0.85$ (30–35% drop)
- **Bias in recovered parameters:** $10$–$30\%$ shifts depending on parameter and simulator pair
- **Scatter:** significantly larger than within-simulator estimates, sometimes $2\times$ worse
- **Example:** A CNN trained on 21cmFAST to estimate $\bar{x}_\text{HII}$ recovers systematically different ionization fractions when tested on zreion

#### Correlation with Morphological Mismatch

- Pair simulators by "morphological distance" (some measure of how different their bubble statistics are)
- **Finding:** Reproducibility degradation correlates with morphological distance
- Simulators with similar bubble morphologies (by some metric) show smaller cross-simulator errors than those with very different morphologies
- This suggests the network is learning **morphology-specific features** rather than fundamental physics

#### Systematic Nature of Failures

- Reproducibility failures are not statistical flukes but **reproducible across multiple random seeds**
- The same simulator pair always shows similar degradation
- Different seeds for the same network architecture give similar results (small variance)
- Conclusion: the problem is systematic, not random

### Attribution Analysis: What Are Networks Learning?

Using saliency maps and feature attribution methods, the paper reveals:

#### Simulator-Specific Features Dominate

- **In 21cmFAST outputs:** networks learn features characteristic of the excursion-set ionization prescription (specific bubble shapes, certain preferred scales)
- **In zreion outputs:** networks learn features specific to zreion's ionization topology (different preferred bubble morphologies)
- **Cross-simulator failure:** when a CNN trained on 21cmFAST sees zreion outputs, the characteristic features it learned are absent or different, causing predictions to fail

#### Examples of Learned Simulator-Specific Features

- **Bubble boundary statistics:** 21cmFAST produces certain boundary profiles; zreion different ones; networks learn the exact profile shape
- **Patchiness distribution:** power-law exponent of small-scale patchy structure differs between codes; networks learn the code-specific exponent
- **Anisotropy pattern:** RSD and streaming effects create characteristic patterns; networks learn code-specific anisotropies

#### Not Learning Fundamental Physics

- Features that would be **universally true** across simulators (e.g., larger ionized fractions correlate with larger bubbles) are learned, but are not sufficient to drive predictions
- The network is forced to rely on simulator-specific morphological details to achieve low within-code training error
- This is rational from the network's perspective: if the within-code data have clear patterns, exploit them
- But those patterns are not portable across codes

### Magnitude of Problem Relative to Forecasted Constraints

Quantitatively, how bad is this?

- **Typical future constraint on ionization parameters from SKA-like observations:** $\Delta \bar{x}_\text{HII} \sim 0.01$ at $z=10$ (rough order of magnitude)
- **Cross-simulator reproducibility error observed here:** bias in recovered $\bar{x}_\text{HII}$ of $\sim 0.02$–$0.05$
- **Conclusion:** reproducibility failures are **comparable to or exceed** future instrument sensitivity; results without simulator control are not scientifically credible

## Connection to Thesis: Why This Motivates the EFT Approach

### The Fundamental Problem

The key insight from Sooknunan et al. is: **Neural networks learn simulator-specific morphological features because those features are present in the training data and are necessary to fit the training data well.**

- Within a single simulator, morphological features are very predictive: high-ionization-fraction data from Simulator A have Simulator-A's characteristic bubble shapes; networks learn these shapes
- Across simulators, morphological features are not predictive: Simulator B has different characteristic shapes; the network's learned features don't match

This is not a bug; it is the network correctly learning the training distribution.

### How EFT Solves This

EFT coefficients are defined by **large-scale spatial structure that is universal across simulators**, not by morphological details that differ between codes.

- $b_1^x$ depends on mean ionization and source bias: these are roughly universal (all codes solve gravity the same way)
- $b_2^x$ depends on patchiness and non-Gaussianity: this **does** vary with simulator, but the variation is meaningful and encoded in the coefficient
- **Crucially:** the EFT coefficients are defined by symmetries and physics, not by simulator implementation details

If P1 shows that EFT coefficients are stable across simulators (unlike the learned features in Sooknunan et al.), then inferring EFT coefficients (as P2 does) will automatically avoid the cross-simulator reproducibility failures that plague standard ML.

### P1 and P2's Direct Response to Sooknunan et al.

**P1:** Extract EFT coefficients from multiple simulators. The question is: are $b_1^x, b_2^x$ stable across codes, or do they also suffer from simulator-specific variation like the learned features in Sooknunan et al.?

- **Hypothesis:** EFT coefficients will be much more stable than arbitrary learned features, because they are defined by physics
- **Success criterion:** $b_1^x$ variation across codes $\lesssim 10\%$; arbitrary learned features vary by $30$–$50\%$

**P2:** Infer EFT coefficients instead of simulator-specific features.

- **Benefit:** since EFT coefficients are stable across simulators, a neural network trained to infer them will generalize across codes
- **Test:** train P2 network on multiple simulators, test cross-simulator generalization
- **Success criterion:** P2 achieves cross-simulator R² comparable to within-simulator R² from standard ML; or at least significantly better than single-simulator training

## Critical Reading: What This Paper Does Well and Limitations

### Strengths

1. **Systematic and reproducible:** Tests multiple simulators, multiple architectures, and reports error bars and statistical significance. This is how reproducibility research should be done.

2. **Direct relevance to community:** Most ML papers in 21cm cosmology cite "good within-simulator performance" as validation. This paper shows why that is meaningless for real applications.

3. **Attribution analysis:** Doesn't just report that networks fail; explains *why* by showing what features they learned. This mechanistic insight is crucial.

4. **Clear implications:** The paper is explicit that this is not fixable by better engineering or better architectures, but requires rethinking what we infer.

### Caveats and Gaps

1. **Limited simulator set:** The paper tests against a few simulators. More simulators would strengthen claims about which morphological features cause failures.

2. **Observable choices:** The analysis focuses on specific outputs (e.g., $\bar{x}_\text{HII}(z)$) or full maps. Other observables (bispectrum, void statistics, etc.) might show different reproducibility behavior.

3. **No solution proposed:** Sooknunan et al. diagnose the problem but don't test any solutions. [[Solt et al 2026 (Multi-Simulator Training)]] and the thesis do this.

4. **Attribution analysis is qualitative:** Saliency maps are useful but somewhat subjective. Quantitative metrics for "how simulator-specific are the learned features" would be stronger.

5. **Doesn't test EFT approach:** The paper doesn't explicitly test whether EFT coefficients would avoid the reproducibility failures. This is where the thesis contributes.

## Why This Is the Most Comprehensive Reproducibility Study

Before Sooknunan et al., simulator dependence was demonstrated in individual cases:
- [[Zhou & La Plante 2022 (CNN Reionization)]]: one architecture (CNN), one comparison (21cmFAST → zreion)
- Scattered discussion in other papers

Sooknunan et al. elevates this to:
- **Multiple architectures:** CNNs, MLPs, (possibly ViTs)
- **Multiple simulator pairs:** not just two simulators but a matrix of comparisons
- **Quantitative metrics:** detailed error analysis, not just "it fails"
- **Mechanistic understanding:** attribution analysis showing what went wrong
- **Statistical rigor:** error bars, significance tests, multiple random seeds

This comprehensive approach makes it clear the problem is **fundamental and pervasive**, not a quirk of one architecture or one simulator pair.

## Implications for Inference Strategy

### Why Standard ML Benchmarking Is Misleading

The standard ML benchmarking in 21cm papers:
```
1. Generate simulated data from Simulator A
2. Train network on 80% of data
3. Test on held-out 20% of Simulator A
4. Report low error; claim success
5. Publish
```

This workflow is **perfectly calibrated to hide cross-simulator problems.** The 20% test set comes from the same simulator, same parameter distributions, same morphology distribution as the training set. The network can overfit to simulator-specific patterns and still get low errors.

**What Sooknunan et al. shows:** You must test on a different simulator to learn whether the network learned real physics or simulator artifacts.

### Recommended Benchmarking for 21cm ML

- **Minimum:** Train on Simulator A, test on Simulator B (different code)
- **Better:** Train on multiple simulators, test on held-out simulator
- **Best:** Quantify the morphological distance between simulators, show reproducibility vs. morphological distance

## Open Questions Motivated by This Paper

> [!gap]
> **EFT coefficient stability:** Do EFT coefficients suffer from the same cross-simulator reproducibility failures? Or are they stable by construction (because they are defined by physics, not by learned morphological features)? P1 directly answers this.

> [!gap]
> **What are the minimal features for cross-simulator generalization?** Sooknunan et al. shows that arbitrary learned features are simulator-specific. What is the minimal set of statistics/features that are truly universal? EFT coefficients are candidates, but others might work too (e.g., power spectrum moments, bispectrum in certain limits).

> [!gap]
> **Can multi-simulator training really fix this?** [[Solt et al 2026 (Multi-Simulator Training)]] shows improvements, but is the problem truly solved or just ameliorated? Does the improvement come from averaging morphologies or from learning universal features?

> [!gap]
> **Other observables:** Do the same reproducibility failures occur for other statistics (bispectrum, void probability, reionization bubble size distribution)? Or are some statistics more robust across simulators than others?

## For Your Thesis: Why This Paper Is Foundational

Reading Sooknunan et al. makes it clear that:

1. The problem (cross-simulator generalization in ML) is real, quantified, and not going away with better engineering
2. The solution must be conceptual: change what we infer, not how we infer it
3. EFT coefficients are a principled candidate for "what to infer" because they are defined by physics, not by learned morphology
4. P1 and P2 are not just interesting; they are **necessary** to establish that the EFT approach actually solves the problem Sooknunan et al. characterize

This paper transforms the thesis from "an interesting idea about EFT" to "a direct and empirically motivated response to a critical limitation of current 21cm inference methods."
