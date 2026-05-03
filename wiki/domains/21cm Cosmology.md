---
type: domain
title: "21cm Cosmology"
created: 2026-04-14
updated: 2026-04-16
tags:
  - domain/21cm
  - domain/cosmology
status: mature
related:
  - "[[Reionization Physics]]"
  - "[[Effective Field Theory]]"
---

# 21cm Cosmology

## What It Is: The Hyperfine Transition of Hydrogen

The 21 cm line is a hyperfine transition of neutral hydrogen (HI): a spin-flip of the electron relative to the proton, from the parallel-spin state (ortho-hydrogen) to the anti-parallel state (para-hydrogen). This transition is extremely weak — the Einstein A coefficient is $A = 2.87 \times 10^{-15}\,\text{s}^{-1}$ — which means a hydrogen atom takes an average of ~11 million years to undergo this transition spontaneously. However, it is **resonant** at rest-frame frequency $\nu_0 = 1420.405751768(2)\,\text{MHz}$ and has a well-defined, extremely narrow linewidth. Because the high-redshift Universe contains vast quantities of neutral hydrogen during the Dark Ages and Epoch of Reionization, this line can be used to map the structure of the intergalactic medium (IGM) across cosmic time.

**Redshift dependence:** Observed at redshift $z$, the signal is redshifted to frequency $\nu_\text{obs} = \nu_0 / (1+z) = 1420\,\text{MHz}/(1+z)$. Thus:
- At $z = 6$ (early reionization): $\nu_\text{obs} \approx 203\,\text{MHz}$
- At $z = 12$ (mid-reionization): $\nu_\text{obs} \approx 115\,\text{MHz}$
- At $z = 30$ (Cosmic Dawn): $\nu_\text{obs} \approx 44\,\text{MHz}$

HERA observes roughly in the range 50–250 MHz, corresponding to $z \sim 6$–$30$. SKA-Low will observe from 50 MHz to 350 MHz, probing $z \sim 6$–$35$.

## Historical Context and Observational Milestones

The 21 cm line has a rich history of discoveries:

1. **Van de Hulst prediction (1944):** Jan Hendrik van de Hulst theoretically predicted that HI in the Milky Way should emit at 21 cm.

2. **First detection (1951):** Edward Purcell and Harold Ewen first detected HI emission from the Milky Way at 21 cm using a horn antenna at Columbia University — confirming van de Hulst's prediction and opening the era of HI astronomy.

3. **Galactic HI mapping (1950s-1980s):** The 21 cm line became the primary tool for mapping Milky Way structure; the classic Shklovsky-Hibbard rotation curves were based on 21 cm mapping.

4. **Extragalactic HI surveys (1980s-2000s):** 21 cm enabled surveys of nearby galaxies and local universe structure (e.g., the Blind HI Parkes All-Sky Survey, HIPASS).

5. **Early universe 21 cm (2000s-present):** Recognition that the 21 cm signal from the Epoch of Reionization and Dark Ages is a powerful cosmological probe:
   - Global 21 cm signal (absorption profile) measured by EDGES (Bowman et al. 2018; Monsalve et al. 2021)
   - Power spectrum measurements attempted by LOFAR (Patil et al. 2017, upper limits)
   - HERA early constraints (2021-2023 season, improving limits)

## The 21cm Brightness Temperature

The observable in 21 cm cosmology is the **differential brightness temperature** $\delta T_b$, defined as the difference between the brightness temperature of the 21 cm radiation from the IGM and the brightness temperature of the cosmic microwave background (CMB):

$$
\delta T_b(\mathbf{x}, z) = T_\text{21cm}(\mathbf{x}, z) - T_\text{CMB}(z)
$$

In the **saturated spin-temperature limit** ($T_S \gg T_\text{CMB}$, which is well-justified for $z < 12$ after Ly$\alpha$ coupling and X-ray heating operate), the signal simplifies to:

$$
\delta T_b(\mathbf{x}, z) \approx 27\,\text{mK} \left(\frac{\Omega_b h^2}{0.022}\right) \left(\frac{0.15}{\Omega_m h^2}\right)^{1/2} \left(\frac{1+z}{10}\right)^{1/2} \, x_\text{HI}(\mathbf{x}, z) \left[1 + \delta_m(\mathbf{x}, z) - \frac{\partial_\parallel v_\parallel}{aH}\right]
$$

