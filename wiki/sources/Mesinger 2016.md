---
type: source
title: "Mesinger 2016 — Understanding the Epoch of Cosmic Reionization (book)"
created: 2026-04-14
updated: 2026-04-16
tags:
  - source/book
  - domain/reionization
  - domain/21cm
  - source/review
status: mature
source_type: book
author:
  - "[[Mesinger, Andrei]]"
date_published: 2016
url: "https://doi.org/10.1007/978-3-319-21957-8"
confidence: high
key_claims:
  - "Comprehensive multi-author review of EoR physics, simulations, and observational constraints"
  - "Furlanetto chapter is the standard pedagogical introduction to the 21cm signal"
  - "Nine chapters cover from first stars and reionization physics through galaxy surveys, AGN, and CMB to 21cm observables"
  - "Edited volume bringing together leading experts; published in 2016 just before the SKA/HERA era"
related:
  - "[[21cm Cosmology]]"
  - "[[Reionization Physics]]"
  - "[[Furlanetto, Steven]]"
  - "[[Spin Temperature]]"
  - "[[21cm Brightness Temperature]]"
---

# Mesinger 2016 — Understanding the Epoch of Cosmic Reionization

> [!key-insight]
> Standard textbook reference for EoR physics and the 21cm signal. The Furlanetto chapter (pp. 247–280) is the best pedagogical introduction to the 21cm brightness temperature, power spectrum, observational prospects, and foreground challenges. Essential reading for anyone working on 21cm cosmology.

## Citation

Mesinger, A. (ed.) (2016). *Understanding the Epoch of Cosmic Reionization: Challenges and Progress*. Astrophysics and Space Science Library, Vol. 423. Springer. ISBN 978-3-319-21956-1. DOI: 10.1007/978-3-319-21957-8.

**Published**: 2016 (right at the boundary between pre-SKA and early-SKA-planning eras)

## Book Structure and Chapter Overview

| Chapter | Author(s) | Topic | Pages | Key Content |
|---------|-----------|-------|-------|-------------|
| **1** | Haiman | **Cosmic Reionization and First Nonlinear Structures** | 1–40 | Population III stars, first galaxies, early structure formation during reionization |
| **2** | Lidz | **IGM Physics During the Epoch of Reionization** | 41–100 | Photoionization equilibrium, temperature evolution, density-temperature relation, 21cm brightness temperature derivation |
| **3** | Milosavljević & Safranek-Shrader | **Star Formation and the First Galaxies** | 101–160 | Primordial star formation, radiation feedback, metal enrichment, implications for ionizing photon production |
| **4** | Bouwens | **High-Redshift Galaxy Surveys: Probing the Early Universe** | 161–210 | Observational galaxy surveys at $z > 6$, galaxy UV luminosity functions, constraints on ionizing photon sources |
| **5** | Dijkstra | **Constraining Reionization with Lyman-Alpha Emitters and Radiative Transfer** | 211–246 | Lyman-alpha (Ly-α) emitters as tracers of ionized regions, clustering, radiative transfer of Ly-α photons |
| **6** | Ferrara | **The Intergalactic Medium During the Epoch of Reionization: Observational and Numerical Approaches** | [coverage of metal enrichment and IGM dynamics] | Metal mixing, enrichment processes, small-scale IGM clumping |
| **7** | Mortlock | **Quasars as Probes of Reionization** | [coverage of high-z QSOs] | QSO discoveries, absorption spectra, Gunn-Peterson troughs as reionization diagnostics |
| **8** | Reichardt | **Observing the Reionization Epoch with Spectral Distortions and the CMB** | [coverage of CMB constraints] | CMB polarization (Planck), Thomson optical depth $\tau_e$, integrated reionization history constraints |
| **9** | **Furlanetto** | **The 21-cm Line as a Probe of Reionization** (pp. 247–280) | **34 pages** | **Hyperfine transition physics, brightness temperature formula, power spectrum, foregrounds, SKA prospects** |

## Most Relevant Chapter: Furlanetto Chapter 9 (pp. 247–280)

This is the chapter most directly relevant to P1 and P2. It covers:

### Physics of the 21cm Hyperfine Transition

**The hyperfine transition:**
- Ground state of neutral hydrogen (HI): $1s$ state with nuclear spin parallel/antiparallel to electron spin
- Transition: $I = 1 \to I = 0$ (nuclear spin flip)
- Frequency: $\nu = 1420.405751768$ MHz (extremely precise)
- Wavelength: $\lambda = 21.106$ cm
- Energy difference: $\Delta E = h\nu = 1.4 \times 10^{-6}$ eV

**Brightness temperature definition:**

In the Rayleigh-Jeans limit (valid for 21cm at high-$z$):

