---
type: concept
title: "Bias Expansion"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/theory
  - domain/eft
status: developing
complexity: advanced
domain: "[[Effective Field Theory]]"
related:
  - "[[Effective Field Theory]]"
  - "[[Matter Overdensity Field]]"
  - "[[Renormalization]]"
  - "[[Simulator Dependence]]"
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Qin et al 2022 (EFT Redshift Space)]]"
sources:
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Qin et al 2022 (EFT Redshift Space)]]"
  - "[[Baradaran et al 2024 (Hybrid EFT)]]"
---

# Bias Expansion

## What is the Bias Expansion?

The bias expansion is the central mathematical framework of this thesis. It provides a systematic, operator-basis approach to modeling how the ionization field $x_\mathrm{HII}$ depends on the underlying matter distribution across different reionization simulations. Instead of treating each simulator's approach to reionization as independent black boxes, the bias expansion reveals their common structure: all simulators follow the same operator basis, but differ only in the values of the **bias coefficients** at each redshift.

The key insight is that the ionization field fluctuations can be expanded as a perturbative series in the matter overdensity field $\delta_m$, similar to how galaxy formation bias works. This expansion is **simulator-independent**: the functional form is universal, but the coefficients encode the specific physics each code implements (ionization sources, radiative transfer, recombination rates, etc.).

## Mathematical Form

### Real Space Expansion

The ionization field fluctuations are expanded as:

$$\delta_x(\mathbf{x},z) = b_1^x \delta_m(\mathbf{x},z) + \frac{b_2^x}{2} \delta_m^2(\mathbf{x},z) + b_{\nabla^2}^x \nabla^2 \delta_m(\mathbf{x},z) + \varepsilon^x(\mathbf{x},z)$$

where:

- **$\delta_x(\mathbf{x},z)$** is the ionization field fluctuation around the mean neutral fraction $\bar{x}_\mathrm{HII}(z)$
- **$\delta_m(\mathbf{x},z)$** is the matter overdensity field
- **$b_1^x$** is the linear bias coefficient—the response of ionization to linear matter perturbations
- **$b_2^x$** is the quadratic (non-linear local) bias coefficient—captures the non-linear patchiness of the ionization field
- **$b_{\nabla^2}^x$** is the Laplacian bias coefficient—encodes the effective bubble scale and scale-dependent physics
- **$\varepsilon^x(\mathbf{x},z)$** is the stochastic term—unbiased noise irreducible at the EFT order

The expansion is truncated at second order in $\delta_m$ because higher-order terms scale as $\delta_m^3$, which are suppressed by small-scale physics and are not needed for the power spectrum regime where EFT is valid.

### Fourier Space Expansion

In Fourier space (with convention $\tilde{\delta}(\mathbf{k}) = \int \delta(\mathbf{x}) e^{-i\mathbf{k}\cdot\mathbf{x}} d^3x$), the expansion becomes:

$$\tilde{\delta}_x(\mathbf{k},z) = b_1^x \tilde{\delta}_m(\mathbf{k},z) + \frac{b_2^x}{2} \int \frac{d^3q}{(2\pi)^3} \tilde{\delta}_m(\mathbf{q}) \tilde{\delta}_m(\mathbf{k}-\mathbf{q}) + b_{\nabla^2}^x (-k^2) \tilde{\delta}_m(\mathbf{k},z) + \tilde{\varepsilon}^x(\mathbf{k},z)$$

The quadratic term involves a convolution integral, which upon simplification in perturbation theory becomes related to the second-order gravitational coupling kernel $F_2(\mathbf{q}, \mathbf{k}-\mathbf{q})$.

## Physical Interpretation of Each Term

### Linear Bias: $b_1^x$

The linear bias coefficient measures how directly the ionization field responds to the linear matter density field. Its physical origin is:

$$b_1^x \approx \bar{x}_\mathrm{HI} - \bar{x}_\mathrm{HII} \cdot b_{\mathrm{S},1}$$

