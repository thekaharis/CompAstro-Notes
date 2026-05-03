---
type: source
title: "Sailer, Chen & White 2022 — Optical Depth from Perturbative 21cm"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/eft
  - domain/21cm
  - domain/inference
status: mature
source_type: paper
author:
  - "[[Sailer, Neha]]"
  - "[[Chen, Shi-Fan]]"
  - "[[White, Martin]]"
date_published: 2022
url: "https://arxiv.org/abs/2205.11504"
journal: "JCAP, 2022(10), 007"
confidence: high
key_claims:
  - "The optical depth to reionization τ_e can be constrained from large-scale 21cm clustering using the perturbative bias expansion"
  - "21cm auto- and cross-power spectra with CMB lensing give competitive τ constraints without relying on CMB polarization alone"
  - "The symmetries-based bias expansion provides a principled basis for forecasting 21cm observational power"
  - "Large-scale 21cm power is dominated by linear bias b_1^x, making robust forecasts possible even with EFT coefficient uncertainties"
  - "Cross-correlation with CMB lensing breaks degeneracies between τ and ionization field bias coefficients"
related:
  - "[[Effective Field Theory]]"
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Qin et al 2022 (EFT Redshift Space)]]"
  - "[[Bias Expansion]]"
  - "[[Power Spectrum as Summary Statistic]]"
  - "[[21cm Cosmology]]"
---

# Sailer, Chen & White 2022 — Optical Depth from Perturbative 21cm

> [!key-insight]
> The perturbative 21cm bias expansion enables rigorous forecasting of reionization observables: in particular, the optical depth to reionization $\tau_e$ can be extracted from the large-scale 21cm power spectrum and its cross-correlation with CMB lensing, using EFT bias coefficients as the bridge between theory and data.

## Citation

Sailer, N., Chen, S.-F. & White, M. (2022). "Optical depth to reionization from perturbative 21cm clustering." *Journal of Cosmology and Astroparticle Physics*, 10, 007. arXiv:2205.11504.

## Core Claim

The bias expansion for the 21cm brightness temperature field — built from the symmetries of the EFT — provides a rigorous framework for connecting large-scale 21cm power spectra to the optical depth to reionization $\tau_e$.

**Key physical insight:**
The optical depth is defined as:
$$\tau_e = \sigma_T \int_0^\infty n_e(z') \frac{dz'}{H(z')} = \sigma_T \int_0^\infty \bar{n}_H x_\text{HII}(z') \frac{dz'}{H(z')}$$

This integral picks out the **volume-weighted ionized fraction**, which correlates with the 21cm field through the EFT bias:
$$\delta T_b(\mathbf{k}) = b_1^x \delta_m(\mathbf{k}) + b_2^x \delta_m^2(\mathbf{k}) + ...$$

By measuring how the large-scale 21cm power spectrum varies with cosmological parameters (especially those that change $\tau_e$), one can extract $\tau_e$ from 21cm data alone.

**Why this matters:**
- **CMB polarization** (Planck): measures $\tau_e$ integrated over all redshift; cannot distinguish reionization histories (e.g., early brief reionization vs. late extended reionization)
- **21cm power spectrum**: sensitive to the **redshift evolution** of ionization; can distinguish different histories
- **Combined analysis**: 21cm + CMB provides both the integrated $\tau_e$ (from polarization) and the history (from 21cm), with strong consistency checks

## Methods: Perturbative EFT Framework

### Bias Expansion for the 21cm Field

