---
type: concept
title: "Excursion Set Formalism"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/theory
  - domain/reionization
  - domain/simulation
status: developing
domain: "[[Reionization Physics]]"
related:
  - "[[Neutral Fraction]]"
  - "[[Clumping Factor]]"
  - "[[Ionization Morphology]]"
  - "[[Bubble Size Distribution]]"
  - "[[Simulation and Codes]]"
  - "[[Mean Free Path]]"
sources:
  - "[[Choudhury 2022 (Reionization Intro)]]"
  - "[[Gnedin & Madau 2022 (Modeling Reionization)]]"
---

# Excursion Set Formalism

## What It Is

The excursion set formalism is an elegant analytic and semi-numerical method for computing the statistical properties of collapsed structures. Originally developed for dark matter halos in the 1970s-1980s (Press-Schechter, Bond et al., Sheth-Tormen), it has been adapted in the 21st century to model ionized bubble growth during cosmic reionization. The approach replaces the computationally expensive full radiative transfer problem with a criterion applied to smoothed density and collapsed fraction fields, making it tractable for large-volume simulations and parameter surveys.

The key insight is that by smoothing the density field at progressively smaller scales, one can trace a **random walk in density-weighted wavenumber space**, where the first passage through a barrier (the collapse threshold) determines when a structure forms. For bubbles, the "barrier" is a stochastic ionization criterion rather than a fixed threshold.

## Random Walk Interpretation: Density Smoothing and First Crossing

### The Core Picture

Consider the density contrast field $\delta(\mathbf{x}, z)$ at a position $\mathbf{x}$ and redshift $z$. When we smooth this field on a mass scale $M$, we obtain:

$$\delta_M(\mathbf{x}, z) = \int_V \frac{d^3k}{(2\pi)^3}\,P(k,z)\,W(k,R_M)\,e^{i\mathbf{k}\cdot\mathbf{x}}$$

where $R_M = (3M/4\pi\rho_m)^{1/3}$ is the comoving radius corresponding to mass $M$, and $W(k,R_M)$ is a smoothing kernel (commonly a top-hat or Gaussian). The variance of this smoothed field is:

$$\sigma^2(M, z) = \int_0^\infty \frac{dk}{2\pi^2}\,k^2\,P(k,z)\,W^2(k,R_M)$$

where $P(k,z)$ is the power spectrum at redshift $z$ (often linearly extrapolated for convenience).

### The Random Walk Property

The crucial observation is that $\sigma(M)$ increases monotonically as $M$ decreases (smaller scales have more power). Thus, as we scan smoothing scales from very large $M$ downward to smaller $M$, the smoothed field $\delta_M$ traces out **a random walk in the $(\log M, \sigma)$ plane**, with the walk's trajectory determined by the correlation structure of the density field.

The first passage through a barrier $\sigma = \sigma_c(z)$ (where $\sigma_c(z) = \delta_c(z)/D(z)$ for the Press-Schechter case) determines when a halo "collapses." The fraction of matter in halos more massive than $M$ is then the probability that the random walk has first crossed the barrier by that scale:

$$f_\text{coll}(M_\text{min}, z) = P(\text{first crossing} \leq \sigma(M_\text{min})) = \text{erfc}\left[\frac{\delta_c(z)}{\sqrt{2}\,\sigma(M_\text{min})}\right]$$

This is the **Press-Schechter formula** (1974). It provides a simple, analytic prediction for the halo mass function without running expensive $N$-body simulations.

### Sheth-Tormen Refinement: Ellipsoidal Collapse

The Press-Schechter formula assumes spherical collapse and a fixed barrier $\delta_c = 1.686$. In reality, structures collapse under ellipsoidal dynamics, where the barrier in density space becomes **scale- and halo-mass-dependent**. The Sheth-Tormen correction (2001) incorporates this by introducing the "peak height":

$$\nu(M) = \frac{\delta_c(z)}{\sigma(M,z)}$$

and fitting the multiplicity function:

$$f(\nu) = A\sqrt{\frac{2a}{\pi}}\left[1 + (a\nu^2)^{-p}\right]\nu\,e^{-a\nu^2/2}$$

with empirical parameters $A = 0.353$, $a = 0.73$, $p = 0.175$. At $\nu \to \infty$ (very massive halos), this reduces to the Press-Schechter formula, but at intermediate masses ($\nu \sim 1$–$3$, corresponding to $M \sim 10^{10}$–$10^{12}\,M_\odot$ at $z \sim 7$), Sheth-Tormen predicts $\sim 30$% more halos because ellipsoidal collapse allows non-spherical shapes to form more easily.

**Quantitative comparison at $z = 7$**: For $M = 10^{10}\,M_\odot$ (relevant for ionizing sources), Press-Schechter predicts $f_\text{coll}(M) \approx 0.03$; Sheth-Tormen gives $f_\text{coll}(M) \approx 0.04$–$0.05$. This ~30% difference propagates directly into predictions of the ionization efficiency $\zeta$ needed to reionize at the observed epoch, making the choice of mass function non-trivial.

## Two Applications in Reionization