**Key components:**
- The overall normalization (~27 mK) includes the hyperfine temperature difference, cosmological parameters, and redshift factors
- $x_\text{HI}(\mathbf{x}, z)$ is the neutral hydrogen fraction: 0 if fully ionized, 1 if fully neutral
- $\delta_m(\mathbf{x}, z) \equiv [\rho_m(\mathbf{x},z) - \bar{\rho}_m(z)] / \bar{\rho}_m(z)$ is the matter overdensity
- $\partial_\parallel v_\parallel / (aH)$ is the redshift-space distortion term (line-of-sight velocity gradient in units of the Hubble parameter)

**Why this limit is used:** The saturated spin-temperature limit assumes that collisional excitation/de-excitation (via H-H collisions and electron scattering) and Ly$\alpha$ absorption/scattering couple the spin temperature $T_S$ of neutral hydrogen to the kinetic temperature $T_K$ of the gas. This is valid at $z < 12$ after cosmic reionization has begun and Ly$\alpha$ photons from star formation are abundant. At higher redshifts (Cosmic Dawn, $z \sim 12-30$), the spin temperature can depart from this limit and the signal can have the opposite sign. The thesis assumes throughout that this limit holds.

## 21cm as a Tomographic Probe

The 21 cm signal is a **three-dimensional tomographic probe** with properties very different from the CMB:

| Property | 21 cm | CMB |
|----------|-------|-----|
| Dimensionality | 3D (full volume) | 2D (surface) |
| Redshift coverage | $z \sim 6$-$30$ | $z \sim 1089$ (single epoch) |
| Number of modes | $\sim 10^6$-$10^7$ in cosmological surveys | $\sim 10^4$ multipole modes |
| Spatial resolution | $\lesssim 1$ Mpc (at meter-wavelength interferometry) | $\sim 200$ kpc (from power spectrum analysis) |
| Time coverage | Snapshots across $\Delta z \sim 24$ in redshift | Single snapshot, high precision |

This means 21 cm offers **vastly more modes** for statistical analysis than the CMB. A HERA observation of a 1 deg² field at $z \sim 8$ for 1000 hours yields information in ~10⁶ Fourier modes, compared to ~10⁴ for the full-sky CMB.

## The 21cm Brightness Temperature: Physical Interpretation

Breaking down the terms in the brightness temperature formula:

1. **$x_\text{HI}$ dependence:** The signal is proportional to the neutral fraction. Fully ionized regions ($x_\text{HI} = 0$) contribute zero signal; fully neutral regions contribute maximum signal.

2. **Density modulation $[1 + \delta_m]$:** Even at fixed $x_\text{HI}$, denser regions are brighter because they contain more neutral hydrogen atoms. This is the **density-weighted signal**.

3. **Redshift-space distortion $[\partial_\parallel v_\parallel / (aH)]$:** Peculiar velocities along the line of sight shift the observed frequency. Inflow (toward us) increases frequency, outflow decreases it. This creates a characteristic **Kaiser effect** in redshift space: overdense regions falling together appear "squashed" along the line of sight, while underdense regions (expanding) appear "elongated". This is exploited in 2D power spectrum analysis.

Combining these, the **EoR signal is unique**:
- During reionization ($z \sim 6-8$), the signal shows **bright ionized bubbles** (high $x_\text{HI}$ around sources) surrounded by **dark neutral regions** (low $x_\text{HI}$ in voids)
- At $z \sim 12$ (early reionization), small ionized bubbles are just beginning to overlap — highly patchiness
- At $z \sim 6$ (late reionization), large ionized regions dominate — smooth structure except at very small scales

## The Noise Model: Sensitivity of 21cm Interferometers

The observed 21 cm signal is contaminated by **noise** from multiple sources:

### Radiometric Noise (Thermal)

The signal-to-noise per baseline of an interferometer is determined by the radiometric equation:

$$
\text{SNR} = \frac{\Delta \Omega \sqrt{t \Delta \nu}}{T_\text{sys} \lambda^2 / (2 A_e)}
$$