where $\bar{x}_\mathrm{HI}$ and $\bar{x}_\mathrm{HII}$ are the mean neutral and ionized fractions, and $b_{\mathrm{S},1}$ is the **source linear bias**. This relation shows that $b_1^x$ depends on the source distribution (which depends on the matter density field) and the local balance between ionization rate and recombination. In regions of higher source density (positive $\delta_m$), ionization proceeds faster, creating negative ionization field fluctuations (more ionized). Hence, $b_1^x$ is typically negative during the epoch of reionization.

The sign and magnitude of $b_1^x$ varies with redshift as the ionization front propagates outward, making it a key diagnostic of reionization morphology.

### Quadratic Bias: $b_2^x$

The quadratic bias coefficient captures **non-linear, local** feedback effects. While the linear term assumes ionization responds uniformly to matter density, in reality the ionization field exhibits patchy, non-linear behavior. Regions of very high density ionize first (because of enhanced source density); regions of very low density remain neutral longer. The quadratic term parameterizes this:

$$\frac{b_2^x}{2} \delta_m^2$$

This term is always positive (proportional to $\delta_m^2$) and grows rapidly in overdense regions. It reduces the local ionization fraction beyond what the linear term alone predicts. The coefficient $b_2^x$ is thus typically negative: it describes a suppression of ionization in very overdense regions due to physical feedback (e.g., lower gas density suppresses recombination, but enhanced ionization sources in overdense regions compete with this).

Without renormalization (discussed below), $b_2^x$ depends on the small-scale UV cutoff of the matter field—a serious problem for simulator comparison.

### Laplacian Bias: $b_{\nabla^2}^x$

The Laplacian bias couples the ionization field to the Laplacian of the matter density field, i.e., the second spatial derivative:

$$b_{\nabla^2}^x \nabla^2 \delta_m$$

In Fourier space, $\nabla^2 \leftrightarrow -k^2$, so this term becomes $-b_{\nabla^2}^x k^2 \delta_m(k)$. It encodes **scale-dependent physics**: ionization does not respond instantaneously to all scales of matter perturbations. The response is suppressed on scales smaller than the typical ionization bubble radius $R_\mathrm{eff}$.

The physical scaling is:

$$b_{\nabla^2}^x \approx -\frac{R_\mathrm{eff}^2}{3}$$

where the factor $1/3$ comes from relating the Laplacian to the mean-square curvature. As bubbles grow during reionization, $R_\mathrm{eff}$ increases, so $b_{\nabla^2}^x$ becomes more negative. This term is essential for matching the small-scale power suppression observed in all reionization codes.

### Stochastic Term: $\varepsilon^x(\mathbf{x},z)$

The stochastic noise term represents all physics that cannot be described as a local, deterministic function of the matter field. Sources include:

- **Stochastic source formation**: the exact positions and properties of ionization sources are not perfectly correlated with the matter field
- **Radiative transfer details**: photon transport, scattering, and the finite speed of light create memory effects and non-local dependencies
- **Recombination fluctuations**: local temperature and density variations affect recombination rates non-trivially
- **Simulation-specific implementations**: different codes use different recipes for these processes

The key property is that $\varepsilon^x$ is **unbiased**: $\langle \varepsilon^x \rangle = 0$ and $\langle \varepsilon^x \delta_m \rangle = 0$. Its power spectrum is the **stochastic power** $P_{\varepsilon\varepsilon}(k,z)$, which is the most novel cross-simulator diagnostic in this thesis.

## Power Spectrum

The power spectrum of the ionization field follows from the bias expansion:

$$P_{xx}(k,z) = (b_1^x)^2 P_{mm}(k,z) + 2 b_1^x b_2^x P_{m\delta^2}(k,z) + (b_2^x)^2 P_{\delta^2\delta^2}(k,z) + 2 b_1^x b_{\nabla^2}^x (-k^2) P_{mm}(k,z) + \ldots + P_{\varepsilon\varepsilon}(k,z)$$

where:

- $P_{mm}(k,z)$ is the matter power spectrum from linear perturbation theory
- $P_{m\delta^2}(k,z)$ is the cross-power between the linear and quadratic matter fields, computed via second-order perturbation theory
- $P_{\delta^2\delta^2}(k,z)$ is the power in the squared matter field
- The Laplacian term includes the $k^2$ factor, giving $-k^2 P_{mm}(k,z)$ (scale-dependent suppression)
- All cross-terms between operators are included consistently

