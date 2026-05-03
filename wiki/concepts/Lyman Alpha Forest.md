---
type: concept
title: "Lyman Alpha Forest"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/observable
  - domain/reionization
status: seed
domain: "[[Reionization Physics]]"
aliases:
  - "Ly-alpha forest"
  - "Lyman-alpha forest"
  - "GP trough"
  - "Gunn-Peterson trough"
related:
  - "[[Neutral Fraction]]"
  - "[[Ferrara & Pandolfi (IGM Reionization)]]"
  - "[[Mean Free Path]]"
sources:
  - "[[Ferrara & Pandolfi (IGM Reionization)]]"
  - "[[Choudhury 2022 (Reionization Intro)]]"
---

# Lyman Alpha Forest

## What It Is

The Lyman-alpha forest is the series of absorption features blueward of the Ly$\alpha$ emission line in quasar spectra, caused by neutral hydrogen along the line of sight at various redshifts. Each absorption system corresponds to a patch of neutral gas at a different redshift. The observable quantity is the **transmitted flux fraction**, which encodes information about the neutral hydrogen column density and the ionization state of the intergalactic medium (IGM).

The mean transmitted flux fraction is:
$$
\langle F \rangle = \langle e^{-\tau_\alpha} \rangle = e^{-\tau_\text{eff}}
$$
where $\tau_\text{eff}$ is the effective Ly$\alpha$ optical depth, which encodes the mean neutral fraction. When $\tau_\text{eff}$ is large, the flux is heavily suppressed; when small, the forest is transparent.

## Radiative Transfer of Lyman-Alpha Photons

### The Lyman-Alpha Absorption Cross-Section

The Lyman-alpha line arises from the hydrogen transition $2P \leftrightarrow 1S$. The absorption cross-section has a characteristic shape called the **Voigt profile**, which results from two competing broadening mechanisms:

$$\sigma_\alpha(\nu) = \frac{3\lambda_\alpha^2}{8\pi} A_\alpha \cdot \phi(\nu)$$

where $A_\alpha \approx 6.27 \times 10^8$ s$^{-1}$ is the Einstein A coefficient for spontaneous emission, $\lambda_\alpha \approx 121.6$ nm is the rest wavelength, and $\phi(\nu)$ is the normalized Voigt profile.

### Voigt Profile: Natural + Doppler Broadening

The Voigt profile is the convolution of two broadening mechanisms:

1. **Natural broadening (Lorentzian core):** Arises from the finite lifetime of the excited state. The natural linewidth is $\Delta\nu_\text{nat} = A_\alpha / (4\pi) \approx 100$ MHz, corresponding to a frequency width of $\Delta\nu_\text{nat} / c \approx 10^{-4}$ of the line center. This produces a Lorentzian wing with $\phi(\nu) \propto 1/[(\nu - \nu_0)^2 + (\Delta\nu_\text{nat}/2)^2]$ far from line center.

2. **Thermal (Doppler) broadening (Gaussian wings):** Arises from the thermal motion of hydrogen atoms. The Doppler width is $\Delta\nu_D = \nu_0 \sqrt{k_B T / m_H c^2}$. At $T \sim 10^4$ K (typical IGM temperature), $\Delta\nu_D \approx 100$ GHz. Atoms moving toward the observer are blue-shifted; those moving away are red-shifted. This produces a Gaussian envelope $\phi(\nu) \propto \exp(-[(\nu - \nu_0) / \Delta\nu_D]^2)$.

The **Voigt profile** $\phi(\nu)$ is their convolution:
$$\phi(\nu) = \frac{a}{\pi^{3/2}\Delta\nu_D} \int_{-\infty}^{\infty} \frac{\exp(-y^2)}{(\nu - \nu_0 - y\Delta\nu_D)^2 + (a\Delta\nu_D)^2} dy$$

where $a = \Delta\nu_\text{nat} / (4\pi\Delta\nu_D)$ is the damping parameter. For Ly-$\alpha$, $a \approx 10^{-3}$ at typical IGM temperatures, so the **Lorentzian core dominates at line center** (where the optical depth is highest) and the Gaussian wings dominate far from line center.

