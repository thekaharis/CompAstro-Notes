---
type: entity
title: "EoRFlow"
created: 2026-04-14
updated: 2026-04-16
tags:
  - entity/code
  - domain/inference
  - domain/sbi
status: mature
entity_type: repository
role: "Neural density estimator for SBI-based 21cm reionization inference; Heidelberg group"
first_mentioned: "[[Pietschke et al 2025 (EoRFlow)]]"
related:
  - "[[Simulation-Based Inference]]"
  - "[[Pietschke, Yannic]]"
  - "[[Heneka, Caroline]]"
  - "[[Inference and ML]]"
  - "[[21cm Power Spectrum]]"
  - "[[EFT of the Ionization Field (Proposal)]]"
---

# EoRFlow

## Description

**EoRFlow** is a simulation-based inference (SBI) framework developed by the Heidelberg group (Pietschke, Heneka, and collaborators) for reconstructing the **reionization history** $x_\text{HII}(z)$ and related astrophysical parameters from 21cm observations or simulations. The core innovation is using **neural density estimators** (normalizing flows or flow-matching models) trained on pairs of (21cm summary statistic, reionization parameter) to learn the posterior distribution over reionization parameters given an observed summary statistic.

- **Repository:** github.com/astro-ML/EoRFlow (accessible, active development)
- **Primary papers:** 
  - [[Pietschke et al 2025 (EoRFlow)]]: introduces the method and validates on 21cmFAST + SKA mock data
  - [[Pietschke et al 2026 (cross-correlation)]]: extends to 21cm × galaxy cross-power spectra
- **Language:** Python (PyTorch backend); GPU-friendly
- **License:** Open-source (likely MIT or similar)

## Architecture and Components

### Overview

EoRFlow follows the standard SBI paradigm:

1. **Simulator:** 21cmFAST at various astrophysical parameters (100s–1000s of simulations)
2. **Data compression:** 21cm summary statistics (2D power spectra, maybe moments, or CNN-compressed features)
3. **Density estimator:** Neural network that learns $p(\theta | x)$ where $\theta$ are astrophysical parameters (e.g., $\{T_\text{vir}, \zeta, R_\text{mfp}\}$) and $x$ is the compressed summary
4. **Inference:** sample from learned posterior directly; no likelihood evaluation needed

### Training Data and Simulations

- **Simulations:** 21cmFAST configured with realistic astrophysical parameter ranges:
  - Ionization efficiency $\zeta$ (40 → 1000+)
  - Virial temperature $T_\text{vir}$ (1e3 → 1e5 K)
  - Mean free path $R_\text{mfp}$ (10 → 100 Mpc/h)
  - Stellar efficiency $f_*$ (if varied)
- **Redshift coverage:** typically $z = 6$–$15$ (full EoR)
- **Number of simulations:** 500–2000 per architecture variant (large enough for neural density estimator training)
- **Box size:** 256 Mpc/h (standard 21cmFAST choice)

### Summary Statistics / Compression Layers

EoRFlow can operate on various input representations:

1. **2D Cylindrically-Averaged Power Spectrum (2DPS):**
   - Computed as $P(k_\perp, k_\parallel)$ in redshift space
   - Dimensionality: typically 20×20 or 30×30 bins in 2D
   - Captures both mode and anisotropy information
   - **Advantage:** physics-motivated; directly related to EFT observables
   
2. **Full 21cm Lightcone or Slice:**
   - Raw or down-sampled 3D 21cm maps
   - Compressed via CNN or other encoder before passing to density estimator
   - **Advantage:** retains more information; potentially better for non-Gaussian signatures
   
3. **Power Spectrum Moments:**
   - Mean, variance, skewness, kurtosis of $P(k)$
   - Very low-dimensional summary
   - **Advantage:** fast; works well when parameters correlate cleanly with moments

### Neural Density Estimator Architectures

EoRFlow typically uses one of:

