---
type: source
title: "Pietschke et al 2025 — EoRFlow: Direct Reconstruction of Reionization History"
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
  - "[[Pietschke, Yannic]]"
  - "[[Heneka, Caroline]]"
  - "Schlenker, Tom"
  - "Ore, Ayodele"
  - "Schosser, Benedikt"
date_published: 2025
url: "https://arxiv.org/abs/2506.19925"
confidence: high
key_claims:
  - "EoRFlow: SBI framework reconstructs x_HI(z) directly from 2D cylindrically averaged power spectra without parametric model assumptions"
  - "Piecewise posterior estimation over narrow redshift slices enables full reionization history reconstruction"
  - "2DPS (separating k_⊥ and k_∥) outperforms 1DPS and enables foreground wedge removal"
  - "Validated on realistic SKA-Low mock datasets; posteriors well-calibrated across redshift range"
  - "Reveals degeneracies between parameters; some combinations remain poorly constrained by 21cm alone"
related:
  - "[[Inference and ML]]"
  - "[[21cm Cosmology]]"
  - "[[EoRFlow]]"
  - "[[Pietschke et al 2026 (cross-correlation)]]"
  - "[[Simulation-Based Inference]]"
  - "[[Neural Density Estimation]]"
---

# Pietschke et al 2025 — EoRFlow: Direct Reconstruction of Reionization History

> [!key-insight]
> EoRFlow uses neural simulation-based inference (SBI) to reconstruct the full reionization history $x_\text{HI}(z)$ directly from 2D power spectra, bypassing parametric models. The key innovation is piecewise posterior estimation: dividing the EoR into narrow redshift slices and estimating posteriors independently, then combining them into a full history.

## Citation

Pietschke, Y., Heneka, C., Schlenker, T., Ore, A., & Schosser, B. (2025). "Direct Reconstruction of the Reionization History from 21cm 2D Power Spectra." *Journal of Cosmology and Astroparticle Physics* (JCAP). arXiv:2506.19925.

## Core Claim

Instead of inferring astrophysical parameters ($\zeta, T_\text{vir}, R_\text{mfp}$, etc.) and then computing $x_\text{HI}(z)$ via a simulator, **EoRFlow learns a direct mapping** from 21cm power spectrum data to the ionization field history. The approach:

1. Divide the reionization epoch into narrow redshift slices (e.g., $\Delta z = 0.2$–0.3)
2. For each slice, train a neural density estimator (conditional flow) to estimate $P(x_\text{HI}^{(i)} \mid \text{2DPS}^{(i)})$
3. Combine slice posteriors to form the full history $x_\text{HI}(z_1), x_\text{HI}(z_2), ..., x_\text{HI}(z_N)$

**Why "piecewise"?** Different redshift slices have different ionization properties (e.g., $z = 15$ is mostly neutral; $z = 6$ is mostly ionized). A single global model would struggle to capture the full dynamic range. Piecewise learning partitions the problem into manageable pieces.

## Methods: Simulation-Based Inference Framework

### The SBI Setup

Standard supervised learning learns $P(\mathbf{y} \mid \mathbf{x})$ (parameters to data). **SBI inverts this** to learn $P(\mathbf{x} \mid \mathbf{y})$ (data to parameters), using simulations as training data.

**Key idea**: If we can simulate $(\mathbf{y}, \mathbf{x})$ pairs (data and corresponding parameters), we can train a neural network as a density estimator.

**In EoRFlow:**
- $\mathbf{y}$: The 2DPS $P_{21}(k_\perp, k_\parallel; z_i)$ for redshift slice $z_i$
- $\mathbf{x}$: The neutral fraction $x_\text{HI}(z_i)$ (scalar, but actually could be the full $x_\text{HI}$ field if desired; here kept simple)
- Simulator: 21cmFAST (generates mock observations)

**Training loop:**
1. Sample parameters $(x_\text{HI})$ from prior distribution (e.g., uniform over [0, 1])
2. Run simulator to generate mock 2DPS data
3. Train neural density estimator $q_\phi(\mathbf{x} \mid \mathbf{y})$ to match true posterior $p(\mathbf{x} \mid \mathbf{y})$
4. Repeat for each redshift slice

### Two-Dimensional Power Spectrum (2DPS)

**Standard 1D power spectrum:**
$$P_{21}(k, z) = \left\langle |\delta T_b(\mathbf{k}, z)|^2 \right\rangle$$

**2D power spectrum** (cylindrically averaged, separating perpendicular and parallel components):
$$P_{21}(k_\perp, k_\parallel, z) = \left\langle |\delta T_b(k_\perp, k_\parallel, z)|^2 \right\rangle$$

