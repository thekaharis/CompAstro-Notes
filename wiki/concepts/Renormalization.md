---
type: concept
title: "Renormalization"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/theory
  - domain/eft
status: developing
complexity: advanced
domain: "[[Effective Field Theory]]"
related:
  - "[[Bias Expansion]]"
  - "[[Effective Field Theory]]"
  - "[[Matter Overdensity Field]]"
  - "[[Power Spectrum Error]]"
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Qin et al 2022 (EFT Redshift Space)]]"
sources:
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Qin et al 2022 (EFT Redshift Space)]]"
  - "[[Baldauf et al 2012 (Renormalization in SPT)]]"
  - "[[Senatore & Zaldarriaga 2017 (Lagrangian Resummation)]]"
---

# Renormalization

## What is Renormalization in EFT?

Renormalization is a procedure to remove ultraviolet (UV) sensitivity—dependence on small-scale, high-wavenumber modes—from the bias coefficients in the [[Bias Expansion]]. Without renormalization, the quadratic bias coefficient $b_2^x$ depends on the resolution or smoothing scale of the simulation, making simulator comparison impossible. With proper renormalization, the bias coefficients become **well-defined, scale-independent quantities** that truly capture the ionization physics, independent of implementation details.

The renormalization procedure is borrowed from effective field theory in particle physics, where it addresses the problem that loop integrals diverge at high energies without a UV cutoff. In the context of cosmological biasing, the analogous problem is that quadratic and higher-order bias terms depend on the unresolved small-scale power of the matter field. Renormalization absorbs these UV-divergent pieces into the definition of the bias coefficients, leaving only the physically meaningful parts.

## The Problem: UV Sensitivity Without Renormalization

Consider the naïve bias expansion:

$$\delta_x(\mathbf{x},z) = b_1^x \delta_m(\mathbf{x},z) + \frac{b_2^x}{2} \delta_m^2(\mathbf{x},z) + b_{\nabla^2}^x \nabla^2 \delta_m(\mathbf{x},z) + \varepsilon^x(\mathbf{x},z)$$

The linear term $b_1^x \delta_m$ is unproblematic: it is well-defined and unique. However, the quadratic term $\frac{b_2^x}{2} \delta_m^2$ is problematic. Let us see why.

### UV Divergence of the Quadratic Term

The power spectrum contribution from the quadratic term involves integrals like:

$$\langle \delta_m^2(\mathbf{k}) \delta_m(-\mathbf{k}) \rangle = \int \frac{d^3q}{(2\pi)^3} P_{mm}(q) P_{mm}(|\mathbf{k}-\mathbf{q}|)$$

As the wavenumber $q$ goes to infinity (small scales), the integrand approaches a constant. In 3D, the integral:

$$\int_0^\infty dq \, q^2 \, (\text{const}) = \infty$$

diverges logarithmically. This divergence reflects a fundamental property: **the value of $\delta_m^2$ depends on the sum of all small-scale fluctuations**, not just the large scales relevant to reionization.

In simulations, this integral is cut off at the Nyquist wavenumber $k_\mathrm{Ny} = \pi / \Delta x$, where $\Delta x$ is the grid resolution. Thus, the measured quadratic power depends critically on resolution:

$$\langle \delta_m^2 \rangle_{\Delta x} = \int_0^{k_\mathrm{Ny}(Delta x)} \frac{dq}{2\pi^2} q^2 P_{mm}(q)$$

A high-resolution simulation with small $\Delta x$ has larger $k_\mathrm{Ny}$ and thus larger $\langle \delta_m^2 \rangle$. To match the measured power spectrum, the extracted $b_2^x$ must compensate: high-resolution simulations yield different $b_2^x$ than low-resolution ones, even though the physical ionization process is identical.

This is a serious problem: if bias coefficients depend on resolution, they are not fundamental quantities, and cross-simulator comparison becomes meaningless.

## The Renormalization Prescription

The solution is to renormalize the quadratic operator using the **Standard Perturbation Theory (SPT) renormalization**. The renormalized quadratic operator is:

$$[\delta_m^2]_\mathrm{renorm} = (\delta_m^{(1)} + \delta_m^{(2)})^2 - (\delta_m^{(2)})^2 - \frac{68}{21} \sigma_L^2 \, \delta_m^{(1)}$$

This expression looks complicated, but its logic is sound. Let us parse it term by term.

### Term 1: Total Density-Squared

The first term:

$$(\delta_m^{(1)} + \delta_m^{(2)})^2 = (\delta_m^{(1)})^2 + 2 \delta_m^{(1)} \delta_m^{(2)} + (\delta_m^{(2)})^2$$

