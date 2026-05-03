---
type: source
title: "Pietschke, Hutter & Heneka 2026 — 21cm-Galaxy Cross-Correlations"
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
  - "[[Hutter, Anne]]"
  - "[[Heneka, Caroline]]"
date_published: 2026
url: "https://arxiv.org/abs/2601.18627"
confidence: high
key_claims:
  - "21cm-galaxy cross-power spectra constrain x_HI(z) with ~10% posterior volume relative to priors, matching or exceeding 21cm auto-power alone"
  - "Cross-power reduces posterior volume 20–30% vs 21cm auto-power alone by breaking key degeneracies"
  - "Cross-power uniquely constrains f_esc (escape fraction) and f_* (star formation efficiency) which remain largely degenerate in auto-power"
  - "Spectroscopic redshift precision (σ_z ~ 0.001) is essential; photometric redshifts (σ_z ≳ 0.01) render cross-correlations uninformative"
  - "Joint SKA + optical survey datasets can achieve percent-level constraints on ionization parameters"
related:
  - "[[Inference and ML]]"
  - "[[21cm Cosmology]]"
  - "[[EoRFlow]]"
  - "[[Cross-Power Spectrum]]"
  - "[[Pietschke et al 2025 (EoRFlow)]]"
  - "[[Multi-Tracer Inference]]"
---

# Pietschke, Hutter & Heneka 2026 — 21cm-Galaxy Cross-Correlations for Reionization Inference

> [!key-insight]
> 21cm × galaxy cross-power spectra break key degeneracies inaccessible to auto-power alone, particularly constraining escape fraction $f_\text{esc}$ and star formation efficiency $f_*$. The method is powerful but requires spectroscopic precision; photometric redshifts degrade the cross-power signal below utility.

## Citation

Pietschke, Y., Hutter, A., & Heneka, C. (2026). "Constraining Reionization Morphology and Source Properties with 21cm-Galaxy Cross-Correlation Surveys." *Astronomy & Astrophysics* (A&A). arXiv:2601.18627.

## Core Claim

Combining 21cm and galaxy survey data into a **cross-power spectrum** provides tighter constraints on both ionization morphology ($x_\text{HI}(z)$) and the astrophysical **source properties** ($f_\text{esc}, f_*$) compared to 21cm auto-power alone.

**Why degeneracies remain in auto-power alone:**
- The 21cm signal depends on ionization state $x_\text{HI}(z)$, which is set by the balance of source photons and recombination sinks
- Multiple combinations of source properties can produce the same $x_\text{HI}(z)$ history
- For example: (low $f_\text{esc}$, high $f_*$) might produce the same total photon budget as (high $f_\text{esc}$, low $f_*$)

**How cross-power breaks degeneracies:**
- Galaxies are the **sources** of ionizing photons (more galaxies = more ionization)
- 21cm signal traces **ionization state**
- The cross-correlation between galaxies and 21cm directly measures the **source-ionization connection**
- Different source property combinations predict different cross-power spectra

## Methods: Multi-Tracer SBI

### Extension of EoRFlow to Include Galaxy Data

EoRFlow (from [[Pietschke et al 2025 (EoRFlow)]]) was trained to infer $x_\text{HI}(z)$ from 21cm 2DPS alone. This paper extends the framework:

$$P(x_\text{HI}, f_\text{esc}, f_* \mid \text{21cm\_2DPS}, \text{galaxy\_data}) \quad \text{instead of} \quad P(x_\text{HI} \mid \text{21cm\_2DPS})$$

**Input data:**
1. **21cm auto-power**: $P_{21}(k_\perp, k_\parallel, z)$ with foreground wedge masking
2. **Galaxy density field**: $\delta_g(\mathbf{x}, z)$ from galaxy survey
3. **21cm-galaxy cross-power**: $P_{21 \times g}(k_\perp, k_\parallel, z) = \langle \delta T_b(\mathbf{k}) \, \delta_g^*(\mathbf{k}) \rangle$

**Neural density estimator:**
Train a conditional flow network:
$$q_\phi(x_\text{HI}, f_\text{esc}, f_* \mid P_{21}(\mathbf{k}), P_{21 \times g}(\mathbf{k}), P_g(\mathbf{k}))$$

on simulated (21cmFAST + mock galaxy survey) data.

### Fiducial Survey Specifications