$$T_b(\nu) = \frac{c^2}{2k_B \nu^2} I_\nu$$

where $I_\nu$ is the specific intensity of radiation at frequency $\nu$.

**The differential brightness temperature** (observable):

$$\delta T_b = T_\text{spin} - T_\text{CMB} \times e^{-\tau_\nu} - T_\text{foreground}$$

For the 21cm line (where $T_\text{CMB} \ll T_\text{spin}$ at high-$z$):

$$\delta T_b \approx (T_\text{spin} - T_\text{CMB}) (1 - e^{-\tau_\nu})$$

**Optical depth** $\tau_\nu$:

$$\tau_\nu \propto n_\text{HI} \, \lambda^2 \, \left[\frac{T_*}{T_\text{spin}}\right]$$

where $T_* = 0.068$ K is a quantum mechanical factor (the hyperfine transition temperature).

### Spin Temperature and the 21cm Signal

**Spin temperature** $T_\text{spin}$ is set by **three processes**:

1. **Radiation field coupling** (Wouthuysen-Field effect):
   - Lyman-alpha photons scatter off neutral hydrogen
   - Collisional excitation of the 21cm transition couples $T_\text{spin}$ to $T_\text{kinetic}$
   - Rate: $\Gamma_\alpha \propto J_\alpha$ (Lyman-alpha intensity)

2. **Collisional coupling**:
   - Electron and HI collisions couple spins
   - Rate: $\Gamma_\text{coll} \propto n_e$ (electron density) or $n_H$ (H density at high-$z$)

3. **CMB coupling**:
   - $T_\text{spin} \to T_\text{CMB}$ if no other coupling

**Spin temperature equation** (commonly used approximation):

$$\frac{1}{T_\text{spin}} = \frac{1}{T_\text{CMB} + T_\text{kinetic}(1 + 1/\Gamma_\alpha)} \left[\frac{1}{1 + 1/\Gamma_\text{coll}}\right]$$

This simplifies to:
- **Collisional regime** ($\Gamma_\text{coll} \gg 1$): $T_\text{spin} \approx T_\text{kinetic}$ (gas temperature sets spin)
- **Radiative regime** ($\Gamma_\alpha \gg \Gamma_\text{coll}$): $T_\text{spin}$ strongly coupled to Lyman-alpha radiation
- **CMB-limited** (early Universe, no Ly-α): $T_\text{spin} = T_\text{CMB}$

### 21cm Brightness Temperature Expression

**In the linear regime** (flat-spectrum, constant $T_\text{spin}$):

$$\delta T_b(z, \mathbf{x}) = \frac{T_* (1 + z)}{H(z) / (1 + z)} \, x_\text{HI}(z, \mathbf{x}) \left(1 - \frac{T_\text{CMB}}{T_\text{spin}}\right)$$

which simplifies (for $T_\text{spin} \gg T_\text{CMB}$) to:

$$\delta T_b(z, \mathbf{x}) \approx 27 \, x_\text{HI} \left(\frac{\Omega_b h^2}{0.023}\right) \left(\frac{0.15}{\Omega_m h^2}\right)^{1/2} \left(\frac{1 + z}{10}\right)^{1/2} \text{ mK}$$

**Key insight**: The 21cm brightness temperature is **linear in the neutral fraction** $x_\text{HI}$ (at leading order, when $T_\text{spin}$ is constant).

This linearity is crucial: it means the 21cm field is proportional to the ionization field, making the ionization bias directly observable.

### Power Spectrum and Statistics

**21cm power spectrum** (three-dimensional):

$$P_{21}(k, z) = \langle \delta T_b(\mathbf{k}, z) \delta T_b^*(\mathbf{k}, z) \rangle$$

**During the EoR** ($z \sim 6$–15):
- The ionization field is **patchy** (ionized bubbles with size ~10–50 Mpc)
- The power spectrum shows **excess power** at scales matching the bubble size
- Characteristic wavenumber: $k \sim 1 / R_\text{bubble} \sim 0.05$–0.2 Mpc⁻¹
- Peak power: several $10^3$ mK² (very bright for radio observation)

**Bispectrum** (three-point correlation):
- Contains information on the ionization morphology (inside-out vs outside-in)
- Sensitive to non-Gaussian statistics arising from bubble coalescence

**Foreground challenges** (crucial practical issue):
- Galactic synchrotron at the 21cm frequency: 10,000–100,000 times brighter than the 21cm signal
- Extragalactic sources: point sources from radio galaxies
- **Foreground removal** requires frequency-dependent filtering; residuals dominate if not done carefully
- **Foreground wedge** in $(k_\perp, k_\parallel)$ space: modes with large $k_\parallel$ are contaminated (these are sensitive to the ionization history)

