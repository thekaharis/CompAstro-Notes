---
type: entity
title: "Heneka, Caroline"
created: 2026-04-14
updated: 2026-04-16
tags:
  - entity/person
status: seed
entity_type: person
role: "Computational cosmologist; 21cm ML and SBI; Heidelberg"
first_mentioned: "[[Ore et al 2025 (SKATR)]]"
related:
  - "[[EoRFlow]]"
  - "[[SKATR]]"
  - "[[Inference and ML]]"
---

# Heneka, Caroline

## Role and Affiliation

Computational cosmologist at Institut für Theoretische Physik, Universität Heidelberg, Germany. Principal investigator leading the Heidelberg 21cm Machine Learning group, a research program focused on applying modern machine learning techniques—particularly simulation-based inference (SBI)—to 21cm cosmology and the epoch of reionization.

## Academic Background and Career

Heneka received her PhD in theoretical physics/cosmology and has since established herself as a leading figure in the emerging intersection of machine learning and 21cm science. Her career has been marked by a strategic focus on applying recent advances in simulation-based inference, neural networks, and deep learning to problems in reionization cosmology where traditional likelihood-based inference approaches face computational challenges.

She currently leads a research group at Heidelberg that trains students (including PhD students Yannic Pietschke and Ayodele Ore) in these cutting-edge methods. Her group's publications reflect rapid iteration and innovation, with multiple major papers in 2025-2026 introducing new frameworks and applications.

## Research Focus and Methodology

**Simulation-Based Inference (SBI) for 21cm:** Heneka's group pioneered the application of modern SBI techniques to 21cm cosmology. SBI methods bypass the need to compute explicit likelihood functions (which is intractable for complex forward models like 21cm simulations) by training neural networks to map from observations to parameters, using simulations as training data. This is a powerful approach when the forward model is fast to simulate but slow/impossible to evaluate in likelihood space.

**Neural Network Architectures for Cosmological Data:** Her group has explored various neural network architectures appropriate for 21cm data:
- Autoencoders for data compression
- Vision Transformers (ViTs) for capturing spatial structure in 21cm maps
- Normalizing flows for posterior characterization
- Convolutional networks for power spectrum estimation

**Cross-Simulator Generalization:** One of the most important challenges in 21cm cosmology is that different simulation codes (21cmFAST, ARES, CROC, etc.) produce different ionization field statistics for the same input parameters. This "simulator dependence" problem is a major source of systematic uncertainty. Heneka's group has tackled this directly:
- EoRFlow uses machine learning to map from one simulator (21cmFAST) to observables
- SKATR (developed by her student Ore) uses self-supervised learning to learn simulator-independent representations

**Multi-Probe and Cross-Correlation Analyses:** Beyond 21cm alone, her group has extended to multi-probe analyses combining 21cm with galaxy surveys and other cosmological probes. This includes 21cm-galaxy cross-power analyses that exploit correlations between different tracers of structure.

**Theoretical Understanding Alongside ML:** Importantly, Heneka's group does not treat machine learning as a black box. There is ongoing effort to understand what the neural networks learn, to connect ML architectures to the physics they capture, and to ensure interpretability.

## Research Style and Approach

Heneka's approach is characterized by:
- **Methodological rigor:** Careful validation of ML methods, study of systematic uncertainties, and comparisons to classical approaches
- **Physics-informed design:** Neural network architectures are chosen with cosmological physics in mind (e.g., using Vision Transformers to capture spatial structure meaningful in cosmology)
- **Multi-tool philosophy:** Using both classical cosmological methods and modern ML, rather than viewing them as competitors
- **Training-intensive focus:** Emphasis on careful data generation, training procedures, and regularization to ensure ML models generalize beyond training data
- **Collaborative approach:** Working closely with students and across research groups to validate methods

## Key Contributions to the Field

**EoRFlow Framework (2025):** Developed by her student Pietschke, EoRFlow was introduced by Heneka's group as a simulation-based inference framework for 21cm power spectra. It uses neural density estimators to map from 21cm observations to reionization parameters (x_HI(z), T_K(z), and astrophysical parameters like stellar mass fraction and ionizing photon efficiency). EoRFlow is now the primary tool being extended by P2.

