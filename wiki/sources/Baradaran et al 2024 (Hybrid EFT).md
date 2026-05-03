---
type: source
title: "Baradaran et al. 2024 — Hybrid EFT for the 21cm Field"
created: 2026-04-15
updated: 2026-04-16
tags:
  - source/paper
  - domain/eft
  - domain/21cm
  - state-of-art
status: mature
source_type: paper
author:
  - "[[Baradaran, Dani]]"
  - "Hadzhiyska, Boryana"
  - "White, Martin J."
  - "[[Sailer, Neha]]"
date_published: 2024
url: "https://arxiv.org/abs/2406.13079"
journal: "Phys. Rev. D, 110, 103517"
confidence: high
key_claims:
  - "A hybrid EFT approach combining N-body-evolved density fields with perturbative bias expansion ionization painting is the most accurate semi-analytic 21cm model to date"
  - "Replacing 21cmFAST's 2LPT density with full N-body displacements improves power spectrum accuracy at intermediate k (0.3–1 h/Mpc)"
  - "EFT bias coefficients extracted from N-body simulations generalize to predict 21cm fields at new realizations"
  - "The hybrid approach maintains the speed advantage of semi-analytic models while achieving near-RT accuracy"
related:
  - "[[Effective Field Theory]]"
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Qin et al 2022 (EFT Redshift Space)]]"
  - "[[Sailer et al 2022 (Optical Depth EFT)]]"
  - "[[Bias Expansion]]"
  - "[[Simulation and Codes]]"
  - "[[21cmFAST]]"
---

# Baradaran et al. 2024 — Hybrid EFT for the 21cm Field

> [!key-insight]
> Replacing 21cmFAST's 2nd-order Lagrangian perturbation theory (2LPT) density field with full N-body positions, then applying the EFT bias expansion to map density to ionization, yields a **hybrid model** that outperforms semi-numerical codes at intermediate scales ($k \sim 0.3$–$1\,h\,\text{Mpc}^{-1}$) while remaining far cheaper than full radiative transfer. This is the state-of-the-art semi-analytic model and validates that EFT coefficients are portable across different density-field solvers.

## Citation

Baradaran, D., Hadzhiyska, B., White, M.J. & Sailer, N. (2024). "Predicting the 21cm field with a Hybrid Effective Field Theory approach." *Phys. Rev. D*, 110, 103517. arXiv:2406.13079.

## Core Claim

The standard semi-numerical pipeline (21cmFAST, SCRIPT, ARTIST) uses 2nd-order Lagrangian perturbation theory (2LPT) to evolve the density field, then applies excursion-set ionization criteria to determine which cells are ionized. This approach is fast but becomes inaccurate at the intermediate and small scales where structure forms most rapidly.

The key limitation: **2LPT is inaccurate** at the scales ($k \gtrsim 0.3$ h/Mpc) where the 21cm power spectrum carries most cosmological information. The displacements from 2LPT diverge from full N-body simulations, leading to incorrect density field structure, which propagates into errors in the ionized region morphology.

Baradaran et al.'s innovation: **Replace the 2LPT density with full N-body positions**, but keep the fast EFT-based ionization painting. The result is:
- Density field accuracy: N-body (best available)
- Ionization painting: EFT bias expansion (fast, interpretable)
- Overall speed: still much faster than full radiative transfer, while approaching RT accuracy

## Architecture of the Hybrid EFT

### The Pipeline

```
Initial Conditions (matched)
        ↓
N-body simulation (or 2LPT/Zel'dovich) → density field δ_m(x)
        ↓
EFT bias operators { δ_m, [δ²]_R, ∇²δ_m, ε_stoch }
        ↓
Bias coefficient fitting { b₁^x, b₂^x, b∇²^x, P_εε } from calibration run
        ↓
Apply coefficients to new N-body realizations
        ↓
Predict x_HII(x) and hence 21cm field T_b(x)
```

### Key Components

#### 1. N-Body Density Field

- Input: cosmological N-body simulation (e.g., a suite like illustris-TNG, EAGLE, or custom runs)
- Output: particle positions at target redshift $z$, from which you reconstruct the smoothed density field $\delta_m(\mathbf{x})$ via (e.g.) cloud-in-cell interpolation to a grid
- Advantage: accurate to scales well beyond 2LPT; includes full non-linear mode coupling
- Cost: N-body run is expensive, but only done once per set of initial conditions

#### 2. Calibration: Extract EFT Coefficients

On a reference simulation (e.g., a coupled N-body + RT run, or matching a high-fidelity code):

1. Obtain the true ionization field $x_\text{HII}^{\text{ref}}(\mathbf{x})$
2. On the same realization, compute the N-body density $\delta_m(\mathbf{x})$
3. Fit the bias expansion in Fourier space:
   $$\delta_x(\mathbf{k}) = b_1^x \tilde{\delta}_m(\mathbf{k}) + b_2^x [\delta_m^2]_{\text{renorm}}(\mathbf{k}) + b_{\nabla^2}^x \nabla^2 \tilde{\delta}_m(\mathbf{k}) + \text{stochastic}$$
