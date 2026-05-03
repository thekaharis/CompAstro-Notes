---
type: domain
title: "Effective Field Theory"
created: 2026-04-14
updated: 2026-04-16
tags:
  - domain/eft
  - domain/theory
status: mature
related:
  - "[[Reionization Physics]]"
  - "[[21cm Cosmology]]"
  - "[[Simulation and Codes]]"
---

# Effective Field Theory

## What It Is in This Context

An **Effective Field Theory (EFT)** describes the large-scale behaviour of a system by expanding in operators consistent with symmetries, without needing to know the small-scale (UV) details. In this thesis, the EFT is applied to the ionization field $x_\text{HII}$ during the Epoch of Reionization: on scales larger than the characteristic ionized bubble radius, $x_\text{HII}$ must be expressible as a sum of all local operators built from the matter density field and its derivatives, with free coefficients that absorb the UV (sub-bubble) physics.

The general philosophy of EFT is to **integrate out degrees of freedom** at scales smaller than the EFT cutoff scale $\Lambda$ (in this context, the bubble scale ~1-20 Mpc). The result is an effective action or correlation function that depends only on longer-wavelength degrees of freedom, but whose coefficients (the EFT parameters) encode the integrated effects of the short-scale physics.

## The General EFT Framework: Operator Expansion

In any EFT, the key steps are:

1. **Identify the symmetries** of the problem (what transformations leave the physics invariant)
2. **Enumerate all operators** consistent with those symmetries up to a given order in derivatives or other small parameters
3. **Write the effective action/correlation** as a sum of these operators with free coefficients
4. **Match coefficients** by comparing to microscopic theory (simulations, data, or UV-complete theory)
5. **Use matching conditions** to make predictions at different scales or in different observables

For the ionization field:

- **Symmetries:** Statistical isotropy (no preferred direction), Galilean invariance (boost invariance of the equations of motion in the matter frame)
- **Small parameter:** $\epsilon \sim (k/k_{\text{NL}})$ where $k_{\text{NL}} \sim \Lambda^{-1}$ is the inverse of the nonlinearity scale (the bubble scale)
- **Operators:** All local combinations of $\delta_m$ and its derivatives that respect the symmetries
- **Coefficients:** The bias coefficients $\{b_1^x, b_2^x, b_{\nabla^2}^x, \ldots\}$ that depend on redshift and reionization physics

## Derivation of the Operator Basis from Symmetries

### Statistical Isotropy

The universe is **statistically homogeneous and isotropic** on large scales (above ~300 Mpc). This means:

- The two-point correlation function depends only on the separation vector $|\mathbf{r}|$, not on its direction
- In Fourier space, there is no preferred direction; the power spectrum depends only on $k = |\mathbf{k}|$

This constrains the operators: we cannot include vectors like $\nabla \delta_m$ (which points in a specific direction) without pairing them appropriately. This is why $\delta_m^2$ is allowed (scalar), and $(\nabla \delta_m)^2$ is allowed (also scalar), but a vector like $\nabla_i \delta_m \, \nabla^j \delta_m$ with $i \neq j$ is not allowed in the power spectrum (though it could appear in higher-order correlation functions).

### Galilean Invariance

In the **Eulerian frame** (fixed in space), velocities appear in the equation of motion. However, reionization physics respects **Galilean invariance**: the results should not depend on the choice of reference frame (at least on scales larger than the Hubble scale).

This implies:
- The ionization bias should depend on **density and density gradients**, not on the velocity field itself
- Operators like $v_i v^i$ are not Galilean-invariant (they change under a boost) but $(\partial_i v_i) = \nabla \cdot \mathbf{v}$ is invariant (it equals the density time-derivative in Eulerian coordinates)

In practice, this means:
- $\delta_m$ is allowed (density contrast)
- $\delta_m^2$ is allowed (products of density)
- $\nabla^2 \delta_m$ is allowed (density curvature)
- But $v_i$ by itself is **not** an allowed operator in an EFT respecting Galilean invariance
- And $\delta_m \, v_i$ is **not** allowed as a separate operator because $v_i$ is not invariant

(The velocity field is an auxiliary variable determined by $\delta_m$ and gravity; it is not independent.)

