---
type: overview
title: "Thesis Wiki Overview"
created: 2026-04-14
updated: 2026-04-15
tags:
  - meta
status: developing
---

# Thesis Wiki Overview

## What This Wiki Is About

This wiki tracks research for a Master's thesis in Computational Astrophysics on **EFT-based simulator-robust 21 cm reionization inference**. The central problem: upcoming 21 cm telescopes (HERA, SKA) will require inference pipelines trained on simulations, but different simulation codes produce different results even for matched physics — a systematic called *simulator dependence*. The thesis proposes using the Effective Field Theory (EFT) of the ionization field as a shared, physically interpretable representation that is common to all simulators by construction.

## The Two-Part Research Plan

**P1 — EFT Characterization:** Measure the bias coefficients $\{b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon}\}$ of the ionization field $x_\text{HII}$ across multiple simulation codes (starting with 21cmFAST, then SCRIPT or SimFast21) with matched cosmologies and initial conditions. Validate the EFT description and map its regime of validity.

**P2 — Cross-Simulator Inference:** Train inference models to target EFT coefficients rather than native simulator parameters. Test whether this improves generalization across simulators compared to current approaches.

## The Core Theoretical Claim

In the saturated spin-temperature limit, the 21 cm brightness temperature satisfies $\delta T_b \propto x_\text{HI} \cdot (\text{gravitational terms})$. Gravity is shared across simulators; code-to-code differences live entirely in $x_\text{HII}$. The ionization field admits a long-wavelength bias expansion:

$$
\delta_x(\mathbf{x}, z) = b_1^x\,\delta_m + \frac{b_2^x}{2}\,\delta_m^2 + b_{\nabla^2}^x\,\nabla^2\delta_m + \varepsilon^x
$$

The EFT coefficients encode the simulator-specific physics in a compact, interpretable form. Different simulators map to different coefficient *trajectories* over redshift, not different operator bases.

## Key Foundational Papers

### EFT Theory
- [[McQuinn & D'Aloisio 2018]] — Original perturbative bias expansion for the 21 cm field; Minimal Model
- [[Qin et al 2022 (EFT Redshift Space)]] — Extension to redshift space with renormalization; THESAN validation
- [[Sailer et al 2022 (Optical Depth EFT)]] — Forecasting $\tau$ using the EFT framework; observational use case
- [[Baradaran et al 2024 (Hybrid EFT)]] — Hybrid EFT with N-body accuracy; most accurate semi-analytic model

### Simulator Dependence Evidence Chain
- [[Zhou & La Plante 2022 (CNN Reionization)]] — CNN failure cross-code (21cmFAST → zreion); canonical demonstration
- [[Berklas & Pober 2025]] — Within-code model dependence in MCMC inference; problem is intra-code too
- [[Sooknunan et al 2024 (ML Reproducibility)]] — Systematic ML survey; all architectures fail; features are code-specific

### Current State of the Art (Mitigation)
- [[Solt et al 2026 (Multi-Simulator Training)]] — Multi-simulator training; empirical baseline for P2 to beat

## Background Reading (Ingested)

Four pedagogical reviews providing the physical foundation for the thesis:

- [[Choudhury 2022 (Reionization Intro)]] — Derives the photon budget and global reionization equation from first principles; defines the parameters ($\zeta$, $T_\text{vir}$, $R_\text{mfp}$, $f_\text{esc}$) that appear throughout the thesis
- [[Ferrara & Pandolfi (IGM Reionization)]] — IGM physics, Lyman-alpha forest, Gunn-Peterson effect; grounds observational constraints on $\bar{x}_\text{HI}(z)$
- [[Trac & Gnedin 2009 (Reionization Simulations)]] — RT algorithm taxonomy (moments/MC/ray-tracing); convergence across codes; why galaxies dominate reionization
- [[Gnedin & Madau 2022 (Modeling Reionization)]] — Complete map of the simulation landscape; 21cmFAST sec. 6.1.1; defines semi-numerical vs. DMO+SAM vs. fully coupled RT

## Key Simulation Codes

- [[21cmFAST]] — Primary code; semi-numerical, fast, group's main tool
- [[SCRIPT]] — Semi-numerical, public, most tractable second code for comparison
- [[THESAN]] — Full radiative transfer suite; Qin et al. 2022 validated against this
- [[SimFast21]], [[GRIZZLY]], [[zreion]] — Additional codes in the field

## Domains

- [[21cm Cosmology]] — Signal physics, observational context
- [[Reionization Physics]] — EoR history, ionization morphology
- [[Effective Field Theory]] — The theoretical framework
- [[Simulation and Codes]] — Code survey and comparison
- [[Inference and ML]] — Inference methodology
- [[Thesis Work]] — Working notes, timeline, deliverables