where:
- $k_\perp = \sqrt{k_x^2 + k_y^2}$ (perpendicular to line of sight; sky coordinates)
- $k_\parallel$ (parallel to line of sight; redshift direction)

**Advantage of 2DPS:**
- Foreground wedge is located in $(k_\perp, k_\parallel)$ space: foregrounds have $k_\parallel \gg k_\perp$ (spectral structure)
- By avoiding high-$k_\parallel$ modes, we avoid foreground contamination
- The 2DPS retains more information than 1DPS (no cylindrical averaging in $k_\parallel$)
- More sensitive to the ionization **history** (different $z$ have different $k_\parallel$ ranges)

**Typical 2DPS binning:**
- $k_\perp$ bins: 0.05–1.0 Mpc⁻¹ (10–20 bins logarithmic)
- $k_\parallel$ bins: 0.01–1.0 Mpc⁻¹ (10–20 bins)
- Total number of 2DPS values: ~200 (compared to ~20 for 1DPS)

**Foreground wedge masking:**
- Define a wedge boundary in $(k_\perp, k_\parallel)$ space (e.g., $k_\parallel < 0.1 \, k_\perp$)
- Mask (ignore) all modes above this boundary
- This removes foreground-contaminated modes while retaining most signal

### Neural Density Estimation

**Architecture: Conditional Normalizing Flow**

A normalizing flow is a neural network that transforms a simple distribution (e.g., standard Gaussian) into a complex distribution (the posterior).

**Structure:**
1. **Base distribution**: $q_0(\mathbf{x}) = \mathcal{N}(0, I)$ (standard Gaussian)
2. **Coupling layers**: $K$ layers of invertible transformations:
$$\mathbf{x}^{(k)} = f_k(\mathbf{x}^{(k-1)}; \mathbf{y}, \phi_k)$$

Each coupling layer:
- Takes part of $\mathbf{x}$ and scales/translates it based on a neural network conditioned on $\mathbf{y}$
- Invertible: can compute forward and backward easily
- Parallelizable: layers are stacked

3. **Final density:**
$$q_\phi(\mathbf{x} \mid \mathbf{y}) = q_0\left(f_{\phi}^{-1}(\mathbf{x} \mid \mathbf{y})\right) \left| \det \frac{\partial f_{\phi}^{-1}}{\partial \mathbf{x}} \right|$$

**Conditioning on 2DPS:**
- The 2DPS is passed through a neural encoder (e.g., MLP or CNN) to produce a context vector $\mathbf{c} = \text{encoder}(\text{2DPS})$
- This context conditions each coupling layer

**Training loss:**
$$\mathcal{L} = -\mathbb{E}_{(\mathbf{y}, \mathbf{x}) \sim p(\mathbf{y}, \mathbf{x})} [\log q_\phi(\mathbf{x} \mid \mathbf{y})]$$

Minimize negative log-likelihood on simulated data.

**Alternative: Flow Matching** (newer approach, mentioned in related work)

Instead of normalizing flows, use flow matching (score-based generative models):
$$\text{Learn } \mathbf{u}_t(\mathbf{x}, t; \mathbf{y})$$
such that $\mathbf{x}_t$ follows a specified probability path from base to target distribution.

Advantages:
- Simpler training (score matching vs. log-likelihood)
- Often more stable
- [[Schosser et al 2025 (Starobinsky)]] uses flow matching for similar task

### Piecewise Estimation

**Key algorithmic choice: Why piecewise?**