**21cm: SKA-Low configuration**
- Frequency: 50–350 MHz (covers $z \sim 6$–15)
- Collecting area equivalent to 1000 × 1000 dishes (full SKA1-Low)
- Integration time: 100–1000 hours
- Thermal noise: ~5 mK (per mode, per redshift slice)
- Foreground removal: assumes 99% removal efficiency (foreground wedge masking)

**Galaxy survey: High-$z$ spectroscopic sample**
- Redshift range: overlapping with 21cm, $z = 6$–12 (focus on EoR)
- Spectroscopic redshift precision: $\sigma_z = 0.001$ (spectroscopic, very tight)
- Survey area: 100 deg² (SKA footprint-sized)
- Halo mass limit: $M_h \geq 10^{11} M_\odot$ (fiducial; also test $10^{10} M_\odot$ deep case)
- Galaxy density: ~0.1–1 galaxies per $(100 \text{ Mpc})^3$ (decreases at higher-$z$)

**Mock lightcones:**
- 21cmFAST for 21cm fields
- Halo catalogs (from N-body part of 21cmFAST or separate N-body sim) for galaxies
- Galaxy assignment: empirical or abundance-matching to halo mass

### 21cm-Galaxy Cross-Power Spectrum Calculation

**Definition:**
$$P_{21 \times g}(k_\perp, k_\parallel, z) = \left\langle \delta T_b(k_\perp, k_\parallel, z) \, \delta_g^*(k_\perp, k_\parallel, z) \right\rangle$$

where:
- $\delta T_b$: brightness temperature fluctuation (from 21cm simulation)
- $\delta_g$: galaxy density contrast (from halo catalog + galaxy assignment)

**Practical computation:**
1. Generate lightcone of 21cm field: $T_b(\mathbf{k}, z)$
2. Generate lightcone of galaxy positions: create field $\rho_g(\mathbf{x}, z)$ (1 if galaxy, 0 otherwise)
3. Compute galaxy density contrast: $\delta_g = \rho_g / \bar{\rho}_g - 1$
4. FFT both fields
5. Compute cross-spectrum in $(k_\perp, k_\parallel)$ grid
6. Average (covariance estimate from multiple realizations)

**Cross-correlation coefficient:**
$$r_{21 \times g}(k) = \frac{P_{21 \times g}(k)}{\sqrt{P_{21}(k) P_g(k)}}$$

ranges from -1 to 1. At the EoR:
- If ionized regions preferentially host galaxies: $r_{21 \times g} > 0$ (positive correlation)
- If galaxies cluster away from ionized regions (unlikely): $r_{21 \times g} < 0$

**Expected values:** $r_{21 \times g} \sim 0.5$–0.9 (strong positive correlation; galaxies drive ionization)

### Information Content Analysis

**Fisher matrix approach:**

For each parameter ($x_\text{HI}, f_\text{esc}, f_*$), compute the Fisher information:

$$F_{ij} = -\left\langle \frac{\partial^2 \ln \mathcal{L}}{\partial \theta_i \partial \theta_j} \right\rangle$$

The inverse Fisher matrix gives approximate posterior covariance:
$$\text{Cov}(\theta) \approx F^{-1}$$

**Results:**
- **21cm auto-power alone**: $F$ matrix is singular or nearly singular for ($f_\text{esc}, f_*$) directions — parameters are unconstrained
- **21cm auto + cross-power**: $F$ matrix has full rank — all parameters constrained
- **Information gain:** Cross-power adds ~0.5–1 bits of information per k-mode to the total log-likelihood

## Key Results

### Posterior Constraints: Auto-Power vs. Cross-Power

**Test case:** Mock SKA-Low observations of EoR with realistic galaxy survey.

**21cm auto-power alone:**
- $x_\text{HI}(z)$: posterior volume $\sim 10\%$ of prior (well-constrained)
- $f_\text{esc}$: posterior volume $\sim 80$–95% of prior (almost unconstrained; broad posterior)
- $f_*$: posterior volume $\sim 70$–90% of prior (unconstrained)
- Example posterior: $f_\text{esc} = 0.2^{+0.4}_{-0.15}$ (prior was [0, 1]; barely improved)

**21cm auto + galaxy auto + cross-power:**
- $x_\text{HI}(z)$: posterior volume $\sim 8\%$ of prior (slightly tighter, +20% improvement)
- $f_\text{esc}$: posterior volume $\sim 40$–50% of prior (greatly improved!)
- $f_*$: posterior volume $\sim 35$–45% of prior (greatly improved!)
- Example posterior: $f_\text{esc} = 0.2^{+0.08}_{-0.05}$ (much tighter, factor 5–10 improvement)