The characteristic Voigt profile shape — a sharp core surrounded by slowly-decaying wings — means that:
- The **line core is extremely optically thick**: $\tau_0 = \sigma_0 n_\text{HI} L \sim 10^3$–$10^5$ even for modest neutral fractions
- The **line wings are optically thin**: absorption at frequencies far from line center requires either very high column densities or damping wing effects
- **Temperature variations affect the line shape**: hotter gas has broader Gaussian wings, cooler gas has sharper cores

### Why the Line Center Is So Optically Thick

At the line center ($\nu = \nu_0$), the cross-section reaches its maximum:
$$\sigma_0 = \frac{3\lambda_\alpha^2}{8\pi} A_\alpha \frac{1}{\sqrt{\pi}\Delta\nu_D} \approx 10^{-17} \text{ cm}^2$$

For a neutral fraction of $x_\text{HI} \sim 10^{-3}$ (99.9% ionized) and a typical column density of $N_\text{HI} \sim 10^{20}$ cm$^{-2}$, the optical depth at line center is:
$$\tau(\nu_0) = \sigma_0 N_\text{HI} \sim 10^3$$

This explains why the Lyman-alpha forest is so efficient at suppressing flux, even in mostly ionized regions. **A universe with mean neutral fraction $\bar{x}_\text{HI} \sim 10^{-3}$ and $\bar{x}_\text{HI} \sim 10^{-4}$ are observationally indistinguishable** because both produce complete absorption (see the saturation discussion below).

## The Gunn-Peterson Effect and Historical Context

### The Gunn-Peterson Trough

For a uniform neutral IGM at redshift $z$, the Ly$\alpha$ optical depth integrated along the line of sight is:
$$\tau_\text{GP} = \int_0^z \frac{d\tau}{dz'} dz' \approx 10^5 \times \bar{x}_\text{HI} \times \left(\frac{1+z'}{10}\right)^3 \text{ (order of magnitude)}$$

This produces a **complete absorption trough blueward of the quasar Ly-$\alpha$ emission line**, with essentially zero transmitted flux. The trough extends from the Ly-$\alpha$ line to the Ly-$\beta$ line at higher frequency (shorter wavelength in the quasar rest frame), a feature called the **Gunn-Peterson trough** after Gunn & Peterson (1965), who predicted this effect as a signature of a neutral IGM.

### Discovery and Observational Milestones

- **Gunn & Peterson (1965)**: Theoretical prediction that a neutral IGM would produce a complete absorption trough blueward of quasar Ly-$\alpha$ lines, making it impossible to observe the forest at high redshift.
- **Becker et al. (2001) and Fan et al. (2002)**: Discovery of Gunn-Peterson troughs in SDSS quasar spectra at $z \gtrsim 6.1$, providing the **first direct evidence that reionization ended around $z \approx 6$**. This was a landmark observation that immediately became a cornerstone constraint on reionization.
- **Peebles (2019)**: Noted the significance of the Gunn-Peterson effect in the context of the 21 cm and CMB constraints; Jim Peebles won the 2019 Nobel Prize in Physics in part for theoretical work related to reionization physics.

The rapid transition in the Ly-$\alpha$ forest from being present at $z \lesssim 6$ to completely saturated at $z \gtrsim 6$ provides the primary observational evidence that reionization occurred at a specific epoch, rather than gradually over a wide redshift range.

## Critical Subtlety: Saturation

A key point ([[Ferrara & Pandolfi (IGM Reionization)]]):

> The GP trough saturates at $\bar{x}_\text{HI} \gtrsim 10^{-3}$. Even a mostly ionized universe ($\bar{x}_\text{HI} \sim 10^{-4}$–$10^{-3}$) produces complete absorption.

This saturation effect is crucial because it means **the Lyman-alpha forest cannot directly probe the bulk of reionization**. The transmitted flux drops by 2–3 orders of magnitude in only $\Delta z \approx 0.5$ at $z \sim 5.5$–$6$, but this does **not** require the mean neutral fraction to be close to unity at $z = 6$. Instead, it reflects the fact that even a small residual neutral fraction is sufficient to absorb all the Ly-$\alpha$ photons in the quasar spectrum.

More precisely, once $\bar{x}_\text{HI}$ drops below $\sim 10^{-3}$, the flux becomes essentially zero. For redshifts where $\bar{x}_\text{HI}} > 10^{-3}$, we cannot distinguish whether $\bar{x}_\text{HI}} = 0.1$ or $\bar{x}_\text{HI}} = 1$ — both look the same observationally. This limitation is why the Lyman-alpha forest **probes the endpoint of reionization**, not its duration or internal structure.

