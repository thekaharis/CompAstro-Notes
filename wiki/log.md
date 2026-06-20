---
type: meta
title: "Operation Log"
updated: 2026-06-20
---

# Operation Log

*Append-only. New entries go at the TOP.*

---

## [2026-06-20] synthesis | Mode-cutoff findings consolidated; Siren3D plan filed

**Sources**: [[FNO Lightcone Experimental Findings]] Acts 3, 5, 6, and 7; current U-FNO v1/v2/v3 metrics and experiment interpretation.

**Concept created**:
- [[Spectral Mode Cutoff in FNOs]] — distinguishes the spectral branch's `n_modes` truncation from a hard output band-limit. Documents why pointwise, nonlinear, and U-Net paths can produce above-cutoff structure; translates mode counts into nominal axis-dependent physical edges; and records the repeated null results from isotropic modes, asymmetric LOS modes, and enlarged LOS receptive field.

**Planning note created**:
- [[Siren3D Residual Refinement Plan]] — proposes a frozen-U-FNO + coordinate-conditioned SIREN logit-residual head, zero-initialized to preserve the baseline. Includes boundary-aware sampling, staged fine-tuning, parameter-matched controls, success/stop criteria, and risks.

**Finding note updated**:
- Added the precise mode-cutoff interpretation and the empirical claim that the tested models are not bottlenecked by retained mode count.
- Added Siren3D as the next different-basis test after the global-pooling residual.
- Replaced the stale “try U-NO” item: the local-path experiment has already succeeded through U-FNO.

**Indexes/cache updated**: `wiki/index.md`, `wiki/thesis/planning/_index.md`, `wiki/concepts/_index.md`, and `wiki/hot.md`.

**Decision order**: global-pooling residual → boundary-distance diagnostic → frozen-U-FNO Siren3D with controls → limited joint fine-tuning only after a clean residual-only win.

---

## [2026-06-07] finding | U-FNO + SyncBN -- architectural breakthrough; Act 5 written up

**Source**: 30-epoch U-FNO + SyncBN run on the 4× H200 NVL cluster, `checkpoints_3d_ufno/metrics.jsonl`.  16-cone detailed viz run on the converged checkpoint (`figures/ufno-detailed_20260606-234954_job3966888/`) confirms the cone-61 high-z artefact diagnosed at epoch 20 of the pre-SyncBN run is fully resolved.

**Finding note updated**: [[FNO Lightcone Experimental Findings]] gains a new **§Act 5 -- U-FNO architecture: decisive breakthrough**.  Subsections: hypothesis, change, the **SyncBN gotcha** (documented as a methodological lesson), the 30-epoch trajectory table, comparison vs the FNO 100-epoch asymptote, **visual evidence** (embeds three diagnostic-cone lightcone strips + the 16-cone summary grid), and a paragraph on why `val_h1 = 8.27` is the bubble-wall-sharpness signal.  The §Headline Results table is updated from 4 to 5 rows; the §Synthesis section is rewritten -- the previous "information-bound" diagnosis is explicitly retracted in favour of an **inductive-bias-bound** reading with two boxed operational floors (pure-FNO at 0.056 / 11.36, U-FNO at 0.042 / 8.27).

