---
type: concept
title: "Cross-Power Spectrum"
created: 2026-04-14
updated: 2026-04-16
tags:
  - concept/statistics
  - domain/21cm
  - domain/galaxy-surveys
status: expanded
complexity: intermediate
domain: "[[21cm Cosmology]]"
aliases:
  - "21cm-galaxy cross-power"
  - "cross-correlation power spectrum"
  - "21cm-UV cross-power"
related:
  - "[[Power Spectrum as Summary Statistic]]"
  - "[[EoRFlow]]"
  - "[[2D Power Spectrum]]"
  - "[[Foreground Wedge]]"
  - "[[Ionizing Photon Sources]]"
sources:
  - "[[Pietschke et al 2026 (cross-correlation)]]"
  - "[[Park et al 2014 (21cm-Ly-alpha correlation)]]"
  - "[[Beardsley et al 2016 (Cross-correlation Methods)]]"
---

# Cross-Power Spectrum

## Definition and Mathematical Formalism

The cross-power spectrum measures the **correlation between 21cm intensity fluctuations and an external tracer** (typically galaxy number density from spectroscopic surveys):

$$
P_\times(k) = \langle \tilde{\delta}_{21}(\mathbf{k})\, \tilde{\delta}_{g}^*(\mathbf{k}) \rangle
$$

where:
- $\tilde{\delta}_{21}(\mathbf{k})$ is the Fourier transform of 21cm brightness temperature fluctuations $\delta T_b(\mathbf{r})$
- $\tilde{\delta}_{g}(\mathbf{k})$ is the Fourier transform of galaxy number density fluctuations $\delta_g(\mathbf{r}) = n_g(\mathbf{r})/\bar{n}_g - 1$
- The angle brackets denote statistical ensemble average (in practice, averages over Fourier modes in the same $k$ bin)
- The asterisk denotes complex conjugate (for real fields, the cross-power is real, but the notation emphasizes that the operation is a bilinear correlation)

### 2D Generalization

For the full 2D power spectrum separating perpendicular and parallel modes:

$$
P_\times(k_\perp, k_\parallel) = \langle \tilde{\delta}_{21}(k_\perp, k_\parallel)\, \tilde{\delta}_{g}^*(k_\perp, k_\parallel) \rangle
$$

This is the quantity actually used in [[EoRFlow]] and [[Pietschke et al 2026 (cross-correlation)]], where the 2D geometry is critical for foreground mitigation (galaxies have well-defined redshifts from spectroscopy, projecting cleanly onto $k_\parallel$).

## Cross-Correlation Coefficient and Coherence

### Definition: Correlation Coefficient

To quantify the **strength of correlation**, the cross-correlation coefficient is defined:

$$
r(k) = \frac{P_\times(k)}{\sqrt{P_{21}(k) \cdot P_g(k)}}
$$

where:
- $P_{21}(k)$ is the 21cm auto-power spectrum
- $P_g(k)$ is the galaxy auto-power spectrum
- $-1 \leq r(k) \leq 1$, with $r = 0$ meaning no correlation and $r = \pm 1$ meaning perfect correlation (anti-correlation)

**Physical interpretation:**
- $r(k) \to 1$: 21cm and galaxy fields are perfectly correlated (they trace the same structure with the same sign)
- $r(k) \to 0$: 21cm and galaxy fields are uncorrelated (independent fluctuations)
- $r(k) \to -1$: 21cm and galaxies are anti-correlated (opposite contrast: where galaxies peak, 21cm is depressed)

### Typical Values and Their Meaning

During reionization:
- **Large scales** ($k \lesssim 0.1$ Mpc$^{-1}$): $r(k) \approx 0.7 - 0.95$, because galaxies and ionizing photons trace similar large-scale structure, and HII regions expand from galaxy locations
- **Intermediate scales** ($0.1 \lesssim k \lesssim 0.5$ Mpc$^{-1}$): $r(k) \approx 0.4 - 0.8$, with decreasing correlation as velocity effects and ionization morphology details matter
- **Small scales** ($k \gtrsim 1$ Mpc$^{-1}$): $r(k) \lesssim 0.5$, limited by the finite lifetime and extent of HII regions

