---
type: source
title: "Gnedin & Madau 2022 (Modeling Reionization)"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/simulation
  - domain/reionization
  - source/review
status: mature
source_type: paper
author:
  - "[[Gnedin, Nickolay Y.]]"
  - "[[Madau, Piero]]"
date_published: 2022
url: ""
confidence: high
key_claims:
  - "Comprehensive taxonomy of all reionization simulation types: semi-numerical (21cmFAST, ARTIST, AMBER), DMO+SAM (ASTRAEUS, DRAGONS), partially coupled, and fully coupled"
  - "No single code captures all relevant physics — trade-off between speed/volume and physical fidelity is fundamental"
  - "Semi-numerical codes reproduce global reionization history well but can misrepresent small-scale morphology compared to full RT"
  - "21cmFAST and SCRIPT use excursion-set formalism; differs from radiative transfer codes in how ionization bubbles are assigned"
related:
  - "[[Simulation and Codes]]"
  - "[[Radiative Transfer]]"
  - "[[Reionization Physics]]"
  - "[[Excursion Set Formalism]]"
  - "[[21cmFAST]]"
  - "[[SCRIPT]]"
  - "[[Trac & Gnedin 2009 (Reionization Simulations)]]"
---

# Gnedin & Madau 2022 (Modeling Reionization)

> [!key-insight]
> The definitive modern taxonomy of reionization simulation methods — from the underlying IGM physics through every class of numerical model — serving as a comprehensive road map for the field entering the SKA era.

## Citation

Gnedin, N. Y. & Madau, P. (2022). "Modeling Cosmic Reionization." *Springer Nature* (review). Fermilab / Kavli UCHICAGO / UCSB.

## Core Claim

Simulating cosmic reionization requires tracking the coupled evolution of dark matter, gas thermodynamics, star formation, and the radiative transfer of ionizing photons across cosmological volumes. No current code does all of this self-consistently at adequate resolution; the field has developed a spectrum of approximations, each capturing different aspects of the physics at the cost of others.

This review systematically maps the **trade-space** between:
- **Computational speed** (minutes to weeks per simulation)
- **Simulation volume** (100 Mpc to >1 Gpc)
- **Physical fidelity** (analytical models to fully coupled hydro+RT)
- **What physics is captured** (global history, morphology, feedback effects)

## Pedagogical Framework

The review structures reionization modeling as a sequence of increasingly realistic models, each solving a subset of the full physics:

1. **Analytical models** → understand scaling laws and basic physics
2. **Semi-analytical models** → add halo mass functions and excursion sets
3. **Semi-numerical codes** → add density field evolution
4. **DMO + SAM** → couple N-body dark matter to semi-analytic star formation
5. **Partially coupled** → add simplified radiative transfer
6. **Fully coupled** → hydro + RT + star formation (gold standard, small volumes)

This hierarchy makes it clear why different codes are used for different science questions.

## Key Results

### Section 2: IGM Physics and Radiative Transfer

**Photoionization rate** (integral definition):

$$\Gamma_\text{HI}(z, \mathbf{x}) = 4\pi \int_{\nu_\text{LL}}^\infty \frac{\sigma_\text{HI}(\nu)}{h\nu} J_\nu(z, \mathbf{x}) \, d\nu$$

where:
- $\sigma_\text{HI}(\nu)$ is the photoionization cross-section (resonance peak near Lyman limit, then power law)
- $J_\nu$ is the mean intensity of radiation at frequency $\nu$
- The integral runs over all ionizing frequencies (above 13.6 eV)

**Gas temperature evolution during reionization:**

During the EoR, photoionization **rapidly heats** the IGM:
- **Before reionization**: $T \sim 100$ K (adiabatic cooling from early universe)
- **During reionization** ($z \sim 6$–8): Photoionization heating raises $T$ sharply
- **After reionization**: $T \approx 15,000$ K (at mean density), cools slightly to $T_0 \sim 7,000$–$12,000$ K by $z = 0$

The heating occurs because **each photoionization event leaves a residual electron with ~2 eV of kinetic energy** (on average, for a UV photon exceeding the ionization threshold).

**Timescale**: Temperature rises over ~1 Myr during reionization, then evolves slowly.

**Secondary ionizations by X-rays:**

