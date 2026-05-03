---
type: concept
title: "Matter Overdensity Field"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/theory
  - domain/cosmology
status: developing
complexity: advanced
domain: "[[Cosmological Perturbation Theory]]"
related:
  - "[[Bias Expansion]]"
  - "[[Renormalization]]"
  - "[[Linear Growth Factor]]"
  - "[[Effective Field Theory]]"
  - "[[Perturbation Theory]]"
  - "[[Power Spectrum]]"
sources:
  - "[[Dodelson 2003 (Modern Cosmology)]]"
  - "[[Bernardeau et al 2002 (Large-scale Structure)]]"
  - "[[Baldauf et al 2012 (Renormalization in SPT)]]"
---

# Matter Overdensity Field

## What is the Matter Overdensity Field?

The matter overdensity field $\delta_m(\mathbf{x},z)$ quantifies how the local mass density at position $\mathbf{x}$ and redshift $z$ deviates from the cosmic mean density. It is the fundamental variable in cosmological perturbation theory and the primary driver of all structure growth in the universe via gravity. In the context of this thesis, $\delta_m$ serves as the foundational input to the [[Bias Expansion]], determining how the ionization field responds to underlying matter clustering.

The overdensity field bridges microscopic physics (gas dynamics, ionization) with large-scale structure (gravitational evolution, power spectrum). Its distribution is well-understood from linear perturbation theory at large scales and can be accurately modeled via second-order perturbation theory at mildly non-linear scales. This makes it an ideal basis for the EFT expansion of the ionization field.

## Mathematical Definition

The matter overdensity field is defined as:

$$\delta_m(\mathbf{x},z) = \frac{\rho(\mathbf{x},z) - \bar{\rho}(z)}{\bar{\rho}(z)}$$

where:

- **$\rho(\mathbf{x},z)$** is the local matter density at position $\mathbf{x}$ and cosmic time $z$
- **$\bar{\rho}(z)$** is the cosmic mean density at redshift $z$, averaged over large scales

By definition, the mean overdensity vanishes: $\langle \delta_m \rangle = 0$. Negative overdensities ($\delta_m < 0$) indicate underdensities (voids); positive overdensities ($\delta_m > 0$) indicate overdensities (filaments, clusters).

### Fourier Space Convention

The Fourier transform of the overdensity field uses the convention:

$$\tilde{\delta}_m(\mathbf{k},z) = \int \delta_m(\mathbf{x},z) \, e^{-i\mathbf{k}\cdot\mathbf{x}} \, d^3x$$

The inverse transform is:

$$\delta_m(\mathbf{x},z) = \int \frac{d^3k}{(2\pi)^3} \tilde{\delta}_m(\mathbf{k},z) \, e^{i\mathbf{k}\cdot\mathbf{x}}$$

In Fourier space, perturbations at different wavenumbers are decoupled (in linear perturbation theory), making this representation natural for theoretical analysis.

## Growth via the Linear Growth Factor

The evolution of matter perturbations with redshift is governed by gravitational instability. In the linear regime ($|\delta_m| \ll 1$), the growth is described by the **linear growth factor** $D(z)$:

$$\delta_m(\mathbf{k},z) = D(z) \, \delta_m(\mathbf{k},z=0)$$

The growth factor $D(z)$ is normalized to unity at present day ($D(z=0) = 1$) and decreases monotonically into the past (as the universe becomes more matter-dominated). In a matter-dominated universe, $D(z) \propto (1+z)^{-1}$; in a $\Lambda$CDM universe, the evolution is more complex due to dark energy.

The growth factor satisfies the second-order ODE:

$$\ddot{D} + 2H\dot{D} - \frac{4\pi G \bar{\rho}}{a^3} D = 0$$

where dots denote derivatives with respect to cosmic time $t$.

### Growth Rate Parameter

The **growth rate** $f(z)$ characterizes how fast perturbations grow:

$$f(z) = \frac{d \ln D}{d \ln a} \approx \Omega_m(z)^{0.55}$$

where $\Omega_m(z)$ is the matter density fraction at redshift $z$. This parameter appears in redshift-space distortion calculations and is a key probe of gravity theories.

## Perturbation Theory Decomposition

In perturbation theory, the overdensity field is expanded as a power series in the **initial** (linear) fluctuations. This decomposition is essential for understanding non-linear effects:

$$\delta_m(\mathbf{k},z) = \delta_m^{(1)}(\mathbf{k},z) + \delta_m^{(2)}(\mathbf{k},z) + \delta_m^{(3)}(\mathbf{k},z) + \ldots$$