### Estimation from Data: Bias and Optimal Filtering

Given finite observational data with noise, the measured cross-power is:

$$
P_\times^\text{obs}(k) = P_\times^\text{true}(k) + N_\times(k)
$$

where $N_\times(k)$ is the noise (including thermal noise and residual foreground contamination). The noise in the cross-power is typically **lower than the auto-power noise**, because foregrounds (if uncorrelated with galaxies) mostly contribute to auto-powers and less to cross-powers.

**Bias correction:** If the 21cm noise is $N_{21}(k)$ and galaxy noise is $N_g(k)$, the cross-power picks up a bias term:

$$
\langle P_\times^\text{obs}(k) \rangle = P_\times^\text{true}(k) + \langle N_{21}(k) N_g(k) / 2 \rangle \approx P_\times^\text{true}(k)
$$

(For statistically independent noise sources, the bias is small, scaling as the product of noise levels.)

**Signal-to-noise ratio:** The SNR for detecting the cross-power is:

$$
\text{SNR}_\times = \frac{P_\times(k)}{\sqrt{N_{21}(k) \cdot N_g(k)}}
$$

which can be **larger than individual auto-power SNRs** if the foreground contamination is efficiently rejected and the two fields are sufficiently correlated.

## Why Cross-Power: Physical Motivation

### Foreground Rejection: The Uncorrelated Contamination Argument

**Radio foregrounds (synchrotron, free-free radiation) have specific properties:**
- Smooth spectrum across the 21cm observation band (intensity $\propto \nu^{-2.5}$)
- Bright point sources (AGN) with angular structure
- Galactic diffuse emission extending across the full sky
- **Crucially: Foreground structure on the sky has NO relation to galaxy positions**

Consider the observing geometry:
- A point source at angular position $(l, m)$ and frequency $\nu$ contributes to both the 21cm and any galaxy survey at that position
- But there is **no systematic correlation** between the source's brightness at frequency $\nu$ and the galaxy density at position $(l, m)$, because the foreground source is not a galaxy

Mathematically, if foreground contamination $\mathbf{F}$ is added to the true 21cm signal:

$$
\tilde{\delta}_{21}^\text{obs} = \tilde{\delta}_{21}^\text{true} + \tilde{F}
$$

then the cross-power becomes:

$$
P_\times^\text{obs}(k) = \langle (\tilde{\delta}_{21}^\text{true} + \tilde{F})\, \tilde{\delta}_{g}^* \rangle = P_\times^\text{true}(k) + \langle \tilde{F}\, \tilde{\delta}_{g}^* \rangle
$$

If the foreground $\tilde{F}$ and galaxy field $\tilde{\delta}_g$ are statistically independent (what they probe are independent structures), then:

$$
\langle \tilde{F}\, \tilde{\delta}_{g}^* \rangle = \langle \tilde{F} \rangle \langle \tilde{\delta}_{g}^* \rangle = 0
$$

(assuming zero-mean foreground fluctuations)

**Result:** Foregrounds are **suppressed in the cross-power** compared to the 21cm auto-power, while the true 21cm-galaxy correlation is retained. This provides powerful foreground rejection without requiring precise foreground subtraction (which is notoriously difficult in radio astronomy).

### Complementary Information: Breaking Degeneracies

The 21cm auto-power $P_{21}(k)$ is sensitive to:
- **Ionization fraction** $x_\text{HII}(z)$ — larger ionized regions suppress small-scale power
- **Ionization morphology** — clustered vs. diffuse reionization have different power spectrum shapes
- **Velocity fields** — redshift-space distortions affect power spectrum anisotropy

But $P_{21}(k)$ **alone** is degenerate in the source properties:
- A model with high escape fraction $f_\text{esc}$ and low efficiency $f_* M_h / M_\text{sfrH}$ (stars per halo mass) can produce the same ionization fraction $x_\text{HII}$ as a model with low $f_\text{esc}$ and high $f_*$
- Both produce similar $P_{21}(k)$, so the ionizing photon sources remain unconstrained

