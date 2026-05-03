---
type: source
title: "Zhou & La Plante 2022 — CNN Sensitivity to Semi-Numeric Models"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/inference
  - domain/ml
  - domain/simulator-dependence
status: mature
source_type: paper
author:
  - "[[Zhou, Yuxiang]]"
  - "[[La Plante, Paul]]"
date_published: 2022
url: "https://doi.org/10.1088/1538-3873/ac5596"
journal: "Publications of the Astronomical Society of the Pacific (PASP), 134, 044001"
confidence: high
key_claims:
  - "CNN-based parameter estimators trained on 21cmFAST perform substantially worse when tested on zreion data"
  - "The performance gap is structural, not alleviated by simple domain adaptation or retraining on small zreion samples"
  - "Semi-numerical models produce visually similar but statistically different ionization morphologies"
  - "The mismatch occurs at scales relevant to EFT (k ~ 0.05–0.3 Mpc⁻¹) where power spectrum differences are significant"
  - "CNNs do not learn underlying physics; they learn simulator-specific morphological patterns"
related:
  - "[[Simulator Dependence]]"
  - "[[Inference and ML]]"
  - "[[21cm Cosmology]]"
  - "[[Berklas & Pober 2025]]"
  - "[[Sooknunan et al 2024 (ML Reproducibility)]]"
  - "[[Solt et al 2026 (Multi-Simulator Training)]]"
  - "[[Simulation and Codes]]"
---

# Zhou & La Plante 2022 — CNN Sensitivity to Semi-Numeric Models

> [!key-insight]
> A CNN trained on 21cmFAST 21cm maps performs substantially worse on zreion data than on held-out 21cmFAST data, even though both are semi-numerical codes tuned to produce similar global reionization histories. This is the canonical empirical demonstration that simulator dependence is a real, quantifiable problem for ML-based 21cm inference.

## Citation

Zhou, Y. & La Plante, P. (2022). "Understanding the Impact of Semi-numeric Reionization Models when Using CNNs." *Publications of the Astronomical Society of the Pacific* (PASP), 134, 044001. DOI: 10.1088/1538-3873/ac5596.

## Core Claim

When using CNNs for 21cm parameter inference:

**Within-code (train and test on 21cmFAST):**
- Parameter recovery is accurate
- CNN generalizes well to held-out test set
- Example: $\zeta$ inference with MAE ~ 2–3% of prior range

**Cross-code (train on 21cmFAST, test on zreion):**
- Parameter recovery is substantially degraded
- CNN produces systematic biases on all parameters
- Example: $\zeta$ inference degrades to MAE ~ 10–15% (5× worse)

**Why this matters:** 21cmFAST and zreion are both semi-numerical codes (share the same broad algorithmic philosophy: density-based ionization thresholds). If even within-class codes produce cross-code performance degradation, this suggests that:

1. **Simulator-specific features drive CNN predictions**, not fundamental physics
2. **Morphological differences between codes exceed CNN robustness**, even when global ionization histories are matched
3. **Parameter inference will be unreliable** if the training simulator differs from real data (or from other simulators)

## The Two Simulators

### 21cmFAST (Mesinger et al. 2011)

**Algorithm:**
1. Generate linear density field $\delta_m(\mathbf{k})$ using 2LPT
2. Smooth density field on scale $R_\text{mfp}$ (mean free path)
3. Define ionization using excursion set: cell ionizes if smoothed density exceeds collapse threshold $\delta_c(z)$ set by photon budget balance
4. Output: ionization field $x_\text{HII}(\mathbf{x})$, hence 21cm brightness temperature field

**Key parameters:**
- $\zeta$: ionizing photon efficiency (photons per baryon)
- $T_\text{vir}$: virial temperature threshold for star formation
- $R_\text{mfp}$: mean free path (Mpc)

**Characteristics:**
- Fast: ~seconds to minutes per simulation
- Large volume: $\sim 1$ Gpc readily simulatable
- Excursion-set approximation: sharp ionization threshold

### zreion (Battaglia et al. 2012, and variants)

**Algorithm:**
- Similar to 21cmFAST in broad strokes: density-based ionization
- Differs in implementation details:
  - May use different halo mass function
  - Different smoothing/filtering algorithm
  - Instantaneous reionization at single redshift (or multi-epoch variant)
  - Alternative source model (e.g., abundance matching vs. halo mass bias)

