---
type: meta
title: Wiki Index
updated: 2026-09-13
---

# Wiki Index

## Domains

- [[21cm Cosmology]] — Signal physics, brightness temperature, HERA/SKA observational context
- [[Reionization Physics]] — EoR history, bubble morphology, ionization sources and sinks
- [[Effective Field Theory]] — Bias expansion, perturbation theory, EFT operators and coefficients
- [[Simulation and Codes]] — 21cmFAST, SCRIPT, THESAN, radiative transfer codes
- [[Inference and ML]] — SBI, neural networks, EoRFlow, SKATR, parameter estimation pipelines
- [[Thesis Work]] — Research log, methodology, P1/P2 tasks, timeline, deliverables

## Papers

### Reionization Physics (Background)
- [[Choudhury 2022 (Reionization Intro)]] — Pedagogical review; halo mass functions, photon budget, global reionization equation; **foundational background**
- [[Ferrara & Pandolfi (IGM Reionization)]] — Two-lecture overview; IGM physics, Lyman-alpha forest, GP effect, ionization topology
- [[Mesinger 2016]] — EoR review book (ed. Mesinger); Furlanetto ch. 9 = 21cm pedagogy

### Reionization Simulations (Background)
- [[Trac & Gnedin 2009 (Reionization Simulations)]] — Review of RT simulation methods; RT algorithm taxonomy; sources vs sinks
- [[Gnedin & Madau 2022 (Modeling Reionization)]] — Comprehensive code taxonomy; 21cmFAST, ARTIST, ASTRAEUS, fully coupled RT; **the field map**
- [[Mesinger et al 2010 (21cmFAST)]] — Original 21cmFAST paper; FFRT excursion-set ionization; Zel'dovich density; ~10% PS agreement with full RT; **code foundation**

