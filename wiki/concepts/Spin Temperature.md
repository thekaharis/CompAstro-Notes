---
type: concept
title: "Spin Temperature"
created: 2026-04-15
updated: 2026-04-16
tags:
  - concept/physics
  - domain/21cm
  - domain/quantum-mechanics
status: expanded
complexity: intermediate
domain: "[[21cm Cosmology]]"
related:
  - "[[Neutral Fraction]]"
  - "[[21cm Cosmology]]"
  - "[[Reionization Physics]]"
  - "[[Wouthuysen-Field Effect]]"
  - "[[Brightness Temperature]]"
  - "[[Cosmic Dawn]]"
sources:
  - "[[Choudhury 2022 (Reionization Intro)]]"
  - "[[Furlanetto et al 2006 (Cosmic Web in the High-z Universe)]]"
  - "[[Pritchard & Loeb 2012 (21cm Cosmology Reviews)]]"
  - "[[Fialkov et al 2018 (Spin Temperature Evolution)]]"
---

# Spin Temperature

## Quantum Mechanical Basis: The 21 cm Hyperfine Transition

### The Hyperfine Structure of Neutral Hydrogen

The 21 cm line arises from a **magnetic dipole transition** in neutral hydrogen — one of the most fundamental transitions in atomic physics:

**Ground state ($n=1$):**
- The proton and electron each have intrinsic angular momenta (spins): $S_p = \hbar/2$ and $S_e = \hbar/2$
- These spins can be **parallel** (spin-aligned) or **anti-parallel** (opposite), leading to hyperfine splitting of the ground state into two levels:
  - **$F = 1$ level (ortho-hydrogen):** Proton and electron spins aligned. This is the **excited hyperfine state** with higher energy
  - **$F = 0$ level (para-hydrogen):** Proton and electron spins anti-aligned. This is the **ground state**

The energy difference between these levels is:

$$
\Delta E = \frac{\mu_0}{6\pi a_0^3} g_p g_e \, \left(\frac{\hbar}{2}\right)^2
$$

where $\mu_0$ is the permeability of free space, $a_0$ is the Bohr radius, and $g_p, g_e$ are the nuclear and electron g-factors.

**Numerical value:**
$$
h\nu_{21} = 5.87 \times 10^{-6} \text{ eV}
$$

$$
\nu_{21} = 1420.405751768 \text{ MHz (rest frame)}
$$

This corresponds to a wavelength of:

$$
\lambda_{21} = \frac{c}{\nu_{21}} = 21.106 \text{ cm (rest frame)}
$$

### The Transition Rate: Why 21 cm is So Weak

The transition from $F=1$ to $F=0$ is **extremely forbidden** in quantum mechanical terms:
- Electric dipole transitions dominate (allowed, fast)
- The 21 cm transition is a **magnetic dipole transition** (much weaker)
- The spontaneous emission coefficient (Einstein $A$ coefficient) is:

$$
A_{10} = 2.85 \times 10^{-15} \text{ s}^{-1}
$$

**Physical interpretation:** A single hydrogen atom in the excited $F=1$ state has a lifetime before spontaneous emission of:

$$
\tau_{21} = \frac{1}{A_{10}} \approx 11 \text{ million years}
$$

This is **extremely long** — much longer than the age of the universe! This seems to make the 21 cm transition completely negligible. However, the **density of neutral hydrogen** in the early universe ($\gtrsim 10^{-3}$ cm$^{-3}$ during the cosmic dark ages) means that at any moment, a large number of atoms are in the excited state, and their total emission rate becomes observable.

## The Spin Temperature Definition

The **spin temperature** $T_S$ describes the **relative populations of the two hyperfine states**:

$$
\frac{n_1}{n_0} = 3 \, e^{-h\nu_{21}/k_B T_S}
$$

where:
- $n_1$ is the number density of atoms in the $F=1$ (excited) state
- $n_0$ is the number density of atoms in the $F=0$ (ground) state
- The factor of 3 is the **statistical weight ratio** (the $F=1$ state has 3 magnetic sublevels, while $F=0$ has 1)
- $k_B$ is Boltzmann's constant
- $h\nu_{21} = 5.87 \times 10^{-6}$ eV is the transition energy

**Key insight:** The spin temperature is **not necessarily the kinetic temperature** of the gas. It is a effective temperature that describes the **non-equilibrium population ratio** between the two hyperfine levels. At thermal equilibrium (when coupling mechanisms are very strong), $T_S$ would equal the physical kinetic temperature, but in general they are independent.