is the full second-order expansion of $\delta_m^2$ in perturbation theory. It includes the linear field squared, the cross-term between first and second order, and the second-order field squared.

### Term 2: Second-Order Field Squared

The second term $-(\delta_m^{(2)})^2$ removes the contribution from squaring the second-order perturbation theory field. This piece is not part of the physical non-linear response we wish to capture; it is a higher-order (third-order) contribution. By subtracting it, we isolate the first and second-order pieces.

### Term 3: The Counter-term

The critical term is:

$$-\frac{68}{21} \sigma_L^2 \, \delta_m^{(1)}$$

This is the **counter-term** that absorbs the UV divergence. Here:

$$\sigma_L^2 = \int_0^\infty \frac{dk}{2\pi^2} k^2 P_{mm}(k)$$

is the linear variance, which depends on the integral of the matter power spectrum over all scales. Without a UV cutoff, this integral diverges. However, within the renormalization procedure, $\sigma_L^2$ is **defined at a UV cutoff** $\Lambda$ corresponding to the resolution scale (e.g., the grid spacing in a simulation):

$$\sigma_L^2(\Lambda) = \int_0^\Lambda \frac{dk}{2\pi^2} k^2 P_{mm}(k)$$

The counter-term $-\frac{68}{21} \sigma_L^2(\Lambda) \delta_m$ precisely cancels the UV divergence in the quadratic contribution when computed in perturbation theory.

### The Coefficient 68/21

The coefficient $68/21 \approx 3.238$ is not arbitrary. It comes from integrating the second-order perturbation theory kernel $F_2(\mathbf{q}, \mathbf{p})$ over all mode combinations:

$$\frac{68}{21} = \int \frac{d^3q d^3p}{(2\pi)^6} F_2(\mathbf{q}, \mathbf{p})^2 \delta_D(\mathbf{q} + \mathbf{p})$$

Its precise value is essential: if the coefficient is wrong, the UV divergence is not properly removed. This is why renormalization cannot be done ad hoc; the coefficient must come from the underlying perturbation theory.

Interestingly, $68/21 = (34/21)^2$, where $34/21 \approx 1.619$ is the coefficient in the standard SPT expression for the one-loop power spectrum correction. This is not a coincidence; the quadratic structure naturally leads to the square.

## Effect of Renormalization on the Power Spectrum

After renormalization, the bias expansion becomes:

$$\delta_x(\mathbf{x},z) = b_1^x \delta_m^{(1)} + \frac{b_2^x}{2} [\delta_m^2]_\mathrm{renorm} + b_{\nabla^2}^x \nabla^2 \delta_m^{(1)} + \varepsilon^x$$

When this is Fourier-transformed and the power spectrum is computed, the key difference is:

**Without renormalization**: $b_2^x$ includes UV sensitivity. Different simulations with different resolutions extract different $b_2^x$, making cross-simulator comparison unreliable.

**With renormalization**: The renormalized operator removes UV sensitivity. The same physics yields the same $b_2^x$ across simulators with different resolutions. Additionally, the regime of validity extends to larger wavenumbers.

### Concrete Example: Extension of Validity Regime

McQuinn & D'Aloisio (2018) found EFT validity to $k \lesssim 0.2-0.5 \, h/\mathrm{Mpc}$ without systematic renormalization. Qin et al. (2022) implemented renormalization and achieved validity to $k \lesssim 0.8 \, h/\mathrm{Mpc}$, a factor of $\sim 2-4$ extension.

This extension arises because renormalization removes the leading UV divergence. In perturbation theory, the breakdown of the expansion is partly due to uncontrolled growth of higher-order terms stemming from UV sensitivity. By absorbing this sensitivity into the coefficients, renormalization suppresses the higher-order corrections, allowing the expansion to remain valid to larger $k$.

## Practical Implementation

In practice, renormalization is implemented as follows:

1. **Decompose the density field** in the simulation into linear and second-order parts:
   $$\delta_m^{(1)} = D(z) \delta_m^{(1)}(z=0)$$
   $$\delta_m^{(2)} = D^2(z) F_2[\delta_m^{(1)}(z=0), \delta_m^{(1)}(z=0)]$$
   
   The linear field is straightforward; the second-order field is computed via the SPT kernel.

2. **Compute the counter-term variance** at the UV cutoff scale:
   $$\sigma_L^2(\Lambda) = \int_0^\Lambda \frac{dk}{2\pi^2} k^2 P_{mm}(k,z)$$
   
   The cutoff $\Lambda$ is typically chosen as the Nyquist frequency of the simulation or slightly below to avoid aliasing effects.

