---
type: concept
title: "Neutral Fraction"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/observable
  - domain/reionization
status: developing
domain: "[[Reionization Physics]]"
aliases:
  - "xHI"
  - "ionized fraction"
  - "neutral hydrogen fraction"
  - "reionization history"
related:
  - "[[Ionization Morphology]]"
  - "[[Lyman Alpha Forest]]"
  - "[[Excursion Set Formalism]]"
  - "[[21cm Cosmology]]"
  - "[[Effective Field Theory]]"
sources:
  - "[[Choudhury 2022 (Reionization Intro)]]"
  - "[[Ferrara & Pandolfi (IGM Reionization)]]"
  - "[[Trac & Gnedin 2009 (Reionization Simulations)]]"
---

# Neutral Fraction

## Definition: Volume-Averaged vs. Mass-Averaged

The primary definition is the **volume-averaged neutral hydrogen fraction**:

$$\bar{x}_\text{HI}(z) \equiv \frac{\langle n_\text{HI} \rangle}{\langle n_H \rangle} = \frac{\int d^3x \, n_\text{HI}(\mathbf{x}, z)}{\int d^3x \, n_H(\mathbf{x}, z)}$$

This is the global, redshift-dependent neutral fraction — the primary scalar descriptor of the reionization history. Together with the [[Ionization Morphology]] (the spatial structure), it fully characterizes the ionization state of the IGM at any epoch.

### Mass-Averaged Neutral Fraction

In principle, one could also define a **mass-weighted** neutral fraction:

$$\bar{x}_\text{HI}^{\text{mass}} = \frac{\int d^3x \, \rho(\mathbf{x})\, x_\text{HI}(\mathbf{x})}{\int d^3x \, \rho(\mathbf{x})}$$

where $\rho$ is the matter density. Since neutral gas preferentially resides in high-density regions (dense filaments, galaxies, Lyman-limit systems), we have:

$$\bar{x}_\text{HI}^{\text{mass}} > \bar{x}_\text{HI}^{\text{volume}}$$

in the low-neutral-fraction regime ($\bar{x}_\text{HI} \lesssim 0.1$). This distinction matters because different observational probes sample different density regimes:
- **21 cm:** Sensitive to all neutral hydrogen, both diffuse and dense; approximates volume-average
- **Lyman-alpha forest:** Preferentially sensitive to underdense regions; biased toward lower densities
- **Damped Lyman-alpha systems (DLAs):** Preferentially sensitive to very high densities

For this work, unless otherwise specified, "neutral fraction" refers to the **volume-average** $\bar{x}_\text{HI}(z)$.

## The Reionization History: $\bar{x}_\text{HI}(z)$

The evolution of the volume-averaged neutral fraction from recombination to the present day traces the **reionization history**:

| Epoch | Redshift | $\bar{x}_\text{HI}$ | Physical state | Key probe |
|-------|----------|------|------|------|
| **Recombination** | $z \sim 1100$ | $\approx 1$ | Neutral IGM forms; recombination of H and He | CMB |
| **Dark Ages** | $z \sim 20$–$1100$ | $\approx 1$ | Universe expands and cools; no ionizing sources | (none; unobservable) |
| **Cosmic Dawn** | $z \sim 15$–$20$ | $\approx 1$ | First stars form; faint X-rays begin heating | (21 cm absorption?) |
| **Epoch of Reionization (EoR)** | $z \sim 6$–$15$ | $1 \to 0$ | Ionization by galaxies and quasars; state changes from mostly neutral to mostly ionized | 21 cm, Ly$\alpha$ emitters, Ly$\alpha$ forest |
| **Post-reionization** | $z \lesssim 6$ | $\lesssim 10^{-3}$ | Nearly fully ionized; only dense absorbers remain neutral | Quasar absorption, Ly$\alpha$ forest |
| **Present day** | $z = 0$ | $\sim 10^{-4}$ | Fully ionized except in miniature galaxies (absorption in ultra-faint dwarf galaxies) | Local 21 cm surveys |