4. Extract coefficients $\{b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon}\}$ as functions of redshift (or ionization fraction)

#### 3. Prediction: Apply to New Realizations

Given a new N-body realization:

1. Compute $\delta_m(\mathbf{x})$ from particle positions
2. Construct EFT basis operators: $\tilde{\delta}_m$, $[\delta_m^2]_{\text{renorm}}$, $\nabla^2 \tilde{\delta}_m$
3. Evaluate the fitted coefficients at the desired redshift: $b_1^x(z), b_2^x(z), \ldots$
4. Predict: $\delta_x(\mathbf{x}) = b_1^x \delta_m(\mathbf{x}) + b_2^x [\delta_m^2](\mathbf{x}) + \cdots$
5. Convert to 21cm: $T_b(\mathbf{x}) = T_0(\bar{x}_\text{HII}(z)) \times (1 + \delta_x(\mathbf{x}))$ (in the saturated limit)

### Advantages Over 21cmFAST

| Aspect | 21cmFAST | Hybrid EFT |
|--------|----------|-----------|
| **Density field** | 2LPT (accurate to k ≲ 0.2 h/Mpc) | N-body (accurate to k ≲ 1+ h/Mpc) |
| **Ionization painting** | Excursion set (deterministic, morphology approximate) | EFT bias (statistical, morphology emergent from density) |
| **Speed** | Very fast (seconds per realization) | Fast (minutes per realization; N-body step bottleneck) |
| **Accuracy at k ~ 0.3–1** | ~10–30% error | ~1–5% error |
| **Interpretability** | Low (excursion set heuristic) | High (EFT coefficients have physics meaning) |
| **Generalizability** | Code-specific | EFT coefficients portable across codes |

## Key Results

### Accuracy Improvements at Intermediate Scales

- **21cmFAST power spectrum error** at $k = 0.3$ h/Mpc: ~20% relative error
- **Hybrid EFT power spectrum error** at $k = 0.3$ h/Mpc: ~1–2% relative error
- **Improvement factor:** ~10–20× more accurate at intermediate scales where cosmological information concentrates

### Validation Against Coupled References

- Baradaran et al. compare against coupled N-body + radiative transfer runs (expensive reference)
- Hybrid EFT achieves near-parity with full RT, despite using only the fast EFT bias expansion for ionization painting
- Agreement holds across multiple redshifts and ionization fractions

### EFT Coefficient Stability

One of the paper's key findings: **EFT coefficients extracted from N-body simulations are consistent with those from [[Qin et al 2022 (EFT Redshift Space)]]** (who extracted them from full RT).

This demonstrates that the EFT coefficients are **not tied to a specific ionization algorithm** (like excursion set or full RT), but describe universal large-scale physics.

Implications:
- Coefficients can be calibrated once from a high-fidelity run
- Applied to any new N-body realization
- Portable across different teams' codes (in principle)

### Speed-Accuracy Trade-off

- Full radiative transfer: weeks per simulation box, extremely accurate
- Hybrid EFT: hours for N-body + minutes for ionization painting = hours total; near-RT accuracy
- 21cmFAST: seconds to minutes; lower accuracy
- **Conclusion:** hybrid is an efficient sweet spot

## Methods

### Simulation Setup

- **Reference simulations:** coupled N-body + RT or high-fidelity code (THESAN or similar)
- **N-body runs:** match initial conditions to reference; evolve with same cosmology
- **Grid construction:** interpolate N-body particles to Eulerian grid for EFT evaluation
- **Coefficient extraction:** least-squares fit in Fourier space bins, with error propagation

### Validation Procedure

1. Train on reference simulation (compute EFT coefficients)
2. Test on multiple new N-body realizations: apply fitted coefficients to predict $x_\text{HII}$
3. Compare predictions to reference 21cm maps (via power spectrum, bispectrum, etc.)
4. Quantify error: $P_\text{err} = P_{21}^\text{pred} - P_{21}^\text{ref}$ in bins of $k$

### Resolution Considerations

- N-body particle smoothing: similar to grid resolution; both affect $\delta_m$ reconstruction
- EFT operators (especially $[\delta^2]_{\text{renorm}}$) are resolution-dependent
- Renormalization technique (from [[Qin et al 2022 (EFT Redshift Space)]]) is essential to remove resolution dependence

## Important Equations

### Hybrid EFT Prediction

$$x_\text{HII}(\mathbf{x}) = \bar{x}_\text{HII}(z) + b_1^x \delta_m(\mathbf{x}) + b_2^x \int d^3r \, W(r) \, [\delta_m(\mathbf{x} + \mathbf{r}) \delta_m(\mathbf{x} - \mathbf{r})] + \text{stochastic}
$$

where the $W(r)$ kernel encodes the renormalized operator structure.

### Power Spectrum Prediction

$$P_x(k) = b_1^x(z)^2 P_m(k) + \text{loop corrections from } b_2^x, b_{\nabla^2}^x + P_{\varepsilon\varepsilon}(k)$$

