---
type: concept
title: "Power Spectrum Error"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/analysis
  - domain/eft
status: developing
complexity: advanced
domain: "[[Effective Field Theory]]"
related:
  - "[[Bias Expansion]]"
  - "[[Regime of Validity]]"
  - "[[Ionization Morphology]]"
  - "[[Effective Field Theory]]"
  - "[[Power Spectrum]]"
  - "[[McQuinn & D'Aloisio 2018]]"
sources:
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Qin et al 2022 (EFT Redshift Space)]]"
  - "[[Venumadhav et al 2017 (EFT of LSSpert)]]"
---

# Power Spectrum Error

## What is the Power Spectrum Error?

The power spectrum error $P_\mathrm{err}(k,z)$ quantifies how well the [[Bias Expansion]] description of the ionization field matches the actual power spectrum from reionization simulations. It is the residual power remaining after the EFT model is subtracted from the measured ionization field power spectrum. This quantity defines the **regime of validity** for the bias expansion and is the primary diagnostic for assessing whether EFT generalization across simulators is reliable at a given scale and redshift.

Physically, $P_\mathrm{err}$ encodes all physics that the bias expansion fails to capture: non-local radiative transfer effects, stochastic source fluctuations beyond the parameterized noise, bubble-scale resonances, and other small-scale non-perturbative phenomena. By quantifying this error, we can identify the maximum wavenumber at which EFT predictions are trustworthy.

## Mathematical Definition

The power spectrum error is defined operationally as:

$$P_\mathrm{err}(k,z) \equiv P_\mathrm{ion}^{\mathrm{sim}}(k,z) - P_\mathrm{EFT}(k,z)$$

where:

- **$P_\mathrm{ion}^{\mathrm{sim}}(k,z)$** is the measured ionization field power spectrum directly from the simulation
- **$P_\mathrm{EFT}(k,z)$** is the power spectrum predicted by the bias expansion using best-fit coefficients

The best-fit coefficients $(b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon})$ are extracted by fitting the bias expansion to the simulated power spectrum, typically at low $k$ where EFT is reliable. The error is then computed as the residual at higher wavenumbers where the fit is not constrained.

### Relative Error Measure

More commonly, we use the **relative error** (fractional error):

$$\frac{P_\mathrm{err}(k,z)}{P_\mathrm{ion}^{\mathrm{sim}}(k,z)} \equiv \frac{P_\mathrm{ion}^{\mathrm{sim}}(k,z) - P_\mathrm{EFT}(k,z)}{P_\mathrm{ion}^{\mathrm{sim}}(k,z)}$$

This measures what fraction of the simulated power spectrum is unexplained by the EFT model. A relative error of 10% means the EFT captures 90% of the power spectrum; 5% means 95%, etc.

The relative error is scale-dependent: small-scale perturbations (high $k$) produce larger errors than large-scale perturbations (low $k$). This is expected because EFT breaks down first at small scales.

## Regime of Validity Criterion

The **regime of validity** for the bias expansion is conventionally defined as the wavenumber range where:

$$\frac{P_\mathrm{err}(k,z)}{P_\mathrm{ion}^{\mathrm{sim}}(k,z)} < \delta_\mathrm{crit}$$

where $\delta_\mathrm{crit}$ is a critical error threshold. Different works use different thresholds:

- **McQuinn & D'Aloisio (2018)**: $\delta_\mathrm{crit} \approx 10\%$
- **Qin et al. (2022)**: $\delta_\mathrm{crit} \approx 5\%$ (more stringent)
- **Some forecasting works**: $\delta_\mathrm{crit} \approx 20\%$ (more permissive for speed)

The choice of threshold reflects the acceptable error level for cosmological inference. If EFT must predict parameters with sub-percent precision, tighter thresholds apply. If the goal is qualitative understanding, looser thresholds suffice.

## Scale Dependence of Error

The power spectrum error grows with wavenumber, following a characteristic pattern during reionization:

### Low Wavenumber Regime ($k \lesssim 0.1 \, h/\mathrm{Mpc}$)

In this regime, the error is minimal and the bias expansion is highly accurate. The ionization field responds linearly to matter fluctuations; non-linear effects are perturbative. The error here is dominated by noise from the stochastic term $\varepsilon^x$ and numerical precision in the simulation. Typically:

$$\frac{P_\mathrm{err}}{P_\mathrm{ion}} \lesssim 1-5\%$$

### Intermediate Regime ($0.1 \lesssim k \lesssim 0.5 \, h/\mathrm{Mpc}$)