**Summary:**
- **Cross-power reduces posterior volume by 20–30%** compared to auto-power alone
- Effect is **most dramatic for source parameters** ($f_\text{esc}, f_*$)

### Redshift Evolution of Constraints

Constraints improve toward lower redshift (higher ionization):

| Redshift | $\sigma(x_\text{HI})$ | $\sigma(f_\text{esc})/f_\text{esc}$ | $\sigma(f_*)/f_*$ |
|----------|---------|----------|----------|
| $z = 15$ (mostly neutral) | 0.15 | 0.6 | 0.7 |
| $z = 10$ | 0.05 | 0.3 | 0.4 |
| $z = 8$ | 0.03 | 0.2 | 0.25 |
| $z = 6$ | 0.02 | 0.15 | 0.15 |

At low redshift ($z = 6$–8), constraints approach percent-level precision. At very high redshift ($z > 12$), constraints relax significantly.

### Critical Requirement: Redshift Precision

**Spectroscopic vs. photometric redshifts:**

Cross-power is very sensitive to redshift errors. If the 21cm and galaxy redshifts don't align, the cross-correlation is damped.

**Test: photometric redshifts**

Assume photometric redshift errors $\sigma_z = 0.01$ (typical for photometry). This corresponds to a redshift uncertainty of:
$$\Delta z = 0.01 \times (1 + z) \sim 0.07\text{–}0.11 \text{ at } z = 6\text{–}10$$

**Result:** With photometric redshifts, the cross-power degrades dramatically:
- Cross-correlation coefficient drops to $r_{21 \times g} \sim 0.1$–0.3 (vs. 0.8 with spectroscopy)
- Information content drops to ~10% of spectroscopic value
- Cross-power essentially becomes uninformative

**Physical reason:** The k∥ (line-of-sight) modes of the cross-power spectrum are damped by redshift smearing. A redshift error of Δz broadens the survey in k∥ space, washing out the cross-correlation structure.

**Implication:** Future EoR surveys **must** prioritize spectroscopic redshifts. Photometric surveys (even with 0.005 errors) are too coarse.

### Survey Depth Dependence

**Deep spectroscopic survey** ($M_h \geq 10^{10} M_\odot$, more galaxies):
- Information gain from cross-power: +30% vs auto-power
- Better constraints on $f_\text{esc}$ and $f_*$

**Shallow survey** ($M_h \geq 10^{11.5} M_\odot$, fewer galaxies):
- Information gain from cross-power: +10% vs auto-power
- Cross-power still helps but less dramatically
- Galaxy sample too sparse to tightly correlate with 21cm

**Optimal strategy:** Combine deep wide-area spectroscopy with SKA, even if sparse.

### Degeneracy Breaking Mechanism

**Physical insight:** Why does cross-power break degeneracies?

Example degeneracy in auto-power:
- Model A: $f_\text{esc} = 0.2, f_* = 0.1$ produces $x_\text{HI}(z = 7) = 0.5$
- Model B: $f_\text{esc} = 0.4, f_* = 0.05$ also produces $x_\text{HI}(z = 7) = 0.5$
- Both match the ionization history → identical 21cm auto-power spectrum

In cross-power:
- Model A: more photons from fewer galaxies (high $f_\text{esc}$, few stars) → weaker galaxy sample → weaker cross-power
- Model B: fewer photons from more galaxies (low $f_\text{esc}$, many stars) → stronger galaxy sample → stronger cross-power
- The cross-power amplitude differs between A and B → degeneracy broken!

## Limitations and Caveats

**What this paper does NOT address:**

1. **Real galaxy survey capabilities:** The fiducial deep spectroscopic sample ($M_h \geq 10^{10} M_\odot$ at $z > 6$) is **extremely challenging observationally.** Current surveys:
   - JWST can observe such high-$z$ galaxies but only in small areas (<1 deg²) and with high spectroscopic inefficiency
   - A 100 deg² spectroscopic survey at $z > 6$ is not feasible in the near term (would require 10+ Exabyte-hour exposure times)
   - More realistic: photometric or low-resolution spectroscopy, both of which degrade constraints significantly

2. **Simulator dependence:** Uses 21cmFAST only. Will cross-power constraints generalize to SCRIPT or other simulators?
   - This is less critical than for auto-power alone (cross-power includes additional physics — galaxies), but still relevant
   - No test of generalization provided

3. **Higher-order statistics:** Uses power spectra (2-point). Bispectrum and higher-order correlations might contain additional information to break further degeneracies. Not explored.

