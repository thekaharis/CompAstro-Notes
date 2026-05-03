---
type: source
title: "Trac & Gnedin 2009 — Computer Simulations of Cosmic Reionization"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/simulation
  - domain/radiative-transfer
  - source/review
status: mature
source_type: paper
author:
  - "[[Trac, Hy]]"
  - "[[Gnedin, Nickolay Y.]]"
date_published: 2009
url: "https://arxiv.org/abs/0906.4348"
confidence: high
key_claims:
  - "Three radiative transfer methods (moments/M1, Monte Carlo, ray-tracing) have converged on consistent reionization morphologies despite algorithmic differences"
  - "Quasars alone cannot reionize the universe by z=6; ionizing photon output is insufficient by factor ~100"
  - "Star-forming galaxies dominate the ionizing photon production; quasar contribution relegated to heating/feedback"
  - "The mean free path from Lyman-limit systems and the mean galaxy separation are the two key characteristic scales governing the overlap epoch"
  - "Photon conservation is the critical algorithmic requirement; codes that violate it produce spurious ionization morphologies"
  - "Semi-numerical codes like 21cmFAST (developed after this review) approximate the full RT results surprisingly well"
related:
  - "[[Simulation and Codes]]"
  - "[[Radiative Transfer]]"
  - "[[Reionization Physics]]"
  - "[[Neutral Fraction]]"
  - "[[Ionization Morphology]]"
  - "[[Gnedin & Madau 2022 (Modeling Reionization)]]"
---

# Trac & Gnedin 2009 — Computer Simulations of Cosmic Reionization

> [!key-insight]
> A focused, authoritative review of numerical methods for simulating cosmic reionization — coupling N-body structure formation with radiative transfer — establishing that despite very different algorithmic approaches, modern RT codes converge on consistent pictures of reionization morphology, sources, and sinks.

## Citation

Trac, H. & Gnedin, N. Y. (2009). "Computer Simulations of Cosmic Reionization." arXiv:0906.4348.

## Core Claim

Cosmic reionization can be robustly simulated by coupling dark matter structure formation with radiative transfer of ionizing photons. The three major RT approaches — **moments/M1**, **Monte Carlo**, and **ray-tracing** — have converged on qualitatively consistent pictures of the reionization process:

1. **Star-forming galaxies**, not quasars, dominate ionizing photon production
2. **Inside-out morphology**: high-density regions ionize first, voids last
3. **Characteristic scales** set by the mean free path and mean galaxy separation are ~few Mpc
4. **Photon conservation** is the critical algorithmic requirement

This review pre-dates 21cmFAST v1 (2011) and SCRIPT, the semi-numerical codes that later became dominant. It establishes the "ground truth" from full RT simulations against which semi-numerical codes can be validated.

## Part I: N-Body and Structure Formation Foundations

### Matter and Galaxy Distribution

**Initial conditions:**
- Start with linear density perturbations set by inflation
- Evolve with N-body simulation (DM particles) or SPH (particles + gas)
- Identify halos via friend-of-friends or spherical overdensity
- Compute halo mass function, apply abundance matching or SAM for galaxy properties

**Halo-based source model:**
- Star formation occurs in halos above a threshold mass (atomic cooling: $M > 10^8 M_\odot$, or molecular cooling threshold)
- Ionizing photon production per halo is proportional to stellar mass (or halo mass via abundance matching)
- Photons propagate from halo positions through the IGM

**Key result**: The **mean galaxy separation** scales as:
$$d_\text{SRC} = \left(\frac{\bar{n}_H}{n_\text{SRC}}\right)^{1/3} \sim 1\text{–}5 \text{ Mpc} \quad \text{(at } z \sim 6\text{)}$$

This is the **characteristic scale of ionized bubble overlap**. When bubbles from different sources start to touch ($d_\text{SRC} \sim \lambda_\text{MFP}$), the ionized volume grows rapidly to percolation.

### Halo Bias and Clustering

Halos (and hence galaxies) cluster more strongly than the underlying dark matter:
$$\delta_h(\mathbf{k}) = b_h(z, k) \delta_m(\mathbf{k})$$

