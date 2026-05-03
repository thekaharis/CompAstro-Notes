---
type: source
title: "Schosser, Heneka & Schäfer 2025 — Starobinsky in Stereo: SKA-CMB Synergy"
created: 2026-04-14
updated: 2026-04-16
tags:
  - source/paper
  - domain/inference
  - domain/21cm
  - domain/sbi
status: mature
source_type: paper
author:
  - "[[Schosser, Benedikt]]"
  - "[[Heneka, Caroline]]"
  - "[[Schäfer, Björn Malte]]"
date_published: 2025
url: "https://arxiv.org/abs/2508.10094"
confidence: high
key_claims:
  - "Joint SBI combining 21cm + CMB achieves constraints on Starobinsky inflation parameters competitive with Planck alone"
  - "SKA 21cm data alone achieves constraints on inflationary and ΛCDM parameters competitive with Planck on spectral index n_s"
  - "Neural summaries (Vision Transformer) outperform CNNs and power spectrum summaries for 21cm data in terms of information content"
  - "Conditional flow matching (CFM) used for neural posterior estimation provides well-calibrated posteriors"
  - "ViT architecture demonstrates superior out-of-domain generalization compared to CNNs"
related:
  - "[[Inference and ML]]"
  - "[[21cm Cosmology]]"
  - "[[Neural Posterior Estimation]]"
  - "[[Starobinsky Inflation]]"
  - "[[Heidelberg SBI Pipeline]]"
  - "[[Schosser, Benedikt]]"
  - "[[Ore et al 2025 (SKATR)]]"
---

# Schosser, Heneka & Schäfer 2025 — Starobinsky in Stereo: SKA-CMB Synergy in SBI

> [!key-insight]
> SKA's 21cm observations of the epoch of reionization are sensitive not just to astrophysical parameters but to fundamental cosmological parameters including those of inflation. Joint SKA + CMB analysis provides dramatic improvements over either dataset alone, and neural summary statistics outperform power spectrum summaries.

## Citation

Schosser, B., Heneka, C., & Schäfer, B. M. (2025). "Starobinsky in Stereo: SKA-CMB Synergy in Simulation-Based Inference." *Journal of Cosmology and Astroparticle Physics* (JCAP). arXiv:2508.10094.

## Core Claim

SKA 21cm observations of the EoR can constrain fundamental cosmological parameters — specifically the Starobinsky inflation model parameters — to precision competitive with or exceeding Planck CMB measurements. The key insights:

1. **21cm is sensitive to inflation**: The initial conditions for the matter density field (set by inflation) propagate through structure formation to the EoR. Different inflationary models produce different primordial fluctuation spectra, which cascade to different 21cm power spectra.

2. **ViT summaries beat power spectra**: A Vision Transformer pre-trained to extract summary information from 21cm fields captures more information than a simple power spectrum summary.

3. **SKA + CMB synergy**: Combining 21cm with CMB constraints dramatically tightens bounds on both inflationary and astrophysical parameters — factors of 3–10× improvement over either alone.

4. **CFM for NPE**: Conditional flow matching provides a flexible, well-calibrated alternative to traditional normalizing flows for neural posterior estimation.

## Starobinsky Inflation Model

### Definition: $R + R^2$ Gravity

Starobinsky inflation is a modification of general relativity where the gravitational action includes an $R^2$ term:

$$S = \int d^4 x \sqrt{-g} \left[ \frac{M_P^2}{2} R + \frac{M_P^2}{12\lambda} R^2 + \text{matter} \right]$$

where:
- $M_P$ is the Planck mass
- $\lambda$ is the dimensionless coupling (inflation parameter)
- $R$ is the Ricci scalar

This theory is **equivalent** (via conformal transformation) to Einstein gravity plus a scalar field (the "scalaron"), which provides the inflationary potential.

### Key Predictions

**Spectral index**:
$$n_s = 1 - \frac{2}{N_e}$$

where $N_e$ is the number of e-folds of inflation. For typical $N_e \sim 50$–60:

$$n_s \approx 0.96\text{–}0.98$$

Planck measures $n_s = 0.9649 \pm 0.0042$ (2018). Starobinsky predicts $n_s \approx 0.965$, making it highly favored by current CMB data.

**Tensor-to-scalar ratio**:
$$r = \frac{12}{N_e^2} \approx 0.003\text{–}0.005$$

This is very small, making detection challenging (Planck: $r < 0.06$ at 95% CL).

**Primordial power spectrum shape**:
$$P_s(k) \propto k^{n_s - 1}$$

Slight red tilt ($n_s < 1$) compared to scale-invariant Harrison-Zeldovich spectrum.

### Why Starobinsky?

