---
type: domain
title: "Inference and ML"
created: 2026-04-14
updated: 2026-04-16
tags:
  - domain/inference
  - domain/ml
status: mature
related:
  - "[[Simulation and Codes]]"
  - "[[Effective Field Theory]]"
  - "[[Simulator Dependence]]"
---

# Inference and ML

## The Inference Problem

Given 21cm observations (power spectra, images, cross-spectra with galaxy surveys), infer astrophysical parameters ($\zeta$, $T_\text{vir}$, $R_\text{mfp}$) and/or cosmological parameters (tensor-to-scalar ratio $r$, tilt $n_s$, etc.). 

**Why this is hard:**
- The likelihood $P(\text{data} \mid \theta)$ is **intractable** — there is no closed-form formula
- Simulations are **stochastic**: different random seeds produce different 21cm outputs for the same parameters
- The data space is **high-dimensional**: a single 21cm observation cube contains $\sim 10^6$ to $10^7$ voxels
- The likelihood could be multimodal (multiple parameter sets produce similar observables)

**Standard approaches are infeasible:**
- MCMC sampling of the likelihood is too slow: each likelihood evaluation requires running a full simulation (~hours to days on a cluster)
- Grid-based methods require too many evaluations to cover parameter space

This motivates **simulation-based inference (SBI)** approaches that bypass direct likelihood evaluation.

## Simulation-Based Inference (SBI): The Full Pipeline

SBI is also called **likelihood-free inference**. Instead of evaluating the likelihood directly, SBI learns the posterior $P(\theta \mid \text{data})$ from a training set of (simulation, params) pairs generated **ahead of time** during a calibration phase.

### The Complete SBI Pipeline

**Step 1: Training Set Generation**
- Sample $N_\text{train}$ parameter sets from a prior $p(\theta)$ (typically uniform over the astrophysical parameter space of interest)
- For each parameter set, run a fast simulation (21cmFAST takes ~1-10 seconds per realiz, scalable to 1000s)
- Extract summary statistics (power spectra, cross-powers) from each simulation
- Result: a dataset $\{(\mathbf{s}_i, \theta_i)\}_{i=1}^{N_\text{train}}$ where $\mathbf{s}_i$ is the summary statistic and $\theta_i$ is the parameter vector

**Typical training set sizes:**
- Proof-of-concept: ~100 simulations
- Reasonable inference: ~500-1000 simulations
- High-accuracy (SKA-era): ~5000-10000 simulations
- Training time: 100-1000 CPU-hours for 21cmFAST

**Step 2: Summary Statistics (Compression)**
- The raw simulation outputs are too high-dimensional to train ML models directly
- Extract **compressed statistics** that retain most information but reduce dimensionality
- Common choices:
  - **1D power spectrum:** $P_{21}(k_1, z_1), P_{21}(k_2, z_1), \ldots$ ~50-100 numbers per redshift bin
  - **2D power spectrum:** $P_{21}(k_\perp^i, k_\parallel^j)$ ~500-1000 numbers
  - **Cross-power spectrum:** $P_{21 \times g}(k)$ ~50-100 numbers
  - **Neural summaries:** learned compressed representations via VAE or autoencoder (~64-256 dimensions)

**Why compression is essential:** Full images (1000³ pixels) cannot be used directly; even 21cm lightcone cubes (1024³ voxels) are too large. Compression to power spectra or neural features is mandatory.

**Step 3: Density Estimation (Learning the Posterior)**
- Train a **density estimator** (e.g., normalizing flow, neural network) that maps $\mathbf{s} \to P(\theta \mid \mathbf{s})$
- Common architectures:
  - **Normalizing flows:** Continuous, invertible transformations of a simple distribution (e.g., Gaussian) to the posterior. Excellent for capturing multi-modality and correlations.
  - **Neural posterior estimation (NPE):** A neural network directly parameterizes the posterior at each summary point
  - **Ratio-based methods (TMNRE, swyft):** Learn the likelihood ratio $P(\mathbf{s}, \theta) / [P(\mathbf{s}) P(\theta)]$ instead of the posterior directly

