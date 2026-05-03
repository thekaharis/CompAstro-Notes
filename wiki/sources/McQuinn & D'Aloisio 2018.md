---
type: source
title: "McQuinn & D'Aloisio 2018"
created: 2026-04-14
updated: 2026-04-16
tags:
  - source/paper
  - domain/eft
  - foundational
status: mature
source_type: paper
author:
  - "[[McQuinn, Matthew]]"
  - "[[D'Aloisio, Anson]]"
date_published: 2018
url: "https://arxiv.org/abs/1806.08372"
confidence: high
key_claims:
  - "The large-scale 21cm signal from reionization is well described by a perturbative bias expansion in 2–3 coefficients"
  - "Minimal Model P_err/P₂₁ < 10% at k ≲ 0.2–0.5 h/Mpc across three different RT simulations"
  - "EFT coefficients encode source bias, neutral fraction, characteristic bubble size, and patchiness"
related:
  - "[[Effective Field Theory]]"
  - "[[Qin et al 2022 (EFT Redshift Space)]]"
  - "[[Baradaran et al 2024 (Hybrid EFT)]]"
  - "[[Sailer et al 2022 (Optical Depth EFT)]]"
  - "[[Bias Expansion]]"
  - "[[Regime of Validity]]"
---

# McQuinn & D'Aloisio 2018

> [!key-insight]
> The 21cm signal from reionization may be perturbative: a bias expansion in $\delta_m$ and its derivatives describes simulated large-scale structure with $P_\text{err}/P_{21} < 10\%$ across multiple radiative transfer codes. This foundational paper establishes that the EFT language can describe reionization-era 21cm observations, opening the door to physical, model-independent parameter inference.

## Citation

McQuinn, M. & D'Aloisio, A. (2018). "The observable 21cm signal from reionization may be perturbative." *JCAP*. arXiv:1806.08372.

## Core Claim

Large-scale 21cm fluctuations from reionization act as a biased tracer of the matter field, captured by the **Minimal Model**:

$$
\delta_{21} = b_1\!\left(1 - \frac{R^2_\text{eff} k^2}{3}\right)\!\tilde{\delta} + b_2\tilde{\delta}^2
$$

where $\tilde{\delta} = \delta_m(1 + z)$ is the linear density field (in linear growth D(z) normalization, accounting for the $(1+z)$ factor inherent in peculiar velocity contributions), and $R_\text{eff}$ encodes the characteristic scale of ionized regions (roughly the "bubble size" correlation length). The model captures $\gtrsim 90\%$ of the signal power over much of the relevant $k$ range, demonstrating that reionization is **not** a fundamentally nonlinear phenomenon at accessible scales, but rather a perturbatively biased field like galaxies or Lyman-alpha forest.

The physical interpretation is non-trivial: the bias coefficients are not simple functions of density but encode the properties of ionized bubble boundaries, which act as the primary driver of large-scale 21cm fluctuations. The coefficient $b_1$ incorporates both the ionization fraction $\bar{x}_\text{HII}$ and the source bias $b_{S,1}$, while $R_\text{eff}$ and $b_2$ encode bubble size and shape statistics.

## Key Results

### Regime of Validity
- **Minimal Model accuracy:** $P_\text{err}/P_{21} < 10\%$ for $k \lesssim 0.2$–$0.5\,h\,\text{Mpc}^{-1}$, across three independent large-scale RT simulations
- Breakdown scale depends on redshift (lower $z$ = higher $k$ validity) and ionization fraction (more ionized = larger regime)
- At the lowest redshifts tested ($z \sim 6$), the regime extends to $k \sim 0.5\,h\,\text{Mpc}^{-1}$; at higher redshifts (more ionized), regime shrinks

### Bias Coefficients and Their Physical Meaning
- **$b_1$ interpretation:** $b_1 \approx \bar{x}_\text{HII} - \bar{x}_\text{HII} b_{S,1}$ (ionization fraction minus source bias weighted by ionization fraction); evolves with $\bar{x}_\text{HII}(z)$ over the EoR
- **$R_\text{eff}$ interpretation:** characteristic bubble radius, roughly $R_\text{eff} \sim 10$–$30$ Mpc/h depending on redshift and reionization scenario; encodes the typical distance scale over which ionized regions cluster
- **$b_2$ interpretation:** encodes non-Gaussian patchiness and bubble boundary sharpness; smaller in smooth reionization (low $T_\text{vir}$), larger in "clumpy" scenarios (high $T_\text{vir}$)
- Trajectory of $b_1, b_2, R_\text{eff}$ as functions of $\bar{x}_\text{HII}$ is nearly universal across the three tested RT codes

