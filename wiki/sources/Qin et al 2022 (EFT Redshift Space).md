---
type: source
title: "Qin et al. 2022 — EFT Bias Expansion in Redshift Space"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/eft
  - domain/21cm
  - foundational
status: mature
source_type: paper
author:
  - "[[Qin, Yuxiang]]"
  - "Schutz, Katelin"
  - "Smith, Annika"
  - "Garaldi, Enrico"
  - "Kannan, Rahul"
  - "Vogelsberger, Mark"
  - "Hernquist, Lars"
date_published: 2022
url: "https://arxiv.org/abs/2205.06270"
journal: "Phys. Rev. D, 106, 123506"
confidence: high
key_claims:
  - "The perturbative bias expansion for 21cm extends to redshift space with renormalized bias coefficients"
  - "Validated against THESAN radiative transfer simulations: percent-level agreement for k ≲ 0.8 h/Mpc at x_HI ≳ 0.4"
  - "Renormalization removes the resolution dependence present in raw bias coefficients"
  - "Redshift-space distortions (RSD) are incorporated via an additional velocity-bias term that is comparable to quadratic bias at intermediate k"
related:
  - "[[Effective Field Theory]]"
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Baradaran et al 2024 (Hybrid EFT)]]"
  - "[[Bias Expansion]]"
  - "[[Renormalization]]"
  - "[[Redshift Space Distortions]]"
  - "[[THESAN]]"
---

# Qin et al. 2022 — EFT Bias Expansion in Redshift Space

> [!key-insight]
> The EFT bias expansion for the 21cm signal holds in redshift space with renormalized coefficients, achieving percent-level agreement against the THESAN full radiative transfer suite up to $k \lesssim 0.8\,h\,\text{Mpc}^{-1}$ at $\bar{x}_\text{HI} \gtrsim 0.4$. Renormalization is essential: it removes UV-divergent contributions that spoil the accuracy at intermediate scales. This extension makes the EFT framework directly applicable to real 21cm observations.

## Citation

Qin, W., Schutz, K., Smith, A., Garaldi, E., Kannan, R., Vogelsberger, M. & Hernquist, L. (2022). "An Effective Bias Expansion for 21cm Cosmology in Redshift Space." *Phys. Rev. D*, 106, 123506. arXiv:2205.06270.

## Core Claim

