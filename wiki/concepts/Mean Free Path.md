---
type: concept
title: "Mean Free Path"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/physics
  - domain/reionization
status: developing
domain: "[[Reionization Physics]]"
aliases:
  - "Rmfp"
  - "mfp"
  - "mean free path of ionizing photons"
related:
  - "[[Ionization Morphology]]"
  - "[[Clumping Factor]]"
  - "[[Bubble Size Distribution]]"
  - "[[Excursion Set Formalism]]"
  - "[[Lyman Limit Systems]]"
sources:
  - "[[Choudhury 2022 (Reionization Intro)]]"
  - "[[Trac & Gnedin 2009 (Reionization Simulations)]]"
  - "[[Gnedin & Madau 2022 (Modeling Reionization)]]"
---

# Mean Free Path of Ionizing Photons

## Definition and Physical Derivation

The **mean free path** $\lambda_\text{MFP}$ (often written $R_\text{mfp}$ in the context of bubble radii) is the characteristic distance that an ionizing photon (with energy 13.6 eV or greater) travels through neutral intergalactic medium before being absorbed by a neutral hydrogen atom or a **Lyman-limit system** (LLS) — a dense absorber with neutral hydrogen column density $N_\text{HI} \gtrsim 10^{17}\,\text{cm}^{-2}$ and optical depth $\tau_\text{LL} \gtrsim 1$ to ionizing radiation.

### Derivation from LLS Number Density

The mean free path can be derived from the absorption cross-section and the number density of absorbers:

$$\lambda_\text{MFP} = \frac{1}{n_\text{LLS} \cdot \sigma_\text{LL}}$$

where:
- $n_\text{LLS}$ is the line density (number per unit comoving distance) of Lyman-limit systems
- $\sigma_\text{LL}$ is the geometric cross-section of an LLS; typical scale $\sigma_\text{LL} \sim \pi R_\text{LLS}^2$ with $R_\text{LLS} \sim 10$–$100\,\text{kpc}$

More carefully, the effective optical depth accumulated by a photon traveling distance $l$ through a medium with LLS distribution is:

$$\tau_\text{eff}(l) = \int_0^l dl'\, n_\text{LLS}(l')\,\sigma_\text{LL}$$

The mean free path is defined as the distance at which $\tau_\text{eff}(\lambda_\text{MFP}) = 1$:

$$\tau_\text{eff}(\lambda_\text{MFP}) = n_\text{LLS} \cdot \sigma_\text{LL} \cdot \lambda_\text{MFP} = 1$$

giving $\lambda_\text{MFP} = 1/(n_\text{LLS} \sigma_\text{LL})$.

### Column Density Distribution Function

The LLS abundance is often described via the **column density distribution function** $f(N_\text{HI})$ — the number density of systems with column density between $N$ and $N + dN$:

$$\frac{dN}{dz}\,dN = f(N_\text{HI})\,dN$$

Observations from quasar absorption spectra find a power-law distribution:

$$f(N_\text{HI}) \propto N_\text{HI}^{-\beta}$$

with $\beta \sim 1.5$–$2.0$ (sometimes written as $\partial^2N / \partial z \, \partial \ln N$). The mean free path is computed by integrating over all LLS:

$$\frac{1}{\lambda_\text{MFP}} = \int_{N_\text{min}}^{\infty} dN \, f(N_\text{HI})\,\sigma_\text{LL}(N_\text{HI})$$

where the cross-section $\sigma_\text{LL}(N)$ depends on column density (denser systems have higher optical depths but may have similar physical sizes; the relationship is complex).

## Observational Measurements

### Quasar Absorption Line Surveys (z = 2–6)

The current best observational constraints on mean free path come from **Lyman-limit absorption in quasar spectra**:

- **Worseck et al. (2014):** Measured the incidence of LLS in the XQ-100 quasar sample at $z = 2$–$4.5$; found $\lambda_\text{MFP} \sim 100$–$150$ Mpc at $z = 2$, decreasing to $\lambda_\text{MFP} \sim 20$–$50$ Mpc at $z = 4$.

- **Prochaska & Wolfe (2009):** Earlier work on damped Lyman-alpha systems (DLAs) and sub-LLS gave $\lambda_\text{MFP} \sim 70$ Mpc at $z \sim 3$.

