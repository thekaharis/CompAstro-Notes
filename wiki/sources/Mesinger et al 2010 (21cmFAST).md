---
type: source
title: "Mesinger, Furlanetto & Cen 2010 — 21cmFAST"
created: 2026-04-20
updated: 2026-04-20
tags:
  - source/paper
  - domain/simulation
  - domain/21cm
  - foundational
status: mature
source_type: paper
author:
  - "[[Mesinger, Andrei]]"
  - "[[Furlanetto, Steven R.]]"
  - "Cen, Renyue"
date_published: 2010
url: "https://arxiv.org/abs/1003.3878"
confidence: high
key_claims:
  - "21cmFAST generates full 3D realizations of density, ionization, velocity, and spin temperature fields using approximate semi-numerical methods"
  - "Power spectra agree with state-of-the-art hydrodynamic simulations to within 10s of percent down to the Nyquist frequency"
  - "A single redshift realization on a 1 Gpc box runs in minutes on a single processor vs. three days on a 1536-node cluster for full RT"
  - "Ionization field computed using the FFRT (filtered/friend-of-friend-like) excursion-set algorithm on the evolved density field"
  - "Spin temperature field computed self-consistently from the Wouthuysen-Field coupling and X-ray heating"
related:
  - "[[py21cmfast]]"
  - "[[Simulation and Codes]]"
  - "[[Excursion Set Formalism]]"
  - "[[Spin Temperature]]"
  - "[[Brightness Temperature]]"
  - "[[Mesinger 2016]]"
  - "[[Gnedin & Madau 2022 (Modeling Reionization)]]"
---

# Mesinger, Furlanetto & Cen 2010 — 21cmFAST

> [!key-insight]
> This is the original 21cmFAST paper. It establishes the code's semi-numerical approach: use the Zel'dovich approximation for density evolution and the excursion-set formalism for ionization, bypassing expensive radiative transfer. The speed-accuracy trade-off (~10% power spectrum error vs. many orders of magnitude faster) is the foundation on which all subsequent 21cmFAST-based inference work rests.

## Citation

Mesinger, A., Furlanetto, S., & Cen, R. (2010). "21cmFAST: A Fast, Semi-Numerical Simulation of the High-Redshift 21-cm Signal." *MNRAS*, arXiv:1003.3878.

## Context

This paper was the primary reference code for 21cm signal simulation throughout the 2010s and into the 2020s. The modern version of the code (py21cmFAST, now 21cmFAST v4+) is built on these foundations. It is the primary simulation tool for thesis work (P1 and P2).

## Core Method

### Density Field
- Initial conditions generated in Lagrangian space, evolved using **first-order perturbation theory (Zel'dovich approximation)**
- No separate baryonic treatment; dark matter and gas approximated together
- Accurate at large scales (k ≲ 0.5 h/Mpc at z ~ 7), where MWA/LOFAR/SKA are sensitive
- Fast: ~10 minutes for a 768³ realization at z = 7 on a single CPU

### Ionization Field (FFRT Algorithm)
- Uses a semi-numerical adaptation of the **excursion-set formalism** applied to the evolved density field
- A cell is flagged as ionized if the cumulative photon count within a spherical filter of radius $R_\text{mfp}$ exceeds the recombination requirement
- Iterates over decreasing filter scales — finds largest ionized regions first, producing inside-out reionization topology
- Bypasses halo-finding (unlike predecessor DexM), gaining speed at the cost of some morphological detail

### Spin Temperature Field
- Introduced in this paper as a new feature (earlier DexM only did post-heating limit)
- Computes Wouthuysen-Field coupling from Ly-α flux and X-ray heating self-consistently
- Key parameters: X-ray efficiency ($\zeta_X$), Ly-α efficiency, minimum virial temperature

### Brightness Temperature
$$\delta T_b(\mathbf{x},z) \approx 27 x_\text{HI}(1+\delta_\text{nl})\left(1 - \frac{T_\gamma}{T_S}\right)\left(\frac{H}{dv_r/dr + H}\right)\left[\frac{1+z}{10}\cdot\frac{0.15}{\Omega_m h^2}\right]^{1/2}\frac{\Omega_b h^2}{0.023}\ \text{mK}$$

## Key Results

- **Density field**: Power spectra from 21cmFAST agree with hydrodynamic simulations (Trac et al. 2008) to within 10s of percent at k ≲ 0.5 h/Mpc; percent-level agreement at large scales across all redshifts z = 7–20
- **Ionization field**: Inside-out reionization topology reproduced; bubble size distribution agrees well at large bubble scales; differences on small scales where resolution matters
- **Peculiar velocity gradient**: Good agreement with simulations; RSD captured at the 10% level
- **Full 21cm brightness temperature**: Power spectrum agrees to within tens of percent; large-scale features (EoR morphology, timing) well reproduced

## Parameters (Original 2010 Version)

The main astrophysical knobs in the original code:

| Parameter | Symbol | Role |
|---|---|---|
| Ionization efficiency | $\zeta$ | Number of ionizing photons per baryon in collapsed structure |
| Virial temperature threshold | $T_\text{vir}$ | Minimum halo mass for star formation |
| Mean free path | $R_\text{mfp}$ | Photon horizon in ionized IGM; controls recombination sinks |
| X-ray efficiency | $\zeta_X$ | X-ray heating rate; sets spin temperature |
| Ly-α efficiency | $\zeta_\alpha$ | Wouthuysen-Field coupling efficiency |

## Why This Paper Matters for the Thesis

1. **Primary simulation code**: P1 uses 21cmFAST (alongside SCRIPT) to measure EFT coefficients. Understanding the native parameters and algorithm is essential for interpreting coefficient differences between codes.

2. **The native-parameter problem**: 21cmFAST's native parameters ($\zeta$, $T_\text{vir}$, $R_\text{mfp}$) are defined within this algorithm. They are not physical observables — different algorithms map the same physics onto different parameter values. This is the core problem that [[Berklas & Pober 2025]] demonstrates and the thesis proposes to solve.

3. **Excursion-set ionization as EFT target**: The FFRT excursion-set algorithm generates large-scale ionization structure that, by construction, is determined by the large-scale density field filtered at bubble scale. This is exactly the regime where the EFT bias expansion should be valid (scales larger than bubble size). The paper implicitly motivates why the EFT works for 21cmFAST outputs.

4. **Historical baseline**: The ~10% power spectrum agreement with full RT at relevant scales (k ≲ 0.5 h/Mpc) sets the accuracy floor for EFT coefficient extraction. If the EFT has ~5–10% residuals, they are comparable to the code's own approximation errors.

## Open Questions Relative to Thesis

> [!gap]
> **Version gap**: The 2010 paper describes the original C-based code. Current thesis work uses py21cmFAST (v4.1.1), which adds Halo Finder integration, updated astrophysics prescriptions (PopII/PopIII, inhomogeneous recombinations), and Python wrappers. How much do EFT coefficients vary between v1 prescriptions and modern v4 prescriptions?

> [!gap]
> **FFRT vs. SCRIPT topology**: The FFRT excursion-set algorithm and SCRIPT's algorithm produce different bubble morphologies. P1 will directly test whether this topology difference manifests as a difference in EFT coefficients or is absorbed into $b_{\nabla^2}^x$ and $P_{\varepsilon\varepsilon}$.
