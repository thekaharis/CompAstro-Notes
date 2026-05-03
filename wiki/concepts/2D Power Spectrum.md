---
type: concept
title: "2D Power Spectrum"
created: 2026-04-14
updated: 2026-04-16
tags:
  - concept/statistics
  - domain/21cm
status: expanded
complexity: intermediate
domain: "[[21cm Cosmology]]"
aliases:
  - "2DPS"
  - "cylindrically averaged power spectrum"
  - "wedge-filtered power spectrum"
related:
  - "[[Power Spectrum as Summary Statistic]]"
  - "[[Foreground Wedge]]"
  - "[[EoRFlow]]"
  - "[[Redshift-Space Distortions]]"
  - "[[Kaiser Effect]]"
sources:
  - "[[Pietschke et al 2025 (EoRFlow)]]"
  - "[[Morales & Wyithe 2010 (21cm Observables)]]"
  - "[[Pober et al 2014 (HERA Foreground Wedge)]]"
---

# 2D Power Spectrum

## Definition and Basic Concept

The 2D (cylindrically averaged) power spectrum $P(k_\perp, k_\parallel)$ is a fundamental statistical measure that separates Fourier modes perpendicular to the line of sight ($k_\perp$) from modes along the line of sight ($k_\parallel$). This separation is crucial in 21cm cosmology because the two directions probe fundamentally different physics:

- **$k_\perp$ (transverse/perpendicular modes):** Trace spatial structure across the sky (angular scales). These modes directly correspond to comoving distances perpendicular to our line of sight. Conversion to physical scale: $\Delta\theta \approx \frac{\lambda}{D_A}$ relates to $k_\perp \approx \frac{2\pi}{\Delta\theta \cdot D_A}$ where $D_A$ is the comoving angular diameter distance.

- **$k_\parallel$ (parallel modes along line of sight):** Trace frequency/redshift structure. These modes are sensitive to the radial dimension, which probes both spatial structure along the line of sight and peculiar velocity effects. For a frequency resolution $\Delta \nu$, the wavenumber scale is $k_\parallel \approx \frac{2\pi \Delta \nu}{\nu_{21}} \frac{dz}{d\nu}$ where the derivative converts frequency differences to redshift differences.

## Mathematical Form

$$
P_{21}(k_\perp, k_\parallel) = \langle |\tilde{\delta}_{21}(k_\perp, k_\parallel)|^2 \rangle
$$

where:
- $\tilde{\delta}_{21}(k_\perp, k_\parallel)$ is the Fourier transform of the 21cm brightness temperature fluctuation $\delta T_b(\mathbf{r})$ in cylindrical coordinates
- The 2D power spectrum is computed by azimuthally averaging over the angle $\phi$ in the plane perpendicular to the line of sight
- $k_\perp = \sqrt{k_x^2 + k_y^2}$ is the magnitude of the perpendicular wavevector
- $k_\parallel = k_z$ is the component along the line of sight

**Why azimuthal averaging?** The underlying 3D matter field (and thus ionization field) is statistically isotropic in the sky plane at fixed redshift. Thus, rotations around the line of sight should not change the power. Averaging over azimuthal angle improves signal-to-noise by combining information from different sky directions that probe the same physical scale.

## Practical Form with 1D Averaging

In practice, observers construct the 2DPS by:

1. **Gridding the data** into 3D Fourier space with axes $(k_x, k_y, k_\parallel)$
2. **Computing the FFT** from the observed brightness temperature cube
3. **Cylindrically binning** the power into annuli of fixed $k_\perp = \sqrt{k_x^2 + k_y^2}$ and fixed $k_\parallel$
4. **Averaging** power values that fall in the same $(k_\perp, k_\parallel)$ bin

This procedure can be written as:

$$
P_{21}(k_\perp, k_\parallel) = \frac{1}{N_\text{modes}(k_\perp, k_\parallel)} \sum_{(k_x, k_y, k_z) \text{ in bin}} |\tilde{\delta}_{21}(k_x, k_y, k_z)|^2
$$

where the sum is over all $(k_x, k_y)$ pairs satisfying $\sqrt{k_x^2 + k_y^2} \approx k_\perp$ for a fixed $k_z = k_\parallel$.

