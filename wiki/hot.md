---
type: meta
title: "Hot Cache"
updated: 2026-05-12T00:00:00
---

# Recent Context

## Last Updated
2026-05-12 — Weekly arXiv digest (May 4–11, 2026) ingested. Four new paper notes ([[Staddon 2026 (Isotropic FNO)]], [[Worku et al 2026 (PMFs 21cm Forecasts)]], [[Wang & Shan 2026 (JWST Reionization Degeneracy)]], [[Byrne et al 2026 (Digital Whitening Systematic)]]) plus a new "Symmetry: Isotropic / Equivariant FNOs and the 21 cm Anisotropy" section appended to the [[Fourier Neural Operator]] concept.

## Isotropic FNO + 21 cm Anisotropy (Sixth Pass — new)

**[[Staddon 2026 (Isotropic FNO)]]** — radially-binned spectral kernel; the main technical update is in the [[Fourier Neural Operator]] concept note.

- **Construction**: $R_\ell(\mathbf{k}) \to R_\ell(|\mathbf{k}|)$ via parameter sharing within radial bins. Operator becomes $SO(d)$-equivariant.
- **Numbers**: ~16x fewer spectral params in 2D, ~96x in 3D; matched or better accuracy on isotropic benchmarks. Equivariance ≈ free rotational data augmentation.
- **Key distinction for 21 cm**: equivariance ≠ invariance. The constraint is on the *operator*, not the *output field*. An anisotropic input (e.g. one carrying a velocity field or a LOS direction) produces an anisotropic output.
- **Right factorization of the 21 cm forward chain**:
  1. *Isotropic FNO core*: $(\delta_m, \theta) \to (x_\text{HI}, T_b^\text{real})$ in comoving real space. This is where 21cmFAST produces its boxes; the physics is rotationally symmetric.
  2. *Downstream symmetry-breaking layers*: RSD using $\mathbf{v}_\text{pec}$ and $\hat{\mathbf{n}}_\text{LOS}$, light-cone interpolation, beam, foreground wedge.
- **Failure mode**: if you fold RSD into the FNO without passing the LOS as an explicit input, equivariance kills the $\mu^2$ Kaiser term.
- **Why this matters for the thesis**: parameter savings directly cut required training-sim count (the 21cmFAST bottleneck); ideologically consistent with EFT's "universal operator × code-specific coefficient" decomposition. Symmetry-axis escalation now reads: vanilla FNO → isotropic FNO → equivariant FNO with explicit LOS input.

## Recent arXiv Papers (May 4–11, 2026 window)

- **[[Worku et al 2026 (PMFs 21cm Forecasts)]]** (arXiv:2605.05323): `zeus21` extended with a PMF contribution to $P_\text{lin}(k)$, HERA/SKA forecasts. Useful as an example of how new-physics priors plug into an EoR forward model; EFT bias coefficients are defined relative to whatever $P_\text{lin}(k)$ is fed in, so this is a relabel-the-input scenario, not an EFT-killer.
- **[[Wang & Shan 2026 (JWST Reionization Degeneracy)]]** (arXiv:2605.03635): structural $f_\text{esc} \times f_{\star,0}$ degeneracy of global reionization observables; JWST UV LF shape breaks it. Relevant for P2 posterior interpretation: 21 cm alone will produce elongated posteriors along the product direction unless a UV LF shape prior is added.
- **[[Byrne et al 2026 (Digital Whitening Systematic)]]** (arXiv:2605.05489): instrumentation; digital whitening + re-quantization induces a frequency-dependent gain distortion not removed by bandpass calibration. Forecast-realism caveat, off critical path.
- **Cross-listed but unchanged**: [[Solt et al 2026 (Multi-Simulator Training)]] (arXiv:2601.05229) appeared as a cross-listing in this week's `/new` page. Already mature in the wiki as the P2 empirical baseline.

## Key Structural Insight (Sixth Pass)
The thesis now has a clean symmetry argument linking P1 and P2. EFT factorizes the ionization field into universal operators × code-specific bias coefficients. An isotropic-FNO surrogate enforces the same factorization at the architectural level: a rotationally symmetric spectral kernel does the universal lifting, while observation-side anisotropies (RSD, LOS, wedge) live in explicit downstream layers. The two halves of the pipeline now share the same inductive bias rather than re-discovering it independently.

