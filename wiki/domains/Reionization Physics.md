---
type: domain
title: "Reionization Physics"
created: 2026-04-14
updated: 2026-04-16
tags:
  - domain/reionization
  - domain/cosmology
status: mature
related:
  - "[[21cm Cosmology]]"
  - "[[Effective Field Theory]]"
  - "[[Simulation and Codes]]"
---

# Reionization Physics

## What It Is: The Epoch of Reionization (EoR)

The **Epoch of Reionization (EoR)** is the period in cosmic history when the first stars and galaxies produced enough ionizing (UV) photons to reionize the neutral hydrogen that had filled the Universe since recombination. The reionization history determines the large-scale structure of the 21 cm signal during $z \sim 6$-$30$ and encodes crucial information about early star formation and galaxy physics.

- **Recombination:** At $z = 1089$ (age ~380,000 years), the Universe cooled to ~3000 K; free electrons and protons combined to form neutral hydrogen
- **Dark Ages:** From $z \sim 1089$ to $z \sim 30$, the universe remained neutral; no stars, only dark matter
- **First stars (Cosmic Dawn):** Around $z \sim 20$-$30$, the first Population III stars form in collapsed dark matter halos
- **Reionization era:** $z \sim 6$-$20$, ionizing photons gradually ionize the universe
- **Completion:** By $z \lesssim 6$ (from Ly$\alpha$ forest saturation), the universe is mostly ionized

**The observable:** The 21 cm signal directly images the distribution of neutral hydrogen as it gets ionized, providing a 3D tomographic picture of this crucial epoch.

## The Reionization Sequence: Topology and Morphology

Reionization does not happen uniformly across space. Instead, it follows a characteristic **inside-out** topology:

### Detailed Timeline

1. **$z \sim 30$ (cosmic time ~70 million years):** First stars ignite in dense regions. Ionizing photons escape into the surrounding IGM.

2. **$z \sim 15$-$20$ (cosmic time ~150-300 million years):** Small isolated ionized bubbles form around the first clusters of sources. Because of Jeans instability and the halo mass function, sources cluster preferentially in overdense regions. Thus, overdense regions get ionized **first** (inside-out topology).

3. **$z \sim 10$-$15$ (cosmic time ~350-600 million years):** Bubbles grow and begin to overlap. The ionized volume fraction increases roughly as $Q_\text{HII}(z)$ (the volume-filling fraction of HII regions). The topology transitions from isolated bubbles to connected networks.

4. **$z \sim 7$-$10$ (cosmic time ~600-900 million years):** **Percolation transition.** When roughly 50% of the volume is ionized, ionized regions form a connected network spanning the universe. The percolation transition is a phase transition in statistical physics—the topological structure changes qualitatively.

5. **$z \sim 6$ (cosmic time ~1 billion years):** Reionization essentially complete. Final neutral fraction $\bar{x}_\text{HI} < 10^{-3}$ from Ly$\alpha$ forest measurements.

### The Inside-Out Topology

The "inside-out" picture is confirmed by both semi-numerical simulations and full radiative transfer codes. Physically:

- **Source clustering:** Stars form preferentially in overdense regions. The halo mass function is biased such that massive (star-forming) halos cluster more strongly than the average mass.
- **Ionization follows sources:** Because photon mean free paths are finite (~10-50 Mpc), ionization extends from sources over a characteristic distance. Regions near many sources are ionized first.
- **Result:** Overdense regions ionize first; underdense regions (voids) are ionized last.

This is opposite to matter formation (where voids expand and grow first), making reionization topology uniquely informative about source properties.

## The Photon Budget: Detailed Derivation

The **global reionization history** is governed by the competition between ionizing photon production from stars and photon consumption by recombinations. The key governing equation is:

$$
\frac{dQ_\text{HII}}{dt} = \frac{\dot{n}_\text{ion}}{\bar{n}_H} - \frac{C\,\alpha_B(T)\,\bar{n}_H\,Q_\text{HII}}{H(z)(1+z)}
$$

where:

- $Q_\text{HII}(z)$ is the **volume-filling fraction of ionized regions:** 0 if fully neutral, 1 if fully ionized
- $\dot{n}_\text{ion}$ is the **ionizing photon emissivity** (photons per unit volume per unit time)
- $\bar{n}_H$ is the mean hydrogen number density
- $C = \langle n_e^2 \rangle / \langle n_e \rangle^2$ is the **clumping factor** (how density fluctuations enhance recombinations)
- $\alpha_B(T)$ is the **Case B recombination coefficient** (includes both direct recombination and excited-state cascades)
- $H(z)$ is the Hubble parameter; the denominator includes the expansion factor $(1+z)$

### Deriving the Photon Budget from First Principles

Starting from rate equations for neutral and ionized regions:

**Production (ionization):**
A photon produced at position $\mathbf{r}_s$ travels a distance $\lambda_\text{mfp}$ (mean free path) before being absorbed by a neutral H atom, ionizing it. The volume ionized by a single photon is roughly $\sim \lambda_\text{mfp}^3$. The number density of ionizing photons produced is:

$$
n_\text{ion}(\mathbf{x}, z) = \int_{\text{sources}} f_\text{esc}(\mathbf{x}_s) \, N_\gamma \, \dot{\rho}_*(\mathbf{x}_s, z) \, P(\mathbf{x}_s \to \mathbf{x}) \, d^3 x_s
$$

where:
- $f_\text{esc}$ is the escape fraction (fraction of photons escaping the galaxy)
- $N_\gamma$ is the number of photons per stellar baryon
- $\dot{\rho}_*$ is the star formation rate density
- $P(\mathbf{x}_s \to \mathbf{x})$ is the probability a photon reaches from $\mathbf{x}_s$ to $\mathbf{x}$

Integrating over all sources and averaging over space gives the global emissivity:

$$
\dot{n}_\text{ion} = f_\text{esc} \, N_\gamma \, \dot{\rho}_*
$$

**Consumption (recombinations):**
Ionized regions recombine when free electrons and protons collide. The recombination rate depends on density squared (two particles must meet):

$$
\text{Recombination rate} \sim \alpha_B(T) \, n_e \, n_p
$$

In ionized regions, $n_e = n_p$ (charge neutrality), so:

$$
\text{Recombination rate} \sim \alpha_B(T) \, n_e^2
$$

Integrating over space, the global recombination rate is:

$$
\text{Recombination rate} = \alpha_B(T) \, \bar{n}_H^2 \, C \, Q_\text{HII}
$$

where the factor $C = \langle n_e^2 \rangle / \langle n_e \rangle^2$ accounts for density clumping (high-density regions recombine faster).

**Combining:** The net rate of ionization is:

$$
\frac{dQ_\text{HII}}{dt} = \frac{\dot{n}_\text{ion}}{\bar{n}_H} - \alpha_B(T) \, \bar{n}_H \, C \, Q_\text{HII}
$$

This is the standard reionization equation used in all semi-numerical codes.

## Sources of Ionizing Photons

### Stars Dominate the Ionizing Photon Budget

**Stellar contribution:** Young, massive stars (O and early B stars) produce ionizing photons. The number of photons per stellar baryon is $N_\gamma \sim 1000$ (depends on IMF and stellar population synthesis).

The integrated stellar photon production easily exceeds what is needed to reionize the universe if escape fraction is sufficient ($f_\text{esc} \sim 10-20\%$).

### AGN/Quasars Are Subdominant

Quasars (active galactic nuclei in massive black holes) are often considered as alternative ionizing sources.

**Why AGN cannot reionize the universe alone:**
- Number density: Quasars are rare; the space density of quasars at $z \sim 6$ is $\phi_Q(z) \sim 10^{-6}$ Mpc$^{-3}$ (c.f. star-forming galaxies at $10^{-2}$ Mpc$^{-3}$)
- Ionizing output: While individual quasars are luminous, their total integrated ionizing photon output is ~100× **less** than stars
- Direct evidence: If quasars reionized the universe, the ionized fraction would jump suddenly as each new quasar ignites. Instead, observations show a smooth reionization history.

**AGN do contribute to:**
- **Early heating:** X-ray emission from AGN heats the IGM
- **He reionization:** Harder photons from AGN may contribute to He II reionization at $z \sim 3$
- **Proximity zone physics:** Quasar vicinity has enhanced ionization (proximity zones in quasar spectra)

But **stars are the dominant ionizing source during the main EoR.**

### X-ray Binaries and Other Sources

