---
type: source
title: "Worku, Cruz & Kamionkowski 2026 — Primordial Magnetic Fields at Cosmic Dawn: 21-cm Forecasts with HERA and SKA"
created: 2026-05-12
updated: 2026-05-12
tags:
  - source/paper
  - domain/21cm
  - domain/reionization
  - forecast
  - new-physics
status: seed
source_type: paper
author:
  - "Worku, Keduse"
  - "Cruz, Hector Afonso G."
  - "Kamionkowski, Marc"
date_published: 2026
url: "https://arxiv.org/abs/2605.05323"
confidence: medium
key_claims:
  - "Primordial magnetic fields (PMFs) enhance low-mass halo abundance at Cosmic Dawn by sourcing additional small-scale matter power"
  - "Enhanced small-scale power accelerates early galaxy formation, shifts Lyman-alpha coupling, X-ray heating, and reionization to earlier times"
  - "PMFs leave correlated signatures on global and fluctuating 21cm signals; the analytic framework zeus21 is extended to include a physically motivated PMF contribution to the linear matter power spectrum"
  - "Forecasts produced for HERA and SKA assuming the extended zeus21 forward model"
related:
  - "[[21cm Cosmology]]"
  - "[[Reionization Physics]]"
  - "[[HERA]]"
  - "[[SKA]]"
  - "[[Matter Overdensity Field]]"
---

# Worku, Cruz & Kamionkowski 2026 — PMFs at Cosmic Dawn: 21-cm Forecasts with HERA and SKA

> [!key-insight]
> Extends the analytic `zeus21` framework to include a physically motivated primordial-magnetic-field (PMF) contribution to the linear matter power spectrum, including radiative damping before recombination. Propagates the boosted small-scale power through to global and fluctuating 21 cm observables and produces forecast sensitivity for HERA and SKA.

## Citation

Worku, K., Cruz, H. A. G., & Kamionkowski, M. (2026). "Primordial Magnetic Fields at Cosmic Dawn: 21-cm Forecasts with HERA and SKA." arXiv:2605.05323.

## Core Claim

Primordial magnetic fields modify the matter power spectrum on small scales by sourcing extra fluctuations that survive radiative damping prior to recombination. The extra small-scale power increases the abundance of low-mass halos at Cosmic Dawn, which accelerates:

- Lyman-$\alpha$ coupling (earlier WF coupling onset)
- X-ray heating of the IGM
- The onset and duration of reionization

These shifts imprint correlated signatures on the global 21 cm signal and the 21 cm power spectrum. The authors build the PMF contribution into the analytic `zeus21` forward model and produce HERA/SKA forecasts.

## Why It Matters for This Thesis

This paper is a methods-adjacent contribution rather than a competitor to the thesis. Three reasons it is worth filing:

1. **Forward-model layer**. The thesis's P2 will need a fast forward model for inference; `zeus21` is one of the analytic options (alongside 21cmFAST and the FNO surrogate plan in [[FNO Approach for 21cm Emulation]]). Worku et al. extend `zeus21`'s linear matter power spectrum input — a clean example of how new-physics priors get attached to the front of an EoR forward model. The same modular plug-in style works for EFT-coefficient priors or alternative initial-condition models.

2. **What an EFT description does **not** absorb**. A modification of $P_\text{lin}(k)$ at small scales is exactly the kind of input the EFT bias expansion takes as given — the EFT coefficients are defined relative to whatever linear matter field is fed in. So Worku et al.'s PMF scenario does not invalidate the EFT framework; it just relabels the input. Useful framing for P2's discussion of what the EFT representation is and is not robust to.

3. **HERA / SKA forecast realism**. Provides recent forecast assumptions (noise model, observation time, foreground treatment) that can be reused for P2's inference forecasting if needed.

## Connections

- Forward-model plug-in style $\leftrightarrow$ [[Effective Field Theory]] input-power-spectrum interface
- HERA/SKA forecast assumptions $\leftrightarrow$ [[FNO Approach for 21cm Emulation]] downstream observation operator
- Small-scale power enhancement $\leftrightarrow$ [[Matter Overdensity Field]] (linear vs nonlinear)

## Open Questions

> [!gap]
> Do EFT coefficients extracted in a PMF-modified $P_\text{lin}(k)$ universe transfer back to the standard $\Lambda$CDM EFT coefficients with just a shift in the input power spectrum, or do they pick up genuinely new operators? Likely the former, but worth confirming as part of P1's renormalization sanity checks.

## Citation Stub

```
Worku, K., Cruz, H. A. G., Kamionkowski, M. "Primordial Magnetic Fields at Cosmic Dawn: 21-cm Forecasts with HERA and SKA." arXiv:2605.05323 (2026).
```