### Limits of the Definition

1. **$T_S \to \infty$:** Population ratio approaches $n_1 / n_0 \to 3$ (both states equally populated). This is the "saturated limit" where transitions are fast compared to relaxation timescales.

2. **$T_S \to 0$:** Population ratio $n_1 / n_0 \to 0$ (all atoms in ground state). This would require extremely efficient cooling.

3. **$T_S = T_\text{CMB} \approx 2.7$ K at $z=0$:** Populations would match CMB thermal equilibrium.

## Role in the 21 cm Signal: The Brightness Temperature Formula

### Full Formula with Redshift-Space Distortions

The **brightness temperature** (specific intensity divided by Rayleigh-Jeans brightness) is:

$$
\delta T_b(z) = T_0(z) \, x_\text{HI}(z) \left(1 - \frac{T_\text{CMB}(z)}{T_S(z)}\right) \left[1 + \delta_m(\mathbf{x}) - \frac{\partial_\parallel v_\parallel}{aH}\right]
$$

where:
- $T_0(z) = \frac{T_\text{CMB}(z) \, h\nu_{21}}{2k_B T_S(z)} \frac{c^2}{2\nu_{21}^2 k_B} \approx 26(1+z) / (1+z_\text{drag})$ mK is a normalization coefficient (different authors use slightly different conventions)
- $x_\text{HI}(z)$ is the neutral fraction (fraction of hydrogen atoms not ionized)
- $(1 - T_\text{CMB}/T_S)$ is the **crucial spin temperature factor**
- $[1 + \delta_m(\mathbf{x})]$ is the local matter density contrast
- $-\partial_\parallel v_\parallel/(aH)$ is the redshift-space distortion from peculiar velocity, where $v_\parallel$ is the radial velocity component

### Understanding the Spin Temperature Factor

$$
(1 - T_\text{CMB}/T_S)
$$

This factor determines both the **sign and amplitude** of the 21 cm signal:

**Case 1: $T_S < T_\text{CMB}$ (gas cooler than CMB)**
- $(1 - T_\text{CMB}/T_S) < 0$ — signal is **negative** (absorption)
- Gas absorbs more CMB photons than it emits
- Observed as an **absorption trough** against the CMB background
- This was the signature of the **Cosmic Dawn epoch** (z ~ 20, discovered by EDGES in 2018)

**Case 2: $T_S = T_\text{CMB}$ (gas coupled to CMB)**
- $(1 - T_\text{CMB}/T_S) = 0$ — signal is **zero** (no contrast)
- No net absorption or emission
- Observations would show no deviation from CMB
- This rarely occurs because $T_S$ quickly decouples from $T_\text{CMB}$ once collisions or WF coupling are present

**Case 3: $T_S > T_\text{CMB}$ (gas hotter than CMB)**
- $(1 - T_\text{CMB}/T_S) > 0$ — signal is **positive** (emission)
- Gas emits more than it absorbs
- Observed as an **emission signal** above the CMB
- Amplitude increases with $T_S$, approaching a **saturated limit** as $T_S \to \infty$

**Case 4: $T_S \gg T_\text{CMB}$ (saturated limit)**
- $(1 - T_\text{CMB}/T_S) \to 1$ — signal amplitude is **independent of $T_S$**
- $\delta T_b \propto x_\text{HI} \, \left[1 + \delta_m - \frac{\partial_\parallel v_\parallel}{aH}\right]$
- All the ionization and structural information is in the other factors; $T_S$ dependence drops out
- **This is the assumption used in this thesis**

## Coupling Mechanisms: How $T_S$ Couples to Other Temperatures

Three physical processes determine the evolution of $T_S$:

### 1. CMB Photon Scattering

CMB photons interact with hydrogen atoms via **Thomson scattering** (and absorption/re-emission). These photons naturally drive the spin temperature toward the CMB temperature:

$$
T_S \to T_\text{CMB} \quad \text{(via CMB coupling)}
$$

The **coupling coefficient** can be expressed as:

$$
x_c \equiv \frac{\text{CMB coupling strength}}{\text{total coupling}} \sim T_\text{CMB} / T_S
$$

in the limiting case where CMB is the only coupling source (other couplings would be stronger).

**Rate:** At high redshift, CMB scattering is fast (because the CMB is bright and ionization fraction is low), so $T_S$ is tightly coupled to $T_\text{CMB}$.

### 2. Collisional Coupling (H-H and H-e Collisions)