### Linear Density Field: $\delta_m^{(1)}$

The first-order (linear) field evolves simply according to the growth factor:

$$\delta_m^{(1)}(\mathbf{k},z) = D(z) \, \delta_m^{(1)}(\mathbf{k},z=0)$$

In real space, the linear field represents the smoothed density fluctuations in the absence of non-linear gravitational effects. It is Gaussian-distributed (if the initial conditions are Gaussian), with power spectrum:

$$P_{mm}^{(1)}(k,z) = D^2(z) \, P_{mm}^{(1)}(k,z=0)$$

### Second-Order Density Field: $\delta_m^{(2)}$

Gravitational instability causes matter to cluster non-linearly. Second-order perturbation theory (SPT) computes the leading non-linear corrections:

$$\delta_m^{(2)}(\mathbf{k},z) = \int \frac{d^3q}{(2\pi)^3} F_2(\mathbf{q}, \mathbf{k}-\mathbf{q}) \, \delta_m^{(1)}(\mathbf{q},z) \, \delta_m^{(1)}(\mathbf{k}-\mathbf{q},z)$$

The gravitational coupling kernel $F_2$ encodes how two Fourier modes of the linear field combine to produce non-linear power at wavenumber $\mathbf{k}$:

$$F_2(\mathbf{q}, \mathbf{p}) = \frac{5}{7} + \frac{1}{2}\frac{\mathbf{q} \cdot \mathbf{p}}{q p}\left(\frac{q}{p} + \frac{p}{q}\right) + \frac{2}{7}\left(\frac{\mathbf{q} \cdot \mathbf{p}}{qp}\right)^2$$

This expression comes from solving the fluid equations with gravitational forcing and keeping only the leading non-linear terms. The kernel has interesting limits:

- **Aligned modes** ($\mathbf{q} \parallel \mathbf{p}$): $F_2 \approx 1$
- **Perpendicular modes** ($\mathbf{q} \perp \mathbf{p}$): $F_2 \approx 1/2$

The second-order field grows as $\delta_m^{(2)} \propto D^2(z)$ and becomes significant at mildly non-linear scales ($k \gtrsim 0.1 \, h/\mathrm{Mpc}$).

### Higher-Order Terms

Third-order and higher contributions involve triple and multiple integrals of linear field modes with increasingly complex kernels $F_3, F_4, \ldots$ These are suppressed at the scales of interest for this thesis (large-scale bias modeling) and are typically neglected.

## Power Spectrum and Variance

### Linear Power Spectrum

The power spectrum of the linear density field is defined as:

$$\langle \tilde{\delta}_m^{(1)}(\mathbf{k}) \tilde{\delta}_m^{(1)*}(\mathbf{k}') \rangle = (2\pi)^3 \delta_D(\mathbf{k} - \mathbf{k}') P_{mm}^{(1)}(k,z)$$

where $\delta_D$ is the Dirac delta function. The power spectrum is often written in terms of the **dimensionless power spectrum**:

$$\Delta^2(k,z) = \frac{k^3}{2\pi^2} P_{mm}(k,z)$$

which has units of power and is scale-invariant for power-law spectra. The linear power spectrum is computed from a Boltzmann code (e.g., CAMB, CLASS) that solves the coupled photon-baryon-dark-matter system during radiation domination and recombination.

### Linear Variance

The **linear variance** at smoothing scale $R$ (or equivalently, at wavenumber $k \approx 1/R$) is:

$$\sigma_L^2(R,z) = \int_0^\infty \frac{dk}{2\pi^2} k^2 P_{mm}^{(1)}(k,z) W^2(kR)$$

where $W(kR)$ is a smoothing window (e.g., top-hat in real space, Gaussian in Fourier space). The variance quantifies the typical amplitude of density fluctuations at that scale.

For the renormalization procedure discussed in [[Renormalization]], the quantity of interest is the unsmoothed variance:

$$\sigma_L^2 = \int_0^\infty \frac{dk}{2\pi^2} k^2 P_{mm}^{(1)}(k)$$

This quantity diverges if we integrate to arbitrarily high $k$ (ultraviolet divergence), which is why renormalization is necessary to remove the UV sensitivity of non-linear operators.

### Non-Linear Power Spectrum

The full power spectrum including second-order corrections is:

$$P_{mm}(k) = P_{mm}^{(1)}(k) + P_{mm}^{(2)}(k) + P_{mm}^{1-loop}(k) + \ldots$$

where $P_{mm}^{(2)}(k)$ is the second-order term and $P_{mm}^{1-loop}(k)$ are loop corrections from second-order perturbation theory. These corrections are important for matching simulations at $k \sim 0.1-0.5 \, h/\mathrm{Mpc}$ and motivate the use of renormalization schemes.

## Laplacian Operator and Scale-Dependent Physics

The Laplacian of the density field, $\nabla^2 \delta_m$, appears in the [[Bias Expansion]] as the Laplacian bias term $b_{\nabla^2}^x \nabla^2 \delta_m$. In Fourier space:

$$\nabla^2 \delta_m \leftrightarrow -k^2 \tilde{\delta}_m(\mathbf{k})$$

This operator suppresses long-wavelength modes (small $k$) and enhances short-wavelength modes (large $k$). It represents a **scale-dependent response**: the ionization field does not respond equally to all scales of matter perturbations. Small-scale perturbations (short wavelengths, large $k$) are suppressed because the ionization response is limited by the bubble scale $R_\mathrm{eff}$.

Thus, the term $b_{\nabla^2}^x \nabla^2 \delta_m$ in real space becomes $-b_{\nabla^2}^x k^2 \tilde{\delta}_m(k)$ in Fourier space, contributing a $-k^2$ suppression to the power spectrum. Since $b_{\nabla^2}^x \approx -R_\mathrm{eff}^2/3$ is negative, the Laplacian term acts to suppress power at high $k$, as expected physically.

## Relationship to Ionization Field

The ionization field's dependence on the matter field is the core idea of the bias expansion:

$$\delta_x(\mathbf{x},z) = b_1^x(\delta_m) \delta_m + b_2^x \delta_m^2 + b_{\nabla^2}^x \nabla^2 \delta_m + \varepsilon^x$$

Different simulators model reionization via different physics (sources, radiative transfer, recombination), but the **operator basis** $(\delta_m, \delta_m^2, \nabla^2 \delta_m)$ is universal. The ionization field responds to the matter field through:

1. **Linear response** to matter clustering ($b_1^x \delta_m$)
2. **Non-linear feedback** in overdense and underdense regions ($b_2^x \delta_m^2$)
3. **Scale-dependent suppression** on bubble scales ($b_{\nabla^2}^x \nabla^2 \delta_m$)
4. **Stochastic noise** uncorrelated with matter ($\varepsilon^x$)

Understanding $\delta_m$ in detail is thus essential for interpreting how different simulators produce different ionization fields.

## Numerical Considerations: Simulations vs. Theory

In N-body and hydrodynamical simulations (like those used to generate reionization simulations), the density field is discretized onto a grid or particle mesh. The measured $\delta_m(\mathbf{x})$ from simulations contains:

- **Noise** from finite resolution and particle sampling
- **Resolution dependence**: the small-scale power depends on grid/force resolution
- **Aliasing effects**: modes beyond the Nyquist frequency fold back into the resolved modes

When computing the bias expansion, these effects must be accounted for. The [[Renormalization]] procedure addresses UV sensitivity precisely because simulation resolution introduces an effective UV cutoff.

## Connections to Related Concepts

- **[[Bias Expansion]]**: The overdensity field is the fundamental input to the bias expansion
- **[[Effective Field Theory]]**: EFT treats the matter field as the fundamental variable and expands other fields in powers of its fluctuations
- **[[Renormalization]]**: The renormalized quadratic operator $[\delta_m^2]_\mathrm{renorm}$ removes UV sensitivity stemming from $\sigma_L^2$
- **[[Linear Growth Factor]]**: Controls the time evolution of linear density perturbations
- **[[Power Spectrum]]**: The power spectrum of the matter field is input to computing the ionization field power spectrum
- **[[Perturbation Theory]]**: Provides systematic expansion of non-linear density fields via the kernels $F_2, F_3, \ldots$

## Summary

The matter overdensity field is the fundamental variable in cosmological perturbation theory and the basis for the bias expansion of the ionization field. Its evolution is governed by gravity, well-understood from linear perturbation theory, and accessible via second-order perturbation theory at intermediate scales. The perturbation theory decomposition into linear and non-linear components $\delta_m^{(1)}, \delta_m^{(2)}, \ldots$ directly maps onto the terms in the bias expansion, making the ionization field predictions both physically interpretable and computationally tractable across different reionization simulators.