Different physical models predict different **shapes** for the reionization history:

1. **Rapid reionization** (e.g., high escape fraction $f_\text{esc} \sim 0.3$, early-forming galaxies):
   - Sharp transition: $\bar{x}_\text{HI}$ drops from ~0.5 to ~0.01 over $\Delta z \sim 1$
   - Centered at $z_\text{mid} \sim 7.5$–$8$
   - Predicted by some simulations with strong feedback

2. **Extended reionization** (e.g., low $f_\text{esc} \sim 0.05$, late-forming sources):
   - Gradual transition: $\bar{x}_\text{HI}$ decreases smoothly over $\Delta z \sim 3$–$5$
   - Midpoint $z_\text{mid} \sim 6$–$7$
   - Typical of lower-feedback models

3. **Multi-phase reionization** (e.g., early mini-quasars, then galaxies):
   - Multiple transitions with inflection points
   - Less commonly considered but not ruled out

## Observational Constraints

The global $\bar{x}_\text{HI}(z)$ is constrained by several complementary observational probes, each sensitive to different density regimes and redshift ranges:

### 1. CMB Optical Depth ($\tau_e$)

The **electron scattering optical depth** of the CMB is:

$$\tau_e = \int_0^{z_*} dz' \frac{dt'}{dz'} \sigma_T n_e(z') = \sigma_T \int_0^{z_*} dz' \frac{(1+z')}{H(z')} \bar{n}_e(z')$$

where $\bar{n}_e = \bar{n}_H (1 - \bar{x}_\text{HI})$ is the volume-averaged electron density and $\sigma_T$ is the Thomson scattering cross-section. $\tau_e$ is sensitive to when electrons (from ionized hydrogen and helium) are present in the universe.

**Current measurement (Planck 2021):**
$$\tau_e = 0.054 \pm 0.007$$

This is the tightest global constraint on the reionization history. Inverting the integral gives a **mean reionization redshift** $z_\text{re}$:

$$z_\text{re} \approx 7.0 \pm 0.8$$

with some model dependence on the assumed shape of $\bar{x}_\text{HI}(z)$ (e.g., whether reionization is abrupt or extended).

**Strengths:** Precise measurement; constrains integral of ionized fraction over time

**Weaknesses:** Degenerate — many different $\bar{x}_\text{HI}(z)$ histories can give the same $\tau_e$; cannot pin down detailed shape

### 2. Lyman-alpha Forest and Gunn-Peterson Troughs

The **Gunn-Peterson (GP) trough** is a dramatic feature in quasar absorption spectra at $z > 5.3$: the Ly$\alpha$ optical depth jumps from modest values ($\tau_\text{Ly}\alpha \sim 5$–$10$ at $z \sim 5$) to extreme values ($\tau_\text{Ly}\alpha \gtrsim 1000$ at $z > 6$) over a very short redshift range ($\Delta z \lesssim 0.5$).

The optical depth scales as:

$$\tau_\text{Ly}\alpha \propto (1-\bar{x}_\text{HI})\,n_H$$

Thus a jump in $\tau_\text{Ly}\alpha$ indicates a jump in neutral fraction. The observed rapid evolution at $z \approx 5.5$–$6.5$ is consistent with:

$$\bar{x}_\text{HI}(z=6) \sim 10^{-4}\text{ to } 10^{-3}$$

— i.e., *very small* neutral fractions at $z = 6$. This is **not** consistent with a gentle, extended reionization; the data prefer rapid completion by $z \sim 6$.

**Why the saturation?** At neutral fractions $\bar{x}_\text{HI} \gtrsim 10^{-3}$, even tiny amounts of neutral gas produce enormous optical depths due to the Ly$\alpha$ cross-section. Thus the GP trough saturates and cannot directly measure $\bar{x}_\text{HI}$ in the range $0.01 < \bar{x}_\text{HI} < 1$ — it only tells us that reionization was mostly complete by $z = 6$.

**Quantitative constraints:**
- $z \sim 5.8$: $\bar{x}_\text{HI} < 10^{-4}$ (Becker et al. 2015, Fan et al. 2006)
- $z \sim 6.5$: $\bar{x}_\text{HI} \sim 10^{-3}$ to $10^{-2}$ (strong evolution)
- $z \sim 7$: $\bar{x}_\text{HI} \sim 0.1$–$0.3$ (extrapolation; not directly measured)

**Lyman-alpha forest at $z = 2$–$5$:** The statistics of the forest can constrain mean free path and UV background; confirms that by $z \sim 2$, reionization is complete and the IGM is fully ionized.

### 3. Lyman-alpha Emitter (LAE) Abundance

Lyman-alpha photons from galaxies are easily scattered by neutral hydrogen (Ly$\alpha$ has a large scattering cross-section). When the IGM is partially ionized, LAEs suffer attenuation and their observed number density drops sharply.

The **LAE visibility** declines by a factor ~10 between $z \sim 6$ (where $\bar{x}_\text{HI} \sim 0.1$–$0.3$) and $z \sim 7$ (where $\bar{x}_\text{HI} \sim 0.5$). This provides a loose constraint on the midpoint of reionization:

$$z_\text{mid} \sim 6.5 \text{ to } 7.5$$

Quantitatively, the LAE number density evolves as $n_\text{LAE}(z) \propto \exp(-\tau_\text{eff})$ where $\tau_\text{eff} \propto (1-\bar{x}_\text{HI})$. A sharp decline in LAE counts around $z \sim 7$ is evidence for the reionization midpoint.

**Strengths:** Direct probe of large-scale ionization at the relevant redshifts

**Weaknesses:** Degenerate with galaxy evolution (fewer galaxies at high-$z$ even without reionization); requires detailed radiative transfer models to extract $\bar{x}_\text{HI}$

### 4. 21 cm Power Spectrum (Future: HERA, SKA)

The 21 cm brightness temperature power spectrum directly encodes $\bar{x}_\text{HI}(z)$ and the morphology:

$$\delta T_b \propto (1 - \bar{x}_\text{HI}) \left[\delta_b - \frac{\delta \bar{T}_s}{\bar{T}_s}\right]$$

where the factor $(1 - \bar{x}_\text{HI})$ weights the brightness by the neutral fraction. Measuring the power spectrum across multiple redshifts and fitting to models of $\bar{x}_\text{HI}(z)$ constrains the full history.

**Strengths:** High sensitivity to $\bar{x}_\text{HI}$; ability to map the full spatial structure (morphology), not just global average

**Weaknesses:** Challenges with foreground removal and calibration; requires simulations to interpret

## Local vs. Global Neutral Fraction

The **local** neutral fraction $x_\text{HI}(\mathbf{x}, z)$ is a 3D field that varies in space. Its value depends on local density, proximity to sources, and photon absorption. This field appears directly in the 21 cm brightness temperature:

$$T_b \propto (1 - x_\text{HI})\,\beta_c\,T_s$$

where $\beta_c$ is a collisional coupling coefficient.

The **global** (or volume-averaged) neutral fraction $\bar{x}_\text{HI}(z)$ is the spatial average of this field. It is what EoRFlow and other inference pipelines reconstruct from 21 cm power spectra.

The relationship between local and global enters the [[Effective Field Theory]] description. The ionization field fluctuation is:

$$\delta_x(\mathbf{x}) = x_\text{HII}(\mathbf{x}) - \bar{x}_\text{HII}$$

where $x_\text{HII} = 1 - x_\text{HI}$ is the ionized fraction. The bias expansion is:

$$\delta_x = b_1^x\,\delta_m + b_2^x\,\delta_m^2 + b_{\nabla^2}^x\,\nabla^2 \delta_m + \ldots$$

The coefficient $b_1^x$ explicitly contains the global ionized fraction:

$$b_1^x \approx \bar{x}_\text{HII} - \bar{x}_\text{HI}\,b_{S,1}$$

where $b_{S,1}$ is the bias of sources (galaxies producing ionizing photons). Thus measuring $b_1^x$ at a known $\bar{x}_\text{HII}$ constrains the source bias $b_{S,1}$, which is otherwise difficult to measure directly.

## The Photon Budget Problem

The global photon budget is a fundamental constraint:

$$\dot{n}_\text{ion} = \dot{n}_\text{rec} + \frac{d}{dt}[n_H (1 - \bar{x}_\text{HI})]$$

where:
- $\dot{n}_\text{ion}$ = ionizing photon production rate (from stars and quasars)
- $\dot{n}_\text{rec}$ = recombination rate (depends on clumping factor $C$, temperature, density)
- RHS second term = rate of increase of ionized volume

At $z \sim 6$ with rapid reionization, the photon production must barely keep pace with recombinations in the diffuse gas plus the rapid increase in ionized volume. Estimates suggest:

$$\frac{\dot{n}_\text{ion}}{n_H} \sim C \cdot \alpha \cdot n_e \cdot n_p + (1 - \bar{x}_\text{HI}) \frac{d\bar{x}_\text{HI}}{dt}$$

With $C \sim 3$ (clumping factor), ionization cross-section $\alpha \sim 2 \times 10^{-13}\,\text{cm}^3\,\text{s}^{-1}$, typical IGM conditions, and rapid evolution $d\bar{x}_\text{HI}/dt \sim 0.1\,\text{Myr}^{-1}$, the required ionizing photon production is extremely tight. This is the **"photon budget problem"**:

There are barely enough ionizing photons produced by known galaxies and quasars to reionize the universe by $z = 6$. Matching the observed reionization history requires:
- Ionizing escape fractions $f_\text{esc} \sim 0.1$–$0.2$ (higher than direct measurements of local galaxies, ~5%)
- Or additional ionizing sources not yet discovered (early quasars, Pop III stars, etc.)
- Or low recombination rates (low clumping factor or unusual metallicity)

This tension is one of the deepest unsolved problems in reionization physics and motivates the need for precise 21 cm measurements to test different scenarios.

## Role in This Thesis

This thesis uses 21 cm observations (or simulations thereof) to constrain the **spatial structure** of reionization, not just the global $\bar{x}_\text{HI}(z)$ history:

- **P2 (EoRFlow-adjacent):** Reconstructs $\bar{x}_\text{HI}(z)$ — the scalar history — from 21 cm power spectra
- **P1 (this work):** Goes deeper by characterizing the *fluctuations* of $x_\text{HII}(\mathbf{x})$ through EFT coefficients $b_1^x$, $b_2^x$, $b_{\nabla^2}^x$, and noise

The coefficient $b_1^x$ is particularly interesting because it contains $\bar{x}_\text{HI}$ explicitly in its expression, linking the global history to local bias:

$$b_1^x(\bar{x}_\text{HII}) \approx \bar{x}_\text{HII} - \bar{x}_\text{HI}\,b_{S,1}$$

Thus EFT extraction can use the known global $\bar{x}_\text{HII}(z)$ (measured separately) to infer the source clustering $b_{S,1}$, which is an astrophysical property of ionizing sources and feeds back into understanding galaxy evolution at high redshift.

## See Also

- [[Ionization Morphology]] — the spatial structure at each $\bar{x}_\text{HI}$
- [[Lyman Alpha Forest]] — observational probe of neutral fraction at lower redshifts
- [[Excursion Set Formalism]] — the physical model that predicts $\bar{x}_\text{HI}(z)$ evolution
- [[21cm Cosmology]] — how neutral fraction enters the observed 21 cm signal
- [[Effective Field Theory]] — how neutral fraction enters EFT bias coefficients
- [[Clumping Factor]] — affects the photon budget and hence $\bar{x}_\text{HI}$ evolution