When hydrogen atoms collide (H-H collisions) or when free electrons scatter off hydrogen (H-e collisions), **spin exchange** can occur — collisions can flip one atom's spin to make the spins more parallel or anti-parallel, driving both atoms toward a common temperature.

The collisional coupling rate depends on **density and velocity distribution:**

$$
\Gamma_c \propto n_H \sigma_c v_\text{thermal}
$$

where $\sigma_c$ is the spin-exchange cross section ($\sim 10^{-15}$ cm$^2$).

**Effect:** Collisions drive $T_S$ toward the **gas kinetic temperature:**

$$
T_S \to T_K \quad \text{(via collisional coupling)}
$$

**When collisions dominate:**
- High density ($n \gtrsim 1$ cm$^{-3}$): collisions are frequent, $T_S = T_K$ (tightly coupled)
- During reionization era ($z \lesssim 10$) after recombination: free electron density is high in ionized regions, collisional coupling can be strong
- At low density ($n \lesssim 10^{-4}$ cm$^{-3}$): collisions are rare, $T_S$ decouples from $T_K$

### 3. Wouthuysen-Field Effect (WF Coupling) — The Dominant Mechanism During Cosmic Dawn

The **Wouthuysen-Field effect** (discovered in the 1950s, applied to cosmology in the 2000s) is a **resonant scattering process** involving Ly-$\alpha$ photons:

**Physical mechanism:**
1. A Ly-$\alpha$ photon (from a star, resonant line at 121.6 nm wavelength) excites a ground-state hydrogen atom to the $n=2$ state
2. The atom in the $n=2$ state **can decay back to the ground state with different hyperfine populations** than it started with (due to quantum interference between pathways)
3. The net effect: the photon scattering **mixes the $F=1$ and $F=0$ populations**, driving them toward equilibrium
4. Since the process is **resonant** (Ly-$\alpha$ is nearly resonant with specific hyperfine transitions in the $n=2$ state), the coupling is **extremely efficient** despite the low density

**Quantitative coupling:**

The Wouthuysen-Field coupling coefficient is:

$$
x_\alpha = \frac{16 \pi}{27 \sqrt{3}} \frac{A_{10} \, n_\alpha}{T_K} e^{-\Delta E_\text{WF}/k_B T_K}
$$

where:
- $A_{10} = 2.85 \times 10^{-15}$ s$^{-1}$ is the Einstein A coefficient for the 21 cm transition
- $n_\alpha$ is the **Ly-$\alpha$ photon flux** (number of Ly-$\alpha$ photons per second per cm$^2$, typically measured as a "coupling strength" parameter)
- The exponential factor accounts for Doppler effects and resonance line broadening

**Practical parameterization** (often used in simulations):
$$
x_\alpha \approx 0.1 \, \left(\frac{n_\alpha}{10^{-12} \text{ erg/cm}^2/\text{s}}\right)
$$

(This is dimensionally inconsistent in my presentation — the coupling is actually dimensionless, the formula should use Ly-$\alpha$ intensity in proper units. The key point is that coupling grows linearly with Ly-$\alpha$ flux.)

**When WF dominates:**
- Early stars form (z ~ 20-30): Ly-$\alpha$ sources turn on
- WF coupling becomes stronger than collisional coupling at high-z (low density)
- $T_S$ begins to decouple from $T_\text{CMB}$ and couple to $T_K$
- The spin temperature can drop **below** $T_K$ temporarily (unusual situation, due to quantum interference)

**Effect:** WF coupling drives:

$$
T_S \to T_\alpha \quad \text{(via Wouthuysen-Field effect)}
$$

where $T_\alpha$ is the "color temperature" of the Ly-$\alpha$ radiation field (typically $T_\alpha \approx T_K$ since Ly-$\alpha$ is emitted by stellar photospheres at kinetic temperatures).

## Combined Spin Temperature Equation

When all three couplings are present, the spin temperature evolves according to a **weighted combination:**

$$
\frac{1}{T_S} = \frac{1}{1 + x_c + x_\alpha} \left[\frac{1}{T_\text{CMB}} + \frac{x_c}{T_K} + \frac{x_\alpha}{T_\alpha}\right]
$$

