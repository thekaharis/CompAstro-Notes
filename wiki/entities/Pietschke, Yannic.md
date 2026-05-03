---
type: entity
title: "Pietschke, Yannic"
created: 2026-04-14
updated: 2026-04-16
tags:
  - entity/person
status: seed
entity_type: person
role: "PhD student, Heidelberg; EoRFlow lead developer"
first_mentioned: "[[Pietschke et al 2025 (EoRFlow)]]"
related:
  - "[[EoRFlow]]"
  - "[[Heneka, Caroline]]"
  - "[[Inference and ML]]"
---

# Pietschke, Yannic

## Role and Affiliation

PhD student at Institut für Theoretische Physik, Universität Heidelberg, Germany, and Institute for Astronomy, University of Vienna, Austria. Working in the research group of Caroline Heneka on simulation-based inference for 21cm cosmology. Lead developer of EoRFlow, a neural density estimation framework for Bayesian inference from 21cm observations.

## Academic Background and Research Focus

Pietschke is pursuing PhD research on machine learning for 21cm cosmology, with emphasis on simulation-based inference (SBI), neural posterior estimation, and the exploitation of higher-dimensional observables (like 2D power spectra) in 21cm analysis. His work combines expertise in both cosmological simulations and modern machine learning methods.

## Research Contributions: EoRFlow Framework

**EoRFlow (2025):** Pietschke is the first author on the EoRFlow paper, which introduces a simulation-based inference framework for 21cm observations. EoRFlow represents a significant methodological advance and is the direct predecessor to P2.

**Core Framework:** EoRFlow uses neural density estimation (via normalizing flows) to learn the posterior distribution of reionization parameters given 21cm observations. The framework:

1. **Uses 21cmFAST Simulations as Training Data:** Rather than using a pre-computed likelihood function (intractable for the 21cm forward model), EoRFlow trains on a large set of 21cmFAST simulations with varying parameters. This simulation ensemble becomes the training dataset.

2. **Neural Density Estimator:** A normalizing flow network is trained to map from 21cm observations to the posterior distribution of parameters. Flows are particularly well-suited to this task because they provide both:
   - Accurate posterior estimates (unlike simpler variational methods)
   - Fast sampling from the posterior (enabling downstream analysis)

3. **Targets Reionization Parameters:** EoRFlow infers reionization parameters including:
   - x_HI(z): ionization history
   - T_K(z): kinetic temperature history
   - Astrophysical parameters driving reionization (e.g., stellar mass fraction f_*, ionizing photon efficiency ξ_ion)

4. **Uses 2D Power Spectrum (2DPS):** Importantly, EoRFlow uses the 2D power spectrum (power as function of parallel and perpendicular wavenumber) rather than the 1D power spectrum. This retains more information, distinguishes between density and velocity effects, and provides better constraints on redshift-evolution parameters like z_reion.

5. **Accounts for Observational Effects:** The framework includes modeling of observational effects like foreground contamination, instrumental noise, and resolution limitations.

**Validation Against Classical Methods:** The EoRFlow paper includes detailed comparisons with classical MCMC approaches, demonstrating that the neural posterior estimates are accurate and not substantially biased relative to Bayesian ground truth.

## Extensions: Cross-Correlation Analysis

**Extended Framework for Cross-Power (2026):** Pietschke is the first author on a follow-up paper extending EoRFlow from 21cm auto-power to 21cm-galaxy cross-power measurements. This extension:

1. **Multi-Probe Analysis:** Jointly uses 21cm and galaxy surveys to extract more information than 21cm alone
2. **Shared Latent Structure:** Recognizes that both probes trace the same underlying reionization history (x_HI(z)) but with different biases and sensitivities
3. **Synergistic Constraints:** Combines observations to break degeneracies and achieve tighter parameter constraints

This extension demonstrates the flexibility of the SBI framework and suggests future directions for related work (including P2).

## Research Style and Approach

Pietschke's approach is characterized by:

- **Methodological sophistication:** Careful attention to neural network design, loss functions, training procedures, and regularization
- **Empirical validation:** Extensive testing against classical methods to ensure reliability
- **Observable-focused:** Emphasis on using realistic, information-rich observables (2DPS rather than 1DPS)
- **Physics-informed architecture:** Network designs informed by cosmological considerations (e.g., handling hierarchical redshift structure)
- **Systematic extension:** Building from single-probe (EoRFlow auto-power) to multi-probe (cross-power) analyses

## Key Contributions