Error growth becomes noticeable. Second-order perturbation theory corrections ($\delta_m^2$, Laplacian term) become important, and the [[Renormalization]] procedure starts to matter significantly. Without renormalization, error is larger; with it, validity extends further. Typical errors:

$$\frac{P_\mathrm{err}}{P_\mathrm{ion}} \sim 5-20\%$$

### High Wavenumber Regime ($k \gtrsim 0.5-0.8 \, h/\mathrm{Mpc}$)

Here, bubble-scale physics dominates. The effective bubble radius $R_\mathrm{eff}$ sets a characteristic scale: perturbations smaller than the bubble are damped by the finite bubble size, and the ionization field becomes non-local in the matter field. Non-perturbative physics (photon diffusion, recombination fronts, ionization shadows) becomes crucial. Errors grow rapidly:

$$\frac{P_\mathrm{err}}{P_\mathrm{ion}} \gtrsim 20-50\%$$

In this regime, EFT fails, and a different approach (e.g., direct simulation-based models) is necessary.

## Redshift Dependence of Error

The error also varies dramatically with redshift, reflecting different reionization states:

### Early Reionization ($z \sim 15-20$, $x_\mathrm{HI} \sim 0.9-1$)

The universe is nearly fully neutral; ionization bubbles are small and rare. The error is relatively low because:
- The ionization field is nearly uniform ($x_\mathrm{HI} \approx 1$ everywhere)
- Fluctuations are small and linear
- The stochastic term is small because sources are sparse

Typical error: $\lesssim 10\%$ at $k \lesssim 0.5 \, h/\mathrm{Mpc}$

### Mid Reionization ($z \sim 10-15$, $x_\mathrm{HI} \sim 0.1-0.9$)

This is the regime where reionization is actively proceeding, with large spatial variations in ionization. Bubble sizes are intermediate (tens of Mpc). The error is substantial because:
- The ionization field exhibits sharp gradients at bubble boundaries
- Non-linear effects (patchiness, recombination) peak
- The stochastic term is large (sources are clustered, radiative transfer is non-local)

Typical error: $\sim 15-30\%$ at $k \lesssim 0.5 \, h/\mathrm{Mpc}$

### Late Reionization ($z \sim 6-10$, $x_\mathrm{HI} \sim 0-0.1$)

The universe is nearly fully ionized; only dense regions (galaxies, filaments) remain neutral. The error is again lower because:
- The ionization field is nearly uniform ($x_\mathrm{HI} \approx 0$ almost everywhere)
- Neutral gas is confined to rare high-density pockets
- The ionization bias becomes complex, and some simulators diverge in their recipes

Typical error: variable, $\sim 5-20\%$, depending on how different codes model residual neutral gas

## Breakdown Scale and Effective Bubble Radius

The wavenumber at which error grows significantly is related to the **effective bubble radius** $R_\mathrm{eff}$ via:

$$k_\mathrm{break} \sim \frac{1}{R_\mathrm{eff}} \sim \frac{1}{R_\mathrm{mfp}}$$

where $R_\mathrm{mfp}$ is the mean free path for ionizing photons. During mid-reionization, $R_\mathrm{eff}$ grows from $\sim 1$ Mpc to $\sim 20-50$ Mpc, so:

$$k_\mathrm{break} \sim 0.02-1 \, h/\mathrm{Mpc}$$

At scales much smaller than $R_\mathrm{eff}$ ($k > 1/R_\mathrm{eff}$), the ionization state cannot vary smoothly because the smallest ionization bubbles have size $\sim R_\mathrm{eff}$. This introduces non-locality: ionization at a point depends on the density field at distances out to $R_\mathrm{eff}$, violating the local operator assumption.

## Validation from Simulations: McQuinn & D'Aloisio 2018

The foundational validation of the EFT approach comes from McQuinn & D'Aloisio (2018), who tested the bias expansion against 21cmFAST simulations and found:

- **At $k \lesssim 0.2 \, h/\mathrm{Mpc}$**: Relative error $< 10\%$ across most of reionization
- **At $k \sim 0.3-0.5 \, h/\mathrm{Mpc}$**: Error rises to $\sim 10-15\%$
- **At $k > 0.5 \, h/\mathrm{Mpc}$**: Error exceeds 20-30%, entering the breakdown regime

This work established the default validity regime: $k \lesssim 0.2-0.5 \, h/\mathrm{Mpc}$ depending on reionization state.

## Extended Validity with Renormalization: Qin et al. 2022

Qin et al. (2022) showed that properly implementing [[Renormalization]] extends the validity regime significantly:

- **Without renormalization**: $k_\mathrm{max} \sim 0.2-0.3 \, h/\mathrm{Mpc}$ (limited by UV sensitivity in $b_2^x$)
- **With renormalization**: $k_\mathrm{max} \sim 0.8 \, h/\mathrm{Mpc}$ (error at $5\%$ level)