**Training time:** 1-100 GPU-hours depending on architecture and training set size

**Step 4: Inference on Observed Data**
- Given an observed 21cm dataset $\mathbf{s}_\text{obs}$, pass it through the trained density estimator
- Obtain a posterior sample or posterior distribution $P(\theta \mid \mathbf{s}_\text{obs})$
- Extract credible intervals, point estimates, marginalized posteriors

**Time to inference:** ~1 second (amortized inference)

### Key Bottlenecks

1. **Simulation generation** (most expensive): 100-1000 CPU-hours for a training set
2. **Summary statistics design:** Choosing the right compression is critical; poor compression wastes information
3. **Neural network training:** 1-100 GPU-hours; requires careful hyperparameter tuning
4. **Coverage & calibration:** Must validate that the learned posterior accurately represents the true posterior (see [[Cross-Simulator Generalization]])

## Variant Inference Strategies

### Amortized vs. Sequential SBI

**Amortized inference** (most common):
- Train a single model on the entire prior volume
- Once trained, the model can be applied to any observed dataset instantly (amortized over many datasets)
- Efficient if you expect many analyses (e.g., many 21cm fields from a survey)
- **All methods used in 21cm to date are amortized**

**Sequential (adaptive) inference:**
- Start with a broad prior
- Observe data → run inference → identify region of parameter space where posterior is non-negligible
- Reweight prior to focus on this region → train new model → repeat
- Methods: SNPE-C (Sequential Neural Posterior Estimation, Conditional), active learning approaches
- **Advantage:** More efficient for very high-dimensional parameter spaces or precise constraints
- **Disadvantage:** Requires multiple rounds of training and inference; slower per-dataset but fewer simulations overall
- Not yet routine in 21cm work (computational cost); more common in particle physics (LHC analyses)

### Ratio Estimation: TMNRE and swyft

The **Truncated Marginal Neural Ratio Estimation (TMNRE)** algorithm (also implemented in the swyft package) is the most used method in 21cm SBI. It works by:

1. **Learning the likelihood ratio:** Instead of learning $P(\theta \mid \mathbf{s})$ directly, learn:
$$
r(\mathbf{s}, \theta) = \frac{P(\mathbf{s}, \theta)}{P(\mathbf{s}) P(\theta)}
$$
where $P(\mathbf{s}) = \int P(\mathbf{s}, \theta) d\theta$ is the marginal likelihood.

2. **Local amortization:** The ratio is learned locally around the observed datapoint, not globally over the entire prior. This makes the problem more tractable: the neural network only needs to distinguish $P(\mathbf{s}_\text{obs}, \theta)$ from noise, not learn the full high-dimensional density.

3. **Neyman-Pearson connection:** The learned ratio directly relates to the **Neyman-Pearson lemma** from statistics: the likelihood ratio is the most powerful test statistic. By learning it accurately, you maximize constraining power.

4. **Sampling the posterior:** Once you have $r(\mathbf{s}_\text{obs}, \theta)$, you can compute:
$$
P(\theta \mid \mathbf{s}_\text{obs}) \propto r(\mathbf{s}_\text{obs}, \theta) P(\theta)
$$
and sample from it using MCMC or other samplers.

**Advantages of TMNRE/swyft:**
- **Memory efficient:** Only stores a neural network classifier, not full density estimator
- **Flexible:** Can use different neural architectures (MLPs, CNNs, transformers)
- **Empirically powerful:** Achieves excellent constraints on 21cm-like synthetic data
- **Active learning ready:** Can be extended to sequential inference

**Typical implementation in 21cm:**
- swyft (Miller et al. 2022): Python package; uses masked autoregressive flows (MAF) as the density model
- Custom implementations: some groups write their own ratio estimators

## Why Normalizing Flows Are the Right Tool for SBI Posteriors

Normalizing flows are bijective neural networks that transform a simple distribution (e.g., standard Gaussian) to an arbitrary target distribution via a series of invertible transformations. They are ideal for SBI because:

1. **Multi-modality:** Unlike Gaussian-based methods, flows can represent multi-modal posteriors. This matters for reionization parameters where multiple combinations of $(\zeta, T_\text{vir})$ can produce similar 21cm power spectra.