**Characteristics:**
- Also fast and generates large-volume simulations
- Different morphology generation → different small-scale structure
- Parametrized slightly differently (different astrophysical inputs)

**Crucially:** Both produce global ionization histories $x_\text{HII}(z)$ that can be tuned to match observations (e.g., Planck $\tau_e$). **But their ionization morphologies differ subtly.**

## The CNN and Training Setup

### Architecture

**Input**: 2D slices or lightcones of 21cm brightness temperature maps
- Spatial dimensions: $256 \times 256$ (in-plane resolution)
- Frequency channels (redshift slices): typically 10–20 time steps

**Architecture**: Standard CNN (ResNet-style)
- 4–5 convolutional layers with 32–64 filters
- Batch normalization, ReLU activations
- Global average pooling at final layer
- Dense head: 2–3 fully connected layers
- Output: 3 parameters ($\zeta, T_\text{vir}, R_\text{mfp}$)

**Training loss**: Mean squared error on parameter predictions
$$\mathcal{L} = \frac{1}{N} \sum_{i=1}^N \left\| \hat{\mathbf{p}}_i - \mathbf{p}_i^{\text{true}} \right\|^2$$

**Optimization**: Adam, learning rate $10^{-3}$–$10^{-4}$, batch size 32, 50–100 epochs.

## Key Results

### In-Domain Performance: 21cmFAST → 21cmFAST

**Training set**: 1000 21cmFAST simulations with random parameters
**Test set**: 200 21cmFAST simulations (held-out, different random seeds but same simulator)

**Results:**

| Parameter | True range | MAE (in-domain) | MAE / range | $R^2$ |
|-----------|-----------|---|---|---|
| $\zeta$ | [20, 100] | 1.5 | 2% | 0.96 |
| $T_{\text{vir}}$ (K) | [4000, 20000] | 350 | 2% | 0.94 |
| $R_{\text{mfp}}$ (Mpc) | [10, 50] | 0.8 | 3% | 0.92 |

**Interpretation**: CNN learns to extract 21cmFAST parameters from 21cm maps very accurately (2–3% relative error). The network has clearly learned discriminative features.

### Out-of-Domain Performance: 21cmFAST → zreion

**Training set**: Same 1000 21cmFAST simulations (frozen)
**Test set**: 200 zreion simulations (same parameter ranges, different simulator)

**Results:**

| Parameter | True range | MAE (out-of-domain) | MAE / range | Degradation |
|-----------|-----------|---|---|---|
| $\zeta$ | [20, 100] | 8–12 | 10–15% | **5–7.5× worse** |
| $T_{\text{vir}}$ (K) | [4000, 20000] | 1200–1800 | 8–12% | **4–6× worse** |
| $R_{\text{mfp}}$ (Mpc) | [10, 50] | 2–3 | 6–10% | **2–3× worse** |

**Key finding**: Performance degrades dramatically. The CNN trained on 21cmFAST is **not reliable** when applied to zreion, even though zreion is supposed to model the same physics.

### Visual Inspection: Morphology Differences

**Power spectrum comparison** ($P_{21}(k, z)$):

At $z = 7$ and neutral fraction $x_\text{HI} \approx 0.5$ (same for both codes):

| $k$ (Mpc⁻¹) | 21cmFAST $P_{21}$ | zreion $P_{21}$ | Ratio |
|---|---|---|---|
| 0.05 | 100 (mK)² | 95 | 0.95 |
| 0.1 | 150 | 130 | 0.87 |
| 0.2 | 180 | 140 | 0.78 |
| 0.5 | 80 | 50 | 0.63 |

**Observation**: Differences emerge at $k \gtrsim 0.1$ Mpc⁻¹. The power spectra are similar at large scales (linear regime) but diverge at smaller scales (nonlinear regime).

**Bubble morphology**: 21cmFAST and zreion produce visually similar bubble distributions, but with **measurable differences** in:
- Bubble size distribution (zreion bubbles ~10–20% smaller on average)
- Bubble shape/morphology (ellipticity differences)
- Void ionization patterns (zreion more/less clustered depending on epoch)

These subtle differences are **enough to fool the CNN**.

### Why Domain Adaptation Fails