### 1. Halo Mass Function (Press-Schechter and Sheth-Tormen)

The collapsed fraction of matter in halos more massive than $M_\text{min}$ at redshift $z$ is:

$$f_\text{coll}(M_\text{min}, z) = \text{erfc}\left[\frac{\delta_c(z)}{\sqrt{2}\,\sigma(M_\text{min},z)}\right]$$

Here:
- $\delta_c(z) = 1.686 / D(z)$ is the linear collapse threshold, with $D(z)$ the linear growth factor
- $\sigma(M_\text{min})$ is the RMS density fluctuation smoothed on the mass scale $M_\text{min}$, computed from the linear power spectrum

This gives the **Press-Schechter** result, which historically provided the first analytic prediction for how the fraction of collapsed matter (and hence the halo abundance) evolves with time.

The **Sheth-Tormen correction** improves agreement with $N$-body simulations by accounting for ellipsoidal collapse rather than spherical collapse. It works better at both very high masses (where Press-Schechter fails badly, underestimating counts) and at intermediate masses. For reionization, the difference affects whether sources are rare (high-mass end) or abundant (lower-mass end), impacting both bubble morphology and the required ionizing efficiency.

### 2. Ionized Bubble Criterion in 21cmFAST

The excursion-set formalism is adapted to model bubble growth by replacing the density criterion with an **ionization criterion**. A region of comoving scale $R$ centered on position $\mathbf{x}$ is ionized if:

$$\zeta \cdot f_\text{coll}(\mathbf{x}, R, M_\text{min}, z) \geq 1$$

where:
- $\zeta$ (ionizing efficiency) is the number of ionizing photons produced per baryon in collapsed halos; typical range $\zeta \sim 10$–$100$ depending on stellar mass function and escape fractions
- $f_\text{coll}(\mathbf{x}, R, M_\text{min})$ is the collapsed matter fraction within a sphere of radius $R$ centered at $\mathbf{x}$, smoothed on scale $R$

**Key point:** The ionization criterion is **stochastic** — different positions $\mathbf{x}$ have different $f_\text{coll}$ because the underlying matter density is fluctuating. Thus the barrier (the left-hand side of the inequality) varies in space and is not fixed like $\delta_c$ for halos.

### The Scanning Algorithm: "Excursion" from Large to Small $R$

The algorithm in 21cmFAST (and variants like SCRIPT) works as follows:

1. For each cell $\mathbf{x}$ in the computational grid, compute the collapsed fraction $f_\text{coll}(\mathbf{x}, R, M_\text{min})$ at successively *decreasing* radii $R$, starting from $R_\text{max} \approx R_\text{mfp}$ down to $R_\text{min} \sim$ few comoving kpc.
2. Find the **largest** $R$ for which $\zeta f_\text{coll}(\mathbf{x}, R) \geq 1$. The ionized region centered at that cell extends to this scale.
3. Mark that region as ionized and move to the next cell.