Hard X-ray photons (from AGN, X-ray binaries, or shocks) can ionize already-ionized gas:
- Single X-ray photon: produces multiple ion-electron pairs, heating the gas more efficiently than UV photons
- **Fraction of energy going to heat vs. ionization**: $f_\text{heat}$ depends on ionization state
  - When $x_\text{HII} \ll 1$ (early, mostly neutral): $f_\text{heat} \sim 0.3$–0.4 (most energy goes to ionization)
  - When $x_\text{HII} \gtrsim 0.1$: $f_\text{heat} \gtrsim 0.64$ (most energy goes to heat)

This **coupling between ionization and heating** is important for feedback effects on small-scale structure.

**Clumpy IGM and the clumping factor:**

The clumping factor $C = \langle n^2 \rangle / \langle n \rangle^2$ accounts for the fact that recombination is a two-body process and scales as $n^2$:

$$\dot{n}_\text{rec} = C(z) \, \alpha_B(T) \, \bar{n}_H^2 (1+z)^3$$

In a **perfectly smooth IGM**: $C = 1$

In a **realistic clumpy IGM**: $C$ depends on:
- Simulation resolution (Jeans smoothing length)
- Sub-grid clumping models
- Epoch (evolves with structure formation)

**Measured values** from various simulations:
- Fully coupled hydro RT: $C(z=6) \sim 2$–3
- DMO (unresolved) + estimate: $C(z=6) \sim 5$–10
- **Highly uncertain** — varies by 2–3 orders of magnitude depending on assumptions

This is a **major source of simulator dependence**. Different codes implement clumping differently (some dynamically, some with sub-grid models).

**Mean-field Equation of Radiative Transfer:**

In the optically thin limit (photon mean free path $\lambda_\text{mfp} > $ computational scale), the RT equation in comoving coordinates becomes:

$$\frac{d J_\nu}{dt} + c\,\hat{n} \cdot \nabla J_\nu = -H(z) J_\nu - \alpha_\nu \rho(J_\nu - S_\nu)$$

where:
- First term: time evolution in expanding universe
- Second: streaming of photons
- Third: redshifting (Hubble drag)
- Fourth: absorption and emission
- Fifth: source term $S_\nu$

**Optically thick limit**: When $\lambda_\text{mfp} \ll$ computational scale, absorption dominates; this requires short-characteristics or other approximate RT methods.

### Section 5: Analytical and Semi-Analytical Models

**Simple ionization model** (photon budget approach):

$$\frac{dQ_\text{HII}}{dt} = \frac{\dot{n}_\text{ion}(\mathbf{x}, z)}{\bar{n}_H} - \frac{Q_\text{HII}}{t_\text{rec}(x_\text{HII}, z)}$$

**Analytical reionization histories** based on power-law forms:
- $Q_\text{HII}(z) \propto \left[\frac{1+z}{z+1}\right]^{\beta}$ (empirical fitting form)
- $z_\text{reion}$ (redshift when $Q_\text{HII} = 0.5$) estimated from CMB constraints: $z_\text{reion} \sim 7.5 \pm 0.5$

**PDF-based outside-in models** (now mostly discredited):
- Assume ionization occurs from lowest-density regions first (smallest recombination sink)
- Predict voids ionize before peaks
- Morphology does NOT match high-resolution RT simulations (which show inside-out)

**Excursion-set inside-out models** (foundational to 21cmFAST):
- Assume ionization follows large-scale structure: high-density peaks ionize first
- Use Press-Schechter or Sheth-Tormen mass functions to compute $f_\text{coll}$ (fraction of mass in halos $> M_\text{min}$)
- Reionization history: $Q_\text{HII}(z) \approx f_\text{coll}(M_\text{min}(z), z)$ (at leading order)
- Morphology naturally inside-out (ionized regions coincide with high-density, high-bias regions)
- **Much faster** than radiative transfer codes

### Section 6: Full Taxonomy of Numerical Codes

**Classification scheme:**

| Category | Speed | Volume | Fidelity | Example codes | What's resolved? |
|----------|-------|--------|----------|----------------|------------------|
| Semi-numerical | $\sim$ min | $\sim 1$ Gpc | Morphology approx. | **21cmFAST**, **SCRIPT**, ARTIST, AMBER | Ionization history, bubbles |
| DMO + SAM | $\sim$ hr | $\sim 1$ Gpc | Galaxy physics approx. | ASTRAEUS, DRAGONS | N-body DM + semi-analytic reionization |
| Partially coupled | $\sim$ day | $\sim 100$ Mpc | RT approximate | SPHINX, ATON | Hydro + simplified RT |
| Fully coupled | $\sim$ week | $\sim 50$ Mpc | Most faithful | THESAN, C2-Ray, RAMSES-RT | Hydro + full RT + star formation |