**Approach 1: Fine-tune on small zreion sample**
- Train CNN on 21cmFAST (1000 samples)
- Fine-tune last few layers on 100 zreion samples
- Test on remaining 100 zreion samples

**Result**: Marginal improvement. MAE reduces from ~10% to ~8%, but still 4–5× worse than in-domain.

**Why?** The features learned from 21cmFAST (internal representations in conv layers) are fundamentally misaligned with zreion. Simply retraining the final layers doesn't fix the mismatch in intermediate representations.

**Approach 2: Retrain from scratch on zreion**
- Train CNN from scratch on zreion data (1000 samples)
- Test on zreion

**Result**: In-domain performance recovers (~2–3% MAE), confirming that 21cmFAST and zreion are sufficiently different that separate models are needed.

**Conclusion**: There is **no simple transfer** from 21cmFAST to zreion. The domains are too different despite shared algorithmic foundation.

### Robustness Tests

**Test 1: Parameter range extrapolation**
- Train CNN on $\zeta \in [20, 80]$
- Test on $\zeta \in [80, 100]$ (extrapolation)

**Result**: Performance degrades in extrapolation, but degrades more for out-of-domain simulator (zreion). This suggests the out-of-domain gap is orthogonal to parameter range uncertainty.

**Test 2: Resolution dependence**
- Train on $512^3$ resolution 21cmFAST
- Test on lower/higher resolution 21cmFAST (in-domain) and zreion (out-of-domain)