## Foreground Wedge Geometry

### The Wedge in $(k_\perp, k_\parallel)$ Space

Foreground contamination (synchrotron radiation, point sources, galaxies) enters primarily through power that couples the sky brightness to the frequency axis via a specific relationship. The key insight is that foregrounds have angular structure on the sky that is **smooth in frequency** (because their spectrum across the 21cm observation band is smooth). In Fourier space, this means foreground power is concentrated at small $k_\parallel$ (low frequency variation, high coherence across the band) and can have any $k_\perp$ (any angular scale).

More precisely, the foreground wedge occupies the region:

$$
k_\parallel < \frac{k_\perp}{\sin\theta} \approx \frac{k_\perp}{\theta} \quad \text{(for small angles)}
$$

where $\theta$ is the observing beam width. This creates a **triangular "wedge"** in the $(k_\perp, k_\parallel)$ plane with its apex at the origin and its edges defined by $k_\parallel \propto k_\perp$.

### Why the Wedge Exists: The Delay Signature

Foregrounds entering via cross-talk between spatial and spectral dimensions create what is called the "delay signature." Consider a bright point source at angular position $(l_0, m_0)$ with a smooth spectrum $S(\nu)$ across the observation band. Its Fourier transform in $(k_x, k_y, k_\parallel)$ space will show power concentrated near $(k_x, k_y)$ corresponding to the angle $(l_0, m_0)$ but spread in $k_\parallel$ according to the smoothness of $S(\nu)$. Instrumental effects (antenna primary beam, cable delays, imperfect bandpass subtraction) couple spatial frequencies to spectral frequencies in a way that concentrates power in the low-$k_\parallel$ region.

### Using the Wedge for Foreground Avoidance

The critical advantage of the 2DPS over 1D power spectrum: **we can precisely excise the contaminated wedge region without losing all information about a given $(k_x, k_y)$ pair.** In the 1D power spectrum $P(k)$, all Fourier modes with the same magnitude $k = \sqrt{k_x^2 + k_y^2 + k_z^2}$ are averaged together regardless of their location in $(k_\perp, k_\parallel)$ space. If foreground contamination affects some $(k_x, k_y, k_z)$ tuples with $|k| = k_0$, we must discard the entire spherical shell $k = k_0$, losing all information about the uncontaminated modes with the same magnitude.

With 2DPS, we keep all modes with $k_\parallel > k_\parallel^\text{max wedge}(k_\perp)$, discarding only the foreground-contaminated region. This typically allows retention of $\gtrsim 50\%$ more Fourier modes compared to aggressive 1D filtering.

## Redshift-Space Distortions and the Kaiser Effect

### Why $k_\perp$ and $k_\parallel$ Matter Differently

A crucial reason the 2DPS is essential is that **peculiar velocities affect radial and transverse directions differently.** Galaxy/gas peculiar velocities (from falling into overdensities and escaping from underdensities) systematically distort the clustering pattern. Specifically:

- **Peculiar velocity component along the line of sight** ($v_\parallel$) shifts the observed redshift: $z_\text{obs} = z_\text{true} + (1+z) v_\parallel / c$. This maps spatial information along the line of sight to frequency space, distorting the $k_\parallel$ distribution of modes.

- **Peculiar velocity component perpendicular to the line of sight** ($v_\perp$) causes minimal cosmological distortion because line-of-sight distance is determined by frequency, not by transverse position.

The **Kaiser formula** quantifies this anisotropy:

$$
P(k_\perp, k_\parallel) = P_0(k) \left[ 1 + \beta \frac{k_\parallel^2}{k^2} \right]^2
$$

where:
- $P_0(k)$ is the underlying real-space (matter) power spectrum (isotropic in 3D)
- $\beta = f/b$ is the redshift-space distortion parameter, with $f \approx \Omega_m(z)^{0.55}$ the logarithmic growth rate and $b$ the galaxy bias
- The factor $[k_\parallel^2 / k^2]$ weights the effect: at fixed $k$, modes with $k_\parallel \gg k_\perp$ (nearly radial) show the strongest distortion; modes with $k_\parallel \ll k_\perp$ (nearly transverse) show minimal distortion
- The $(1 + \beta k_\parallel^2 / k^2)^2$ form means redshift-space distortions **enhance power** along the line of sight ("Kaiser enhancement" or "Fingers of God" in galaxy surveys)

