---
type: source
title: "Ferrara & Pandolfi (IGM Reionization)"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/reionization
  - source/review
  - domain/lyman-alpha
status: mature
source_type: paper
author:
  - "[[Ferrara, Andrea]]"
  - "[[Pandolfi, Stefania]]"
date_published: 2013
url: ""
confidence: medium
key_claims:
  - "Two-lecture pedagogical overview of the IGM and cosmic reionization: from the Lyman-alpha forest to the topology of HII regions"
  - "The Gunn-Peterson trough at z > 6 is consistent with a volume-averaged neutral fraction of only ~10^-4 to 10^-3, not a fully neutral IGM"
  - "Reionization is inside-out: denser, more biased regions ionize first; voids are last to be reionized"
  - "IGM opacity is dominated by Lyman-limit systems, not continuous absorption; photon mean-free-path sets the scale of ionized bubbles"
related:
  - "[[Reionization Physics]]"
  - "[[Lyman Alpha Forest]]"
  - "[[Neutral Fraction]]"
  - "[[Ionization Morphology]]"
  - "[[21cm Cosmology]]"
  - "[[Inside-Out Reionization]]"
---

# Ferrara & Pandolfi (IGM Reionization)

> [!key-insight]
> A two-lecture course on the IGM and cosmic reionization covering the history of the Lyman-alpha forest, the physics of photoionization equilibrium, and the topology of HII regions — the essential observational and physical context for 21 cm work.

## Citation

Ferrara, A. & Pandolfi, S. "Reionization of the Intergalactic Medium." *Il Nuovo Cimento*, Vol. ?, N. ? (lecture notes, ~2013). Ferrara: Scuola Normale Superiore, Pisa; Pandolfi: Niels Bohr Institute, Copenhagen.

## Course Structure

**Lecture I: The Lyman-Alpha Forest and IGM Foundations** (~60 minutes)
- Historical context: Ly-α forest discovery and interpretation
- Physics of photoionization equilibrium
- Measuring neutral fractions from absorption spectra
- IGM thermal evolution and temperature measurements

**Lecture II: Cosmic Reionization Topology** (~60 minutes)
- Sources of ionizing radiation (stars vs. AGN vs. X-rays)
- Sinks: recombination and absorption in dense regions
- The ionization topology: inside-out vs. outside-in
- Observational probes during the reionization epoch
- Patchy reionization and 21 cm signal implications

## Core Claim

The IGM is the dominant baryon reservoir at high redshift. Its ionization and thermal state is set by the balance between UV/X-ray radiation from early galaxies and black holes, and recombinations in dense clumps. Understanding the Lyman-alpha forest — the IGM's primary observational tracer — is prerequisite to interpreting all other reionization observables including the 21 cm signal.

The **topology** of reionization (not just the global ionized fraction) is encoded in the large-scale structure: high-density peaks (where halos form) ionize first; low-density voids last. This "inside-out" picture is the paradigm supported by modern simulations and is fundamental to understanding EFT bias coefficients.

## Key Results

### Lecture I — IGM Physics and the Lyman-Alpha Forest

**Historical context:**
- **Gunn & Peterson (1965)**: Predicted that if the universe is mostly neutral ($x_\text{HI} \gtrsim 0.1$), quasar spectra would show a continuous trough of Lyman-alpha absorption blueward of the quasar's Lyman-alpha emission line (the "Gunn-Peterson trough")
- **Discovered at $z > 6$** (Becker et al. 2001; Fan et al. 2002): High-$z$ quasars DO show GP troughs, confirming that the universe transitions from neutral → ionized between $z \sim 6$ and $z \sim 5$
- **At lower redshift** ($z \sim 2$–5): Lyman-alpha forest shows discrete absorption features (individual neutral hydrogen clouds), not a continuous trough

**Lyman-alpha line formation:**
The Lyman-alpha transition ($n = 2 \to 1$, $\lambda = 121.6$ nm) is the **resonance line** of neutral hydrogen. Any neutral hydrogen absorbs strongly at this wavelength.

For a quasar with emission line at observed wavelength $\lambda_\text{obs}$:
- Blueward of $\lambda_\text{obs}$ (towards shorter wavelengths), we look at **lower redshifts**
- Each absorption feature at wavelength $\lambda < \lambda_\text{obs}$ corresponds to a cloud at redshift $z < z_\text{QSO}$
- The **transmitted flux** $F(\lambda) = e^{-\tau(\lambda)}$ where $\tau$ is the optical depth