#### **Semi-Numerical Codes** (Fast, large volume)

**21cmFAST** (THE code for this thesis):
- **Algorithm** (Section 6.1.1): 
  1. Generate linear density field $\delta_m(\mathbf{x}, z)$ at desired redshift
  2. Apply **excursion-set ionization** based on collapsed fraction $f_\text{coll}(z)$:
     - A cell ionizes if its smoothed density exceeds the critical threshold for collapsed halos
     - Smoothing radius controls bubble size (related to mean free path)
  3. Output: ionization field $x_\text{HII}(\mathbf{x}, z)$ and hence brightness temperature $T_b(\mathbf{x}, z)$
  4. Compute power spectrum $P_{21}(k, z)$
  
- **Key tunable parameters** (this is crucial for P2):
  - $\zeta$: Number of ionizing photons per baryon (escape-fraction-weighted)
  - $T_\text{vir}$: Minimum virial temperature for star-forming halos (in K, ~10,000 default)
  - $R_\text{mfp}$: Mean free path of ionizing photons (Mpc)
  - $L_\text{box}$, $N$: Box size and resolution
  
- **Assumptions**:
  - Excursion set (sharp threshold, not fuzzy ionization fronts)
  - No RT calculation; ionization is instantaneous once threshold crossed
  - Clumping factor $C$ is tabulated or computed from halo gas
  - Star formation in all halos above $T_\text{vir}$ (instantaneous feedback)
  
- **Strengths**: Speed (run thousands of models), large volume (captures large-scale ionization topology), parameter flexibility
- **Weaknesses**: No actual photon propagation; bubble morphology is determined by density thresholds, not source photons; feedback effects approximate

**SCRIPT** (mentioned throughout; semi-coupled radiative ionization code for simulations):
- Similar philosophy to 21cmFAST but with additional couplings between ionization and density field evolution
- May use slightly different halo mass function or clumping model
- Expected to produce similar but not identical ionization fields as 21cmFAST at same parameters
- **This is the key comparison for P1: how much do EFT coefficients differ between 21cmFAST and SCRIPT?**

**ARTIST and AMBER**:
- Similar speed to 21cmFAST
- ARTIST: analytic radiative transfer approximation (faster but less accurate RT)
- AMBER: adaptive mesh refinement for sub-grid structure

#### **DMO + SAM Codes** (Dark matter only + semi-analytic model for galaxy formation)

**Approach**: Run dark-matter-only N-body simulation, then post-process with semi-analytic galaxy formation and reionization models.

**ASTRAEUS** (at high-$z$):
- N-body DM sim $\to$ halo catalog (virial radius, mass, merger history)
- SAM: semi-analytic stellar mass growth, feedback (stellar winds, SN, quasars)
- Reionization: compute ionization field from galaxies in halo catalog
- Couples reionization back to galaxy formation (feedback)
- **Resolution**: ~10s of Mpc per particle (10^3 particles per halo at $z=6$)

**DRAGONS**:
- Similar to ASTRAEUS; includes dust and metals
- More detailed stellar population synthesis

**Advantages**:
- Moderate speed (hours per model)
- Captures some feedback effects
- Large volume (Gpc-scale)

**Disadvantages**:
- Star formation is semi-analytic (not self-consistent)
- Spatial resolution of ionization set by halo resolution, not gas resolution
- Cannot capture small-scale density effects on ionization fronts

#### **Partially Coupled Codes** (Hydro + simplified RT)

**SPHINX**:
- Hydrodynamical simulation (gas evolution) + radiative transfer
- Simplified RT (approximate method, faster than full implicit RT)
- Smaller volume (~100 Mpc) to enable hydro resolution
- More faithful to actual physics than semi-numerical codes

**Drawback**: Limited volume means cosmic variance is large; fewer independent realizations feasible.

#### **Fully Coupled Codes** (Gold standard, small volume)

**THESAN**:
- Full coupled hydro + RT + star formation in same code
- Resolves gas dynamics, star formation physics, and RT simultaneously
- Small volume (~100 Mpc per side) due to computational cost
- Cost: **1–2 weeks per model** on supercomputers

**C2-Ray, RAMSES-RT**:
- Similar philosophy; different implementation details
- Also small volume, slow

**Why slow?** RT is expensive: need to track photons or solve RT equation implicitly across the domain at every hydro timestep.