For the **21cm signal during reionization**, the interpretation is subtly different:
- During reionization, ionized regions expand and neutral regions are surrounded by ionized gas. This creates a "bias" structure where the HII region boundary traces the underlying matter density
- Additionally, the reionizing front's expansion creates coherent velocity patterns (HII regions expanding outward)
- These effects create anisotropy between $k_\perp$ and $k_\parallel$, though the sign and magnitude differ from galaxy RSD

### Observational Implications: Typical $k$ Values

Realistic 21cm instruments can access different ranges of $k_\perp$ and $k_\parallel$:

**Transverse scales ($k_\perp$):** Determined by the field of view and angular resolution
- **SKA-Low** (operating at $z \sim 8$ during reionization): Field of view $\sim 1°$ yields $k_\perp \sim 0.01 - 1$ Mpc$^{-1}$ range. Higher resolution beams ($\sim 2$-$10$ arcsec) access $k_\perp \sim 1 - 100$ Mpc$^{-1}$.
- **HERA** (144 element array): FoV $\sim 0.5°$ provides $k_\perp \sim 0.02 - 2$ Mpc$^{-1}$ depending on frequency.

**Radial scales ($k_\parallel$):** Determined by frequency resolution and bandwidth
- Frequency resolution $\Delta \nu = 100$ kHz over 21cm (1.4 GHz, $\nu_{21}$ at $z=8$, band roughly 180-200 MHz) maps to $\Delta z \approx 0.01$ at $z=8$
- This corresponds to $k_\parallel \sim 0.1 - 0.5$ Mpc$^{-1}$ depending on redshift
- Wider bandwidth increases the range of $k_\parallel$ accessible (up to $\sim 1$ Mpc$^{-1}$ for full band)

**Typical science-accessible scales** lie in the **2D "EoR window"**: $0.01 - 0.5$ Mpc$^{-1}$ (both directions), corresponding to Mpc-scale structure during reionization.

## Estimation from Data: Methods and Systematics

### Power Spectral Estimation Methods

Several algorithms are used to estimate the 2DPS from observational data cubes:

**1. Direct FFT + Cylindrical Binning** (most common for 21cm)
- Apply FFT to the calibrated data cube in $(x, y, \nu)$ coordinates
- Apply window function to each spatial and spectral dimension (Hann, Blackman, or matched filter)
- Compute power spectrum as $P = |FFT|^2 / (V \cdot W)$ where $W$ is the normalization factor for the window
- Bin into $(k_\perp, k_\parallel)$ grid
- Advantages: Simple, fast, easy to parallelize
- Disadvantages: Spectral leakage from strong foregrounds can corrupt weak EoR signal

**2. CLEAN-like Deconvolution** (adapted from radio interferometry)
- Iteratively remove bright contamination (foreground mode by mode)
- Used in HERA analysis pipeline
- Advantages: Can suppress foreground leakage
- Disadvantages: Computationally expensive, risk of over-subtraction

**3. Matched Filtering / Optimal Weighting**
- Weight modes inversely by their noise variance: $w(k) \propto 1/[\sigma^2_\text{noise}(k)]$
- Maximizes signal-to-noise for detection
- Advantages: Reduces noise bias
- Disadvantages: Different weighting for different $(k_\perp, k_\parallel)$ complicates interpretation

### Noise Model Differences Between Directions

A crucial asymmetry in 21cm observations is the **noise variance's different dependence on direction:**

**Perpendicular ($k_\perp$) noise:**
- Dominated by **thermal receiver noise** summed over baseline combinations
- Scales as $\sigma^2_\perp \propto 1/(N_\text{baselines} \cdot \Delta \nu \cdot \Delta t)$
- Improves with longer integration time $\Delta t$ and wider bandwidth $\Delta \nu$
- More baselines (denser array) reduce noise

