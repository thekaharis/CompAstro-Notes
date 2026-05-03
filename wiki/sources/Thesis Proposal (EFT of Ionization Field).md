---
type: source
title: "Thesis Proposal — EFT of the Ionization Field for Simulator-Robust 21 cm Inference"
created: 2026-04-20
updated: 2026-04-20
tags:
  - source/thesis-doc
  - domain/eft
  - domain/inference
  - domain/21cm
  - foundational
status: mature
source_type: project-proposal
author:
  - "Supervisor (unnamed)"
date_published: 2026
confidence: high
key_claims:
  - "Simulator dependence should be formulated at the level of the ionization field xHII, not the composite 21cm field"
  - "The ionization field admits a long-wavelength bias expansion in the matter density (EFT) on scales larger than the bubble size"
  - "EFT coefficients {b1x, b2x, b∇²x, Pεε} provide a shared, physically interpretable, simulator-independent representation of reionization morphology"
  - "Cross-simulator ML inference should generalize better when targeting EFT parameters instead of simulator-native parameters"
  - "P1: measure and validate EFT across 21cmFAST and SCRIPT; P2: train inference pipeline using EFT coefficients as targets"
related:
  - "[[Effective Field Theory]]"
  - "[[Simulator Dependence]]"
  - "[[Bias Expansion]]"
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Qin et al 2022 (EFT Redshift Space)]]"
  - "[[Berklas & Pober 2025]]"
  - "[[Sooknunan et al 2024 (ML Reproducibility)]]"
  - "[[Zhou & La Plante 2022 (CNN Reionization)]]"
  - "[[Solt et al 2026 (Multi-Simulator Training)]]"
  - "[[py21cmfast]]"
  - "[[SCRIPT]]"
---

# Thesis Proposal — EFT of the Ionization Field

> [!key-insight]
> This is the foundational document for Haris' thesis. It frames the simulator-dependence problem as one that should be solved at the level of the **ionization field** using an EFT bias expansion, rather than at the level of the composite 21cm field or through purely empirical multi-simulator training. The EFT coefficients serve as the shared physical language across all simulators.

## Document Purpose

This is the project proposal written by the supervisor. It defines the thesis problem, motivation, theoretical framework, and two concrete work packages (P1 and P2). It is the primary reference for understanding the scope and hypotheses of the thesis.

## Problem Statement

Upcoming 21cm measurements of the Epoch of Reionization require inference pipelines trained on simulations. The core obstacle is **simulator dependence**: different reionization codes (21cmFAST, SCRIPT, zreion, GRIZZLY, THESAN, …) implement source modelling, recombinations, partial ionization, and bubble growth differently, and therefore produce different ionization morphologies even for similar global histories. Inference pipelines trained on one simulator fail on another.

Three empirical demonstrations establish the problem:

- **[[Berklas & Pober 2025]]**: MCMC-based inference (21CMMC-style) returns biased posteriors when internal 21cmFAST ionization model is varied — simulator dependence operates even within a single code.
- **[[Zhou & La Plante 2022 (CNN Reionization)]]**: CNN estimators trained on 21cmFAST fail when applied to zreion data.
- **[[Sooknunan et al 2024 (ML Reproducibility)]]**: Systematic ML reproducibility failures across simulators — networks learn code-specific features, not physical ones.

Multi-simulator training ([[Solt et al 2026 (Multi-Simulator Training)]]) helps empirically but does not provide a principled framework.

## Theoretical Framework

### Key Observation

In the saturated spin-temperature regime, the 21cm brightness temperature is:

$$\delta T_b(\mathbf{x}, z) \propto x_\text{HI}(\mathbf{x}, z)\left[1 + \delta_m(\mathbf{x}, z) - \frac{\partial_\| v_\|}{\mathcal{a}H}\right]$$

For fixed cosmology and matched initial conditions, the matter and velocity sectors are **shared across all simulators to leading order**. The dominant code-to-code freedom enters through $x_\text{HII}(\mathbf{x}, z)$.