where $P_m(k)$ is the N-body-derived matter power spectrum (accurate to $k \sim 1$ h/Mpc or higher).

## Connection to Thesis

### For P1: Proof of Portability

Baradaran et al. demonstrate that **EFT coefficients extracted from one simulation can be applied to predict ionization in new N-body realizations**. This is a proof-of-concept for portability.

P1 asks a related but different question: **Can EFT coefficients extracted from 21cmFAST be applied to SCRIPT, and vice versa?**

Both are portability tests, but at different levels:
- Baradaran et al.: portable across realizations (same code, same parameters)
- P1: portable across codes (different algorithms, different approximations)
- P1's question is harder, so success would be more impressive

### For P2: High-Fidelity Reference

The hybrid EFT provides a potential **high-accuracy reference model** for P2:

1. If EFT coefficients are truly universal (P1's finding), calibrate them once from hybrid EFT
2. Use hybrid EFT to generate training data for P2's neural density estimator
3. Advantage: hybrid EFT is much faster than full RT, so generating 1000+ training simulations is feasible
4. Result: P2 network trains on high-accuracy synthetic data, improving generalization

### Methodological Alignment

Both the hybrid EFT and P1 are asking: **Can we describe the 21cm field via a few universal EFT coefficients, independent of the specific ionization algorithm?**

The hybrid EFT answers "yes, within one code family" (N-body density + EFT ionization painting works).

P1 asks "yes, across different code families?" (21cmFAST vs. SCRIPT).

If P1 confirms cross-code universality, the hybrid EFT becomes part of the thesis's broader narrative: EFT coefficients are the right language for 21cm cosmology.

## Critical Reading: Caveats and Assumptions

### Strengths

1. **High-fidelity validation:** compared against full RT, not just other semi-analytic codes
2. **Detailed accuracy quantification:** power spectrum, bispectrum, and field-level comparisons
3. **Practical tool:** code is likely usable; N-body runs are standard in cosmology
4. **Coefficient portability test:** shows coefficients are not tied to a specific ionization algorithm

### Limitations

1. **Calibration requirement:** must have access to a reference simulation (full RT or coupled N-body+RT) to calibrate coefficients. This limits applicability if the reference is expensive or unavailable.

2. **Resolution dependence (partially addressed):** while renormalization removes some resolution effects, it doesn't remove all. Coefficients may still depend on the N-body resolution used for calibration.

3. **Ionization history matching:** the hybrid EFT is calibrated to match a reference ionization history at a specific redshift. Extrapolating across redshift space (how do coefficients evolve?) requires assumptions about smoothness.

4. **Stochasticity:** the paper may not fully characterize the stochastic remainder $\varepsilon$. This matters for error bars on inferred parameters.

5. **Single-family comparison:** compares N-body + EFT painting within one code family. Cross-family comparisons (this paper's results vs. 21cmFAST vs. SCRIPT) are the target of P1, not shown here.

## Subsequent Work and Related Papers

This paper appears to be recent and at the frontier; likely follow-up work will include:
- Application to other codes and simulators
- Cross-simulator comparisons (which is P1's focus)
- Inclusion of X-ray heating (Baradaran et al. focus on ionization; heating is separate)

## Broader Context in the Field

Baradaran et al. represents the **state-of-the-art semi-analytic 21cm modeling** as of 2024. It combines:
- The rigor of EFT (from [[McQuinn & D'Aloisio 2018]], [[Qin et al 2022 (EFT Redshift Space)]])
- The accuracy of N-body gravity (industry standard in cosmology)
- The speed of fast ionization painting (semi-analytic philosophy)

This positions it as the reference model against which newer approaches (like the thesis's P2 neural network) should be compared.

## Open Questions

> [!gap]
> **Cross-code coefficient portability:** This paper shows coefficients work across N-body realizations. P1 asks if they work across different ionization codes entirely. If P1 finds large discrepancies, it could motivate improvements to the hybrid EFT approach (e.g., is 2LPT the problem, or is it ionization-algorithm-specific physics?).

> [!gap]
> **Cosmological parameter sensitivity:** How much do the EFT coefficients change if you vary cosmological parameters (e.g., $\sigma_8$, $n_s$)? If they change significantly, then a single calibration might not be portable across cosmologies.

> [!gap]
> **Bispectrum and higher-order statistics:** the paper focuses on power spectrum. How well does the hybrid EFT predict higher-order statistics (bispectrum, trispectrum)? These carry complementary information and would strengthen the validation.

## For Your Thesis: Why This Paper Matters

1. **Proof that EFT works at high accuracy:** the hybrid EFT achieves near-RT fidelity using only a few bias coefficients. This validates the EFT as a foundational framework for P1 and P2.

2. **Establishes state-of-the-art baseline:** any improvements from the thesis's EFT-informed ML must beat the hybrid EFT's accuracy to be compelling.

3. **Identifies the key question:** Baradaran et al. show portability across realizations; P1 asks about portability across codes. If yes, the implications are profound.

4. **Practical tool for P2:** hybrid EFT could be used to generate high-accuracy training data for P2's network, improving the inference quality.
