---
type: finding
title: "Rhizome Neural Operator Results"
created: 2026-10-03
updated: 2026-10-14
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - concept/architecture
  - concept/training-budget
  - finding/positive
status: active
verdict: positive
related:
  - "[[Rhizome Neural Operator Figures]]"
  - "[[Native LOS Window Training]]"
  - "[[Multi-Field 21cmFAST Data]]"
  - "[[Global Reionization History Emulator]]"
  - "[[3-D Operator Matrix Final Results]]"
  - "[[2-D x_HI Variant Leaderboard (35 Runs)]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[Phase Coherence and Bubble Size Bias]]"
  - "[[LOS Bandwidth as the 3-D Bottleneck]]"
sources:
  - "`rhizome-neural-operator/` (repo `thekaharis/rhizome-neural-operator`): `ebm21cm/model/rhizome.py`, `ebm21cm/model/rhizome3d.py`, `ebm21cm/train_rhizome*.py`, `ebm21cm/export_*.py`"
  - "`rhizome-neural-operator/runs/` — `sweep1/`, `rhizome_xhi_w128*/`, `rhizome_xhi_w64_fnosplit/`, `rhizome3d/`, `rhizome3d_mf/`, `rhizome_mf2d_w64_structured*/`, `eval3d/`"
  - "`data/eval_cubes/{rhizome3d_*,rhizome2d_*,fno_cnn_whno_es,mf_cnn_whno_es_*}/` (exported test cubes)"
  - "fno-21cm evaluation suite (`viz.physical_evaluation`, `bubble_size_evaluation`, `power_spectrum_evaluation`, `boundary_band_diagnostic`) via `slurm/eval3d_suite.sbatch`"
---

# Rhizome Neural Operator Results

The **rhizome** is a recurrent, state-dependent integral operator: a hidden
state of `width` channels per grid cell is updated `T` times by a gated
source/receiver integral whose kernel is applied in Fourier space (truncated to
`modes`), with tied weights across updates. It was tested on the 21cmFAST
density -> $x_\text{HI}$ task,
first on 2-D slices with line-of-sight (LOS) context, then on native-LOS 3-D
windows, then multi-field (density + LOS velocity -> $x_\text{HI}$ + $T_b$), and
finally as a **slice-wise 2-D model that reassembles full 3-D cones**, first for
$x_\text{HI}$ and then multi-field (§6), the best rhizome variant overall.

**Figures** (head-to-head against UFNO, physical metrics, power spectra, slices,
strips, power-loss variants, 3-D runs): [[Rhizome Neural Operator Figures]].

## Key findings

- **The rhizome beats every fno-21cm model it was compared against, on every task.**
  - 3-D $x_\text{HI}$: test RMSE **0.0594** vs fno `cnn_whno_es` 0.0684.
  - Multi-field: **0.0495 / 5.79 mK** vs fno's best 0.0560 / 6.54 mK.
  - The margin is largest on physical observables: τ_e, timing, the b₁ bias, bubble sizes and front width.
- **Slice-wise 2-D beats native 3-D.** A 2-D rhizome that sees each slice plus 13 LOS density bands (±32 cells), applied slice by slice to rebuild whole cones, beats the 3-D rhizome trained on the **same 1,600 cones**.
  - It wins on nearly every physical metric over 200 test cones (§5).
  - It costs ~7x less training time.
  - It shows no LOS jitter.
  - This is direct evidence for [[LOS Bandwidth as the 3-D Bottleneck]]: what the 3-D models need from the LOS is ~±32 cells of context, not a 256-cell joint prediction.
- **Most of the 2-D advantage over fno 2-D models is LOS information.** The single-slice rhizome performs at the fno 2-D level; adding the LOS bands cuts mixed-slice RMSE by 36% (§2).
- **Much of the τ_e and global-history gap to fno comes from the loss, not the operator.**
  - fno trains MSE through a sigmoid. Near $x_\text{HI}=1$ the gradient vanishes, so fno leaves fully neutral cells at ~0.997: a measured offset of −0.002 to −0.003 at z > 15.
  - That offset integrates into a τ_e bias.
  - The rhizome trains BCE and saturates to −0.00006 (§4.3).
  - Timing (midpoint, duration), bias, P_ε, bubble sizes and fronts are *not* explained by this offset.
- **A warm restart at the end of training buys 3–6%.** A constant-LR continuation buys ~1%.
- **Best variant: multi-field slice-wise 2-D, trained on all 6,600 cones (§6).** Against fno's best multi-field model (`cnn_whno_es` `tbs+histtb`, "UFNO" in the head-to-head figures), on the same 199 test cones:
  - x_HI value-distribution W1 is −65% and the b₁ pull −57%;
  - bubble-size W1 −54%, small-scale incoherence −45%, front width 3.9 vs 6.2 Mpc;
  - T_b value-distribution W1 during reionization is −34%;
  - it wins all 8 inspected cones by 12–28% in full-cone RMSE.
- **Its one weakness is T_b before reionization.** It adds small-scale T_b power (+25σ vs +4σ for the 3-D rhizome), concentrated in quiet absorption-era slices (§6.3). Three fixes did not work:
  - training on 3.9× more cones improved those T_b values (W1 −31%) but left the excess power unchanged;
  - smoothing the spin variable along the LOS removed the excess only by destroying real structure (T_b RMSE +40–110%);
  - LOS context to ±128 cells made it worse (+36σ).

  **A small-scale $T_b$ power term in the loss fixes it:** +24.8σ -> **+1.5σ**, better than the 3-D rhizome's +4.1σ.
  - It also improves the statistics: $T_b$ power within 1–2% at all scales, bubble-size W1 −14%, τ_e −20%.
  - The price is 4–8% higher per-voxel RMSE (consistent over 80–90% of cones) and ~6% on edges (§6.7).
  - Keep both variants: the power-loss model for 21-cm statistics, the plain model for per-voxel accuracy.
  - **Adding the same term on $x_\text{HI}$** (§6.8) roughly halves the high-k $x_\text{HI}$ power deficit (k > 1 error over active slices 0.163 -> 0.089) and keeps the absorption-era fix (+1.3σ), for another 2–4% per-voxel RMSE and slightly lower small-scale coherence.
- **A third of the absorption-era $T_b$ error is a per-slice constant offset** (random sign per cone, not a bias). Its size is the same for all three model families and of the order of the global-history emulator's own error (§6.5).
- **It is also the fastest model end to end** once its input building runs on the GPU with prefetched reads: **5.5 s per full cone on an A100 / 3.7 s on an H200**, vs 12.8 / 8.3 s for the 3-D rhizome and 9.8 / 7.0 s for fno (§7).
- **The rhizome's Fourier kernel shows no low-frequency collapse** (high/low-quarter weight ratio 0.78–0.94 vs 0.10–0.45 for the U-FNO), so SIREN kernels would not fix a spectral bias here (§6.4).
- **A radius-restricted real-space kernel never matches the Fourier kernel** (§6.9).
  - The gap shrinks with radius but saturates: +62% at R = 1 cell, +13% at R = 4, +12% at R = 6. The best local kernel (R = 8, rank 16) is still +6.5%.
  - At equal training cost (R ≈ 2–3) the local kernel is 19–36% worse. The N log N vs N·n argument misses the channel mixing: a dense local kernel costs C²·n per pixel.
  - Reach matters more than per-offset channel mixing.
- **The number of updates T barely matters** (§6.10): T = 3, 6 and 10 are within 2%, and two T = 6 seeds agree to five digits on validation. T = 3 trains in 60% of the time.
- **One or two updates cost only a few percent** (§6.10). Test RMSE: T = 2 is +1–2%, T = 1 is +3–4%. A single full update (T = 1, Δt = 1, no recurrence) is within 5% of the best rollout. The rollout depth is not what separates the rhizome from fno.
- **Freezing the gates at the initial state costs about 2%,** consistently over two seeds (§6.14). Frozen gates still depend on the conditioning and still multiply the kernel at both ends, so this measures only the value of updating the gates during the rollout. Removing the gates altogether (A = B = 1) is not yet tested.
- **A two-level rhizome helps only with the plain loss** (§6.15).
  - The best plain-loss model is a spectral kernel on a 4× coarser grid plus a compact R = 2 kernel at full resolution: −3% validation score vs the single-level model with the same updates, at half the parameters. It is also the only plain-loss model without a high-k $x_\text{HI}$ power deficit.
  - The coarse level must be spectral.
  - With both power terms there is no gain.
- **The trained rollout is a transient, not an iteration to equilibrium** (§6.16).
  - Every model is best exactly at its trained T and (for T ≤ 6) degrades when run further; T = 10 settles.
  - Beyond the trained length the state ends in a small two-cycle (1–6% per update). This is the signature of an overshooting step size; a Δt = 0.25 run is training.
- **The emulated $x_\text{HI}$ history is the important scalar input** (§6.11). Dropping it costs 15% on validation (test $x_\text{HI}$ +12%, $T_b$ +7%) and 10–30% of the small-scale power during reionization; dropping the $T_b$ history costs only 2%.
- **The gates extend the kernel's reach to the excursion-set scale** (§6.13). The bare Fourier kernel falls to half within 3.6 Mpc, but averaged over 7,200 receiver cells the gates boost incoming connections out to 10–25 Mpc. Ionized cells keep their receivers open and collect from the furthest; front and neutral cells settle after 2–3 updates.
  - The power-loss model gates more strongly and more locally at fronts (3.5× vs 2.0×, half-width 9 vs 14 Mpc).
- **At native LOS resolution, UFNO smooths along the line of sight** (§6.12). Its $x_\text{HI}$ and $T_b$ power falls off at $k_\parallel \gtrsim$ 0.5 Mpc⁻¹, which the 512-point evaluation grid (LOS cells of 4–14 Mpc) could not show. The slice-wise rhizome loses power only at $k_\parallel \gtrsim$ 1.5 Mpc⁻¹; with both power terms its $x_\text{HI}$ power is within ±10% in 91–100% of all (k⊥, k∥) cells.

## 1. Setup

| | 2-D | 3-D | slice-wise 2-D |
|---|---|---|---|
| input | slice + 13 LOS density bands (±32 cells: single slices within ±3, band means to ±32) | native LOS windows 256 + 2×32 halo (fno-21cm pipeline) | 2-D model on every slice, bands built from the raw cone |
| conditioning | log(1+z), 11 parameters (FiLM-style scalars) | `z_params` channels | as 2-D |
| loss | BCE on $x_\text{HI}$ | masked BCE (+ MSE on normalized $T_b$ for multi-field) | BCE |
| data | slice cache: 16 window + 2 background slices / cone, 5,280 train cones (own split) | fno 2000-cone preparation (1600/200/200; multi-field: 1594/199/199, cleaned $T_b$) | fair split: fno's 1,600 train cones, 48+6 slices / cone; multi-field: §6 |