where:
- $\Delta \Omega$ is the solid angle of the beam
- $t$ is the observation time
- $\Delta \nu$ is the frequency resolution (bandwidth per channel)
- $T_\text{sys}$ is the system temperature (receiver + sky noise)
- $\lambda$ is the wavelength
- $A_e$ is the effective antenna area

For HERA:
- Beam size at 150 MHz: $\sim 1°$
- System temperature: $T_\text{sys} \sim 500\,\text{K}$ (sky + receiver dominated)
- 1000-hour observations reach noise levels of $\sim 1\,\text{mK}^2$ in the power spectrum

### Sample Variance (Cosmic Variance)

Even with zero radiometric noise, cosmic variance (the finite volume of a survey) limits how well we can measure the power spectrum. For a survey volume $V$:

$$
\sigma^2_\text{sample} = \frac{P_{21}(k)^2}{(2\pi)^3 / V}
$$

For a 1 deg² field at $z \sim 8$ reaching $k \sim 0.1 h/\text{Mpc}$, cosmic variance is comparable to or dominates thermal noise.

### Foreground Contamination (Dominant)

Galactic synchrotron and extragalactic point sources are $\sim 4$–$5$ orders of magnitude **brighter** than the EoR 21 cm signal. Critical properties:

- **Sky brightness temperature:** Galactic synchrotron at 150 MHz is $\sim 300-600\,\text{K}$ (scales as $\nu^{-2.8}$)
- **EoR signal:** $\delta T_b \sim 10$–$100\,\text{mK}$ (depending on ionization state)
- **Contrast ratio:** Foregrounds are $10^4$–$10^5$ times brighter

Foreground mitigation is a major technical challenge:

1. **Spectral smoothness:** Galactic foregrounds vary smoothly with frequency (~MHz scales at 150 MHz), while the EoR signal varies on smaller frequency intervals (~10 kHz) due to Hubble-time line-of-sight structure. Foregrounds occupy a **foreground wedge** in $(k_\perp, k_\parallel)$ space.

2. **Chromatic Point Spread Function (PSF):** The antenna beam is slightly different at each frequency (chromatic), which mixes angular scales with frequency. This creates the characteristic **foreground wedge**: foregrounds appear primarily at large angles and low $k_\parallel$ values, while the **EoR window** (low $k_\perp$, high $k_\parallel$) is less contaminated.

3. **Foreground avoidance:** Rather than attempting to model and subtract foregrounds (which introduces systematic errors), most pipelines excise the foreground wedge, retaining only the EoR window with $k_\parallel / k_\perp \gtrsim 0.1$-$0.2$ (varies by instrument and assumed foreground model).

## Current Experimental Status

### HERA (Hydrogen Epoch of Reionization Array)

- **Status:** Operating (2018–present)
- **Location:** South Africa (Karoo)
- **Sensitivity:** Currently reaching noise floors of ~1 mK² in power spectrum at $z \sim 8$ with 1000-hour integrations
- **Recent results:** Upper limits on the reionization-era 21 cm power spectrum (2021-2023 season); upper limits constrain hot-ionosphere models and exclude certain reionization scenarios
- **Key advantage:** Redundant baselines (all ~14.6 m antenna spacing) allow precise calibration; good sensitivity to large-scale modes
- **Ongoing improvements:** Additional antennas planned; improved RFI mitigation

### LOFAR (Low-Frequency Array)

- **Status:** Operating (station commissioning 2012–2022; observations continuing)
- **Location:** Netherlands (with international stations)
- **Redshift range:** $z \sim 8-10$
- **Current results:** Upper limits on power spectrum; ongoing efforts on foreground mitigation and calibration
- **Key advantage:** Large collecting area (32 core stations, 48 remote); independent baselines

### MWA (Murchison Widefield Array)

- **Status:** Operating (2013–present)
- **Location:** Australia
- **Redshift range:** $z \sim 6-10$ (observing at higher frequencies than HERA/LOFAR for lower z)
- **Recent results:** Detection of HI absorption features in quasar spectra; constraints on the neutral fraction evolution

### SKA-Low (Square Kilometre Array Low Frequency)