**Galaxy surveys provide complementary information:**
- Star-forming galaxies (traced by UV-selected or H-alpha emission surveys) directly measure $f_* M_h$ — the stellar mass density history
- Cross-correlating 21cm with galaxies measures how strongly 21cm perturbations are tied to galaxy positions
- A model with high $f_\text{esc}$ (photons escape easily, ionize distant gas, creating extended HII regions) produces **lower cross-correlation** (galaxy position is less predictive of local ionization state)
- A model with low $f_\text{esc}$ (photons trapped locally) produces **higher cross-correlation** (ionized regions tightly coupled to galaxy locations)

**Mathematical explanation:**
The cross-power is proportional to $f_\text{esc}$:

$$
P_\times(k) \propto \int d\nu \, \delta T_b^\text{signal}[\nu(z)] \, \delta_g[\nu(z)]
$$

The signal strength $\delta T_b \propto x_\text{HII}$. But $x_\text{HII}$ depends on both $f_\text{esc}$ (photon output per star) and galaxy positions. If $f_\text{esc}$ increases, the ionization fronts expand and become less tightly coupled to galaxy positions, **reducing correlation**. Thus, the cross-power is sensitive to $f_\text{esc}$ in a way the auto-power is not.

### "Confirmation of Cosmological Origin"

A secondary motivation: detecting a significant 21cm-galaxy cross-correlation at the expected strength would confirm the 21cm signal is **truly cosmological** (i.e., correlated with the matter distribution via galaxies) rather than a systematic or noise artifact that is uncorrelated with galaxies.

## Observational Considerations: Spectroscopic Redshifts

### Why Spectroscopic Redshifts are Essential

The success of 21cm-galaxy cross-correlation depends critically on **redshift accuracy**. Here's why:

**The problem with photometric redshifts:**
Galaxy photometric surveys (e.g., photometry-only, using broadband colors) achieve redshift precision $\sigma_z \sim 0.01(1+z) \sim 0.08$ at $z = 8$. In Fourier space, a redshift uncertainty maps to an error in the $k_\parallel$ coordinate:

$$
\Delta k_\parallel = \frac{d k_\parallel}{dz} \sigma_z \approx \frac{2\pi}{\Delta z_\text{Hubble}} \sigma_z
$$

where $\Delta z_\text{Hubble}$ is the Hubble distance in redshift units. At $z = 8$:

$$
\Delta k_\parallel \approx \frac{2\pi}{100 \text{ Mpc}} \times 0.08 \sim 0.005 \text{ Mpc}^{-1}
$$

This is **comparable to or larger than the power spectrum structure** on the scales we measure ($k_\parallel \sim 0.1 - 0.5$ Mpc$^{-1}$). The result: **photometric redshift errors smear out the cross-power**, removing the sharp features that distinguish different $f_\text{esc}$ models.

Quantitatively, the "smearing" reduces the cross-power amplitude:

$$
P_\times^\text{smeared}(k_\parallel) \approx P_\times^\text{true}(k_\parallel) \exp(-k_\parallel^2 \sigma_k^2)
$$

where $\sigma_k$ is the redshift error in $k_\parallel$ units. For $\sigma_k \sim 0.01$ Mpc$^{-1}$ and $k_\parallel \sim 0.2$ Mpc$^{-1}$:

$$
P_\times^\text{smeared} / P_\times^\text{true} \approx \exp(-(0.2 \times 0.01)^2) \approx 0.96
$$

which is acceptable. But if errors are larger (photometric $\sigma_z \sim 0.03$ vs spectroscopic $\sigma_z \sim 0.001$), the suppression becomes severe.