where the bias $b_h$ is scale-dependent and increases at large scales.

**Implication for ionization**: Since ionized regions are located at halos, the ionization field inherits the bias of the halo distribution:
$$\delta_x = (b_x) \delta_m + ...$$

This is exactly what P1 aims to measure via EFT bias coefficients.

## Part II: Radiative Transfer Algorithms

### Three Major RT Approaches

#### **1. Moments Methods (M1, Eddington Approximation)**

**Idea**: Reduce the full RT equation to conservation laws for photon energy density and flux.

**Full RT equation** (too expensive to solve explicitly):
$$\frac{\partial I_\nu}{\partial t} + c\,\mathbf{\hat{n}} \cdot \nabla I_\nu + \text{(redshifting, absorption, scattering)} = 0$$

where $I_\nu$ is the specific intensity (function of position, direction, frequency — 5D).

**Moments reduction**: Define intensity moments:
$$E = \int \frac{I_\nu}{c} d\Omega d\nu \quad \text{(energy density)}$$
$$\mathbf{F} = \int \mathbf{\hat{n}} \frac{I_\nu}{c} d\Omega d\nu \quad \text{(flux)}$$

Equations for $E$ and $\mathbf{F}$:
$$\frac{\partial E}{\partial t} + \nabla \cdot \mathbf{F} = \text{(source, sink)}$$
$$\frac{\partial \mathbf{F}}{\partial t} + c^2 \nabla P = -c^2 \nabla P_0 + \text{...}$$

**Closure** (Eddington approximation): Relate second moment (pressure) to lower moments:
$$P_\text{rad} \approx \frac{E}{3}$$

This is exact for isotropic radiation, approximate for beamed radiation.

**Advantages**:
- Reduced dimensionality (5D → 3D)
- Relatively fast: scales as $\mathcal{O}(N_\text{grid}^3)$ per timestep
- High dynamic range: can handle both optically thin and thick regimes