### Full 1-Loop Expansion
- Extending to the full operator basis (up to 6 independent bias and stochastic terms) improves fit at intermediate $k$ (0.3–0.7 h/Mpc)
- However, in the regime where the Minimal Model is accurate ($k \lesssim 0.2$ h/Mpc), most of the predictive power resides in just $R_\text{eff}$ and $b_2$; adding more operators provides negligible gain
- The "reduced" model thus balances efficiency (few parameters) with fidelity (accurate over the regime where observations will constrain parameters)

### Observational Validation Targets
- Cross-correlation coefficient $r_{21m}(k)$ between 21cm and matter fields provides a direct test of the bias picture: $r_{21m}$ should drop below 1 at the breakdown scale, and its slope is diagnostic of ionization morphology
- Simulations show $r_{21m}(k) \sim 0.95$–$0.99$ at low $k$, dropping to $\sim 0.8$–$0.9$ near the breakdown scale

## Methods

### Simulations and Codes
- Three different large-scale cosmological radiative transfer (RT) codes, each with typical box sizes 256 Mpc/h:
  - Full 3D RT solvers representing state-of-the-art at 2018
  - Each independently computed ionization fractions and 21cm brightness temperatures on N-body density fields
  - Outputs span redshift $z = 6$–$15$, covering much of the reionization epoch
  
### Analysis Pipeline
1. **Extract the 21cm field:** computed as $\delta_{21} = \delta T_b / \bar{T}_b$ where $\bar{T}_b$ is the (brightness temperature-weighted) mean and $\delta T_b$ is the deviation
2. **Fourier transform:** both density field $\delta_m(\mathbf{k})$ and 21cm field $\delta_{21}(\mathbf{k})$ computed via FFT to Fourier space
3. **Bias expansion regression:** treat the Minimal Model as a template and solve for bias coefficients via nonlinear regression in Fourier space:
   $$\delta_{21}(\mathbf{k}) = b_1 \left(1 - \frac{R^2_\text{eff} k^2}{3}\right) \tilde{\delta}(\mathbf{k}) + b_2 \tilde{\delta}^2_{\mathbf{k}} + \text{stochastic noise}$$
   Coefficients extracted by minimizing $\chi^2$ in the low-$k$ regime and validated on intermediate $k$
4. **Error quantification:** $P_\text{err}(\mathbf{k}) = P_{21}(\mathbf{k}) - P_\text{model}(\mathbf{k})$ computed in bins, relative error $P_\text{err}/P_{21}$ tracked across $k$ and redshift

### Approximations and Limitations
- **Linearity of density field:** the analysis assumes $\tilde{\delta}$ is the linear density field; at higher $k$ where density becomes nonlinear, the bias interpretation breaks down
- **No velocity (redshift-space) treatment:** the paper works in real space; velocity effects in redshift space are not included (addressed in [[Qin et al 2022 (EFT Redshift Space)]])
- **Gaussian stochasticity assumption:** noise is modeled as Gaussian; any non-Gaussian stochastic scatter (e.g., from sub-resolution structure) is not explicitly addressed
- **Fixed bubble description:** $R_\text{eff}$ and $b_2$ are allowed to evolve with $\bar{x}_\text{HII}$ but are assumed to follow a universal trajectory; individual simulation realizations are not tested

## Important Equations

### Minimal Model Core
$$\delta_{21}(z, \mathbf{k}) = b_1(z) \left[1 - \frac{R^2_\text{eff}(z) k^2}{3}\right] \tilde{\delta}(\mathbf{k}) + b_2(z) \tilde{\delta}^2_{\mathbf{k}} + \varepsilon_\text{stoch}(\mathbf{k})$$

**Variables:**
- $\delta_{21}$: 21cm brightness temperature contrast
- $b_1$: linear bias (ionization-weighted); evolves from $\sim 1$ at high $z$ to $\sim 0$ as reionization completes
- $R_\text{eff}$: characteristic bubble scale in Mpc/h; correlates with reionization model ($R_\text{eff} \sim c_\text{eff} / (1+z)$ scaling observed)
- $b_2$: quadratic bias (patchiness); related to the skewness of the ionization field
- $\varepsilon_\text{stoch}$: stochastic remainder uncorrelated with linear field

### Physical Interpretation of $b_1$
$$b_1 = \bar{x}_\text{HII} \times (1 - b_{S,1})$$
where $b_{S,1}$ is the bias of ionization sources (galaxies). This shows that the 21cm bias is *not* the source bias, but a weighted combination.