**Spectroscopic requirements:**
- **DESI** (Dark Energy Spectroscopic Survey): High-precision redshifts $\sigma_z \sim 0.0003(1+z) \sim 0.002$ at $z = 8$, near-perfect for cross-correlation
- **4MOST**: Similar precision to DESI
- **Euclid** (proposed spectroscopy): $\sigma_z \sim 0.001$ for some targets, sufficient
- **JWST early galaxies** (if spectroscopy performed): Can achieve $\sigma_z \sim 0.0001$, excellent

### Observational Geometry and Mode Coupling

Another practical consideration: when correlating a 21cm survey with a galaxy survey, the surveys have **different spatial footprints and sensitivities**:

$$
P_\times^\text{obs}(k) = \int d^3r_1 d^3r_2 \, W_{21}(\mathbf{r}_1) \, W_g(\mathbf{r}_2) \, \delta T_b(\mathbf{r}_1) \, \delta_g(\mathbf{r}_2)
$$

where $W_{21}(\mathbf{r})$ and $W_g(\mathbf{r})$ are the window functions (survey sensitivity, beam, coverage). The convolution of different window functions can couple $k$-modes, introducing correlations between different Fourier bins.

**Practical mitigation:**
- **Use the same survey patch** for both 21cm and galaxy data (spatial overlap required)
- **Deconvolve window functions** in post-processing
- **Use optimal estimators** that account for mode coupling (computationally expensive)

## Practical Estimation and Signal-to-Noise

### Direct Estimator

The simplest estimator for cross-power from observed data:

$$
\hat{P}_\times(k) = \frac{1}{V \cdot M_k} \sum_{\mathbf{k'} \text{ in bin } k} \tilde{\delta}_{21}^\text{obs}(\mathbf{k'}) \, [\tilde{\delta}_{g}^\text{obs}(\mathbf{k'})^*]
$$

where $M_k$ is a normalization factor accounting for the mode count and window functions.

### Noise in the Cross-Power

The covariance of the cross-power estimator:

$$
\text{Cov}(P_\times(k_i), P_\times(k_j)) = \begin{cases}
\frac{1}{N_\text{modes}(k)} [P_{21}(k) P_g(k) + P_\times^2(k)] & i = j \\
\text{smaller off-diagonal terms} & i \neq j
\end{cases}
$$

The noise variance (error bar) on each $P_\times(k)$ bin:

$$
\sigma[P_\times(k)] = \sqrt{\frac{P_{21}(k) P_g(k)}{N_\text{modes}(k)}}
$$

**Key point:** The noise in the cross-power depends on the **geometric mean** of the two auto-powers, not the sum. If one field (e.g., 21cm) is much noisier than the other (e.g., optical galaxy survey), the cross-power noise is dominated by the noisier field but is still lower than the auto-power noise of that field.

### Detection Significance

For a measurement of cross-power at multiple $k$ bins, the combined significance is:

$$
S/N = \sqrt{\sum_k \frac{[P_\times^\text{obs}(k) - P_\times^\text{model}(k)]^2}{\sigma^2[P_\times(k)]}}
$$

A typical HERA-plus-spectroscopic-galaxy detection might achieve $S/N \sim 5-10$ over the EoR-window modes ($k_\perp, k_\parallel \sim 0.01 - 0.5$ Mpc$^{-1}$), depending on integration time and foreground rejection effectiveness.

## Results from Pietschke et al. 2026 (Cross-Correlation Analysis)

Key findings from the reference paper:

1. **Constraint improvements:** Cross-power + auto-power jointly constrains $x_\text{HII}(z)$ with posterior volume (PV) 20–30% smaller than auto-power alone. The cross-power breaks degeneracies.

2. **Source property constraints:** The combination uniquely constrains $f_\text{esc}$ and $f_*$ separately:
   - Auto-power alone: $f_\text{esc}$ and $f_*$ highly degenerate, posterior volume $\gtrsim 70\%$ of prior
   - Cross-power + auto-power: $f_\text{esc}$ constrained to 50% of prior range, $f_*$ to 60% of prior range (rough numbers)
   
3. **Photometric redshift fatal flaw:** Including a photometric galaxy catalog instead of spectroscopic ($\sigma_z = 0.01$ vs. 0.001) **completely washes out** the constraint power of the cross-correlation:
   - $f_\text{esc}$ posterior volume returns to $\gtrsim 80\%$ of prior (nearly unconstraining)
   - The auto-power remains constraining, but the complementary information from cross-power is lost

4. **Foreground rejection quantified:** The foreground-suppression factor in the cross-power is $\sim 10-100$ depending on scale (larger suppression at high-$k_\parallel$ where foreground contamination is less severe). This allows safe use of modes that would be discarded in auto-power analyses.

## Physical Interpretation: How $f_\text{esc}$ Separates from $f_*$

### Physical Mechanism

Consider two limit cases:

**High escape fraction ($f_\text{esc} \approx 1$):**
- Ionizing photons escape galaxies easily
- They ionize gas at distances $\sim$ Jeans length (100s pc to kpc)
- HII regions become **large and overlapping**
- 21cm contrast (per unit ionized fraction) decreases: large ionized regions have lower small-scale power
- **Correlation with galaxies decreases:** an overdensity of galaxies does not strongly predict local 21cm (because photons from those galaxies have already ionized the whole region)

**Low escape fraction ($f_\text{esc} \approx 0.1$):**
- Ionizing photons are mostly absorbed inside galaxies or immediate halos
- HII regions are **small and tightly grouped around galaxies**
- 21cm contrast is high: small HII regions create more structure in the signal
- **Correlation with galaxies increases:** galaxy overdensities are highly predictive of HII region locations and local 21cm signal

The cross-correlation coefficient $r(k)$ explicitly captures this: $r(k) \propto (1 - f_\text{esc})$ (roughly), while the auto-power depends more sensitively on the total photon budget $f_\text{esc} \times f_*$.

### Disentangling $f_*$

The galaxy survey directly measures the spatial distribution of stellar mass (via star-forming galaxies). The cross-power's sensitivity to where the **ionizing sources are located** helps determine $f_*$ separately from $f_\text{esc}$:

- If $f_*$ is high, there are many stellar sources per unit volume, and ionizing photons come from everywhere
- If $f_*$ is low, ionizing photons come only from rare, massive halos
- These scenarios produce **different spatial distributions** of ionization fronts relative to all galaxy positions

By correlating 21cm with the full galaxy population (from surveys like DESI), the analysis can determine whether ionization traces high or low-mass galaxies, directly constraining $f_*$.

## Why This Matters for This Thesis

1. **Breaking the $f_\text{esc}$-$f_*$ degeneracy:** This thesis aims to separately constrain escape fraction and star formation efficiency. The cross-power is the primary lever for this goal.

2. **Improving constraints on ionization physics:** Even a modest $S/N$ detection of cross-power (say, $\sim 5\sigma$ for a few $k$ bins) would significantly improve constraints on the ionization morphology and source properties.

3. **Integrating spectroscopic surveys:** [[EoRFlow]] can be extended to include cross-power terms if spectroscopic galaxy catalogs become available (feasible with DESI, 4MOST, or Euclid). This thesis design anticipates this possibility.

4. **Foreground robustness:** The cross-power's foreground suppression potentially allows use of more observational modes, improving the information content relative to auto-power-only analyses.

## Connections to Related Concepts

- **[[2D Power Spectrum]]:** The 2D structure is critical for accurate cross-power measurement (redshift precision)
- **[[Power Spectrum as Summary Statistic]]:** Cross-power is a multi-field extension of this idea
- **[[Foreground Wedge]]:** Foregrounds are suppressed in cross-power precisely because they are uncorrelated with galaxies
- **[[EoRFlow]]:** The flow network can be extended to include cross-power as an additional observable, improving parameter inference
- **[[Ionizing Photon Sources]]:** Cross-power is most sensitive to the properties ($f_\text{esc}$, $f_*$) of ionizing sources
- **[[Redshift Space Distortions]]:** Affect both 21cm and galaxy surveys; must be understood to interpret cross-power correctly