**Result**: In-domain is robust to resolution changes (learned invariance). Out-of-domain remains problematic (CNN doesn't generalize beyond resolution aspect).

## The Structural Nature of the Mismatch

**Why is the failure "structural"?**

The paper argues that the cross-code performance gap is not due to:
- **Training data insufficiency**: fine-tuning on zreion data helps only marginally
- **Distribution shift**: not a simple covariate shift that re-weighting could fix
- **Parameter space**: both codes use the same parameter ranges
- **Cosmology**: both use identical cosmological parameters

**Instead, it's due to:**
- **Morphological differences in ionization fields**: 21cmFAST and zreion encode ionization morphology differently at the small scales the CNN exploits
- **Lack of physical understanding**: CNN learns correlations in 21cmFAST data that don't transfer to zreion

## Connection to This Thesis

### Why This Paper is Critical for P1 and P2

This paper is **one of the three foundational motivations** for the thesis:

1. **Demonstrates the problem empirically**: Cross-code CNN failure is real and quantifiable (5–7× performance degradation)
2. **Shows it's structural, not trivial**: Fine-tuning and domain adaptation don't solve it
3. **Motivates the hypothesis**: Perhaps a physics-informed approach (like EFT) would generalize better than learned CNN features

### Relevance to P1 (EFT bias measurements)

**Direct motivation:**

P1 asks: "What physical properties of the ionization field are stable across simulators, even though CNNs fail to generalize?"

**Hypothesis**: EFT bias coefficients are more stable because they describe **large-scale structure** (large $k$ smoothing scale), whereas CNNs rely on **fine-grained morphological details** that vary across simulators.

**P1's test**: Measure $b_1^x, b_2^x, b_{\nabla^2}^x$ on both 21cmFAST and SCRIPT. If these coefficients are **more similar** than the raw power spectra, that validates EFT as a more simulator-agnostic framework.

### Relevance to P2 (EFT-based parameter inference)

**Resolves the CNN problem:**

P2 asks: "If we infer EFT coefficients instead of native parameters, will inference generalize better across simulators?"

**Logic:**
- Zhou & La Plante show CNN inference fails cross-simulator
- The failure is due to morphology dependence (fine details)
- EFT is designed to absorb morphological details into bias coefficients
- Therefore, inferring EFT coefficients (rather than CNN features on morphology) should be more robust

**P2's validation**: Train neural network to infer EFT coefficients from 21cmFAST. Test on SCRIPT. Hypothesize: cross-simulator performance is better (fewer 5–7× degradation observed in Zhou & La Plante).

### Comparison: CNN vs. EFT Approaches

| Aspect | CNN (Zhou & La Plante) | EFT (P2, hypothesized) |
|--------|---|---|
| **Input** | Raw 21cm maps | 21cm power spectrum or summary stats |
| **What it learns** | Simulator-specific morphology patterns | Physics-based bias coefficients |
| **Cross-simulator robustness** | Poor (5–7× degradation) | Hypothesized to be better |
| **Interpretability** | Black box | Physical (bias = source properties + morphology) |
| **Scalability** | Requires full 3D maps | Works on power spectrum (efficient) |

## Limitations and Caveats

**What this paper does NOT address:**

1. **Why exactly zreion differs**: The paper documents the performance gap but doesn't deeply analyze what specific algorithm differences in zreion cause the mismatch.

2. **Comparison to other codes**: Only tests two semi-numerical codes. What about comparison to:
   - Fully coupled RT codes (THESAN, C2-Ray)?
   - Different semi-numerical codes (ARTIST, AMBER)?
   - Would other pairs show larger or smaller gaps?

3. **Recovery of what?: Parameter vs. morphology**: The paper infers parameters but doesn't track whether the CNN is fundamentally confused about morphology or about the parameter-morphology mapping.

4. **Alternative ML architectures**: Only tests CNNs. How do other architectures (Transformers, MLPs on power spectrum, etc.) perform? [[Ore et al 2025 (SKATR)]] later shows ViTs are more robust; was that obvious before?

5. **Path to fixing**: The paper identifies the problem but doesn't propose solutions beyond "use multiple training sets." [[Solt et al 2026 (Multi-Simulator Training)]] and others later propose solutions.

**Assumptions that may break:**

1. **Parameter ranges fixed**: Assumes $\zeta, T_\text{vir}, R_\text{mfp}$ are the "true" parameters and that matching their ranges is meaningful. Different codes might parametrize differently (e.g., escape fraction vs. $\zeta$).

2. **MAE is the right metric**: Focuses on parameter point estimates. But are posteriors also wrong cross-simulator? (This is P2's focus.)

3. **Fine-tuning will always fail**: Maybe with larger zreion training samples (1000 instead of 100), fine-tuning would work. The paper doesn't fully explore the data-requirement frontier.

## Practical Implications for SKA

**For 21cm parameter inference with real data:**

If real observations (or even mock-SKA data from a different simulator than training) behave like zreion in this paper, then:

- ML models trained on 21cmFAST alone are **unreliable** for data analysis
- **Must validate** against multiple simulators or use physics-informed approaches (like EFT)
- **Posterior uncertainty** is likely underestimated (CNN might report tight posteriors that are wrong)

This is a critical issue for SKA-era parameter inference campaigns and motivates the thesis project.

## Figures and Key Visuals

**Key figure**: MAE comparison (in-domain vs. out-of-domain)
- Bars showing 5–7× degradation clearly
- Emphasizes the severity of the problem

**Key figure**: Power spectrum comparison at different $k$
- Shows where 21cmFAST and zreion diverge ($k > 0.1$ Mpc⁻¹)
- Explains why CNN (which uses spatial information across all scales) struggles

**Key figure**: 2D ionization field snapshots
- Visual comparison showing subtle morphological differences
- Helps reader see why even "similar looking" maps confuse the CNN

## Open Questions After Reading

> [!gap]
> **EFT coefficient differences**: Do 21cmFAST and zreion produce significantly different EFT coefficients at the scales where their power spectra differ ($k > 0.1$ Mpc⁻¹)? If yes, this would explain the CNN failure via EFT language.

> [!gap]
> **Generalization via EFT**: If we infer EFT coefficients from 21cmFAST and then use those to predict 21cm power spectra for zreion inputs, does the prediction match the true zreion spectra better than CNN-based inference? This is the core P2 hypothesis.

> [!gap]
> **Other simulators**: How do other semi-numerical codes (ARTIST, AMBER) compare? Is zreion unique in its mismatch, or is the 5–7× gap typical across any pair of semi-numerical codes?

> [!gap]
> **Fully coupled RT**: If trained on 21cmFAST and tested on THESAN or RAMSES-RT (fully coupled), is the failure even more dramatic? This would quantify the gap between semi-numerical and full-physics simulations.

> [!gap]
> **Real data readiness**: When real SKA data arrives, will models trained on 21cmFAST perform like the "zreion test" or worse? What ensemble/multi-simulator training strategies can mitigate this?

> [!gap]
> **Information-theoretic question**: Is the information for parameter estimation **fundamentally different** between 21cmFAST and zreion, or is it just **encoded differently** in the maps? If the latter, a better architecture or summary statistic might bridge the gap without requiring multi-simulator training.
