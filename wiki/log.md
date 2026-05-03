---
type: meta
title: "Operation Log"
updated: 2026-04-28
---

# Operation Log

*Append-only. New entries go at the TOP.*

---

## [2026-04-28] ingest | Batch ingest — 2 FNO papers + 1 new planning note

**Sources**: `Thesis/FNOs/1910.03193v3.pdf`, `Thesis/FNOs/2204.11127v3.pdf`

**PDFs copied to**: `.raw/articles/`

**Summaries created**:
- [[Lu et al 2020 (DeepONet)]] — DeepONet: branch-trunk universal operator approximation; arbitrary output locations; high-order convergence; comparison to FNO
- [[Rahman et al 2023 (U-NO)]] — U-NO: U-shaped neural operators; encoder-decoder with skip connections; first 3D spatiotemporal neural operator; 26–44% gains over FNO on Darcy/Navier-Stokes

**Planning note created**:
- [[FNO Approach for 21cm Emulation]] — Detailed operational plan for two emulation tasks:
  1. Task 1: $\mathcal{G}_1: (\delta_m^\text{lin}, \theta) \to T_b(\mathbf{x},z)$ — brightness temperature surrogate for use as P2 forward model
  2. Task 2: $\mathcal{G}_2: (\delta_m, \theta) \to x_\text{HI}(\mathbf{x},z)$ — neutral fraction operator with explicit EFT connection; includes FNO–EFT scale decomposition analysis; FiLM conditioning strategy; cross-code transfer test via BEoRN

**Index updated**: new "Neural Operator Architectures" section under Papers; new "Planning Notes" section; source count 18 → 20

**Key new insight**: U-NO's native 3D spatiotemporal capability enables treating reionization as a single joint spatial+redshift operator, rather than slicing along redshift. The U-NO encoder bottleneck has a natural EFT interpretation (coarse-scale compression ↔ EFT truncation at $k_\text{max}$). DeepONet's arbitrary output locations are noted as an alternative for irregular observational geometries.

---

---

## [2026-04-20] ingest | Qin et al. 2022 (arXiv:2205.06270) — PDF ingested

