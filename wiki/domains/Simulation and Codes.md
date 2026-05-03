---
type: domain
title: "Simulation and Codes"
created: 2026-04-14
updated: 2026-04-16
tags:
  - domain/simulation
  - domain/codes
status: mature
related:
  - "[[Reionization Physics]]"
  - "[[Effective Field Theory]]"
  - "[[Inference and ML]]"
  - "[[Simulator Dependence]]"
---

# Simulation and Codes

## The Landscape: The Fundamental Trade-off

Reionization simulations fall into four broad categories with fundamentally different speed/accuracy trade-offs ([[Gnedin & Madau 2022 (Modeling Reionization)]], Section 6). No current code captures **all** relevant physics at adequate resolution over cosmological volumes. Understanding which approximations a code makes is essential for interpreting physical differences between codes, and crucially, for interpreting EFT coefficient differences in the thesis.

| Class | Speed | Volume | Physical fidelity | Examples |
|-------|-------|--------|-------------------|---------|
| **Semi-numerical** | Seconds-minutes | Large ($\sim$Gpc / box side) | Morphology approximate; sub-bubble physics via prescriptions | 21cmFAST, BEoRN, AMBER |
| **DMO + SAM** | Hours-days | Large ($\sim$100-300 Mpc) | Galaxy physics approximate; galaxy formation via recipes; RT approximate | ASTRAEUS, DRAGONS |
| **Partially coupled** | Days-weeks | Medium ($\sim$50-100 Mpc) | RT approximate; limited to small regions; feedback approximate | CRASH + hydro, ATON + N-body |
| **Fully coupled RT** | Weeks-months | Small ($\sim$95 Mpc) | Most physically faithful; self-consistent galaxy formation + RT; full hydro | THESAN, C²-Ray + hydro |

**The core trade-off is fundamental and unavoidable:**
- Semi-numerical codes run in **seconds to minutes**, making them ideal for exploring parameter space and generating large training sets (100s-1000s of realizations)
- Full RT codes run in **weeks to months**, achievable only for a handful of runs on the largest clusters
- The difference is not merely instrumental; it reflects the computational cost of solving the radiative transfer equation explicitly

### Why the Speed Difference Is So Large

- **Semi-numerical:** Assume sources ionize regions based on a heuristic (excursion-set criterion, conditional luminosity function). No explicit photon tracking. Compute density field from perturbation theory (2LPT) rather than N-body. Result: ~10^4–10^5× speedup.
- **Full RT:** Explicitly solve the radiative transfer equation (or stochastically sample photon packets) on every cell, accounting for source geometry, absorption cross-sections, and scattering. This requires solving coupled PDEs at every time step. Result: factors of 10^4–10^5 slower.

## The Simulator Dependence Problem

**Even when codes are tuned to the same global reionization history** $\bar{x}_\text{HII}(z)$ (by adjusting astrophysical parameters), they produce **different ionization morphologies** and different 21 cm statistics — especially at small-to-intermediate scales (1-20 Mpc). This is [[Simulator Dependence]].

The differences arise because codes make different choices in:
- How they place and evolve sources
- How they compute ionized regions (excursion-set vs. RT)
- How they handle recombinations and partial ionization
- How they evolve the density field (2LPT vs. N-body)

ML models trained on one code learn these code-specific morphological signatures and mistake them for universal physics. When applied to data from a different code (or real data), they produce biased inferences.

## Semi-Numerical Codes

Semi-numerical codes use **approximate prescriptions** to paint ionized regions onto a density field without explicitly solving radiative transfer. They run in seconds to minutes on a single CPU, making them ideal for training set generation.

### 21cmFAST

**Primary code for the thesis.**

- **Type:** Semi-numerical, excursion-set based
- **Developer:** Andrei Mesinger (original paper [[Mesinger et al 2010 (21cmFAST)]]); current maintainers include Steven Murray (py21cmfast wrapper)
- **Current version:** py21cmfast (Python wrapper); active development
- **Repository:** github.com/21cmfast/21cmFAST

#### How 21cmFAST Works

1. **Density field:** Generates an initial density field from a linear power spectrum (specified cosmology). Evolves it using **2nd-order Lagrangian Perturbation Theory (2LPT)**, which is accurate for the large-scale density field up to $k \sim 0.3-0.5 h/\text{Mpc}$.