2. **Correlations:** The posterior over 21cm parameters is highly correlated (e.g., increasing $\zeta$ has similar effects to increasing $T_\text{vir}$). Flows naturally capture these correlations via their flexible learned transformations.

3. **Non-Gaussianity:** The posterior can be highly non-Gaussian, especially at high redshifts or when observational constraints are strong. Flows handle this without assumptions.

4. **Invertibility:** Flows are invertible, allowing both forward sampling (generate $\theta \sim P(\theta | \mathbf{s})$) and density evaluation (compute $P(\theta | \mathbf{s})$ at any point).

5. **Compared to MCMC:** MCMC struggles in high dimensions due to step-size tuning and slow mixing. Flows give instant samples and don't require tuning.

**Contrast with simpler alternatives:**
- **Gaussian posterior:** Assumes unimodal, normal distribution; fails for multi-modal posteriors
- **Histogram binning:** Inefficient in high dimensions (curse of dimensionality)
- **MCMC:** Slow per-dataset; requires tuning; difficult in high dimensions

## The Curse of Dimensionality for 21cm

A 21cm lightcone has approximately:
- Sky area: ~1-100 deg²
- Frequency bandwidth: ~50-200 MHz (corresponding to $\Delta z \sim 5-20$)
- Frequency resolution: ~1 MHz (enough to resolve Ly$\alpha$ structure)
- Result: ~10⁶ to 10⁷ independent voxels

**Why compression is mandatory:**
- Training a neural network with 10⁷-dimensional input is infeasible (memory, computation, curse of dimensionality)
- Data compression to power spectra reduces this to ~100-1000 dimensions
- Further neural compression (ViT, CNN autoencoders) can reduce to ~50-256 dimensions
- Trade-off: compression removes some information, but is necessary for tractability

**Compression strategies in current use:**
- **Power spectrum + cross-spectrum:** Industry standard; loses directional information but captures most statistical information
- **2D power spectrum:** Better foreground handling; increases dimensionality slightly
- **Neural summaries (SKATR):** Use vision transformers to learn simulator-agnostic representations; maintains more information but less interpretable
- **Wavelets:** Capture multi-scale structure; intermediate between power spectrum and raw image

## Evaluating SBI Performance: Beyond R²

Standard metrics like $R^2$ (coefficient of determination) are insufficient for SBI. A model can have high $R^2$ on training data but still produce poorly-calibrated posteriors. Key validation metrics:

### 1. Coverage Tests (TARP)

**Testing Averaged Ranked Probability (TARP):**
- For each test case, compute the cumulative posterior probability $\alpha_i$ below the true parameter value (for each parameter dimension)
- The set $\{\alpha_1, \ldots, \alpha_N_\text{test}\}$ should be uniformly distributed on [0, 1] if the posterior is well-calibrated
- Plot: fraction of true values below $\alpha$ threshold vs. $\alpha$. A 45° line indicates perfect calibration; deviations indicate miscalibration.
- **If posterior is too narrow:** Points cluster near $\alpha = 0$ or $\alpha = 1$ (over-confident)
- **If posterior is too wide:** Points cluster near $\alpha = 0.5$ (under-confident)

### 2. Simulation-Based Calibration (SBC)

- Generate new test simulations from the prior (not from the training set)
- Infer parameters using the trained SBI model
- For each parameter and each test case, compute the rank of the true parameter value within posterior samples
- If the posterior is well-calibrated, the ranks should be uniformly distributed

### 3. Posterior Predictive Checks

- Sample from the learned posterior
- Generate new synthetic data from the model at these samples
- Compare the distribution of synthetic data to the observed data
- If they match, the posterior is reasonable

### 4. Chi-Squared Tests (Insufficient Alone)

- Compute $\chi^2 = \sum_i (d_i - m_i)^2 / \sigma_i^2$ where $d_i$ is data, $m_i$ is model at posterior mean, $\sigma_i$ is noise
- For a good fit, $\chi^2 \sim N_\text{dof}$ with small variance
- **Limitation:** High $\chi^2$ may indicate poor fit, but low $\chi^2$ doesn't guarantee the posterior is correct (could be under-constrained)