This paper extends [[McQuinn & D'Aloisio 2018]] in two critical directions:

1. **Redshift space:** incorporates redshift-space distortions (RSD) via an additional velocity-bias term. Observations are made in redshift space (peculiar velocities mix with cosmic expansion along the line of sight), so this is essential for realistic inference.

2. **Renormalization:** uses renormalization group (RG) techniques from field theory to remove UV-divergent contributions to the bias coefficients. These divergences arise when computing loop integrals (like $b_2 \propto \int P(q) dq / q^2$) over unresolved small scales. Renormalization makes the coefficients well-defined independent of simulation resolution.

The resulting framework achieves substantially better accuracy at intermediate $k$ (0.3–0.8 h/Mpc) than the Minimal Model, and is validated against THESAN — the most rigorous full-physics radiative transfer + hydrodynamics suite available.

## The Bias Expansion in Redshift Space

### Full 1-Loop Expansion with RSD

In redshift space, the 21cm brightness temperature contrast acquires contributions from peculiar velocities along the line of sight. The full 1-loop bias expansion is:

$$
\tilde{\delta}_{21}^{s}(\mathbf{k}) = b_1\left(1 - \frac{R_\text{eff}^2 k^2}{3}\right) \tilde{\delta}_m(\mathbf{k}) + b_2[\delta^2]_\text{renorm}(\mathbf{k}) + b_{\nabla^2}\left(\nabla^2 \delta_m\right)(\mathbf{k}) + b_v f k_\parallel^2 / k^2 \, \tilde{\delta}_m(\mathbf{k}) + \varepsilon(\mathbf{k})
$$

where:
- $b_1$: linear bias coefficient (ionization-weighted mean); same as in real space
- $[\delta^2]_\text{renorm}$: renormalized quadratic bias operator; removes the UV-divergent piece of $\delta^2$ to make the coefficient resolution-independent
- $b_{\nabla^2}$: gradient bias (kinetic energy term); suppresses power at small scales ($\propto k^2$)
- **$b_v f k_\parallel^2 / k^2$:** the **velocity-bias term** from RSD; $f = d\ln D / d\ln a$ is the growth rate (~0.5 at $z=6$), $k_\parallel$ is the line-of-sight wavenumber
- $\varepsilon(\mathbf{k})$: stochastic scatter uncorrelated with the linear field

### The Velocity-Bias Term: Physical Meaning

The coefficient $b_v$ arises from the coupling of ionization to peculiar velocities:
- Peculiar velocities stretch/compress structures along the line of sight
- If ionization traces the underlying dark matter accurately (high $b_1$), RSD modulates the 21cm signal
- The velocity bias $b_v$ quantifies how sensitive the ionization field is to velocity gradients
- At low ionization ($\bar{x}_\text{HII} \ll 1$), $b_v \sim b_1$ (ionization traces density, so RSD acts directly)
- At high ionization ($\bar{x}_\text{HII} \to 1$), $b_v$ can be smaller (ionization is nearly uniform, insensitive to velocity structure)

### Renormalization: The Technical Innovation

**Why it's needed:**

In loop integrals (e.g., computing the contribution of density fluctuations to $b_2$), you encounter:

$$b_2^{\text{bare}} \propto \int_0^\infty P(q) \, dq \sim \text{divergent at } q \to \infty
$$

This divergence is unphysical: it reflects the fact that the UV (small-scale) structure is not described by the linear theory power spectrum $P(q)$. In real data, there is a cut-off at the resolution scale.

**How renormalization fixes it:**

Subtract the UV-divergent part explicitly:

$$[\delta^2]_\text{renorm} = \delta^2 - \langle \delta^2 \rangle_{\text{UV}}
$$

The counter-term $\langle \delta^2 \rangle_{\text{UV}}$ is chosen so that the resulting coefficient $[b_2]_R$ is independent of where you place the UV cut-off. This ensures $[b_2]_R$ is a **physical observable**, not a simulation artifact.

**Practical impact:** 

The renormalized $[b_2]_R$ is stable across different simulation resolutions (8, 16, 32 grid points per halo, etc.), whereas the bare $b_2$ scales with resolution. This is crucial for cross-code comparisons where codes use different grid spacings.

## Key Results

### Regime of Validity in Redshift Space

- **Minimal Model (real space):** $P_\text{err}/P_{21} < 10\%$ for $k \lesssim 0.5\,h\,\text{Mpc}^{-1}$ (McQuinn & D'Aloisio)
- **Full 1-loop with renormalization (redshift space):** $P_\text{err}/P_{21} \lesssim$ few percent for $k \lesssim 0.8\,h\,\text{Mpc}^{-1}$ at $\bar{x}_\text{HI} \gtrsim 0.4$
  
The improvement in regime of validity (0.5 → 0.8 h/Mpc) is substantial: it extends into the intermediate-scale regime where much of the cosmological information resides.

### THESAN Validation

Qin et al. validate against **THESAN**, the most rigorous test available:
- Full 3D radiative transfer coupled to hydrodynamics
- Thousands of ionizing photon packets tracked self-consistently
- Includes absorption, scattering, and heating/cooling physics
- Much more expensive than semi-numerical codes but highest fidelity

Results:
- Percent-level power spectrum agreement ($P_\text{err}/P_{21} \sim 1$–$3\%$) across $k \lesssim 0.8\,h\,\text{Mpc}^{-1}$ and multiple redshifts
- Shows that the EFT holds not just for semi-numerical codes but for full RT + hydro
- Validates that the physics is truly captured by the bias expansion, not an artifact of simplified codes

### Renormalization Impact

Concrete numbers showing why renormalization matters:

- **Raw $b_2$ coefficient** (without renormalization): varies by $\sim 30\%$ when grid resolution changes from 8 to 32 cells per halo
- **Renormalized $[b_2]_R$ coefficient:** varies by $\lesssim 5\%$ across the same resolution range
- Conclusion: renormalization is not optional; it is necessary for resolution-independent comparisons

### Velocity-Bias Measurements

- $b_v$ is typically comparable to $b_2$ at intermediate $k$ ($k \sim 0.3$–$0.5$)
- At $k \sim 0.1$, $b_v$ contribution is negligible; at $k \sim 0.7$, it is significant
- Ignoring $b_v$ introduces $\sim 10$–$20\%$ errors in power spectrum predictions at intermediate scales
- Implication: any realistic inference using 21cm data must include velocity bias, not just the minimal model

## Methods

### Simulations and Data

- **THESAN suite:** multiple boxes with different ionization histories and redshifts
- **Neutral fraction range:** $\bar{x}_\text{HI} = 0.1$–$0.9$ (covers much of the EoR)
- **Redshift range:** $z = 6$–$13$ (accessible to future surveys)

### Bias Extraction Procedure

1. **Compute 21cm field in real space:** from THESAN outputs
2. **Apply redshift-space distortion:**  displace particles along line of sight by $\Delta z = v_z / H(z)$
3. **Fourier transform to get 21cm power** in redshift space: $P_{21}^s(k)$
4. **Regress against density field:** using the expansion above, extract coefficients via least-squares fit
5. **Apply renormalization:** subtract the UV-divergent part to stabilize coefficients across codes
6. **Validate:** compare $P_\text{model}(b_1, [b_2]_R, b_{\nabla^2}, b_v)$ to $P_{21}^s(k)$ across multiple scales

### Comparison Tests

- Minimal Model (McQuinn & D'Aloisio) vs. full 1-loop with renormalization
- Real space vs. redshift space
- Effect of including/excluding velocity bias term
- Robustness to simulation resolution

## Key Physics Insights

### Why RSD Changes the Expansion

Peculiar velocities modify the ionization field structure along the line of sight. Gravitationally bound regions (which are more ionized due to higher source density) fall inward (negative peculiar velocity), stretching the 21cm signal. This stretching introduces a new bias operator $\propto k_\parallel^2$.

In the saturated limit (where 21cm brightness temperature tracks ionization), RSD makes the 21cm map look "squashed" along the line of sight — the characteristic "Kaiser squashing" seen in galaxy surveys.

### Why Renormalization Is Physical

The renormalization removes the UV divergence by recognizing that the bias expansion is only valid at scales $k \lesssim 1/(aM)$ where $aM$ is the "Jeans length" of ionized bubbles. Below this scale, the EFT breaks down and the small-scale structure should not contribute to the large-scale bias coefficient.

This is the same renormalization used in galaxy bias theory (where it's well-established) and fluid turbulence (where it's called "closure approximation"). Applying it to 21cm is natural and principled.

## Connection to Thesis

### For P1

P1 targets the **ionization field** $x_\text{HII}$ rather than the 21cm brightness temperature $\delta T_b$. However, the renormalization formalism applies **directly** to the ionization field:

- Extract $b_1^x, b_2^x, b_{\nabla^2}^x$ from ionization field using the same expansion
- Apply renormalization counter-terms to ensure resolution independence
- The velocity-bias term is **irrelevant** for P1 (which works in real space on the ionization field)
- But it becomes relevant for P2, which infers from observed (redshift-space) 21cm maps

### For P2

The extension to redshift space is critical for P2:

1. **Real observations are in redshift space:** SKA, HERA, etc. measure in $(l, m, z)$ coordinates where z is redshift, not comoving distance
2. **EFT coefficients can be extracted from observed power spectra:** if you measure $P_{21}^s(k)$ from data, you can fit EFT coefficients directly (in principle)
3. **Mapping real-space EFT to redshift-space observables:** this is where $b_v$ and the full 1-loop expansion become essential
4. **Design question for P2:** should you infer $\{b_1, b_2, b_{\nabla^2}, b_v\}$ directly from observed (redshift-space) 21cm data? Or map back to real-space ionization field first?

## Key Difference from McQuinn & D'Aloisio 2018

| Aspect | McQuinn & D'Aloisio 2018 | Qin et al. 2022 |
|--------|--------------------------|-----------------|
| **Observable** | $\delta T_b$ in real space | $\delta T_b$ in redshift space |
| **Bias terms** | $b_1, b_2, b_{\nabla^2}$ (Minimal) | $b_1, b_2, b_{\nabla^2}, b_v$ (1-loop) |
| **Renormalization** | No | Yes; removes UV divergence from $b_2$ |
| **Validation codes** | Semi-numerical + some RT | THESAN (full RT + hydro) |
| **$k$ regime** | ≲ 0.5 h/Mpc | ≲ 0.8 h/Mpc |
| **Velocity effects** | Not included | Included via $b_v$ term |
| **Resolution robustness** | Raw $b_2$ resolution-dependent | Renormalized $[b_2]_R$ stable |

## Important Equations

### Redshift-Space Power Spectrum Prediction

$$P_{21}^s(k) = \left[b_1 - b_v f \mu^2 \right]^2 P_\delta(k) + \text{loop corrections} + \text{stochastic}$$

where $\mu = k_\parallel / k$ is the cosine of the angle to the line of sight. This shows how RSD modifies the linear power spectrum through the velocity-bias term.

### Renormalized Quadratic Bias

$$[b_2]_R = b_2^\text{bare} - C[b_2] \int_{\Lambda}^\infty \frac{P(q)}{q^2} dq$$

where $C[b_2]$ is a counter-term fixed by the renormalization condition, and $\Lambda$ is the UV cutoff. The result is independent of $\Lambda$ by construction.

## Figures Worth Noting

- **Figure comparing real vs. redshift space:** shows how $b_v$ term dominates at intermediate $k$, distorting the 21cm power spectrum shape
- **THESAN validation plots:** percent-level power spectrum agreement across multiple redshifts
- **Resolution robustness test:** $[b_2]_R$ stability across grid resolutions (striking contrast to bare $b_2$)

## Critical Reading: Caveats and Implications

### What This Paper Gets Right

1. **Rigorous theory:** the renormalization group approach is mathematically sound and borrowed from well-tested frameworks
2. **Highest-fidelity validation:** THESAN is the gold standard; no other code is more accurate
3. **Practical regime:** extending validity to $k \lesssim 0.8$ h/Mpc covers much of the information-rich regime
4. **Clear physics:** RSD interpretation via $b_v$ is transparent and matches intuition from galaxy surveys

### Important Caveats

1. **Limited code coverage:** only tested against THESAN. Does renormalization work equally well in 21cmFAST, SCRIPT, or other semi-numerical codes? This is P1's central question.

2. **Intermediate $k$ assumptions:** the 1-loop expansion assumes $k \lesssim$ (size of ionized bubbles)$^{-1} \sim 0.1$–$0.3$ h/Mpc. At $k \sim 0.8$, you are starting to resolve individual bubbles; is the expansion really trustworthy there?

3. **Velocity bias calibration:** $b_v$ is measured empirically from THESAN. Is it stable across different ionization models (e.g., different $\zeta, T_\text{vir}$)? The paper doesn't vary these systematically.

4. **Stochasticity:** the paper assumes stochastic scatter is Gaussian and uncorrelated with the bias terms. Non-Gaussian stochasticity (e.g., from rare ionized bubbles) is not addressed.

## Subsequent Work and Related Papers

- **[[Baradaran et al 2024 (Hybrid EFT)]]**: applies the renormalized EFT coefficients from Qin et al. to N-body simulations; shows they generalize beyond the THESAN validation
- **[[Sailer et al 2022 (Optical Depth EFT)]]**: uses the Qin et al. framework for forecasting observational constraints on optical depth

## Open Questions

> [!gap]
> **Cross-code velocity bias:** Does $b_v$ vary significantly across different codes? If yes, is it as well-behaved as $b_1$, or does it encode more simulator-specific information? For P2, this affects whether the inferred velocity bias is simulator-independent.

> [!gap]
> **Real-space vs. redshift-space ionization field:** P1 works in real space. But P2 must connect real-space EFT coefficients to redshift-space observations. Is the mapping clean, or does simulator dependence creep back in at this stage?

> [!gap]
> **Non-linear redshift space:** the expansion assumes linear theory growth rate $f$. At higher $k$, $f$ is modified by non-linear effects. How large is this correction at $k \sim 0.8$?

## For Your Thesis: Action Items

1. **Adopt renormalization:** P1 must use renormalized bias coefficients to ensure resolution independence when comparing 21cmFAST and SCRIPT
2. **Real-space focus:** P1 focuses on ionization field (real space), so velocity bias is not directly relevant; but document this
3. **Prepare for P2:** ensure P1's coefficients can be connected to redshift-space observables via the Qin et al. framework