**Strengths**: Most physically faithful; can assess systematic errors in faster codes

**Weaknesses**: Very slow (limits parameter space exploration); small volume (cosmic variance); expensive

### **Speed / Fidelity Trade-off**

The review emphasizes the **fundamental trade-off**:

**Slow codes (fully coupled)** can capture:
- Detailed gas dynamics and cooling
- Ionization fronts and photon propagation
- Feedback on star formation (radiation pressure, photoheating)
- But only for ~100 Mpc volumes and limited parameter ranges

**Fast codes (semi-numerical)** can:
- Explore large parameter spaces (P2 inference requires this)
- Simulate large volumes (cosmic variance control)
- Run thousands of models quickly (feasible for Bayesian inference)
- But miss small-scale morphological details

**The core problem for P1 and P2**: Different codes inhabit different points in this trade-space. Understanding which approximations drive EFT coefficient differences is the essence of P1.

## Methods

**Review structure:**
- 50+ pages, Springer Nature template (living review format)
- Sections 2–4: Physical foundations (cooling, feedback, radiative transfer)
- Section 5: Analytical/semi-analytical models (scaling laws, excursion sets)
- Section 6: Complete taxonomy of all major simulation codes (21cmFAST, ARTIST, ASTRAEUS, THESAN, etc.)
- Section 7: Comparison of codes on standard test cases (when available)

**Code coverage**: As of 2022, reviews every major reionization simulation code published in the literature, with ~200 references.

## Key Equations Summary

**Photoionization rate**:
$$\Gamma_\text{HI} = 4\pi \int_{\nu_\text{LL}}^\infty \frac{\sigma_\text{HI}(\nu)}{h\nu} J_\nu \, d\nu$$

**Reionization equation** (global):
$$\frac{dQ_\text{HII}}{dt} = \frac{\dot{n}_\text{ion}}{\bar{n}_H} - \frac{C(z) \alpha_B(T) \bar{n}_H (1+z)^3 x_\text{HII}}{1}$$

**Clumpy recombination rate**:
$$\dot{n}_\text{rec} = C(z) \, \alpha_B(T) \, \bar{n}_H^2 (1+z)^3$$

**Temperature evolution** (heating/cooling):
$$\frac{dT}{dt} = \left[\text{photoionization heating} - \text{adiabatic expansion} - \text{Compton cooling} - \text{line cooling}\right] / c_v$$

**Excursion-set ionization** (21cmFAST and SCRIPT):
$$x_\text{HII}(\mathbf{x}) = \begin{cases} 1 & \text{if } \delta_\text{smoothed}(\mathbf{x}) > \delta_c(z) \\ 0 & \text{otherwise} \end{cases}$$

where the critical density $\delta_c$ is set by the condition that the number of ionizing photons equals the recombination sink.

## Connection to This Thesis

### Relevance to P1 (Simulator dependence in EFT coefficients)

**Directly critical**:

This review is **the map** for understanding simulator dependence. The key insights:

1. **21cmFAST vs. SCRIPT**: Both are semi-numerical, both use excursion sets. But they may differ in:
   - Halo mass function implementation (Press-Schechter vs. Sheth-Tormen vs. N-body fits)
   - Clumping factor model (tabulated vs. computed dynamically)
   - Minimum mass threshold implementation
   - RT approximation vs. none
   
   **P1's core empirical question**: Quantify these differences and measure their impact on EFT coefficients.

2. **Why EFT at all?**: If 21cmFAST and SCRIPT differ in approximations, the ionization fields $x_\text{HII}^{\text{21cmFAST}}$ and $x_\text{HII}^{\text{SCRIPT}}$ will differ. EFT bias coefficients $\{b_1^x, b_2^x, b_{\nabla^2}^x, P_{\epsilon\epsilon}\}$ are the **universal language** that captures this difference in a compressible way — i.e., **maybe** the coefficients are similar across codes even if the fields differ in detail.

3. **Validating EFT against RT codes**: Gnedin & Madau note that semi-numerical codes "reproduce global reionization history well but can misrepresent small-scale morphology." This is where EFT comes in: if small-scale morphology differences don't matter (because they're absorbed into $P_{\epsilon\epsilon}$, the noise power), then EFT is robust. If they do matter, EFT breaks down.

### Relevance to P2 (Cross-simulator generalization)

**Central motivation**:

P2's hypothesis is that **EFT-inferred parameters generalize better across simulators than native parameters**.