2. **Excursion-set ionization:** At each spatial point, 21cmFAST computes the integrated collapsed fraction of halos within a radius $R$:
   $$\int_M^\infty n(M', z) dM' \geq \zeta^{-1}$$
   If this exceeds the ionizing efficiency threshold $\zeta^{-1}$, the point is ionized.

3. **Bubble definition:** This criterion effectively defines an **ionized bubble** at each point. Bubbles naturally grow with redshift (as $\zeta^{-1}$ decreases) and cluster in overdense regions.

4. **Thermal history:** Computes spin temperature $T_S$ and kinetic temperature $T_K$ via simplified prescriptions (coupling to Ly$\alpha$ photons, X-ray heating, adiabatic heating).

5. **Output:** Brightness temperature field $\delta T_b(\mathbf{x}, z)$ and neutral fraction $x_\text{HI}(\mathbf{x}, z)$.

#### Key Parameters

- **$\zeta$ (ionizing efficiency):** Photons per baryon above the ionizing threshold; effectively sets the source strength
- **$T_\text{vir}$ (virial temperature):** Minimum halo temperature for star formation; sets the minimum ionizing halo mass $M_\text{min}$
- **$R_\text{mfp}$ (mean free path):** Mean distance ionizing photons travel before absorption; sets the characteristic bubble size
- **$R_\text{mfp}$ vs. $T_\text{vir}$ interplay:** Larger $R_\text{mfp}$ → larger bubbles → smoother ionization field → smaller $|b_{\nabla^2}^x|$

#### Strengths

- **Speed:** ~1-10 seconds per simulation on a single CPU (thousands of realizations per hour cluster-wide)
- **Large volumes:** Can simulate 1-5 Gpc boxes (matching the scale of cosmological surveys)
- **Simplicity:** Easy to modify; standard in the field; well-documented
- **Physical basis:** Excursion-set criterion has strong theoretical grounding

#### Limitations (and implications for simulator dependence)

- **2LPT density field:** Accurate only to $k \lesssim 0.3-0.5 h/\text{Mpc}$; N-body codes are more accurate at smaller scales (but 21cmFAST output is typically only used at $k \lesssim 0.5$, so this is acceptable)
- **Spherical bubble assumption:** Excursion-set ionization assumes spherical bubbles; real bubbles are more complex due to density anisotropy and photon anisotropy
- **Uniform mean free path:** The ionizing photon mean free path is assumed constant with position; in reality, it varies due to density clumping
- **Simplified recombinations:** Uses a global clumping factor $C(z)$; does not resolve sub-grid recombinations in individual cells
- **Result:** The ionization morphology produced by 21cmFAST is an **approximation**; it matches observations but does not exactly match full RT codes on small-to-intermediate scales. This is the source of much of the simulator dependence.

### BEoRN

**Secondary code for P1 comparison.** (Replaces SCRIPT, which is no longer publicly available.)

- **Type:** Semi-numerical, halo-based source model with flexible Lyman-α / X-ray / ionizing radiation profiles
- **Developer:** Schosser et al. (2023); maintained at [github.com/cosmic-reionization/BEoRN](https://github.com/cosmic-reionization/BEoRN)
- **Paper:** Schosser et al. 2023, MNRAS 526, 2942 ([arXiv:2305.15466](https://arxiv.org/abs/2305.15466))
- **Language:** Python — no separate compilation required
- **Status:** Public; actively maintained; validated against 21cmFAST

#### How BEoRN Differs from 21cmFAST

BEoRN (Bubbles during Epoch Of Reionization Numerical-simulator) uses a physically different source and IGM evolution model:

1. **Built on N-body / 21cmFAST halo catalogs:** Rather than generating its own density field, BEoRN accepts the density field and halo catalogs directly from an external source — including 21cmFAST. This makes **matched initial conditions trivial**: run 21cmFAST to generate ICs + halo catalogs, pass them both to BEoRN, and the two codes are guaranteed to start from the same density realization.

2. **Profile-based ionizing radiation:** Instead of painting ionized regions via an excursion-set criterion, BEoRN places spherical ionization profiles around each halo, whose shape and amplitude are set by a flexible parameterisation. This produces a qualitatively different bubble morphology.

3. **Lyman-α and X-ray heating:** BEoRN simultaneously computes spin temperature evolution via separate Lyman-α coupling and X-ray heating profiles. The coupling between ionization, heating, and the 21cm signal is therefore more self-consistent than in base 21cmFAST.

4. **Source model calibration:** BEoRN re-calibrates the intensity of radiation to match 21cmFAST's global reionization history $\bar{x}_\text{HII}(z)$ — ensuring apples-to-apples comparison at fixed global history while preserving morphological differences.

#### Physical Differences from 21cmFAST

- **Bubble morphology:** Profile-based ionization produces different bubble size distributions compared to the excursion-set criterion. The effective radius $R_\text{eff}$ and patchiness can differ by 20–50%.
- **Ionization patchiness:** The $b_2^x$ coefficient is sensitive to bubble overlap; BEoRN's profile stacking differs from 21cmFAST's barrier-crossing logic.
- **Stochastic term:** $P_{\varepsilon\varepsilon}$ reflects discreteness of the bubble field, which differs between the two algorithms.
- **Result:** BEoRN is an ideal **second code** for P1 because it is:
  - Python (seamless integration with the thesis pipeline)
  - Accepts 21cmFAST ICs directly (matched ICs require no custom glue code)
  - Physically different from 21cmFAST (different ionization and source models)
  - Publicly available and well-documented
  - Tractable for P1's ~50-run matched ICs study

#### SCRIPT (deprecated for this thesis)

SCRIPT (Charlotte Mason, Cambridge group) was the original planned secondary code. Its repository (`github.com/charlottenosam/SCRIPT`) is no longer publicly accessible. BEoRN is the designated replacement for all P1 and P2 cross-simulator comparisons.

### AMBER

- **Type:** Semi-numerical, adaptive mesh refinement (AMR) excursion-set
- **Notes:** Improves on 21cmFAST by using adaptive mesh refinement for the excursion-set calculation; better handles sub-grid physics and partially ionized regions
- **Advantage:** More accurate bubble morphology than 21cmFAST at small scales
- **Status:** Less widely used; mentioned in [[Gnedin & Madau 2022 (Modeling Reionization)]] Sec. 6.1.3

### Other Semi-Numerical Codes

**ARTIST / Analytic RT approximations:**
- Uses analytic approximations for radiation transfer without explicit excursion-set criterion
- Alternative to excursion-set family; independently derived ionization structure
- Described in [[Gnedin & Madau 2022 (Modeling Reionization)]] Sec. 6.1.2

**SimFast21:**
- Another 21cmFAST alternative; similar excursion-set approach
- Santos et al. 2010; less commonly used in recent work
- Used in some cross-simulator tests

**zreion:**
- Used in Zhou & La Plante 2022 cross-simulator test
- Assignment-based scheme; morphology differs from excursion-set codes

**GRIZZLY:**
- Ghara et al.; faster than full RT but more physical than pure excursion-set
- Radiative transfer approximation

## Dark Matter Only + Semi-Analytic Models (DMO+SAM)

These codes run **N-body dark matter simulations** for accurate large-scale structure, then add **semi-analytic prescriptions** for galaxy formation and radiative transfer. More physically faithful galaxy populations than pure semi-numerical, at moderate computational cost (hours to days).

### ASTRAEUS

- **Type:** N-body DM + semi-analytic galaxy formation + approximate RT
- **Developer:** Katz et al.
- **Method:** 
  1. Run N-body DM simulation (Gadget3 or similar)
  2. Track halo merger trees (consistent structure evolution)
  3. Apply semi-analytic recipes for galaxy formation (star formation, feedback, stellar mass)
  4. Model reionization-galaxy feedback self-consistently (photo-evaporation of small halos)
- **Advantage:** Captures how reionization feeds back on galaxy growth (smaller halos are photo-evaporated, suppressing star formation in low-mass systems)
- **Limitation:** RT is still approximate; galaxy physics is still prescribed
- **Mentioned in:** [[Gnedin & Madau 2022 (Modeling Reionization)]] Sec. 6.2.1

### DRAGONS

- **Type:** N-body DM + semi-analytic galaxy model
- **Developer:** Hutter et al.
- **Method:** Similar to ASTRAEUS; includes detailed galaxy physics (dust, metals, merger trees)
- **Mentioned in:** [[Gnedin & Madau 2022 (Modeling Reionization)]] Sec. 6.2.2

**Status:** DMO+SAM codes are less commonly used for large-scale inference compared to semi-numerical codes (slower), but provide valuable validation against more realistic galaxy formation.

## Radiative Transfer Codes: The Ground Truth

Full radiative transfer codes **explicitly propagate ionizing photons** through the inhomogeneous IGM. They are the ground truth against which semi-numerical approximations are calibrated. However, full RT is computationally expensive (weeks to months per simulation), limiting the number of runs that can be completed.

### Radiative Transfer Algorithm Taxonomy

Three main algorithm families exist, with different strengths and weaknesses ([[Trac & Gnedin 2009 (Reionization Simulations)]]):

#### 1. Moments Methods (M1 / Eddington Approximation)

**How it works:**
- Reduce the full radiative transfer equation (a complicated integro-differential equation) to conservation laws for photon energy density $E$ and flux $\mathbf{F}$
- Close the system via an **Eddington tensor**: an approximation for the radiation field anisotropy
- In the M1 approximation, $\mathbf{P} = f \mathbf{E}$, where $f$ is the Eddington factor (usually ~1/3)

**Advantages:**
- Relatively fast (10-100× faster than full angular RT)
- High dynamic range in density; handles both diffuse IGM and dense clumps well
- Photon conservation is natural (built into conservation law)

**Limitations:**
- Approximate angular dependence (the Eddington factor is not exact)
- Can produce spurious (non-physical) fluxes at low optical depth

**Example codes:** THESAN (uses AREPO + M1), RAMSES-RT

#### 2. Monte Carlo Methods

**How it works:**
- Stochastically sample photon packets from sources (each packet represents many real photons)
- Track packet propagation through the grid
- Compute absorption, scattering, and energy deposition
- Repeat for many packets to build up statistical distribution

**Advantages:**
- Naturally conserves photons (every packet is tracked)
- Handles complex geometry well (no approximations needed for anisotropy)
- Straightforward to implement; intuitive physics

**Limitations:**
- Computationally expensive (need many packets for low noise)
- Statistical noise (fluctuations from finite number of packets)
- Hard to parallelize efficiently

**Example codes:** CRASH, MCRT

#### 3. Ray-Tracing Methods

**How it works:**
- Cast rays from each source in directions
- Follow rays through the grid, computing ionization along each ray
- Accurate geometric computation of shadowing and ray divergence

**Advantages:**
- Accurate angular dependence
- Natural for point sources (sharp rays)

**Limitations:**
- Computation grows as $N_\text{sources} \times N_\text{directions} \times N_\text{cells}$; scaling is poor for large volumes with many sources
- Memory-intensive

**Example codes:** C²-Ray, iLIEVU, ATON

### Algorithm Convergence

Important result from [[Trac & Gnedin 2009 (Reionization Simulations)]]: the three algorithm families have **converged on a consistent qualitative picture** of the reionization process when run on identical initial conditions. 

Quantitative differences remain:
- Bubble size distributions can differ by ~30% between algorithms
- Temperature structures at reionization fronts differ (front thickness, heating)
- Small-scale ($k > 0.2 h/\text{Mpc}$) morphologies vary more than large-scale

**Implication for thesis:** Even "ground truth" full RT codes agree at the level of 20-30% on morphological details. The EFT description at large scales ($k < 0.2 h/\text{Mpc}$) should be robust to these differences.

### THESAN: The Most Complete Modern Simulation

**Details:**
- **Type:** Fully coupled radiative-transfer hydrodynamical
- **Method:** 
  1. Hydrodynamics via AREPO code (moving-mesh hydrodynamics)
  2. Radiative transfer via M1 approximation
  3. Galaxy formation via IllustrisTNG feedback recipes (supernovae, AGN feedback, cooling, star formation)
  4. Fully self-consistent: sources are galaxies produced by the hydro simulation, not imposed externally

- **Properties:**
  - Box size: 95 Mpc/h (comoving)
  - Resolution: 2048³ dark matter particles + 4096³ gas cells
  - Computational cost: ~100 million CPU-hours (requires HPCs like Fugaku or Perlmutter)
  - Outputs: Full 3D density, temperature, ionization fields at multiple redshifts

- **Developer:** Garaldi et al. (2021, arXiv); continuing development at multiple institutions
- **Status:** Public (Illustris project); data available for download

- **Validation:** Qin et al. 2022 validated the EFT bias expansion against THESAN and showed excellent agreement at $k \lesssim 0.8 h/\text{Mpc}$ with renormalized coefficients. This provides **proof** that the EFT works for full RT codes.

- **Strength:** Captures gas thermodynamics, partial ionization, feedback self-consistently. Closest to "ground truth" reionization physics.

### C²-Ray

- **Type:** Full RT, ray-tracing based
- **Developer:** Iliev et al.
- **Status:** Long-standing workhorse code; used in many convergence studies (Iliev et al. 2006 comparison project)
- **Impact:** Established that full RT codes agree on morphology to within ~30%
- **Limitation:** Slower than methods-based codes; scaling to large volumes challenging

## Photon Conservation: A Critical Algorithmic Requirement

Any physically correct RT code must **conserve photons**. Every ionizing photon produced must either:
1. Ionize a hydrogen atom
2. Be absorbed (by dust, by already-ionized atoms in an expanding HII region)
3. Escape the simulation volume

**Algorithms that violate photon conservation** are unphysical and can produce spurious ionization patterns.

**Good algorithms scale as $\mathcal{O}(N)$** with the number of resolution elements (cells or particles) and **automatically conserve photons** by construction. Examples:
- Monte Carlo methods: each packet is tracked; conservation is guaranteed
- Moments methods with proper flux limiting: conservation laws inherently conserve particles
- Methods like Smoothed Particle Hydrodynamics (SPH) with radiative transfer: require careful implementation to conserve photons

## Matched Initial Conditions: A Critical Requirement for P1

For P1 (comparing 21cmFAST and BEoRN), the two codes must use the **same cosmological initial conditions**. This is essential to ensure that morphological differences arise from the ionization algorithms, not from different random realizations of the density field.

### Why This Is Straightforward with BEoRN

BEoRN is specifically designed to consume 21cmFAST outputs. It accepts the density field and halo catalogs produced by 21cmFAST directly, with no format conversion required. The procedure is:

1. **Run 21cmFAST** with a fixed `random_seed` to produce $\delta_m(\mathbf{x})$ and the halo catalog; write both to the 21cmFAST cache
2. **Point BEoRN** at the 21cmFAST cache directory — it reads the same density field and halos
3. **Calibrate BEoRN** source parameters so that $\bar{x}_\text{HII}(z)$ matches the 21cmFAST run (see P1 Step 2d)

The matter power spectra from both codes agree at sub-percent level by construction (same underlying density field).

### Technical Notes

- py21cmfast has hooks to export initial conditions and evolved density/halo fields (`write=True`)
- BEoRN's `halo_catalog_dir` parameter points directly to the py21cmfast cache
- Testing: verify $P_{mm}^\text{21cmFAST} / P_{mm}^\text{BEoRN} = 1.000 \pm 0.001$ before running the full simulation grid

## The Speed/Fidelity Trade-off in Context

**For P1 (EFT coefficient extraction):**
- Semi-numerical codes are **appropriate** because they are fast and can run ~50 realizations of matched ICs in reasonable time
- The EFT is a large-scale description ($k < 0.5 h/\text{Mpc}$)
- At large scales, semi-numerical codes agree with full RT reasonably well (within 30-50% on morphology)
- Question: Do EFT coefficients agree between semi-numerical codes and full RT at the same $\bar{x}_\text{HII}(z)$? P1 establishes this by comparing 21cmFAST + BEoRN (both semi-numerical).

**For P2 (training an inference model):**
- A large training set is necessary (~500 simulations for reasonable posterior accuracy with TMNRE)
- This requires a **fast code** (21cmFAST at 1-10 sec/simulation)
- Full RT would require ~500 × weeks = 10^4 CPU-years (infeasible)
- Solution: Train on 21cmFAST, validate on BEoRN and potentially on THESAN (for a small subset)

## Key Concepts

- [[Excursion Set Formalism]] — core algorithm in 21cmFAST; explains how ionized regions are defined (BEoRN uses a profile-based model instead)
- [[Initial Conditions]] — matched $\delta_m(\mathbf{x})$ grid across codes required for fair P1 comparison
- [[Radiative Transfer]] — the three algorithm families; tradeoffs between speed and accuracy
- [[Clumping Factor]] — sub-grid recombination prescription; varies between codes
- [[Simulator Dependence]] — systematic differences between codes at fixed reionization history
- [[Mean Free Path]] — sets the characteristic ionized bubble size; critical parameter
- [[2LPT (2nd-order Lagrangian Perturbation Theory)]] — density field evolution in semi-numerical codes

## Key Entities

- [[21cmFAST]] — primary simulation code; fast; excursion-set based; public
- [[BEoRN]] — secondary simulation code; semi-numerical; halo-profile approach; Python; ideal for P1 (replaces SCRIPT)
- [[THESAN]] — full radiative transfer; ground truth for validation; smaller box (95 Mpc); public data
- [[py21cmfast]] — Python wrapper for 21cmFAST; maintained by Steven Murray

## Sources

- [[Trac & Gnedin 2009 (Reionization Simulations)]] — RT algorithm taxonomy; convergence; sources vs sinks; foundational
- [[Gnedin & Madau 2022 (Modeling Reionization)]] — Complete code taxonomy; 21cmFAST Sec. 6.1.1; speed/fidelity trade-offs; **the field map**
- [[McQuinn & D'Aloisio 2018]] — EFT validated across 3 RT codes; establishes that semi-numerical vs RT comparison is meaningful at large $k$
- [[Qin et al 2022 (EFT Redshift Space)]] — THESAN validation of EFT; demonstrates renormalized EFT works for full RT to $k \lesssim 0.8$
- [[Iliev et al. 2006 (Comparison project)]] — Iliev et al. code comparison project; established convergence of RT algorithms