---

## FiLM Conditioning (Fifth Pass — new concept)

**[[FiLM Conditioning]]** — Feature-wise Linear Modulation as the parameter-injection mechanism for the FNO/U-NO surrogate.

- **Affine form**: $\text{FiLM}_\theta(h)_{i,c,x} = \gamma_{c}(\theta_i)\cdot h_{i,c,x} + \beta_{c}(\theta_i)$. Channel-wise affine, spatial-constant. $\gamma, \beta \in \mathbb{R}^C$ produced by a small MLP from $\theta$.
- **Placement**: after $W_\ell h_\ell + \mathcal{F}^{-1}(R_\ell \mathcal{F}(h_\ell))$, before the activation, in every FNO block. Identity-init trick ($\gamma = 1 + \gamma^\text{raw}$, last linear zero-initialized) so the block starts as an unmodulated FNO.
- **Fourier-space action**: $\gamma_c(\theta)$ is a wavenumber-independent gain on channel $c$; $\beta_c(\theta)$ is a DC offset. FiLM **cannot reshape spectral profile** — that is $R_\ell$'s job. Mode-shaping requires spectral FiLM ($R_\theta = R \odot \gamma(\theta)$) or a hypernetwork over $R$.
- **Escalation path** for thesis: channel-wise FiLM → spectral FiLM → hypernetwork.
- **Why not the alternatives**: concatenation wastes capacity; per-voxel affine breaks resolution invariance; scalar modulation is too blunt.
- **Pitfall for Task 2** (EFT-coefficient extraction from FNO): overexpressive FiLM can memorize through parameters and mask physical degeneracies. Watch for non-smooth $\gamma, \beta$ vs $\theta$.

## FNO Architecture Papers (Fourth Pass — new)

- **Lu et al. 2020** (arXiv:1910.03193): DeepONet — branch net encodes input function at fixed sensors; trunk net encodes output query location; inner product gives $G(u)(y)$. Implements universal approximation theorem for operators. High-order convergence (up to exponential) vs. training set size. Key advantage over FNO: arbitrary output locations (no grid required). Useful fallback for irregular observational geometries (interferometric $uv$-plane).
- **Rahman et al. 2023** (arXiv:2204.11127, TMLR): U-NO — U-Net architecture adapted to function spaces. Encoder contracts spatial domain (↓ resolution, ↑ channels), decoder expands back with skip connections. **First neural operator for 3D spatiotemporal domains.** 26% improvement over FNO on Darcy flow, 44% on Navier-Stokes, 37% on 3D spatiotemporal task. Allows 3× deeper / 25× more params within same GPU memory. **Preferred architecture** for 21cm emulation over vanilla FNO.

## New Planning Note

**[[FNO Approach for 21cm Emulation]]** — Two emulation tasks defined:

1. **Task 1** — $\mathcal{G}_1: (\delta_m^\text{lin}, \theta) \to T_b(\mathbf{x},z)$: brightness temperature surrogate. Linear density + params in, full 21cm field out. ~$10^4$–$10^5\times$ speedup over 21cmFAST. Plug into P2 SBI loop as fast forward model. U-NO architecture with FiLM conditioning on $\theta$.
2. **Task 2** — $\mathcal{G}_2: (\delta_m, \theta) \to x_\text{HI}(\mathbf{x},z)$: learns the same functional as the EFT bias expansion, but without truncation. Key analysis: extract EFT coefficients from FNO output and compare to P1 ground truth. Scale decomposition: FNO and EFT should agree at $k < k_\text{max}^\text{EFT}$. Cross-code transfer test to BEoRN bridges to P2.

This work is aspirational (outside core P1+P2 scope) but concretely actionable if P1 stays on track.

## EFT Proposal Reference Papers (Third Pass — all new)

### EFT Theory Chain (now complete)
- **Qin et al. 2022** (arXiv:2205.06270): EFT in redshift space with renormalized coefficients; validated on THESAN; $k \lesssim 0.8\,h\,\text{Mpc}^{-1}$ at $\bar{x}_\text{HI} \gtrsim 0.4$. Key: **renormalization is mandatory** for resolution-independent coefficient comparison across codes.
- **Sailer, Chen & White 2022** (arXiv:2205.11504): τ forecasts from perturbative 21cm × CMB lensing; EFT bias coefficients are the bridge from large-scale 21cm to $\tau$.
- **Baradaran et al. 2024** (arXiv:2406.13079, PRD 110, 103517): hybrid EFT — N-body density field + EFT ionization painting; percent-level accuracy at intermediate $k$; most accurate semi-analytic 21cm model. Direct successor to McQuinn & D'Aloisio.