### Power Spectrum Prediction (minimal model)
$$P_{21}(k) = b_1^2 \left(1 - \frac{R^2_\text{eff} k^2}{3}\right)^2 P_\delta(k) + b_2^2 P_{\delta\delta}(k) + \cdots$$
where $P_\delta(k)$ is the linear matter power spectrum and $P_{\delta\delta}$ accounts for the bispectrum projection onto the second operator.

## Figures Worth Noting

- **Fig. 2:** Cross-correlation coefficient $r_{21m}(k)$ vs $k$ — key validation target for P1; shows breakdown scale varies with simulator and redshift
  - $r_{21m}(k) = P_{21\delta}(k) / \sqrt{P_{21}(k) P_\delta(k)}$ should be close to 1 in the EFT regime and drop near the breakdown scale
  - Differences in $r_{21m}(k)$ between codes are a direct window into simulator-specific aspects of ionization morphology
  
- **Fig. 3/4:** Bias coefficient trajectories as function of $\bar{x}_\text{HII}$ (redshift evolution)
  - Shows $b_1$, $b_2$, $R_\text{eff}$ evolution across the reionization epoch for each of the three codes
  - Near-universal trajectories (code-to-code agreement within $\sim 5$–$10\%$) suggest that the EFT language captures the physics independent of implementation
  - Deviations between codes are largest in the mid-ionization regime ($\bar{x}_\text{HII} \sim 0.3$–$0.7$), where ionization morphology varies most between codes
  
- **Fig. 6:** $P_\text{err}/P_{21}$ as function of $k$ and $\bar{x}_\text{HII}$ — regime of validity diagnostic
  - Contour showing where the minimal model error falls below 10% threshold
  - Illustrates how the valid $k$ range shrinks at higher redshift and higher ionization fractions

## Connection to Thesis

### Relevant to P1: Direct Foundation
This is the foundational paper for P1. The thesis extends the same analysis in two directions:
1. **Different field:** P1 targets $\delta_x$ (the ionization field $x_\text{HII}$ directly) rather than $\delta_{21}$ (which mixes ionization, density, and RSD)
2. **Hypothesis:** by isolating ionization, the bias coefficients will be even more stable across codes than McQuinn & D'Aloisio find, since gravity (which drives density) is shared across all simulators
3. **Deliverable:** P1 will reproduce Fig. 2 ($r_{21m}(k)$) but for the ionization field, establishing the cross-correlation of $x_\text{HII}$ with density as the key observable

### Relevant to P2: Coefficient Trajectories as Inference Targets
The bias coefficient trajectories from P1 (as functions of $\bar{x}_\text{HII}$ or redshift) become the **inference targets for P2**. Instead of inferring astrophysical parameters like $f_*, T_\text{vir}, R_\text{mfp}$, P2 directly estimates $b_1^x(z), b_2^x(z)$, etc., which are stable across simulators by construction.

### The Supervisor's Key Innovation
The supervisor's proposal pivots from McQuinn & D'Aloisio's $\delta_{21}$ to the ionization field $\delta_x = \delta x_\text{HII}$. This is crucial because:
- **Density is universal:** all simulators use the same gravity / dark matter N-body solver
- **Ionization is simulator-specific:** different source prescriptions, recombination models, and radiative transfer solvers produce different $x_\text{HII}(z, \mathbf{r})$ maps even when integrated $\bar{x}_\text{HII}(z)$ is matched
- Therefore, focusing on $\delta_x$ isolates the simulator-dependent freedom while removing the shared gravitational physics, making comparison across codes more direct

## Subsequent Work Building on This Paper

### Immediate Extensions
- **[[Qin et al 2022 (EFT Redshift Space)]]**: extends McQuinn & D'Aloisio to redshift space, showing that RSD introduces additional bias terms but the minimal model structure persists; validates on THESAN RT code; pushes regime of validity to $k \lesssim 0.8\,h\,\text{Mpc}^{-1}$ (improved over real space)
  
- **[[Sailer et al 2022 (Optical Depth EFT)]]**: applies the same perturbative bias expansion to optical depth $\tau$ rather than 21cm power; uses the EFT framework to forecast constraint improvements from future 21cm experiments; shows that $\tau$ constraints improve dramatically with including higher-order bias terms
  
- **[[Baradaran et al 2024 (Hybrid EFT)]]**: hybrid approach combining N-body-computed density (shared across codes) with EFT-calibrated ionization painting; achieves highest accuracy semi-analytic 21cm predictions to date; validates on both 21cmFAST and SCRIPT

