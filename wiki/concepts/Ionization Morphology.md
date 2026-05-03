---
type: concept
title: "Ionization Morphology"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/physics
  - domain/reionization
status: developing
domain: "[[Reionization Physics]]"
related:
  - "[[Neutral Fraction]]"
  - "[[Bubble Size Distribution]]"
  - "[[Excursion Set Formalism]]"
  - "[[Mean Free Path]]"
  - "[[Effective Field Theory]]"
  - "[[21cm Cosmology]]"
sources:
  - "[[Ferrara & Pandolfi (IGM Reionization)]]"
  - "[[Trac & Gnedin 2009 (Reionization Simulations)]]"
  - "[[Gnedin & Madau 2022 (Modeling Reionization)]]"
---

# Ionization Morphology

## What It Is

The **ionization morphology** is the spatial structure of the ionization field $x_\text{HII}(\mathbf{x}, z)$ — where ionized bubbles are located, what sizes and shapes they have, how they are distributed relative to the underlying matter density field, and how this topology evolves as reionization proceeds. It is the "three-dimensional shape and topology of the ionized universe" at a given cosmic epoch.

Understanding morphology is central to 21 cm cosmology because the power spectrum $P_\text{21cm}(k)$ encodes morphological information: large-scale power reflects bubble size and spatial clustering, while small-scale power reflects internal bubble structure. The morphology also determines all four EFT bias coefficients and the leading-order error term $P_{\varepsilon\varepsilon}$.

## Inside-Out Reionization

Reionization proceeds **inside-out**: dense, biased regions near clustered galaxies ionize first; underdense voids ionize last. This is not a universal principle — it follows from the underlying physics of source distributions and the excursion-set criterion.

### Physical Mechanism

The excursion-set ionization criterion,

$$\zeta \cdot f_\text{coll}(\mathbf{x}, R) \geq 1,$$

requires that the *number* of ionizing photons from collapsed matter within radius $R$ exceeds the *number* of hydrogen atoms within $R$. In an overdense region:
- $f_\text{coll}$ is higher (more massive halos per volume)
- Hence more ionizing photons per unit volume
- The criterion is satisfied at a smaller radius $R$
- Bubbles grow faster

Conversely, in a void:
- $f_\text{coll}$ is lower
- Fewer photons per unit volume
- A larger radius is needed to satisfy the criterion
- Bubble growth is slow; voids remain neutral until late

### Observational Evidence for Inside-Out

- **Lyman-alpha emitter (LAE) clustering:** LAEs cluster ~2–4× more strongly than the underlying matter, indicating strong bias. If reionization were "outside-in" (voids ionizing first), LAEs (which preferentially live in dense regions) would be invisible at early epochs — contradicting observations.
- **Gunn-Peterson trough:** The rapid evolution at $z \approx 5.5$–$6.5$ is consistent with percolation dynamics (all-or-nothing connectivity), not gradual "outside-in" ionization.
- **Full radiative transfer simulations:** THESAN, C$^2$-Ray, GADGET-3/SUNSET all confirm inside-out morphology when ionizing sources follow the matter distribution.

The alternative "outside-in" scenario (fewer recombinations in low-density gas) is physically disfavored because photon absorption (Lyman-limit systems) and radiative recombination are both distributed throughout the IGM; inside-out bias from source clustering dominates.

## Three Morphological Stages

As $\bar{x}_\text{HII}$ evolves from 0 to 1, the ionization field undergoes distinct topological transitions:

### Stage 1: Pre-Overlap ($\bar{x}_\text{HI} \gtrsim 0.7$, $z \gtrsim 7$)

- Small, isolated ionized bubbles centered on individual galaxy clusters and overdense regions
- Bubble radius distribution peaks at small scales: $R_\text{eff} \sim 0.5$–$2\,\text{Mpc}$
- Bubbles are nearly spherical and non-overlapping; the ionized volume has a "Swiss cheese" morphology with the neutral phase as the continuous matrix
- Bubble separation is large; sources are widely spaced
- The power spectrum is dominated by bubble-scale fluctuations; the 21 cm signal is anticorrelated with density (bright regions are ionized voids with fewer sources)