- **Becker et al. (2013):** At the highest redshifts reachable, $z \sim 5$–$5.5$, the mean free path is estimated to be $\lambda_\text{MFP} \sim 5$–$10$ Mpc (much smaller due to the neutral IGM).

### Evolution with Redshift

The observations suggest an evolution:

$$\lambda_\text{MFP}(z) \propto (1+z)^{-\gamma}$$

with $\gamma \sim 4$–$5$ at high redshift. This is a **rapid evolution**: from $z = 6$ to $z = 10$, the mean free path decreases by a factor $(10/6)^5 \sim 10$–$30$!

More concretely:
- $z = 6$: $\lambda_\text{MFP} \sim 3$–$10$ Mpc
- $z = 8$: $\lambda_\text{MFP} \sim 0.3$–$1$ Mpc
- $z = 10$: $\lambda_\text{MFP} \sim 0.03$–$0.1$ Mpc

This steep evolution reflects the increasing neutral fraction $\bar{x}_\text{HI}$ at higher $z$, which increases the abundance of absorbers (both diffuse neutral gas and dense systems).

### Extrapolation to $z > 6$: Uncertainty

**A major source of uncertainty** is extrapolating these measurements to $z > 6$, where direct observations are sparse. Different models give:

1. **Linear extrapolation of power law:** $\lambda_\text{MFP}(z) = \lambda_0 (1+z_0)^{-\gamma} / (1+z)^{-\gamma}$ with $\gamma \sim 5$ gives very small $\lambda_\text{MFP}$ at $z > 7$ (few hundred kpc).

2. **Self-consistent recombination model:** Using the ionization state and LLS physics self-consistently can give gentler evolution (larger $\lambda_\text{MFP}$).

3. **Simulation predictions:** Full RT simulations (THESAN, GADGET-3) compute $\lambda_\text{MFP}$ directly from their particle distributions and typically find values intermediate between conservative and aggressive extrapolations.

This extrapolation uncertainty is **not a minor detail** — it affects the predicted bubble sizes, the photon budget, and hence the inferred source properties needed to reionize by $z \sim 6$. Different choices of $\lambda_\text{MFP}(z)$ can shift the required escape fraction $f_\text{esc}$ by factors of 2–3.

## Mean Free Path as a Simulation Parameter

In semi-numerical reionization codes (21cmFAST, SCRIPT), $\lambda_\text{MFP}$ is a **free input parameter** that sets the maximum search radius in the excursion-set criterion:

$$\text{Ionized if } \zeta f_\text{coll}(\mathbf{x}, R) \geq 1 \text{ for some } R \leq R_\text{mfp}$$

Physically, this encodes the fact that photons cannot propagate beyond $\lambda_\text{MFP}$ due to absorption, so even if the ionization criterion would be satisfied at larger $R$, bubbles are capped at $R_\text{mfp}$.

**In practice**, $\lambda_\text{MFP}$ is often:
- Set to a constant value (e.g., 50 Mpc at all epochs)
- Interpolated from observational measurements at $z \lesssim 6$
- Varied as a free parameter to match observational reionization history (e.g., Planck CMB optical depth)

Different semi-numerical codes and reionization models use different values, producing different bubble morphologies at the same global $\bar{x}_\text{HII}(z)$. This is one source of the EFT coefficient variation that P1 aims to quantify.

## Relationship to UV Background Strength

The mean free path depends on the **hardness of the UV background** — i.e., the spectral energy distribution of ionizing photons.

- **Softer UV** (more photons near 13.6 eV, fewer at high energies): lower $\lambda_\text{MFP}$ because low-energy photons are absorbed more readily
- **Harder UV** (hotter sources or metal-poor stars): higher $\lambda_\text{MFP}$ because high-energy photons penetrate farther through the LLS population

This creates a **feedback loop**: as reionization progresses and the ionized fraction grows, the mean UV photon energy (the ratio of hard to soft photons) increases, which can *increase* $\lambda_\text{MFP}$ slightly. However, the dominant effect is still the decreasing neutral fraction and LLS abundance, which decrease $\lambda_\text{MFP}$ at fixed UV spectrum.

## Distinction: $\lambda_\text{MFP}$ (Photon Transport) vs. $R_\text{eff}$ (Bubble Morphology)