X-ray binaries and other compact objects produce X-rays, which:
- Ionize hydrogen and helium indirectly (creating secondary ionizations)
- Heat the IGM (critical for the Ly$\alpha$ forest observations)
- Probably subdominant to stellar ionization in terms of photon budget

## The Photon Budget Sinks: Recombinations and Absorption

### Sink 1: Recombinations in the Diffuse IGM

Once an HII region forms, it is constantly eroded by recombinations:

$$
n_e^- \, n_p \, \alpha_B(T) \, \text{rate} \propto n_e^2
$$

This is **density-dependent:** high-density regions recombine faster. The clumping factor $C$ parameterizes this:

$$
C(z) = \frac{\langle n_e^2 \rangle}{\langle n_e \rangle^2}
$$

- **Early universe ($z \sim 100$):** Nearly uniform density, $C \sim 1-2$
- **Well into reionization ($z \sim 6$):** Density contrasts are large, $C \sim 5-30$

The clumping factor evolution is one of the **most uncertain** inputs to the photon budget—semi-numerical codes must adopt it from simulations or observational constraints.

### Sink 2: Lyman-Limit Systems (LLS)

**Lyman-limit systems** are optically thick absorbers with HI column density $N_\text{HI} > 10^{17}$ cm$^{-2}$. They:

- Are partially ionized during reionization (but not fully transparent)
- Absorb a significant fraction of ionizing photons
- Set the effective photon mean free path $\lambda_\text{mfp}$

The mean free path is determined by:

$$
\lambda_\text{mfp}^{-1} = \int_{N_\text{HI} > 10^{17}}^{\infty} \sigma_\text{abs}(N_\text{HI}) \, n_\text{LLS}(N_\text{HI}) \, dN_\text{HI}
$$

where $\sigma_\text{abs}$ is the absorption cross-section and $n_\text{LLS}$ is the comoving number density of systems at each column density.