3. **Form the renormalized operator**:
   $$[\delta_m^2]_\mathrm{renorm} = (\delta_m^{(1)} + \delta_m^{(2)})^2 - (\delta_m^{(2)})^2 - \frac{68}{21} \sigma_L^2(\Lambda) \delta_m^{(1)}$$

4. **Fit the bias expansion** to the simulated power spectrum using the renormalized operator, extracting $b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon}$.

5. **Verify resolution independence** by repeating steps 1-4 with simulations at different resolutions and confirming that the extracted coefficients agree.

## Resolution Independence and Universality

The key test of renormalization is **resolution independence**: if renormalization works, then fitting the EFT to simulations at different resolutions should yield identical bias coefficients (up to statistical noise and systematic simulation differences).

Qin et al. (2022) verified this: they ran simulations at three different resolutions (64, 128, 256 cells) and found that the renormalized $b_2^x$ agrees across resolutions to $\lesssim 5\%$, whereas the unrenormalized $b_2^x$ differs by factors of 2-3.

This resolution independence is the hallmark of proper renormalization. It confirms that the procedure truly removes UV sensitivity and leaves only the physical ionization response.

## Limitations and Open Questions

While renormalization is powerful, it has limitations:

### 1. Does Renormalization Fully Address Simulator Differences?

Different simulators may have different ionization physics beyond resolution. For example:
- **21cmFAST** uses Gaussian density and a simplified ionization model
- **THESAN** includes full hydrodynamics and detailed radiative transfer
- **SCRIPT** uses semi-numerical approach with source clustering

Even after renormalization, do their bias coefficients match? Partly yes—renormalization removes artificial resolution differences. But genuine physics differences (e.g., how radiative transfer is computed) may yield different coefficients. This is not a failure; rather, it shows that residual simulator differences are physical, not artifacts.

### 2. Choice of UV Cutoff Scale

The renormalization depends on the choice of cutoff $\Lambda$. If $\Lambda$ is set too high (beyond Nyquist), aliasing contaminates the integral. If set too low, some perturbative information is lost. The "correct" choice is not always obvious and may be simulation-dependent.

### 3. Higher-Order Renormalization

The counter-term $-\frac{68}{21} \sigma_L^2 \delta_m$ addresses the leading UV divergence in the quadratic operator. But higher-order operators (cubic, quartic) also diverge. In principle, each order requires its own renormalization. However, for the scales and precision relevant to this thesis, second-order renormalization suffices.

## Connection to EFT Consistency

The requirement for renormalization reveals a deep principle of effective field theory: **a theory is effective only if it respects its UV scale**. In this case, the UV scale is set by the ionization bubble size $R_\mathrm{eff}$. Below this scale, the theory breaks down and cannot be trusted. Renormalization is not a magical fix—it is an honest accounting of this limitation.

By properly renormalizing, we ensure that the bias coefficients encode only the long-wavelength (infrared) physics relevant to large-scale structure, not spurious UV artifacts. This makes the EFT framework reliable and predictive.

## Connections to Related Concepts

- **[[Bias Expansion]]**: Renormalization corrects the quadratic term in the expansion
- **[[Effective Field Theory]]**: Renormalization is a core EFT principle
- **[[Matter Overdensity Field]]**: The counter-term depends on the variance of the matter field
- **[[Power Spectrum Error]]**: Renormalization reduces the power spectrum error and extends the validity regime
- **[[McQuinn & D'Aloisio 2018]]**: Pioneering EFT work for ionization
- **[[Qin et al 2022 (EFT Redshift Space)]]**: Applied systematic renormalization

## Summary

Renormalization is a crucial step for making the ionization field bias expansion well-defined and simulator-independent. The renormalized quadratic operator absorbs UV divergence through a counter-term proportional to the linear variance, with a coefficient $68/21$ derived from perturbation theory. This procedure removes the artificial resolution dependence of the unrenormalized quadratic bias, enabling fair comparison across simulators with different resolutions and implementations. The success of renormalization—verified by resolution-independent bias coefficients—demonstrates that the ionization field response is governed by long-wavelength physics, even when the microscopic implementation differs. Renormalization extends the EFT validity regime from $k \lesssim 0.2-0.5$ to $k \lesssim 0.8 \, h/\mathrm{Mpc}$, significantly improving the utility of EFT for cosmological inference from 21cm observations of reionization.