- **Status:** Under construction (telescope design finalized; deployment 2027–2030)
- **Projected sensitivity:** ~100× more sensitive than HERA; able to measure the full reionization history in power spectrum mode
- **Redshift range:** $z \sim 6-35$
- **Expected impact:** First detections of the reionization-era 21 cm power spectrum; precise measurements of source properties ($\zeta$, $f_\text{esc}$, etc.)
- **Design:** ~130,000 antennas in a sparse random configuration; collecting area $\sim 1\,\text{km}^2$

## Key Observables and Their Information Content

### 1D Power Spectrum $P_{21}(k, z)$

The power spectrum is the Fourier transform of the two-point correlation function:

$$
P_{21}(k, z) = \frac{1}{(2\pi)^3} \int d^3 r \, e^{i\mathbf{k} \cdot \mathbf{r}} \langle \delta T_b(\mathbf{0}, z) \delta T_b(\mathbf{r}, z) \rangle
$$

**Advantages:**
- Compact (50–100 numbers for a full redshift cube)
- Well-understood Fisher forecasts and error budgets
- Connects directly to perturbation theory and EFT

**Limitations:**
- Isotropic power (averaged over directions) loses some information
- Cannot disentangle density and velocity contributions

**Information content:**
- Large scales ($k \lesssim 0.1 h/\text{Mpc}$): reionization history $\bar{x}_\text{HII}(z)$ and source bias
- Intermediate scales ($0.1 < k < 0.5 h/\text{Mpc}$): bubble morphology and EFT coefficients
- Small scales ($k > 0.5 h/\text{Mpc}$): departure from EFT, full bubble topology

### 2D Power Spectrum $P_{21}(k_\perp, k_\parallel)$

**Definition:** Separate the power spectrum by angular scale ($k_\perp$ in the plane of the sky) and line-of-sight scale ($k_\parallel$ along the redshift direction):

$$
\delta T_b(\mathbf{k}_\perp, k_\parallel, z) = \int d^2 x_\perp \int dz \, e^{i(\mathbf{k}_\perp \cdot \mathbf{x}_\perp + k_\parallel \Delta z)} \delta T_b(\mathbf{x}_\perp, z)
$$

and compute $P_{21}(k_\perp, k_\parallel) = \langle |\delta T_b|^2 \rangle$ in 2D bins.

**Advantages:**
- Enables **foreground wedge excision** (see [[Foreground Wedge]]): keep $|k_\parallel| / k_\perp \gtrsim 0.1-0.2$, avoid low $k_\parallel$ modes contaminated by smooth foregrounds
- Captures **redshift-space distortions** separately from density fluctuations
- Increases constraining power on EFT coefficients: Pietschke et al. (2025) show 2DPS yields Fisher constraints ~3× tighter than 1DPS

**Limitations:**
- More numbers (~500–1000 for full 2D grid)
- Requires careful modeling of foreground wedge edge

### 21cm × Galaxy Cross-Power Spectrum

**Definition:** Cross-correlate the 21 cm signal with the density field traced by galaxies (via spectroscopic surveys):

$$
P_{21 \times g}(k, z) = \langle \delta T_b(\mathbf{k}) \delta n_g(\mathbf{k}) \rangle
$$

where $\delta n_g$ is the galaxy density fluctuation.

**Advantages:**
- **Breaks degeneracies:** The cross-power depends on source properties (ionizing efficiency $\zeta$, escape fraction $f_\text{esc}$, stellar mass fraction $f_*$) in a different way than the 21 cm auto-power
- **Removes cosmic variance:** Two-point statistics from different tracers are less affected by cosmic variance
- **Direct source bias measurement:** $P_{21 \times g} / P_{gg}$ directly reveals the ionization bias relative to galaxy density

**Limitations:**
- Requires spectroscopic galaxy redshifts (expensive; currently available only in the local universe)
- 21 cm × galaxy cross-power at high-z requires joint SKA/JWST or similar

**Forecasts:** Pietschke et al. (2026) show that including cross-power constraints can improve $f_\text{esc}$ constraints by factor of ~2 compared to 21 cm power spectrum alone.

### Bispectrum (Higher-Order Statistics)

The bispectrum is the Fourier-space analog of the three-point correlation function:

$$
B_{21}(k_1, k_2, k_3) = \langle \delta T_b(\mathbf{k}_1) \delta T_b(\mathbf{k}_2) \delta T_b(\mathbf{k}_3) \rangle (2\pi)^3 \delta^3(\mathbf{k}_1 + \mathbf{k}_2 + \mathbf{k}_3)
$$