### Simulator Dependence Papers (now all ingested)
- **Berklas & Pober 2025** (arXiv:2511.13854): MCMC model-dependence within 21cmFAST; internal model variation biases posteriors. Key: problem is not just cross-code but within-code.
- **Sooknunan et al. 2024** (arXiv:2412.15893): systematic ML reproducibility survey; all architectures fail cross-simulator; networks learn code-specific morphological features, not physics.
- **Zhou & La Plante 2022** (PASP 134, 044001): CNN 21cmFAST→zreion failure; canonical cross-code demonstration; power spectrum differences visible at $k \sim 0.1$–$0.5\,h\,\text{Mpc}^{-1}$.
- **Solt, Pober & Bach 2026** (arXiv:2601.05229): multi-simulator training; improved OOD for $\Delta z$; **empirical baseline P2 must beat**. Limitation: compressed targets, no physical model for what's being universalized.

## Previously Ingested Papers (still active)
- McQuinn & D'Aloisio 2018 (arXiv:1806.08372) — EFT foundational; now linked to full EFT chain
- Heidelberg group (EoRFlow, SKATR, Starobinsky)
- Background reviews (Choudhury, Ferrara & Pandolfi, Trac & Gnedin, Gnedin & Madau)

## Key Facts
- Thesis topic: EFT of the ionization field $x_\text{HII}$ as a simulator-independent representation for 21cm reionization inference
- EFT target: $\{b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon}\}$ — all four coefficient types now have clear physical interpretations and literature context
- Renormalization (Qin et al. 2022 formalism) **must be applied** in P1 for resolution-independent cross-simulator comparison
- Simulator dependence is now documented with a full evidence chain across MCMC, CNNs, and general ML
- P2's empirical baseline is Solt et al. 2026; must demonstrate superiority via EFT-targeted inference

## Key New Structural Insight (Third Pass)
The three simulator-dependence papers (Berklas & Pober 2025, Zhou & La Plante 2022, Sooknunan et al. 2024) collectively show the problem operates at all levels: classical MCMC, single-architecture CNNs, and systematic ML surveys. Solt et al. 2026 is the best mitigation to date but lacks physical grounding. This makes the EFT approach the first *principled* solution with a physical basis for why it works.

## PDF Download Status
Papers in EFT folder:
- ✅ 1806.08372v3.pdf (McQuinn & D'Aloisio 2018)
- ✅ EFT_of_ionization_fields_v2.pdf (proposal)
- ❌ 2511.13854 (Berklas & Pober 2025) — needs manual download
- ❌ 2406.13079 (Baradaran et al. 2024) — needs manual download
- ✅ 2205.06270 (Qin et al. 2022) — PDF in .raw/articles/
- ❌ 2205.11504 (Sailer et al. 2022) — needs manual download
- ❌ 2601.05229 (Solt et al. 2026) — needs manual download
- ❌ 2412.15893 (Sooknunan et al. 2024) — needs manual download
- ❌ Zhou & La Plante 2022 (PASP) — no arXiv ID in paper; find via doi:10.1088/1538-3873/ac5596

Papers in FNOs folder:
- ✅ 1910.03193v3.pdf (Lu et al. 2020 — DeepONet) — PDF in .raw/articles/
- ✅ 2204.11127v3.pdf (Rahman et al. 2023 — U-NO) — PDF in .raw/articles/

## Active Threads
- P1 deliverable: reproduce McQuinn & D'Aloisio Fig. 2 (cross-correlation coefficient $r_{21m}(k)$)
- Apply Qin et al. renormalization formalism in P1 coefficient extraction
- Open question: does EFT hold within-code (across 21cmFAST model variants per Berklas & Pober)?
- Resolved: second simulator for P1 is BEoRN (Schosser et al. 2023, github.com/cosmic-reionization/BEoRN) — SCRIPT no longer publicly available
- Open question: has EoRFlow been tested cross-simulator? If not, P2 directly improves it