The improvement arises because renormalization removes the resolution dependence of the quadratic bias coefficient, allowing the EFT to remain valid to higher $k$.

## Cross-Correlation Coefficient as Alternative Diagnostic

An alternative measure of EFT validity is the **cross-correlation coefficient** between the simulated and EFT power spectra:

$$r(k,z) = \frac{P_\mathrm{ion, EFT}(k,z)}{\sqrt{P_\mathrm{ion}^{\mathrm{sim}}(k,z) \cdot P_\mathrm{EFT}(k,z)}}$$

When EFT perfectly matches simulations, $r = 1$. When they are uncorrelated, $r \approx 0$. When EFT underestimates power, $r < 1$.

The advantage of this diagnostic is that it is less sensitive to absolute error amplitudes and focuses on pattern matching. In the validity regime:

$$r(k,z) \gtrsim 0.95-0.98$$

This criterion is sometimes used as an alternative or complementary definition of where EFT is reliable.

## Sources of Power Spectrum Error

The error arises from several physical sources:

### 1. Bubble-Scale Non-Locality

Once $k > 1/R_\mathrm{eff}$, ionization cannot respond instantaneously to local matter fluctuations because the ionization bubble size sets a coherence scale. The ionization state at one point depends on the density integrated over volume $\sim R_\mathrm{eff}^3$, violating the local bias assumption.

### 2. Radiative Transfer Non-Locality

Photons propagate through space; their absorption and scattering depend on paths and history, not just local density. This creates memory effects and non-local correlations that the bias expansion (which assumes local operators) cannot capture.

### 3. Stochastic Source Formation

The exact positions of ionization sources (galaxies, quasars, stars) fluctuate stochastically. While the mean source density correlates with matter, individual source placement has variance beyond the correlation. This generates the stochastic term $\varepsilon^x$, which cannot be predicted from $\delta_m$ alone.

### 4. Percolation and Topology Transitions

During the transition from isolated bubbles to a percolating network, the ionization field topology changes qualitatively. Bubble merging and coalescence introduce rapid, non-smooth variations that perturbation theory struggles to describe.

### 5. Recombination Fluctuations

Recombination rates depend non-linearly on local temperature and density. Regions with enhanced density have lower recombination rates and ionize faster—a feedback effect not fully captured by the quadratic term $b_2^x \delta_m^2$.

### 6. Hydrodynamics and Gas Dynamics

In full hydrodynamical simulations (e.g., THESAN), gas density and temperature evolve dynamically, creating non-trivial correlations with ionization. The 21cmFAST simplified approach (Gaussian density) doesn't capture these complexities, producing different errors.

## Implications for Cross-Simulator Generalization

The power spectrum error is the key uncertainty in this thesis's goal: **cross-simulator generalization via EFT**. If error is low ($\lesssim 10\%$), fitting EFT to one simulator allows prediction of another simulator's power spectrum. If error is high ($\gtrsim 20\%$), the EFT description is not universal, and generalization fails.

Different simulators may have different errors at the same $(k,z)$ due to their implementation differences. If errors differ significantly, the bias coefficients extracted from different codes will not match, even after accounting for physical differences (resolution, ionization source model, etc.).

## Connections to Related Concepts

- **[[Bias Expansion]]**: The error measures how well the bias expansion works
- **[[Regime of Validity]]**: The regime of validity is defined by the error threshold
- **[[Ionization Morphology]]**: Bubble size and morphology set the breakdown scale
- **[[Effective Field Theory]]**: EFT validity is bounded by this error
- **[[McQuinn & D'Aloisio 2018]]**: Pioneering validation work
- **[[Qin et al 2022 (EFT Redshift Space)]]**: Extended validity via renormalization

## Summary

The power spectrum error quantifies the accuracy of the bias expansion description of the ionization field. It is minimal at large scales ($k \lesssim 0.1 \, h/\mathrm{Mpc}$), grows at intermediate scales, and becomes dominant at small scales ($k \gtrsim 0.5-0.8 \, h/\mathrm{Mpc}$). The error depends critically on redshift, ionization state, and effective bubble size. Using the criterion $P_\mathrm{err}/P_\mathrm{ion} < 5-10\%$, the bias expansion is valid for $k \lesssim 0.2-0.5 \, h/\mathrm{Mpc}$ without renormalization, extended to $k \lesssim 0.8 \, h/\mathrm{Mpc}$ with renormalization. Understanding and minimizing this error is essential for achieving reliable cross-simulator generalization of 21cm cosmology inference.