The beauty of this formula is that **all dependence on the specific simulator physics is encoded in the coefficients** $b_1^x(k,z)$, $b_2^x(z)$, and $b_{\nabla^2}^x(z)$ and the stochastic power $P_{\varepsilon\varepsilon}(k,z)$. The perturbation theory contributions ($P_{mm}$, $P_{m\delta^2}$, etc.) are universal and can be computed from any linear Boltzmann code.

## Measuring Bias Coefficients

The bias coefficients are measured via cross-correlation with the matter field. From the expansion:

$$\langle \delta_x(\mathbf{k}) \delta_m(-\mathbf{k}) \rangle = b_1^x P_{mm}(k) + b_2^x \langle \delta_m^2(\mathbf{k}) \delta_m(-\mathbf{k}) \rangle + \ldots$$

The linear bias $b_1^x$ is extracted as:

$$b_1^x(k,z) = \frac{P_{x,m}(k,z)}{P_{mm}(k,z)}$$

where $P_{x,m}$ is the cross-power spectrum between the ionization and matter fields. This is clean because the matter-matter cross-term dominates at low $k$.

Higher-order coefficients are extracted by fitting the full spectrum shape or by constructing appropriate power combinations that isolate each operator.

## Regime of Validity

The bias expansion is valid in the **linear and mildly non-linear regime** where:

$$P_\mathrm{err}(k) / P_{xx}(k) \lesssim 10\%$$

This defines a wavenumber range:

- **McQuinn & D'Aloisio (2018)**: EFT valid for $k \lesssim 0.2-0.5 \, h/\mathrm{Mpc}$ depending on reionization state
- **Qin et al. (2022)** with renormalization: extended to $k \lesssim 0.8 \, h/\mathrm{Mpc}$

The breakdown occurs when bubble-scale physics becomes non-perturbative, i.e., when $k \sim R_\mathrm{eff}^{-1}$ or $k \sim R_\mathrm{mfp}^{-1}$ (mean free path scale). At these scales, the local operator basis fails because ionization depends non-locally on the matter field—photons scatter over many mean free paths before being absorbed.

## Simulator Independence and the Central Thesis Claim

The **key novelty** of this thesis is the recognition that the bias expansion operator basis is simulator-independent. Different codes (21cmFAST, SCRIPT, THESAN, etc.) produce different ionization fields because they implement reionization physics differently. However, the differences manifest purely in the redshift-dependent bias coefficients $b_1^x(z)$, $b_2^x(z)$, $b_{\nabla^2}^x(z)$, and stochastic power $P_{\varepsilon\varepsilon}(k,z)$—not in the operator basis itself.

This insight enables **cross-simulator generalization**: if we fit an EFT model to one simulator and measure its bias coefficients, we can, with appropriate renormalization and extrapolation, predict the power spectrum in another simulator. This is only possible because the operator basis is universal.

## Connections to the Thesis

- **[[Effective Field Theory]]**: The bias expansion is the application of EFT methodology to the ionization field
- **[[Matter Overdensity Field]]**: $\delta_m$ is the fundamental input field; its perturbation theory decomposition $\delta^{(1)}, \delta^{(2)}$ appears in the expansion
- **[[Renormalization]]**: The renormalized quadratic operator ensures $b_2^x$ is well-defined and simulator-independent
- **[[Power Spectrum Error]]**: The error $P_\mathrm{err}$ defines where the bias expansion breaks down
- **[[Simulator Dependence]]**: The coefficients are simulator-dependent; understanding this variation is key to generalization
- **[[McQuinn & D'Aloisio 2018]]**: Pioneering work establishing the validity regime
- **[[Qin et al 2022 (EFT Redshift Space)]]**: Extended validation with renormalization

## Summary

The bias expansion provides a universal parameterization of the ionization field in terms of local operators acting on the matter density field. Its success lies in encapsulating all simulator-specific physics into a small set of coefficients, allowing different codes to be compared and generalized using the same mathematical language.