### Locality

Only **local** operators appear in the EFT expansion. An operator is local if it involves derivatives of $\delta_m$ at the same spatial point. Non-local operators (e.g., $\delta_m(\mathbf{x}) \, \delta_m(\mathbf{x} + \mathbf{r})$ for $|\mathbf{r}| > \Lambda^{-1}$) involve UV physics and should be integrated out.

This limits the operator basis to:
- $\delta_m(\mathbf{x})$ and its derivatives
- Integrated fields like $\int d^3 y K(|\mathbf{x} - \mathbf{y}|) \delta_m(\mathbf{y})$ can appear, but with kernels $K$ that fall off on short scales

## The Bias Expansion for the Ionization Field

The central equation of the thesis:

$$
\delta_x(\mathbf{x}, z) \equiv x_\text{HII}(\mathbf{x}, z) - \bar{x}_\text{HII}(z) = b_1^x\,\delta_m + \frac{b_2^x}{2}\,\delta_m^2 + b_{\nabla^2}^x\,\nabla^2\delta_m + \varepsilon^x(\mathbf{x}, z)
$$

where:

- $\delta_m(\mathbf{x}, z) = [\rho_m(\mathbf{x},z) - \bar{\rho}_m(z)] / \bar{\rho}_m(z)$ is the **matter overdensity** computed from simulations or perturbation theory

- $b_1^x(z)$ is the **linear bias coefficient**: it parameterizes the leading-order response of the ionization field to density fluctuations. Physically, it encodes:
  - Whether ionization is **correlated** ($b_1^x > 0$) or **anti-correlated** ($b_1^x < 0$) with overdensity
  - The strength of this correlation
  - It is related to source bias and the mean ionized fraction; typically $b_1^x > 0$ during most of reionization (overdense regions ionize first)

- $b_2^x(z)$ is the **quadratic (or second-order) bias coefficient**: it captures the non-linear response of ionization to density. Physically:
  - Arises from the clustering of sources (via the source bias $b_{S,2}$)
  - Also arises from the patchy coupling of the radiation field to density fluctuations
  - Can be positive or negative; sign varies through reionization history
  - In many models, $b_2^x \approx -\bar{x}_\text{HII} \cdot b_{S,2}$ early on, but later becomes dominated by patchy RT effects

- $b_{\nabla^2}^x(z)$ is the **derivative (or tidal) bias coefficient**: it parameterizes non-locality at the bubble scale. Physically:
  - The $\nabla^2 \delta_m$ term captures how the ionization field depends on the local **curvature** of the density field
  - This non-locality arises from finite-range processes (photon mean free path $R_\text{mfp}$, finite recombination time)
  - The coefficient is related to the effective ionized bubble scale: $b_{\nabla^2}^x \propto -R_\text{eff}^2$
  - When $R_\text{eff}$ is large (large bubbles), the ionization field is more locally determined, and $|b_{\nabla^2}^x|$ is larger

- $\varepsilon^x(\mathbf{x}, z)$ is the **stochastic term** (noise): represents the irreducible scatter in the ionization field that cannot be explained by local density and its derivatives. Sources include:
  - Discreteness of ionized bubbles (shot noise from bubble counting)
  - Stochastic recombinations (small-scale fluctuations in recombination rates)
  - Sub-grid sources (unresolved stellar populations)
  - Probabilistic source assignment in semi-numerical codes

The power spectrum of the stochastic term is $P_{\varepsilon\varepsilon}(k, z)$, which is one of the EFT observables. It is the most **simulator-sensitive** coefficient because different codes implement bubble discreteness and sub-grid physics differently.

## Perturbation Theory Orders

The EFT expansion is constructed in increasing orders of the small parameter $\epsilon \sim k / k_{\text{NL}}$:

### Linear order ($\epsilon^0$)
- $\delta_m^{(1)}$ — the linear density field. In perturbation theory, $\delta_m^{(1)}(\mathbf{k}) = D(z) \times$ (initial density perturbation).
- Grows as the linear growth factor $D(z)$ (normalized to 1 at $z=0$ in standard conventions)
- Small-scale: $P_{mm}^{(1)}(k)$ is the linear matter power spectrum

