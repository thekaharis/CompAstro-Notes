---
type: meta
title: "Planning Index"
created: 2026-04-21
updated: 2026-07-16
tags:
  - domain/thesis
  - domain/planning
---

# Thesis Planning

Detailed, step-by-step operational plans for each work package. These documents go beyond the high-level roadmap in [[Thesis Work]] and focus on the exact computations, code patterns, sanity checks, and decision points at each stage.

## Documents

- [[P1 EFT Characterization]] — Matched ICs → perturbative basis → coefficient extraction → stochastic analysis → regime mapping → interpretation
- [[P2 Cross-Simulator Inference]] — Training set design → mapping → swyft setup → cross-simulator test → baseline comparison
- [[FNO Approach for 21cm Emulation]] — Neural-operator strategy for the density-to-ionization and brightness-temperature maps
- [[21cmFAST → FNO Pipeline]] — Data-transfer, training, checkpoint, and prediction pipeline
- [[Siren3D Residual Refinement Plan]] — Coordinate-conditioned residual refinement of U-FNO bubble boundaries, with controls and stop criteria
- [[Windowed Local-FNO U-Net Plan]] — Windowed spectral mixing (overlapping Hann patches, shifted grids) + global Fourier bottleneck; localizes the transform to buy high effective frequencies
- [[Smooth-Target Reparametrization Plan]] — Learn a smooth surrogate ($z_\text{re}$, signed distance) instead of $x_\text{HI}$; reconstruct by deterministic thresholding so uncertainty displaces fronts rather than blurring them
- [[Lightcone z_re Map Target]] — Implementation of the smooth-target plan's candidate 1: per-pixel $z_\text{re}(x,y)$ fitted from the lightcone (Gompertz/step LS), 2-D FNO with mask handling; reconstruction sanity checks done, training pending
- [[Warped LOS Grid Plan]] — Non-uniform LOS cache grid (density ∝ ensemble-mean $|dx_\text{HI}/d\chi|$, CDF-inverted): the uniform-z cache is ~37 Mpc at low z where fronts live; round-trip evaluation tool + volume-weighted loss merged, real-data run pending

## Reading Order

Read [[P1 EFT Characterization]] first — P2 depends on the P1 pipeline and its outputs. Each document is self-contained but cross-references the other.

## How These Relate to Other Wiki Pages

- Physics background: [[Effective Field Theory]], [[Reionization Physics]], [[Simulation and Codes]]
- Foundational paper for P1 methodology: [[McQuinn & D'Aloisio 2018]]
- Foundational paper for P2 methodology: [[Pietschke et al 2025 (EoRFlow)]], [[Ore et al 2025 (SKATR)]]
- High-level timeline and deliverables: [[Thesis Work]]