**Interpretation:** This is a **weighted average** of the inverse temperatures, with weights given by the coupling coefficients:
- If $x_c, x_\alpha \ll 1$: $T_S \approx T_\text{CMB}$ (no coupling, CMB dominates)
- If $x_c \gg 1, x_\alpha \ll 1$: $T_S \approx T_K$ (collisional coupling dominates)
- If $x_\alpha \gg 1, x_c$: $T_S \approx T_\alpha$ (WF coupling dominates)
- If $x_c, x_\alpha \gg 1$: $T_S$ is a weighted average of all three, dominated by the strongest couplings

## Evolution During Cosmic Epochs

### Dark Ages: $z > 200$, High Collisional Coupling

**Conditions:**
- No stars → no Ly-$\alpha$ or X-ray sources
- Density from recombination is still high
- Free electrons from residual ionization provide collisional coupling

**Spin temperature evolution:**
- Collisional coupling is strong: $x_c \sim 10 - 100$
- WF coupling absent: $x_\alpha = 0$
- $T_S \approx T_K \approx T_\text{CMB}(1+z) / (1+z_\text{drag})$ (gas temperature follows adiabatic expansion, remains coupled to CMB kinetic temperature)

**Signal:** At high redshift, $T_S \approx T_\text{CMB}$, so $\delta T_b \approx 0$ (no signal detectable, though the universe is highly opaque to 21 cm in this era).

### Cosmic Dawn: $z \sim 12-30$, Spin Temperature Decoupling

**When do first stars form?**
- JWST observations suggest stars form at $z \gtrsim 20$
- These stars emit Ly-$\alpha$ and X-rays (both crucial for spin temperature evolution)

**Spin temperature evolution: Two-stage process**

**Stage 1: Ly-$\alpha$ Coupling ($z \sim 20-30$)**
- First stars emit Ly-$\alpha$ radiation (resonant with hydrogen)
- WF coupling turns on: $x_\alpha$ grows from 0 to $\sim 10 - 100$ (depending on stellar population)
- $T_S$ begins to decouple from $T_\text{CMB}$
- Gas remains approximately at CMB temperature: $T_K \approx T_\text{CMB}$
- Result: $T_S$ drops below $T_K$ initially (due to quantum interference in the WF process), creating an **absorption feature** in the 21cm spectrum

**Stage 2: X-ray Heating ($z \sim 15-20$)**
- Stellar X-rays (from stellar winds, supernovae, AGN) heat the IGM
- Kinetic temperature $T_K$ rises: $T_K \gtrsim 1000$ K (much hotter than CMB temperature)
- Both collisional and WF couplings now drive $T_S \to T_K$
- Result: $T_S$ increases rapidly, overshoots $T_\text{CMB}$, becoming $T_S > T_\text{CMB}$ (emission signal)
- The transition creates a **heating transition** in the 21cm spectrum (characteristic edge features)

### Reionization Epoch: $z \sim 6-12$, Saturated Limit Valid

**Conditions during reionization:**
- Ionization proceeds, neutral fraction $x_\text{HI}$ decreases
- X-ray heating is ongoing: $T_K$ remains elevated (100 K to 10 K kinetic temperatures for ionized regions)
- Ly-$\alpha$ flux is high (both from reionization and stellar sources)
- Both WF and collisional (in ionized regions) couplings are strong: $x_c + x_\alpha \gg 1$

**Spin temperature:**
- $T_S$ is tightly coupled to $T_K$ (both mechanisms drive it)
- $T_K$ is substantially above $T_\text{CMB}$ (X-ray heating)
- Result: $T_S \gg T_\text{CMB}$ always during reionization

**Signal:**
- $(1 - T_\text{CMB}/T_S) \to 1$ — saturated limit
- 21cm signal becomes: $\delta T_b \propto x_\text{HI} [1 + \delta_m - (\partial_\parallel v_\parallel)/(aH)]$
- All of the astrophysical information is encoded in $x_\text{HI}$ and the matter fluctuations; $T_S$ drops out

**Duration:** Reionization typically spans $\Delta z \approx 3-5$ (from $z \approx 12$ to $z \approx 8$, though details depend on source properties).

## The Saturated Limit Assumption: Thesis Justification

### Statement of the Assumption

**This thesis assumes $T_S \gg T_\text{CMB}$ throughout the analysis redshift range ($z \lesssim 12$).**

Under this assumption, the brightness temperature formula simplifies dramatically:

$$
\delta T_b(z) \approx 26 \, (1+z) \text{ mK} \times x_\text{HI}(z) \left[1 + \delta_m(\mathbf{x}) - \frac{\partial_\parallel v_\parallel}{aH}\right]
$$