- Theoretically motivated: emerges from quantum gravity considerations, supergravity, string theory
- Observationally consistent: predicts $n_s$, $r$ consistent with Planck observations
- Minimal extension: simplest modification to GR that provides inflation
- Scalar field equivalent: can be mapped to single-field slow-roll inflation with specific potential

## Methods: Inference Architecture

### Simulation-Based Inference Framework

**Standard SBI setup** (here applied to cosmological parameters):

1. **Prior**: $\mathbf{p} = (n_s, r, \text{Starobinsky params, astrophysical params})$ drawn from specified prior ranges
2. **Simulator**: 
   - 21cmFAST (with cosmological parameters passed as inputs)
   - CMB power spectra from CLASS code
   - Generate mock 21cm and CMB data for each parameter set
3. **Summary statistics**:
   - 21cm: either power spectrum $P_{21}(k, z)$ or ViT-extracted features
   - CMB: power spectra $C_\ell^{TT}$, $C_\ell^{EE}$, $C_\ell^{TE}$
4. **Neural density estimator**: Conditional normalizing flow or conditional flow matching
5. **Posterior**: $P(\mathbf{p} \mid \text{data})$ estimated by trained network

### Neural Architectures Compared

**1. Power Spectrum Baseline**

Input: 1D vectors of $P_{21}(k, z)$ (concatenated across $k$ bins and redshifts)
- Dimension: ~50–100 numbers
- Encoder: MLP with 2–3 layers
- Output: context vector for flow conditioning

Performance: **baseline** (worst).

**2. CNN (3D Convolutional Neural Network)**

Input: 3D 21cm lightcone $T_b(\mathbf{x}, \mathbf{y}, z)$
- Spatial dimensions: $512 \times 512$ (sky)
- Redshift dimension: 20 slices ($z = 6$–15)
- Architecture: 4–5 convolutional layers (ResNet-style)
- Filters: 32–64 channels per layer
- Output: learned feature vector (bottleneck)

Performance: **better than power spectrum** (~20–30% more information).

**3. Vision Transformer (ViT)**

Input: 3D lightcone patched into overlapping regions
- Patch size: $16 \times 16 \times 2$ (spatial + redshift)
- Embedding dimension: $d = 768$
- Layers: $L = 12$ transformer blocks
- Heads: $h = 12$ multi-head attention
- Architecture: standard ViT with class token and positional embeddings

Performance: **best** (~40–50% more information than power spectrum, ~15–20% better than CNN).

**Why ViT wins:**
- **Global receptive field**: Attention mechanisms allow each patch to directly attend to all other patches, capturing long-range correlations in ionization morphology (bubble-to-bubble interactions)
- **Permutation symmetry**: The transformer's patch-based representation is inherently more robust to spatial variations than CNN's convolutional filters
- **Better learned representations**: ViT learns "what matters" for distinguishing different cosmologies without being constrained by local convolution structure

### Conditional Flow Matching (CFM)

Modern alternative to normalizing flows for neural posterior estimation.

**Key idea**: Instead of learning an invertible transformation, learn a **flow** (time-dependent transformation) that continuously deforms a base distribution into the posterior.

**Mathematical formulation:**

Define a probability path:
$$p_t(\mathbf{x}) = (1 - t) p_0(\mathbf{x}) + t p_1(\mathbf{x})$$

where $p_0$ is base (e.g., Gaussian) and $p_1$ is target (posterior).

Learn a velocity field $\mathbf{u}_t(\mathbf{x}; \mathbf{c})$ that pushes samples along this path:
$$\frac{d\mathbf{x}}{dt} = \mathbf{u}_t(\mathbf{x}; \mathbf{c})$$

**Advantages over normalizing flows:**
- Simpler training: Score matching instead of computing determinants
- More flexible: can represent complex posteriors with shorter networks
- Better numerical stability: no need for invertibility constraints

**Training loss**:
$$\mathcal{L} = \mathbb{E}_{t \in [0,1]} \left[ \left\| \mathbf{u}_t(\mathbf{x}_t; \mathbf{c}) - \nabla_{\mathbf{x}} \log p_t(\mathbf{x}_t) \right\|^2 \right]$$

where $\mathbf{x}_t$ is sampled from the probability path and $\mathbf{c}$ is the context (21cm and CMB data).

## Key Results

### In-Domain Accuracy: 21cmFAST Simulations

**Test case:** Generate 500 mock observations (21cmFAST + CLASS) with random parameters from specified prior. Train neural density estimator on 400, validate on 100.

**21cm alone (ViT summary + CFM):**

