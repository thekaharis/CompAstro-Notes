---
type: source
title: "Choudhury 2022 (Reionization Intro)"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/reionization
  - source/review
status: mature
source_type: paper
author:
  - "[[Choudhury, Tirthankar Roy]]"
date_published: 2022
url: "https://arxiv.org/abs/2209.05580"
confidence: high
key_claims:
  - "Pedagogical derivation of the reionization photon budget from first principles: sources, sinks, and the global neutral fraction equation"
  - "Excursion-set formalism (Press-Schechter, Sheth-Tormen) provides the halo mass function needed for semi-numerical models"
  - "Reionization probes reviewed: Lyman-alpha forest, CMB optical depth, Lyman-alpha emitters, 21 cm signal"
related:
  - "[[Reionization Physics]]"
  - "[[Excursion Set Formalism]]"
  - "[[Neutral Fraction]]"
  - "[[Spin Temperature]]"
  - "[[21cm Cosmology]]"
---

# Choudhury 2022 (Reionization Intro)

> [!key-insight]
> A self-contained pedagogical derivation of reionization physics — from halo mass functions and gas cooling through the ionizing photon budget to observational probes — written as an accessible entry point for students new to the field.

## Citation

Choudhury, T. R. (2022). "A Short Introduction to Reionization Physics." *Springer Nature* (book chapter). arXiv:2209.05580. _In memory of T. Padmanabhan._

## Core Claim

Reionization is fully determined by the competition between ionizing photon production and recombinations/sinks in the IGM. This review builds the theoretical machinery — halo mass functions, cooling thresholds, escape fractions, and the global neutral fraction equation — from scratch, providing a clean derivation of every key relation used in semi-numerical models like 21cmFAST.

## Pedagogical Approach

The review is structured as a **progressive build-up**:
1. **Gravitational collapse** → halo mass functions (linear perturbation theory)
2. **Cooling physics** → minimum halo mass for star formation (virial temperature thresholds)
3. **Star formation** → number of ionizing photons per baryon (top-heavy IMF assumptions)
4. **IGM recombination** → recombination coefficient and clumping factor
5. **Global reionization** → coupled ODE for neutral fraction evolution
6. **Observational probes** → connecting theory to measurements

This bottom-up approach makes each step transparent and is the pedagogical standard for reionization courses.

## Key Results

### Halo Mass Functions

**Press-Schechter (classical)**:
$$n_\text{PS}(M, z) = \frac{2}{\pi^{1/2}} \frac{\bar{\rho}_m}{M^2} \left|\frac{d\ln\sigma(M)}{d\ln M}\right| \exp\left[-\frac{\delta_c^2(z)}{2\sigma^2(M)}\right]$$

where $\delta_c(z)$ is the critical overdensity for collapse (rises from ~1.686 at $z=0$ to ~1.6 at high-$z$).

**Sheth-Tormen correction** (better match to N-body):
$$n_\text{ST}(M, z) = A \sqrt{\frac{a}{\pi}} \frac{\bar{\rho}_m}{M^2} \left|\frac{d\ln\sigma(M)}{d\ln M}\right| \left(1 + \left[\frac{a\delta_c^2(z)}{\sigma^2(M)}\right]^p\right) \exp\left[-\frac{a\delta_c^2(z)}{2\sigma^2(M)}\right]$$

with $A = 0.353$, $a = 0.73$, $p = 0.175$. This form provides **5–15% accuracy** at $M > 10^{10}\,M_\odot$ compared to simulations, vs. ~30% for Press-Schechter at high masses.

**Collapsed fraction**:
$$f_\text{coll}(M_\text{min}, z) = \text{erfc}\left[\delta_c(z) / \sqrt{2\sigma^2(M_\text{min})}\right]$$

The fraction of mass in halos more massive than $M_\text{min}$ — the input to all semi-numerical reionization codes.

### Cooling and Star Formation Thresholds

**Atomic cooling** (Hydrogen):
- Requires $T_\text{vir} \gtrsim 10^4$ K
- Virial temperature: $T_\text{vir} = \frac{\mu m_u}{3k_B} v_\text{c}^2 = \frac{\mu m_u}{3k_B} \frac{GM}{R_\text{vir}}$
- For a halo at $z=10$: **minimum atomic-cooling mass $M_\text{min} \sim 10^8 M_\odot$**
- This is the default $T_\text{vir}$ parameter in 21cmFAST (though observations may favor $10^7$–$10^9 M_\odot$)

**Molecular cooling** (Hydrogen molecules H₂):
- Can cool below $T_\text{vir} \sim 500$ K
- Allows star formation in **smaller halos: $M \sim 10^6$ M_\odot**
- BUT highly sensitive to **Lyman-Werner feedback**: UV photons from early stars dissociate H₂ in neighbor halos
- Escape fraction and spectral hardness of ionizing sources set whether molecular cooling is viable at a given epoch