Following [[McQuinn & D'Aloisio 2018]] and [[Qin et al 2022 (EFT Redshift Space)]], the 21cm brightness temperature fluctuation is expanded in powers of the density contrast:

$$\delta T_b(\mathbf{k}, z) = \mathcal{A}(z) \left[ b_1^x(z) \delta_m(\mathbf{k}) + \frac{b_2^x(z)}{2!} \delta_m^2(\mathbf{k}) + b_{\nabla^2}^x(z) \nabla^2 \delta_m(\mathbf{k}) + ... + \epsilon(\mathbf{k}, z) \right]$$

where:
- $\mathcal{A}(z) = (T_\text{spin} - T_\text{CMB})/T_\text{CMB}$ is an amplitude factor (at high-$z$, $\mathcal{A} \approx T_\text{spin} / T_\text{CMB} \gg 1$)
- $b_1^x(z)$: linear bias coefficient (redshift-dependent)
- $b_2^x(z)$: quadratic bias coefficient
- $b_{\nabla^2}^x(z)$: Laplacian bias (captures smoothing effects of finite bubble size)
- $\epsilon(\mathbf{k}, z)$: stochastic noise (uncorrelated with density perturbations)

**Minimal model** (keeping only linear term):
$$\delta T_b(\mathbf{k}, z) \approx \mathcal{A}(z) b_1^x(z) \delta_m(\mathbf{k})$$

Valid at **large scales** ($k \ll k_\text{NL} \sim R_\text{mfp}^{-1} \sim 0.1$ Mpc⁻¹).

### Dependence of Bias on τ

The linear bias coefficient $b_1^x(z)$ depends on the **ionized fraction** $x_\text{HII}(z)$:
- Ionized regions are **associated with overdensities** (halos, galaxies)
- Therefore, the ionization field has **positive bias** with respect to matter
- As the universe ionizes (moving from neutral to ionized), the bias evolves

The relationship is approximately:
$$b_1^x(z) \approx \frac{d\bar{x}_\text{HII}}{d\bar{x}_\text{HII}} = 1 + b_\text{halo}(z)$$

where $b_\text{halo}$ is the halo bias at the minimum mass threshold for star formation.

**Direct connection to $\tau_e$:**
Since $\tau_e = \int \bar{x}_\text{HII}(z') dz'$, a change in $\tau_e$ directly changes the ionization history $\bar{x}_\text{HII}(z)$, which shifts the bias $b_1^x(z)$, which is reflected in the 21cm power spectrum.

### Fisher Matrix Forecasting

Standard Fisher analysis for parameter constraints:

$$F_{\alpha\beta} = \sum_k \frac{\partial \mathcal{M}_k}{\partial \theta_\alpha} (\mathcal{C}_k)^{-1}_{ij} \frac{\partial \mathcal{M}_{kij}}{\partial \theta_\beta}$$

where:
- $\mathcal{M}_k$ are the predicted power spectra (auto and cross)
- $\mathcal{C}_k$ is the covariance matrix (includes cosmic variance and shot noise)
- $\theta = (\tau_e, b_1^x(z_1), ..., b_1^x(z_N), \text{other cosmology})$ are the parameters

**Procedure:**
1. Generate fiducial 21cm and CMB lensing power spectra for a reference cosmology
2. Take numerical derivatives to construct Fisher matrix
3. Invert to get parameter covariance: $\text{Cov} = F^{-1}$
4. Report 1-$\sigma$ forecast on $\tau_e$ and marginalize over bias coefficients

### Data Vectors Considered

**1. 21cm auto-power**:
$$P_{21}(k, z) = \left\langle |\delta T_b(\mathbf{k}, z)|^2 \right\rangle$$

Measured from 21cm observations (SKA mock). Large-scale: $k < 0.1$ Mpc⁻¹ (EFT-valid regime).

**2. CMB lensing (Planck):**
$$P_\kappa(\ell) = \left\langle |\kappa(\ell)|^2 \right\rangle$$

where $\kappa$ is the CMB lensing convergence (sensitive to integrated matter along line of sight).

**3. 21cm × CMB lensing cross-power:**
$$P_{21 \times \kappa}(k, \ell) = \text{cross-correlation between 21cm and CMB lensing}$$

This is the key new observational handle — the cross-power breaks degeneracies between $\tau_e$ and the bias coefficient $b_1^x(z)$.

## Key Results

### τ_e Constraint from 21cm Auto-Power

**Fiducial forecast** (SKA Phase 1 sensitivity):

Using 21cm large-scale power ($k < 0.05$ Mpc⁻¹, $z = 6$–12):

$$\sigma(\tau_e) / \tau_e \sim 5\text{–}10\% \quad \text{(21cm alone)}$$

This is comparable to current Planck CMB polarization constraints ($\sigma(\tau_e) = 0.007$ at $\tau_e \approx 0.056$, giving $\sigma/\tau \sim 12\%$).

**Key caveat:** Bias coefficients are marginalized over (treated as nuisance parameters). Their uncertainties partially degrade the $\tau_e$ constraint.

### Improvement from CMB Lensing Cross-Correlation

**Combined 21cm auto + cross with Planck κ:**

$$\sigma(\tau_e) / \tau_e \sim 2\text{–}3\% \quad \text{(21cm + CMB lensing)}$$

**Improvement factor:** ~3–4× tighter than 21cm alone.

**Why?** The cross-power directly measures the correlation between ionized regions and matter overdensities. This breaks the degeneracy between:
- Parameters that change $\tau_e$ (ionization history) → changes $b_1^x$
- Parameters that change bias directly (e.g., halo mass function) → also change $b_1^x$

The cross-power with an **independent tracer** (CMB lensing) resolves this ambiguity.

### Marginalizing Over Bias Coefficients

**Naive approach**: Assume bias is known (unphysical).

**Realistic approach**: Bias is unknown, must be marginalized over.

**Result:** Marginalizing over $b_1^x(z_i)$ for 5–10 redshift bins increases the uncertainty in $\tau_e$ by factor ~1.5–2 (compared to fixed bias). But constraints remain interesting (still ~5–10% precision).

**Physical insight:** At **large scales** ($k \ll k_\text{NL}$), the power spectrum is sensitive only to the linear bias $b_1^x$. Higher-order bias terms $b_2^x$, $b_{\nabla^2}^x$ affect smaller scales and do not significantly degrade $\tau_e$ constraints if we restrict to $k < 0.05$ Mpc⁻¹.

## Connection to This Thesis

### Relevance to P1 (EFT bias measurements)

**Direct and crucial:**

This paper is the **observational use case** for the EFT framework and the bias measurements that P1 extracts from simulations.

**Specific connections:**

1. **Coefficient extraction methodology**: P1's procedure for fitting $b_1^x(z), b_2^x(z), b_{\nabla^2}^x(z)$ to simulation power spectra is the simulation-side counterpart to Sailer et al.'s observational framework. P1 provides the $z$-dependent functional forms needed for Sailer et al.'s forecasts.

2. **Cross-simulator stability**: Sailer et al. assume $\tau_e$ constraints are robust if the bias coefficients are well-characterized. If P1 shows that EFT coefficients differ significantly across simulators (21cmFAST vs. SCRIPT), that would propagate into systematic uncertainties on $\tau_e$ inference. Conversely, if P1 shows they're stable, Sailer et al.'s $\tau_e$ forecasts inherit that robustness.

3. **Scale dependence**: Sailer et al. restrict analysis to large scales ($k < 0.05$ Mpc⁻¹) where the EFT is most accurate. P1's measurement of bias coefficients at what scales the EFT is valid directly validates the scales Sailer et al. recommend for data analysis.

### Relevance to P2 (EFT-based parameter inference)

**Indirect but important:**

P2 aims to infer astrophysical parameters ($\zeta, T_\text{vir}, R_\text{mfp}$) from 21cm observations. Sailer et al. show that the same 21cm data constrains cosmological parameters ($\tau_e$).

**Practical implication:** When analyzing real SKA data (or mock-SKA data), the analysis must simultaneously fit:
- Cosmological parameters (including $\tau_e$)
- Astrophysical parameters (including $\zeta, T_\text{vir}, R_\text{mfp}$)

The interplay between these can create degeneracies. P2's assumption that astrophysical parameters can be cleanly extracted may need revision in the presence of cosmological nuisances. However, Sailer et al.'s use of the cross-power breaks some degeneracies, suggesting that multi-tracer approaches (as P2 might employ) could help.

### Supports / contradicts

- **Builds on**: [[McQuinn & D'Aloisio 2018]] and [[Qin et al 2022 (EFT Redshift Space)]] (EFT framework)
- **Validated by**: [[Choudhury 2022 (Reionization Intro)]] and [[Ferrara & Pandolfi (IGM Reionization)]] (reionization physics)
- **Applied in**: Future SKA analysis pipelines (once EFT coefficients are calibrated via P1)

## Key Equations

**21cm bias expansion** (large-scale limit):
$$\delta T_b(\mathbf{k}, z) = \mathcal{A}(z) b_1^x(z) \delta_m(\mathbf{k}) + \text{noise}$$

where $\mathcal{A}(z) = (T_\text{spin} - T_\text{CMB})/T_\text{CMB}$.

**21cm power spectrum** (from bias expansion):
$$P_{21}(k, z) = |\mathcal{A}(z)|^2 |b_1^x(z)|^2 P_m(k, z)$$

where $P_m$ is the matter power spectrum.

**Optical depth** (integrated ionization):
$$\tau_e = \sigma_T \int_0^\infty \bar{n}_H x_\text{HII}(z') \frac{dz'}{H(z')}$$

**Fisher information** for parameter $\theta_\alpha$:
$$F_{\alpha\beta} = \sum_k \frac{\partial \ln P}{\partial \theta_\alpha} (P_\text{cov})^{-1} \frac{\partial \ln P}{\partial \theta_\beta}$$

## Methods

**Analysis approach:**
- Perturbative EFT framework with symmetry-based bias expansion
- Fisher matrix forecasts (linearized approximation; valid if posteriors are approximately Gaussian)
- Fiducial cosmology: Planck 2018 ΛCDM
- Mock 21cm and CMB lensing power spectra generated from simulations

**SKA configuration assumed:**
- 100 dishes (scaled from full design) for pencil-beam sensitivity estimates
- Frequency range: 50–350 MHz
- Foreground removal: perfect (optimistic; real SKA will have residuals)

## Limitations and Caveats

**What this paper does NOT address:**

1. **Marginalizing over reionization history shape**: The analysis assumes the reionization history is well-parametrized by $\tau_e$ alone. In reality, the shape of $\bar{x}_\text{HII}(z)$ (early sharp vs. late extended) affects the bias evolution and could introduce additional parameters.

2. **Nonlinear regime**: Analysis restricted to $k < 0.05$ Mpc⁻¹ (deeply linear regime). The small-scale power (which can be measured with high signal-to-noise) is discarded due to EFT uncertainty.

3. **Real foreground residuals**: Assumes perfect foreground removal. Real SKA observations will have foreground leakage, which correlates with the 21cm signal at large scales and biases parameter estimates.

4. **Assuming known bias shape**: Bias coefficients are treated as free parameters per redshift bin, but no assumptions about their scale-dependence are made. Physically, biases should vary smoothly with redshift; imposing that could tighten constraints.

5. **No cross-simulator validation**: Uses simulations (presumably 21cmFAST) as fiducial. Does not address whether systematic differences in how different simulators compute $b_1^x$ would affect $\tau_e$ forecasts.

**How the thesis addresses some gaps:**

- P1 measures bias coefficients across codes → validates that Sailer et al.'s assumptions hold (or quantifies how much they break)
- P1's scale-dependent bias analysis → extends Sailer et al. beyond the minimal large-scale-only model

## Figures and Key Results

**Key figure**: $\sigma(\tau_e)$ vs. $k_\max$ (the maximum wavenumber included in the analysis)
- Shows that large-scale power ($k < 0.05$ Mpc⁻¹) dominates the $\tau_e$ constraint
- Including smaller scales (up to $k_\text{NL} \sim 0.1$ Mpc⁻¹) improves constraints by ~50%, but with increasing EFT uncertainty

**Key figure**: Posterior correlations between $\tau_e$ and bias coefficients
- Shows that bias coefficients are degenerate with $\tau_e$ when using auto-power alone
- Degeneracy is broken by the cross-power with CMB lensing

## Open Questions After Reading

> [!gap]
> **Mapping from bias to $\tau_e$**: The connection between $b_1^x(z)$ and $\bar{x}_\text{HII}(z)$ is assumed but not fully detailed. Can this relationship be inverted? That is, given a measured $b_1^x(z)$, can one directly infer $\bar{x}_\text{HII}(z)$ and hence $\tau_e$, or does one always need a forward simulator?

> [!gap]
> **Brightness temperature vs. ionization field bias**: Sailer et al. fit the bias of the 21cm brightness temperature $\delta T_b$, but P1 targets the ionization field $x_\text{HII}$. Is the mapping $b_1^{T_b} \leftrightarrow b_1^x$ simple (constant factor) or do higher-order terms couple them? This affects how P1's measurements translate to Sailer et al.'s predictions.

> [!gap]
> **Redshift-space distortions**: Sailer et al. do not discuss redshift-space distortions (RSD), which enter the 21cm power spectrum at intermediate scales ($k \sim 0.01$–$0.1$ Mpc⁻¹). How do RSD complicate the bias expansion, and do they help or hurt $\tau_e$ constraints?

> [!gap]
> **Future: extending to non-linear scales**: If the EFT can be extended to mildly nonlinear scales (k ~ 0.1–0.3 Mpc⁻¹) with better modeling of $b_2^x$ and $b_{\nabla^2}^x$, how much would $\tau_e$ constraints improve? This would motivate P1 to provide precise bias measurements beyond the linear regime.