### EFT Bias Expansion

On scales larger than the characteristic bubble size, the ionization field admits a long-wavelength bias expansion:

$$\delta_x(\mathbf{x}, z) \equiv x_\text{HII}(\mathbf{x}, z) - \bar{x}_\text{HII}(z) = b_1^x(z)\,\delta_m + \frac{b_2^x(z)}{2}\,\delta_m^2 + b_{\nabla^2}^x(z)\,\nabla^2\delta_m + \varepsilon^x(\mathbf{x}, z)$$

**Physical meaning of coefficients:**

| Coefficient | Physical Interpretation |
|---|---|
| $b_1^x$ | Linear ionization bias — how strongly ionized regions correlate with overdensity; encodes source bias |
| $b_2^x$ | Non-linear bias — sensitivity to overdensity squared; encodes non-Gaussianity |
| $b_{\nabla^2}^x$ | Higher-derivative term — encodes characteristic smoothing scale ~ bubble size |
| $P_{\varepsilon\varepsilon}$ | Stochastic power — irreducible scatter from sub-resolution physics (recombinations, source discreteness) |

Different simulators differ in **the trajectory of these coefficients** as a function of redshift/ionized fraction, not in the operator basis. This makes EFT coefficients a **shared physical language** across codes.

### Prior EFT Work

| Paper | Contribution |
|---|---|
| [[McQuinn & D'Aloisio 2018]] | Introduced perturbative bias expansion for 21cm; validated against 3 RT sims |
| [[Qin et al 2022 (EFT Redshift Space)]] | Extended to redshift space; validated on THESAN; k ≲ 0.8 h/Mpc |
| [[Sailer et al 2022 (Optical Depth EFT)]] | Forecasted τ constraints using perturbative 21cm + CMB lensing |
| [[Baradaran et al 2024 (Hybrid EFT)]] | Hybrid EFT: N-body density + EFT ionization painting; best accuracy |

## Proposed Work

### P1: EFT Characterisation Across Simulation Codes

**Objective:** Measure and validate the EFT of the ionization field across multiple simulation codes, determine its regime of validity, and quantify what simulator variation looks like in EFT space.

**Codes:** Primarily **21cmFAST** and **SCRIPT**. Possibly additional codes.

**Key questions:**
- Does the ionization field admit a stable EFT description across codes (i.e., do the EFT coefficients converge at large scales)?
- Where does the EFT break down (bubble scale, partial ionization, …)?
- Does simulator variation produce structured differences in EFT coefficient trajectories, and are those differences interpretable?

### P2: EFT-Informed Cross-Simulator Inference

**Objective:** Test whether inference targeted at ionization-field EFT coefficients generalises better across simulators than existing approaches (native parameters, compressed summaries), and demonstrate an end-to-end route from 21cm data to astrophysical constraints through EFT space.

**Central hypothesis:** If the EFT description is accurate, training an ML estimator to infer EFT coefficients (rather than simulator-native parameters) should produce an estimator that generalises to other simulators, because the EFT coefficients are the same physical quantities regardless of which code generated the data.

## Central Hypothesis

> EFT coefficients of the ionization field provide the correct shared representation for simulator-robust 21cm inference. Cross-simulator generalisation improves when models are trained to infer EFT parameters rather than simulator-native parameters or overly compressed summaries.

## References in Proposal

The proposal explicitly cites: Berklas & Pober 2025 (`arXiv:2511.13854`), McQuinn & D'Aloisio 2018 (`arXiv:1806.08372`), Baradaran et al. 2024 (`arXiv:2406.13079`), Qin et al. 2022 (`arXiv:2205.06270`), Sailer et al. 2022 (`arXiv:2205.11504`), Solt et al. 2026 (`arXiv:2601.05229`), Sooknunan et al. 2024 (`arXiv:2412.15893`), Zhou & La Plante 2022 (PASP 134, 044001).
