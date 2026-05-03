---
type: concept
title: "Radiative Transfer"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/method
  - domain/simulation
status: seed
domain: "[[Simulation and Codes]]"
related:
  - "[[Excursion Set Formalism]]"
  - "[[Ionization Morphology]]"
  - "[[Simulation and Codes]]"
  - "[[Mean Free Path]]"
sources:
  - "[[Trac & Gnedin 2009 (Reionization Simulations)]]"
  - "[[Gnedin & Madau 2022 (Modeling Reionization)]]"
---

# Radiative Transfer

## What It Is

Radiative transfer (RT) is the propagation of ionizing photons through the inhomogeneous IGM, including their absorption, scattering, and re-emission. The process drives the ionization state of hydrogen from neutral ($x_\text{HI} \approx 1$) to ionized ($x_\text{HI} \approx 0$) during reionization. RT is a fundamental physical process that determines the **morphology** (structure and patchiness) of the reionized regions, the **thermal history** of the IGM (heating due to photoheating by hard photons), and the **mean free path** of ionizing photons.

## The Full Radiative Transfer Equation

### Derivation from the Boltzmann Equation

The full RT equation for specific intensity $I_\nu$ (energy flux per unit frequency, per unit solid angle) in an expanding universe comes from integrating the Boltzmann equation for photons ([[Gnedin & Madau 2022 (Modeling Reionization)]], Eq. 15):

$$
\frac{1}{c}\frac{\partial I_\nu}{\partial t} + \frac{\mathbf{n}}{a(t)}\cdot\frac{\partial I_\nu}{\partial \mathbf{x}} - \frac{H(t)}{c}\frac{\partial}{\partial \nu}(\nu I_\nu) - 3\frac{H(t)}{c}I_\nu = -\kappa_\nu I_\nu + j_\nu
$$

where:
- **LHS, Term 1** ($\frac{1}{c}\frac{\partial I_\nu}{\partial t}$): Time evolution of intensity
- **LHS, Term 2** ($\frac{\mathbf{n}}{a}\cdot\nabla_\mathbf{x} I_\nu$): Streaming of photons along direction $\mathbf{n}$, with cosmological scaling by inverse expansion factor $1/a$
- **LHS, Term 3** ($-\frac{H}{c}\frac{\partial}{\partial\nu}(\nu I_\nu)$): **Cosmological redshift** — photons lose energy as space expands, creating an effective frequency shift. This term is absent in non-cosmological RT.
- **LHS, Term 4** ($-3\frac{H}{c}I_\nu$): **Dilution of intensity** due to volume expansion at rate $3H$ (from $\nabla \cdot \mathbf{v} = 3H$ in an expanding universe)
- **RHS, Term 1** ($-\kappa_\nu I_\nu$): **Absorption** of photons at opacity $\kappa_\nu$ (dominates where neutral gas is dense)
- **RHS, Term 2** ($j_\nu$): **Emission** of photons from sources (stars, quasars, black holes)

This is a **7-dimensional partial differential equation**: 3 spatial coordinates $\mathbf{x}$, 2 angular coordinates (direction $\mathbf{n}$ on the unit sphere), 1 frequency $\nu$, and time $t$. Solving it directly is prohibitively expensive.

### What Makes Cosmological RT Hard

1. **Enormous dynamic range in density**: The IGM density varies by factors ~$10^6$ from voids to galactic halos, and the opacity $\kappa_\nu$ scales nonlinearly with density. A uniform grid must resolve both the sparsest voids and the densest clumps.

2. **Short mean free paths at I-front boundaries**: Near ionization fronts (I-fronts), where $x_\text{HI}$ transitions from ~1 to ~0 over a narrow zone, the opacity is very high. Photon packets travel only short distances before being absorbed, requiring very high spatial resolution (~10 pc) to resolve the I-front structure accurately.

3. **Many sources with different properties**: Stars have different lifetimes (OB stars: ~few Myr), black holes have variable accretion rates, and quasars vary stochastically. The source term $j_\nu$ is spatially and temporally complex.

4. **Frequency dependence**: The opacity depends on frequency (resonances, edges, continuum), and different frequencies couple to different ionization states (HI, HeII, etc.), making the frequency dimension essential rather than collapsible.

