---
type: entity
title: "Ore, Ayodele"
created: 2026-04-14
updated: 2026-04-16
tags:
  - entity/person
status: seed
entity_type: person
role: "PhD student, Heidelberg; SKATR lead developer"
first_mentioned: "[[Ore et al 2025 (SKATR)]]"
related:
  - "[[SKATR]]"
  - "[[Heneka, Caroline]]"
  - "[[Inference and ML]]"
---

# Ore, Ayodele

## Role and Affiliation

PhD student at Institut für Theoretische Physik, Universität Heidelberg, Germany, working in the research group of Caroline Heneka. Lead developer of SKATR (SKA Transformer), a self-supervised deep learning framework for 21cm cosmology that addresses the cross-simulator generalization problem.

## Academic Background and Research Focus

Ore is pursuing PhD research on machine learning methods for 21cm cosmology, with particular emphasis on self-supervised learning, Vision Transformers, and the challenge of generalizing machine learning models across different simulation codes. His work represents the intersection of modern computer vision techniques (transformers, contrastive learning) and cosmological inference problems.

## Research Contributions and SKATR

**Self-Supervised Learning Approach:** Rather than relying on labeled training data (simulations from a single code, which introduces simulator bias), SKATR uses a self-supervised learning strategy. The framework trains a Vision Transformer (ViT) to learn invariant representations by contrasting data from different simulators. The key insight is that while different codes produce different ionization field statistics, physical principles ensure certain invariances exist. By training the network to recognize these invariances, SKATR learns to map 21cm observations to interpretable latent space features.

**Vision Transformer Architecture:** Ore's use of Vision Transformers for 21cm data is physically motivated. Transformers excel at capturing long-range spatial correlations, which is essential in 21cm maps where ionized bubbles at one location can be correlated with structure far away (due to the hierarchical nature of reionization and the large scales involved). The ViT architecture naturally respects the spatial structure of 2D/3D cosmological maps.

**Cross-Simulator Generalization:** The core problem SKATR addresses is the same problem that motivates the EFT approach: different reionization codes (21cmFAST, ARES, CROC) predict different ionization field statistics for the same input parameters. SKATR's strategy is to learn representations that are robust to these simulator differences by training on data from multiple codes simultaneously. This provides an alternative (non-physics-based) approach to cross-simulator generalization.

**Comparison with Other Methods:** The SKATR paper includes comparisons with supervised learning baselines and with EoRFlow, positioning SKATR relative to existing approaches. These comparisons are important for understanding SKATR's strengths and limitations.

## Research Style

Ore's approach reflects modern deep learning methodology:
- **Data-driven:** Emphasis on learning from diverse training data (multiple simulators) rather than encoding prior physics
- **Self-supervised:** Avoiding reliance on expensive labeled training data
- **Careful validation:** Testing on held-out simulators and comparing to supervised baselines
- **Architecture-motivated:** Choosing neural network components (ViTs) for principled reasons related to the cosmological problem
- **Interpretability focus:** Attempting to understand what the learned representations capture about cosmology

## Key Contributions

**SKATR Framework (2025):** Ore is the lead author on the SKATR paper, introducing the self-supervised ViT approach to 21cm inference. This is his primary contribution to the field and represents a significant methodological advance in 21cm inference.

**Co-authorship on EoRFlow:** Ore also appears as a co-author on the EoRFlow paper, indicating involvement in or understanding of the simulation-based inference approach that SKATR is being compared against.

**Demonstrating ML-Based Solutions:** Beyond SKATR specifically, Ore's work contributes to demonstrating that machine learning approaches can address fundamental problems in reionization inference, such as simulator dependence.

## Relevance to This Thesis

Ore's work is directly and importantly relevant to the thesis for several reasons:

1. **Alternative Approach to the Same Problem:** SKATR and the EFT-based P2 approach both aim to solve the cross-simulator generalization problem, but they take opposite philosophical directions:
   - SKATR: Data-driven, self-supervised learning; learns invariances empirically
   - EFT (P2): Physics-driven, model-based; explicitly parameterizes simulator differences through effective parameters

   Understanding SKATR deeply is essential for articulating why the EFT approach is complementary or preferable: EFT provides interpretability, physics grounding, and systematic improvability that pure ML may lack.

2. **Competitive Benchmark:** Any paper on P2 (an EFT-based inference framework) will likely benchmark against SKATR as the most directly comparable recent work. Thus, understanding SKATR's design, performance, and limitations is essential for proper positioning of P2.

3. **Shared Research Group:** Both Ore and Pietschke (the lead developer of EoRFlow, the direct predecessor to P2) work in Heneka's group. This means the three approaches (EoRFlow, SKATR, P2) are being developed in dialogue with each other, informed by ongoing discussion within the Heidelberg group.

4. **Methodological Lessons:** SKATR's careful validation procedures, testing on held-out simulators, and comparison to baselines provide methodological guidance for how P2 should be evaluated. The fact that SKATR compares against supervised learning baselines suggests that P2 should similarly compare against other approaches (classical MCMC, other ML methods).

5. **Understanding Limitations:** By studying SKATR, one gains insight into what problems exist in the "pure ML" approach to cross-simulator generalization:
   - Black-box nature: Difficult to interpret what the network has learned
   - Simulator dependence of training: Results depend on which simulators are in the training set
   - Limited extrapolation: Unclear how models generalize beyond training parameter ranges
   - No physical interpretation: Learned representations may not correspond to physical quantities

   These are exactly the problems an EFT-based approach aims to address.

6. **Vision Transformer Insights:** If P2 also uses neural networks for feature extraction or posterior approximation, lessons from Ore's successful use of ViTs may be relevant.

## Connections and Collaborations

Ore is embedded in Heneka's research group at Heidelberg. His direct connections include:

- **Caroline Heneka** — PhD advisor and group leader
- **Yannic Pietschke** — Fellow student in the group; lead developer of EoRFlow
- **Other members of Heneka's group** — Involved in related 21cm ML research

The Heidelberg group's collaborative structure ensures that Ore's work on SKATR is informed by and discussed alongside Pietschke's work on EoRFlow.

## Papers / Work

| Title | Year | Relevance |
|-------|------|-----------|
| [[Ore et al 2025 (SKATR)]] | 2025 | First author; SKATR self-supervised Vision Transformer framework for 21cm inference; addresses cross-simulator generalization problem; main methodological alternative to EFT-based P2 |
| [[Pietschke et al 2025 (EoRFlow)]] | 2025 | Co-author; appears on the EoRFlow paper, indicating involvement in or awareness of supervised SBI approach |

## Notes

Ore represents the cutting-edge machine learning approach to 21cm cosmology. His SKATR framework is, from a methodological perspective, the most direct competitor to the EFT-based approach that P2 aims to develop. However, "competitor" is perhaps the wrong framing—SKATR and EFT-based methods are complementary, addressing the same problem (cross-simulator generalization) from different angles (data-driven vs. physics-driven). Understanding SKATR thoroughly is essential for properly positioning an EFT-based method in the landscape of modern 21cm inference techniques, articulating what advantages physics-grounded, interpretable EFT provides relative to black-box deep learning approaches.