## The Amortization Gap

The difference between the amortized posterior $P_\text{amortized}(\theta | \mathbf{s})$ and the optimal posterior $P_\text{optimal}(\theta | \mathbf{s})$ is the **amortization gap**. 

**Why it exists:**
- Amortized inference trains a single model to work for **all** possible summaries
- Optimal inference (sequential/adaptive) optimizes locally for each specific observation
- Amortized models are necessarily less accurate because they must cover the full prior space

**How to minimize it:**
- Larger training sets → smaller gap
- Better summary statistics → smaller gap (less information lost)
- More flexible neural architecture → smaller gap

**Typical size:** For 21cm SBI with 500-1000 training simulations, the amortization gap is ~10-20% of the credible interval width.

## The Cross-Simulator Generalization Problem

This is the central problem P2 addresses (see also [[Simulator Dependence]]). Models trained on one code fail on another because they learn simulator-specific morphological features.

### Three Empirical Failure Modes

1. **Zhou & La Plante 2022: CNN failure across codes**
   - CNN trained on 21cmFAST → tested on zreion
   - Systematic bias of ~30% in inferred $\zeta$

2. **Berklas & Pober 2025: Within-code model dependence**
   - 21CMMC trained on 21cmFAST with different recombination models
   - Posterior shifts of 1-2 σ depending on model choice

3. **Sooknunan et al. 2024: ML reproducibility failure**
   - 10+ ML architectures, all fail cross-simulator
   - In-code R² = 0.90–0.95 vs. cross-code R² = 0.35–0.55

## Current Approaches to Cross-Simulator Generalization

### 1. Multi-Simulator Training (Solt et al. 2026)

Train on pooled data from multiple codes simultaneously.

**Strengths:**
- Empirically improves OOD performance
- Simple to implement

**Limitations:**
- No physical basis for what is being learned
- Only works if training set contains target code
- Discards spatial information (uses $\Delta z$ scalar target)

### 2. EFT-Informed Inference (Thesis P2)

Target EFT coefficients instead of native parameters.

**Hypothesis:** EFT coefficients are more stable across codes because they are defined by physics, not simulators.

**Prediction:** Cross-simulator R² should improve by factor ~2-5 compared to native parameter inference.

### 3. Self-Supervised Representations (Ore et al. 2025, SKATR)

Use Vision Transformer with contrastive learning to obtain simulator-agnostic features.

**Strengths:**
- Demonstrated empirically to work
- Data-driven; no physical assumptions

**Limitations:**
- Black-box; hard to interpret
- Requires large unlabeled training set

## Input Summary Statistics: Comparison

| Statistic | Dimensionality | Information | Foreground Handling | Code-Dependence |
|-----------|-----------------|-------------|-------------------|-----------------|
| 1D power spectrum | 50-100 | Good | Via wedge removal | High (morphology) |
| 2D power spectrum | 500-1000 | Excellent | Direct wedge excision | High |
| 21cm × galaxy cross | 50-100 | Good | Via cross-correlation | Lower (depends on sources) |
| ViT embeddings | 64-256 | Excellent | Automatic | Lower (learned) |

## The Alternative: Self-Supervised Summaries (SKATR)

[[Ore et al 2025 (SKATR)]]: Self-supervised ViT learns simulator-agnostic representations empirically. The method:

1. Train a Vision Transformer on unlabeled 21cm images from multiple codes
2. Use contrastive learning (SimCLR or similar) to learn features invariant to simulator choice
3. Use these features as input to a second-stage SBI model
4. Achieved cross-simulator generalization without explicit EFT model

**Complementarity to EFT approach:**
- **P2 (EFT):** physics-informed, interpretable, uses theory to guide the representation
- **SKATR:** data-driven, interpretable via attention maps, discovers simulator-agnostic features empirically

Both target the same root problem ([[Simulator Dependence]]) but via different routes.

## Key Inference Methods and Software

### 21cm-Specific Pipelines

