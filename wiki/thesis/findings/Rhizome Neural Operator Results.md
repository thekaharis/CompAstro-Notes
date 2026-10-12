---
type: finding
title: "Rhizome Neural Operator Results"
created: 2026-10-03
updated: 2026-10-12
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
- **Wider kernel band:** full-budget 36/48-mode runs; SIREN only if those help (§6.4).
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
- Figures copied to the vault: `figures/rhizome-results_20261012/` (see [[Rhizome Neural Operator Figures]]).
- Launch records: `runs/rhizome3d/COMMON*.txt`, `runs/rhizome3d_mf/LAUNCH.txt`, `runs/rhizome_xhi_w128_fnosplit.LAUNCH.txt`, `runs/rhizome_mf2d.LAUNCH.txt`.