5. **Computational cost dominance**: Full RT without approximations costs ~10–100 GPU-hours for a single 95 Mpc box simulation, compared to milliseconds for semi-numerical codes. This makes it prohibitive for parameter studies or large surveys.

## Three Algorithm Families

([[Trac & Gnedin 2009 (Reionization Simulations)]])

### 1. Moments Methods (M1 / Eddington Approximation)

#### Concept

Instead of tracking the full 7D intensity distribution $I_\nu(\mathbf{x}, \mathbf{n}, \nu, t)$, moments methods evolve only low-order moments (energy density and flux):

- **Zeroth moment**: $E_\nu(\mathbf{x}, \nu, t) = \frac{1}{c}\oint I_\nu\,d\Omega$ — photon energy density per unit frequency
- **First moment**: $\mathbf{F}_\nu(\mathbf{x}, \nu, t) = \oint \mathbf{n}I_\nu\,d\Omega$ — photon flux vector

The system is closed using an **Eddington tensor** that relates the pressure tensor $P_{ij} = (1/c) \oint n_i n_j I_\nu\,d\Omega$ to the lower moments. The **M1 approximation** is a specific choice:

$$P_{ij} = f_E \left(E_\nu \delta_{ij} + 3 \left(\frac{F_i F_j}{c^2 E_\nu^2} - \frac{\delta_{ij}}{3}\right)\right)$$

where the **Eddington factor** $f_E$ encodes assumptions about the angular distribution of photons.

#### The Eddington Factor

The key parameter is $f_E(\mathbf{x}, \nu, t)$:

- **Isotropic radiation** (photons evenly distributed in all directions): $f_E \to 1/3$
- **Highly directional** (photons in a narrow beam, like an I-front): $f_E \to 1$
- **M1 ansatz**: $f_E = \frac{1}{3} + \frac{2}{3}(1 - 3\beta)^2$ where $\beta = |F|/(cE)$

The choice of $f_E$ is crucial: too small, and the code under-predicts directionality at I-fronts; too large, and it over-estimates pressure gradients, causing spurious instabilities.

#### Two-Stream Problem

A known limitation: when two ionization fronts pass through each other (e.g., bubbles expanding from different sources merging), the M1 approximation breaks down because it assumes a single predominant photon direction. Two beams at different angles get "averaged" by the Eddington closure, losing the ability to model interference or beam-crossing geometry. This can lead to unphysical merging of ionization fronts and over-estimated recombination rates at merger boundaries.

#### Characteristics

**Strengths:**
- High dynamic range: M1 naturally handles factors ~$10^6$ in opacity because it evolves energy density (naturally log-scale) rather than intensity
- Scales as $\mathcal{O}(N)$ in resolution: $\sim N$ operations per timestep for an $N$-grid
- Fast: can run on GPUs with reasonable wall-clock time
- Handles many sources naturally: each source injects photons into a single cell, no ray-casting needed

**Weaknesses:**
- Approximate angular dependence: The Eddington closure is a closure assumption, not exact, introducing systematic errors in photon angular distribution
- Two-beam issue: merging bubbles lose information about beam crossing
- I-front sharpness: M1 tends to smear I-front boundaries compared to more expensive methods

**Examples:** THESAN (AREPO + M1), RAMSES-RT, GAMER

### 2. Monte Carlo Methods

#### Concept

Monte Carlo (MC) RT emits photon packets stochastically from sources and tracks their trajectories through the grid, computing absorption probabilities and propagation distances.

#### Photon Packet Weights

Rather than individual photons, MC codes track **weighted packets**:
- Each packet carries a weight $w$ (number of physical photons represented)
- The weight is not 0 or 1; it can be any positive number
- Absorption is probabilistic: at each step, a packet has a chance to be absorbed based on the optical depth $\tau = \kappa_\nu \rho \Delta s$ over distance $\Delta s$

#### Optical Depth Sampling

The distance a photon travels before absorption is sampled from the probability distribution:
$$P(\text{absorption at distance } s) = \frac{d}{ds} (1 - e^{-\tau(s)})$$

where $\tau(s)$ is the accumulated optical depth. When a photon is absorbed, the energy is added to the local gas, ionizing hydrogen and heating the medium.

#### Re-emission and Scattering