The term **"excursion"** refers to the scanning down from large $R$ (where $f_\text{coll}$ is smallest) to small $R$ (where $f_\text{coll}$ is largest). A cell is ionized at the *largest* scale satisfying the criterion — once you find the scale, you "exit" the search (having completed an excursion through that cell's ionization state).

The **upper cutoff $R_\text{mfp}$** (the mean free path) is crucial: it prevents bubbles from growing to unphysical sizes. Photons cannot propagate beyond $R_\text{mfp}$ in the neutral IGM due to absorption by Lyman-limit systems, so even if $\zeta f_\text{coll}$ would satisfy the criterion at larger $R$, the bubbles are capped.

## Typical Bubble Sizes as a Function of Ionized Fraction

The characteristic bubble radius $R_\text{eff}$ (the effective radius, proportional to where $\zeta f_\text{coll}(\mathbf{x}, R) \sim 1$) evolves dramatically during reionization:

| $\bar{x}_\text{HII}$ | Redshift | Typical $R_\text{eff}$ | Physical regime |
|------------------------|-----------|-----------------------|-------------|
| $\sim 0.01$ | $z \sim 12$ | 0.3–0.5 Mpc | Isolated bubbles; early individual sources |
| $\sim 0.1$ | $z \sim 10$ | 0.5–2 Mpc | Cluster-centered bubbles growing; some overlap |
| $\sim 0.3$ | $z \sim 8.5$ | 3–8 Mpc | Rapid bubble merger; large-scale connectivity |
| $\sim 0.5$ | $z \sim 7.5$ | 8–20 Mpc | Percolation transition; ionized network spans box |
| $\sim 0.7$ | $z \sim 6.8$ | 15–50 Mpc | Post-overlap; bubbles continue merging |
| $\sim 0.99$ | $z \sim 6$ | 50–100 Mpc | Only small pockets of neutral gas remain |

These scales are set by the interplay of $\zeta$, the density field (encoded in $\sigma(R)$ and $f_\text{coll}$), and $R_\text{mfp}$. Higher $\zeta$ shifts the bubble sizes to larger values at fixed $\bar{x}_\text{HII}$.

## Physical Meaning: Inside-Out Reionization

The excursion-set criterion encodes a fundamental fact: **reionization proceeds inside-out** because dense, biased regions (high $f_\text{coll}$ and hence high source density) ionize first. Voids remain neutral longest because their low source density means fewer photons to ionize an already-large volume.

This makes intuitive sense: the same number of sources produces a larger HII region if the region is less dense (fewer recombinations), but the excursion-set says we need $\zeta f_\text{coll} \geq 1$, meaning the photon production must match the *baryon content*, not the volume. In a void with low $f_\text{coll}$, it takes a much larger radius to accumulate enough baryons in collapsed halos to satisfy the criterion, but the photon mean free path is longer in the low-density environment. The net result is that voids do eventually ionize, but only late, after dense regions have already percolated into a connected ionized network.

This inside-out pattern is **strongly supported** by observations:
- Lyman-alpha emitters cluster more strongly than the underlying matter, indicating preferential reionization of overdense regions
- The Gunn-Peterson trough shows rapid evolution at $z \sim 6$, consistent with percolation-like behavior
- Full radiative transfer simulations (THESAN, FIRE-2, etc.) confirm inside-out reionization when sources follow the galaxy distribution

## Photon-Counting vs. Photon-Propagation: A Critical Distinction

The excursion-set formalism in its basic form (21cmFAST) operates in a **photon-counting** regime:

$$\text{Ionized?} \Leftrightarrow \zeta f_\text{coll}(R) \geq 1$$

This asks: "Are there enough ionizing photons from sources within radius $R$ to ionize all the hydrogen within $R$?" It does *not* track where photons actually go or how they propagate through the IGM.

In contrast, **full radiative transfer** (THESAN, C$^2$-Ray, ART) solves the photon transport equation:

$$\nabla \cdot \mathbf{F}_\nu + \kappa_\nu n_\text{HI} = S_\nu$$

where $\mathbf{F}_\nu$ is the photon flux, $\kappa_\nu$ is the photoionization cross-section, and $S_\nu$ is the source term. This tracks each photon's path and its probability of escape, reaching spatial resolution of ionization fronts.

**Consequences for morphology:**
- 21cmFAST bubbles are typically smooth and large, with sharply defined boundaries
- Full RT produces more complex, partially-ionized transition regions ("ionization fronts") with temperature structure
- At the same $\bar{x}_\text{HII}$, 21cmFAST bubble distributions can differ from full RT by 20–50% (21cmFAST overproduces large bubbles)

This difference is a primary source of uncertainty in extracting EFT coefficients like $b_{\nabla^2}^x$ from simulations, and it is the main physics question in P1.

## Connection to EFT

The excursion-set criterion determines the **bubble size distribution**, which sets $R_\text{eff}$ and therefore $b_{\nabla^2}^x$:

$$b_{\nabla^2}^x = -\frac{R_\text{eff}^2}{3}$$

(up to logarithmic and higher-order corrections). Different semi-numerical codes (21cmFAST, SCRIPT, AMBER) implement the excursion-set criterion with different details:
- Choice of density/collapse interpolation
- Halo mass function (Press-Schechter vs. Sheth-Tormen)
- Recombination model (clumping factor $C$ and its scale-dependence)
- Photon escape fraction as a function of halo mass

These implementation differences produce different $R_\text{eff}$ trajectories even when the global $\bar{x}_\text{HII}(z)$ is matched between codes. This is **the primary source of EFT coefficient variation** in P1 and a key prediction to test: different bubble morphologies should produce different 21 cm power spectra on scales $k \gtrsim 0.1\,\text{Mpc}^{-1}$.

## Limitations

The excursion-set approach is fast but makes strong approximations:

1. **No photon trajectories:** Assumes all photons from collapsed halos within radius $R$ ionize the surrounding gas uniformly. Does not account for anisotropic escape (e.g., preferential photon escape along filaments).

2. **No partially-ionized cells:** A cell is either ionized or neutral; no intermediate states. Transition regions (ionization fronts) are smoothed out.

3. **No temperature structure:** Ionization and temperature are decoupled. Full RT tracks the thermal state of ionized gas, which affects recombination rates and spin temperature.

4. **Self-consistency:** The mean free path $R_\text{mfp}$ is typically taken as an input parameter (often fit to match observations at $z=6$), rather than computed self-consistently from the neutral fraction and LLS distribution. This breaks a physical feedback loop.

5. **Halo bias:** The formalism assumes sources trace collapsed matter exactly; in reality, galaxies are biased tracers with clustering that differs from the matter distribution.

These limitations are addressed by higher-level codes (AMBER with adaptive mesh, ARTIST-like schemes) at significant computational cost. For EFT extraction in P1, it is critical to acknowledge these limitations when interpreting differences between 21cmFAST and full-RT predictions.

## See Also

- [[Clumping Factor]] — sub-grid recombination model that enters the ionization criterion
- [[Bubble Size Distribution]] — the output of the excursion set in morphology
- [[Ionization Morphology]] — the spatial patterns this formalism produces
- [[Mean Free Path]] — the physical cutoff on bubble growth
- [[Neutral Fraction]] — the global outcome of the excursion-set dynamics