**X-ray heating feedback**: Hard X-ray photons heat the IGM, raising the minimum cooling temperature and suppressing star formation in small halos. Effect quantified through heating-to-ionization ratio.

### Ionizing Photon Budget

**Photon production rate**:
$$\dot{n}_\text{ion}(z) = \int_{M_\text{min}}^{\infty} n(M, z) \, \dot{N}_\gamma(M, z) \, dM$$

where $\dot{N}_\gamma$ is the photon production rate per halo (depends on stellar mass, IMF, metallicity, binary fraction, X-ray/AGN contribution).

**Recombination rate**:
$$\dot{n}_\text{rec}(z) = C(z) \, \alpha_B(T_\text{IGM}) \, n_e \, n_{\text{HII}} \approx C \, \alpha_B \, \bar{n}_H^2 (1 + z)^3$$

where:
- $C = \langle n^2 \rangle / \langle n \rangle^2$ is the **clumping factor** (~1 in uniform IGM, 5–10 in realistic simulations)
- $\alpha_B(T)$ is the Case-B recombination coefficient (~$2.6 \times 10^{-13}$ cm³ s⁻¹ at $T=10^4$ K, declining as $T^{-0.7}$)
- The $(1+z)^3$ factor accounts for comoving density evolution

**The ionizing photon budget**:
$$\dot{n}_\text{ion} = f_\text{esc} \, N_\gamma \, \dot{n}_* > C \, \alpha_B \, \bar{n}_H^2 \, x_\text{HII}$$

where $f_\text{esc}$ is the escape fraction of ionizing photons (measured at 0.1–0.5 in observations/simulations). **This inequality determines reionization timescale.**

### Global Neutral Fraction Evolution

The master equation for reionization is:
$$\frac{d Q_\text{HII}}{dt} = \frac{\dot{n}_\text{ion}(\bar{x}_\text{HII}, z)}{\bar{n}_H} - \frac{C(z) \alpha_B(T) \bar{n}_H (1+z)^3 x_\text{HII} x_\text{HII}}{(1+z)^3}$$

where $Q_\text{HII} = 1 - x_\text{HI}$ is the **ionized volume filling factor**.

Equivalently, introducing the **recombination time** $t_\text{rec} = [C \alpha_B \bar{n}_H (1+z)^3]^{-1}$:
$$\frac{d x_\text{HI}}{dt} = -\frac{1}{t_\text{rec}} x_\text{HI} + \frac{\dot{n}_\text{ion}}{\bar{n}_H (1-x_\text{HI})}$$

This is nonlinear in $x_\text{HI}$ and must be integrated forward in time. The **S-shape** of the reionization curve (slow start, rapid transition, slow saturation) emerges naturally.

**Key timescales:**
- At early times ($x_\text{HI} \approx 1$): $t_\text{rec} \gg$ dynamical timescale → slow ionization
- At $x_\text{HI} \approx 0.5$: Both terms significant → rapid transition
- At late times ($x_\text{HI} \lesssim 0.01$): Recombination sink negligible → sources again limit the rate

**Global reionization history predictions** depend sensitively on:
1. The halo mass function choice (PS vs. ST) — affects $f_\text{coll}$ by ~30% at high-$z$
2. The minimum mass $M_\text{min}$ (tunable parameter; default $T_\text{vir} = 10^4$ K in 21cmFAST)
3. The escape fraction $f_\text{esc}$ (constant or redshift/mass-dependent?)
4. The clumping factor $C$ (varies by ~factor 2–3 depending on simulation/model)
5. Radiative feedback mechanisms (Lyman-Werner feedback, X-ray heating, photoevaporation)

### Observable Probes of Reionization

**1. Lyman-alpha forest** (most detailed):
- Transmitted flux in high-redshift QSO spectra: $F(\lambda) = e^{-\tau_\text{eff}(\lambda)}$
- Sensitive to neutral fractions $x_\text{HI} \gtrsim 10^{-5}$
- Provides evolution of **mean neutral fraction** from $z \sim 6$ down to $z \sim 2$
- Sensitive to column density fluctuations and IGM temperature

**2. Lyman-limit systems** (optically thick):
- Absorption at $\lambda_\text{LL} = 912$ Å edge; quenches Lyman-alpha transmission
- Probability of encountering a damped Lyman-alpha system (DLA) or Lyman-limit system
- Constrains clumping factor $C$ and absorption cross-sections

**3. Gunn-Peterson trough**:
- At $z > 6$, Lyman-alpha lines fully blended due to high neutral fraction
- Effective optical depth: $\tau_\text{eff} = \sigma_\text{HI} \bar{n}_\text{HI} \int dz / H(z)$
- **Constraint**: $\bar{x}_\text{HI}(z=6) \lesssim 10^{-3}$–$10^{-4}$ (IGM not fully neutral even at high-$z$)