### Broader Context
- **[[Ferrara & Pandolfi (IGM Reionization)]]**: semi-analytic approach to modeling reionization; independent of the EFT framework but provides complementary physical insight into how ionization morphology emerges from astrophysics
  
- **[[Mesinger 2016]]**: seminal 21cmFAST code and review; provides the semi-numerical reference frame that McQuinn & D'Aloisio's RT results are compared against (implicitly)

## Critical Reading: Key Caveats and Subsequent Development

### What the Paper Does Well
- **Clear separation of concerns:** distinguishes bias (universal, large-scale physics) from stochasticity (code-specific small-scale physics)
- **Cross-code validation:** testing on three independent RT codes in 2018 was genuinely novel and strengthens claims
- **Interpretable coefficients:** $b_1, b_2, R_\text{eff}$ have clear physical meanings, not black-box parameters

### Important Caveats to Keep in Mind

1. **Redshift-space effects:** The paper works in real space. Redshift-space distortions (RSD) from peculiar velocities introduce additional bias terms and affect the cross-correlation $r_{21m}(k)$. [[Qin et al 2022 (EFT Redshift Space)]] shows that RSD can substantially modify the inferred regime of validity. Any forward modeling for inference (like P2) must account for RSD.

2. **Source bias vs. ionization bias:** The paper conflates the bias of ionization sources (galaxies) with the bias of the ionization field. At high redshift where star formation is concentrated in high-density peaks, these can differ significantly. More careful tracking of the source-to-ionization-field mapping would strengthen the model.

3. **Simulator-specific morphologies:** While trajectories of $b_1, b_2, R_\text{eff}$ are "universal," the underlying bubble size and shape distributions *do* vary between the RT codes tested (as acknowledged in the paper). The bias expansion averages over these morphological differences; it does not explain them.

4. **Limited scope of validation:** The three RT codes tested in 2018 are all full 3D solvers. Semi-numerical codes like 21cmFAST or SCRIPT use different approximations (e.g., excursion set ionization, spherical geometry). McQuinn & D'Aloisio do not test against these; [[Sooknunan et al 2024 (ML Reproducibility)]] later shows these codes have distinct morphological signatures.

### What Subsequent Papers Have Shown

- **[[Qin et al 2022 (EFT Redshift Space)]]** shows that in redshift space, the Minimal Model breaks down at lower $k$ than in real space (due to RSD squashing large-scale ionization filaments), but the bias interpretation remains valid — you just need more terms
  
- **[[Berklas & Pober 2025]]** and **[[Sooknunan et al 2024 (ML Reproducibility)]]** demonstrate that the universality of bias coefficients breaks down more severely when comparing full RT codes with semi-numerical codes, suggesting the McQuinn & D'Aloisio results may be specific to the RT code family
  
- **[[Baradaran et al 2024 (Hybrid EFT)]]** shows that when you separately compute density (via N-body) and ionization (via EFT painting), you can achieve higher accuracy than the unified bias expansion — suggesting the unified approach misses some structure

## Research Questions Opened by This Paper

1. **Why is ionization a biased tracer?** The physical mechanism is bubble-boundary clustering, but a more rigorous symmetry-based derivation (à la standard galaxy bias theory) would be valuable
   
2. **Can you predict the bubble size $R_\text{eff}$ from first principles?** The paper finds $R_\text{eff}$ empirically; a model relating it to $T_\text{vir}, \zeta, R_\text{mfp}$ would enable direct parameter inference

3. **How do the bias coefficients depend on the details of reionization sources?** The paper holds source model fixed; extending to varying $T_\text{vir}, \zeta$ (etc.) would clarify how much freedom is encoded in each coefficient

4. **Do semi-numerical codes obey the same EFT?** This is directly addressed by P1, which compares 21cmFAST and SCRIPT

## Open Questions for This Thesis

> [!gap]
> **Cross-code universality:** P1 will test whether the EFT coefficients of the ionization field (not 21cm brightness temperature) are universal across 21cmFAST and SCRIPT, and whether any deviations correlate with known morphological differences between the codes. If $b_1^x, b_2^x$ are truly universal, this validates targeting them for inference in P2.

> [!gap]
> **Regime of validity for ionization:** Does the regime where $P_\text{err} / P_x < 10\%$ (for the ionization field) match the regime for 21cm? Or is ionization more or less "smooth" (i.e., more or less perturbative) than the 21cm signal? This will determine the $k$ range accessible for parameter inference in P2.

> [!gap]
> **Redshift-space treatment:** For realistic observations (which are in redshift space), P1 must include RSD. How much do the bias coefficients shift when moving from real to redshift space for the ionization field?