**Optical depth evolution:**
$$\tau_\text{eff}(z) = \int_z^\infty \sigma_\text{HI}(\lambda) \, n_\text{HI}(z') \frac{dz'}{H(z')} \propto (1+z)^\gamma$$

with $\gamma \approx 2.7$ at $z < 6$. The mean transmitted flux evolves as:
$$\langle F(z) \rangle = e^{-\tau_\text{eff}(z)}$$

**The Gunn-Peterson saturation argument:**

In a fully neutral IGM ($x_\text{HI} \approx 1$), the optical depth would be **infinite** blueward of Lyman-alpha. But observations show:
- At $z \sim 6$: $\langle F \rangle \sim 0.1$–$0.2$ (some transmission remains)
- At $z \sim 5.5$–6: Transition from discrete features to continuous trough

This **cannot be explained** if $x_\text{HI}(z=6) \gg 0.1$. Instead:

$$x_\text{HI}(z=6) \sim 10^{-3} \text{ to } 10^{-4}$$

**Critical insight**: Even at the "end of reionization," the volume-averaged neutral fraction is tiny. The GP trough saturates well before the universe is fully neutral because Lyman-alpha absorption is so efficient.

**Consequences for reionization timeline:**
- Quasars at $z \sim 6$ exist in an **ionized universe**
- The universe was **substantially neutral only at $z > 7$–8**
- The reionization transition is **rapid** (over $\Delta z \sim 1$–2)

**IGM temperature evolution:**

Lyman-alpha lines have **width** set by thermal motions:
$$b = \sqrt{\frac{2k_B T}{m_\text{H}}} \approx 7 \text{ km/s} \sqrt{\frac{T}{10^4 \text{ K}}}$$

By measuring line widths, we infer **IGM temperature**.

- **During reionization** ($z \sim 6$–8): Photoionization heating by UV photons rapidly heats the IGM from $T \sim 100$ K to $T \sim 10,000$–$20,000$ K
- **Post-reionization** ($z < 5$): Temperature stabilizes at $T_0 \sim 7000$–$12,000$ K (at mean density)
- **Temperature-density relation**: $T(z) = T_0 \left[(1+\delta)/\bar{\rho}\right]^{\gamma - 1}$ where $\gamma \approx 1.4$–1.6 (measured from power-law fits to forest spectra)

**Pressure broadening and the Doppler broadening regime:**

The forest naturally breaks into two regimes:
1. **Linear/mildly-nonlinear**: Overdensities $1 < 1 + \delta < 10$; Doppler broadening dominates; lines are relatively narrow
2. **Saturated**: Overdensities $\delta > 10$; lines become so dense that only the Doppler wings are visible (saturated absorption)

This structure is crucial for EFT: the **nonlinear relationship** between density and neutral fraction (due to saturation) is encoded in the $b_2$ coefficient.

### Lecture II — Cosmic Reionization Topology

**Sources of ionizing photons:**

1. **Stellar UV** (main contributor):
   - Star-forming galaxies produce photons at $\nu > 13.6$ eV (Lyman-limit)
   - Ionizing photon production rate per solar mass per unit time: $\xi_\text{ion}$ (order-unity in Salpeter IMF)
   - Ionizing photons escape with efficiency $f_\text{esc}$ (measured to be 0.1–0.5 in observations)

2. **Active galactic nuclei (AGN)**:
   - Dominant at lower redshift ($z < 3$)
   - At high-$z$: subdominant but contribute 10–20% of ionizing photons
   - Harder spectra than stars (more X-rays); can ionize Helium

3. **X-ray binaries and shocks**:
   - Secondary ionizations from hard X-rays
   - Less constraining at reionization epoch but important for heating

**Sinks: Recombination and absorption**

1. **Case B recombination** (recombination to $n=2$ in atomic hydrogen):
   - Rate: $\alpha_B(T) \approx 2.6 \times 10^{-13} (T/10^4 \text{ K})^{-0.7}$ cm³ s⁻¹
   - Slower than Case A (which includes Lyman-alpha escape) but more realistic for optically thick IGM

2. **Lyman-limit systems** (optically thick neutral hydrogen):
   - Absorption of Lyman-continuum photons at $\lambda < 912$ Å (ionizing photons)
   - Cross-section: $\sigma_\text{LL}(\nu) = \sigma_0 (\nu / \nu_L)^{-3}$ (resonance, strong)
   - These systems **self-shield**: absorb photons preferentially, reducing ionization in their interior
   - Fraction of Lyman-limit absorbers: $n_\text{LL} \sim 0.1–0.5 \, (1+z)^2$ cm⁻³

3. **Clumpy recombination**:
   - Dense clumps have high recombination rates
   - Clumping factor $C = \langle n^2 \rangle / \langle n \rangle^2$ ranges from ~1 (smooth) to ~5–10 (clumpy)
   - Directly affects the ionization front speed

**Inside-out vs. outside-in topologies**

**Outside-in (discredited):**
- Ionize lowest-density regions first (smallest recombination sink)
- Voids ionize before peaks
- Predicted patchy reionization, but morphology doesn't match simulations

**Inside-out (supported by simulations and observations):**
- Ionize highest-density regions first (site of quasar and galaxy formation)
- Ionized bubbles nucleate around massive halos
- Bubbles expand and merge, eventually percolating across the universe
- Voids are ionized **last**, often by radiation leaking from neighboring bubbles
- This topology is a **direct consequence of source localization** (halos are biased to high-density regions) plus the tight relationship between source and ionized volume

**Evidence for inside-out:**

1. **Simulations**: Every modern radiative-transfer simulation shows inside-out topology (Iliev et al. 2006; Trac & Gnedin 2009; see [[Trac & Gnedin 2009 (Reionization Simulations)]])

2. **Patchy reionization observations**: Different high-$z$ quasars along the same line of sight show different GP trough properties, indicating that the ionization state is **spatially variable** and correlated with large-scale structure (inside-out would produce such patterns; outside-in would not)

3. **LAE clustering**: Lyman-alpha emitters show **enhanced clustering** during reionization, indicating they prefer ionized regions (which are preferentially in high-density peaks)

4. **21cm constraints** (forecasts): The 21cm power spectrum shows a characteristic **scale-dependent modulation** due to patchy reionization, with enhanced power at scales corresponding to ionized bubble sizes (~10–50 Mpc). This matches inside-out predictions.

**Mean free path and bubble size:**

The **mean free path of ionizing photons** is determined by Lyman-limit systems:
$$\lambda_\text{mfp} = \left[ n_\text{LL}(z) \, \sigma_\text{LL}(\nu) \right]^{-1} \sim 10\text{–}50 \text{ Mpc} \quad \text{(at } z \sim 7 \text{)}$$

Ionized bubbles grow to roughly the mean free path size before merging with neighbors. This sets the **characteristic scale** of patchy reionization.

In EFT language: the mean free path $R_\text{mfp}$ is a key parameter controlling the bubble size and hence the **scale dependence** of the EFT expansion. It controls the transition from the EFT-valid linear regime ($k \ll 1/R_\text{mfp}$) to the highly nonlinear regime ($k \gg 1/R_\text{mfp}$).

**Global ionization equation revisited:**

$$\frac{d Q_\text{HII}}{dt} = \left[ \frac{\dot{n}_\text{ion}}{\bar{n}_H} \right]_\text{sources} - \left[ \frac{C \alpha_B(T) \bar{n}_H (1+z)^3 x_\text{HII}}{1} \right]_\text{recombination}$$

The **ratio** of sources to sinks determines the ionization history:
- **Source-dominated** ($\dot{n}_\text{ion} \gg$ recombination): rapid ionization, fraction evolves sharply
- **Sink-dominated** (recombination grows): slower ionization, saturation plateau at $Q_\text{HII} < 1$

This competition is fundamental to reionization and is what [[Choudhury 2022 (Reionization Intro)]] derives from first principles.

**Patchy reionization during the EoR:**

At intermediate epochs ($z \sim 7$–8):
- Ionized fraction: $x_\text{HII} \sim 0.2$–0.8
- Morphology: Discrete ionized bubbles with size ~10–30 Mpc, surrounded by neutral gas
- Fluctuations: Ionization field has large spatial variance
- Observable signature: 21cm power spectrum shows **excess power** at scales matching bubble sizes (e.g., $k \sim 0.1$–$0.3$ Mpc⁻¹)

**Observational probes summary**

| Probe | Redshift range | What it measures | Limitation |
|-------|----------------|-----------------|-----------|
| Lyman-alpha forest | $z = 2$–6 | Mean $n_\text{HI}$, temperature | Not sensitive to $x_\text{HI} \ll 10^{-3}$ |
| Gunn-Peterson trough | $z > 6$ | Mean $x_\text{HI}$ | Only sensitive to very high neutral fractions; saturates early |
| LAE clustering & number | $z = 5$–7 | Ionized bubble size/distribution | Limited by available sources; luminosity bias |
| 21 cm signal | $z = 6$–15 | Ionization morphology, power spectrum | Requires 21 cm telescopes (SKA, HERA) |
| CMB polarization (Planck) | Integrated over all $z$ | Reionization optical depth $\tau_e$ | Only constrains history, not morphology |

## Methods

**Pedagogical approach:**
- Derives photoionization equilibrium, recombination, and IGM temperature from first principles
- Reviews both analytical models and observational constraints
- Uses observational data to motivate physical models (inverse approach: data → physics)
- 53 pages, written for an advanced graduate audience (assumes GR + particle physics basics)

**Key derivations:**
- Photoionization rate $\Gamma$ as a function of UV spectrum and column density
- Equilibrium neutral fraction including secondary ionizations
- Temperature evolution with heating and cooling
- Optical depth calculations for various absorption systems

## Key Equations

**Photoionization equilibrium** (balance between ionization and recombination):
$$n_\text{HI}\,\Gamma_\text{HI} = n_e\,n_\text{HII}\,\alpha_B(T)$$

Rearranging:
$$x_\text{HI} = \frac{\Gamma_\text{HI}}{\Gamma_\text{HI} + \alpha_B(T) n_e}$$

**Photoionization rate** (integral over all ionizing photons):
$$\Gamma_\text{HI}(z) = \int_{\nu_\text{LL}}^\infty \frac{\sigma_\text{HI}(\nu)}{h\nu} \, J_\nu(z) \, d\nu$$

where $J_\nu$ is the specific intensity of radiation.

**Mean-free-path attenuation** (photons are absorbed by Lyman-limit systems):
$$J_\nu(x, z) = J_\nu^0(z) \, e^{-\tau_\text{LL}(x,z)}$$

where $\tau_\text{LL}$ is the optical depth due to Lyman-limit absorbers along the line of sight.

**Gunn-Peterson optical depth**:
$$\tau_\text{GP}(z) = \sigma_\text{HI}(\nu_\text{Ly}) \int_z^\infty \frac{n_\text{HI}(z')}{H(z')} dz' = \sigma_\text{HI} n_\text{HI} \chi(z)$$

where $\chi(z)$ is the comoving distance to redshift $z$.

**Transmitted flux** (observable):
$$F(z) = e^{-\tau_\text{GP}(z)}$$

**Temperature-density relation** (from spectral measurements):
$$T(z, \delta) = T_0(z) \left[1 + \delta(z)\right]^{\gamma - 1}$$

with $\gamma \approx 1.4$–1.6 (measured).

## Connection to This Thesis

### Relevance to P1 (EFT bias measurements)

**Direct relevance:**

1. **Ionization topology**: The "inside-out" picture described here IS the physics underlying the [[EFT Bias]] coefficients.
   - The $b_1^x$ term captures linear density-ionization correlation
   - The $b_2^x$ term captures the **nonlinear saturation** effect (dense regions ionize more efficiently than linear growth would suggest)
   - The $b_{\nabla^2}^x$ term captures **streaming effects** (ionized bubbles smooth small-scale density fluctuations)

2. **Clumping factor $C$**: This review emphasizes the role of clumpy recombination. Different simulators (21cmFAST, SCRIPT) may model $C$ differently:
   - 21cmFAST: often uses a **simple model** $C(z)$ (e.g., evolving as $(1+z)^\alpha$)
   - SCRIPT or full RT: may compute $C$ dynamically from the density field
   - This is a **primary source of simulator dependence** in EFT coefficients (P1's core question)

3. **Mean free path**: Ferrara & Pandolfi emphasize the mean-free-path scale as the characteristic bubble size. This is precisely the scale that controls the **scale dependence** of EFT:
   - For $k \ll 1/R_\text{mfp}$: EFT should be valid (smooth structure)
   - For $k \gg 1/R_\text{mfp}$: EFT breaks down (bubble edges matter)
   - The mean free path is a **tunable parameter** ($R_\text{mfp}$ in 21cmFAST); different codes may set it differently

### Relevance to P2 (EFT-based parameter inference)

**Indirect but crucial:**
- The sources (escape fraction $f_\text{esc}$, stellar mass fraction $f_*$) and sinks (clumping $C$, Lyman-limit absorption, minimum mass $M_\text{min}$ or equivalently $T_\text{vir}$) that P2 infers as native parameters are all discussed here
- The **inside-out topology** means that the ionization field **inherits the bias** of the matter field (halos live in high-density regions)
- This is the physical justification for why P2 expects the EFT coefficients to be **relatively universal** (captured by the underlying source/sink physics) even if native parameters differ slightly across codes

### Supports / contradicts

- **Complements**: [[Choudhury 2022 (Reionization Intro)]] — Choudhury is more theoretical/bottom-up (photon budget); Ferrara & Pandolfi more observational/phenomenological (forest, quasars, topology)
- **Validates**: [[Trac & Gnedin 2009 (Reionization Simulations)]] — RT simulation results confirming inside-out topology
- **Provides context for**: [[McQuinn & D'Aloisio 2018]] EFT expansion (the physics of the ionization field that EFT describes is outlined here)

## Limitations and Caveats

**What this review does NOT cover in detail:**

1. **AGN feedback and ionization**: AGN contribution to ionizing photons mentioned but not quantified. Impact on thermal state and reionization history not fully developed.

2. **Helium reionization**: Follows Hydrogen reionization; briefly mentioned but not discussed. Important for understanding Ly-α forest at $z < 3$.

3. **Metal-enriched IGM**: Metallicity evolution, metal cooling, metal-line absorption not covered. Important at $z < 5$ but not primary for understanding Hydrogen reionization.

4. **Radiative transfer in detail**: The mean-field approach assumes photons propagate freely except for absorption. Focuses on sources and sinks, not the actual RT algorithm.

5. **21 cm signal theory**: Noted as observable but not derived. [[Mesinger 2016]] and [[Maselli & Ferrara 2016]] provide better coverage of spin temperature and power spectrum.

**Assumptions that may break:**

1. **Local equilibrium assumption**: Assumes photoionization equilibrium is reached at each point (timescale faster than ionization front propagation). May fail near ionization fronts.

2. **Constant mean free path**: Assumes $\lambda_\text{mfp}$ is constant in space and time. Actually depends on density, source spectrum, and prior ionization state.

3. **Salpeter IMF**: Assumes top-heavy stellar IMF (needed for ionizing photon yield). Real star formation may have different IMF, affecting photon budget.

4. **Homogeneous escape fraction**: Assumes $f_\text{esc}$ is uniform. Real galaxies show mass and redshift dependence (possibly related to halo feedback).

## Figures and Pedagogical Value

This is a pedagogical work. Key figures include:
- **High-$z$ quasar spectra** at $z = 5$–7 showing Gunn-Peterson troughs
- **IGM opacity evolution** vs. redshift (mean free path, clumping factor)
- **Ionization topology** (snapshots of inside-out reionization in simulations)
- **Lyman-alpha forest** column density distribution at different redshifts

## Open Questions After Reading

> [!gap]
> **Inside-out mapping to EFT**: The lectures emphasize inside-out topology but don't quantify how this maps to EFT coefficients. Specifically: if a region is "ionized second" (lower density than average), does that mean it contributes negatively to $b_1^x$? How does the ionization bias evolve during the EoR?

> [!gap]
> **Clumping factor in different codes**: The review states that clumping is poorly constrained, varying by a factor 2–3 across simulations. Does P1 find that differences in clumping modeling are the dominant source of EFT coefficient variation?

> [!gap]
> **Mean free path as a key parameter**: If $R_\text{mfp}$ is the scale that sets the EFT regime (small-$k$ where EFT is valid), can P1 and P2 extract $R_\text{mfp}$ from the EFT coefficients by inverting the measurement?

> [!gap]
> **Patchy reionization morphology**: At what neutral fraction does the inside-out topology produce the largest 21cm power spectrum features? Does this correspond to the epoch when the EFT bias coefficients are largest?