### Second-order ($\epsilon^1$)
- $\delta_m^{(2)}$ — the second-order (nonlinear) contribution to the density field from gravity. Computed as:
$$
\delta_m^{(2)}(\mathbf{x}, z) = -\frac{3}{7} \int d^3 k_1 d^3 k_2 \, (2\pi)^3 \delta^3(\mathbf{k}_1 + \mathbf{k}_2 - \mathbf{k}) F_2(\mathbf{k}_1, \mathbf{k}_2) \delta^{(1)}(\mathbf{k}_1) \delta^{(1)}(\mathbf{k}_2)
$$
where $F_2$ is the second-order perturbation theory kernel (depends on the cosmology and gravitational growth)
- This is the first nonlinear correction from gravitational evolution

- $[\delta^2]_\text{renorm}$ — the **renormalized square** of the linear field, which removes UV dependence:
$$
[\delta^2]_\text{renorm} = \left(\delta^{(1)} + \delta^{(2)}\right)^2 - (\delta^{(2)})^2 - \frac{68}{21}\sigma^2_L \delta^{(1)}
$$
where $\sigma^2_L$ is the variance of the linear density field on short scales (regulated to the EFT cutoff)
- The subtraction $-(\delta^{(2)})^2 - \frac{68}{21}\sigma^2_L \delta^{(1)}$ removes power from modes shorter than the cutoff

### Derivative operators
- $\nabla^2 \delta_m^{(1)}$ — the Laplacian of the linear field. In Fourier space, this is $\nabla^2 \delta(\mathbf{k}) = -k^2 \delta(\mathbf{k})$.
- This grows as $\sim D(z)$ at late times (perturbative regime)
- Represents the local curvature structure at each point

Higher-order combinations (e.g., $(\nabla^2 \delta)^2$, $\nabla^4 \delta$) appear in higher-order EFT, but the basis above captures the leading 1-loop order.

## Why the Operator Basis Is Simulator-Independent

Different simulators (21cmFAST, SCRIPT, THESAN) implement different source prescriptions, recombination models, and bubble-growth algorithms. Yet they all produce ionization fields that:

1. **Obey the same physics laws:** gravity (via $\delta_m$), photon propagation (via $R_\text{mfp}$), and ionization chemistry
2. **Respect the same symmetries:** statistical isotropy and Galilean invariance (approximate, on cosmological scales)
3. **Operate in the same universe:** same cosmological parameters $(\Omega_m, \Omega_b, h, \ldots)$

Therefore, all simulated ionization fields must be describable by the same **operator basis**. The basis is **independent of simulator** because it is determined only by symmetries and locality, not by implementation details.

What **does** vary between simulators is the **coefficient trajectory** $\{b_1^x(z), b_2^x(z), b_{\nabla^2}^x(z), P_{\varepsilon\varepsilon}(k,z)\}$. Different codes produce different values because they:

- Implement different source mass functions (affects $b_1^x$)
- Use different recombination models (affects all coefficients)
- Evolve the density field differently (21cmFAST's 2LPT vs. full N-body)
- Handle ionization topology differently (excursion-set vs. conditional luminosity function vs. full RT)

This is the **key insight** of the thesis: the EFT provides a **universal language** for expressing ionization fields, and simulator differences manifest as differences in coefficient values, not differences in the basis.

## Physical Interpretations of EFT Coefficients

Based on reionization physics (from [[Choudhury 2022 (Reionization Intro)]] and [[Ferrara & Pandolfi (IGM Reionization)]]):

### $b_1^x$: Source Bias and Mean Ionized Fraction

$$
b_1^x(z) \approx \bar{x}_\text{HI}(z) - \bar{x}_\text{HII}(z) \cdot b_{S,1}(z)
$$

where $b_{S,1}$ is the bias of ionizing sources relative to matter.

- **Physical meaning:** How strongly ionized regions are clustered relative to matter. Positive $b_1^x$ means overdense regions are preferentially ionized.
- **Early reionization ($\bar{x}_\text{HII} < 0.2$):** Sources are clustered in overdense regions ($b_{S,1} > 0$), so ionized regions are also biased. $b_1^x > 0$.
- **Mid reionization ($\bar{x}_\text{HII} \sim 0.5$):** Source bias may decrease or reverse, but the mean ionized fraction effect dominates. $b_1^x$ remains positive but may decrease.
- **Late reionization ($\bar{x}_\text{HII} > 0.8$):** Most regions are ionized; the ionization field becomes less correlated with density. $b_1^x$ may become negative (underdense regions are harder to ionize, so ionization anti-correlates with density).

**This is the most **astrophysically sensitive** coefficient because it depends directly on the source virial temperature $T_\text{vir}$ (via the minimum halo mass and thus the source bias) and the ionizing efficiency $\zeta$.**

### $b_2^x$: Patchiness and Radiation Coupling

$$
b_2^x(z) \approx -\bar{x}_\text{HII}(z) \cdot b_{S,2}(z) + \text{[RT patchy coupling]}
$$

- **Source clustering contribution:** If sources cluster quadratically with density ($b_{S,2} \neq 0$), then ionization inherits this clustering.
- **Patchy RT contribution:** Even if sources do not cluster quadratically, the ionization field does because of patchy coupling of the radiation field to density fluctuations. This is a **uniquely reionization-driven** contribution.
- **Sign:** Can flip through reionization history. Early on, usually negative (source-dominated). Late on, can become positive (RT patchy term dominates).
- **Magnitude:** Typically smaller than $b_1^x$; often $|b_2^x| \lesssim 0.5 |b_1^x|$.

### $b_{\nabla^2}^x$: Effective Bubble Scale

$$
b_{\nabla^2}^x(z) \propto -R_\text{eff}^2(z)
$$

where $R_\text{eff}$ is the characteristic ionized bubble radius at redshift $z$.

- **Physical meaning:** The $\nabla^2 \delta_m$ term captures non-locality; the coefficient measures how strong the non-locality is.
- **Large bubbles:** If $R_\text{eff}$ is large (ionization fully extended, deep into reionization), then local curvature effects are important, and $|b_{\nabla^2}^x|$ is large.
- **Small bubbles:** If $R_\text{eff}$ is small (early reionization, small isolated bubbles), then local curvature is less important, and $|b_{\nabla^2}^x|$ is small.
- **Typical values:** $R_\text{eff} \sim 5-20$ Mpc during mid-to-late reionization, so $b_{\nabla^2}^x \sim -(5-20)^2 \sim -25$ to $-400$ Mpc² (in appropriate units).

**This is the most **simulator-sensitive** coefficient** because different codes implement bubble growth (excursion-set radius, conditional luminosity function, full RT morphology) differently, leading to different effective bubble size distributions.

### $P_{\varepsilon\varepsilon}(k, z)$: Stochasticity and Shot Noise

The power spectrum of the stochastic term:

$$
P_{\varepsilon\varepsilon}(k, z) = \langle |\varepsilon^x(\mathbf{k})|^2 \rangle
$$

**Sources:**
- **Bubble discreteness:** The ionization field is patchy — made of discrete bubbles of different sizes. The shot noise from counting bubbles appears as a scale-independent (white noise) component at small $k$ and a power-law decay at larger $k$.
- **Stochastic recombinations:** Recombination rates fluctuate at small scales; this creates additional stochasticity.
- **Lyman-limit systems:** Rare, optically-thick absorbers (cold gas clouds with $N_\text{HI} > 10^{17}$ cm$^{-2}$) introduce discrete scattering into the radiation field.
- **Sub-grid source shot noise:** Unresolved stellar populations within halos produce stochasticity.

**Key properties:**
- Roughly **scale-independent** at $k \ll k_{\text{NL}}$ (shot noise)
- Rises with redshift during reionization (more bubbles = more shot noise; bubbles are more discrete early on)
- Falls after reionization (fewer bubbles = less shot noise)
- Highly **code-dependent** because different codes implement bubble sampling and sub-grid physics differently

## Regime of Validity

The EFT expansion breaks down when $k \sim k_{\text{NL}} \sim 1/R_\text{eff}$, i.e., when the wavelength becomes comparable to the bubble scale.

Empirically (from McQuinn & D'Aloisio 2018):
$$
\frac{P_\text{err}}{P_{21}} \lesssim 10\% \quad \text{for} \quad k \lesssim 0.2 \text{ to } 0.5 \, h\,\text{Mpc}^{-1}
$$

More recent work (Qin et al. 2022) using renormalized coefficients extends this to:
$$
\frac{P_\text{err}}{P_{21}} \lesssim 1\% \quad \text{for} \quad k \lesssim 0.8 \, h\,\text{Mpc}^{-1}
$$

This is achieved by carefully handling the renormalization subtraction for $\delta_m^2$ at each $k$.

**Dependence on redshift and physics:**
- Early reionization ($z \sim 12$, $\bar{x}_\text{HII} \sim 0.1$): $R_\text{eff} \sim 5-10$ Mpc, so $k_{\text{NL}} \sim 0.1$ h/Mpc. EFT valid for $k \lesssim 0.05$ h/Mpc.
- Mid reionization ($z \sim 8$, $\bar{x}_\text{HII} \sim 0.5$): $R_\text{eff} \sim 15-25$ Mpc, so $k_{\text{NL}} \sim 0.04$ h/Mpc. EFT valid for $k \lesssim 0.02$ h/Mpc.
- After reionization ($z < 6$): $R_\text{eff}$ is ill-defined (universe fully ionized), but the same formalism applies to residual ionization fluctuations.

## The Cross-Correlation Coefficient Method

A practical way to measure EFT coefficients is via the **cross-correlation** between 21 cm power and matter power:

$$
r(k, z) = \frac{P_{21 \times m}(k, z)}{\sqrt{P_{21}(k) \times P_{mm}(k)}} = \frac{P_{21 \times m}(k)}{\sqrt{P_{21} \times P_{mm}}}
$$

This measures the correlation coefficient between ionization and density fields at each $k$.

**Derivation:**
- $P_{21 \times m}$ is the cross-power spectrum
- If ionization is a perfect linear tracer of density ($\delta_x = b \delta_m$), then $r = 1$
- As reionization becomes non-linear and stochastic, $r < 1$

**Extracting $b_1^x$:**
- At very large scales ($k \to 0$), the cross-correlation approaches $r \approx 1$ because the nonlinear and stochastic terms average out
- The linear bias $b_1^x$ can be extracted from $r(k \to 0)$ or from the power spectrum ratio: $b_1^x \approx \sqrt{P_{21}(k \to 0) / P_{mm}(k \to 0)}$

**Limitations:**
- Requires measuring both $P_{21}$ and $P_{mm}$ (the matter power)
- The matter power is not directly observable at high-$z$; must be inferred from density field simulations or N-body codes
- Limited to the EFT-valid range where linear bias is meaningful

## How EFT Coefficients Appear in Observables

On the power spectrum, the EFT expansion predicts:

$$
P_{21}(k, z) = \left[ b_1^x + \frac{b_2^x}{2} \langle \delta_m^2 \rangle / \sigma^2_L + b_{\nabla^2}^x k^2 + P_{\varepsilon\varepsilon}(k) / P_{mm}(k) \right]^2 P_{mm}(k) + P_{\varepsilon\varepsilon}(k)
$$

(schematic; exact form depends on including 1-loop contributions and renormalization)

**Features:**
- **Large-scale plateau (linear regime):** $P_{21}(k) \propto b_1^x$ at $k \ll k_{\text{NL}}$
- **$k^2$ suppression from $b_{\nabla^2}^x$:** At intermediate scales, the derivative bias term becomes important; the power spectrum receives a negative correction proportional to $k^2$. This creates a characteristic **shape** in $P_{21}(k)$ that depends on $R_\text{eff}$.
- **Stochastic floor:** At all scales, there is an additive white-noise term from $P_{\varepsilon\varepsilon}$

## Connection to Galaxy Clustering and the EFTofLSS

The bias expansion for the ionization field is directly analogous to the **bias expansion for galaxies** used in large-scale structure surveys (BOSS, DESI, Euclist). The galaxy bias expansion is:

$$
\delta_g(\mathbf{x}, z) - \bar{n}_g(z) = b_1^g \delta_m + \frac{b_2^g}{2} \delta_m^2 + b_{\nabla^2}^g \nabla^2 \delta_m + \varepsilon^g(\mathbf{x}, z)
$$

This is the same form as the ionization bias expansion, just with different physical interpretation:
- $b_1^g$ = galaxy linear bias (related to halo bias and galaxy formation physics)
- $b_2^g$ = galaxy quadratic bias (related to nonlinear clustering and environment-dependent galaxy growth)
- $b_{\nabla^2}^g$ = galaxy tidal bias (related to halo ellipticity and environment)

The parent framework is the **EFTofLSS** (Effective Field Theory of Large Scale Structure) developed by Senatore & Zaldarriaga (2012) and extended by many authors. The 21cm bias expansion is a direct application of this framework to the ionization field instead of the galaxy density field.

**Key difference:** Whereas galaxy bias encodes how galaxies (a discrete tracer) populate the dark matter distribution, ionization bias encodes how the ionization state (a continuous field) responds to density. Both are UV completions of the same large-scale EFT.

## Foundational Papers and Development

```
Senatore & Zaldarriaga 2012       ← EFTofLSS: general framework
        ↓
McQuinn & D'Aloisio 2018          ← applies EFT to ionization field; Minimal Model; 3 RT codes
        ↓
Qin et al. 2022                   ← extends to redshift space; renormalization; THESAN validation
        ↓
Sailer et al. 2022                ← optical depth (τ) EFT; observational forecasts
        ↓
Baradaran et al. 2024             ← hybrid EFT: N-body density + EFT ionization painting
        ↓
Thesis (P1/P2)                    ← EFT of x_HII specifically; cross-simulator comparison; inference
```

## Key Concepts

- [[Matter Overdensity Field]]
- [[Bias Expansion]]
- [[Renormalization]]
- [[Stochastic Term]]
- [[Linear Growth Factor]]
- [[Regime of Validity]]
- [[Power Spectrum Error]]
- [[Operator Basis]]
- [[Symmetry Principles]]

## Foundational Papers

- [[McQuinn & D'Aloisio 2018]] — introduced bias expansion for 21 cm field; Minimal Model; validated on 3 RT codes; gold standard
- [[Qin et al 2022 (EFT Redshift Space)]] — extended to redshift space with renormalized coefficients; validated on THESAN; $k \lesssim 0.8\,h\,\text{Mpc}^{-1}$
- [[Baradaran et al 2024 (Hybrid EFT)]] — hybrid EFT combining N-body density with EFT ionization painting; most accurate semi-analytic 21cm model to date
- [[Sailer et al 2022 (Optical Depth EFT)]] — symmetries-based bias expansion applied to optical depth $\tau$; forecasts $\tau$ constraints from future 21cm experiments

## Parent Framework

- [[Senatore & Zaldarriaga 2012 (EFTofLSS)]] — the general EFT framework for large-scale structure; parent of all bias expansions

## Physical Background

- [[Choudhury 2022 (Reionization Intro)]] — provides the physical inputs (halo mass function, photon budget) that determine EFT coefficients
- [[Ferrara & Pandolfi (IGM Reionization)]] — ionization topology and bubble morphology; physical interpretation of $b_1^x$, $b_2^x$, $b_{\nabla^2}^x$
- [[Gnedin & Madau 2022 (Modeling Reionization)]] — code taxonomy clarifying what physical differences between simulators are captured in EFT coefficients
- [[Trac & Gnedin 2009 (Reionization Simulations)]] — RT algorithm diversity; explains why full RT codes differ from semi-numerical at morphological level

## Sources

- [[McQuinn & D'Aloisio 2018]] — foundational paper
- [[Qin et al 2022 (EFT Redshift Space)]] — renormalization and redshift-space extensions
- [[Sailer et al 2022 (Optical Depth EFT)]] — τ forecasts using EFT
- [[Baradaran et al 2024 (Hybrid EFT)]] — N-body + EFT painting
- [[Choudhury 2022 (Reionization Intro)]] — physical inputs to EFT
- [[Ferrara & Pandolfi (IGM Reionization)]] — ionization topology and bubble morphology
- [[Gnedin & Madau 2022 (Modeling Reionization)]] — code taxonomy
- [[Trac & Gnedin 2009 (Reionization Simulations)]] — RT algorithm diversity