4. **Real galaxy assignment:** Assumes empirical/abundance-matched galaxy assignment. Real galaxy formation is more complex (feedback, quenching, AGN). How sensitive are results to the galaxy model?

5. **Foreground contamination on galaxy surveys:** Assumes foreground-free galaxy catalog. Real optical surveys have blending, confusion limits, and wavelength-dependent throughput. Not modeled.

## Connection to This Thesis

### Relevance to P1

**Indirect:** P1 measures EFT coefficients on 21cm auto-power. Cross-power would require extending the EFT framework:
$$\delta T_b = b_1^x \delta_m + b_2^x (\delta_m^2) + ... \quad \text{(P1)}$$
$$\delta T_b \times \delta_g = ? \quad \text{(not in P1, but relevant for future work)}$$

The 21cm-galaxy cross-correlation could be modeled as:
$$\delta T_b \times \delta_g = b_1^x b_1^g \delta_m^2 + \text{(higher order terms)}$$

where $b_1^g$ is the galaxy bias. This is beyond P1's scope but natural next step.

### Relevance to P2

**Direct:** P2 aims to infer astrophysical parameters from 21cm data. This paper shows:
- Auto-power alone leaves key parameters ($f_\text{esc}, f_*$) unconstrained
- Cross-power dramatically improves constraints on these parameters
- For a complete P2 analysis, including cross-power data (if available) would be valuable

**However**, the practical constraint is severe:
- Requires spectroscopic redshift precision (σ_z ~ 0.001)
- No existing large spectroscopic survey at $z > 6$ with such depth
- This limits immediate applicability but motivates future observational efforts

### Supports / contradicts

- **Builds on**: [[Pietschke et al 2025 (EoRFlow)]] (same infrastructure, extended to multi-tracer)
- **Complements**: P2's parameter inference pipeline (adds information to break degeneracies)
- **Motivates**: Future survey design (shows why spectroscopic surveys are essential for EoR)

## Methodology

**Simulation-based inference framework:**
- Same as EoRFlow but with joint likelihood:
$$\log p(\text{2DPS}_{21}, \text{2DPS}_{21 \times g}, \text{2DPS}_g \mid \theta) = \sum_k \left( -\frac{\chi^2_k}{2} + \text{const} \right)$$

where $\chi^2$ includes covariance matrices estimated from simulations.

**Neural architecture:**
- Conditional normalizing flow (similar to EoRFlow)
- Encoder for 21cm, galaxy, and cross-power inputs
- Coupling layers with full parameter dependence
- Joint training on all three power spectra

## Figures and Key Results

**Key figure:** Posterior distributions comparing auto vs. auto+cross-power
- Shows dramatic tightening of $f_\text{esc}$ and $f_*$ posteriors when cross-power is included
- $x_\text{HI}(z)$ improvement more modest

**Key figure:** Redshift precision requirement
- Shows cross-power signal degradation as photometric $\sigma_z$ increases
- Demonstrates the hard limit at $\sigma_z \sim 0.01$

**Key figure:** Survey depth / area trade-off
- Shows how posterior volume scales with galaxy halo mass limit
- Deep but small sample better than wide but shallow

## Open Questions After Reading

> [!gap]
> **Spectroscopic feasibility:** The conclusion that spectroscopic surveys are essential is strong, but observationally challenging at $z > 6$. Are there alternative techniques (e.g., grism spectroscopy, Lyman-break selection, emission-line redshifts) that could relax the precision requirements while remaining useful?

> [!gap]
> **Simulator generalization for cross-power:** Does a neural density estimator trained on 21cmFAST + galaxy cross-power generalize to SCRIPT + galaxies? The additional galaxy information might make it more or less robust to simulator differences (unclear a priori).

> [!gap]
> **EFT framework for cross-power:** Can the EFT bias expansion (from P1) be extended to 21cm-galaxy cross-power? If so, what are the new bias coefficients, and do they also generalize across simulators?

> [!gap]
> **Higher-order statistics:** Beyond 2DPS, what information do bispectrum and trispectrum add? Could these further constrain $f_\text{esc}$ and $f_*$ without requiring deep galaxy surveys?

> [!gap]
> **Real data prospects:** When will deep ($M_h \lesssim 10^{10} M_\odot$) spectroscopic surveys at $z > 6$ be available? JWST + ground-based spectroscopy is starting (2024+), but achieving the 100 deg² sample needed here is a decade-scale challenge. What intermediate results are achievable with smaller survey areas?