3-D model: anisotropic modes (36,36,24), rank-48 factorized spectral kernel, 6
updates, step 0.5, LOS zero-pad 64, bf16 autocast with float32 FFT, 20 epochs
of 6,400 windows at lr 2e-3 (warmup + cosine), 40-cone validation subset per
epoch, full evaluation at the end.

## 2. 2-D $x_\text{HI}$ (slice cache)

**Sweep** (15k steps, batch 16, A100, one seed each; mixed-slice RMSE =
slices with mean $x_\text{HI}$ in 0.05–0.95):

| change from centre (w64, modes 24, T=6, lr 2e-3) | val BCE | mixed RMSE |
|---|---:|---:|
| centre | 0.1502 | 0.1123 |
| width 32 / 96 / 128 | 0.1539 / 0.1500 / 0.1489 | 0.1189 / 0.1126 / 0.1093 |
| batch 32 (2× slices) | **0.1477** | **0.1077** |
| modes 12 / 36 / 48 | 0.1528 / 0.1496 / 0.1533 | 0.1193 / 0.1117 / 0.1177 |
| updates 3 / 10 | 0.1514 / 0.1518 | 0.1142 / 0.1154 |
| **single slice only** (`center`) | 0.1980 | **0.1741** |
| single slices within ±3 (`singles`) | 0.1694 | 0.1380 |

- **LOS bands dominate.** Single slice 0.174 -> ±3 slices 0.138 -> all bands 0.112.
- **Width:** parameters grow ~width² (1.1 M -> 18.3 M from w32 to w128), but training time grows only ~linearly (275 -> 73 slices/s). Accuracy gains are diminishing: w64 ≈ w96, and w128 is −3%.
- **At equal compute, more slices beat more width.**

**Final run** (w128, batch 32, plateau-stopped at 68k steps, 6.5 h A100):
test mixed-slice RMSE **0.099**, all-slice 0.092, ionized IoU 0.914.

**Against fno-21cm 2-D models** on the same 7,036 validation slices (sweep w128
at 15k steps):

| | slice RMSE | ionized IoU | front width (truth 3.0 Mpc) |
|---|---:|---:|---:|
| **rhizome** | **0.109** | **0.873** | **6.1** |
| fno LWF | 0.178 | 0.755 | 32.6 |
| fno WHNO | 0.181 | 0.755 | 31.0 |
| LocalFNO / U-FNO | 0.184 / 0.195 | 0.742 / 0.722 | — |

The fno 2-D models see a single slice. The single-slice rhizome (0.174) sits at
their level, so the LOS bands, not the operator, make most of this gap.

## 3. 3-D native LOS windows, $x_\text{HI}$

**Test RMSE, 200 cones, full native resolution:**

| model | params | 20 epochs | + constant 2e-5, 10 ep | **+ warm restart** (lr 5e-4, cosine, 10 ep) |
|---|---:|---:|---:|---:|
| rhizome w48 | 5.8 M | 0.0619 | 0.0613 | **0.0594** |
| rhizome w64 | — | 0.0650 | 0.0644 | 0.0628 |
| rhizome w48 / w64 at lr 3e-4 | | 0.0701 / 0.0690 | | |
| fno `cnn_whno_es` (30 epochs) | 3.5 M | 0.0684 | | |

- **Narrower is better here:** w48 beats w64.
- **lr 2e-3 is right:** 3e-4 is 13% worse at w48.
- The 40-cone validation subset was again a poor proxy for the full split (see [[Native LOS Window Training]]).

**Physical suite** (fno-21cm tools, 200 test cones, medians; rhizome w48 after
the warm restart vs fno `cnn_whno_es`):

| metric | rhizome | fno |
|---|---:|---:|
| \|Δτ_e\| / σ_Planck | **0.019** | 0.058 |
| \|Δz(x̄_HI=0.5)\| | **0.028** | 0.098 |
| \|Δ duration\| | **0.031** | 0.060 |
| $x_\text{HI}$ PDF W1 (active) | **0.021** | 0.030 |
| b₁ pull | **1.58** | 3.41 |
| P_ε ratio (ideal 1) | **0.89** | 0.77 |
| bubble-size W1, active (Mpc) | **0.81** | 1.39 |
| small-scale ($k>1$) power error | **0.222** | 0.336 |
| 3-D edge L2 / H1, ±2 Mpc band | **0.219 / 0.137** | 0.235 / 0.145 |
| front width (Mpc) | **5.9** | 7.5 |

The warm restart improved the bubble-size W1 by 22% (1.04 -> 0.81). Its 3-D
edge gains over the 20-epoch model are significant in the paired bootstrap
over 175 cones.

