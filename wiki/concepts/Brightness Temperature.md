---
type: concept
title: "Brightness Temperature"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/observation
  - domain/21cm
status: developing
complexity: advanced
domain: "[[21cm Cosmology]]"
related:
  - "[[21cm Cosmology]]"
  - "[[Neutral Fraction]]"
  - "[[Spin Temperature]]"
  - "[[Redshift Space Distortions]]"
  - "[[Matter Overdensity Field]]"
  - "[[Brightness Temperature Fluctuations]]"
sources:
  - "[[Zaldarriaga, Kovetz, Silk 2018]]"
  - "[[Beardsley et al 2016]]"
  - "[[Pober et al 2014]]"
---

# Brightness Temperature

## What is 21cm Brightness Temperature?

The brightness temperature $\delta T_b$ quantifies the differential brightness temperature of the cosmic 21cm line—the hyperfine transition of neutral hydrogen. This observable is the primary signature used to probe the Epoch of Reionization (EoR) and the structure of the ionization field across cosmic time. Unlike galaxy surveys or lensing observations, 21cm observations directly measure the spatial distribution of neutral gas through its characteristic radio emission/absorption.

The brightness temperature is not a true thermodynamic temperature, but rather an intensity measurement converted to temperature units. When neutral hydrogen undergoes the hyperfine transition (spin flip of the electron in the hydrogen atom), it emits (or absorbs) photons at a rest wavelength of 21 centimeters ($\nu = 1420$ MHz). The intensity of this line encodes information about the amount of neutral gas and the physical conditions (velocity, density, temperature) in the intergalactic medium.

During reionization, as ionization sources create expanding bubbles of ionized gas, the neutral hydrogen fraction decreases spatially and in time. These spatial variations create measurable fluctuations in the 21cm brightness temperature that carry direct information about the ionization morphology and its correlation with matter density.

## Mathematical Form: The Full Expression

The differential 21cm brightness temperature is given by:

$$\delta T_b(\mathbf{x},z) = 27 \, x_\mathrm{HI}(1 + \delta_m) \left(1 - \frac{T_\mathrm{CMB}}{T_S}\right) \frac{H(z)}{dv_r/dr + H(z)} \sqrt{\frac{1+z}{10} \frac{0.15}{\Omega_m h^2}} \frac{\Omega_b h^2}{0.023} \, \mathrm{mK}$$

This formula is dense with physical content. Let us break down each factor:

### Overall Coefficient: 27 mK

The prefactor 27 mK sets the scale. It encodes the fundamental atomic physics: the intensity of the 21cm line depends on the Einstein A coefficient for the hyperfine transition and basic radiative transfer. All terms in the formula are dimensionless, so the 27 mK sets the absolute brightness temperature scale.

### Neutral Fraction: $x_\mathrm{HI}(z)$

The neutral fraction is the crucial reionization variable. It represents the fraction of hydrogen remaining in neutral atomic state:

$$x_\mathrm{HI}(z) = \frac{\langle n_\mathrm{HI} \rangle}{\langle n_H \rangle}$$

During the EoR, $x_\mathrm{HI}$ decreases from $\sim 1$ (fully neutral at $z \sim 30-50$) to $\sim 0.001$ (fully ionized at $z \sim 6$). The 21cm signal is directly proportional to this quantity: where neutral hydrogen remains, the signal is bright; where ionization has proceeded, it vanishes. This proportionality is the power of 21cm cosmology—it provides a direct probe of ionization.

### Matter Overdensity: $(1 + \delta_m)$

The density factor $(1 + \delta_m)$ accounts for two effects:

1. **Higher neutral hydrogen density in overdense regions**: Overdense regions contain more hydrogen atoms, producing a stronger 21cm signal (absent ionization). 
2. **Number density perturbations**: Cosmological density fluctuations enhance or suppress the local hydrogen density and thus the observed brightness temperature.

In the linear regime, $\delta_m \ll 1$, so this factor is approximately unity plus small perturbations. In highly overdense regions (galaxy clusters, cosmic filaments), $\delta_m$ can reach order unity or higher.

### Spin Temperature Factor: $\left(1 - \frac{T_\mathrm{CMB}}{T_S}\right)$

