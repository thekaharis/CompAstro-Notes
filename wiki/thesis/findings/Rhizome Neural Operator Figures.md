---
type: finding
title: "Rhizome Neural Operator Figures"
created: 2026-10-12
updated: 2026-10-13
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - concept/architecture
status: active
related:
  - "[[Rhizome Neural Operator Results]]"
  - "[[3-D Operator Matrix Final Results]]"
  - "[[Phase Coherence and Bubble Size Bias]]"
  - "[[Multi-Field 21cmFAST Data]]"
sources:
  - "`rhizome-neural-operator/runs/eval3d/` — `h2h_rhizome_all_vs_ufno/`, `slicewise2d_mf_xhi_power_loss/`, `slicewise2d_mf_wide_vs_mf/`, `smooth_u_test/`, `mode_weights/`, `rhizome_w48_cont10_vs_fno_whno_es/`, `rhizome_mf_C_B_vs_fno_histtb/`, `slicewise2d_w64_fnosplit_vs_3d/`, `ps_plane3d_best.png`"
  - "fno-21cm evaluation suite plots (`viz.physical_evaluation`, `power_spectrum_evaluation`, `bubble_size_evaluation`, `boundary_band_diagnostic`, `multifield_slices`, `multifield_detailed`, `multifield_lightcone_strips`), re-rendered for the head-to-head by `ebm21cm/replot_suite.py`"
---

# Rhizome Neural Operator Figures

Figure companion to [[Rhizome Neural Operator Results]]; numbers and context are
there, section numbers (§) refer to it. All figures are on the 199 (multi-field)
or 200 ($x_\text{HI}$-only) held-out test cones unless a cone is named. Copies
live in `figures/rhizome-results_20261012/` `figures/rhizome-cyl-power_20261013/` and `figures/rhizome-mechanism_20261013/`.

**Naming in the plots.** "Rhizome" = the multi-field slice-wise 2-D model trained
on all cones (`rhizome2d_mf_w64_all`, the plain BCE + $T_b$ MSE variant); "UFNO" =
fno-21cm's best multi-field model (`cnn_whno_es` `tbs+histtb`). Elsewhere
`rhizome2d_mf_w64_all_pw0.03` adds the $T_b$ power loss (§6.7),
`..._pw0.03_px0.03` also the $x_\text{HI}$ power loss (§6.8), `rhizome3d_mf_C_cont10`
is the 3-D multi-field rhizome C, `rhizome3d_w48_cont10` the 3-D $x_\text{HI}$ rhizome and
`fno_cnn_whno_es` fno's 3-D $x_\text{HI}$ model.

## 1. Head-to-head: Rhizome vs UFNO (§6.1)

### 1.1 Physical metrics

![[h2h_physical_history.png]]
*Global history and timing.* Left: median (16–84% band) error of the global
$x_\text{HI}(z)$ — the Rhizome is flat on zero, UFNO sits −0.002 to −0.004 low,
the MSE-through-sigmoid saturation offset of §4.3. Then the τ_e error in Planck σ
(median 0.01σ vs 0.08σ), and predicted vs true midpoint and duration
(median |err| 0.010 vs 0.017 and 0.018 vs 0.044).

![[h2h_physical_pdfs.png]]
*Value distributions* of $x_\text{HI}$ and $T_b$ during reionization (PDF W1 $x_\text{HI}$ 0.0095 vs 0.027,
$T_b$ 0.79 vs 1.19 mK; partially-ionized fraction 0.136 vs 0.174, truth 0.089).

![[h2h_physical_21cm.png]]
*21-cm statistics.* Transverse $T_b$ power by stage, its evolution at fixed $k$,
variance and skewness of $\delta T_b$, and the power bias in units of single-slice
sample variance for $T_b$ and $x_\text{HI}$.

![[h2h_physical_eft.png]]
*EFT diagnostics:* linear bias b₁ (pull 0.99 vs 2.28) and the stochastic term
P_ε (ratio 0.954 vs 0.793).

### 1.2 Power spectra and coherence ($x_\text{HI}$)