**Disadvantages**:
- Closure approximation not perfect; anisotropic radiation handled poorly
- Photon direction information lost (can't track shadows accurately)

**Convergence**: M1 method (Gnedin 2003) and variants show ~10–20% accuracy on bubble sizes and morphology compared to more exact methods.

#### **2. Monte Carlo RT**

**Idea**: Stochastically sample photon packets; track each packet from source until absorption.

**Algorithm**:
1. Generate photon packet at source halo with energy $E_\gamma$ and direction sampled from source spectrum/pattern
2. Propagate packet through domain, stepping through cells
3. At each step, compute probability of absorption/scattering
4. If absorbed, deposit energy (heat, ionize gas)
5. Repeat for many packets

**Computational cost**:
- Per packet: $\mathcal{O}(\text{path length})$ operations
- Total: $\mathcal{O}(N_\text{packets} \times \text{path length})$
- Very expensive for large volumes (scales poorly with box size)

**Advantages**:
- Naturally handles complex geometry (shadows, multi-scattering)
- No closure approximation needed; exact (within noise)
- Easy to parallelize (independent packets)

**Disadvantages**:
- Computationally expensive; limited to smaller volumes ($\sim 100$ Mpc)
- Shot noise: need many packets for smooth statistics

#### **3. Ray-Tracing**

**Idea**: Cast rays from each source; compute what each ray ionizes.

**Algorithm**:
1. For each source, identify rays pointing outward in a cone/sphere
2. Trace each ray through the domain, computing ionization along path
3. Accumulate ionization from all rays at each location

**Advantages**:
- Exact for optically thin regime (limited recombination)
- Fast: scales as $\mathcal{O}(N_\text{sources} \times N_\text{rays})$
- Handles complex source geometries well

**Disadvantages**:
- Breaks down when sources blend (overlap regime) due to double-counting
- Photon number conservation not enforced; can violate energy conservation
- Poor for optically thick regime (non-linear recombination)

### Photon Conservation: Critical Requirement

**The core challenge**: In a recombining medium, photon production and loss must balance exactly to get correct ionization evolution.

**Violation examples**:
- Ray-tracing without photon counting: doesn't enforce $\sum \text{ionizing photons} = $ sinks
- Some Monte Carlo implementations: shot noise prevents exact counting
- Moments methods with poor closure: spurious energy transport

**Test of photon conservation**: Integrate ionization over all space, compute net photon production rate, compare to recombination sink.

**Results from Iliev et al. (2006) code comparison**:
- **Conservative methods** (M1, improved Monte Carlo): photon conservation within 5% ✓
- **Non-conservative** (basic ray-tracing, some older codes): errors ~20–50% ✗

**Impact on morphology**: Codes that violate photon conservation produce spurious ionized regions and incorrect bubble morphologies.

## Part III: Key Results and Comparisons

### Source: Quasars vs. Galaxies

**Ionizing photon production rates** (per comoving Mpc³ at z ~ 6):

| Source type | Production rate | Required rate for EoR |
|---|---|---|
| Galaxies (UV) | ~10⁵ photons Mpc⁻³ s⁻¹ | ~10⁵ (required) |
| Quasars | ~10³ photons Mpc⁻³ s⁻¹ | ~10⁵ (needed) |
| Ratio | Galaxies / Quasars | **~100:1** |

**Conclusion**: Quasars produce ~100 times fewer ionizing photons than needed to reionize by z=6. Even with optimistic assumptions on quasar duty cycle and spectrum, they fall short by factor ~3–5.

**Historical significance**: This settles decades of debate (pre-2009) about whether quasars could reionize the universe. They cannot (or at best, contribute ~10–20%). Galaxies must dominate.

### Sinks: Recombination and Absorption

**Sink 1: Clumpy gas recombination**

In a clumpy IGM, recombination is enhanced by density clumping:
$$\dot{n}_\text{rec} = C(z) \alpha_B(T) n_e n_\text{H}$$

Clumping factor $C$ varies significantly:
- **Early epochs** ($z > 12$, before reionization): $C \sim 30$–50 (very clumpy gas)
- **During EoR** ($z \sim 6$–8): $C \sim 5$–10 (partially ionized, gas still collects in filaments)
- **After EoR** ($z < 5$): $C \sim 1$–2 (ionized gas becomes more uniform)

**Effect on ionization timescale**: Higher $C$ increases recombination sink, slows ionization. Clumping factor determines how long reionization lasts.

**Sink 2: Lyman-limit systems**

Absorption of ionizing photons in Lyman-limit absorbers (optically thick systems with $N_\text{HI} > 10^{17}$ cm⁻²):

- **Number density**: $n_\text{LL} \sim 0.1$–0.5 $(1+z)^2$ cm⁻³
- **Cross-section**: $\sigma_\text{LL}(\nu) \sim 10^{-18}$ cm² at ionization edge
- **Mean free path**: $\lambda_\text{MFP} = (n_\text{LL} \sigma_\text{LL})^{-1} \sim 5$–20 Mpc

Lyman-limit systems are **self-shielding**: photons get absorbed in the dense core, limiting ionization depth. This sets the **size of ionized bubbles**.

**Key scale**: Mean free path $\lambda_\text{MFP}$ is the characteristic ionized bubble size — exactly what is parameterized as $R_\text{mfp}$ in 21cmFAST!

### Morphology Convergence

**Test setup** (Iliev et al. 2006 code comparison):
- 100 Mpc³ box, identical cosmology, sources, initial conditions
- Run through 5 different RT codes (moments, Monte Carlo, ray-tracing variants)
- Compare ionization morphology at $z = 7$ (mid-reionization)

**Results**:
- **Bubble morphology**: Inside-out topology confirmed in all codes (ionize overdensities first)
- **Bubble size distribution**: Agreement to ~30% across codes; slight variations due to algorithm differences
- **Correlation functions**: Power spectrum shape consistent across codes
- **Two-point topology**: All show similar morphology (filaments, voids, clusters)

**Conclusion**: Despite very different numerical approaches, all RT codes converge on the same **qualitative picture**. Quantitative differences are small (few tens of percent).

This gives confidence that **the physics of reionization is robust** — not an artifact of one code's specific choices.

## Part IV: Grid vs. Particle Codes

### Eulerian (Grid-Based) Codes

**Examples**: C2-Ray, ATON, GADGET-RT (with grid)

**Advantages**:
- Natural for IGM evolution (gas dynamics)
- Efficient for RT (ray-casting on Cartesian grid)
- Good angular resolution for directional RT effects

**Disadvantages**:
- Poor halo resolution (limited dynamic range)
- Lagrangian codes better resolve star-forming regions

### Lagrangian (SPH, Particle-Based) Codes

**Examples**: GADGET (smoothed particle hydrodynamics)

**Advantages**:
- Naturally adaptive: more particles in dense regions
- Excellent halo and star formation region resolution
- Natural for cosmological simulations

**Disadvantages**:
- RT on particles is awkward (particles don't naturally form a grid)
- More expensive for large volumes

### Adaptive Mesh Refinement (AMR)

**Combines advantages**: Use grid at coarse level, refine around halos and ionization fronts.

**Examples**: ENZO (with RT module), RAMSES

- Best dynamic range
- Most expensive
- Gold standard for detailed morphology

## Connection to This Thesis

### Relevance to P1 (EFT bias measurements)

**Fundamental validation:**

This 2009 review establishes that full RT simulations **converge on consistent ionization morphologies**. This convergence is the reason to expect that EFT bias coefficients (which depend on morphology) should also be well-defined and similar across different RT codes.

Conversely, if EFT coefficients differ dramatically between codes, that would suggest the RT algorithms produce fundamentally different physics — contradicting the convergence shown here.

**Specific connection**: The "bubble sizes agree to ~30%" statement means that the **scale-dependence** of the ionization bias (captured in the EFT expansion) should be similar across codes to within ~30%. P1 tests whether this holds for 21cmFAST vs. SCRIPT.

### Relevance to P2 (EFT-based parameter inference)

**Indirect but important context:**

P2 assumes that EFT coefficients measured from simulators can be mapped back to astrophysical parameters ($\zeta, T_\text{vir}, R_\text{mfp}$). This mapping is justified if EFT coefficients are **more universal** than raw morphologies.

Trac & Gnedin show that despite different RT codes producing ~30% differences in bubble sizes, the **global ionization history** (main curve of $x_\text{HII}(z)$) is very similar. This suggests that **global properties** are more universal than local details.

**P2's hypothesis extends this**: If global properties are universal, then **large-scale structure** (captured by EFT) should be even more universal than bubble details. This motivates P2's focus on EFT.

### Comparison: Full RT vs. Semi-Numerical Codes

This review predates semi-numerical codes, but the **comparison is revealing**:

- **Full RT** (this review): high fidelity, small volumes (~100 Mpc), weeks to months per simulation
- **Semi-numerical** (21cmFAST, SCRIPT, post-2009): approximate RT, large volumes (~Gpc), minutes per simulation
- **Trade-off**: Semi-numerical codes sacrifice small-scale fidelity for speed and volume

The fact that semi-numerical codes were later developed and found to match global properties (and even rough morphology) suggests that the approximations they make preserve the **essential physics** for EFT purposes.

## Key Equations

**Mean free path** (from Lyman-limit absorption):
$$\lambda_\text{MFP} = \left[ n_\text{LL}(z) \sigma_\text{LL}(\nu) \right]^{-1}$$

where $n_\text{LL} \sim 0.1$–0.5 $(1+z)^2$ cm⁻³ and $\sigma_\text{LL} \sim 10^{-18}$ cm².

**Mean galaxy separation**:
$$d_\text{SRC} = \left(\frac{\bar{n}_H}{n_\text{SRC}}\right)^{1/3}$$

where $n_\text{SRC}$ is the galaxy number density.

**Recombination rate** (clumpy):
$$\dot{n}_\text{rec} = C(z) \alpha_B(T) \bar{n}_H^2 (1+z)^3$$

**Moments equation** (M1 closure):
$$\frac{\partial E}{\partial t} + c \nabla \cdot \mathbf{F} = -\text{(source, sink)}$$

**Photon conservation** (integral check):
$$\int_{\text{box}} n_{\text{ion}} d^3x = \int_{\text{sources}} N_\gamma dt - \int_{\text{sinks}} \dot{n}_\text{rec} dt$$

## Methods

**Review structure:**
- 19 pages, arXiv preprint (later published in Gnedin & Madau 2022 extension)
- Synthesizes existing RT simulations from literature
- No new simulations presented; focus is on comparison and methodology

**Key references cited:**
- Iliev et al. (2006): code comparison benchmark
- Gnedin (2003, 2010): M1 moments method
- Furlanetto & Oh: analytic models
- Bromm & Larson: galaxy formation context

## Limitations and Caveats

**What this paper does NOT cover:**

1. **Feedback mechanisms**: Photoheating feedback on galaxy formation, radiation pressure, etc., are mentioned but not detailed. How much does feedback affect the reionization history?

2. **Spectral dependence**: Treats ionizing photons as single energy bin. Real sources have spectra spanning 13.6 eV to >100 eV, with complex absorption dependencies.

3. **Metals and lines**: Metal absorption (He, C, O, Fe) not included. Metallicity evolution not addressed.

4. **AGN contributions**: Quasars discussed only for photon production. AGN feedback and X-ray heating touched upon but not modeled.

5. **High-$z$ structure** (z > 15): Focus is on overlap epoch; very early reionization (if it occurs) not addressed.

**Assumptions that may break:**

1. **Constant escape fraction**: Assumes $f_\text{esc}$ is fixed. Real galaxies likely have mass-dependent and redshift-dependent escape fractions.

2. **Halo-based sources**: Assumes all sources are in halos above threshold. Might miss dwarf galaxies or first stars in minihalos.

3. **Homogeneous clumping**: Clumping factor $C$ is global or $z$-dependent only. Actually depends on scale and local density structure.

## Figures Worth Noting

**Fig. 1:** Transmitted fraction from high-$z$ QSO spectra
- Shows rapid transition from transmission (~1%) to Gunn-Peterson trough (complete absorption)
- Canonical evidence that reionization ends ~z=6

**Fig. 2:** Ionizing photon production rates vs. redshift
- Galaxies dominate: 10⁵ vs. 10³ photons for quasars
- Quantitatively shows why quasars alone fail

**Fig. 3:** Two-point correlation function of galaxies vs. dark matter
- Shows galaxy clustering excess compared to matter
- Motivates halo bias and inside-out ionization topology

**Fig. 4 (Iliev et al. reference):** Ionization morphology snapshots from different RT codes
- Shows convergence: all codes produce inside-out morphology
- Bubble sizes similar across codes (~30% variation)

## Open Questions After Reading

> [!gap]
> **Photon conservation in semi-numerical codes**: 21cmFAST and SCRIPT don't perform explicit RT. Do they conserve photons implicitly (via the excursion-set algorithm)? Or is there an inherent photon loss/gain that affects EFT coefficients?

> [!gap]
> **Small-scale morphology and EFT validity**: Trac & Gnedin show bubble sizes agree to ~30% across RT codes. Is this 30% variation within the EFT error budget, or is it too large? Does EFT break down for mildly nonlinear scales ($k \sim 0.1$–0.3 Mpc⁻¹)?

> [!gap]
> **Clumping factor universality**: The clumping factor varies across codes. Is there a systematic dependence (e.g., grid resolution)? And how does this translate to differences in EFT coefficients?

> [!gap]
> **Semi-numerical vs. full RT**: How well do 21cmFAST and other semi-numerical codes reproduce the RT morphologies shown in this review? Are EFT coefficients measured from 21cmFAST consistent with those from full RT codes?

> [!gap]
> **Lyman-limit systems as a tunable parameter**: $R_\text{mfp}$ (related to mean free path) is a key 21cmFAST parameter. How sensitive is the ionization morphology to $R_\text{mfp}$? And does variation match the ~30% morphological variance shown by Iliev et al.?