This factor determines whether the 21cm line is in **absorption** or **emission**:

$$\left(1 - \frac{T_\mathrm{CMB}}{T_S}\right) = \begin{cases}
\text{positive} & \text{if } T_S > T_\mathrm{CMB} \quad \text{(emission)} \\
\text{negative} & \text{if } T_S < T_\mathrm{CMB} \quad \text{(absorption)} \\
\text{zero} & \text{if } T_S = T_\mathrm{CMB} \quad \text{(no signal)}
\end{cases}$$

The **spin temperature** $T_S$ is the effective temperature of the hyperfine level population. During the EoR:

- **Before reionization begins** ($z \gtrsim 20$): $T_S \gg T_\mathrm{CMB}$ (collisions dominate, decoupling from CMB), yielding emission
- **During early reionization** ($z \sim 15-20$): $T_S$ increases further due to Lyman-alpha coupling, producing strong emission
- **Late in reionization** ($z \sim 6-10$): $T_S$ may remain high, but neutral fraction drops sharply, suppressing the overall signal
- **After reionization** ($z < 6$): Very few neutral atoms remain, so $T_S$ is irrelevant

The quantity $T_\mathrm{CMB} \approx 2.73 \, (1+z)$ K is the CMB temperature at redshift $z$.

### Velocity Gradient Term: $\frac{H(z)}{dv_r/dr + H(z)}$

This term encodes **redshift-space distortions (RSD)** and the Doppler effect. The Hubble expansion causes all distant objects to recede, but peculiar velocities due to gravitational inhomogeneities create additional Doppler shifts. The term arises from transforming the frequency space to redshift space:

$$\frac{dz}{dr} = H(z) + \frac{1}{a} \frac{dv_r}{dr}$$

where $H(z) = \dot{a}/a$ is the Hubble expansion rate and $dv_r/dr$ is the peculiar velocity gradient (rate of change of radial velocity with distance). The factor $\frac{H(z)}{dv_r/dr + H(z)}$ corrects the observed signal for these velocity effects.

In regions of strong convergence (infall toward overdensities), $dv_r/dr$ is negative and large, suppressing this factor. In regions of divergence (outflow from voids), $dv_r/dr$ is positive, enhancing it. This effect creates the characteristic **RSD pattern** in 21cm maps: enhanced power along lines of sight aligned with velocity gradients.

### Cosmological Scaling: $\sqrt{\frac{1+z}{10} \frac{0.15}{\Omega_m h^2}}$

This term scales the brightness temperature with redshift and cosmological parameters. It reflects how the physical density of hydrogen and the cosmic expansion change with $z$ and the matter density fraction $\Omega_m$. The specific values ($1+z$ vs. 10, 0.15 vs. $\Omega_m h^2$) are calibrated to standard cosmologies.

### Baryon Density: $\frac{\Omega_b h^2}{0.023}$

The baryon fraction $\Omega_b h^2$ sets the abundance of hydrogen in the universe. The coefficient 0.023 is a reference value (approximately the current Planck value). This factor accounts for the fact that 21cm brightness depends on total hydrogen abundance.

## Saturated Spin Temperature Limit

In the regime where the spin temperature is much larger than the CMB temperature ($T_S \gg T_\mathrm{CMB}$), which holds during most of the EoR, the factor simplifies:

$$\left(1 - \frac{T_\mathrm{CMB}}{T_S}\right) \approx 1$$

In this **saturated limit**, the brightness temperature formula simplifies to:

$$\delta T_b \propto x_\mathrm{HI} \left[1 + \delta_m - \frac{\partial_\parallel v_\parallel}{aH}\right]$$

This is the form most commonly used in EFT analyses. Here:

- **$x_\mathrm{HI}$**: the neutral fraction (reionization variable)
- **$(1 + \delta_m)$**: density fluctuations
- **$-\frac{\partial_\parallel v_\parallel}{aH}$**: the RSD term (velocity divergence along the line of sight)

The velocity term comes from expanding $\frac{H}{dv_r/dr + H} \approx 1 - \frac{dv_r/dr}{H} = 1 - \frac{\partial_\parallel v_\parallel}{aH}$ to first order.

## Physical Interpretation