![[h2h_ps_stage_curves.png]]
*Power ratio and cross-correlation r(k) by reionization stage.* Both models lose
small-scale power late in reionization, UFNO more. The Rhizome keeps r > 0.9 to
higher k at every stage (1 − r at k > 1: 0.096 vs 0.174).

![[h2h_ps_overlay.png]]
*Power spectra of truth and both models, stage overlays.*

![[h2h_ps_cyl_ratio.png]]
![[h2h_ps_cyl_r.png]]
*Cylindrical (k⊥, k∥) power ratio and coherence* of both models.

### 1.3 Bubble sizes and ionization fronts

![[h2h_bubble_size_distribution.png]]
![[h2h_bubble_size_summary.png]]
*Mean-free-path bubble-size distributions by stage and their W1 distance to the
truth* (active W1 0.56 vs 1.21 Mpc).

![[h2h_edge_3d.png]]
![[h2h_edge_slice.png]]
*Error profiles across ionization fronts* (3-D and per-slice boundary bands):
front width 3.9 vs 6.2 Mpc (truth 2.77); 3-D edge H1 ±2 Mpc 0.106 vs 0.147.

### 1.4 Cones, slices and strips

![[h2h_cone24.png]]
*Test cone 24.* Top: $x_\text{HI}$ lightcone strips (truth, Rhizome, UFNO) with signed
error and the global history. Bottom: transverse slices at x̄ = 0.17 / 0.40 /
0.61 / 0.80. Rhizome RMSE 0.045 vs 0.057 full cone; UFNO's fronts are blurred
and it leaves a faint haze inside ionized regions.

![[h2h_cone1751.png]]
![[h2h_cone417.png]]
*Cones 1751 and 417*, same layout. Over the 8 inspected cones the Rhizome wins
all by 12–28% in full-cone RMSE.

![[h2h_error_maps_xhi0.4.png]]
*Signed error maps at x̄_HI ≈ 0.4 on 8 cones* (red: too neutral). The Rhizome's
errors are thin rims on bubble walls; UFNO misses whole regions (e.g. cone 24,
417) and its rims are wider.

![[slices_rhizome_cone24_xhi.png]]
![[slices_ufno_cone24_xhi.png]]
*$x_\text{HI}$ slices of cone 24 at five redshifts* (truth, prediction, error), Rhizome then UFNO.

![[slices_rhizome_cone24_tb.png]]
![[slices_ufno_cone24_tb.png]]
*$T_b$ slices of cone 24.* Colour scale per column. The absorption-era columns
(z ≈ 13.6, 16.3) show the per-slice offset of §6.5 as a uniform tint of the
error map.

![[detailed_rhizome_cone24_xhi.png]]
![[detailed_ufno_cone24_xhi.png]]
![[detailed_rhizome_cone24_tb.png]]
![[detailed_ufno_cone24_tb.png]]
*Detailed pages, cone 24:* slices, zooms and per-slice statistics for each field,
Rhizome then UFNO.

![[strips_rhizome_xhi.png]]
![[strips_ufno_xhi.png]]
*$x_\text{HI}$ lightcone strips* (transverse row y = 100 Mpc, active band): truth,
prediction and error per cone. Rhizome on cones 24, 27, 417, 425; UFNO on the
cones it was exported for natively (24, 27). Cone 27 (z_mid ≈ 16) is the
shared weak case: ionized gas predicted too neutral at the front.

![[strips_rhizome_tb.png]]
![[strips_ufno_tb.png]]
*$T_b$ lightcone strips*, same layout.

## 2. Coherence vs small-scale power (§6.1)

![[ps_plane_coherence_vs_power_best.png]]
*Small-scale coherence r(k > 1) against small-scale power error*, the plane of
[[Phase Coherence and Bubble Size Bias]], with the 3-D operator matrix and the
multi-field fno runs. The multi-field slice-wise rhizome sits apart from every fno
model: r 0.90 vs 0.82–0.83, power error 0.17 vs 0.31–0.34.

## 3. Mode-weight diagnostic (§6.4)

![[mode_weight_maps.png]]
![[mode_weight_profiles.png]]
*Per-mode RMS of the learned Fourier kernel relative to initialization.* Maps over
Fourier plane and profiles. Flat up to the band edge (high/low-quarter ratio
0.78–0.94, vs 0.10–0.45 for the U-FNO): no low-frequency collapse. Ridges along the
axes and diagonals are the mirror lines of the dihedral augmentation.