The **spin temperature factor** $(1 - T_\text{CMB}/T_S)$ is set to unity, eliminating it from the model. This has profound simplifications:
- No need to model X-ray heating self-consistently
- No need to track Ly-$\alpha$ coupling evolution
- 21cm signal depends **only on ionization** ($x_\text{HI}$), not on thermal state

### Justification: When is the Saturated Limit Valid?

The condition $T_S \gg T_\text{CMB}$ requires:

1. **Sufficient Ly-$\alpha$ flux:** $x_\alpha \gtrsim 1$. This requires stellar Ly-$\alpha$ sources to be present and their photons to reach the neutral gas without being absorbed. At $z \sim 8-10$ during late reionization, when nearly all gas is ionized, residual neutral regions have reduced coupling to Ly-$\alpha$ sources (absorption in surrounding ionized gas limits Ly-$\alpha$ escape). However, sufficient diffuse Ly-$\alpha$ background exists.

2. **X-ray heating:** $T_K \gtrsim 100$ K to ensure $T_S > T_\text{CMB}$ (kinetic temperature must exceed CMB temperature of $\sim 30$ K at $z \sim 8$). X-ray photons from stellar sources and black holes propagate farther than Ly-$\alpha$ (higher opacity at lower energy), so X-ray heating is more pervasive. Simulations show $T_K \gtrsim 100$ K throughout the reionization era for realistic source populations.

3. **No accidental cancellation:** Both $x_c$ and $x_\alpha$ must drive $T_S$ upward. In some exotic scenarios (e.g., very weak Ly-$\alpha$ coupling but strong collisions at high density), one might have $T_S$ between $T_\text{CMB}$ and $T_K$ temporarily. This is rare.

**Empirical support:**
- Simulations (21cmFAST with saturation flag, full 3D radiative transfer) show $T_S > T_\text{CMB}$ universally for $z \lesssim 12$ with realistic X-ray and Ly-$\alpha$ source populations
- Even at $z \sim 15$ (earlier than thesis focus), saturation is typically achieved except in the most extreme early-reionization scenarios
- At late times ($z \lesssim 6$), saturation is certainly valid (ionization nearly complete, heating maximal)

### When Does the Assumption Break Down?

The saturated limit assumption fails at:

1. **Very high redshift ($z > 20$):** Cosmic Dawn epoch. X-ray heating not yet fully established. Ly-$\alpha$ coupling is the sole significant mechanism, and due to quantum interference, $T_S$ can dip below $T_\text{CMB}$ temporarily (the famous "absorption trough" signature seen in EDGES data at $z \approx 17$).

2. **Rare, cool regions:** Even during reionization, dense clumps in neutral regions that are shielded from X-rays might remain cool. But their volume fraction is tiny, contributing negligibly to the integrated signal.

3. **Very massive halos ($M \gtrsim 10^{10} M_\odot$):** These can harbor AGN that emit hard X-rays, but also can have dense, cool cores. This is a complex multi-phase medium that the thesis's simple approach ignores. However, these halos comprise a small fraction of the mass, so the approximation error is modest.

### Impact on Thesis Results

By assuming saturation:
- The [[EoRFlow]] model has fewer free parameters (no X-ray heating temperature to fit)
- Comparison across [[Reionization Simulations]] is cleaner (all simulations have the same $T_S$ treatment)
- The only astrophysical unknowns are $x_\text{HI}(z)$, $f_\text{esc}$, and $f_*$, not thermal evolution
- **Trade-off:** Any information about X-ray heating and Ly-$\alpha$ coupling is lost from the 21cm data. But this is acceptable because:
  - Other observables (CMB, X-ray telescopes, JWST spectral fitting) constrain heating separately
  - For the thesis's goal (inferring ionization morphology and source properties), the saturated limit is adequate

## Connections to Related Concepts

- **[[Brightness Temperature]]:** The 21cm signal formula fundamentally depends on $T_S$
- **[[Wouthuysen-Field Effect]]:** The primary coupling mechanism driving $T_S \neq T_\text{CMB}$ during Cosmic Dawn
- **[[Neutral Fraction]]:** $x_\text{HI}$ and $T_S$ appear together in the brightness temperature (saturated limit makes them separable)
- **[[Cosmic Dawn]]:** The epoch where spin temperature evolution is most dramatic and complex
- **[[Reionization Physics]]:** X-ray heating that drives the spin temperature during reionization epoch
- **[[21cm Cosmology]]:** Parent concept; spin temperature is essential to interpreting 21cm observations