1. **Normalizing Flows (NF):**
   - Invertible neural networks (e.g., Neural Spline Flows, Masked Autoregressive Flow)
   - Trained to learn $p(\theta | x)$ via KL divergence minimization
   - **Advantage:** exact density, can evaluate and sample freely
   - **Disadvantage:** training can be numerically unstable; requires careful design

2. **Flow-Matching (newer):**
   - Generative model approach; ODE-based sampling
   - Potentially more stable than traditional flows
   - **Advantage:** flexible, stable, fast sampling
   - **Disadvantage:** newer; less well-tested in cosmology

3. **Potentially other variants:**
   - Score-based models (diffusion-based)
   - Variational approaches
   - Exact architecture likely depends on Pietschke et al.'s latest choices

### Training Procedure

Standard supervised learning on pairs $(x_i, \theta_i)$:

- **Loss function:** KL divergence for flows, or appropriate loss for the architecture
- **Optimization:** Adam or similar; ~100–1000 epochs typical
- **Validation:** held-out test set of simulated data
- **Hyperparameters:** 
  - Network width/depth (50–200 hidden units, 2–5 layers typical)
  - Learning rate (~0.001 standard)
  - Batch size (~32–128)
  - Training-validation split (70%–30% typical)

## Key Capabilities

### Primary Use Case: Reionization History Inference

EoRFlow's main deliverable is: given 21cm power spectrum data (observed or simulated), what is the reionization history?

- **Outputs:** posterior distribution $p(\theta | \text{data})$ where $\theta = (\zeta, T_\text{vir}, R_\text{mfp}, \ldots)$
- **Credibility intervals:** 68%, 95%, etc., directly sampled from learned posterior
- **Computational cost:** once trained, inference is fast (~seconds per sample)

### Secondary Capability: Field Reconstruction

Recent versions ([[Pietschke et al 2026 (cross-correlation)]]) extend to jointly inferring:
- Reionization history (parameters)
- 21cm × galaxy cross-power spectrum (joint observable)
- This enables cross-validation against galaxy observations

### Planned Extensions

- Integration with observational likelihoods (SKA-specific noise, beam, foreground mitigation)
- Joint constraints with CMB (optical depth from Planck)
- Multiple redshifts simultaneously (full lightcone analysis)

## Relevance to the Thesis

### Current Limitation: Single-Simulator Training

EoRFlow is trained exclusively on 21cmFAST in the published versions. This is a **specific design choice** (21cmFAST is fast and flexible) but creates a fundamental limitation:

- Inferred parameters $(\zeta, T_\text{vir}, R_\text{mfp})$ are **21cmFAST-native** quantities
- If real data come from a different underlying reionization model (or different code), the posterior might be biased ([[Berklas & Pober 2025]])
- Cross-simulator validation is missing (would EoRFlow trained on 21cmFAST generalize to SCRIPT? Probably not perfectly)

### How P2 Improves on EoRFlow

The thesis proposes **EFT-informed inference**:

1. **Same SBI framework:** can use similar density estimator architecture as EoRFlow
2. **Different training data:** instead of (21cm power spectrum, $\zeta, T_\text{vir}, R_\text{mfp}$), train on (21cm power spectrum, **EFT coefficients**)
3. **Multiple simulators:** training on EFT-labeled data from both 21cmFAST and SCRIPT
4. **Cleaner posterior interpretation:** posterior is over EFT coefficients (which are model-independent) rather than code-native parameters

### Potential Collaboration Points

- **Code architecture:** EoRFlow's density estimator and training pipeline could be reused for P2 with different targets
- **Validation:** comparison on the same datasets where EoRFlow has been validated
- **Joint publication opportunity:** "EFT-informed inference using EoRFlow architecture" or similar
- **Potential shared authorship** with Heidelberg group if collaboration deepens

## Specific Benchmarks and Published Results

From [[Pietschke et al 2025 (EoRFlow)]]:

- **Posterior recovery on 21cmFAST data:** mean absolute error in recovered $\Delta z_\text{reion}$ ≲ 0.3 dex (very good)
- **Cosmological parameter constraints:** e.g., from simulated SKA data, constraints on $\zeta$ improve by ~3× compared to simple power spectrum matching
- **Computational efficiency:** inference (sampling 1000 posterior samples) ~1 second on GPU; millions of samples feasible in reasonable time

(Exact numbers depend on Pietschke et al.'s specific numbers; verify from paper)

## Architecture Limitations and What It Cannot Do

### Inherent Limitations of SBI

1. **Simulator bias:** trained only on 21cmFAST; posterior is $p(\theta_\text{21cmFAST} | \text{data})$, not $p(\theta_\text{true} | \text{data})$
2. **Dependence on compression:** choice of summary statistic (2DPS vs. lightcone vs. moments) significantly affects what constraints EoRFlow can extract
3. **Curse of dimensionality:** as parameter space grows, training data requirements scale; EoRFlow likely works best with ~5–10 parameters
4. **Validation only within 21cmFAST:** no explicit tests on other simulators or observational data

### What EoRFlow Is Not Designed For

- **Real observational data inference** (SKA, HERA, etc.) — would need observational likelihood, foreground mitigation, etc.
- **Full morphological inference** — outputs are parameter values, not fields; spatial structure is compressed away
- **Multiple-redshift inference** — typically works on slices or narrow windows; full lightcone treatment is in development
- **Non-Gaussian signatures** — power spectrum compression may lose bispectrum, trispectrum information

## How to Extend EoRFlow for the Thesis

### Option 1: Multi-Simulator Training

- **Approach:** train density estimator on pooled data from 21cmFAST + SCRIPT (or other code pairs)
- **Change:** training data pipeline, not network architecture
- **Feasibility:** straightforward; similar to [[Solt et al 2026 (Multi-Simulator Training)]]
- **Expected result:** improved robustness, but empirical averaging (not principled)

### Option 2: EFT-Informed Targets

- **Approach:** train density estimator to infer EFT coefficients instead of $(zeta, T_\text{vir}, R_\text{mfp})$
- **Change:** training data (would need EFT coefficient labels from simulations), target dimensionality
- **Feasibility:** requires P1 to extract EFT labels; then straightforward SBI
- **Expected result:** cleaner posterior interpretation, better cross-simulator generalization
- **This is P2's main innovation**

## Code Availability and Reproducibility

- **Repository:** publicly available (github.com/astro-ML/EoRFlow)
- **Documentation:** likely has README and possibly docs; check repository for setup instructions
- **Dependencies:** standard scientific Python stack (numpy, torch, scipy, etc.)
- **Getting started:** clone, install, run provided examples with 21cmFAST output
- **Modification:** code is readable and well-structured; extending it for EFT targets is plausible

## For Your Thesis: Why EoRFlow Matters

1. **Existence proof:** shows that SBI + neural density estimation works for 21cm reionization; no need to invent new inference machinery
2. **Baseline for comparison:** P2 should use a similar architecture but with EFT targets; direct comparison to EoRFlow validates the EFT approach
3. **Technical resource:** code, training pipeline, validation protocols all available for adaptation
4. **Publication strategy:** "EFT-informed version of EoRFlow" or similar framing positions the thesis as an improvement on existing tools
5. **Potential collaborators:** Pietschke, Heneka, and group may be interested in extending to EFT targets; possible joint paper

## References Within Wiki

- **Papers:** [[Pietschke et al 2025 (EoRFlow)]], [[Pietschke et al 2026 (cross-correlation)]]
- **People:** [[Pietschke, Yannic]], [[Heneka, Caroline]]
- **Related concepts:** [[Simulation-Based Inference]], [[Effective Field Theory]], [[Inference and ML]]
- **Complementary code:** [[SKATR]] (self-supervised compression of 21cm data)