After absorption, a photon can:
1. **Ionize hydrogen and be lost**: The absorbed energy ionizes an H atom and thermalizes the remaining energy as heat
2. **Be re-emitted** (from the ionized gas, via recombination or scattered radiation): A new photon packet is created with reduced weight (accounting for energy loss), emitted in a random direction

This allows MC to self-consistently handle radiation field recycling: ionizing photons create ionized regions, which recombine and re-emit lower-energy photons.

#### Characteristics

**Strengths:**
- Naturally conserves photons: the sum of packet weights in equals packet weights ionizing + escaping, to machine precision
- No angular approximation: photon direction is tracked exactly, making it ideal for point sources and complex geometries
- Handles radiation redistribution well: scattered and re-emitted photons are tracked with correct energy

**Weaknesses:**
- Computationally expensive: Cost scales as $\mathcal{O}(N_\text{photons})$, and you need $\gtrsim 10^6$–$10^9$ photons for acceptable noise levels
- Noisy diffuse fields: The random nature of packet absorption makes the photoheated gas temperature fluctuate; averaging many packets is required to get smooth temperature fields
- Slow for many sources: if there are $10^5$ sources, you need at least that many packets per timestep, leading to slow overall integration

**Examples:** CRASH, SPHINX (uses a MC variant for ionizing photons)

### 3. Ray-Tracing Methods

#### Concept

Ray-tracing casts geometric rays from sources outward through the grid and computes ionization and heating along each ray.

#### Short vs. Long Characteristics

- **Short characteristics**: Cast rays from each grid cell to its immediate neighbors. Accumulate opacity along short steps, compute local ionization.
- **Long characteristics**: Cast rays from each source through the entire volume. Compute ionization along the full ray path in one go.

#### Characteristics

**Strengths:**
- Geometrically intuitive: rays naturally follow the path of photons, making physical interpretation easy
- Accurate angular dependence: photon direction is tracked exactly, giving sharp I-fronts when emitted from point sources
- Well-suited to point sources (quasars, stars in clusters): the radiation field from a point source is naturally directional

**Weaknesses:**
- Expensive scaling: Cost $\propto N_\text{sources} \times N_\text{resolution}$; with 10000 sources and a $512^3$ grid, this is $10^{16}$ operations, prohibitive
- Limited to a small number of sources: typically used for problems with $\lesssim 100$ discrete sources, not diffuse background from all stars
- Difficult to handle diffuse background: the UV background from stellar sources distributed throughout the volume is hard to represent with discrete rays

**Examples:** C²-Ray (originally for reionization), iLIEVU, ATON

## Convergence of Methods

All three methods have **converged on a consistent qualitative picture** of reionization morphology ([[Trac & Gnedin 2009 (Reionization Simulations)]]): 
- **Inside-out topology**: ionization begins in dense regions (where the first stars form) and propagates outward into lower-density regions
- **Characteristic bubble growth**: once a region is ionized, the bubble expands at a roughly constant speed (the sound speed or ionization front speed, ~10–100 km/s)
- **Percolation transition**: ionization fronts from different sources merge around $z \sim 6$–$8$, and the ionized volume fraction rapidly transitions from 0 to 1

However, **quantitative differences remain** in:

1. **Bubble boundary sharpness**: M1 methods tend to smear I-front boundaries over ~100 pc to ~1 kpc, while ray-tracing methods preserve sharp boundaries. This affects the temperature profile near I-fronts and thus the heat-driven gas dynamics.

2. **Temperature structure in partially-ionized regions**: Different methods handle the recombination zone (where $0 < x_\text{HI} < 1$) differently, leading to variations in $T(x_\text{HI})$ relations. This couples back to ionization balance because $T$ sets the recombination rate.

3. **Bubble size distribution at small scales**: The characteristic size spectrum of ionized bubbles at scales $\lesssim$ a few Mpc depends sensitively on the method's ability to resolve small-scale structure. M1 methods with coarse grids may miss small bubbles entirely.

These differences are **typically small at large scales** (> few Mpc) but become important for precision measurements of the 21 cm power spectrum at small scales ($k > 0.1$ Mpc$^{-1}$).

## Why Semi-Numerical Codes Don't Solve RT