**Quantitative signatures:**
- Bubble number density $n_\text{bubble} \sim (\bar{x}_\text{HII})^3$ roughly scales with the ionized fraction
- Typical sizes: 0.3–2 Mpc comoving
- Variance of $x_\text{HII}$ is large: $\sigma_x^2 \sim \bar{x}_\text{HII}(1-\bar{x}_\text{HII})$ is maximized near 50%

### Stage 2: Percolation ($\bar{x}_\text{HI} \sim 0.5$, $z \sim 7$–$8$)

- Bubbles grow and begin merging; the ionized network becomes topologically connected across the simulation box
- This is a **percolation transition**, analogous to a phase transition in statistical physics
- Below the percolation threshold, ionized bubbles are isolated; above it, they form a spanning cluster
- The percolation transition produces a rapid change in large-scale topology: the ionized phase transitions from disconnected "islands" to a connected "network"
- Large-scale power in $P_\text{21cm}(k)$ grows rapidly as the ionized structure acquires long-range correlations

**Minkowski Functionals and Topological Characterization:**

The **Minkowski functionals** provide a rigorous topological description complementary to power spectra:

$$V_0 = \text{Volume of ionized region}$$
$$V_1 = \text{Surface area of ionization boundary}$$
$$V_2 = \text{Mean curvature integral}$$
$$V_3 = \text{Euler characteristic} = \#(\text{connected components}) - \#(\text{holes}) + \ldots$$

During reionization:
- $V_0 \propto \bar{x}_\text{HII}$ grows monotonically
- $V_1$ (surface area) peaks near percolation; above percolation it decreases as bubbles merge and boundaries become simpler
- $V_3$ (Euler characteristic) drops sharply at percolation: many small disconnected bubbles ($V_3$ large) → one giant spanning cluster ($V_3$ small)

These topological measures are measurable in principle from 21 cm maps and are highly sensitive to the morphological stage.

### Stage 3: Post-Overlap ($\bar{x}_\text{HI} \lesssim 0.2$, $z \lesssim 6.5$)

- Ionized phase is a nearly continuous network; remaining neutral gas is confined to dense, well-shielded regions: Lyman-limit systems, dense filaments, and voids
- Bubble size distribution broadens to larger scales: $R_\text{eff} \sim 10$–$50\,\text{Mpc}$
- The UV background becomes spatially uniform; local fluctuations in ionizing photon flux are small relative to the mean
- The 21 cm signal is now dominated by density and temperature fluctuations, not ionization patchiness
- EFT description is more reliable: $\ell_x \sim R_\text{eff}$ is now larger than the smallest scales of interest, so the perturbative expansion is valid to higher $k$

**Photon Budget Constraint:**

Post-overlap, the ionizing photon budget is tight. Barely enough photons are produced to reionize by $z \sim 6$. The photon budget equation is:

$$\dot{n}_\text{ion} = \dot{n}_\text{rec} + \frac{d}{dt}\left[n_\text{H}(1-\bar{x}_\text{HI})\right]$$

where $\dot{n}_\text{ion}$ is the ionizing photon production rate (from galaxies and quasars), and $\dot{n}_\text{rec} \propto C \cdot n_e n_p$ accounts for recombinations (with clumping factor $C \sim 3$). The late reionization epoch requires $f_\text{esc} \sim 0.1$–$0.2$ (escape fraction from galaxies), which is difficult to achieve with realistic galaxy physics.

## Key Morphological Scales

### Characteristic Bubble Radius: $R_\text{eff}$

The **effective bubble radius** is the scale on which the ionization field has its strongest fluctuations. It is determined by the excursion-set criterion and evolves with $\bar{x}_\text{HII}$:

$$R_\text{eff}(\bar{x}_\text{HII}) \equiv \text{radius where } \zeta f_\text{coll}(R) \sim 1$$

As $\bar{x}_\text{HII}$ increases, sources become denser and more efficient, so bubbles must grow larger to maintain $\zeta f_\text{coll} \sim 1$. Typical evolution:

| $\bar{x}_\text{HII}$ | $R_\text{eff}$ | Redshift |
|------|------|------|
| 0.01 | 0.3 Mpc | $z \sim 12$ |
| 0.1 | 1 Mpc | $z \sim 10$ |
| 0.5 | 15 Mpc | $z \sim 7$ |
| 0.95 | 50+ Mpc | $z \sim 6$ |

This scale enters the EFT bias coefficient:

$$b_{\nabla^2}^x \approx -\frac{R_\text{eff}^2}{3}$$

Thus measuring $b_{\nabla^2}^x$ from 21 cm power spectra directly constrains the bubble morphology.

### Mean Free Path: $\lambda_\text{MFP}$ or $R_\text{mfp}$

The [[Mean Free Path]] sets an upper cutoff on bubble growth in the excursion-set algorithm. Physically, photons cannot propagate beyond $R_\text{mfp}$ in neutral gas due to absorption by Lyman-limit systems. At $z \sim 6$, observational constraints give $R_\text{mfp} \sim$ few Mpc; extrapolation to $z > 8$ is uncertain but suggests $R_\text{mfp}$ decreases at higher $z$ as $(1+z)^{\gamma}$ with $\gamma \sim 4$–$5$.

### Mean Source Separation: $d_\text{SRC}$

The typical distance between ionizing sources (galaxies and quasars) is set by the galaxy number density. At redshifts $z \sim 6$–$7$, galaxies with halo masses $M \gtrsim 10^{10}\,M_\odot$ have a comoving separation of $d_\text{SRC} \sim$ few Mpc.

The **overlap epoch** occurs when $d_\text{SRC} \lesssim R_\text{mfp}$ — at that point, bubbles from neighboring sources begin to touch and merge, triggering percolation. This criterion links the source distribution, photon physics, and the morphological stage.

## Simulator Dependence of Morphology

Different codes produce different ionization morphologies even at the **same global $\bar{x}_\text{HII}(z)$**. This is a crucial source of systematic uncertainty:

### Semi-Numerical Codes (21cmFAST, SCRIPT)

**Algorithm:** Excursion-set criterion applied to smoothed density and collapsed fraction fields.

**Morphological properties:**
- Large, smooth ionized bubbles with sharp boundaries
- Uniform interior (fully ionized)
- Limited sub-bubble structure; no ionization fronts or transition regions

**Typical bubble size distribution** at $\bar{x}_\text{HII} = 0.3$:
- Peak at $R \sim 5$–$8\,\text{Mpc}$
- Long tail toward large $R$ (rare giant bubbles)
- Sharp lower cutoff (sources are discrete)

### Full Radiative Transfer (THESAN, C$^2$-Ray, SUNSET)

**Algorithm:** Direct photon propagation through adaptive mesh; tracks each photon's path and ionization impact.

**Morphological properties:**
- Complex, irregular bubble shapes (constrained by matter distribution)
- Partially-ionized transition regions ("ionization fronts") with thickness $\sim 10$–$100\,\text{kpc}$
- Rich temperature structure (ionized regions hotter due to photoheating)
- Self-consistent photon escape and recombination

**Typical bubble size distribution** at $\bar{x}_\text{HII} = 0.3$:
- Peak at $R \sim 3$–$5\,\text{Mpc}$ (smaller than 21cmFAST)
- More asymmetric/non-spherical bubbles
- Smoother transition to background
- Better correlation with density peaks

### Quantitative Differences

At fixed $\bar{x}_\text{HII} = 0.3$ ($z \sim 8$–$8.5$), the median bubble sizes differ by ~20–50%:
- 21cmFAST: $R_\text{eff} \sim 6$–$8\,\text{Mpc}$
- THESAN/C$^2$-Ray: $R_\text{eff} \sim 3$–$5\,\text{Mpc}$

This difference translates to EFT coefficients:

$$\Delta b_{\nabla^2}^x \approx -\frac{1}{3}(R_{\text{21cm}}^2 - R_\text{full-RT}^2) \sim -30\text{ to } -50$$