Why?
- Native parameters ($\zeta, T_\text{vir}, R_\text{mfp}$) are **code-specific**:
  - 21cmFAST and SCRIPT define $\zeta$ slightly differently (different halo mass functions, feedback models)
  - The same "true" astrophysical escape fraction might map to different $\zeta$ values in different codes
  
- EFT coefficients ($b_1^x, b_2^x, ...$) are **universal**:
  - They describe the large-scale structure of the ionization field
  - Large-scale structure is set by the ionized bubble distribution, which is determined by the source/sink balance (independent of code details)
  - Therefore, EFT coefficients should be **more stable** across codes

Gnedin & Madau support this by showing that different codes, despite different approximations, reproduce the **global reionization history** $Q_\text{HII}(z)$ reasonably well. If the history is universal, maybe the large-scale ionization structure is too.

### Supports / contradicts

- **Predecessor**: [[Trac & Gnedin 2009 (Reionization Simulations)]] (earlier code comparison and RT algorithm review; this 2022 version updates for SKA era)
- **Validates physics for**: [[Choudhury 2022 (Reionization Intro)]] (photon budget assumptions tested against various codes here)
- **Motivates**: [[McQuinn & D'Aloisio 2018]] (EFT approach needed because codes differ; EFT is the language to compare them)

## Limitations and Caveats

**What this review does NOT provide:**

1. **Direct code comparison**: While the taxonomy is complete, there is **limited head-to-head comparison** of outputs from different codes on identical parameter sets. (This is expensive; different codes use different conventions.)

2. **Systematic error quantification**: The review describes what each code does but does not systematically quantify the errors introduced by each approximation (e.g., "how wrong is the excursion-set approximation?"). 
   - Answer often requires running fully coupled codes and comparing.
   - [[Iliev et al. 2006]] did this for some codes, but not all.

3. **EFT-specific guidance**: The review pre-dates widespread adoption of EFT methods for reionization. Does not discuss how EFT bias coefficients vary across codes or whether they are more stable than native parameters.
   - **This is exactly what P1 and P2 address.**

4. **Computational cost details**: Gives qualitative descriptions ("minutes" vs. "weeks") but not detailed scaling laws (runtime vs. box size, resolution, parameter variations).

**Assumptions in the review that may break:**

1. **Static hierarchy**: The code taxonomy may evolve as new methods are developed. For example, **neural network emulators** (like [[Ore et al 2025 (SKATR)]]) represent a new category not discussed here.

2. **Locality of physics**: Assumes physics is local in space and time (i.e., ionization state at a point depends on nearby gas and sources). This breaks at the ionization front where global photon propagation matters.

3. **Negligible feedback during EoR**: Assumes star formation proceeds at approximately constant efficiency even as ionization changes. At early times ($z > 8$), feedback effects may be stronger.

## Figures and Tables

**Key Table in Section 6**: Complete taxonomy of all codes with columns for:
- Code name
- Category (semi-numerical, DMO+SAM, etc.)
- Speed (runtime estimate)
- Volume (box size)
- Resolution (particle/grid size)
- What physics is included (hydro, RT, feedback, etc.)
- Representative papers

**Key Figure**: Timeline showing the redshift range and typical ionized fractions achieved by different code types.

## Open Questions After Reading

> [!gap]
> **Quantifying code differences**: The review states that semi-numerical codes "can misrepresent small-scale morphology." How large is this misrepresentation, and does it affect the EFT regime ($k < 0.5$ Mpc⁻¹)? This is the core empirical question for P1.

> [!gap]
> **EFT universality**: The review shows that codes produce similar global reionization histories. Does this also mean the **large-scale ionization power spectrum** is similar across codes? If yes, then EFT coefficients should be robust to code choice (supporting P2's hypothesis).

> [!gap]
> **21cmFAST vs. SCRIPT comparison**: The review doesn't compare 21cmFAST and SCRIPT directly. A detailed run-to-run comparison at fixed parameters would be very informative for understanding P1's findings.

> [!gap]
> **Role of clumping factor**: The review emphasizes that clumping factor $C$ is highly uncertain (varies by 2–3× across codes). Does P1 find that clumping factor differences are the dominant source of EFT coefficient variation? If yes, this would be a key systematic to control.

> [!gap]
> **Future directions**: As SKA observations come online, will codes need to be further refined to match observational precision? Will EFT bias coefficients need to be more universally calibrated (across codes) for parameter inference to be reliable?