The brightness temperature equation reveals how the 21cm signal depends on three fundamental processes:

1. **Reionization morphology** ($x_\mathrm{HI}$): Direct tracer of ionization fraction and bubble structure
2. **Matter clustering** ($\delta_m$): Gravity causes matter to cluster; overdense regions have more hydrogen
3. **Peculiar velocities** ($\partial_\parallel v_\parallel$): Infall and outflow patterns imprinted by gravitational structure growth

This combination makes 21cm a powerful probe: it simultaneously constrains the ionization history, the matter power spectrum, and the growth of structure.

## During Reionization: Key Regimes

### Fully Neutral Universe ($z > 20$, $x_\mathrm{HI} \approx 1$)
The signal is bright and reflects primarily matter clustering: $\delta T_b \approx (1 + \delta_m)$. This is the regime farthest from observations but accessible theoretically.

### During Reionization ($15 \lesssim z \lesssim 8$, $0 < x_\mathrm{HI} < 1$)
The signal shows strong fluctuations because $x_\mathrm{HI}$ varies spatially on bubble scales $\sim 10-100$ Mpc. The ionization morphology is imprinted directly on the brightness temperature map. This is the regime EFT targets.

### Fully Ionized Universe ($z < 6$, $x_\mathrm{HI} \approx 0$)
The 21cm signal vanishes because almost no neutral hydrogen remains. However, a small residual signal from neutral gas in dense structures (halos, galaxies) may persist. This regime is not directly observed at 21cm.

## Observational Signatures and Challenges

21cm brightness temperature fluctuations are extremely faint—typical fluctuations are $\mathcal{O}(10)$ mK against foreground contamination at the Kelvin level. Major observational challenges include:

- **Foreground removal**: Synchrotron and free-free foregrounds from galactic and extragalactic sources are $\sim 10^3$ K, requiring exquisite angular resolution and frequency discrimination
- **Thermal noise**: Radio telescopes have limited sensitivity; survey speed trades against depth
- **Polarization and systematics**: Instrumental effects introduce systematic errors that can mimic cosmological signals
- **Redshift degeneracy**: 21cm observations measure frequency; converting to redshift requires precise knowledge of the ionization history

Despite these challenges, next-generation telescopes (HERA, SKA) aim to detect and map these fluctuations, enabling unprecedented tests of reionization models.

## Connection to Bias Expansion

The brightness temperature fluctuations can be understood through the [[Bias Expansion]] framework. When the spin temperature is saturated, the signal becomes:

$$\delta T_b \propto x_\mathrm{HI} \left[1 + \delta_m - \frac{\partial_\parallel v_\parallel}{aH}\right]$$

The neutral fraction $x_\mathrm{HI}$ itself can be expanded:

$$\delta x_\mathrm{HI} = b_1^x \delta_m + \frac{b_2^x}{2} \delta_m^2 + b_{\nabla^2}^x \nabla^2 \delta_m + \varepsilon^x$$

Substituting this into the brightness temperature formula shows how the ionization bias manifests in 21cm observations. The term $x_\mathrm{HI} \delta_m$ generates a product of biased fields, creating a non-trivial power spectrum with cross-terms between different bias operators.

## Connections to Related Concepts

- **[[Spin Temperature]]**: Determines whether the signal is absorption or emission
- **[[Neutral Fraction]]**: The direct tracer of reionization progress; $x_\mathrm{HI}$ is the primary EoR variable
- **[[21cm Cosmology]]**: The broader field of using 21cm observations to study cosmology
- **[[Redshift Space Distortions]]**: The velocity term creates anisotropic power in the observed field
- **[[Matter Overdensity Field]]**: Density fluctuations modulate the brightness temperature
- **[[Bias Expansion]]**: The ionization field bias carries through to the brightness temperature power spectrum

## Summary

The 21cm brightness temperature is a powerful, direct probe of the ionization field during reionization. Its formula encodes information about neutral fraction, matter density, and peculiar velocities in a single observable. The saturated spin temperature limit simplifies the expression and reveals the underlying physics: how ionization, density, and velocity combine to produce the observed signal. Understanding brightness temperature fluctuations and their connection to the ionization field bias is central to extracting cosmological constraints from 21cm observations of the EoR.