Semi-numerical codes like 21cmFAST and SCRIPT replace the full RT equation entirely with the **[[Excursion Set Formalism]]**, an approximation based on the local density field and ionization threshold. This approach is ~$10^6 \times$ faster than full RT, reducing a calculation from hours to milliseconds.

The approximation works as follows:
- For each grid cell, compute the density $\delta(\mathbf{x})$
- If the local density exceeds a critical threshold (determined by the ionization rate and recombination rate), mark the cell as ionized
- The ionization threshold is set such that the **total ionized mass** at redshift $z$ matches observations (e.g., the Lyman-alpha forest optical depth)

This ignores:
- **Photon propagation geometry**: The actual path photons take from sources to absorbers
- **Partially-ionized transition regions**: Real I-fronts have a finite thickness (the recombination zone) with complex temperature structure; excursion set assumes a sharp transition
- **Temperature fluctuations**: RT codes produce spatially varying temperature due to spectral hardening; excursion set assumes uniform temperature

**Why the EFT is designed to work on semi-numerical outputs**: The EFT framework is coarse-grained — it describes the large-scale ionization morphology and 21 cm power spectrum without needing to resolve individual I-fronts. The **small-scale RT physics** (exact I-front shape, temperature fluctuations, recombination rate) gets absorbed into the EFT coefficients. The excursion-set approximation is most accurate where the EFT is most useful: at scales $> \sim$ few Mpc, where the exact details of photon propagation matter less than the large-scale structure of ionization.

## Full RT vs. Semi-Numerical: Computational Cost Comparison

### Full Radiative Transfer

Running a full RT simulation (e.g., THESAN with AREPO + M1):
- Grid resolution: $512^3$ (typical for modern simulations)
- Box size: 95 Mpc (commoving)
- Time integration: from $z = 20$ to $z = 5$ (~1 Gyr simulation time)
- Computational cost: **~100 GPU-hours** on modern hardware (e.g., NVIDIA A100)
- Wall-clock time: ~1–5 hours on a modern GPU cluster

### Semi-Numerical Code

Running 21cmFAST or SCRIPT:
- Same simulation specifications, same cosmology
- Computational cost: **~5 minutes on a laptop** (a single CPU core can handle this)
- Speedup factor: ~$10^4$–$10^6$ compared to full RT

### Implication for EFT Training

The massive speedup of semi-numerical codes makes it practical to generate **training sets** of thousands of simulations, varying cosmological and reionization parameters over a grid. This is computationally infeasible with full RT codes (which would require $10^5$ GPU-hours). The EFT is designed to be trainable on semi-numerical outputs precisely because of this factor-of-a-million advantage.

## Mean Free Path from RT

RT codes compute the **mean free path** $\lambda_\text{MFP}(\nu, z)$ self-consistently from the absorption coefficient:

$$\lambda_\text{MFP}(\nu, z) = 1/\bar{\kappa}_\nu(z) = \frac{1}{\sigma_\text{ion}(z) \bar{n}_\text{HI}(z)}$$

where $\bar{\kappa}_\nu$ is the mean opacity weighted by the radiation field, $\sigma_\text{ion}(\nu)$ is the photoionization cross-section (frequency-dependent), and $\bar{n}_\text{HI}(z)$ is the mean neutral hydrogen number density.

The MFP grows dramatically with redshift as $x_\text{HI}$ decreases:
- At $z = 6$: $\lambda_\text{MFP} \sim 100$ kpc (reionization era, $x_\text{HI}} > 10^{-3}$)
- At $z = 5$: $\lambda_\text{MFP} \sim 100$ Mpc (post-reionization, $x_\text{HI}} < 10^{-4}$)
- At $z = 2$: $\lambda_\text{MFP} \sim 1$ Gpc (fully ionized, extremely weakly absorbing)

In **semi-numerical codes**, $R_\text{mfp}$ is treated as a **free parameter**, often fit to match RT predictions or observations. This is one source of [[Simulator Dependence]]: different codes may use different MFP prescriptions, leading to different morphologies even for the same input density field.

## Photon Conservation as a Sanity Check

A critical requirement for any RT algorithm: **photon conservation**. Over a time interval $\Delta t$:

$$\text{Photons emitted} = \text{Photons used to ionize H} + \text{Photons from recombination} + \text{Photons escaping volume}$$