**Why it matters:**
- Sensitive to **non-Gaussianity** from reionization topology and bubble overlap
- Bubble overlap occurs through **percolation** — a topological phase transition — which is highly non-Gaussian
- The bispectrum shape changes as reionization progresses

**Current status:**
- Not yet routinely used in SBI pipelines (computationally expensive; Fisher forecasts show power spectrum often dominates)
- Potentially valuable for late-stage reionization when percolation effects are large

## The Foreground Wedge in Detail

### Physical Origin

Foregrounds (galactic synchrotron, extragalactic point sources) are much smoother in frequency than the 21 cm EoR signal. Their frequency structure is determined by the source spectral index (~-2.8 for synchrotron) and does not have the fine frequency structure of the EoR.

In an interferometer, **baseline $\mathbf{u}$** (antenna separation in wavelengths) maps to angular scales via $\theta \sim \lambda / |\mathbf{u}|$, where $\lambda$ is the wavelength. At a given frequency, different baselines probe different angular scales.

The **chromatic PSF** (frequency-dependent antenna beam) means that angular resolution varies slowly with frequency. Foregrounds, being smooth in frequency, appear primarily at modes with **low $k_\parallel / k_\perp$ ratios**: they occupy large angles (low $k_\perp$) and low line-of-sight frequency structure (low $k_\parallel$).

The **foreground wedge** is the region where foreground contamination is significant:

$$
|k_\parallel| \lesssim c_{\text{wedge}} \, k_\perp
$$

where $c_{\text{wedge}} \sim 0.05-0.1$ for HERA (depends on foreground model and acceptable contamination level).

### The EoR Window

The **EoR window** is the region outside the foreground wedge where EoR signal can be detected:

$$
|k_\parallel| \gtrsim c_{\text{wedge}} \, k_\perp
$$

In this window, foregrounds are weak enough that careful subtraction or avoidance is possible. The EoR window typically contains:

- Modes with $k_\parallel / k_\perp \gtrsim 0.1-0.2$ (varies by instrument)
- Corresponding to small-scale and intermediate-scale structures: $k \sim 0.05-1.0 h/\text{Mpc}$
- The bulk of the EFT-valid regime ($k < 0.5 h/\text{Mpc}$) is accessible

The wedge-removal strategy allows HERA and future experiments to make measurements in the EoR window by simply discarding modes in the wedge.

## Connection to Effective Field Theory

The 21 cm power spectrum, especially the 2D and cross-power variants, is the direct observational signature of the EFT coefficients $\{b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon}\}$. The EFT of the ionization field (see [[Effective Field Theory]]) predicts how $P_{21}(k)$ depends on these coefficients. Inference pipelines extract these coefficients by fitting the EFT model to measured power spectra.

## Key Concepts

- [[Brightness Temperature]]
- [[Neutral Fraction]]
- [[Power Spectrum as Summary Statistic]]
- [[2D Power Spectrum]]
- [[Cross-Power Spectrum]]
- [[Redshift Space Distortions]]
- [[Spin Temperature]]
- [[Foreground Wedge]]
- [[EoR Window]]

## Key Entities

- [[HERA]]
- [[LOFAR]]
- [[MWA]]
- [[SKA-Low]]

## Sources

- [[Choudhury 2022 (Reionization Intro)]] — Pedagogical overview including 21cm as observational probe; spin temperature discussion; foundational background
- [[Ferrara & Pandolfi (IGM Reionization)]] — IGM physics; Lyman-alpha forest; observational context for the neutral fraction
- [[Mesinger 2016]] — EoR review book (ed. Mesinger); Furlanetto chapter is standard 21cm pedagogy
- [[McQuinn & D'Aloisio 2018]] — EFT of the 21cm signal; connects large-scale structure to EFT coefficients
- [[Pietschke et al 2025 (EoRFlow)]] — 2DPS as SBI input; EoRFlow framework; improved constraints from 2D analysis
- [[Pietschke et al 2026 (cross-correlation)]] — 21cm × galaxy cross-power; constraints on source properties
- [[Qin et al 2022 (EFT Redshift Space)]] — Redshift-space EFT coefficients; validated on THESAN