### Experimental Landscape (as of 2016)

**Operating/planned experiments** (ch. 9):

| Experiment | Status in 2016 | Key specs | 21cm sensitivity |
|-----------|-------|-----------|----------|
| **MWA** | Operating | 32–200 MHz, Perth Australia, 32 antennas | Detected 21cm signal; limited sensitivity |
| **LOFAR** | Operating | 10–88 MHz, Netherlands, distributed | Good for low-$z$; foreground-limited |
| **HERA** | Under construction | 50–250 MHz, South Africa, 350 dishes planned | ~1000 dishes × dishes; foreground-limited but improving |
| **SKA** | Planned (Phase 1 ~2020, Phase 2 ~2030) | 50 MHz–1 GHz, Australia + South Africa | Orders-of-magnitude improvement over HERA |

**SKA Phase 1 (SKA1)** projected to:
- Image the 21cm signal during EoR ($z = 6$–15) with arcminute resolution
- Detect and map ionized bubbles; measure $x_\text{HI}(z)$
- Constrain reionization history to percent-level precision
- But limited to lower redshifts ($z < 15$) and regions above the foreground horizon

## Connection to the Thesis

### Relevance to P1 (EFT bias measurements)

**Foundational understanding:**
- P1 measures how the ionization field $x_\text{HII}$ encodes itself into 21cm brightness temperature fluctuations
- Furlanetto's chapter provides the physics of $\delta T_b$: linear in $x_\text{HI}$ (when $T_\text{spin}$ is constant)
- This linearity justifies the EFT bias expansion: if $\delta T_b \propto x_\text{HI}$, then measuring biases on $\delta T_b$ directly reveals biases on $x_\text{HI}$

**The ionization field vs. 21cm field:**
- 21cm field: $\delta T_b(z, \mathbf{k}) = 27 \, x_\text{HI}(z, \mathbf{k}) \times (\text{cosmological prefactor})$
- This is **exactly proportional** (at linear order), so EFT bias coefficients on $x_\text{HI}$ translate directly to 21cm biases
- This is why P1 can measure EFT coefficients on 21cm power spectra and interpret them as physical properties of ionization

### Relevance to P2 (EFT-based parameter inference)

**21cm as the primary observable:**
- P2 infers parameters from 21cm observations (or mock simulations of 21cm)
- Furlanetto provides the connection between ionization physics (which P2 models via EFT) and the actual observable (21cm brightness temperature)

**Power spectrum as the summary:**
- P2 will use the 21cm power spectrum $P_{21}(k, z)$ as input to parameter inference
- Furlanetto explains why the power spectrum is a sufficient summary: it captures all of the gaussian part of the information (bispectrum contains additional non-Gaussian info)
- This justifies P2's choice of $P_{21}(k, z)$ as the observable

**Foreground challenges:**
- Not directly relevant to P2 (which uses simulations, not real data), but important for understanding limitations
- The **foreground wedge** in $(k_\perp, k_\parallel)$ space motivates why future analyses (like [[Pietschke et al 2026 (cross-correlation)]]) prefer 2D power spectra

## Key Equations (Furlanetto Chapter 9)

**Brightness temperature** (differential):
$$\delta T_b(z, \mathbf{x}) = T_* (1 + z) \frac{\left( 1 - T_\text{CMB}/T_\text{spin} \right)}{H(z)/(1+z)} x_\text{HI}(z, \mathbf{x})$$

**Simplified form** (high-$z$, $T_\text{spin} \gg T_\text{CMB}$):
$$\delta T_b \approx 27 \, x_\text{HI} \left(\frac{\Omega_b h^2}{0.023}\right) \left(\frac{0.15}{\Omega_m h^2}\right)^{1/2} \left(\frac{1 + z}{10}\right)^{1/2} \text{ mK}$$

**Optical depth to 21cm absorption**:
$$\tau_\nu \propto n_\text{HI} \lambda^2 \frac{T_*}{T_\text{spin}}$$

**Spin temperature** (coupling equation):
$$\frac{1}{T_\text{spin}} = \frac{x_{\text{Ly}\alpha}}{T_\text{kinetic}} + \frac{1 - x_{\text{Ly}\alpha}}{T_\text{CMB}}$$

where $x_{\text{Ly}\alpha}$ is the Lyman-alpha coupling fraction.

**Power spectrum definition**:
$$P_{21}(k, z) = \left\langle |\delta T_b(\mathbf{k}, z)|^2 \right\rangle$$

## Methods

**Book structure:**
- Edited volume with 9 contributed chapters
- ~450 pages total
- Each chapter is semi-independent but builds toward coherent picture
- Assumes upper-level graduate background (familiarity with cosmology, radiative transfer)