This is **measurable** in 21 cm power spectra and is a primary prediction of P1: the $k \sim 0.1$–$0.3\,\text{Mpc}^{-1}$ tail of the power spectrum should differ visibly between 21cmFAST-based and full-RT-based cosmologies at the same reionization history.

## Power Spectrum Morphology Encoding

The 21 cm power spectrum encodes morphological information across scales:

### Large Scales ($k \lesssim 0.05\,\text{Mpc}^{-1}$)

Power grows as bubbles merge and create large-scale correlations in the ionized network. At percolation, the long-wavelength power jumps sharply because a spanning cluster of ionized matter develops long-range coherence.

### Intermediate Scales ($k \sim 0.05$–$0.2\,\text{Mpc}^{-1}$)

The **power spectrum "knee"** or turnover occurs near $k \sim 1/R_\text{eff}$. This is the characteristic scale of bubble size. The position of this knee directly reflects $R_\text{eff}$ and shifts to smaller $k$ as reionization progresses (bubbles grow).

### Small Scales ($k \gtrsim 0.3\,\text{Mpc}^{-1}$)

Small-scale power decreases as the ionized field becomes smoother and longer-wavelength fluctuations dominate. The cutoff scale is set by source discreteness and the finite thickness of ionization fronts.

## Percolation and the Phase Transition

At $\bar{x}_\text{HII} \sim 0.5$ (roughly $z \sim 7$–$7.5$), the ionized phase undergoes a **percolation transition**. Below this threshold, ionized bubbles are isolated; above it, they form a spanning cluster that geometrically connects across the entire volume.

This transition is sharp in topological measures (Euler characteristic, genus) but gradual in power spectra. It has profound implications:
- UV background becomes more uniform above percolation (fewer shadowed regions)
- Large-scale power grows rapidly
- The ionization field transitions from "patchy" (high variance) to "mostly ionized with small voids" (lower variance)

Observationally, evidence for percolation at $z \sim 6$–$7$ comes from the rapid transition in the Gunn-Peterson optical depth and LAE visibility.

## Ionizing Background Post-Percolation

Once percolation occurs, the ionizing photon background becomes spatially pervasive. Individual HII regions merge into a nearly uniform ionizing UV background with small residual fluctuations set by local source clustering and recombination.

This regime is relevant for the standard picture of reionization: by $z \sim 6$, the entire IGM is under a UV background so strong that neutral gas only survives in the highest-density regions. The subsequent "dark ages" are truly dark because the ionizing background has reionized all but the most protected neutral structures.

## Connection to EFT

The ionization morphology determines all four EFT bias coefficients of the ionization field:

$$\delta_x = x_\text{HII}(\mathbf{x}) - \bar{x}_\text{HII}$$

- **$b_1^x$:** Large-scale ionization bias; depends on how $x_\text{HII}$ correlates with matter density (inside-out bias and galaxy clustering)
- **$b_2^x$:** Non-linear and patchiness effects; encodes how ionization responds to local density curvature
- **$b_{\nabla^2}^x$:** Bubble scale effects; directly proportional to $R_\text{eff}^2$
- **$P_{\varepsilon\varepsilon}$:** Shot noise from bubble discreteness; larger bubbles → larger shot noise

The power spectrum error (EFT remainder) $P_\text{err}/P_\text{ion}$ as a function of wavenumber $k$ directly shows where the perturbative description breaks down:

$$P_\text{err}(k) \sim 1 \text{ at } k \sim 1/R_\text{eff}$$

This is the critical signature that EFT extractions must address: accurately measure EFT coefficients requires staying in the regime where $k$ is smaller than the break scale $k_\text{break} \sim 1/R_\text{eff}$.

## See Also

- [[Excursion Set Formalism]] — the physical mechanism that produces inside-out morphology
- [[Bubble Size Distribution]] — quantitative description of bubble sizes
- [[Mean Free Path]] — the cutoff scale for bubble growth
- [[Neutral Fraction]] — the global measure; morphology describes the spatial structure
- [[Effective Field Theory]] — how morphology translates to EFT coefficients
- [[21cm Cosmology]] — how morphology appears in observable power spectra