## Flux Decrement and Redshift Evolution

The mean flux decrement is defined as:
$$D_A = \langle 1 - F \rangle = 1 - e^{-\tau_\text{eff}}$$

Observations of the Lyman-alpha forest at lower redshifts ($z \lesssim 5$) show a power-law redshift evolution:
$$\tau_\text{eff}(z) \propto (1+z)^{\gamma+1}$$

where $\gamma$ is the exponent. In the low-redshift ($z < 5.5$) regime where ionization is nearly complete, this power law is well-measured and stable with $\gamma \approx 1$–$2$. However, the power law must be **extrapolated** to higher redshifts where reionization is happening.

### The Saturated Effective Optical Depth Formula

A phenomenological fit to observations gives:
$$\tau_\text{eff}(z) \approx A \times \left(\frac{1+z}{4}\right)^\gamma$$

with fitted parameters $A \approx 0.0025$ and $\gamma \approx 3.5$ for $z < 5.5$. However, **above $z \sim 5.5$, the power law steepens dramatically** ($\gamma$ increases significantly), signaling the transition into the reionization epoch where the mean ionization state is changing rapidly.

## Patchy Opacity and Late-Ending Reionization

### Observational Evidence for Patchiness

A key observation at $z \gtrsim 5.5$ is the **patchy nature of the Gunn-Peterson trough**: different sight lines through the same redshift shell show vastly different optical depths, with some sightlines nearly transparent and others completely opaque. This is direct, line-of-sight evidence for **spatial fluctuations in the ionization fraction** $x_\text{HI}(\mathbf{x}, z)$ on scales of order 100 Mpc or larger.

The patchy trough features consist of:
- **Opacity troughs**: Regions of neutral gas extending 100+ Mpc in comoving distance, with optical depths $\tau_\text{eff} > 10$
- **Transmitted regions**: Islands where $\tau_\text{eff} < 1$, indicating lower neutral fractions
- **Alternating pattern**: A quasi-periodic alternation between opaque and transparent regions

### Becker et al. 2015 and the Discovery of Ionization Fluctuations

Becker et al. (2015) systematically studied the high-$z$ Lyman-alpha forest and reported clear evidence for **ionization fluctuations** at $z \sim 5.5$–$6$: the effective optical depth varies by factors of 2–3 between nearby sightlines, far more than expected from density fluctuations alone. This suggests that the ionization state of the IGM is patchy, not smooth.

The interpretation is that reionization is **not yet complete** at $z \sim 5.5$: different regions of the universe finish reionizing at slightly different times, creating spatial variations in $x_\text{HI}$. Some regions are fully ionized ($x_\text{HI} \sim 10^{-3}$, completely opaque in Ly-$\alpha$), while others retain residual neutral gas.

## The Quasar Proximity Effect

### Concept and Physical Origin

The **quasar proximity effect** is the observation that the Lyman-alpha forest is more transparent in the immediate vicinity of a bright quasar (typically within 5 Mpc of the quasar in the line-of-sight direction) than at larger distances. The interpretation is that the quasar's intense UV radiation field ionizes the gas near the quasar, reducing $x_\text{HI}$ locally and thus reducing the optical depth.

The proximity effect provides a **direct probe of the photoionization rate** $\Gamma_\text{HI}$ near the quasar:
$$\Gamma_\text{HI}(\mathbf{r}) \propto L_\text{quasar} / r^2 \times e^{-\tau(\nu, r)}$$

where $L_\text{quasar}$ is the quasar's ionizing luminosity, $r$ is the distance, and $\tau(\nu, r)$ accounts for attenuation of the photons by intervening neutral gas.

### Using the Proximity Effect to Constrain $x_\text{HI}$

By measuring the extent of the proximity effect (i.e., the size of the ionized bubble around the quasar) and modeling the UV radiation field, one can estimate the **mean neutral fraction near the quasar** at that redshift. This is one of the few methods that can probe $x_\text{HI}$ at $z > 6$ where the forest itself is saturated. However, the proximity effect depends sensitively on uncertain quasar properties (lifetime, spectral hardness, duty cycle), so the constraints are indirect.