The **mean free path evolution** is another critical input:
- At $z \sim 12$ (early EoR): $\lambda_\text{mfp} \sim 10-20$ Mpc (many LLS, photons don't travel far)
- At $z \sim 6$ (late EoR): $\lambda_\text{mfp} \sim 50-100$ Mpc (LLS depleted, photons travel farther)

Different codes estimate $\lambda_\text{mfp}$ differently, leading to different effective bubble size distributions and thus different $b_{\nabla^2}^x$ coefficients.

## The Halo Mass Function and Star Formation

Sources of ionizing photons live inside dark matter halos. The **halo mass function** $n(M, z)$ — the comoving number density of halos per unit mass — determines the source density.

### Press-Schechter Formula

The simplest analytic prediction is the **Press-Schechter formula:**

$$
n(M, z) dM = \frac{\bar{\rho}_m}{M^2} \left| \frac{d \ln \sigma(M)}{dM} \right| \sqrt{\frac{2}{\pi}} \frac{\delta_c(z)}{\sigma(M)} \exp \left( -\frac{\delta_c^2(z)}{2\sigma^2(M)} \right) dM
$$

where:
- $\sigma(M)$ is the RMS density fluctuation on a scale of mass $M$
- $\delta_c(z) \approx 1.686$ is the linearly-extrapolated overdensity threshold for collapse
- The derivative w.r.t. $M$ captures the abundance of critical peaks

**Strengths:** Simple; connects to Gaussian random fields and peak statistics  
**Weaknesses:** Underestimates high-mass halos by ~30-50%; no ellipsoidal collapse correction

### Sheth-Tormen Formula (Improved)

The **Sheth-Tormen formula** improves on Press-Schechter by accounting for ellipsoidal collapse:

$$
n(M, z) dM = 0.353 \, \bar{\rho}_m / M^2 \, f_\text{ST}(\nu) \left| \frac{d \ln \sigma(M)}{dM} \right| dM
$$

with $\nu = \delta_c / \sigma(M)$ and

$$
f_\text{ST}(\nu) = A \left[ 1 + \left(\frac{\nu^2}{a}\right)^p \right] e^{-b\nu^2}
$$

with parameters $A = 0.353$, $a = 0.73$, $b = 0.175$, $p = 0.3$ (or similar; varies slightly by reference).

This matches N-body simulations much better than Press-Schechter, especially at $M \gtrsim 10^{10} M_\odot$.

### The Collapsed Fraction

The **collapsed fraction** $f_\text{coll}(M_\text{min}, z)$ is the total fraction of matter in halos above a minimum mass $M_\text{min}$:

$$
f_\text{coll}(M_\text{min}, z) = \int_{M_\text{min}}^{\infty} \frac{n(M, z) M}{\bar{\rho}_m} dM
$$

This is the key input to semi-numerical codes like 21cmFAST: the star formation rate density is proportional to $f_\text{coll}$, and thus the ionizing photon emissivity scales with $f_\text{coll}$.

## Cooling and the Minimum Halo Mass Threshold

Not all halos can form stars. Gas must be able to cool below the virial temperature to become dense enough for star formation.

### Atomic Cooling Floor

Hydrogen and helium cool efficiently via collisional excitation/de-excitation when:

$$
T_\text{vir} \gtrsim 10^4 \text{ K}
$$

This corresponds to a **virial mass** of:

$$
M_\text{vir} = \frac{3}{10} \frac{v^2_\text{c}}{G} = \frac{3}{10} \left[ \frac{3 G M}{R} \right] = \frac{3}{10} (k_B T_\text{vir}) / \mu_e = 10^8 M_\odot
$$

(exact value depends on cosmology and redshift; the above is approximate)

Above $T_\text{vir} = 10^4$ K, atomic cooling is efficient; below it, cooling is slow.

### Molecular Cooling and Lyman-Werner Feedback

H$_2$ (molecular hydrogen) enables cooling to much lower temperatures:

$$
T_\text{vir} \sim 500 \text{ K} \implies M_\text{vir} \sim 10^6 M_\odot
$$

Thus, if $\text{H}_2$ is present, galaxies can form in much smaller halos.

**However:** Lyman-Werner photons (11.26-13.6 eV) dissociate $\text{H}_2$:

$$
\text{H}_2 + \gamma_\text{LW} \to 2 \text{H} \text{ (dissociation)}
$$

The Lyman-Werner photon background is produced by young stars (the same ones producing ionizing photons). As the universe becomes ionized, the Lyman-Werner background increases, suppressing $\text{H}_2$ cooling.

The **net effect:** 
- **Early reionization ($z \sim 20$, before much star formation):** $\text{H}_2$ cooling allows star formation in $10^6 M_\odot$ halos
- **Late reionization ($z \sim 8$, heavy star formation):** Strong Lyman-Werner background suppresses $\text{H}_2$ cooling; only $10^8 M_\odot$ halos form stars efficiently
- **Result:** The effective minimum halo mass **increases with decreasing redshift** during reionization (a "photochemical feedback")

**The simulation parameter $T_\text{vir}$** encodes this physics: it sets the minimum halo mass for star formation via $M_\text{min} \propto T_\text{vir}$. Different models of Lyman-Werner feedback produce different $T_\text{vir}(z)$ evolutions, leading to different source biases and thus different $b_1^x(z)$.

## Key Physical Processes in the Ionization Field

### Spin Temperature ($T_S$) and the 21cm Signal Limit

The 21 cm line is produced by a transition between the parallel-spin and anti-parallel-spin states of hydrogen. The transition probabilities depend on the **spin temperature** $T_S$, which is **not** the same as the kinetic temperature $T_K$ of the gas.

In the **saturated spin-temperature limit** ($T_S \gg T_\text{CMB} \approx 2.7(1+z)$ K), the 21 cm signal is independent of $T_S$ and depends only on the neutral fraction and density. This limit is valid for:

$$
x_\text{HI}(z) \cdot \left[ 1 - \exp(-\tau_\text{21}) \right] \approx x_\text{HI}(z)
$$

which is true at high-$z$ where neutral fractions are large or when Ly$\alpha$ collisional coupling is strong.

**When this breaks down:** At very early times ($z > 20$) before sufficient Ly$\alpha$ photons are produced, $T_S$ can approach the CMB temperature, and the signal can be **negative** (absorption rather than emission). This is the signature of the Cosmic Dawn 21cm signal that experiments like EDGES are searching for.

**This thesis assumes $T_S \gg T_\text{CMB}$ throughout**, which is justified for the bulk of reionization ($z < 15$) after the first stars have had time to produce Ly$\alpha$ photons.

### Recombinations: In-Bubble and Sub-Grid

Recombinations operate on two scales:

1. **In-bubble recombinations (modeled):** Explicit recombination of free electrons and protons in the diffuse IGM, parametrized by the clumping factor $C$.

2. **Sub-grid recombinations:** In partially ionized cells (especially at the ionization front), exact equilibrium between ionization and recombination is complex. Semi-numerical codes use approximate prescriptions.

Different codes implement sub-grid recombinations differently, contributing to simulator dependence in the stochastic term $P_{\varepsilon\varepsilon}$.

### Gunn-Peterson Effect and Observational Limits

The **Gunn-Peterson trough** is the absorption of QSO light at wavelengths blueward of the Ly$\alpha$ line, caused by neutral hydrogen in the line of sight:

$$
\tau_\text{GP} = \sigma_\alpha \, n_\text{HI} \, \int dz
$$

where $\sigma_\alpha$ is the Ly$\alpha$ cross-section.

For a nearly neutral IGM with $\bar{x}_\text{HI} \sim 0.1$, even this modest neutral fraction produces $\tau_\text{GP} \gg 1$, saturating the Ly$\alpha$ absorption and creating the Gunn-Peterson trough.

**Observational finding:** Gunn-Peterson troughs appear suddenly at $z \gtrsim 6$ in QSO spectra. This is interpreted as the transition from mostly neutral ($z > 6$) to mostly ionized ($z < 6$).

**Important caveat:** The GP effect is extremely sensitive to rare regions of high $\bar{x}_\text{HI}$ and does not directly constrain the neutral fraction in other regions. Thus, even though the GP effect indicates the **end of reionization** is around $z \sim 6$, it says little about the ionization state during most of reionization ($z \sim 6-15$).

### IGM Temperature Evolution

The IGM is heated by ionizing photon absorption (photoionization) and later cooled by adiabatic expansion:

- **Before reionization ($z > 12$):** IGM at mean density is relatively cool, $T_K \sim 100$ K (determined by recombination heating from previous epochs)
- **During hydrogen reionization:** When an HII region forms, the gas is **flash-heated** to $T \sim 15,000$–$20,000$ K by UV radiation pressure
- **After reionization ($z < 6$):** IGM at mean density cools to $T \sim 7,000$–$12,000$ K by adiabatic expansion and inverse Compton cooling
- **The Ly$\alpha$ forest:** Shows temperature evolution via line-width measurements; current constraints suggest $T_0(z=2.5) \sim 9,000$–$15,000$ K

The temperature evolution affects the Ly$\alpha$ forest observations and is a consistency check on reionization models.

## Ionization Topology: Morphology and Structure

The spatial structure of reionization is **inside-out**: biased, dense regions near clustered sources ionize first; voids are last. This has observable consequences:

- **Early reionization ($\bar{x}_\text{HII} \sim 0.1$):** Small isolated bubbles, highly clustered. The 21 cm signal shows bright ionized regions (source-dominated) surrounded by dark neutral regions.
- **Mid reionization ($\bar{x}_\text{HII} \sim 0.5$):** Large bubbles overlapping; percolation transition. Complex topology with filaments and voids.
- **Late reionization ($\bar{x}_\text{HII} \sim 0.9$):** Most regions ionized; residual neutral fraction concentrated in voids and dense regions.

The **bubble size distribution** is captured by the EFT coefficient $b_{\nabla^2}^x \propto R_\text{eff}^2$. Different simulators produce different bubble-size distributions due to different ionization algorithms, leading to different $b_{\nabla^2}^x$ values at fixed $\bar{x}_\text{HII}(z)$.

## The EFT Connection

On scales larger than the characteristic bubble size, the ionization field can be expanded in the EFT basis (see [[Effective Field Theory]]). The physical inputs from reionization physics that determine EFT coefficients:

- **$b_1^x(z)$** ← source bias (determined by $T_\text{vir}$, halo mass function) + mean ionized fraction $\bar{x}_\text{HII}(z)$
- **$b_2^x(z)$** ← source quadratic bias + patchy coupling of radiation field to opacity fluctuations
- **$b_{\nabla^2}^x(z)$** ← effective bubble radius $R_\text{eff}(z)$ (determined by $R_\text{mfp}$ and source clustering)
- **$P_{\varepsilon\varepsilon}(k,z)$** ← bubble discreteness, recombination stochasticity, sub-grid source shot noise

## Key Parameters in Simulation Models

These are the astrophysical parameters that inference aims to constrain:

| Parameter | Symbol | Physical meaning | Typical range |
|-----------|--------|-----------------|---|
| **Ionizing efficiency** | $\zeta$ | Photons per baryon; combines $f_\text{esc}$, IMF, SFE | 10–100 |
| **Virial temperature** | $T_\text{vir}$ | Min. halo temperature for star formation; sets $M_\text{min}$ | $10^4$–$5×10^4$ K |
| **Mean free path** | $R_\text{mfp}$ | Distance ionizing photons travel before absorption | 10–100 Mpc |
| **Clumping factor** | $C$ | Sub-grid recombination enhancement | 2–30 |
| **Escape fraction** | $f_\text{esc}$ | Fraction of ionizing photons escaping galaxies | 0.01–0.5 |
| **Star formation efficiency** | $f_*$ | Fraction of baryons in stars; often implicit in $\zeta$ | 0.01–0.1 |

The **first three** ($\zeta$, $T_\text{vir}$, $R_\text{mfp}$) are the primary targets of 21cm inference; the latter are typically fixed or marginalized over.

## Observational Probes of Reionization

Different observations constrain different aspects:

| Probe | Observable | Physical constraint | Reference |
|-------|-----------|-------------------|-----------|
| **Lyman-α forest** | Transmitted flux vs. wavenumber | $\bar{x}_\text{HI}$ at $z \lesssim 6$ (reaches saturation) | [[Ferrara & Pandolfi (IGM Reionization)]] |
| **Quasar GP trough** | Absorption redward of Ly$\alpha$ | Indicates $z \gtrsim 6$ as reionization end; not precise | [[Ferrara & Pandolfi (IGM Reionization)]] |
| **CMB optical depth** | $\tau_e \approx \int \bar{x}_\text{HII} \, dt$ | Integrated ionization history; low-$z$ sensitive | [[Choudhury 2022 (Reionization Intro)]] |
| **Ly$\alpha$ emitters** | Ly$\alpha$ luminosity function evolution | $\bar{x}_\text{HI}(z)$ + source properties | [[Choudhury 2022 (Reionization Intro)]] |
| **21cm power spectrum** | $P_{21}(k, z)$ + higher moments | Bubble morphology + EFT coefficients; direct probe | [[21cm Cosmology]] |

21 cm observations are unique because they **directly image** the ionization field, rather than inferring it from indirect observables.

## Key Concepts

- [[Neutral Fraction]]
- [[Ionization Morphology]]
- [[Bubble Size Distribution]]
- [[Mean Free Path]]
- [[Excursion Set Formalism]]
- [[Clumping Factor]]
- [[Lyman Alpha Forest]]
- [[Spin Temperature]]
- [[Recombinations]]
- [[Halo Mass Function]]
- [[Inside-Out Reionization]]

## Key Entities

- [[21cmFAST]] — primary semi-numerical code for P1
- [[SCRIPT]] — second code for P1 comparison
- [[THESAN]] — full radiative transfer; ground truth for validation

## Foundational Background Papers

- [[Choudhury 2022 (Reionization Intro)]] — Pedagogical review; halo mass functions, photon budget, global reionization equation; **foundational background for entire thesis**
- [[Ferrara & Pandolfi (IGM Reionization)]] — Two-lecture overview; IGM physics, Lyman-alpha forest, GP effect, ionization topology; observational context
- [[Mesinger 2016]] — EoR review book (ed. Mesinger); Furlanetto chapter on 21cm pedagogy is standard reference
- [[Trac & Gnedin 2009 (Reionization Simulations)]] — RT simulations; sources vs sinks; photon budget; why quasars cannot reionize
- [[Gnedin & Madau 2022 (Modeling Reionization)]] — IGM physics formalism; photoionization, heating, clumping; complete taxonomy of reionization codes

## Sources

- [[Choudhury 2022 (Reionization Intro)]]
- [[Ferrara & Pandolfi (IGM Reionization)]]
- [[Mesinger 2016]]
- [[Trac & Gnedin 2009 (Reionization Simulations)]]
- [[Gnedin & Madau 2022 (Modeling Reionization)]]