**Headline numbers**:
- val L²:  FNO 100-ep. 0.0561 → **U-FNO 30-ep. 0.0418** (−25%)
- val H¹:  FNO 100-ep. 11.36 → **U-FNO 30-ep. 8.27** (−27%)
- val H¹ < 11 achieved for the first time in the entire campaign (the bubble-wall-sharpness signal we'd been watching for)

**Methodological lesson documented**: BatchNorm running stats are **not** synchronised by DDP -- only parameters are.  At `batch_size=1` per rank under 4-rank DDP the per-rank BN sees a single sample, the running stats drift independently, only rank-0's are saved, and the all-reduced eval metric averages over inconsistent forward passes.  Fix is one line (`nn.SyncBatchNorm.convert_sync_batchnorm`) inserted before the DDP wrap.  No-op for pure-FNO (no BN); critical for any architecture with BN under DDP.

**Index updated**: `wiki/index.md` `updated` bumped to 2026-06-07.

**Three follow-up experiments queued** (priority order):
1. Asymmetric Z-modes (`n_modes=(16,16,32)`) on the U-FNO -- physically motivated by LOS step-function content; cheap to test (no FFT cost change).
2. 100-epoch U-FNO baseline run to confirm the asymptote (~3-8 % marginal improvement expected).
3. `BATCH_SIZE=2` per rank on U-FNO to test convergence-speed / final-quality at larger effective batch.

---

## [2026-06-06] finding | 100-epoch BCE run completed — operational floor confirmed and tightened

**Source**: Full 100-epoch run on the cluster (BCE @ 0.5 variant of the modes=16 + parameter-conditioned configuration), `checkpoints_3d/metrics.jsonl`.  Same hardware as the original campaign (4× H200 NVL DDP, ~192 s/epoch, ~5.3 h total wall time).

**Finding note updated**: [[FNO Lightcone Experimental Findings]] gains a new "Addendum (2026-06-06): full 100-epoch trajectory of the BCE run" section under §Act 4 with milestone metrics every ~10 epochs, and the boxed operational-floor line in §Synthesis is tightened to the empirical 100-epoch asymptote.

**Three things this settles**:
1. **Operational floor refined**: `val_l2 ≈ 0.058` → **`val_l2 = 0.0561`**, `val_h1 = 11.36` at epoch 99. The §Synthesis projection from a 20-epoch extrapolation was ~3% conservative but qualitatively right.
2. **Cosine annealing earns the full 100 epochs**: between epochs 30 and 99, `val_l2` dropped 0.060 → 0.0561 (6.5%) and the val-metric oscillation visible at warmer LR (~10% bounce at epochs 15-20) is gone by epoch ~70. Earlier "plateau" calls (epoch 20-30) were premature.
3. **BCE didn't change the asymptote**: the earlier observation (epoch 19: BCE 4% worse than L²+H¹) was an early-trajectory artifact. By epoch 100, both runs are within noise at the floor. Information-bound diagnosis confirmed at the asymptote, not just at the early-epoch comparison.

**Implication for the queued experiments** (in [[FNO Lightcone Experimental Findings]] §"What to Try Next"): the 100-epoch BCE run establishes the empirical baseline that the U-FNO experiment (next up, sbatch script already in place) needs to *beat*, not just tie.  Tie = info-bound diagnosis is final; break = architectural inductive bias mattered after all.

**Index updated**: `wiki/index.md` `updated` bumped to 2026-06-06.

---

## [2026-06-05] finding | 3-D FNO lightcone experiments — parameter conditioning breakthrough + modes/BCE negative findings

**Source**: Experimental campaign on `Code/FNO v3/` (cluster `/pfs/10/work/hd_id260-fno_training/fno-21cm/`). 6600 21cmFAST lightcones from an 11-parameter LHS design, trained as a 3-D FNO mapping density → $x_\text{HI}$ on full $(140, 140, 256)$ cubes under 4× H200 NVL DDP.

**Finding note created**:
- [[FNO Lightcone Experimental Findings]] — Four-act ablation: density only → +parameters → +modes → +BCE.
  - **Act 1 (density only)**: Degenerate constant predictor, val L² = 0.20 flat, val H¹ = 17.85 flat. Visualisation shows cone 6 (a no-reionization extreme) predicted as fully ionized — maximally wrong.
  - **Act 2 (+ 11 LHS params as broadcast channels)**: val L² 0.20 → 0.06 (−61%) at epoch 0 alone; val H¹ 17.85 → 12.5 → 11.5. Predictions show qualitatively correct bubble morphology and correct reionization timing per cone. **Breakthrough.**
  - **Act 3 (n_modes 16 → 24)**: trajectories overlap from epoch ~10. Spectral capacity is not the bottleneck.
  - **Act 4 (BCE term @ weight 0.5)**: val_bce drops fast in epoch 0→1 then plateaus; val L² / val H¹ unchanged at the floor; mild regression at hardest slice ($z=5$ MSE 0.085 → 0.119). BCE commits uncertain voxels to the marginal prior (toward ionized at $z=5$ in the LHS sample), not toward truth.
- **Synthesis**: ceiling is input information, not capacity / loss formulation. Operational floor: val L² ≈ 0.058, val H¹ ≈ 11.5. Per-voxel residual is the irreducible stochasticity that EFT's $P_{\varepsilon\varepsilon}$ term is supposed to capture analytically — natural complement to [[P1 EFT Characterization]].

**Engineering wins documented**:
- Cube precompute + **direct-chunk merge** via `h5py.read_direct_chunk` / `write_direct_chunk`: ~43× speedup over decompress-recompress merge, made the 33-shard cluster build fit in walltime.
- Local NVMe staging in sbatch (28 TB per H200 node) → all 4 ranks share ~3 GB/s local I/O.
- 4-GPU DDP scaling: ~4.1× speedup over single H200 (near-ideal), bringing per-epoch from ~44 min (A30 streaming) → ~4.5 min.

**Methodological lessons**:
- Visualisation caught a silent checkpoint-loading bug (DDP `module.` prefix mismatch + `strict=False`) — viz was showing a random-init model for several runs before discovery. Fixed by an autodetect prefix loader that fails loudly on zero key matches.
- Negative findings (modes=24, BCE) are *informative* — they eliminate entire classes of explanation for the ceiling.

**Index updated**: new "Findings" section in `wiki/index.md`; `updated` bumped to 2026-06-05.

**Next experiments queued** (priority order, documented in finding note §"What to Try Next"):
1. Auxiliary global-history output ($\bar{x}_\text{HI}(z)$ as second head) — cheap regulariser
2. Early-time density as auxiliary input — addresses the diagnosed information bottleneck directly, but expensive (re-run 21cmFAST or compute linear field analytically)
3. Pivot loss to power-spectrum / summary statistics — what [[P2 Cross-Simulator Inference]] / SBI actually needs
4. [[FiLM Conditioning]] instead of channel concatenation
5. [[U-NO]] architecture trial

---

## [2026-05-12] ingest | Weekly arXiv digest (May 4–11, 2026) — 4 papers + FNO concept update

**Source**: Weekly arXiv digest scheduled task, run for the May 4–11 window. Searched four topic clusters (21 cm/EoR, EFT/bias expansion, SBI/neural inference, simulation codes) plus an ad-hoc cluster on Fourier Neural Operators in physical modeling. arXiv API was unreachable from this environment, so the digest was built from the live `astro-ph.CO` `/new` listing and targeted searches.

**Paper notes created**:
- [[Staddon 2026 (Isotropic FNO)]] — arXiv:2605.02597. Radially-binned spectral kernel $R(|\mathbf{k}|)$ makes the FNO $SO(d)$-equivariant. ~16x (2D) / ~96x (3D) parameter cut at matched accuracy on isotropic-PDE benchmarks. Distinguishes equivariance (operator-level) from invariance (output-level); anisotropic inputs still produce anisotropic outputs.
- [[Worku et al 2026 (PMFs 21cm Forecasts)]] — arXiv:2605.05323. Extends `zeus21` with a PMF contribution to $P_\text{lin}(k)$; HERA/SKA forecasts. Modular new-physics-prior pattern that EFT also slots into.
- [[Wang & Shan 2026 (JWST Reionization Degeneracy)]] — arXiv:2605.03635. Structural $f_\text{esc} \times f_{\star,0}$ degeneracy of global reionization observables; JWST UV LF shape breaks it; proposed JWST "crisis" excluded at 4.5σ. Relevant to what 21 cm alone can pin down vs. needs external priors.
- [[Byrne et al 2026 (Digital Whitening Systematic)]] — arXiv:2605.05489. Instrumentation-systematics paper; standard bandpass calibration does not remove the digital-whitening gain distortion. Filed under "forecast realism caveat", not on the critical path.

**Concept note updated**:
- [[Fourier Neural Operator]] — new "Symmetry: Isotropic / Equivariant FNOs and the 21 cm Anisotropy" section. Covers the equivariance-vs-invariance distinction; the correct factorization of the 21 cm forward chain (isotropic FNO core $\to$ explicit downstream symmetry-breaking layers for RSD, light-cone, beam, wedge); the LOS-as-input subtlety for the redshift-space map; symmetry-axis escalation path (vanilla → isotropic → equivariant w/ LOS input). Frontmatter `updated` bumped to 2026-05-12; `sources` extended with Staddon 2026; `related` extended with [[Redshift Space Distortions]].

**Index updated**: bumped `updated` to 2026-05-12; added [[Staddon 2026 (Isotropic FNO)]] under "Neural Operator Architectures"; new sub-section "21 cm Forecasts & Reionization (recent arXiv digest, May 2026)" with the three EoR-side papers; source count 20 → 24.

**Already-in-wiki paper cross-listed this week** (no new note needed):
- [[Solt et al 2026 (Multi-Simulator Training)]] (arXiv:2601.05229) appeared as a cross-listing in today's astro-ph.CO `/new` page. The paper itself is unchanged; flagged here for awareness that the empirical baseline P2 must beat is still actively circulating.

**Papers explicitly *not* ingested**:
- arXiv:2605.05114 (EFT of LSS with Newtonian motion gauges) — EFT extension for general LSS, no 21 cm / reionization application; tangential.
- arXiv:2605.00980 (frequentist tests of SBI for primordial non-Gaussianity) — SBI methodology, but the application is non-Gaussianity not EoR; noted only as a "general SBI-diagnostic caution" for the digest, not worth a wiki entry.

**Key new structural insight (this ingest)**: The thesis now has a clean symmetry argument tying its two halves together. EFT factorizes the ionization field into universal operators (rotationally symmetric in the physics) times code-specific bias coefficients (which absorb the symmetry-breaking small-scale astrophysics). An isotropic-FNO surrogate enforces the same factorization at the architectural level: the spectral kernel is rotationally symmetric, while observation-side anisotropies (RSD, LOS, wedge) live in explicit downstream layers. The two halves of the pipeline now share the same inductive bias rather than re-discovering it independently.

---

---

## [2026-05-11] ingest | New concept note — FiLM Conditioning

**Source**: Working conversation on input architecture for FNO/U-NO surrogate; how to inject cosmological / astrophysical / EFT parameters into spatial field emulators.

**Concept note created**:
- [[FiLM Conditioning]] — Feature-wise Linear Modulation: definition, tensor-level form of the affine transformation ($\gamma_c(\theta) \cdot h_{c,x} + \beta_c(\theta)$, channel-wise, spatial-constant), conditioning-MLP recipe with identity-init trick, placement inside FNO/U-NO blocks, Fourier-space interpretation, escalation path (channel-wise → spectral FiLM → hypernetwork), pitfalls for EFT-coefficient recovery in Task 2.

**Index updated**: added [[FiLM Conditioning]] to "Inference / ML" concepts section.

**Cross-link**: [[FNO Approach for 21cm Emulation]] Strategy B updated from bare "Feature-wise Linear Modulation" text to a wikilink.

**Key new insight (not previously captured)**: FiLM acts in Fourier space as a wavenumber-independent gain per channel — it cannot reshape the spectral profile of a channel, only re-weight which channels dominate. This is the precise reason a future spectral-FiLM or hypernetwork upgrade is needed if $R_\text{mfp}$-like parameters (which control characteristic scales) need to be conditioned on directly. Useful boundary for Task 2 design.

---

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