## 4. Absorption-era $T_b$ tests (§6.3, §6.6)

![[smooth_u_physical_21cm.png]]
*Smoothing u along the LOS* (Gaussian σ = 0–16 cells) vs the 3-D rhizome: removes
the pre-reionization excess only by distorting the $T_b$ statistics. Rejected.

![[wide_los_physical_21cm.png]]
*±128-cell LOS context vs ±32:* larger absorption-era excess (+36σ vs +24.8σ)
and worse late-heating $T_b$ W1 (0.88 vs 0.82 mK). Not adopted.

## 5. Power-loss variants (§6.7, §6.8)

Plain, $T_b$ power loss (pw0.03), $T_b$ + $x_\text{HI}$ power loss (pw0.03_px0.03) and 3-D C,
199 test cones.

![[power_loss_physical_21cm.png]]
*21-cm statistics, active slices.* Top right: $T_b$ power bias per single-slice
sample variance — both power-loss models stay near zero to k ≈ 2 Mpc⁻¹, the plain
model and 3-D C fall to −10 and −12σ. Bottom right: the same for $x_\text{HI}$ — the
$x_\text{HI}$ power term (blue) keeps it smallest at the highest k (≈ −7σ vs −13 to −18σ).

![[power_loss_ps_stage_curves.png]]
*$x_\text{HI}$ power ratio and coherence by stage, four models.* The $x_\text{HI}$ power term
lifts the high-k power ratio (k > 1 error 0.15 vs 0.59 for the $T_b$-only power
loss in the latest stage) and costs a little coherence (1 − r 0.57 vs 0.52).

![[power_loss_edge_3d.png]]
![[power_loss_bubble_size_summary.png]]
*Fronts and bubble sizes:* front width unchanged (3.90 / 3.94 / 3.89 Mpc), edge
H1 slightly worse with each power term (0.114 / 0.112 / 0.106).

![[power_loss_px_detailed_cone1751_xhi.png]]
![[power_loss_plain_detailed_cone1751_xhi.png]]
![[power_loss_px_detailed_cone1751_tb.png]]
![[power_loss_plain_detailed_cone1751_tb.png]]
*Cone 1751, $T_b$ + $x_\text{HI}$ power-loss model vs plain model,* detailed pages for both fields.

## 6. Slice-wise 2-D $x_\text{HI}$ vs 3-D (§5)

![[slicewise_xhi_cone24.png]]
*Cone 24: slice-wise 2-D rhizome (fair split, w64) vs 3-D rhizome vs fno
`cnn_whno_es`.* No LOS jitter in the restacked cone.

![[slicewise_xhi_ps_stage_curves.png]]
*Power ratio and coherence by stage:* the slice-wise model's mid-scale power error
is −60% vs the 3-D models and its small-scale incoherence 0.12 vs 0.18–0.20.

![[slicewise_xhi_error_maps.png]]
*Error maps:* thin rims on bubble walls for the slice-wise model; the 3-D models
miss whole ionized regions.

## 7. 3-D rhizome (§3, §4)

![[xhi3d_physical_history.png]]
![[xhi3d_ps_stage_curves.png]]
![[xhi3d_edge_3d.png]]
*3-D $x_\text{HI}$: rhizome w48 (+warm restart) vs fno `cnn_whno_es`* — global history and
timing, power/coherence by stage, front error profile (§3 table).

![[mf3d_physical_history.png]]
![[mf3d_physical_21cm.png]]
*3-D multi-field: rhizome C and B vs fno `tbs+histtb` / `es+histtb`* — global
history and timing, 21-cm statistics (§4.2 table).

## 8. Cylindrical power at native LOS resolution (§6.11, §6.12)

Fractional power error $P_\text{pred}/P_\text{true} - 1$ per (k⊥, k∥) cell, cone median over
the 199 test cones. Chunks of 140 native slices (200 Mpc) at z ≈ 7, 9, 11, 14, 17, so both
axes run from 0.031 to 2.2 Mpc⁻¹. k⊥ in log bins; k∥ one row per LOS frequency (rows thin
out towards high k∥). Flat white within ±0.1, saturating at ±0.4 (red: too much power).