### EFT Theory (Thesis-Core)
- [[McQuinn & D'Aloisio 2018]] — EFT bias expansion for 21cm; Minimal Model; P_err/P₂₁ < 10%; **foundational**
- [[Qin et al 2022 (EFT Redshift Space)]] — RSD extension; renormalized coefficients; THESAN validation; k ≲ 0.8 h/Mpc
- [[Sailer et al 2022 (Optical Depth EFT)]] — τ forecasts from perturbative 21cm; large-scale EFT + CMB lensing
- [[Baradaran et al 2024 (Hybrid EFT)]] — hybrid EFT: N-body density + EFT ionization painting; best accuracy

### Simulator Dependence (Core Problem)
- [[Berklas & Pober 2025]] — MCMC model dependence within 21cmFAST; biased posteriors from internal model variation
- [[Sooknunan et al 2024 (ML Reproducibility)]] — systematic ML reproducibility failures across simulators; networks learn code-specific features
- [[Zhou & La Plante 2022 (CNN Reionization)]] — CNN failure 21cmFAST→zreion; canonical cross-code demonstration
- [[Solt et al 2026 (Multi-Simulator Training)]] — multi-simulator training mitigates but doesn't solve; **empirical baseline for P2**

### SBI Pipelines & ML Methods
- [[Pietschke et al 2025 (EoRFlow)]] — EoRFlow SBI; $x_\text{HI}(z)$ from 2DPS; SKA-Low validated
- [[Pietschke et al 2026 (cross-correlation)]] — EoRFlow + 21cm×galaxy; constrains $f_\text{esc}$, $f_*$
- [[Ore et al 2025 (SKATR)]] — SKATR self-supervised ViT; **cross-simulator generalization**
- [[Schosser et al 2025 (Starobinsky)]] — SKA+CMB joint SBI; Starobinsky inflation constraints
- [[Duruisseaux et al 2026 (FNO)]] — FNO guide; resolution-invariant operator learning
- [[Deistler et al 2025 (SBI Guide)]] — Comprehensive SBI methods tutorial; NPE/NLE/NRE workflow; diagnostics (SBC, TARP); **methods reference for P2**

### Neural Operator Architectures
- [[Lu et al 2020 (DeepONet)]] — DeepONet; branch-trunk architecture; universal approximation theorem for operators; arbitrary output locations; high-order convergence
- [[Rahman et al 2023 (U-NO)]] — U-shaped Neural Operator; encoder-decoder with skip connections; 3D spatiotemporal native; 26–44% better than FNO on PDE benchmarks; memory-efficient via domain contraction
- [[Staddon 2026 (Isotropic FNO)]] — radially-binned spectral kernel $R(|\mathbf{k}|)$; SO(d)-equivariant FNO; ~16x (2D) / ~96x (3D) parameter reduction; right symmetry for the comoving real-space surrogate
- [[Shi et al 2025 (SirenFNO)]] — SIREN hypernetwork *generates* the Fourier kernel for all modes (no truncation); constant, resolution-independent parameter count; directly targets the FNO low-frequency bias; CP/TT/Tucker kernel decompositions
- [[Pérez Cuadrado et al 2025 (WHNO)]] — replaces Fourier with the **Walsh–Hadamard transform** (global rectangular step-wave basis); no Gibbs on discontinuous fields; same $O(n\log n)$, no trig; **FNO+WHNO ensemble beats either alone** on all 7 configs; the untried step-function basis for bubble walls

### 21 cm Forecasts & Reionization (recent arXiv digest, May 2026)
- [[Worku et al 2026 (PMFs 21cm Forecasts)]] — `zeus21` extended with primordial magnetic field contribution to $P_\text{lin}(k)$; HERA/SKA forecasts; example of modular new-physics priors on the forward model
- [[Wang & Shan 2026 (JWST Reionization Degeneracy)]] — $f_\text{esc} \times f_{\star,0}$ degeneracy of global reionization observables; JWST UV LF *shape* breaks it; "early-galaxy crisis" excluded at 4.5σ; relevant to what 21 cm alone can constrain
- [[Byrne et al 2026 (Digital Whitening Systematic)]] — instrumentation; digital whitening + re-quantization induces a frequency-dependent gain distortion not removed by bandpass calibration; forecast-realism caveat

### Thesis Documents
- [[Thesis Proposal (EFT of Ionization Field)]] — Supervisor's project proposal; defines P1 + P2; EFT coefficients as simulator-independent inference targets; **thesis foundation document**
- [[Chronological Research Report]] — LaTeX report on regenerating 21cmFAST neutral-fraction lightcones from ground-truth density fields, including the FNO/U-FNO, SirenFNO, Local-FNO, smooth-target, and LOS-grid results

## Entities

### People
- [[McQuinn, Matthew]] — UW; foundational EFT paper
- [[D'Aloisio, Anson]] — UC Riverside; foundational EFT paper
- [[Heneka, Caroline]] — Heidelberg ITP; EoRFlow + SKATR group
- [[Pietschke, Yannic]] — Heidelberg/Vienna; EoRFlow lead
- [[Ore, Ayodele]] — Heidelberg; SKATR lead
- [[Schosser, Benedikt]] — Heidelberg ARI; Starobinsky SBI
- [[Mesinger, Andrei]] — SNS Pisa; 21cmFAST developer; book editor
- [[Mason, Charlotte]] — SCRIPT developer
- [[Qin, Yuxiang]] — Qin et al. 2022; EFT on THESAN
- [[Pober, Jonathan C.]] — Brown; Berklas & Pober 2025 + Solt et al. 2026; simulator dependence expert
- [[Sailer, Neha]] — Berkeley; Sailer et al. 2022 + Baradaran et al. 2024; EFT forecasting
- [[Pritchard, Jonathan R.]] — Imperial; Sooknunan et al. 2024; 21cm community leader

### Codes & Tools
- [[py21cmfast]] — primary simulation code
- [[SCRIPT]] — second code for P1
- [[EoRFlow]] — Heidelberg SBI pipeline
- [[SKATR]] — self-supervised ViT; cross-simulator generalization
- [[swyft]] — TMNRE SBI framework for P2
- [[THESAN]] — RT hydrodynamical simulation suite
- [[powerbox]] — power spectrum utilities

### Telescopes & Experiments
- [[HERA]] — primary near-future 21cm array
- [[SKA]] — next-generation; full imaging capability
- [[LOFAR]] — current upper limits
- [[MWA]] — Australian precursor

## Planning Notes

- [[P1 EFT Characterization]] — Step-by-step P1 plan: EFT coefficient extraction across 21cmFAST and BEoRN
- [[P2 Cross-Simulator Inference]] — P2 plan: EFT-targeted SBI; cross-simulator posterior comparison
- [[FNO Approach for 21cm Emulation]] — FNO/U-NO emulation of $T_b$ and $x_\text{HI}$; EFT–FNO connection; suggested timeline
- [[Siren3D Residual Refinement Plan]] — Frozen-U-FNO + coordinate-conditioned sinusoidal residual head for bubble-wall refinement; boundary sampling, controls, and stop criteria
- [[Windowed Local-FNO U-Net Plan]] — U-FNO with **windowed** spectral mixing (overlapping Hann patches and shifted grids) plus one global Fourier bottleneck. A low mode inside a small window corresponds to a high effective frequency on the full grid; the design targets the measured low-frequency collapse at bubble walls. ~10.2 M parameters
- [[Smooth-Target Reparametrization Plan]] — Instead of learning $x_\text{HI}$ directly, learn a **smooth surrogate** (primary: $z_\text{re}(\mathbf{x})$, native 21cmFAST output; secondary: signed distance to front) and reconstruct $x_\text{HI}$ by deterministic thresholding. Uncertainty then appears as front *displacement* rather than front *blurring*. This is orthogonal to basis-side approaches and has good potential for EFT applications.
- [[Lightcone z_re Map Target]] — Implementation of the smooth-target plan's candidate 1, modified so that per-pixel $z_\text{re}(x,y)$ is **fitted from existing lightcones** (Gompertz front / LS step per sightline) rather than taken from the native `z_re_box`. No re-simulation is needed, and the problem becomes 2-D (density LOS slices as channels → $z_\text{re}$ map, NaN pixels masked). A reconstruction check shows that the lo-z/optimal step recovers global $x_\text{HI}(z)$ at voxel MSE ≈ 0.008–0.05; late reionizers are 79–99% no-front (the sentinel problem is real). Training results are in [[z_re Map Training Results]] and [[Loss Objective and Operator Basis Sweep]].
- [[Warped LOS Grid Plan]] — The cube cache's uniform-z LOS grid is **~37 Mpc at low z where the fronts live** (versus ~5 Mpc at saturated high z), a hard, model-independent bound on wall fidelity. The proposed **warped grid** samples with density ∝ ensemble-mean $|d\langle x_\text{HI}\rangle/d\chi|$ plus a floor and uses CDF inversion; envelope, uniform-χ, and crop variants are also considered. The training-free round-trip evaluator and per-timing-class metrics are in place, as are `build_cubes.py --target-z` and the Δχ volume-weighted loss. Real-cone results are in [[Warped LOS Grid Evaluation]].

## Findings

- [[Learned Waveform Basis Operator]] — The adaptive-basis experiment on 2-D $x_\text{HI}$: rather than choose between Fourier and Walsh, learn the mother waveform. **The basis turns out not to be a free parameter.** With the local branch replaced by an identity operator, the bottleneck waveform converges to a sine from four independent starts — sine (fixed point), square (0.914 → 0.9997), sawtooth (0.781 → 0.9995) and random (partial) — with the full 15-harmonic Nyquist budget available to hold any other shape, and with the table norm conserved so the motion is a genuine reparametrization. Every arm scores within 0.0013 of a plain FNO. This is a positive mechanistic result (Fourier is optimal within the candidate family, shown by convergence from four directions) and a negative one for the adaptive basis (freedom available, unused) — and it undercuts the square-wave intuition in [[Square-Wave Basis for Ionization Fields]]. Separate analysis/synthesis banks are a null despite genuinely diverging (r down to 0.67 at the shallowest slot). Deleting the windowed local branch costs at most one replicate-floor width while running ~4× faster on 13% fewer parameters. Replicate noise floor for the whole 2-D task, sd 0.0002–0.0009 in val_l2, is established here from a 21-run seeded control matrix.
- [[3-D Operator Matrix Final Results]] — The 3-D task was evaluated in 27 cells with a 20-epoch budget and 200 held-out test cones (10^9 voxels). `sfno/swhno` is within 2.3% of U-FNO's RMSE at 271x fewer parameters (0.0591 vs 0.0578, 748 k vs 202.9 M); the Walsh-Hadamard global slot transfers from 2-D to 3-D, and the SIREN-generated variant is the best global operator tested. Parameter count does not predict wall-clock time (the window loop and SIREN kernel regeneration dominate; the wavelet local slot costs 460 min/epoch). Auxiliary losses cost val_l2 in the same order across four architectures (plain < hybrid < bsd < expwall), while still helping on their target metrics: the hybrid halves the U-FNO front width, 16.32 -> 8.72 Mpc, for 4% of val_l2. The four metric families have different leaders — RMSE (U-FNO), bubble size (`cnn/swhno`, within 2% at every stage), $P(k)$ amplitude (`swhno/swhno`, 6.5% error), and $P(k)$ coherence (U-FNO) — and every model carries a +0.19 bias at true $x_\text{HI}\approx0.05$. Parameter counts now count complex Fourier weights as two reals. Inference timing (§2.1) shows that `sfno/swhno` is the second slowest model despite being 271x smaller, the global operator is effectively free (`fno/fno` and `fno/whno` differ by 0.005% across 14.7 M params), and the speed-accuracy Pareto front is just {`cnn/whno`, U-FNO}. §7.1 (2026-09-12) settles whether the U-FNO's 3-D gains were line-of-sight gains: **they are not** — decomposing its cylindrical error advantage, $k_\parallel$ explains under 14.9% in all 18 comparisons while $k_\perp$ carries 43–94%, which also closes the long-standing puzzle of why transverse-only edge losses helped `fno/whno` but did nothing for U-FNO.
- [[Phase Coherence and Bubble Size Bias]] — A reanalysis of the matrix evaluation changes how the §5/§7 result should be read. Small-scale phase accuracy, rather than small-scale amplitude, controls the bubble-size distribution: $\langle r(k)\rangle_{k>1}$ predicts MFP bias at Spearman +0.88 ($R^2 = 0.88$, zero bias at $r \approx 0.73$) and JS divergence at -0.92, while the amplitude ratio predicts nothing (-0.27, $p = 0.49$; partial +0.35 once $r$ is controlled). The result survives controls for RMSE (+0.71) and ionized-fraction error (+0.79), and is monotone 4/4 within the fixed-`swhno`-global family. The MFP estimator is a first-passage statistic, so the shortest obstruction dominates; the per-$k$-bin correlation rises monotonically to +0.97 at $k = 1.9$. At $\bar{x}_\text{HI} = 0.4$–$0.6$, every cell gets the ionized area right to 1–3% while the bias spans $-0.006$ to $-0.49$, indicating fragmentation rather than under-ionization. The $k^2$-weighted level-crossing rate $\nu = \sigma_1/\sigma_0$ tracks the MFP ratio at $\rho = -0.83$. The CNN cells' near-zero bias is partly cancellation: they under-produce boundaries ($\nu \approx 0.86$).
- [[Granulometry (BSD) Auxiliary Loss]] — Morphological opening is a differentiable stand-in for the MFP bubble-size distribution (Pearson r = 0.99 against the real estimator, with no threshold, on the raw field). In three seed-matched 20-epoch U-FNO runs, the relative bubble-size bias fell from +0.060 to +0.029 (−51%), with the best Wasserstein distance, at a cost of 6.5% val_l2 / 4.5% test RMSE. At `x̄_HI 0.60–0.80` the bias is +0.0015. JS divergence is marginally worse, so the shape is not fixed, only the mean; the large-bubble regime degrades for every loss. Because a size spectrum is translation-invariant, a field with every bubble displaced 37 px scores 21× better than one with wrong sizes, so this loss cannot be used without an L2/expwall anchor.
- [[U-FNO BatchNorm Train-Eval Mismatch]] — At batch size 1 on 3-D cubes, `ufno_norm=batchnorm` gives identical training loss but 4.6× worse `val_l2` (0.4829 vs 0.1049), with the gap growing from 4.2× to 8.1× and 33% of voxels pinned at hard zero. The checkpoint shows the cause: 31/32 channels in `unet3.conv3_1` have `running_var` below `eps`, producing a 28.6× train/eval scale discrepancy in that layer; `momentum=0.1` at batch 1 makes the running statistics an EMA over ~10 cubes. `UFNO_NORM=groupnorm` turned the worst cell of the matrix into the best completed run (val_l2 0.0471, val_h1 9.15 in 23.6 h, versus fno_whno-plain 0.0611 / 10.97 in 53.1 h).
- [[LOS-Monotone Theta Key in 3-D]] — This pre-registered test was closed on 2026-08-17 with a negative result, confirmed on a second architecture (`fno_whno` 0.0689 vs its plain cell 0.0611). `NOTES-contrast-map.md` §8 fixed the stop rule before the data existed. In a completed 20-epoch U-FNO run, `frac_band` never exceeded 1.2% and reached 0.0% at epoch 7, the epoch with the largest gain. Thus only 0–25 of 2048 refit slices entered the responsive band, and the gains came from the expwall objective rather than the map. On the matched architecture, the map costs 31% val_l2 / 34% val_h1 versus plain L2 (0.0616/12.26 against [[U-FNO BatchNorm Train-Eval Mismatch]]'s 0.0471/9.15). Note that `train gain` is negative = better, and the schedule is never the identity: it applies near-floor theta (~0.29) across the saturated z>12 region, ~60% of every cone, where there is nothing to sharpen.
- [[Loss Objective and Operator Basis Sweep]] — This 2026-07-26 report covers all three tasks. Pure L² beats L²+H¹ by ~35% on $z_\text{re}$ for every architecture, and the nominal 0.5/0.5 weights were misleading: H¹ supplied 99.4% of the 3-D loss, so every archived "L²+H¹" 3-D run was H¹-dominated. SIREN weights improve Local-FNO on $z_\text{re}$ (0.305 → 0.123); width saturates at 32; and mid-run LR comparisons are unreliable. On 2-D $x_\text{HI}$, Walsh–Hadamard in the global slot only is the best model (0.1453 vs Local-FNO 0.1487, U-FNO +9%); the local/global slot matters more than the basis. The U-FNO floor still holds in 3-D (0.0397). The earlier LocalWNO lead was a z-interpolation artifact.
- [[Edge and Wall-Placement Losses]] — `ExponentialWallDistance`, an exponential-in-distance absolute-error loss, reaches front width 1.16 px against truth 1.46, while every RMSE-optimal model sits at ~2.9, at a cost of ~22% RMSE and a high-$k$ power ratio of 0.51 → 0.82. H¹ seminorm and H² are exactly blind to misplacement (1.00× over 4→48 px), whereas a signed-distance loss changes 144×. This revises [[Transport-Based Edge Losses]]: SWD was not the winner; absolute versus squared error is the important distinction. An L² or BCE anchor is not optional.
- [[Warped LOS Grid Evaluation]] — A real-cone round trip over 926,903 front rays found that the production cache recovers only 12.7% of true front sharpness and misses 11.7% of fronts. `warped_256` reaches 33.2% / 4.9% at the same budget and beats uniform-$z$ at 512 slices, showing that sample placement matters more than sample count. `crop15_chi_256` nearly ties it without an ensemble-derived warp. Warped-cache training runs exist but are not yet comparable because they use a different target grid.
- [[z_re Map Training Results]] — Detailed companion to [[Loss Objective and Operator Basis Sweep]] with the 26-run per-model table, the Local-SirenFNO sweep conclusions, both training-failure root causes, the z_re infrastructure, and the per-branch mode-weight diagnostic. The diagnostic shows that the LOS axis is the only place where bandwidth still binds (edge/peak 0.60–0.78 versus 0.03–0.20 transverse).
- [[Structured-Transform Operator Findings]] — Detailed companion on the operator side, including the 29-run shared-slice leaderboard with `width`/`blur` columns against a TRUTH row, the local/global slot sweep, and the A30 benchmark. Local models are 20–60× smaller than the U-FNO at better accuracy and ~40% less peak memory; WHNO costs ~5% throughput and the local-slot wavelet ~53%.
- [[Contrast Map Sharpening]] — The two-parameter $(\theta,\tau)$ output reshaping gives a 6.2% post-hoc oracle gain, but that gain is unrealizable because τ is unpredictable from anything available at inference ($R^2\approx0$ even given z + 11 cosmological params). End-to-end training left a free differentiable sharpening dial near the identity (θ 4.75 → 4.43, ~130× less than truth-matched sharpness). The note also documents a reusable zero-init/weight-decay collapse pathology and a highK+contrast instability.
- [[FNO Lightcone Experimental Findings]] — In the 3-D FNO $\delta_m \to x_\text{HI}$ task on full lightcones (4× H200 DDP, 6600 cones), parameter conditioning drops val L² 0.20 → 0.06 and U-FNO + SyncBN reaches val L² = 0.0418, val H¹ = 8.27. More isotropic/LOS modes, BCE, GroupNorm, stronger H¹ weighting, and a doubled LOS U-Net receptive field do not improve the relevant architecture's floor; the bottleneck is not retained mode count or LOS receptive field.
- [[SirenFNO Spectral Bias Investigation]] — A new mode-weight diagnostic measures the FNO/U-FNO low-frequency collapse (in the 32-mode U-FNO, the low 8/32 modes hold 52% of spectral weight). A 3-D SirenFNO keeps the learned spectrum flat, beats the plain FNO (test L² 0.057→0.050, H¹ 11.6→9.8), but does not yet beat the U-FNO floor (0.040), plausibly because it lacks the local U-Net path. The next tests are boundary-band/$P(k)$ diagnostics and a SirenFNO×U-Net hybrid.
- [[Windowed Local-FNO U-Net Findings]] — In the first windowed Local-FNO run (local modes `(6,6,12)`, 21 epochs, ~10.2 M params), the design hypothesis failed: at epoch 20 the boundary diagnostic was worse than the U-FNO benchmark, with 10–90% front width 32.2 Mpc versus U-FNO 10.7 Mpc (truth 3.6), higher peak RMSE (0.32 vs 0.28), and higher gradient error (0.19 vs 0.16) at the wall. Whole-volume test L² 0.057 / H¹ 10.2 was at the plain-FNO level, but the run was undertrained and still descending. There were no patch seams, so windowed Fourier mixing did not reproduce the U-FNO's real-space convolution path for wall sharpness. At epoch 38, front width was 18.5 versus U-FNO 13.9 Mpc; the boundary-H¹ margin had shrunk by ~8×, but U-FNO remained significantly ahead. The ionized-wall loss experiment failed, and a parity diagnostic showed that the hedging bias (+0.17/+0.21 in nearly-ionized bins) is common to both architectures, so target-side approaches are now the priority.

## Concepts

### EFT / Theory
- [[Bias Expansion]], [[Stochastic Term]], [[Renormalization]], [[Regime of Validity]]
- [[Matter Overdensity Field]], [[Linear Growth Factor]]

### Reionization
- [[Neutral Fraction]], [[Ionization Morphology]], [[Bubble Size Distribution]] ✓ — mean-free-path estimator; U-FNO bubbles run +6–9% too large at early stages
- [[Mean Free Path]], [[Spin Temperature]], [[Excursion Set Formalism]], [[Clumping Factor]]

### Signal / Observation
- [[Power Spectrum as Summary Statistic]], [[2D Power Spectrum]], [[Cross-Power Spectrum]]
- [[Lyman Alpha Forest]], [[Foreground Wedge]], [[Redshift Space Distortions]]

### Inference / ML
- [[Simulation-Based Inference]], [[Neural Posterior Estimation]], [[Simulator Dependence]]
- [[Cross-Simulator Generalization]], [[Self-Supervised Learning]]
- [[Vision Transformer]], [[Fourier Neural Operator]], [[FiLM Conditioning]]
- [[Spectral Mode Cutoff in FNOs]], [[Structured Transform Neural Operators]], [[Walsh-Hadamard Neural Operator]]
- [[Training Set Generation]], [[Initial Conditions]]

### Loss Design / Boundary Sharpness
- [[Hedging Bias of Pointwise Losses]] — why L² (and H¹ one derivative up) provably prefer blurred fronts; the mechanism behind every front-width null
- [[Contrast Map]] — the $(\theta,\tau)$ monotonic output reshaping; definition, why the affine renormalisation is load-bearing, and its closed-negative status
- [[Sliced Wasserstein Edge Loss]] — optimal-transport distance between unit-mass edge measures; the Wasserstein barycenter of shifted sharp edges is still sharp, so it penalises displacement instead of rewarding steepness

### Concepts
- [[Simulator Dependence]] — full concept note with an evidence chain and mitigation map

## Sources

*(Full catalog in `wiki/sources/` — 24 papers summarized.)*

## Comparisons

*(To be populated as needed; a possible comparison is EoRFlow vs SKATR vs P2 on simulator dependence.)*

## Questions

*(To be populated as questions arise.)*

## Gaps

- Has EoRFlow been tested cross-simulator? (motivates P2)
- Does SKATR's cross-simulator generalization extend to coefficient-level interpretability?
- Which second simulator (SCRIPT vs SimFast21) for P1?
- How to match ICs between 21cmFAST and SCRIPT?
- Do EFT coefficients stay stable when 21cmFAST *internal* model is varied (per Berklas & Pober 2025)?
- What exactly are the simulator-specific morphological features that ML networks learn (per Sooknunan et al.)?
- [[Square-Wave Basis for Ionization Fields]] — Partially answered (2026-07-26): global-slot WHNO is the new 2-D $x_\text{HI}$ leader, but the premise was wrong (the payoff is in the *global* bottleneck, not the local walls) and it does not fix front width. 3-D, $z_\text{re}$, the FNO+WHNO ensemble, and the shift-consistency test remain open
- [[Transport-Based Edge Losses]] — Can a transport metric (SWD) recover wall sharpness by penalising *misplaced* edges rather than rewarding *steep* ones? It was the remaining loss-side test; SWD is the only edge term costing <1.2% L²
- [[LOS Bandwidth as the 3-D Bottleneck]] — Mode-weight diagnostics put the binding truncation on the LOS axis (edge/peak 0.60–0.78 versus 0.03–0.20 transverse), with headroom in both knobs. This could not be tested by the 2-D $z_\text{re}$ sweep and remains untested