Figures: [[Rhizome Neural Operator Figures#7. 3-D rhizome (§3, §4)|3-D rhizome vs fno]].

## 4. 3-D multi-field (density + LOS velocity -> $x_\text{HI}$ + $T_b$)

Same data, split and cleaned $T_b$ as fno's `*_histtb_tbclean` runs (verified
identical 1594/199/199 split). The structured head is a port of fno's
`StructuredBrightness`: $T_b = A(z)\,x_\text{HI}(1+\delta)(1-e^u)V(dv/dr)$.
Loss: BCE + MSE on normalized $T_b$. Selection: mean normalized MSE.

### 4.1 Test RMSE ($x_\text{HI}$ / $T_b$ mK)

| run | inputs / head | 20 epochs | + warm restart |
|---|---|---:|---:|
| A0 | density -> $x_\text{HI}$ only | 0.0602 | **0.0567** |
| A | + velocity, + $T_b$ (plain head) | 0.0648 / 9.49 | 0.0622 / 8.71 |
| B | A + global-history emulator channels | 0.0509 / 6.26 | 0.0494 / 6.07 |
| **C** | B + structured $T_b$ head | 0.0507 / 5.97 | **0.0495 / 5.79** |
| fno `cnn_whno` | density only | 0.0836 | |
| fno `es+histtb` | = B | 0.0577 / 6.63 | |
| fno `tbs+histtb` | = C | 0.0560 / 6.54 | |

- **History channels are what help.** A -> B is −21% on $x_\text{HI}$ and −34% on $T_b$.
- **Velocity and a $T_b$ target alone do not help $x_\text{HI}$.** A is *worse* than A0 (one seed).
- **The structured head mainly helps $T_b$.** It also helps reionization timing (C beats B by 15–30% on the midpoint and duration).
- **Density-only rhizome A0 nearly matches fno's best multi-field model:** after the warm restart it beats fno `es+histtb` (0.0567 vs 0.0577), which gets velocity and both histories too.

### 4.2 Physical suite (C, B vs fno histtb runs, 199 cones)

| metric | **C** | B | fno `tbs+histtb` | fno `es+histtb` |
|---|---:|---:|---:|---:|
| \|Δτ_e\| / σ_Planck | 0.014 | **0.013** | 0.076 | 0.116 |
| \|Δz\| at x̄ = 0.25 / 0.5 / 0.75 | **0.013 / 0.011 / 0.009** | 0.017 / 0.013 / 0.013 | 0.026 / 0.017 / 0.016 | 0.021 / 0.020 / 0.026 |
| \|Δ duration\| | **0.022** | 0.031 | 0.044 | 0.059 |
| b₁ pull | **1.52** | 1.54 | 2.28 | 2.87 |
| P_ε ratio | **0.935** | 0.937 | 0.793 | 0.801 |
| bubble W1 active (Mpc) | **0.71** | 0.74 | 1.21 | 0.96 |
| $x_\text{HI}$ power error large / small $k$ | **0.043 / 0.243** | 0.048 / 0.244 | 0.119 / 0.311 | 0.118 / 0.337 |
| $T_b$ PDF W1 active (mK) | **1.10** | 1.15 | 1.19 | 1.25 |
| $T_b$ power ratio $k$ = 0.11 / 0.20 (ideal 1) | **0.98 / 0.96** | 0.91 / 0.88 | 0.90 / 0.90 | 0.92 / 0.91 |
| small-scale $T_b$ power excess, pre-reionization | **+3.9σ** | +3.5σ | +12.8σ | +12.6σ |
| front width (Mpc, truth 2.77) | **4.53** | 4.55 | 6.17 | 5.79 |

- **The structured head fixes $T_b$ power amplitude.** Without it (B), $T_b$ power is ~10% low at every stage.
- **fno adds spurious small-scale $T_b$ structure in the absorption era.**

Figures: [[Rhizome Neural Operator Figures#7. 3-D rhizome (§3, §4)|3-D multi-field]].

### 4.3 Why fno's global history is off (loss, not operator)

- **Both families give the same global-history input**, but fno's global $x_\text{HI}(z)$ sits **−0.002 to −0.003 low from z ≈ 8 to 25**, with a wide cone-to-cone spread. The rhizome is flat on zero.
- **Measured in truly neutral cells at z > 15** (20 cones): mean (pred − truth) is −0.0020 / −0.0030 for the two fno runs, against **−0.00006** for the rhizome. Only 0.1–1.5% of those cells drop below 0.99, so the fno error is a near-uniform shift.
- **Mechanism:** MSE through a sigmoid has a vanishing gradient at saturation; BCE's gradient in logit space stays at (p − y). See [[Hedging Bias of Pointwise Losses]].
- **This shift drives fno's τ_e bias.** Fair comparisons on τ_e and the global history need fno retrained with BCE on $x_\text{HI}$.
- The parameter-only emulator alone gives |Δz_mid| ≈ 0.044 (its own evaluation). Both model families improve on it, the rhizome ~4×.

## 5. Slice-wise 2-D reconstruction of 3-D cones

Idea: treat every native slice as a 2-D sample with its own ±32-cell LOS
context, predict independently, restack. It is maximal-overlap windowing:
window 1, stride 1.

**Quick check** (original 2-D w128, 5,280 cones, own split). Only 21 of 200
3-D test cones were clean, because 161 were in its training set.

- 512-slice grid RMSE: **0.028** vs 3-D rhizome 0.039 vs fno 0.046.
- It beats the 3-D rhizome on 16/21 cones and fno on 21/21.
- Confound: 3.3× more training cones.

**Fair version** (new slice cache from fno's x_HI split = same 1,600 train cones
as the 3-D models, 48+6 slices/cone, ~76k train slices; same hyperparameters).
Results on all 200 test cones:

| metric | 2-D w128 | **2-D w64** | 3-D rhizome w48 (+warm restart) | fno `cnn_whno_es` |
|---|---:|---:|---:|---:|
| \|Δτ_e\| / σ_Planck | **0.011** | **0.011** | 0.019 | 0.058 |
| \|Δz\| at x̄ = 0.25 / 0.5 / 0.75 | **0.014 / 0.011** / 0.009 | 0.021 / 0.014 / **0.008** | 0.033 / 0.028 / 0.018 | 0.042 / 0.098 / 0.084 |
| \|Δ duration\| | 0.034 | **0.022** | 0.031 | 0.060 |
| $x_\text{HI}$ PDF W1 active | **0.011** | 0.013 | 0.021 | 0.030 |
| partially-ionized fraction (truth 0.086) | **0.135** | 0.137 | 0.163 | 0.176 |
| b₁ pull | 1.01 | **0.85** | 1.58 | 3.41 |
| P_ε ratio | **0.95** | 0.94 | 0.89 | 0.77 |
| bubble W1 active (Mpc) | 0.59 | **0.56** | 0.81 | 1.39 |
| power error large / mid / small $k$ | 0.027 / **0.062** / 0.211 | **0.016** / 0.073 / **0.196** | 0.068 / 0.174 / 0.222 | 0.128 / 0.172 / 0.336 |
| 1 − coherence, small $k$ | **0.119** | 0.120 | 0.199 | 0.181 |
| 3-D edge H1, ±2 Mpc | **0.109** | 0.110 | 0.138 | 0.145 |
| front width (Mpc, truth 2.65) | **4.03** | 4.10 | 5.91 | 7.54 |

- **The advantage survives the fair split.** It is driven by front *placement* (incoherence 0.20 -> 0.12), mid-scale power (−60%) and sharper fronts. 3-D edge H1 is −21% vs the 3-D rhizome, P = 0.000 over 175 cones.
- **Width barely matters:** w64 ≈ w128 everywhere. w64 trains in 2.8 h vs 5.0 h, so it is the choice.
- **Per cone** (13 inspected): the 2-D model wins 11.
  - It loses on cone 27, the earliest reionizer (z_mid ≈ 15.9). There the 3-D rhizome's longer LOS context helps slightly, and all models predict ionized gas as too neutral.
  - It also loses narrowly on cone 1066.
- **No LOS jitter.** Slice-to-slice roughness, pred/truth, is 0.97–0.98, against 0.93 for both 3-D models, which are slightly over-smoothed. At native resolution (cone 1063): r = 0.992, parity slope 0.98, std ratio 0.99.
- **Error maps:** the 2-D errors are thin rims on bubble walls. The 3-D models (fno strongly, the 3-D rhizome weakly) miss whole ionized regions and show a faint too-ionized haze over neutral gas (fno).
- **Shared failure:** large flat plateaus of intermediate $x_\text{HI}$ (≈0.3–0.6) in the truth (e.g. cones 770, 354, 1066, 27) are reproduced by no model.

Caveat: the 512-point evaluation grid is uniform in z and over-weights neutral
high-z slices relative to the native grid, so its absolute RMSEs are lower
(e.g. 0.044 vs 0.0594 for the 3-D rhizome). Rankings are unaffected.

Figures: [[Rhizome Neural Operator Figures#6. Slice-wise 2-D $x_\text{HI}$ vs 3-D (§5)|slice-wise vs 3-D]].

## 6. Multi-field slice-wise 2-D (best rhizome variant)

**Model.** The 2-D rhizome (w64, 6 updates, 24 modes, batch 32) on each slice:
- **Inputs:** 13 LOS bands of normalized density and 13 of LOS velocity as image channels. The scalars are 1/(1+z), the 11 parameters, and the 13 band means of each emulated global history ($x_\text{HI}$, $T_b$): 38 values in all.
- **Outputs:** an $x_\text{HI}$ logit and the spin variable u, with $T_b = x_\text{HI}\cdot A(z)(1+\delta)V(dv/dr)\cdot(1-e^u)$.
- **Physics term:** $A(1+\delta)V$ is precomputed per slice with exactly the 3-D structured head's code (`StructuredBrightness3d.physical_factor`).
- **Data:** the cache is built through fno-21cm's own multi-field pipeline, so data, split, normalization and history emulators match §4. Pilot check: $T_b/(x_\text{HI}\cdot A(1+\delta)V)$ gives a smooth spin factor, 0.8 during reionization to −0.08 in absorption.
- **Training:** loss BCE + MSE on normalized $T_b$; selection on the mean normalized MSE; plateau-stopped.

Two training sets, the same 199 val / 199 test cones:

| run | train cones | slices / cone | train slices | steps / A100 time | test-slice x_HI / T_b |
|---|---:|---:|---:|---:|---:|
| 1,594 cones | 1,594 | 48 + 6 | 74.5 k | 77 k / 3.4 h | 0.090 / 7.97 mK |
| **all cones** | 6,169 (of 6,202; 33 non-finite-$T_b$ cones skipped) | 16 + 2 | 98.5 k | 84 k / 3.5 h | **0.087 / 7.71 mK** |

The all-cones preparation (`ebm21cm.data.mf_all_prep`) points at every raw lightcone, keeps the multi-field val/test cones and copies the normalization. The cache builder applies fno-21cm's $T_b$ cleaning per cone; on a pilot cone it matches the mirror-based cache exactly, $T_b$ to float16 rounding.

### 6.1 Physical suite (199 test cones)

Figures: [[Rhizome Neural Operator Figures#1. Head-to-head: Rhizome vs UFNO (§6.1)|head-to-head vs UFNO]], [[Rhizome Neural Operator Figures#2. Coherence vs small-scale power (§6.1)|coherence-power plane]].

| metric | **2-D, all cones** | 2-D, 1,594 cones | 3-D rhizome C (+warm restart) | fno `tbs+histtb` |
|---|---:|---:|---:|---:|
| \|Δτ_e\| / σ_Planck | 0.010 | **0.010** | 0.012 | 0.076 |
| \|Δz\| at x̄ = 0.25 / 0.5 / 0.75 | **0.012** / 0.010 / **0.008** | 0.012 / **0.009** / 0.011 | 0.013 / 0.011 / 0.011 | 0.026 / 0.017 / 0.016 |
| \|Δ duration\| | **0.018** | **0.018** | **0.018** | 0.044 |
| $x_\text{HI}$ PDF W1 active | **0.0095** | 0.0105 | 0.0156 | 0.0271 |
| partially-ionized fraction (truth 0.089) | 0.136 | **0.135** | 0.156 | 0.174 |
| b₁ pull | **0.99** | 1.21 | 1.35 | 2.28 |
| P_ε ratio | 0.954 | **0.960** | 0.945 | 0.793 |
| bubble W1 active (Mpc) | **0.56** | 0.64 | 0.69 | 1.21 |
| $x_\text{HI}$ power error large / mid / small $k$ | 0.019 / 0.057 / **0.168** | **0.006 / 0.052** / 0.169 | 0.029 / 0.116 / 0.223 | 0.119 / 0.175 / 0.311 |
| 1 − coherence, small $k$ | **0.096** | 0.104 | 0.151 | 0.174 |
| 3-D edge H1 ±2 Mpc / front width (Mpc, truth 2.77) | **0.106 / 3.89** | 0.109 / 3.92 | 0.131 / 4.38 | 0.147 / 6.17 |
| $T_b$ PDF W1 active (mK) | **0.79** | 0.84 | 1.06 | 1.19 |
| $T_b$ power ratio active, $k$ = 0.11 / 0.46 | 0.98 / 0.96 | **1.00 / 0.96** | 0.97 / 0.91 | 0.90 / 0.87 |
| $T_b$ PDF W1, pre-reionization (mK) | 0.36 | 0.52 | **0.31** | 0.45 |
| $T_b$ power deviation, pre-reionization, $k$ = 0.11 / 0.46 | +8.7σ / +24.8σ | +7.7σ / +24.8σ | **+1.5σ / +4.1σ** | +3.0σ / +12.8σ |

- **Against 3-D rhizome C, the 2-D model wins every $x_\text{HI}$ morphology metric:** W1 −39%, b₁ pull −27%, bubble W1 −19%, small-scale incoherence −36%, mid-scale power −51%, edge H1 −19% (P = 0.000 over 170 cones).
- **It also wins $T_b$ during reionization** (W1 −25%; power within 4% at all $k$).
- **τ_e, timing and duration tie with 3-D C.** With the history channels, both rhizome models are already 5–7× better than fno there.
- **On the coherence-vs-small-scale-power plane** (`runs/eval3d/ps_plane3d_best.png`) it sits far from every fno model: r(k>1) 0.90 vs 0.82–0.83 for the multi-field fno runs, power error 0.17 vs 0.31–0.34.

### 6.2 All cones vs 1,594 cones (paired, 199 test cones, identical slices)

| per-cone RMSE | 1,594 | all | median Δ | mean Δ (95% CI) | better on | Wilcoxon p |
|---|---:|---:|---:|---:|---:|---:|
| $x_\text{HI}$ full cone | 0.0318 | **0.0308** | −3.6% | −5.6% (−7.5, −3.7) | 86% | 1.5e-20 |
| $T_b$ full cone (mK) | 4.15 | **3.96** | −5.5% | −6.3% (−7.7, −4.8) | 75% | 2.1e-15 |
| $x_\text{HI}$ active slices | 0.0877 | **0.0853** | −3.0% | −4.0% (−5.4, −2.5) | 85% | 4.1e-15 |
| $T_b$ active slices (mK) | 8.74 | **8.47** | −2.4% | −2.2% (−3.8, −0.6) | 74% | 1.0e-8 |
| $T_b$ pre-reionization (mK) | 3.03 | **2.85** | −7.1% | −7.1% (−8.8, −5.2) | 71% | 3.5e-12 |

The earliest reionizer (cone 27, z_mid ≈ 16), the weak case of every model,
gains most: full-cone $x_\text{HI}$ RMSE 0.072 -> 0.064. Each model is a single
seed.

### 6.3 Absorption-era $T_b$: a structural limit of slice-wise prediction

- **What's wrong:** before reionization (x̄_HI ≥ 0.98) the slice-wise model has much more small-scale $T_b$ power than the truth, +25σ at $k$ = 0.46. The 3-D rhizome is at +4σ and fno at +13σ.
- **In the maps:** the $T_b$ slices at z ≈ 12–14 show a fine-grained error pattern.
- **More data did not fix it.** Training on 3.9× more cones improved the absorption-era $T_b$ values (W1 0.52 -> 0.36 mK, close to 3-D C's 0.31; RMSE −7%) but left the excess power unchanged (+24.8σ). So it is not a data-variance effect.
- **Where the excess sits.** The power deviation is a per-slice average of (P_pred − P_true)/(P_true·√(2/N_modes)). Without smoothing, the cone-summed power ratio is in fact slightly *low* (0.97 at $k$ = 0.46) while the deviation is +25σ. So the excess is concentrated in quiet absorption-era slices whose true small-scale $T_b$ power is tiny: per-slice scatter in u is large relative to it there, even though it barely changes the total power.
- **Working hypothesis:** u ($T_\text{CMB}/T_S$) is predicted per slice with nothing in the loss that sees slice-to-slice or small-scale power consistency; the 3-D model predicts it jointly along the LOS.

**Test 1: smoothing u along the LOS at reassembly** (no retraining; Gaussian σ in native cells; T_b-only suite, 199 cones; `runs/eval3d/smooth_u_test/`):

| pre-reionization metric | σ = 0 | 2 | 4 | 8 | 16 | 3-D rhizome C |
|---|---:|---:|---:|---:|---:|---:|
| power deviation, $k$ = 0.46 | +24.8σ | +7.5σ | **+1.1σ** | −2.0σ | −3.9σ | +4.1σ |
| cone-summed power ratio, $k$ = 0.46 | **0.97** | 1.23 | 1.34 | 1.43 | 1.47 | 1.00 |
| $T_b$ PDF W1 (mK) | **0.36** | 0.48 | 0.59 | 0.68 | 0.70 | 0.31 |
| median per-cone $T_b$ RMSE, all slices (mK) | **2.66** | 4.33 | 5.08 | 5.72 | 6.22 | |

- **Smoothing suppresses the per-slice scatter, but u has real fine LOS structure:** even σ = 2 (≈3 Mpc) costs 42% in $T_b$ RMSE.
- **Because $1-e^u$ is nonlinear, averaging u shifts the mean $T_b$** and inflates the summed power (ratio 1.2–1.5).
- **Every reionization-stage $T_b$ metric also degrades** (active W1 0.80 -> 1.04 mK at σ = 4).
- **Rejected as a fix.**

**Test 2: LOS context to ±128 cells** (§6.6): the excess grew to +36σ (W1 0.50 mK). Wider bands seem to give u more inputs to vary on per slice.

Figures: [[Rhizome Neural Operator Figures#4. Absorption-era $T_b$ tests (§6.3, §6.6)|absorption-era tests]].

**Conclusion:** the excess is not data-limited (more cones), not removable post hoc (smoothing), and not a lack of context (wide bands). **Test 3, a loss term on the per-slice relative small-scale $T_b$ power error, removes it** (§6.7). The excess was a property of the training objective: per-pixel losses alone leave the per-slice spin factor unconstrained in quiet slices.

### 6.4 Mode-weight diagnostic (spectral bias)

Per-mode RMS of the learned Fourier kernel, relative to its initialization
(`ebm21cm/mode_weights.py`, the 2-D analogue of [[SirenFNO Spectral Bias Investigation]]):

| model | high/low-quarter weight ratio | low-25% share / flat share |
|---|---:|---:|
| multi-field 2-D (all / 1,594 cones) | 0.80 / 0.82 | 1.17 / 1.15 |
| x_HI 2-D w64 / w128 (fair split) | 0.85 / 0.78 | 1.13 / 1.19 |
| sweep, modes 12 / 24 / 36 / 48 | 0.94 / 0.93 / 0.88 / 0.78 | 1.04–1.16 |
| U-FNO, 32 modes (SirenFNO note) | 0.10–0.45 | ≈ 2.1 |

- **No low-frequency collapse.** Weights grew 13–45× over initialization nearly evenly up to the band edge.
- **Extra modes are used when available:** 36 and 48 modes stay flat out to 1.1 and 1.5 Mpc⁻¹. So the worse 48-mode sweep result (0.1177) is under-training or overfitting at 15k steps, not unused modes.
- **The kernels are stronger along the $k_x$, $k_y$ axes and the 45° diagonals,** the mirror lines of the dihedral training augmentation.
- **What it means for SIREN:** a SIREN-generated kernel would not correct a spectral bias here. It remains only a compact way to extend the band beyond 0.72 Mpc⁻¹. Full-budget 36/48-mode runs are the cheaper first test.

Figures: [[Rhizome Neural Operator Figures#3. Mode-weight diagnostic (§6.4)|mode-weight maps]].

### 6.5 Constant $T_b$ offsets per slice

Each slice's $T_b$ error was split into a constant offset (prediction mean − truth
mean over the 140×140 slice) and the remaining fluctuation error
(`runs/probes/tb_offset.py`, 199 test cones):

| stage | model | $T_b$ RMSE | offset RMS | offset share of MSE |
|---|---|---:|---:|---:|
| pre-reionization (x̄ ≥ 0.98) | 2-D all cones | 2.86 mK | 1.64 mK | 33% |
| | 2-D wide (±128) | 2.91 | 1.69 | 34% |
| | 3-D rhizome C | 3.09 | 1.80 | 34% |
| | fno `tbs+histtb` | 3.72 | 2.02 | 30% |
| late heating (0.8–0.98) | 2-D all cones / 3-D C / fno | 6.54 / 8.11 / 8.83 | 2.73 / 2.84 / 3.02 | 17 / 12 / 12% |
| reionization (0.05–0.8) | 2-D all cones / 3-D C / fno | 10.15 / 12.24 / 13.29 | 3.29 / 3.92 / 4.30 | 10–11% |

- **The offset is real and large before reionization,** but it is **not a systematic bias.** The median offset over cones is < 0.4 mK at every redshift; each cone over- or undershoots its global $T_b$ level by a random amount. (The wide model adds a small +0.1–0.5 mK positive bias at z = 9–25, possibly from its wide history bands near the padded cone ends.)
- **All three model families share nearly the same offset size.** The global $T_b$ level is set by the parameters through the integrated history, which the models receive as the emulated $T_b$ history. That emulator's own error on the multi-field test cones is ≈ 2.1 mK RMS, so the offset looks information-limited rather than loss-limited. $T_b$ is already trained with L2 (MSE); BCE is used only for $x_\text{HI}$.
- **Levers:** a better $T_b$ history emulator, or a dedicated slice-mean correction head with its own loss term.

### 6.6 Wide LOS context (±128 cells)

Six extra density bands (±32–64, ±64–96, ±96–128 cells) as image channels and the
same wide band means of both histories as scalars (32 channels / 50 scalars;
otherwise identical: all cones, 16+2 slices, same hyperparameters; 68 k steps,
2.9 h). 199 test cones:

| metric | **2-D all cones (±32)** | 2-D wide (±128) |
|---|---:|---:|
| \|Δ duration\| | 0.018 | **0.011** |
| bubble W1 active (Mpc) | 0.56 | **0.52** |
| $x_\text{HI}$ power error, large $k$ | 0.019 | **0.013** |
| 3-D edge H1 ±2 Mpc | **0.106** | 0.108 (P = 1.000 in favour of ±32) |
| 1 − coherence, small $k$ | **0.096** | 0.100 |
| $T_b$ W1 late heating (mK) | **0.82** | 0.88 |
| pre-reionization power deviation, $k$ = 0.46 | **+24.8σ** | +36.0σ |

- **Per voxel there is no significant difference.** Paired over 199 cones: $x_\text{HI}$ p = 0.44, $T_b$ p = 0.07. Pre-reionization $T_b$ is slightly worse (+2%, p = 0.008).
- **Gains:** the longer view pins down the reionization duration (−37%), with small gains in bubble sizes and large-scale power.
- **Losses:** absorption-era $T_b$ and, marginally, the edges.
- **Not adopted;** the ±32-cell model remains the best variant.

### 6.7 Small-scale $T_b$ power loss

Loss += λ · mean over slices and 8 log-spaced bins ($k$ = 0.3 Mpc⁻¹ to the grid
Nyquist) of $(\log(P_\text{pred}+\epsilon) - \log(P_\text{true}+\epsilon))^2$,
on the transverse power of mean-subtracted normalized $T_b$ ($\epsilon$ = 1e-6;
`train_rhizome_mf2d.PowerLoss`). Everything else is identical to the all-cones
model.

- **Calibration on the plain model** (256 validation slices), mean log(P_pred/P_true):
  - before reionization **+0.75** (2.1× too much power);
  - late heating −0.10;
  - during reionization −0.46 (blurred fronts).
- **Choice of weight:**
  - λ = 0.03: 92 k steps, 3.9 h; small-scale power error 0.19 vs ≈0.57 for the plain model.
  - λ = 0.1: 30% worse combined score with no better power error; stopped.

**Suite, 199 test cones** (`runs/eval3d/slicewise2d_mf_power_loss/`):

| metric | **2-D power loss λ = 0.03** | 2-D all cones (plain) | 3-D rhizome C |
|---|---:|---:|---:|
| pre-reion. $T_b$ power deviation, $k$ = 0.11 / 0.20 / 0.46 | **+0.9 / +1.0 / +1.5σ** | +8.7 / +13.6 / +24.8σ | +1.5 / +2.4 / +4.1σ |
| pre-reion. summed power ratio, $k$ = 0.46 | **0.997** | 0.974 | 0.996 |
| pre-reion. $T_b$ PDF W1 (mK) | 0.35 | 0.36 | **0.31** |
| active $T_b$ power ratio, $k$ = 0.11 / 0.46 | **0.99 / 0.98** | 0.98 / 0.96 | 0.97 / 0.91 |
| active $T_b$ power deviation, $k$ = 0.46 | **−0.07σ** | −0.44σ | −0.86σ |
| active $T_b$ PDF W1 (mK) | **0.77** | 0.79 | 1.06 |
| \|Δτ_e\| / σ_Planck | **0.008** | 0.010 | 0.012 |
| \|Δz(x̄ = 0.5)\| / duration | 0.010 / 0.018 | 0.010 / 0.018 | 0.011 / 0.018 |
| $x_\text{HI}$ PDF W1 active / b₁ pull | 0.0098 / **0.93** | **0.0095** / 0.99 | 0.0156 / 1.35 |
| bubble W1 active (Mpc) | **0.48** | 0.56 | 0.69 |
| $x_\text{HI}$ power error large / mid / small $k$ | **0.016** / **0.057** / **0.163** | 0.019 / **0.057** / 0.168 | 0.029 / 0.116 / 0.223 |
| 1 − coherence, small $k$ | 0.102 | **0.096** | 0.151 |
| 3-D edge L2 / H1 ±2 Mpc | 0.179 / 0.112 | **0.172 / 0.106** | 0.209 / 0.131 |
| front width (Mpc, truth 2.77) | 3.94 | **3.89** | 4.38 |

**Paired per-voxel accuracy vs the plain model** (199 cones, identical slices):

| per-cone RMSE | plain | power loss | median Δ | power loss better on | Wilcoxon p |
|---|---:|---:|---:|---:|---:|
| $x_\text{HI}$ full cone | 0.0308 | 0.0318 | +5.5% | 8% | 4e-30 |
| $T_b$ full cone (mK) | 3.96 | 4.22 | +6.8% | 17% | 5e-23 |
| $T_b$ pre-reionization (mK) | 2.85 | 3.09 | +7.3% | 22% | 2e-17 |

- **The power loss is a standard perception-vs-distortion trade.** Per-pixel losses favour slightly smoothed fields; the power term enforces realistic small-scale structure at a small cost in pixel accuracy.
- **It fixes the absorption-era excess at every scale without amplitude overshoot.** It also corrects the reionization-era under-power and improves bubble sizes, τ_e and the bias.
- **Costs:** pixel RMSE, edges (H1 +0.006, P = 1.000 for the plain model) and slightly lower small-scale coherence.
- **Constant $T_b$ offsets are unchanged** (1.77 mK RMS, 33% of pre-reionization MSE): the term acts only on fluctuations (§6.5).

### 6.8 Small-scale $x_\text{HI}$ power loss

The same `PowerLoss` term (λ = 0.03, $k \ge 0.3$ Mpc⁻¹, 8 log bins) applied to the
$x_\text{HI}$ probability (sigmoid output), on top of the $T_b$ term of §6.7
(`--xhi-power-weight 0.03`). Motivation: in the plain model the high-k $x_\text{HI}$
power is low during reionization (mean log(P_pred/P_true) −0.16 … −0.92 from
$k$ = 0.3 Mpc⁻¹ to Nyquist, 256 validation slices). Training: 94 k steps, 4.2 h
A100; validation $x_\text{HI}$ power log error 0.88 at 1 k steps -> 0.19.

**Suite, 199 test cones** (`runs/eval3d/slicewise2d_mf_xhi_power_loss/`):

| metric | **+ $x_\text{HI}$ power** | $T_b$ power only (§6.7) | plain | 3-D rhizome C |
|---|---:|---:|---:|---:|
| $x_\text{HI}$ power-ratio error, $k>1$, x̄ 0.02–0.20 / 0.20–0.40 / 0.40–0.60 / 0.60–0.80 | **0.15 / 0.26 / 0.28 / 0.20** | 0.59 / 0.50 / 0.45 / 0.30 | 0.68 / 0.55 / 0.45 / 0.30 | 0.71 / 0.60 / 0.52 / 0.36 |
| $x_\text{HI}$ power-ratio error, $k>1$, active | **0.089** | 0.163 | 0.168 | 0.223 |
| 1 − coherence, $k>1$, active / x̄ 0.02–0.20 | 0.109 / 0.566 | 0.102 / 0.519 | **0.096 / 0.472** | 0.151 / 0.608 |
| $x_\text{HI}$ PDF W1 active | **0.0082** | 0.0098 | 0.0095 | 0.0156 |
| partially-ionized fraction (truth 0.089) | **0.128** | 0.136 | 0.136 | 0.156 |
| pre-reion. $T_b$ power deviation, $k$ = 0.11 / 0.20 / 0.46 | **+0.4 / +0.8 / +1.3σ** | +0.9 / +1.0 / +1.5σ | +8.7 / +13.6 / +24.8σ | +1.5 / +2.4 / +4.1σ |
| active $T_b$ PDF W1 (mK) | 0.91 | **0.77** | 0.79 | 1.06 |
| \|Δτ_e\| / σ_Planck | 0.009 | **0.008** | 0.010 | 0.012 |
| 3-D edge H1 ±2 Mpc / front width (Mpc, truth 2.77) | 0.114 / 3.90 | 0.112 / 3.94 | **0.106 / 3.89** | 0.131 / 4.38 |

**Paired per-voxel accuracy** (199 cones, identical slices; every difference Wilcoxon p < 1e-5):

| per-cone RMSE | vs $T_b$ power only, median Δ | vs plain, median Δ |
|---|---:|---:|
| $x_\text{HI}$ full cone / active slices | +2.6% / +4.2% | +8.2% / +8.2% |
| $T_b$ full cone / active slices (mK) | +2.5% / +1.8% | +9.3% / +7.6% |
| $T_b$ pre-reionization (mK) | +1.8% | +9.2% |

- **The high-k $x_\text{HI}$ amplitude is what the term fixes:** the power deficit roughly halves at every reionization stage (the latest stage 0.59 -> 0.15) and the value distribution becomes the closest of all models.
- **Coherence slips slightly** (small-scale 1 − r +7% over active slices): the extra power is only partly in phase with the truth. The same perception-distortion trade as §6.7.
- **The absorption-era $T_b$ fix survives** and is marginally better (+1.3σ).
- **Costs:** 2–4% per-voxel RMSE on top of the $T_b$ power loss (8–10% vs the plain model in total), reionization-era $T_b$ W1 +18%, edges +2%.
- **Which model to use:** plain for per-voxel accuracy; both power terms for the most realistic small-scale structure in both fields; $T_b$-only in between.

Figures: [[Rhizome Neural Operator Figures#5. Power-loss variants (§6.7, §6.8)|power-loss variants]].

### 6.9 Compact real-space kernel (radius sweep)

**Question:** the Fourier kernel costs ~N log N per channel, a full real-space
integral N². Can a kernel restricted to a disc of radius R cells around each site,
κ(d) = 0 for |d| > R, match the Fourier kernel, and how large must R be?

**Setup:**
- `LocalConv2d` (`ebm21cm/model/rhizome.py`): a periodic disc of integer offsets, with either a dense C×C channel-mixing matrix per offset or, with `rank=r`, K(d) = P_out diag(w(d)) P_in (r spatial filters).
- After T = 6 updates a site sees at most 6R cells (1 cell = 1.43 Mpc).
- Otherwise identical to the plain all-cones model (width 64, T = 6, BCE + $T_b$ MSE, plateau-stopped).

**Cost** (`ebm21cm/bench_kernel_radius.py`, A100, cuDNN autotuned; training step at batch 32, inference at batch 128):

| kernel | offsets | kernel params | training step | inference |
|---|---:|---:|---:|---:|
| **Fourier, modes 24** | — | 9.05 M | 137 ms | 714 slices/s |
| R = 1 / √2 | 5 / 9 | 20–37 k | 126 ms | 835 slices/s |
| R = 2 – 2√2 | 13–25 | 53–102 k | 146 ms | 750 slices/s |
| R = 3 / 4 / 6 | 29 / 49 / 113 | 119 / 201 / 463 k | 177 / 208 / 310 ms | 623 / 526 / 366 slices/s |
| R = 2 / 4 / 8, rank 16 | 13 / 49 / 197 | 2–5 k | 126 / 141 / 199 ms | 852 / 789 / 669 slices/s |

- In arithmetic a dense local kernel costs C²·n per pixel, while the Fourier kernel costs ~C·N log N plus C² per retained mode. So R = 1 already does 6× the Fourier kernel's operations.
- On the GPU, the 1×1 gate/update convolutions dominate the step, so the kernels break even at R ≈ 2.8 (dense) or R ≈ 4 (rank 16).
- Without cuDNN autotuning, R = 3–6 ran up to 2× slower.

**Accuracy** (best validation score; lower is better):

| kernel | reach (6 updates) | val score | vs Fourier | test $x_\text{HI}$ / $T_b$ RMSE | training time |
|---|---:|---:|---:|---:|---:|
| **Fourier, modes 24** | whole slice | **0.02136** | — | **0.0872 / 7.71 mK** | **3.6 h** |
| R = 1 | 9 Mpc | 0.0347 | +62% | 0.121 / 9.76 | 2.8 h |
| R = 2 | 17 Mpc | 0.0290 | +36% | 0.109 / 8.85 | 3.8 h |
| R = 3 | 26 Mpc | 0.0254 | +19% | 0.101 / 8.27 | 4.4 h |
| R = 4 | 34 Mpc | 0.0242 | +13% | 0.097 / 8.10 | 5.2 h |
| R = 6 | 51 Mpc | 0.0239 | +12% | 0.095 / 8.13 | 7.7 h |
| R = 8, rank 16 | 69 Mpc | 0.0228 | +6.5% | 0.093 / 8.04 | 4.6 h |

- **No radius matches the Fourier kernel.** The gap levels off at +12–13% for R = 4–6 at 1.5–2× the training time.
- **At equal cost (R ≈ 2–3) the local kernel is 19–36% worse;** every local kernel within 15% costs more time than the Fourier one.
- **Reach beats channel mixing:** the rank-16 kernel at R = 8 (16 spatial filters, 5 k parameters) beats dense R = 4–6 (64×64 per offset).
- Ionization depends on photon budgets over regions of up to tens of Mpc (excursion-set radii 1–20 Mpc). The Fourier kernel reaches the whole 200 Mpc slice in one update; a few global modes are worth more than any affordable stencil.
- The Fourier model's 9 M kernel parameters are not the explanation either: the dense local models with 0.1–0.5 M parameters do no better than the 5 k-parameter rank-16 one.

### 6.10 Number of updates T

The short 2-D sweep (§2, 15 k steps) put T = 3 / 6 / 10 within 3% of each other, with the
integration time T × step size (step size 0.5) mattering more than T itself. To convergence on the
multi-field all-cones setup (full Fourier kernel, step size 0.5):

| T | seed | val score | test $x_\text{HI}$ / $T_b$ RMSE | steps | training time |
|---:|---:|---:|---:|---:|---:|
| 3 | 0 | **0.02098** | 0.0866 / 7.68 mK | 98 k | **2.2 h** |
| 6 | 0 | 0.02136 | 0.0872 / 7.71 | 84 k | 3.6 h |
| 6 | 1 | 0.02136 | 0.0873 / 7.82 | 74 k | 3.1 h |
| 10 | 0 | **0.02098** | 0.0869 / 7.66 | 71 k | 4.9 h |
| 1 | 0 | 0.02268 | 0.0897 / 8.05 | 72 k | 0.7 h |
| 1 (Δt = 1.0) | 0 | 0.02206 | 0.0885 / 7.97 | 77 k | 0.8 h |
| 2 | 0 | 0.02165 | 0.0881 / 7.86 | 96 k | 1.6 h |

- **Below T = 3 the error rises, but only slightly.**
  - T = 2 costs 1–2% in test RMSE (+3% validation); T = 1 costs 3–4% (+8%).
  - One full update (T = 1, Δt = 1: the state is replaced by a single proposal, no recurrence) beats one damped update but loses to two damped updates with the same integration time T·Δt = 1. So the recurrence itself adds a few percent.
  - Even a single gated global update is within 5% of the best rollout.
- **T makes no material difference between 3 and 10:** T = 3 and T = 10 tie at −1.8% on validation. On test they are within the spread between the two T = 6 seeds ($T_b$ 7.71 vs 7.82 mK).
- **The two T = 6 seeds agree to five digits on validation,** so seed noise in the validation score is far below the 1–2% differences here.
- **T = 3 is the cheaper choice:** same accuracy at ~60% of the training time and half the forward cost per slice.
- **The number of updates is part of the trained model:** run past their T, the models degrade (§6.16).

### 6.11 Global-history ablation

The 38 scalars include 13 LOS band means each of the emulated global $x_\text{HI}$ and $T_b$
histories. `--drop-history xhi|tb` removes one set (25 scalars kept); otherwise identical to the
plain all-cones model (both histories).

| inputs | val score | test $x_\text{HI}$ / $T_b$ RMSE |
|---|---:|---:|
| **both histories** | **0.02136** | **0.0872 / 7.71 mK** |
| no $x_\text{HI}$ history | 0.02453 (+15%) | 0.0973 (+12%) / 8.26 (+7%) |
| no $T_b$ history | 0.02178 (+2%) | 0.0900 (+3%) / 8.04 (+4%) |

Cylindrical power at native LOS resolution (§6.12), share of (k⊥, k∥) cells within ±0.1, z ≈ 7 / 9 / 11 / 14 / 17:

| inputs | $x_\text{HI}$ | $T_b$ |
|---|---|---|
| both histories | 90 / 79 / 78 / 92 / 57% | 88 / 83 / 79 / 73 / 4% |
| no $x_\text{HI}$ history | 79 / 64 / 41 / 30 / 83% | 85 / 78 / 54 / 35 / 25% |
| no $T_b$ history | 93 / 85 / 82 / 68 / 50% | 89 / 84 / 84 / 51 / 6% |

- **The $x_\text{HI}$ history carries most of the global information.** Without it both fields lose 10–30% of their small-scale power at z ≈ 11–14 (high k⊥ and high k∥), and $x_\text{HI}$ gains a large-scale excess at z ≈ 17.
- **The $T_b$ history matters mainly around z ≈ 14** (late heating), where its absence leaves a broad $T_b$ excess at low-to-mid k⊥.
- **Neither history touches the absorption-era excess** at z ≈ 17 (4–6% of cells within ±0.1); that took the power loss (§6.7).

Figures: [[Rhizome Neural Operator Figures#8. Cylindrical power at native LOS resolution (§6.11, §6.12)|history ablation maps]].

### 6.12 Cylindrical power at native LOS resolution

**Why:** fno-21cm's cylindrical maps are computed on the 512-point evaluation cubes
(uniform in z, Δz = 0.039). Their LOS cells are 13.7 / 9.8 / 7.5 / 5.4 / 4.1 Mpc at z ≈ 7 / 9 / 11 / 14 / 17, against 1.43 Mpc natively. So k∥ only reached 0.23–0.77 Mpc⁻¹ while k⊥ reached 2.2 Mpc⁻¹, and small-scale LOS errors were invisible.

**How** (`ebm21cm/native_cyl.py`, accumulated by both exporters, `--native-cyl`):
- 140 native slices (200 Mpc) per chunk around each redshift, so k∥ spans the same 0.031–2.2 Mpc⁻¹ as k⊥.
- fno-21cm's procedure otherwise: per-slice mean removed, Hann window along the LOS, per-cone ratio, median over the 199 test cones.
- k⊥ in 15 log bins, k∥ one row per LOS frequency.
- The 2-D exporters predict only the chunk slices; UFNO's 3-D export predicts full native cones.
- Every model saw identical truth (per-cone true power equal to 1e-7).
- A test checks the chunk sums against fno-21cm's own `_cylindrical_sums`.

**Share of (k⊥, k∥) cells within ±0.1**, z ≈ 7 / 9 / 11 / 14 / 17:

| model | $x_\text{HI}$ | $T_b$ |
|---|---|---|
| UFNO | 19 / 8 / 12 / 21 / 34% | 60 / 76 / 72 / 52 / 34% |
| Rhizome (plain) | 90 / 79 / 78 / 92 / 57% | 88 / 83 / 79 / 73 / 4% |
| + $T_b$ power loss | 84 / 76 / 66 / 44 / 53% | **100 / 100** / 94 / **91** / 60% |
| + $T_b$ and $x_\text{HI}$ power loss | **91 / 94 / 100 / 100 / 99%** | **100** / 99 / **95** / 88 / **69%** |

The shares count each cell once. With one row per LOS frequency most cells sit at high k∥, so they weight small LOS scales heavily.

- **UFNO smooths along the LOS.** Its $x_\text{HI}$ and $T_b$ power falls off at k∥ ≳ 0.5 Mpc⁻¹ at every redshift (to −0.4), on top of its known high-k⊥ deficit. The 512-grid maps stopped below this.
- **The slice-wise rhizome has no comparable LOS problem.** The plain model loses $x_\text{HI}$ power only in the top rows (k∥ ≳ 1.5–2 Mpc⁻¹) and at the highest k⊥. Slice-by-slice prediction neither adds LOS jitter nor loses much LOS structure.
- **Both power terms together give nearly perfect $x_\text{HI}$ power at all (k⊥, k∥),** although the loss acts only on transverse spectra.
- **The $T_b$-only power loss worsens $x_\text{HI}$ at z ≈ 14–17** (a high-k∥ deficit, then a broad excess); adding the $x_\text{HI}$ term removes both.
- **Absorption-era $T_b$ (z ≈ 17) is still the hardest case.** The power-loss models are 60–69% within ±0.1, with the remaining excess in a band at k∥ ≈ 0.5–1 Mpc⁻¹.
- **Open:** UFNO shows a thin excess in the single highest-k∥ row at z ≈ 7, 9 and 17, possibly from its tiled-window inference; not checked.

Figures: [[Rhizome Neural Operator Figures#8. Cylindrical power at native LOS resolution (§6.11, §6.12)|native cylindrical maps]].

### 6.13 Gating mechanism on real slices

What the trained model does with its state-dependent gates. For a receiver cell i,
the re-weighting of its incoming connections by the gates at update t is

$$M_t(j) = \frac{\|\mathrm{diag}(A_i)\,\kappa(r_i - r_j)\,\mathrm{diag}(B_j)\|_F}{\|\kappa(r_i - r_j)\|_F},$$

with A the receiver and B the source gates (channel-wise, in (0, 2)) and κ the
trained Fourier kernel (impulse response, so the model's own weights). It is shown
relative to its mean over j, and its mean is the "gain".

**What M_t is not:** a gain on the transmitted value, not a Jacobian of the output. Each model is a single network.

**Code:**
- `ebm21cm/mechanism_mf.py`: single-slice maps, the multi-field port of `scripts/make_rhizome_mechanism.py`.
- `ebm21cm/mechanism_avg.py`: radial averages.

**Single slices** (4 test slices at x̄_HI ≈ 0.2 / 0.4 / 0.6 / 0.8, receiver on a front, both models):
- **Receiver gate:** opens in ionized gas, channel-RMS 0.37–0.44 vs 0.14–0.21 in neutral cells for the plain model, about 2× in every slice.
- **Source gate:** nearly uniform (0.8–1.1).
- **Bare kernel:** sharply peaked.
- **The ring at 7–10 cells** seen in the power-loss model's maps did not survive averaging (below).

**Averaged** over 120 test slices (x̄_HI 0.1–0.9, one per cone) and 7,217 receivers per model (3,808 front, 1,920 neutral-interior and 1,489 ionized-interior cells, interior = more than 4 cells from the other phase):

| t = 6, mean M_t(j)/⟨M_t⟩ | plain | both power terms |
|---|---|---|
| front: peak / half-width | 2.0× at the centre / 14 Mpc | 3.5× at the centre / 9 Mpc |
| neutral interior | 2.3× / 5 Mpc | 3.8× / 8 Mpc |
| ionized interior | 1.7× at 5 Mpc / 24 Mpc | 2.3× at 5 Mpc / 18 Mpc |
| bare kernel ‖κ‖ | half at 3.6 Mpc, 10% at 11 Mpc | half at 3.6 Mpc, 10% at 14 Mpc |
| mean gain, front, t = 1 -> 6 | 0.19 -> 0.09 | 0.36 -> 0.17 |
| mean gain, ionized interior, t = 1 -> 6 | 0.28 -> 0.32 | 0.42 -> 0.42 |

Half-width: the distance at which the boost above 1 has fallen to half its maximum. The boost reaches 1.0 only beyond about 40 Mpc.

- **The gates extend the kernel's reach** from a few Mpc to 10–25 Mpc, the range of the excursion-set ionizing radii (1–20 Mpc). Ionized cells collect from the furthest (≈ 20 Mpc), cells deep in neutral gas from the nearest (5–8 Mpc).
- **No average ring at fronts.** The boost peaks at the receiver. A radius-dependent peak appears only for ionized-interior cells (5–9 Mpc, both models) and for the plain model's front cells at middle updates (2.2× at 9 Mpc at t = 3, gone by t = 6).
- **Ionized regions keep collecting.** Their receiver gate opens further over the updates (plain 0.34 -> 0.46) and their gain holds. Front and neutral cells settle after 2–3 updates.
- **Stage dependence:** the plain model's front boost grows and narrows as x̄ rises (1.6× / 24 Mpc at x̄ 0.1–0.4 to 2.2× / 9 Mpc at 0.6–0.9). The power-loss model's is nearly constant (3.3–3.6×, 8–9 Mpc).
- **The power-loss model gates about twice as strongly** (gains and receiver gates ~2×) and more locally at fronts. That fits its sharper, more structured fronts.
- **Artifact:** the 3–4 Mpc zigzag in the profiles and the cross-shaped stripes in the maps come from the truncated kernel's sidelobes along the grid axes. Dividing by a small ‖κ‖ amplifies them.

Figures: [[Rhizome Neural Operator Figures#9. Gating mechanism (§6.13)|gate maps and averages]].

### 6.14 Gate ablation: frozen gates

The primary contrast of the planned gate study. `--gate-mode frozen` computes the source and receiver gates once from the initial state $[h^0, c] = [\tanh c, c]$ and holds them over all T = 6 updates. The transmitted value V still follows the evolving state. Because $h^0$ is a function of c, this coincides with "gates from the conditioning only". Otherwise identical to the plain all-cones model; both seeds trained.

| | val score | test $x_\text{HI}$ RMSE | test $T_b$ RMSE |
|---|---:|---:|---:|
| full gates, seed 0 / 1 | 0.02136 / 0.02136 | 0.0872 / 0.0873 | 7.71 / 7.82 mK |
| frozen gates, seed 0 / 1 | 0.02188 / 0.02178 | 0.0886 / 0.0888 | 7.86 / 7.93 mK |
| difference, paired by seed | +2.4% / +2.0% | +1.6% / +1.7% | +1.9% / +1.4% |

- **Updating the gates as the state evolves is worth about 2%,** consistent across both seeds. That is well above the validation seed spread (the full-gate seeds agree to five digits) and at about the level of the test seed spread (1.4% in $T_b$).
- **What the contrast does not measure:** frozen gates still vary across the slice and still multiply the kernel at both ends ($A_i\kappa B_j$, computed from each cell's inputs). So the value of the gating itself is still open.
- **Why that matters:** the global kernel and the inputs cannot explain the rhizome's advantage over fno on their own, because the fno/U-FNO models also have global spectral kernels and the same inputs. A density-only 3-D rhizome (A0) already beat fno's best multi-field model (§4.1). Candidates that full and frozen gates share and fno lacks:
  - the multiplicative, input-dependent gating of the kernel;
  - the recurrent rollout with the conditioning re-injected at every update (§6.10 puts the recurrence at a few percent);
  - BCE on $x_\text{HI}$ (explains the τ_e / global-history offset, §4.3, not the morphology).
- **Remaining arms, implemented** (`--gate-mode none|source|receiver|static`): no gates (A = B = 1, the decisive one), source-only, receiver-only, static per-channel gates.

### 6.15 Two-level rhizome

`RhizomeUNet2d` (`--coarse-factor 4`):
- **Coarse level:** the conditioning is average-pooled 4× (140² -> 35², 5.7 Mpc cells), lifted with its own scalar embedding and rolled out for 3 updates with its own kernel.
- **Merge:** the coarse state is upsampled (periodic bilinear) and merged pointwise into the full-resolution forcing.
- **Fine level:** 3 full-resolution updates, then decoding.
- **Properties:** exact equivariance under periodic shifts by multiples of 4 cells.
- **Kernels:** spectral (24 modes at full resolution, all 17 at 35²) or compact.
- **Motivation:** compact kernels lose on reach (§6.9), while the 24-mode spectral kernel cannot represent couplings below ~8.6 Mpc.
- **Reference:** the single-level model with T = 3.

| full resolution / coarse level | params | val score | test $x_\text{HI}$ / $T_b$ RMSE | test power error $T_b$ / $x_\text{HI}$ |
|---|---:|---:|---:|---:|
| single level, spectral, T = 3 | 4.57 M | 0.02098 | 0.0866 / 7.68 mK | 0.395 / 0.385 |
| A: spectral / compact R = 4 | 4.82 M | 0.02197 (+4.7%) | 0.0888 / 7.92 | 0.391 / 0.373 |
| B: spectral / spectral | 6.85 M | 0.02065 (−1.6%) | 0.0863 / 7.67 | 0.367 / 0.386 |
| **C: compact R = 2 / spectral** | **2.38 M** | **0.02036 (−3.0%)** | **0.0862 / 7.55** | **0.318 / 0.349** |
| D: compact R = 2 / compact R = 4 | 0.35 M | 0.02628 (+25%) | 0.1012 / 8.66 | 0.449 / 0.463 |
| *with both power terms:* single level, T = 6 | 4.57 M | 0.02381 | 0.0941 / 8.26 | 0.234 / 0.163 |
| B + both power terms | 6.85 M | 0.02395 (+0.6%) | 0.0939 / 8.43 | 0.220 / 0.125 |
| C + both power terms | 2.38 M | 0.02506 (+5.2%) | 0.0964 / 8.48 | 0.241 / 0.170 |

Params count complex weights once (the convention of the Rhizome-Notes report). Training ran on mixed GPUs (A on A100; B, C, D on A30; the power-loss runs on H200), so times are not comparable.

- **The coarse level must be spectral.** A compact kernel there (A) is 3–5% worse than single level. With compact kernels at both levels (D) the error rises by 13–25%, as for compact single-level kernels.
- **Spectral coarse level + compact fine level (C) is the best plain-loss model in this note:**
  - −3.0% validation score and −1.7% test $T_b$ RMSE vs the matched single-level model, at half the parameters;
  - the lowest power errors of the plain-loss models;
  - in the native-resolution maps, the only plain-loss model without a high-k $x_\text{HI}$ deficit during reionization: 92–99% of (k⊥, k∥) cells within ±10% at z ≈ 7–11, vs 78–90% single level;
  - but before reionization, C and A develop a broad $x_\text{HI}$ excess: 5–16% of cells within ±10% at z ≈ 17, vs 57%.

  This supports a division of labour by scale: global spectral coupling on the coarse grid, a small stencil for the couplings below the spectral cutoff.
- **B** (spectral at both levels) ties single level in test RMSE with 50% more parameters, and has the best $T_b$ maps of the plain models during reionization (85–95% of cells vs 73–88%).
- **With both power terms the advantage disappears.** B matches the single-level power-loss model in $x_\text{HI}$ and is 2% worse in $T_b$; C is 2–3% worse. Native maps: the single-level power-loss model stays best for $x_\text{HI}$ (91–100%); B and C drop to 41–93%. B is best for absorption-era $T_b$ (80% vs 69% at z ≈ 17). C's plain-loss gain was mainly recovering small-scale power, which the power terms supply anyway.

Figures: [[Rhizome Neural Operator Figures#10. Two-level rhizome and rollout dynamics (§6.15, §6.16)|two-level maps]].

### 6.16 Rollout beyond the trained length

Six checkpoints were run for 30 updates at inference on 512 validation slices (`ebm21cm/rollout_diagnostic.py`). After each update the diagnostic records:
- the relative state change $\|h_t-h_{t-1}\|/\|h_{t-1}\|$;
- the two-step change $\|h_t-h_{t-2}\|/\|h_{t-2}\|$;
- the cosine between successive changes $d_t = h_t-h_{t-1}$ and $d_{t-1}$;
- the validation score of the decoded state.

| model | score at T | at t = 30 | change at T / t = 30 | two-step at t = 30 | cos at T -> t = 30 |
|---|---:|---:|---:|---:|---|
| T = 3 | 0.0205 | 0.0778 (+280%) | 0.43 / 0.032 | 0.013 | +0.58 -> −0.45 |
| T = 6, seed 0 | 0.0209 | 0.0263 (+26%) | 0.13 / 0.026 | 0.008 | +0.64 -> −0.78 |
| T = 6, seed 1 | 0.0209 | 0.0295 (+42%) | 0.14 / 0.009 | 0.005 | +0.70 -> −0.16 |
| **T = 10** | 0.0206 | **0.0206 (flat)** | 0.028 / 0.013 | 0.003 | +0.00 -> −0.82 |
| T = 6, frozen gates | 0.0212 | 0.0223 (+5%) | 0.072 / 0.003 | 0.0001 | +0.62 -> −0.85 |
| T = 6, both power terms | 0.0233 | 0.0563 (+142%) | 0.15 / 0.057 | 0.044 | +0.65 -> −0.52 |

- **The models learn a transient.** Every model is best exactly at its trained T. At T the state still changes by 13–43% per update in a consistent direction (cosine +0.6 to +0.7), and for T ≤ 6 the prediction degrades when run further. The exception is T = 10: change only 3% at T, score flat to t = 30. With enough updates the model settles on a stable prediction.
- **A residual two-cycle.**
  - The state change does not decay to zero. Beyond ~15 updates it levels off at 1–6% per update for every model with state-dependent gates.
  - Successive changes turn anti-aligned (cosine down to −0.8), and the two-step change is 2–4× smaller than the one-step change: the state alternates between two configurations, plus some drift.
  - Frozen gates contract to 0.3%, a nearly pure two-cycle of negligible amplitude.
  - The power-loss model has the largest residual (5.7%).
- **Interpretation, an overshooting step:**
  - Linearized, a direction in which the proposal has slope λ is multiplied by 1 − Δt + Δt·λ per update. The oscillation stops decaying for λ < 1 − 2/Δt, i.e. λ < −3 at Δt = 0.5 and λ < −7 at Δt = 0.25.
  - The state-dependent gates create such strongly negative-slope directions; they are absent with frozen gates.
  - Within the trained horizon there is no oscillation, so the reported accuracies are unaffected. It matters for any reading of the rhizome as an iteration to equilibrium.
- **The earlier short sweep (§2) already hinted at this:** Δt = 1 (no damping) was the worst setting, and T = 6 at Δt = 0.25 matched T = 3 at Δt = 0.5.
- **Runs in progress:**
  - T = 12 at Δt = 0.25 (same T·Δt as the reference), to test whether a smaller step removes the two-cycle;
  - training with random T ∈ {3, …, 12} per batch (`--random-updates 3:12`, validated at 6), to test whether the decoder can be made independent of the rollout length.

  Both track the T = 6 reference within 1% at matched steps so far.

Figures: [[Rhizome Neural Operator Figures#10. Two-level rhizome and rollout dynamics (§6.15, §6.16)|rollout diagnostic]].

## 7. Cost

| model | GPU | training run | inference, one full cone (2,709 slices), A100 / H200 |
|---|---|---|---|
| 2-D w64 slice-wise | A100 | **2.8 h** | — |
| **2-D w64 multi-field slice-wise** (2,588 slices, x_HI + T_b) | A100 | 3.4 h (1,594 cones) / 3.5 h (all cones) | **5.5 s / 3.7 s end to end** (GPU forward 3.8 s / 1.7 s) |
| 3-D rhizome C (multi-field) | H200 | as 3-D rhizome w48 | 12.8 s / 8.3 s end to end (GPU forward 4.4 s / 1.8 s) |
| fno `tbs+histtb` (multi-field) | A100 | as fno `cnn_whno_es` | 9.8 s / 7.0 s end to end (GPU forward 2.0 s / 1.0 s) |
| 2-D w128 slice-wise | A100 | 5.0–6.5 h (92 slices/s) | 7.9 s + 3.2 s CPU bands / 4.0 s |
| 3-D rhizome w48 | H200 | ~12 h + 6 h restart (3.1 windows/s; A100 1.38, ~77 min/epoch) | 4.7 s / 1.9 s |
| fno `cnn_whno_es` | A100 | 44.7 h, 30 epochs (1.32 windows/s, ~81 min/epoch) | 2.1 s / 1.0 s |

- **The 2-D model is ~4× slower per slice in training**: width 128, float32, full-resolution recurrent updates.
- **It needs 15–20× fewer training slices** (2.2 M vs 33–49 M), so a whole run is 4–7× cheaper.
- **Multi-field inference, stage by stage** (`ebm21cm/bench_inference_mf.py`, cone 1751, float32, batch 128):
  - Reading the data windows takes 5.3 s on the A100 and 3.7 s on the H200 for every model.
  - Building the 2-D inputs (LOS bands, history band means, physical factor) took 15.7 s / 8.8 s on 8 CPU cores, which made end to end 24.8 s / 14.2 s.
  - On the GPU (`slice_inputs_gpu`) the input building takes 0.6 s / 0.1 s, giving 9.1 s / 5.2 s end to end.
  - With the next window prefetched in a background thread and each chunk predicted as soon as it is built, the whole cone is read-bound: **5.5 s / 3.7 s**. That is 1.8–2.3× faster end to end than both 3-D models.
  - The GPU inputs match the CPU path to float rounding. The prefetched export differs from the original by $x_\text{HI}$ RMS ≤ 1e-5 and $T_b$ ≤ 0.002 mK (TF32 convolution rounding with different batch splits).
- **The GPU forward alone** matches the 3-D rhizome and is about 2× slower than fno.
- **Batch size barely matters** (660–685 slices/s from 32 to 128); batch 32 needs 2.4 GiB.
- **Evaluation suite** (`ebm21cm/suite_cached.py`, behind `slurm/eval3d_suite.sbatch`):
  - The old suite was I/O-bound: 21 CPU-minutes in 2 h 22 min, re-reading ~38 GB of cubes per model in each of six sequential steps.
  - Now the per-model steps (physics, bubble sizes, power spectra) are cached next to each model's cubes, the steps run in parallel, and the duplicate x_HI pass is skipped in DTB mode.
  - A three-model $T_b$ suite takes 35 min uncached and 26 min with all models cached, with byte-identical outputs. The pairwise edge diagnostics (not cached) are now the floor.
- **bfloat16 is not worth it:** only +14% (A100) / +5% (H200) faster because the FFTs stay float32, and it shifts $x_\text{HI}$ by up to 0.08 and $T_b$ by 0.35 mK RMS.

## 8. Open items

- **Power-loss weight:** λ = 0.03 fixes the absorption-era excess at a 4–8% pixel cost (§6.7). A smaller λ (e.g. 0.01) or a power term restricted to pre-reionization slices might keep most of the gain for less cost. The same for the $x_\text{HI}$ term (§6.8), e.g. λ_x = 0.01.
- **Constant $T_b$ offsets** (§6.5): a better $T_b$ history emulator or a slice-mean correction head.
- **Wider kernel band:** full-budget 36/48-mode runs; SIREN only if those help (§6.4). A local real-space kernel is not an alternative (§6.9).
- **Gate arms:** no gates (A = B = 1), source-only, receiver-only, static gates (§6.14); implemented, not trained. "No gates" decides whether the gating is what separates the rhizome from fno.
- **Step size and rollout length:** Δt = 0.25 (T = 12) and random-T runs in progress (§6.16). Run the rollout diagnostic on both.
- **Two-level model:** C with a gentler power weight, or with only the $T_b$ term, might keep both the plain-loss gain and the power fix (§6.15).
- **T = 3 as the default:** same accuracy as T = 6 at ~60% of the training time (§6.10); not yet evaluated on the full suite.
- **UFNO's top-k∥ row excess** in the native maps (§6.12): check for a window-tiling artifact.
- **fno retrain with BCE on $x_\text{HI}$**, to separate the loss effect (§4.3) from the operator.
- **Single seeds throughout**; the A vs A0 difference (7.6%) may be partly noise.
- **Partial-ionization plateaus** in the truth are a shared blind spot (overpredicted "partially ionized" fraction 0.135–0.18 vs truth 0.086).

## 9. Artifacts

- Suites: `runs/eval3d/{rhizome_w48_cont10_vs_fno_whno_es, rhizome_mf_C_B_vs_fno_histtb, slicewise2d_fnosplit_vs_3d, slicewise2d_w64_fnosplit_vs_3d, slicewise2d_vs_3d_test21, slicewise2d_mf_vs_3d_mf, slicewise2d_mf_all_vs_mf}/`.
- Head-to-head figures, best rhizome vs best fno labelled "Rhizome"/"UFNO" (re-rendered from saved suite results by `ebm21cm/replot_suite.py`, plus side-by-side cone pages and error maps): `runs/eval3d/h2h_rhizome_all_vs_ufno/` (all-cones model) and `h2h_rhizome_vs_ufno/` (1,594-cone model).
- Paired statistics: `runs/probes/paired_mf_all.py`. Mode weights: `runs/eval3d/mode_weights/`.
- Native multi-field cones (8 test cones, $x_\text{HI}$ + $T_b$): `data/eval_cubes/rhizome2d_mf_w64_all/native/`.
- Spin-smoothing test: `runs/eval3d/smooth_u_test/` (`ebm21cm/smooth_spin_test.py`); wide-context suite: `runs/eval3d/slicewise2d_mf_wide_vs_mf/`; $T_b$ offset split: `runs/probes/tb_offset*.py`; paired wide vs all-cones: `runs/probes/paired_wide_vs_all.py`.
- Multi-field inference benchmark: `runs/eval3d/bench_inference_mf_{a100,h200}.json`.
- Power-loss model: `runs/rhizome_mf2d_w64_structured_all_pw0.03/`, cubes `data/eval_cubes/rhizome2d_mf_w64_all_pw0.03/`, suite `runs/eval3d/slicewise2d_mf_power_loss/`, paired stats `runs/probes/paired_pw_vs_all.py`, offsets `runs/probes/tb_offset_pw.py`.
- Coherence vs small-scale power plane with the 3-D matrix: `runs/eval3d/ps_plane3d.png` (all rhizome variants), `ps_plane3d_best.png` (multi-field slice-wise only).
- Benchmarks: `runs/eval3d/bench_inference_{a100,h200}.json`.
- Native slice-wise cones (13 test cones): `data/eval_cubes/rhizome2d_w64_fnosplit_slicewise/native/`.
- $x_\text{HI}$ power-loss model: `runs/rhizome_mf2d_w64_structured_all_pw0.03_px0.03/`, cubes `data/eval_cubes/rhizome2d_mf_w64_all_pw0.03_px0.03/` (natives for 7 cones), suite `runs/eval3d/slicewise2d_mf_xhi_power_loss/`, paired stats `runs/probes/paired_px_vs.py`.
- Figures copied to the vault: `figures/rhizome-results_20261012/` and `figures/rhizome-cyl-power_20261013/` (see [[Rhizome Neural Operator Figures]]).
- Radius sweep: `runs/rhizome_mf2d_w64_structured_all_R{1,2,3,4,6,8_rank16}/`; cost benchmark `runs/eval3d/kernel_radius_bench_a100{,_cudnnbench}.json`.
- T sweep: `runs/rhizome_mf2d_w64_structured_all_{T3,T10,T6_seed1}/`. History ablation: `runs/rhizome_mf2d_w64_structured_all_nohist_{xhi,tb}/`, cubes `data/eval_cubes/rhizome2d_mf_w64_all_nohist_{xhi,tb}/`.
- Gate ablation: `runs/rhizome_mf2d_w64_structured_all_gates_frozen_seed{0,1}/` (`--gate-mode`), cubes and native spectra `data/eval_cubes/rhizome2d_mf_w64_all_gates_frozen_seed{0,1}/`, `runs/eval3d/native_cyl/`.
- Updates below 3: `runs/rhizome_mf2d_w64_structured_all_{T1,T2,T1_dt1}/`. In progress: `..._T12_dt0.25/`, `..._Trand3-12/` (`--random-updates`).
- Two-level rhizome (`RhizomeUNet2d`, `--coarse-*`): `runs/rhizome_mf2d_w64_structured_all_unet{A,B,C,D}/`, `..._unet{B,C}_pw0.03_px0.03/`, cubes `data/eval_cubes/rhizome2d_mf_w64_all_unet*/`, native maps `runs/eval3d/native_cyl/unet*_cyl_error_*.png`.
- Rollout diagnostic: `runs/eval3d/rollout_diagnostic{,_cycles}/` (`ebm21cm/rollout_diagnostic.py`).
- Gating mechanism: single-slice maps `runs/eval3d/mechanism{,_pw_px}/`, averages `runs/eval3d/mechanism_avg/` (per-receiver profiles, `summary.json`).
- Native cylindrical power: `runs/eval3d/native_cyl/<model>_{xhi,tb}.npz` and maps (`ebm21cm/native_cyl.py`, `ebm21cm/plot_cyl_error.py`); 512-grid $T_b$ maps: `runs/eval3d/tb_cyl/`, `runs/eval3d/cyl_error_linear/`.
- Launch records: `runs/rhizome3d/COMMON*.txt`, `runs/rhizome3d_mf/LAUNCH.txt`, `runs/rhizome_xhi_w128_fnosplit.LAUNCH.txt`, `runs/rhizome_mf2d.LAUNCH.txt`.