**Parallel ($k_\parallel$) noise:**
- Dominated by **spectral sensitivity** and **bandpass calibration uncertainties**
- Scales as $\sigma^2_\parallel \propto (\Delta f_\text{rms} / f_\text{avg})^2$ where $\Delta f_\text{rms}$ is the RMS bandpass calibration error
- **Frequency channels are not independent:** correlations between adjacent channels from foreground contamination and instrument response
- RFI excision creates correlated gaps in frequency space
- Noise in $k_\parallel$ improves more slowly with observation time (spectral systematics are quasi-static)

**Practical consequence:** The 2DPS is typically noisier in $k_\parallel$ than $k_\perp$ at comparable scales, making foreground rejection in the low-$k_\parallel$ region critical (where signal is weakest anyway).

## Contrast with 1D Power Spectrum

The spherically averaged 1D power spectrum $P(k)$ compresses all directional information:

$$
P_1(k) = \int_0^{2\pi} d\phi \int_0^{\pi} d\theta \, P(k, \theta) \quad \text{(radial average)}
$$

where $\theta$ is the angle between $\mathbf{k}$ and the line of sight.

**Loss of information:**
- All $(k_\perp, k_\parallel)$ modes with the same $|k|$ are averaged together
- Redshift-space distortion anisotropy is washed out
- Foreground contamination cannot be precisely excised: a contaminated mode at $(k_\perp = 0.2, k_\parallel = 0.05)$ forces discard of all modes with $|k| \approx 0.206$ Mpc$^{-1}$
- Cannot separate transverse and radial sensitivity to different astrophysics (e.g., ionization morphology vs. velocity structure)

## Why This Matters for This Thesis

The thesis leverages the 2DPS for several critical advantages:

1. **Foreground Avoidance Without Complete Mode Loss:** By using the 2DPS and carefully excising only the foreground wedge, the [[EoRFlow]] analysis retains $\sim 50\%$ of the Fourier information compared to 1D spherical filtering. This improves posterior constraints on ionization parameters by $\sim 20-30\%$ relative to 1D power.

2. **Resolving Redshift-Space Distortions:** The anisotropy between $k_\perp$ and $k_\parallel$ carries information about **peculiar velocity fields** (via Kaiser enhancement) and the **morphology of reionization** (anisotropic ionization fronts expanding from biased source distribution). The 2DPS can in principle extract this geometric information, though the thesis primarily uses it for foreground rejection.

3. **Cross-Correlation with Galaxy Surveys:** When cross-correlating with spectroscopic galaxy surveys (via [[Cross-Power Spectrum]]), precise measurement of $(k_\perp, k_\parallel)$ becomes essential. Galaxy surveys measure positions and redshifts, projecting information onto the $(k_\perp, k_\parallel)$ grid. Accurate accounting of the 2D geometry is necessary to avoid smearing the cross-power signal.

4. **EoRFlow Framework:** The [[Pietschke et al 2025 (EoRFlow)]] analysis used in this thesis directly models and constrains the 2DPS. Understanding the structure of the 2DPS — where signal lives, where foregrounds live, which modes are most informative — is essential to interpreting the flow network's inference.

5. **Simulator Dependence Mitigation:** Different [[Reionization Simulations]] (21cmFAST, AMBER, full RTM) produce different ionization patterns, which manifest as different anisotropy signatures in the 2DPS. By fitting to the 2DPS rather than 1D power, the thesis can potentially break degeneracies between different astrophysical models.

## Connections to Related Concepts

- **[[Foreground Wedge]]:** Defines which $(k_\perp, k_\parallel)$ modes are contaminated and must be cut
- **[[Power Spectrum as Summary Statistic]]:** Provides the theoretical context; 2DPS is a multi-dimensional summary statistic
- **[[Redshift-Space Distortions]]:** Cause the anisotropy between $k_\perp$ and $k_\parallel$
- **[[Kaiser Effect]]:** The specific formula for RSD anisotropy
- **[[EoRFlow]]:** Uses 2DPS as input data for the flow network inference
- **[[Cross-Power Spectrum]]:** 2DPS of galaxies and 21cm are separately estimated, then cross-correlated
- **[[21cm Cosmology]]:** Parent concept; 2DPS is the most commonly used summary statistic