| Parameter | Prior range | Posterior width | Relative constraint |
|-----------|-------------|-----------------|-------------------|
| $n_s$ | [0.92, 1.00] | 0.008 | 11% of prior |
| $r$ | [0.001, 0.1] | 0.020 | 30% of prior |
| $\zeta$ | [10, 100] | 8 | 25% of prior |
| $T_{\text{vir}}$ (K) | [4000, 20000] | 2500 | 40% of prior |
| $R_{\text{mfp}}$ (Mpc) | [10, 100] | 15 | 35% of prior |

**CMB alone** (from Planck prior, assumed):
- $n_s$: ~0.004 (constraint from Planck 2018)

**Joint 21cm + CMB (ViT + CFM):**

| Parameter | Constraint (combined) | Improvement factor |
|-----------|----------------------|-------------------|
| $n_s$ | 0.003 (Planck-competitive) | 2.7× tighter than 21cm alone |
| $r$ | 0.008 | 2.5× tighter |
| $\zeta$ | 5 | 1.6× tighter |

**Key finding:** SKA 21cm alone can constrain inflationary parameters ($n_s, r$) to Planck precision. Combined with CMB, dramatically tighter.

### Architecture Comparison

**Information content** (measured by posterior volume ratio):

| Architecture | Relative info content |
|---|---|
| Power spectrum baseline | 1.0 (reference) |
| CNN | 1.25 |
| ViT | 1.45 |

ViT extracts **45% more information** than power spectrum from the same 21cm data.

**Computational cost:**

| Architecture | Training time | Inference time |
|---|---|---|
| Power spectrum baseline | 1 hr | 0.01 ms |
| CNN | 10 hr | 0.1 ms |
| ViT | 50 hr | 1 ms |

ViT is more expensive but justified by information gain (1.45× more info at 5× training cost).

### Out-of-Domain Generalization

**Test**: Train on 21cmFAST, evaluate on zreion (different simulator).

| Architecture | In-domain accuracy | Out-of-domain accuracy | Degradation |
|---|---|---|---|
| Power spectrum | 1.0 | 0.85 | 15% |
| CNN | 1.25 | 0.90 | 28% |
| ViT | 1.45 | 1.35 | 7% |

**ViT is far more robust** to simulator changes. Relative degradation only 7% vs. 28% for CNN.

This mirrors [[Ore et al 2025 (SKATR)]]: ViTs are more generalizable than CNNs for 21cm fields.

### Well-Calibration of Posteriors

**Key validation**: Are the reported credible intervals actually credible?

For a well-calibrated posterior, if you report a 68% credible interval, the true value should be inside that interval 68% of the time (over many realizations).

**Test**: Generate 200 validation realizations, estimate posterior for each, check if 68% credible interval captures true parameter.

**Results:**

| Architecture | Calibration |
|---|---|
| Power spectrum | 71% (slightly overconfident) |
| CNN | 68% (well-calibrated) |
| ViT + CFM | 67% (well-calibrated) |

CFM provides well-calibrated posteriors without explicit calibration adjustments.

## Connection to This Thesis

### Relevance to P1 (EFT bias measurements)

**Peripheral**: Schosser et al. is about cosmological parameters, not EFT coefficients. However:

- Both P1 and this paper require measuring detailed properties of 21cm fields
- This paper demonstrates that 21cm is sensitive to fundamental physics (inflation) propagated through small-scale 21cm structure
- EFT coefficients (P1's target) are the language for describing that small-scale structure; understanding what physical information they encode is relevant

### Relevance to P2 (EFT-based parameter inference)

**Direct and highly relevant**:

1. **Architecture validation**: Schosser et al. demonstrates that ViT outperforms CNN for extracting cosmological information from 21cm. P2 might benefit from using ViT-based summaries (or EFT-based summaries, which are explicitly physical) rather than CNN.

2. **Joint inference complexity**: This paper shows that simultaneously inferring cosmological parameters ($n_s, r$) and astrophysical parameters ($\zeta, T_{\text{vir}}, R_{\text{mfp}}$) is challenging. P2's approach of focusing on EFT coefficients (which encode the combined effects) might naturally handle this coupling better than native parameter inference.

3. **Multi-tracer synergy**: Schosser et al. show that 21cm + CMB together are much more powerful than either alone. This motivates P2 to consider multi-tracer approaches (21cm + galaxies, or 21cm + CMB) for improved parameter constraints.

### Supports / contradicts

- **Validates architecture**: [[Ore et al 2025 (SKATR)]] (ViTs are good for 21cm; this confirms it for a different task)
- **Complements**: [[Pietschke et al 2025 (EoRFlow)]], [[Pietschke et al 2026 (cross-correlation)]] (same Heidelberg group, different targets — astrophysical history vs. cosmological params)
- **Context for**: P2's inference methodology

## Key Equations

**Starobinsky inflation spectral index**:
$$n_s = 1 - \frac{2}{N_e} \approx 0.965 \quad \text{for } N_e \approx 60$$

**Tensor-to-scalar ratio**:
$$r = \frac{12}{N_e^2} \approx 0.003$$

**Probability path** (CFM):
$$p_t = (1 - t) p_0 + t p_1$$

**Velocity field** (learned by network):
$$\mathbf{u}_t(\mathbf{x}; \mathbf{c}) = \nabla_{\mathbf{x}} \log \frac{p_1(\mathbf{x})}{p_0(\mathbf{x})}$$

**Flow evolution**:
$$\mathbf{x}(t) = \mathbf{x}(0) + \int_0^t \mathbf{u}_s(\mathbf{x}(s); \mathbf{c}) \, ds$$

## Methods

**Simulation setup:**
- **21cmFAST**: modified to accept cosmological parameters ($n_s, r$) as inputs and compute 21cm power spectra
- **CLASS**: CMB power spectra computed via perturbation theory for each cosmological parameter set
- **Lightcones**: 3D 21cm lightcones for $z = 6$–15 at $512^3$ resolution
- **Mock observations**: Added realistic SKA-Low noise, Planck noise for CMB

**Training:**
- Neural density estimator: CFM with learned velocity field
- Optimizer: Adam with learning rate $10^{-4}$
- Batch size: 64
- Epochs: 100

**Validation:**
- Posterior calibration: checked on held-out test set
- Out-of-domain test: zreion simulator

## Limitations and Caveats

**What this paper does NOT address:**

1. **Real observational data**: All validation on simulations (21cmFAST + CLASS). Real SKA observations will have systematic errors (calibration, foreground residuals) not modeled here.

2. **Simulator dependence of cosmological constraints**: Uses 21cmFAST exclusively. Do different simulators (SCRIPT, ARTIST, full RT) produce the same cosmological constraints, or is there simulator-dependent bias?

3. **Degeneracies with astrophysics**: The paper doesn't deeply explore how astrophysical parameter uncertainties affect cosmological constraints. If $\zeta$ or $T_{\text{vir}}$ are poorly constrained, could they bias $n_s$ estimates?

4. **Fine-tuning complexity**: Comparing three architectures (power spec, CNN, ViT) introduces many design choices. Which are critical? Is there a simpler architecture that achieves similar performance?

**How the thesis addresses gaps:**

- P1 measures EFT coefficients across simulators → validates that cosmological inference would be stable across codes
- P2 focused inference framework → shows how to jointly fit astrophysics and cosmology via EFT

## Figures and Key Visuals

**Key figure**: Posterior distributions for $n_s$ and $r$ comparing 21cm alone, CMB alone, and joint
- Shows dramatic tightening from joint analysis
- Demonstrates Starobinsky prediction ($n_s \approx 0.965$, $r \approx 0.003$) is well-constrained

**Key figure**: Information content comparison (CNN vs. ViT vs. power spectrum)
- Bar chart showing ViT's advantage
- Justifies the additional computational cost

**Key figure**: Out-of-domain degradation across architectures
- ViT shows superior robustness to simulator change (zreion)
- Motivates use of ViT or physically-informed summaries for robust inference

## Open Questions After Reading

> [!gap]
> **Simulator dependence of $n_s$ constraints**: Does 21cmFAST produce different constraints on $n_s$ compared to SCRIPT or full RT codes? This is critical for real-world applicability; if simulator choice biases $n_s$, then joint CMB+21cm constraints would be unreliable.

> [!gap]
> **Why ViT works for 21cm**: The paper shows ViT outperforms CNN but doesn't deeply explain why. Is it the global receptive field? The patch-based representation? Position embeddings? A deeper analysis would help guide architecture choices for P2.

> [!gap]
> **Degeneracy between cosmology and astrophysics**: How degenerate are $n_s$ and $\zeta$? If changing $\zeta$ by 10% produces a similar 21cm power spectrum change as changing $n_s$ by 0.01, then constraining both simultaneously is problematic. Multi-tracer data (galaxies, CMB) might be essential to break this.

> [!gap]
> **Computational efficiency**: ViT takes 50 hours to train vs. 1 hour for power spectrum baseline. For real SKA analysis (where retraining on new data is frequent), is the 1.45× information gain worth 50× longer training? Could a hybrid approach (power spectrum + learned mixing network) be more practical?

> [!gap]
> **Forecasts for future surveys**: Beyond Starobinsky, what other inflationary models can SKA + CMB distinguish? And can 21cm-galaxy cross-correlations break further cosmological degeneracies?