**SKATR Framework (2025):** Developed by her student Ore, SKATR introduces a self-supervised Vision Transformer approach to 21cm inference. Rather than using labeled simulations, SKATR learns invariant representations by contrasting data from different simulators. This provides an alternative to explicit EFT-based cross-simulator translation.

**Cross-Correlation Extension (2026):** Her group has extended SBI methods from auto-power to cross-power between 21cm and galaxy surveys, enabling joint constraints from multiple observables.

**SKA-CMB SBI (2025):** In collaboration (e.g., Schosser et al.), her group has applied SBI to joint SKA-CMB analyses, exploring synergies between 21cm and CMB observations for inflation parameter constraints.

**Method Validation and Benchmarking:** A consistent theme in Heneka's publications is careful validation: comparing ML-based inference to classical MCMC approaches, studying how performance scales with data quality, and characterizing systematic biases in predictions.

## Relevance to This Thesis

Heneka's work is critically important for understanding the thesis's context and positioning:

1. **SBI as the Inference Framework:** EoRFlow and subsequent extensions (including P2) use SBI as the core inference approach. Understanding Heneka's group's methodological choices—why certain architectures, how to validate SBI, what pitfalls to avoid—is essential for building on their foundation.

2. **EoRFlow as Direct Predecessor:** The thesis's P2 aims to extend EoRFlow from inferring x_HI(z) to inferring EFT coefficients. Understanding exactly what EoRFlow does, how it works, what its strengths are, and what its limitations are is essential for designing P2 as a proper extension.

3. **Cross-Simulator Problem as Motivation:** Heneka's group's work on SKATR highlights the cross-simulator generalization challenge that motivates the EFT approach. By developing an EFT framework that explicitly parameterizes simulator differences, P2 aims to address the same problem as SKATR, but from a more physically-grounded, interpretable angle.

4. **Validation Methodology:** The way Heneka's group validates ML methods—comparing to MCMC, testing on held-out simulations, characterizing systematics—provides a template for how P2 should be validated. An EFT-based inference framework must be validated as thoroughly as any ML-based method.

5. **Network Architecture Choices:** The choices Heneka's group made in EoRFlow (autoencoders, particular loss functions, training procedures) inform what design decisions might be appropriate for P2.

6. **Multi-Probe Thinking:** The extension of her group's methods from 21cm-only to multi-probe analyses (21cm-galaxy cross-power) suggests future directions for EFT-based inference: can an EFT framework simultaneously infer parameters from multiple observables?

7. **Direct Collaboration Potential:** Heneka's group's presence in the wiki (appearing on 4 papers) and the overlap in research questions suggests possible collaboration or at minimum deep engagement with their methods.

## Connections and Collaborations

Heneka leads the Heidelberg 21cm ML group at one of Germany's major universities. Her network includes:

- **Her own group:** PhD students Yannic Pietschke and Ayodele Ore, who are lead developers of EoRFlow and SKATR respectively
- **Broader collaborations:** As evidenced by the 4 papers she appears on (EoRFlow, SKATR, cross-correlation, Starobinsky papers)
- **International network:** Collaborations with groups working on SBI, cosmological inference, and 21cm science across Europe and beyond
- **Potential connection to thesis supervisor:** The fact that her group appears so prominently in the thesis wiki suggests possible connection to the advisor

## Papers / Work

| Title | Year | Relevance |
|-------|------|-----------|
| [[Pietschke et al 2025 (EoRFlow)]] | 2025 | EoRFlow SBI framework; co-author; direct predecessor to P2 |
| [[Pietschke et al 2026 (cross-correlation)]] | 2026 | Extension of SBI to 21cm-galaxy cross-power; co-author |
| [[Ore et al 2025 (SKATR)]] | 2025 | SKATR self-supervised transformer approach; co-author; alternative solution to cross-simulator problem |
| [[Schosser et al 2025 (Starobinsky)]] | 2025 | SKA-CMB joint SBI for inflation; co-author; demonstrates SBI beyond reionization-only analysis |

## Notes

Heneka represents the modern computational and machine learning tradition in 21cm cosmology. Her group's work has established simulation-based inference as a viable and powerful approach to high-dimensional inference problems in reionization science. For a thesis building on EoRFlow to develop an EFT-based inference framework, understanding Heneka's foundational contributions is essential: the methods, validation approaches, and architectural choices she pioneered form the immediate foundation upon which P2 is built.
