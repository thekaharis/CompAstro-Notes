---
type: finding
title: "Rhizome Neural Operator Results"
created: 2026-10-03
updated: 2026-10-03
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
  - "`rhizome-neural-operator/runs/` — `sweep1/`, `rhizome_xhi_w128*/`, `rhizome_xhi_w64_fnosplit/`, `rhizome3d/`, `rhizome3d_mf/`, `eval3d/`"
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
finally as a **slice-wise 2-D model that reassembles full 3-D cones**.

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

## 1. Setup

| | 2-D | 3-D | slice-wise 2-D |
|---|---|---|---|
| input | slice + 13 LOS density bands (±32 cells: single slices within ±3, band means to ±32) | native LOS windows 256 + 2×32 halo (fno-21cm pipeline) | 2-D model on every slice, bands built from the raw cone |
| conditioning | log(1+z), 11 parameters (FiLM-style scalars) | `z_params` channels | as 2-D |
| loss | BCE on $x_\text{HI}$ | masked BCE (+ MSE on normalized $T_b$ for multi-field) | BCE |
| data | slice cache: 16 window + 2 background slices / cone, 5,280 train cones (own split) | fno 2000-cone preparation (1600/200/200; multi-field: 1594/199/199, cleaned $T_b$) | fair split: fno's 1,600 train cones, 48+6 slices / cone |

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

## 6. Cost

| model | GPU | training run | inference, one full cone (2,709 slices), A100 / H200 |
|---|---|---|---|
| 2-D w64 slice-wise | A100 | **2.8 h** | — |
| 2-D w128 slice-wise | A100 | 5.0–6.5 h (92 slices/s) | 7.9 s + 3.2 s CPU bands / 4.0 s |
| 3-D rhizome w48 | H200 | ~12 h + 6 h restart (3.1 windows/s; A100 1.38, ~77 min/epoch) | 4.7 s / 1.9 s |
| fno `cnn_whno_es` | A100 | 44.7 h, 30 epochs (1.32 windows/s, ~81 min/epoch) | 2.1 s / 1.0 s |

- **The 2-D model is ~4× slower per slice in training**: width 128, float32, full-resolution recurrent updates.
- **It needs 15–20× fewer training slices** (2.2 M vs 33–49 M), so a whole run is 4–7× cheaper.
- **Inference speed-ups not yet applied:** w64, bf16, and band building on the GPU. These should bring slice-wise inference to roughly the 3-D rhizome's speed.

## 7. Open items

- **Multi-field slice-wise 2-D** (density + velocity bands, history band means as scalars, structured $T_b$ head with the physical factor $A(z)(1+\delta)V$ precomputed by the 3-D head's code, w64, batch 32) is training since 2026-10-03. Its cache is built from fno's multi-field pipeline, so data, split and normalization match §4. Pilot check: $T_b/(x_\text{HI}\cdot A(1+\delta)V)$ gives a smooth spin factor (0.8 -> −0.08). A slice-wise $x_\text{HI}+T_b$ exporter for the suite is still to be written.
- **fno retrain with BCE on $x_\text{HI}$**, to separate the loss effect (§4.3) from the operator.
- **Single seeds throughout**; the A vs A0 difference (7.6%) may be partly noise.
- **Partial-ionization plateaus** in the truth are a shared blind spot (overpredicted "partially ionized" fraction 0.135–0.18 vs truth 0.086).

## 8. Artifacts

- Suites: `runs/eval3d/{rhizome_w48_cont10_vs_fno_whno_es, rhizome_mf_C_B_vs_fno_histtb, slicewise2d_fnosplit_vs_3d, slicewise2d_w64_fnosplit_vs_3d, slicewise2d_vs_3d_test21}/`.
- Coherence vs small-scale power plane with the 3-D matrix: `runs/eval3d/ps_plane3d.png`.
- Benchmarks: `runs/eval3d/bench_inference_{a100,h200}.json`.
- Native slice-wise cones (13 test cones): `data/eval_cubes/rhizome2d_w64_fnosplit_slicewise/native/`.
- Launch records: `runs/rhizome3d/COMMON*.txt`, `runs/rhizome3d_mf/LAUNCH.txt`, `runs/rhizome_xhi_w128_fnosplit.LAUNCH.txt`, `runs/rhizome_mf2d.LAUNCH.txt`.