**EoRFlow Framework (2025):** The primary contribution. EoRFlow established neural density estimation with normalizing flows as a viable approach to high-dimensional Bayesian inference in 21cm cosmology. This is a methodologically important paper that has influenced subsequent work.

**Use of 2D Power Spectrum:** Pietschke's emphasis on the 2D power spectrum (rather than 1D) as the primary observable is significant. The 2D power spectrum contains more information and distinguishes different physical effects (reionization, density fluctuations, velocity effects). This choice cascades through the EFT-based P2 work.

**Multi-Probe Extension (2026):** Demonstrating that SBI generalizes to cross-correlation analysis expands the scope of what simulation-based inference can address. This shows the framework's flexibility.

**Detailed Validation and Comparison:** Pietschke's papers include thorough validation against classical methods, demonstrating care and scientific rigor in methodology.

## Relevance to This Thesis

Pietschke's work is absolutely foundational to this thesis:

1. **EoRFlow as Direct Predecessor:** P2 is explicitly framed as building on EoRFlow. Understanding exactly what EoRFlow does, how it works, what its strengths are, and what its limitations are is essential for designing P2 as a proper extension.

2. **Same Inference Framework:** Both EoRFlow and P2 use neural density estimation via normalizing flows for posterior approximation. This means the core inference methodology—training data generation, network architecture, loss functions, validation procedures—is shared. Understanding EoRFlow's choices is directly applicable to P2.

3. **2D Power Spectrum as Observable:** EoRFlow's use of 2D power spectrum is inherited by P2. If P2 aims to infer EFT coefficients from 2D power spectra (rather than just x_HI(z) parameters), the observable definition comes directly from Pietschke's work.

4. **From Parameters to EFT Coefficients:** The key extension in P2 is a shift from inferring reionization parameters (x_HI(z), T_K(z), f_*, ξ_ion) to inferring effective field theory coefficients. This builds on EoRFlow's framework but changes what the network outputs:
   - **EoRFlow:** Maps 2DPS → (x_HI(z), T_K(z), f_*, ξ_ion)
   - **P2:** Maps 2DPS → (EFT coefficients)

   This requires understanding what EoRFlow does in detail to properly design the extension.

5. **Validation Methodology:** The careful validation approach Pietschke uses—comparing to MCMC, testing on held-out data, characterizing systematic biases—provides a template for how P2 should be validated. Any claims about P2's performance must be backed by similar rigor.

6. **Observable-Forward Thinking:** Pietschke's emphasis on the 2D power spectrum and later extension to cross-power demonstrates that the observables matter. P2 must similarly think carefully about what observables to target and what information they contain about EFT parameters.

7. **Published Precedent:** EoRFlow provides a published precedent for using neural density estimation in 21cm inference, which lowers the bar for subsequent papers (like P2) using similar methods. This is valuable for positioning within the literature.

## Connections and Collaborations

Pietschke is embedded in Heneka's research group at Heidelberg, with additional affiliation at the University of Vienna. His connections include:

- **Caroline Heneka** — PhD advisor and group leader
- **Ayodele Ore** — Fellow student in the group; lead developer of SKATR
- **Other members of Heneka's group** — Collaborating on multi-probe analyses and related projects
- **Potential Vienna-based collaborators** — Through his Institute for Astronomy affiliation

The group structure ensures that Pietschke's work on EoRFlow is developed in dialogue with other approaches (SKATR, multi-probe extensions).

## Papers / Work

| Title | Year | Relevance |
|-------|------|-----------|
| [[Pietschke et al 2025 (EoRFlow)]] | 2025 | First author; EoRFlow SBI framework using normalizing flows; targets x_HI(z), T_K(z), and astrophysical parameters; uses 2D power spectrum; direct predecessor to P2 |
| [[Pietschke et al 2026 (cross-correlation)]] | 2026 | First author; extension of EoRFlow to 21cm-galaxy cross-power; demonstrates multi-probe SBI |

## Notes

Pietschke represents the modern simulation-based inference approach to 21cm cosmology. His EoRFlow framework has established normalizing flows and neural density estimation as viable tools for high-dimensional Bayesian inference in reionization science. For a thesis developing P2—an EFT-based extension of EoRFlow—understanding Pietschke's work in detail is non-negotiable: EoRFlow is the foundation, and P2 builds directly on it. The success of P2 will depend fundamentally on leveraging the methodological innovations and validation approaches that Pietschke pioneered in EoRFlow.