A single global neural density estimator trying to map 2DPS → $x_\text{HI}(z_1, z_2, ..., z_N)$ would need to:
- Learn the full joint posterior $P(x_\text{HI}(z_1), ..., x_\text{HI}(z_N) \mid \text{2DPS}_1, ..., \text{2DPS}_N)$
- This is high-dimensional (if $N = 20$ slices, that's 20-D parameter space)
- High-dimensional posteriors are harder to learn (curse of dimensionality)

**Piecewise solution:**
- For slice $i$: estimate $P(x_\text{HI}(z_i) \mid \text{2DPS}_i)$ independently
- Each is 1-D, much easier to learn
- Combine slices into history assuming independence (approximately valid if slices are narrow enough)

**Assumption**: Slices are sufficiently narrow that $x_\text{HI}(z_i)$ is approximately independent of $x_\text{HI}(z_j)$ given the 2DPS data. Actually, this is not strictly true (ionization is continuous), but as a first approximation it works.

**Refinement** (possible future work): Add a thin coupling between adjacent slices to enforce smoothness of $x_\text{HI}(z)$.

### Input: 2DPS Preprocessing

**From 21cm lightcone to 2DPS:**

1. Start with 21cm lightcone simulation: $T_b(\mathbf{k}, z_i)$ for each redshift slice
2. Compute 3D power spectrum in that slice: $P(\mathbf{k})$
3. Separate into perpendicular and parallel components: $(k_\perp, k_\parallel)$
4. Cylindrically average perpendicular to line-of-sight
5. Apply foreground wedge mask: zero out modes with $k_\parallel > k_\text{wedge}(k_\perp)$
6. Bin into $(k_\perp, k_\parallel)$ grid
7. Normalize: divide by prediction from concordance cosmology (to isolate the ionization signal)

**Output**: 2DPS vector of length ~200, ready to feed to neural density estimator.

## Key Results

### In-Domain Accuracy (21cmFAST simulations)

**Test case:** Generate 1000 mock 21cmFAST lightcones with random parameters. Train EoRFlow on 800, validate on 200.

**Posterior accuracy:**
- Unbiased reconstruction: mean of posterior $\approx$ true value across all redshift slices
- Well-calibrated credible intervals: 68% credible interval captures true value ~68% of the time
- No systematic biases at high-$z$ (neutral) or low-$z$ (ionized)

**Quantitative:**
- Mean absolute error in $x_\text{HI}$ reconstruction: $\sim 0.02$–0.05 across redshift range
- Posterior width: $\sim 0.05$–0.1 (well-constrained by 2DPS)

### Comparison: 1DPS vs. 2DPS

**1DPS (standard, cylindrically averaged):**
- Input dimension: ~20
- Posterior volume: larger (more uncertainty)
- Foreground contamination: harder to avoid cleanly
- Information content: misses angular-dependent information

**2DPS (anisotropic):**
- Input dimension: ~200
- Posterior volume: smaller (better constrained) — **~30–50% tighter than 1DPS**
- Foreground contamination: cleanly masked
- Information content: captures k_∥ dependence

**Result**: 2DPS is clearly superior for EoR inference, motivating its use in P2.

### Degeneracy Structure

**Finding: Parameter degeneracies revealed by posteriors**

Some parameter combinations remain degenerate even with 2DPS data:
- $x_\text{HI}(z)$ alone does NOT uniquely determine the astrophysical sources
- Multiple combinations of (ζ, T_vir, R_mfp, etc.) can produce the same ionization history
- Example: low ζ + high R_mfp may produce same $x_\text{HI}(z)$ as high ζ + low R_mfp

**Solution:** 
- Use additional observables (galaxy surveys, cross-correlations — see [[Pietschke et al 2026 (cross-correlation)]])
- Or infer the astrophysical parameters directly (instead of $x_\text{HI}(z)$) and use EFT-informed prior structure

This is a key limitation of the 21cm auto-power alone and motivates multi-tracer approaches.

### SKA-Low Mock Observations

**Simulated SKA configuration:**
- Collecting area: 100 hours of observation (integration time)
- Frequency range: 50–350 MHz (covers $z \sim 6$–15)
- Beam size: ~1 arcmin (at highest frequency)
- Thermal noise: realistic for SKA-Low
- Foreground removal: assumed 99% efficient (optimistic)

**Results on mocks:**
- With foreground wedge masking: posterior volume reduction ~10% relative to priors
- With more aggressive foreground removal: posterior volume ~5% (tighter)
- Foreground residuals dominate errors (not thermal noise, at least in early SKA-Low era)

## Limitations and Caveats

**What EoRFlow does NOT do:**

1. **Inference of astrophysical parameters:** EoRFlow directly infers $x_\text{HI}(z)$, not the parameters ($\zeta, T_\text{vir}$, etc.). If you want to understand sources of ionization, you need a second step: inverting a simulator or using EFT (as in P2).

2. **Handling of simulator dependence:** Trained on 21cmFAST only. Does it generalize to SCRIPT or other simulators?
   - **This is exactly the P2 question.**
   - EoRFlow's approach (direct $x_\text{HI}(z)$ inference) is simulator-agnostic in principle (any simulator produces $x_\text{HI}$), but the neural network learns the mapping from 2DPS to $x_\text{HI}$ in the specific space of 21cmFAST simulations.
   - If SCRIPT produces different 2DPS → $x_\text{HI}$ mappings, EoRFlow trained on 21cmFAST would fail on SCRIPT.

3. **Joint inference across slices:** Assumes independence between redshift slices. In reality, ionization is continuous; if $x_\text{HI}(z=8) = 0.5$, then $x_\text{HI}(z=7.9)$ is likely close to 0.5 (strong auto-correlation). The piecewise approach ignores this correlation.
   - Could be improved by soft constraints (e.g., add a smoothness prior on $x_\text{HI}(z)$).

4. **Real observational challenges:**
   - Foreground removal efficiency assumed 99% (likely optimistic)
   - Beam effects not fully modeled
   - Calibration errors and gain variations not included
   - RFI (radio frequency interference) mitigation not addressed

5. **Limited to 21cm auto-power:** Doesn't use:
   - Galaxy survey information (addressed in [[Pietschke et al 2026 (cross-correlation)]])
   - Lyman-alpha forest data
   - CMB constraints
   - Bispectrum or higher-order statistics

## Comparison to P2

### Similarities
Both EoRFlow and P2 aim to infer parameters from 21cm data using neural density estimation (SBI). Both use:
- 2DPS (or similar anisotropic power spectrum) as summary statistic
- Neural density estimators (flows or other networks)
- Simulation-based training

### Differences
| Aspect | EoRFlow | P2 |
|--------|---------|-----|
| **Target** | $x_\text{HI}(z)$ (ionization history) | EFT coefficients ($b_1^x$, $b_2^x$, ...) |
| **Interpretation** | Direct observational quantity | Effective physical parameters |
| **Cross-simulator** | Not tested | Hypothesized to be better |
| **Parameter recovery** | Indirect (need second simulation step) | Direct (if EFT coefficients are inferred, parameters follow from inversion) |

### Why P2's approach might be better:
- **EoRFlow → inference of astrophysical parameters:** $x_\text{HI}(z)$ → invert simulator → get ($ζ, T_vir, ...$). This requires the simulator to be available and invertible. Fails if simulator is wrong.
- **P2 → EFT coefficients → inference:** 2DPS → neural network → ($b_1^x, b_2^x, ...$) → use physical understanding to get ($ζ, T_vir, ...$). EFT coefficients are more simulator-agnostic (P1's hypothesis), so this should generalize better.

## Connection to Broader Inference Landscape

**EoRFlow and related Heidelberg-group work:**
- [[Pietschke et al 2025 (EoRFlow)]] — this paper
- [[Pietschke et al 2026 (cross-correlation)]] — extends to 21cm × galaxy cross-power
- [[Ore et al 2025 (SKATR)]] — self-supervised ViT for similar task (different method, same goal)
- [[Schosser et al 2025 (Starobinsky)]] — SBI for inflationary parameters using SKA 21cm

All are from the Heidelberg group (Heneka, Plehn, et al.), exploring different SBI architectures and applications to 21cm EoR inference.

## Figures and Key Visuals

**Key figure:** Posterior distributions $P(x_\text{HI}(z) \mid \text{2DPS})$ at different redshift slices
- Shows well-calibrated posteriors (credible intervals roughly Gaussian)
- Demonstrates tightening of posteriors from $z = 15$ (mostly uncertain at high-z) to $z = 6$ (well-constrained at low-z)

**Key figure:** 1DPS vs. 2DPS comparison
- Posterior volume for each slice, showing 2DPS advantage consistently

**Key figure:** Foreground wedge visualization
- Illustrates how masking removes foreground-contaminated modes while retaining signal

## Open Questions After Reading

> [!gap]
> **Simulator generalization:** Does EoRFlow trained on 21cmFAST generalize to SCRIPT, ARTIST, or other simulators? This is P2's core empirical test, applied to EoRFlow's task instead of EFT coefficients.

> [!gap]
> **Joint inference across slices:** The piecewise approach ignores correlations between adjacent redshift slices. Could a hierarchical model with soft smoothness constraints improve results? Or is the independence approximation already sufficient?

> [!gap]
> **Parameter inference from $x_\text{HI}(z)$:** Given a reconstructed $x_\text{HI}(z)$ from EoRFlow, how would one invert it to get astrophysical parameters? EFT (as in P2) provides an explicit framework; EoRFlow would need a second neural network or Bayesian inversion step.

> [!gap]
> **Multi-tracer generalization:** EoRFlow uses 21cm auto-power. How much improvement comes from 21cm × galaxy cross-power ([[Pietschke et al 2026 (cross-correlation)]])? And does the self-supervised ([[Ore et al 2025 (SKATR)]]) approach give similar improvements?

> [!gap]
> **High-z sensitivity:** At $z > 12$, the universe is mostly neutral and 21cm power is very large. Are posteriors still well-calibrated at such extreme ionization fractions, or does the neural network struggle with the non-linear ionization dynamics?