- Source: `EFT for Reionization Simulations/An Effective Bias Expansion for 21 cm Cosmology in Redshift Space.pdf`
- Action: PDF copied to `.raw/articles/2205.06270 - Qin et al 2022 (EFT Redshift Space).pdf`
- Wiki note: [[Qin et al 2022 (EFT Redshift Space)]] was already mature from prior summary ingest; no content changes needed
- hot.md: updated PDF download status from ❌ to ✅
- Note: This is the same paper as "An Effective Bias Expansion for 21 cm Cosmology in Redshift Space" (the full title of the Qin et al. 2022 paper). It is the RSD + renormalization extension of [[McQuinn & D'Aloisio 2018]] and is central to P1's renormalization methodology.

---

## [2026-04-20] ingest | Batch ingest — 3 new papers

- Sources: `EFT for Reionization Simulations/EFT_of_ionization_fields_v2.pdf`, `EFT for Reionization Simulations/21cmFAST.pdf`, `Suggested Literature/2508.12939v1.pdf`
- Summaries created: [[Thesis Proposal (EFT of Ionization Field)]], [[Mesinger et al 2010 (21cmFAST)]], [[Deistler et al 2025 (SBI Guide)]]
- Index updated: added entries under Reionization Simulations (Background), SBI Pipelines & ML Methods, and new Thesis Documents section
- Domains updated: [[Simulation and Codes]] — 21cmFAST section linked to original paper
- Key insights:
  - **EFT_of_ionization_fields_v2.pdf**: This is the supervisor's thesis proposal document — the single most important document in the wiki. It defines the thesis hypothesis (EFT coefficients as a shared simulator-independent representation), frames P1 (EFT characterisation across 21cmFAST and SCRIPT) and P2 (EFT-informed cross-simulator inference), and explicitly cites all major motivating papers. The key theoretical move: instead of targeting the composite 21cm field, build the EFT directly for $x_\text{HII}(\mathbf{x},z)$, which is where simulator disagreement actually lives.
  - **21cmFAST.pdf** (Mesinger, Furlanetto & Cen 2010): Original 21cmFAST paper. Establishes the FFRT excursion-set algorithm for ionization and Zel'dovich density evolution. ~10% power spectrum agreement with full RT at k ≲ 0.5 h/Mpc. The native parameter set ($\zeta$, $T_\text{vir}$, $R_\text{mfp}$) defined here is the one Berklas & Pober 2025 shows is unreliable as an inference target — motivating the EFT approach.
  - **2508.12939v1.pdf** (Deistler et al. 2025): The `sbi` package's official tutorial paper. Covers NPE/NLE/NRE algorithms, the full workflow, and critically — SBC and TARP diagnostics for posterior calibration. Essential reference for implementing P2's inference pipeline.

---

---

## [2026-04-15] extend | Wiki-wide propagation of background paper content

- Domains updated (bodies extended, sources populated):
  - [[Reionization Physics]] — full photon budget section, halo mass function, observational probes table, ionization topology, EFT connection
  - [[Simulation and Codes]] — full code taxonomy table, semi-numerical + DMO+SAM + RT sections, AMBER/ASTRAEUS/DRAGONS/ARTIST added, RT algorithm taxonomy (moments/MC/ray-tracing)
  - [[Effective Field Theory]] — physical interpretation of EFT coefficients from new papers; Sources section populated
  - [[21cm Cosmology]] — spin temperature saturation note; new sources added
  - [[Thesis Work]] — background reading table added
  - [[overview]] — Background Reading section added
- Concept files created (8 new):
  - [[Excursion Set Formalism]] — Press-Schechter / Sheth-Tormen / ionized bubble criterion
  - [[Clumping Factor]] — recombination sink; code implementations; EFT connection
  - [[Neutral Fraction]] — definition, evolution table, observational constraints, local vs global
  - [[Ionization Morphology]] — inside-out topology, three morphological stages, simulator dependence
  - [[Mean Free Path]] — LLS physics; $R_\text{mfp}$ as simulation parameter; connection to $b_{\nabla^2}^x$
  - [[Lyman Alpha Forest]] — GP effect; saturation subtlety; relevance to thesis
  - [[Radiative Transfer]] — full RT equation; three algorithm families; convergence; why semi-numerical codes skip RT
  - [[Spin Temperature]] — coupling mechanisms; saturated limit; thesis assumption justified
- Entity files created (3 new):
  - [[Choudhury, Tirthankar Roy]], [[Ferrara, Andrea]], [[Gnedin, Nickolay Y.]]
- Index files updated: concepts/_index.md (✓ markers added), entities/_index.md (grouped by role)

---

## [2026-04-15] ingest | Batch ingest — 4 background papers (Reionization and Second Pass subfolder)

- Sources: `Suggested Literature/Reionization and Second Pass/` — 4 new PDFs
- Summaries created: [[Choudhury 2022 (Reionization Intro)]], [[Ferrara & Pandolfi (IGM Reionization)]], [[Trac & Gnedin 2009 (Reionization Simulations)]], [[Gnedin & Madau 2022 (Modeling Reionization)]]
- Entities noted (not yet created): [[Choudhury, Tirthankar Roy]], [[Ferrara, Andrea]], [[Pandolfi, Stefania]], [[Trac, Hy]], [[Gnedin, Nickolay Y.]], [[Madau, Piero]]
- Domains updated: [[Reionization Physics]] (sources section), [[Simulation and Codes]] (sources section)
- Key insights:
  - **Choudhury 2022**: Best single source for the derivation of the global reionization equation and the photon budget formalism that 21cmFAST implements. Sheth-Tormen mass function is more accurate than Press-Schechter at high masses — relevant for understanding collapsed-fraction differences between codes.
  - **Ferrara & Pandolfi**: Strongest on IGM observational probes (Lyman-alpha forest, GP trough) and inside-out vs outside-in topology. Physical intuition for what EFT coefficients encode in terms of bubble morphology.
  - **Trac & Gnedin 2009**: The three RT algorithm families (moments, Monte Carlo, ray-tracing) have converged; quasars insufficient to reionize. Establishes why full RT codes are the ground truth against which semi-numerical approximations are measured.
  - **Gnedin & Madau 2022**: Complete code taxonomy for 2022. 21cmFAST section (6.1.1) directly relevant to P1. Confirms that the speed/fidelity trade-off is fundamental — no code captures all physics.

---

## [2026-04-15] ingest | Batch ingest — 7 papers

- Sources: `EFT for Reionization Simulations/1806.08372v3.pdf`, `Understanding the Epoch of Cosmic Reionization.pdf`, and 5 papers in `Suggested Literature/`
- Summaries created: [[McQuinn & D'Aloisio 2018]], [[Mesinger 2016]], [[Pietschke et al 2025 (EoRFlow)]], [[Pietschke et al 2026 (cross-correlation)]], [[Ore et al 2025 (SKATR)]], [[Schosser et al 2025 (Starobinsky)]], [[Duruisseaux et al 2026 (FNO)]]
- Entities created: [[Heneka, Caroline]], [[Pietschke, Yannic]], [[Ore, Ayodele]], [[Schosser, Benedikt]], [[Mesinger, Andrei]], [[EoRFlow]], [[SKATR]]
- Concepts created: [[2D Power Spectrum]], [[Cross-Power Spectrum]], [[Self-Supervised Learning]], [[Vision Transformer]], [[Fourier Neural Operator]]
- Domains updated: [[Inference and ML]] (methods table, new entities/concepts, SKATR vs P2 comparison), [[21cm Cosmology]] (2DPS and cross-power added to observables)
- Key insight: SKATR (Ore et al. 2025) demonstrates cross-simulator generalization via self-supervised learning — the ML-driven approach to the same problem P2 addresses via EFT physics. The Heidelberg group (Heneka et al.) are likely connected to the supervisor's network; all 4 of their papers are in the suggested literature.

---

## [2026-04-14] scaffold | Scaffold complete

- Templates created: source, concept, entity, domain, comparison, question
- Sub-indexes created: domains/_index.md, concepts/_index.md, entities/_index.md
- Meta: wiki/meta/dashboard.md (Dataview), .obsidian/snippets/vault-colors.css
- Git: repo initialized, .gitignore written; run `git add -A && git commit -m "Initial vault scaffold"` from terminal to make first commit
- Note: Obsidian not yet installed — download at obsidian.md/download; enable vault-colors snippet in Settings > Appearance > CSS Snippets after install

---

## [2026-04-14] scaffold | Initial wiki structure

- Mode: E (Research)
- Purpose: Master's thesis — EFT-based simulator-robust 21 cm reionization inference
- Structure created: wiki/, .raw/, _templates/, domains (6), core meta pages
- Pages created: [[Wiki Index]], [[Overview]], [[Hot Cache]], [[21cm Cosmology]], [[Reionization Physics]], [[Effective Field Theory]], [[Simulation and Codes]], [[Inference and ML]], [[Thesis Work]]
- Key insight: Wiki initialized from conversation context; foundational papers and concepts already identified from supervisor's project proposal and McQuinn & D'Aloisio 2018.