**4. CMB Thomson optical depth**:
$$\tau_e = \int_0^{\infty} \sigma_T \, n_e(z') \, c\,dt' = \int_0^{\infty} \sigma_T \, n_e(z') \frac{dz'}{H(z')}$$

- Integrated quantity: measures reionization **history**
- Planck 2018: $\tau_e = 0.0567 \pm 0.0073$ (prior constraint on mean ionization history)
- Permits early reionization at $z > 15$ if followed by recombination/cooling

**5. Lyman-alpha emitters** (LAE):
- Requires $x_\text{HI} \lesssim 0.1$ locally (ionized bubble around source)
- Number density evolution probes patchy reionization
- Useful probe of local ionization topology during the EoR

**6. 21 cm signal**:
- Hyperfine transition of neutral hydrogen: $\Delta E = 1.42$ GHz
- Observable from $z \sim 6$ (end of EoR) to $z \sim 200$ (cosmic dawn)
- Sensitive to ionization field $x_\text{HII}$, density field $\delta_m$, and spin temperature
- Power spectrum directly probes EFT physics — the ionized regions that modulate the brightness temperature

## Methods

**Structure and scope:**
- 46 pages, self-contained monograph
- Assumes prior exposure to cosmological perturbation theory and basic statistical mechanics
- Targeted at graduate students and postdocs entering high-redshift astrophysics
- Written as a memorial to Padmanabhan; includes historical perspective on the field

**Derivation philosophy:**
- Every equation derived step-by-step; no "it can be shown that"
- Consistent notation and unit conventions throughout
- Figures provided to illustrate each concept (lightcone maps, mass function comparisons, probe sensitivities)

## Key Equations Summary

**Halo mass function (Sheth-Tormen):**
$$n_\text{ST}(M, z) = A \sqrt{\frac{a}{\pi}} \frac{\bar{\rho}_m}{M^2} \left|\frac{d\ln\sigma}{d\ln M}\right| \left(1 + \left[\frac{a\delta_c^2}{\sigma^2}\right]^p\right) \exp\left[-\frac{a\delta_c^2}{2\sigma^2}\right]$$

**Virial temperature (mass-redshift relation):**
$$T_\text{vir} = \frac{\mu m_u}{3k_B} \frac{GM}{R_\text{vir}} \approx 10^4 \left(\frac{M}{10^8 M_\odot}\right)^{2/3} (1+z) \text{ K}$$

**Global reionization equation:**
$$\frac{dQ_\text{HII}}{dt} = \frac{\dot{n}_\text{ion}(\bar{x}_\text{HII}, z)}{\bar{n}_H} - \frac{C(z)\,\alpha_B(T_\text{IGM})\,\bar{n}_H\,(1+z)^3\,x_\text{HII}^2}{(1+z)^3}$$

**Recombination rate:**
$$\dot{n}_\text{rec} = C \, \alpha_B(T) \, \bar{n}_H^2 \, (1+z)^3$$

where $\alpha_B(T) \approx 2.6 \times 10^{-13}(T/10^4)^{-0.7}$ cm³ s⁻¹.

**CMB optical depth:**
$$\tau_e = \int_0^{z_{\text{reion}}} \sigma_T \, n_e(z') \frac{dz'}{H(z')} \approx \int_0^{z_{\text{reion}}} \sigma_T \, x_\text{HII}(z') \, \bar{n}_H \, \frac{dz'}{H(z')}$$

## Connection to This Thesis

### Relevance to P1 (EFT bias measurements)

**Direct relevance:**
- The **collapsed fraction $f_\text{coll}$** calculated here is the physical input that differentiates 21cmFAST and SCRIPT
- Different implementations of the halo mass function (Press-Schechter vs. Sheth-Tormen vs. N-body calibrated) lead to different $f_\text{coll}(M_\text{min}, z)$
- The **clumping factor $C$** and its redshift/mass dependence encodes sub-grid physics; different codes model this differently
- This is a primary source of simulator dependence in the ionization field $x_\text{HII}$

**Open question P1 addresses:**
How much of the variation in EFT coefficients $\{b_1^x, b_2^x, b_\nabla^2, P_{\epsilon\epsilon}\}$ across codes is _explained_ by differences in $f_\text{coll}$ implementation vs. differences in the ionization topology (inside-out vs. outside-in)?

### Relevance to P2 (EFT-based parameter inference)

**Indirect but important:**
- The astrophysical parameters that P2 infers ($\zeta$, $T_\text{vir}$, $R_\text{mfp}$) all appear explicitly in the reionization equations derived here
- P2's claim that "EFT coefficients allow cross-simulator generalization" rests on the hypothesis that EFT captures the universal physics that these parameters drive
- Choudhury provides the foundation for understanding what physical effects each parameter controls

**Supports / contradicts:**
- **Supports:** [[Gnedin & Madau 2022 (Modeling Reionization)]] and [[Trac & Gnedin 2009 (Reionization Simulations)]]—all use the same ionizing photon budget formalism as a starting point
- **Complementary:** [[Ferrara & Pandolfi (IGM Reionization)]]—Choudhury is more theoretical/bottom-up; Ferrara & Pandolfi more observational/phenomenological

## Limitations and Caveats

**What this review does NOT cover:**
1. **Detailed observational constraints** — focuses on defining the probes, not fitting models to data
2. **AGN contribution to reionization** — briefly mentioned but not quantified (important for $z < 10$ and understanding energetics)
3. **Quasar feedback and photoheating** — included conceptually but detailed energetics not worked out
4. **Molecular cooling dynamics** — Lyman-Werner feedback mentioned but not modeled in detail
5. **Radiative transfer effects on small scales** — assumes "mean-field" ionization; does not capture shadowing/photoevaporation in detail
6. **Foreground physics** — dust, metallicity evolution, stellar populations assumed simplified (solar IMF)

**Assumptions that may break:**
1. **Excursion-set formalism** — assumes sharp threshold collapse; extended collapse (critical of high-$z$ star formation) not included
2. **Constant escape fraction** — real galaxies likely have mass-dependent and redshift-dependent $f_\text{esc}$
3. **Homogeneous IGM** — clumping factor $C$ is assumed separable; actually depends on scale, epoch, and prior ionization state
4. **Ionization in optically thin limit** — at high-$x_\text{HII}$, ionization fronts and shadowing become important; not addressed here

**How subsequent work has refined these:**
- [[McQuinn & D'Aloisio 2018]] extended the EFT framework to include scale-dependent bias, handling small-scale structure within ionized bubbles
- [[Sailer et al 2022 (Optical Depth EFT)]] applies EFT to CMB optical depth, showing how EFT generalizes beyond the 21 cm power spectrum
- [[Ore et al 2025 (SKATR)]] demonstrates that neural networks can learn reionization simulators, suggesting that the model assumptions here can be partially bypassed via data-driven methods

## Figures Worth Noting

**Fig. 1:** Lightcone map of HI/HII field evolution from $z\sim 15$ to $z\sim 5$
- Animated progression shows bubble growth and merger
- Visual intuition for "inside-out" ionization topology
- Shows how small bubbles at early times coalesce into the percolating ionized phase

**Fig. 2:** Press-Schechter vs. Sheth-Tormen halo mass functions at $z=7, 10, 15$
- Clear demonstration of Sheth-Tormen superiority at high masses ($M > 10^{10} M_\odot$)
- Shows mass function steepens at high-$z$ (fewer massive halos available)

**Fig. 3:** Global neutral fraction evolution $x_\text{HI}(z)$ for different $f_\text{esc}$, $T_\text{vir}$, $C$
- Demonstrates sensitivity of reionization history to each physical input
- Shows the characteristic S-shaped transition and late-time plateau

**Fig. 4:** Transmission in Lyman-alpha forest vs. redshift
- Mean transmitted flux evolution showing the dramatic drop at $z > 6$
- Gunn-Peterson trough saturation visualization

**Fig. 5:** CMB optical depth integrand $\sigma_T n_e(z) / H(z)$ vs. redshift
- Shows which epochs dominate the integrated $\tau_e$ measurement
- Illustrates why early reionization (z > 15) is possible even with Planck constraints

## Open Questions After Reading

> [!gap]
> **Halo mass function sensitivity:** The review uses Sheth-Tormen throughout, but notes that even better fits to simulations exist. 21cmFAST uses its own N-body-calibrated fits; SCRIPT may use different fits. **How sensitive are EFT coefficients to the mass function choice?** If $f_\text{coll}$ differs by 20% between codes, does that alone explain the P1 discrepancies, or is there additional physics?

> [!gap]
> **Clumping factor measurement:** The clumping factor $C$ is crucial but poorly constrained observationally. Different simulations (fully coupled RT vs. DMO+SAM) predict $C$ values spanning 5–10. **How much of the EFT coefficient spread in P1 is due to differences in $C$ modeling?**

> [!gap]
> **Escape fraction redshift/mass dependence:** This review uses constant $f_\text{esc}$, but real galaxies show strong trends. **Does 21cmFAST implement mass-dependent $f_\text{esc}$ by default, and does SCRIPT?** This could be a major source of simulator dependence.

> [!gap]
> **Ionization threshold sharpness:** The excursion-set assumption (hard threshold at $\delta_c$) may be too simplistic. **How do fuzzy ionization fronts and partial ionization of overdense regions modify the EFT expansion, especially at small $k$?**