## Relationship Between $\tau_\text{eff}$ and Photoionization Rate

A fundamental relationship connects the effective optical depth to the physical ionization balance:

$$\tau_\text{eff} \propto \frac{n_\text{HI}}{\Gamma_\text{HI}}$$

This comes from the equation of ionization equilibrium: at a given location, the ionization rate $\Gamma_\text{HI} n_\text{HI}$ balances the recombination rate $\alpha n_e n_p$. Rearranging, $n_\text{HI} \propto \Gamma_\text{HI}^{-1}$ (approximately, ignoring density and temperature variations).

**Crucial implication**: Spatial variation in $\tau_\text{eff}$ does **not** necessarily imply variation in $x_\text{HI}$ if the ionizing background $\Gamma_\text{HI}$ is also spatially varying. The patchy Gunn-Peterson trough at $z \sim 5.5$ could result from:
1. Patchy ionization ($x_\text{HI}$ varies while $\Gamma_\text{HI}$ is uniform)
2. Patchy ionizing background ($\Gamma_\text{HI}$ varies while $x_\text{HI}$ is uniform)
3. Some combination of both

This degeneracy is one reason why 21 cm observations (which probe $x_\text{HI}$ more directly via the brightness temperature $\Delta T_b \propto x_\text{HI}$) are complementary to the Lyman-alpha forest.

## Contrasting Epochs: $z < 5$ vs. $z > 5.5$

The Lyman-alpha forest behaves very differently in two regimes:

### $z \lesssim 5$: Ionization Complete, Useful for Cosmology

In this regime, $\bar{x}_\text{HI}} \lesssim 10^{-3}$ and ionization is essentially complete. The Lyman-alpha forest is **not saturated**, meaning flux variations reflect density fluctuations $\delta(\mathbf{x}, z)$ and temperature structure. This regime is scientifically valuable for:
- **Baryon acoustic oscillations (BAO)**: The forest traces the matter power spectrum at small scales ($k \sim 0.1$–$1$ Mpc$^{-1}$), allowing BAO measurements complementary to galaxy surveys
- **Matter power spectrum**: The 1D power spectrum from the Lyman-alpha forest constrains $P(k, z)$ at high redshift
- **Intergalactic medium properties**: Ionization fraction is so small that local ionization balance determines $T(z)$ and $x_\text{HI}(z)$ from first principles

### $z \gtrsim 5.5$: Reionization in Progress, Saturation Dominates

In this regime, the forest is saturated or partially saturated. The transmitted flux is so small that it only weakly constrains $\bar{x}_\text{HI}}$. The forest is **not useful for BAO or power spectrum cosmology** because saturation destroys the information. However, it is scientifically valuable as a **boundary condition on reionization**: the sharp transition in the forest from $z \approx 6$ to $z \approx 5.5$ sets a strict upper limit on when reionization ended.

## Relevance to This Thesis

- The Lyman-alpha forest is the **primary external observational constraint** on $\bar{x}_\text{HI}}(z)$ at $z \lesssim 6$. Any model of reionization must reproduce the observed forest optical depth evolution and patchiness.

- The **patchiness seen in the Gunn-Peterson trough** at $z \sim 5.5$–$6$ reflects spatial fluctuations in ionization on ~100 Mpc scales. This is qualitatively what the [[21 cm Power Spectrum]] will characterize quantitatively at $z > 6$, but with much higher redshift and spatial resolution.

- The forest is **not a useful constraint during the bulk of reionization** ($z \gtrsim 6$) due to saturation — even a neutral fraction of $x_\text{HI}} \sim 10^{-4}$ looks the same as $x_\text{HI}} \sim 1$ observationally. This saturation is precisely why 21 cm observations are essential: they probe $x_\text{HI}}$ directly via the brightness temperature, with sensitivity across the full range $0 < x_\text{HI}} < 1$.

- The effective optical depth $\tau_\text{eff}(z)$ is measurable and well-defined for $z < 6$, providing a [[Neutral Fraction]] constraint that the EFT model (via [[Semi-Numerical Reionization]] and [[Simulation-Based Inference]]) must match.

- The [[Zaroubi 2013]] chapter in [[papers/The Epoch of Reionization]] covers the connection between Lyman-alpha forest observations and 21 cm measurements in the reionization context.