| Method | Reference | Status | Output |
|--------|-----------|--------|--------|
| 21cmMC | Greig & Mesinger | Mature | MCMC chains; slow but proven |
| 21cmEMU | Bye et al. 2022 | Active | ML emulator of 21cmFAST |
| EoRFlow | [[Pietschke et al 2025 (EoRFlow)]] | Active | SBI for $x_\text{HI}(z)$ from 2DPS |
| EoRFlow + cross-power | [[Pietschke et al 2026 (cross-correlation)]] | Active | SBI for source parameters via cross-spectrum |
| SKATR | [[Ore et al 2025 (SKATR)]] | Active | Cross-simulator ViT + SBI |
| Multi-simulator training | [[Solt et al 2026 (Multi-Simulator Training)]] | Active | Scalar targets; improves OOD generalization |
| SKA + CMB joint SBI | [[Schosser et al 2025 (Starobinsky)]] | Active | NPE with flow matching; inflation tests |

### General SBI Software

| Package | Language | Method | Maturity |
|---------|----------|--------|----------|
| sbi | Python | NPE/NLE/NRE (Macke lab) | Mature; canonical reference: [[Deistler et al 2025 (SBI Guide)]] |
| swyft | Python | TMNRE | Mature; widely used in cosmology |
| lampe | Python | TMNRE; ratio est. | Active; new; excellent for large-scale problems |
| nflows | Python | Normalizing flows | Mature; building block for custom SBI |
| Pyro | Python | Probabilistic programming; SMC-ABC | Mature; general-purpose |
| pydelfi | Python | Density estimation via implicit likelihood | Mature; old but still used |

## Key Concepts

- [[Simulation-Based Inference]]
- [[Neural Posterior Estimation]]
- [[Normalizing Flows]]
- [[Power Spectrum as Summary Statistic]]
- [[2D Power Spectrum]]
- [[Cross-Power Spectrum]]
- [[Simulator Dependence]]
- [[Training Set Generation]]
- [[Cross-Simulator Generalization]]
- [[Self-Supervised Learning]]
- [[Vision Transformer]]

## Key Entities

- [[swyft]] — neural ratio estimation framework
- [[lampe]] — improved SBI pipeline
- [[21cmFAST]] — primary simulator for training sets
- [[SCRIPT]] — secondary simulator for P1
- [[py21cmfast]] — Python wrapper for 21cmFAST
- [[EoRFlow]] — end-to-end SBI pipeline for 21cm

## Sources

### EFT Theory (Inference Targets)
- [[McQuinn & D'Aloisio 2018]] — foundational EFT / bias expansion
- [[Qin et al 2022 (EFT Redshift Space)]] — redshift-space EFT; THESAN validation
- [[Sailer et al 2022 (Optical Depth EFT)]] — τ forecasts from EFT-based 21cm analysis
- [[Baradaran et al 2024 (Hybrid EFT)]] — hybrid EFT with N-body accuracy

### Simulator Dependence (Core Problem)
- [[Berklas & Pober 2025]] — within-code model dependence in 21CMMC
- [[Zhou & La Plante 2022 (CNN Reionization)]] — CNN failure 21cmFAST → zreion
- [[Sooknunan et al 2024 (ML Reproducibility)]] — systematic ML reproducibility failure across codes

### Mitigation Strategies
- [[Solt et al 2026 (Multi-Simulator Training)]] — multi-simulator training; empirical baseline
- [[Ore et al 2025 (SKATR)]] — self-supervised transformer; cross-simulator generalization

### SBI Pipelines
- [[Pietschke et al 2025 (EoRFlow)]] — EoRFlow SBI framework; 2DPS + TMNRE
- [[Pietschke et al 2026 (cross-correlation)]] — 21cm × galaxy cross-power SBI
- [[Schosser et al 2025 (Starobinsky)]] — joint SKA+CMB SBI; flow matching
- [[Duruisseaux et al 2026 (FNO)]] — Fourier Neural Operators; emulator architecture

### General SBI Theory
- [[Miller et al 2022 (swyft)]] — swyft framework; TMNRE details
- [[Gnedin & Madau 2022 (Modeling Reionization)]] — simulation codes background