A common source of confusion: $\lambda_\text{MFP}$ and the effective bubble radius $R_\text{eff}$ are **not the same**, though they are correlated:

| Quantity | Definition | Physical meaning |
|----------|-----------|----------|
| $\lambda_\text{MFP}$ | Distance a photon travels before absorption | Photon transport; sets upper limit on bubble growth |
| $R_\text{eff}$ | Characteristic radius of ionized bubbles | Morphological quantity; the scale at which ionization field has peak fluctuations |

Relation:
$$R_\text{eff}(\bar{x}_\text{HII}) \approx \text{scale where } \zeta f_\text{coll}(R) \sim 1 \lesssim \lambda_\text{MFP}$$

So $R_\text{eff}$ is typically *smaller* than $\lambda_\text{MFP}$ (bubbles saturate when photon production matches hydrogen abundance, before reaching the mean free path limit). However:
- If $\lambda_\text{MFP}$ is very small, bubbles are capped and $R_\text{eff} \approx \lambda_\text{MFP}$
- If $\lambda_\text{MFP}$ is very large, bubbles are limited by the ionization criterion and $R_\text{eff} \ll \lambda_\text{MFP}$

In practice, at $z \sim 6$–$8$, both are on the scale of a few Mpc, so the distinction matters for careful morphological predictions.

## Evolution and the Photon Budget Constraint

The rapid decrease of $\lambda_\text{MFP}$ at high redshift has profound implications for the photon budget. The ionization must proceed fast enough to keep up with the shrinking mean free path, or bubbles cannot grow. This creates a tension:

- **Early times** ($z > 10$): $\lambda_\text{MFP}$ is small ($\lesssim 1$ Mpc); bubbles can only be small; reionization is slow
- **Late times** ($z \sim 6$): $\lambda_\text{MFP}$ is larger ($\sim$ few Mpc); bubbles can be larger; reionization must be rapid to finish by $z = 6$

This leads to the conclusion that reionization must have a **rapid tail** — a sudden acceleration near $z \sim 6$, driven by the increase in galaxy abundance and/or escape fraction. This picture is consistent with observations (Gunn-Peterson rapid evolution, LAE disappearance) and 21 cm simulations.

## Connection to EFT

$\lambda_\text{MFP}$ directly affects $R_\text{eff}$ and hence the EFT coefficient:

$$b_{\nabla^2}^x \approx -\frac{R_\text{eff}^2}{3} \sim -\frac{\lambda_\text{MFP}^2}{3}$$

(at late times when bubbles are large and approach the mean free path limit). The EFT perturbative regime breaks down at scales $k \lesssim 1/R_\text{eff} \sim 1/\lambda_\text{MFP}$, typically $k \lesssim 0.1$–$0.2\,\text{Mpc}^{-1}$.

Different choices of $\lambda_\text{MFP}(z)$ produce different EFT trajectories and different predictions for 21 cm power spectra. This is a systematic that must be controlled when using semi-numerical models to extract EFT coefficients.

## Lyman-Limit Systems vs. Clumping Factor

Both the [[Lyman Limit Systems|LLS population]] (encoded in $\lambda_\text{MFP}$) and the [[Clumping Factor]] encode "sink physics" — where ionizing photons are absorbed and where recombinations occur — but at different scales:

- **$\lambda_\text{MFP}$:** Discrete, dense absorbing systems (LLS, DLAs); sets a hard upper limit on bubble growth; enters the excursion-set criterion directly
- **Clumping factor $C$:** Sub-resolution recombination in the diffuse IGM; enters the global photon budget equation; typically $C \sim 3$ (more in high-$z$ universe)

In reality, both effects are important and sometimes degenerate: a higher clumping factor (more recombinations) is partially compensated by a higher $\lambda_\text{MFP}$ (fewer absorbers) when fitting observed reionization histories, because both increase the required ionizing photon production.

## See Also

- [[Ionization Morphology]] — how $\lambda_\text{MFP}$ sets the maximum bubble size
- [[Excursion Set Formalism]] — the algorithm that uses $R_\text{mfp}$ as an input
- [[Clumping Factor]] — the complementary "sink physics" at smaller scales
- [[Neutral Fraction]] — the evolution of which depends on photon absorption and $\lambda_\text{MFP}$