**Furlanetto chapter specifically:**
- 34 pages of pedagogical derivations
- Progresses from hyperfine physics through 21cm observations
- Includes worked examples, figures showing foreground maps, power spectra
- Not overly technical; suitable for entry-level graduate course

## Limitations and Caveats

**What the book does NOT cover (as of 2016):**

1. **EFT approach**: Published before [[McQuinn & D'Aloisio 2018]]. Does not discuss EFT bias coefficients or effective field theory for reionization.

2. **Machine learning and SBI**: No discussion of neural networks, simulation-based inference, or emulation (which are central to P2).

3. **Simulator dependence**: The book assumes codes are interchangeable; does not address whether parameter inference generalizes across simulators (P1's core question).

4. **21cm with realistic foregrounds**: Discusses foreground challenges but does not quantify foreground residuals after removal or their impact on parameter inference.

5. **Line-of-sight structure**: Treats power spectrum as a summary, but does not deeply discuss the additional information in higher-order statistics (bispectrum, trispectrum) or the non-Gaussian structure of ionized bubbles.

**Assumptions that may not hold:**

1. **Constant spin temperature**: Furlanetto assumes $T_\text{spin}$ is roughly constant across the field and redshift range of interest. In reality, $T_\text{spin}$ varies with:
   - Lyman-alpha intensity (which depends on nearby galaxies)
   - Neutral fraction (which changes across the EoR)
   - Density (which sets collisional coupling rate)
   This introduces coupling between $T_\text{spin}$ and ionization, complicating the EFT expansion.

2. **Linear polarization**: The derivation assumes linear Stokes parameters; in reality, polarization rotation and Faraday effects can complicate observations.

3. **Homogeneous foreground spectrum**: Real foregrounds have complex structure. The assumption of a power-law spectrum may not hold across the wide SKA frequency range.

## Pedagogical Value and Entry Point

**This book is the standard entry point for 21cm cosmology:**
- Furlanetto's chapter 9 is widely used as the reference for "what is the 21cm signal?"
- Combined with [[Choudhury 2022 (Reionization Intro)]] (reionization physics) and [[Gnedin & Madau 2022 (Modeling Reionization)]] (simulation codes), this book completes the foundations

**Reading path**:
1. Start with Choudhury 2022 → understand reionization physics
2. Read Mesinger 2016 Ch. 9 (Furlanetto) → understand 21cm observables
3. Skim Mesinger Ch. 1–2, 4 → understand broader EoR context
4. Read Gnedin & Madau 2022 → understand how simulators model this

## Figures and Highlights

**Key figures from Furlanetto's chapter:**
- Hyperfine level diagram showing the 21cm transition
- Brightness temperature vs. neutral fraction (linear relationship)
- Power spectra during different stages of reionization (neutral, patchy, ionized)
- Foreground map at 150 MHz showing galactic and extragalactic sources
- Foreground wedge diagram in $(k_\perp, k_\parallel)$ space

**Figures from other chapters** of value:
- Ch. 1 (Haiman): First galaxies and halo population at high-$z$
- Ch. 4 (Bouwens): High-$z$ UV luminosity function showing sources of ionizing photons
- Ch. 8 (Reichardt): CMB polarization constraints on reionization history

## Open Questions After Reading

> [!gap]
> **Spin temperature variations**: Furlanetto assumes roughly constant $T_\text{spin}$, but real simulations show $T_\text{spin}$ varies spatially and with redshift. How much does this coupling complicate the EFT expansion? Does the linear relationship $\delta T_b \propto x_\text{HI}$ break down?

> [!gap]
> **Information beyond the power spectrum**: The book focuses on power spectrum as the primary observable. But bispectrum and trispectrum contain information on bubble topology and morphology. Are these captured in the EFT bias expansion, or do they require additional effective operators?

> [!gap]
> **Foreground removal impact**: Real SKA observations will have foreground residuals. How much does imperfect foreground removal degrade constraints on ionization parameters? And how sensitive are EFT coefficients to foreground contamination?

> [!gap]
> **Resolution dependence of 21cm power spectrum**: Different simulators (21cmFAST vs. SCRIPT vs. full RT) may produce different small-scale 21cm power spectra due to different resolutions and Jeans smoothing. Does this affect EFT bias measurements in P1?

> [!gap]
> **21cm cross-correlations**: The chapter doesn't discuss cross-correlations with galaxy surveys (now a key part of future SKA science, as in [[Pietschke et al 2026 (cross-correlation)]]). What does the 21cm × galaxy cross-power spectrum probe that 21cm auto-power alone does not?