![[native_cyl_ufno_vs_rhizome_xhi.png]]
*$x_\text{HI}$: UFNO vs plain rhizome vs + $T_b$ power loss vs + $T_b$ & $x_\text{HI}$ power loss.*
UFNO loses power at high k∥ (≳ 0.5 Mpc⁻¹) at every redshift as well as at high k⊥, and
has a large-scale excess from z ≈ 11. The plain rhizome is short only in the top rows and
the highest k⊥; with both power terms the maps are white (91–100% of cells).

![[native_cyl_ufno_vs_rhizome_tb.png]]
*$T_b$, same models.* UFNO again falls off at high k∥ and k⊥. The plain rhizome's
absorption-era excess fills the z ≈ 17 map; the power-loss models leave a band at
k∥ ≈ 0.5–1 Mpc⁻¹ there and are near-white elsewhere.

![[native_cyl_xhi_history_xhi.png]]
![[native_cyl_xhi_history_tb.png]]
*With vs without the $x_\text{HI}$ history input* ($x_\text{HI}$, then $T_b$). Without it both
fields lose 10–30% of their small-scale power at z ≈ 11–14 and $x_\text{HI}$ gains a
large-scale excess at z ≈ 17.

![[native_cyl_tb_history_xhi.png]]
![[native_cyl_tb_history_tb.png]]
*With vs without the $T_b$ history input.* A much smaller effect: a broad $T_b$ excess at
z ≈ 14 without it; the absorption-era excess at z ≈ 17 is unaffected by either history.

## 9. Gating mechanism (§6.13)

Re-weighting of a receiver cell's incoming connections by the gates,
$M_t(j) = \|\mathrm{diag}(A_i)\kappa(r_i-r_j)\mathrm{diag}(B_j)\|_F / \|\kappa(r_i-r_j)\|_F$,
relative to its mean over j. Single slices: test slices at x̄_HI ≈ 0.2, 0.4, 0.6, 0.8,
receiver (circle) on an ionization front, panels cropped to ±32 cells (±46 Mpc);
contours: true x_HI = 0.5. Top row: density band [0, 1], true and predicted x_HI,
kernel norm, receiver and source gates at the last update; bottom row: M_t for
updates 1–6 with the mean gain.

**Plain model:**

![[plain_mechanism_cone32_z7p10.png]]
![[plain_mechanism_cone1208_z9p13.png]]
![[plain_mechanism_cone1228_z6p12.png]]
![[plain_mechanism_cone552_z5p11.png]]
*Receiver gates open in ionized gas (about 2× the neutral value), source gates nearly
uniform. The gates boost connections within 10–20 cells of the receiver; the mean
gain falls from 0.11–0.40 at t = 1 to 0.06–0.14 at t = 6.*

**Model with both power terms** (same slices and receivers):

![[pwpx_mechanism_cone32_z7p10.png]]
![[pwpx_mechanism_cone1208_z9p13.png]]
![[pwpx_mechanism_cone1228_z6p12.png]]
![[pwpx_mechanism_cone552_z5p11.png]]
*Same pattern with about twice the receiver gate and gain. These slices show a ring at
7–10 cells, but the average below shows it is not general.*

**Averages over 7,217 receivers in 120 test slices:**

![[avg_mt_profiles_by_update.png]]
*Mean radial profile of $M_t(j)/\langle M_t\rangle_j$ per update, for front,
neutral-interior and ionized-interior receivers (± s.e.), with the bare kernel norm
(dashed, right axis). The gates extend the coupling from the kernel's 3.6 Mpc
half-width to 10–25 Mpc; ionized cells reach furthest.*

![[avg_mt_front_profile_by_stage.png]]
*Front receivers at the last update by reionization stage: the plain model's boost
grows and narrows with x̄, the power-loss model's is stronger, more local and nearly
stage-independent.*

![[avg_mt_gain_and_receiver_gate.png]]
*Mean gain and receiver gate per update: front and neutral cells settle after 2–3
updates, ionized-interior cells keep opening; the power-loss model is about 2× higher
throughout.*