More precisely:
$$\int_V j_\nu(\mathbf{x}, t) \, d^3\mathbf{x} \, \Delta t / E_\nu = \int_V \Gamma_\text{HI}(\mathbf{x}, t) n_\text{HI}(\mathbf{x}, t) \, d^3\mathbf{x} \, \Delta t + \int_V \alpha(\mathbf{x}, t) n_e n_p \, d^3\mathbf{x} \, \Delta t + \text{escaping flux}$$

where:
- LHS: Total ionizing photons created by sources
- RHS, Term 1: Photons ionizing neutral hydrogen
- RHS, Term 2: Photons from recombination of ionized regions
- RHS, Term 3: Photons leaving the volume

**Why this matters**: Algorithms that fail photon conservation artificially create or destroy photons, producing unphysical ionization morphologies. For instance, if a code under-conserves photons at I-front boundaries, the front will stall (not propagate) even though there are sufficient ionizing photons available globally.

Good RT algorithms are explicitly designed to conserve photons to within discretization error (~0.1–1%). This can be verified by checking:
$$\frac{\text{Photon out} - \text{Photon in}}{\text{Photon in}} < 10^{-3}$$

## The Ionization Front (I-Front) and Resolution Requirements

### Definition and Physics

An **ionization front** is the sharp boundary where $x_\text{HI}$ transitions from ~1 (neutral) to ~$10^{-3}$ (ionized). The transition occurs over a **recombination zone** of thickness:

$$\Delta x_\text{rec} \sim \frac{c_s}{\Gamma_\text{HI} n_\text{HI}} \sim 1 \text{–} 10 \text{ pc}$$

where $c_s$ is the sound speed, $\Gamma_\text{HI}$ is the photoionization rate, and $n_\text{HI}$ is the neutral density. The I-front **propagates outward** at a speed determined by the balance between ionization and recombination:

$$v_\text{front} \sim \frac{\Gamma_\text{HI} n_\text{HI}}{\rho} \sim 10 \text{–} 100 \text{ km/s}$$

### Apparent Superluminal Motion in Low-Density Regions

A counterintuitive observation: in **very low-density regions** (voids), the I-front can appear to move faster than $c$ in comoving coordinates. This is **not actually faster than light** — it reflects the combination of:
1. The I-front propagating at $\sim c_s$ in physical space
2. Cosmological expansion $(1+z) \propto a^{-1}$
3. The definition of "apparent speed" being sensitive to the density dependence

In reality, the I-front speed in physical coordinates remains $\lesssim 10^{-2} c$, well below $c$. The "superluminal" language is somewhat misleading; it's more accurate to say that the **ionized region expands very rapidly in comoving coordinates** due to the low density providing little resistance.

### Resolution Requirements

To resolve an I-front accurately (as needed for precise temperature and density profiles), simulations require grid spacing:

$$\Delta x \lesssim 0.1 \Delta x_\text{rec} \sim 1 \text{ pc (comoving)}$$

For a 95 Mpc box, this requires:
$$N \sim (95 \times 10^6 \text{ pc}) / (1 \text{ pc}) = 10^8 \text{ grid points}$$

This is a $\sim 500^3$ or finer grid, pushing modern simulations to the limit of feasibility. Most production simulations use coarser grids ($128^3$–$256^3$) and accept some blurring of the I-front.

This tension between resolution requirements and computational cost is a key reason why **EFT-based approaches are attractive**: if one can extract large-scale statistics (power spectrum, correlation functions) without perfectly resolving I-fronts, the cost drops dramatically.

## Connections to This Thesis

The understanding of radiative transfer physics — what it captures, what it approximates, and how much it costs — directly motivates the [[Effective Field Theory]] approach in this thesis:

- **Full RT is too slow** to generate training data for machine learning: the EFT and semi-numerical codes are the practical compromise
- **Semi-numerical codes make systematic approximations** (excursion set, no propagation geometry): the EFT coefficients absorb these approximation errors
- **RT codes have converged on morphology** (inside-out, percolation): this gives confidence that large-scale features are robust across simulation methods
- **Mean free path is uncertain** (parameter degeneracy in semi-numerical codes): the EFT is designed to absorb this uncertainty into its structure
