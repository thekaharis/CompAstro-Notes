---
type: meta
title: "Hot Cache"
updated: 2026-07-16T00:00:00
---

# Recent Context

## Last Updated

2026-07-16 — Filed two advancements: [[Lightcone z_re Map Target]] (the smooth-target plan's candidate 1, implemented as a 2-D fitted-$z_\text{re}$ map pipeline) and [[Warped LOS Grid Plan]] (non-uniform LOS cache grid). Previously (2026-07-15): filed the [[Smooth-Target Reparametrization Plan]].

## Key Recent Facts

- **The z_re target is now implemented — as a fitted 2-D map, not `z_re_box`.** [[Lightcone z_re Map Target]]: per-pixel $z_\text{re}(x,y)$ least-squares fitted from existing lightcone $x_\text{HI}(z)$ sightlines (primary: Gompertz front $\exp(-e^{-(z-z_0)/\Delta z})$, stored midpoint $z_\text{half}$; alternative: exact LS step). No re-simulation, no code surgery; a **2-D FNO/U-FNO/LocalFNO** maps 64 density LOS slices (+11 params) → the map; NaN pixels (front outside cone) are edge-clamped + masked, loss `0.5·absL2+0.5·absH1`, masked MSE reported separately. Reconstruction sanity check (12 cones): lo-z-crossing and optimal-step reconstructions of global $x_\text{HI}(z)$ reach voxel MSE ≈ 0.008–0.05 (hi-z crossing bad: 0.13–0.32); **late reionizers are 79–99% no-front pixels** — the sentinel problem is the dominant practical issue. Training not yet run.
- **New data-side attack: warp the LOS cache grid.** [[Warped LOS Grid Plan]]: the current cube cache (256 slices uniform in z) is coarsest **~37 Mpc at low z where the fronts live** — information destroyed at cache time is unlearnable for every model, logically prior to all architecture/target attacks. Candidate grids: **warped** (density ∝ ensemble-mean $|d\langle x_\text{HI}\rangle/d\chi|$ + 20% floor, CDF-inverted), envelope90 (covers early/late timing classes), uniform-χ, crop15. Training-free round-trip evaluator (transition RMSE / sharpness ratio / fronts-missed, per timing class) merged, plus `build_cubes.py --target-z` and a Δχ volume-weighted loss flag (`LOSS_LOS_VOLUME_WEIGHTS=1`). Real-data evaluation pending.

- **Plan: reparametrize the target.** [[Smooth-Target Reparametrization Plan]] — learn a smooth surrogate instead of $x_\text{HI}$ and reconstruct by deterministic thresholding, so model uncertainty becomes front *displacement* rather than front *blurring*. Primary candidate: $z_\text{re}(\mathbf{x})$ (native 21cmFAST `z_re_box`, free targets, Battaglia et al. 2013 cover, bias-expansion link to P1); secondary: signed distance to the front; parked: pre-threshold excursion-set latent + fixed physics layer. Success = reconstructed front width < 10.7 Mpc (U-FNO) at ≤10% L² cost. First step is a one-afternoon **ceiling check** (truth $x_\text{HI}$ from truth $z_\text{re}$). Rationale: both basis-side attacks (Local-FNO, SirenFNO) failed to beat the U-FNO floor; the hedging failure mode is a property of the discontinuous target.

- **Local-FNO does not (yet) sharpen bubble walls — it broadens them.** First run [[Windowed Local-FNO U-Net Findings]] (local modes `(6,6,12)`, 21 epochs): boundary-band diagnostic vs the U-FNO benchmark shows the Local-FNO 10–90% front width = **32.2 Mpc** vs U-FNO **10.7 Mpc** (truth 3.6) — ~3× *broader*, plus higher RMSE (0.32 vs 0.28) and gradient error (0.19 vs 0.16) at the wall. Whole-volume (test L² 0.057 / H¹ 10.2) is at the plain-FNO level, short of the U-FNO floor (0.0418 / 8.27). Run is **undertrained/still descending** (caveat), but the front-width gap is too big for that alone. No patch seams.
- **Implication:** windowed-Fourier mixing is still a Fourier basis (Gibbs within each window); the U-FNO's wall sharpness likely comes from its **real-space conv path**, not from locality per se. Both Local-FNO and SirenFNO (the two "remove the global spectral bias" attacks) currently fail to beat the U-FNO floor → next clean test is a local-path/conv hybrid.

- **The spectral bias is now directly measured.** A new per-mode RMS weight diagnostic ([[SirenFNO Spectral Bias Investigation]]) shows the U-FNO learned spectrum **collapses onto low modes within epoch 0**: at 32 LOS modes the lowest 8/32 modes hold 52% of the weight (uniform = 25%), cutoff ratio falls from 1.0 to 0.1–0.45. This is the mechanism behind every mode-count null in [[FNO Lightcone Experimental Findings]].
- **SirenFNO removes the collapse.** Following [[Shi et al 2025 (SirenFNO)]], a 3-D SirenFNO parameterizes the Fourier kernel with a SIREN hypernetwork over all modes; its measured spectrum stays flat (low-quarter pinned at 0.25, cutoff ratio ≈1.0) at every epoch — full-frequency learning confirmed.
- **But it doesn't beat U-FNO yet.** Held-out: SirenFNO (modes 64, 70 ep) test L²=0.050 / H¹=9.82 beats plain FNO (0.057 / 11.64) but trails the U-FNO benchmark (modes 16, 100 ep) at 0.040 / 7.87. SirenFNO has **no local U-Net path**, so this is not yet apples-to-apples.
- [[FNO Lightcone Experimental Findings]] (seven acts): parameter conditioning was necessary; U-FNO + SyncBN reached val L² = 0.0418, H¹ = 8.27; the floor survived more LOS modes, GroupNorm, H¹ reweighting, larger LOS receptive field.
- [[Spectral Mode Cutoff in FNOs]] now carries both the interpretation (`n_modes` truncates only learned global spectral communication, not output bandwidth) and the new measurement of the weight collapse.
- Two distinct SIREN attacks on the boundary problem: **SirenFNO** (replace the kernel) vs **[[Siren3D Residual Refinement Plan]]** (residual head on frozen U-FNO).
- **A third attack is now filed: [[Windowed Local-FNO U-Net Plan]].** Instead of changing *which modes* the kernel represents, it changes *where the transform is applied* — spectral mixing inside small overlapping Hann windows (a low mode in a 16-voxel window = a high effective frequency on the full grid), plus one retained global Fourier bottleneck. ~10.2 M params, original-grid output, same `0.5·L²+0.5·H¹` objective for an architecture-only comparison. This is the "local U-Net path" control implied by the SirenFNO result.

## Active Threads

- **First $z_\text{re}$-map training runs** ([[Lightcone z_re Map Target]]): FNO2d → U-FNO2d/LocalFNO2d on the fitted Gompertz target; evaluate always in reconstructed $x_\text{HI}$-space (front width vs U-FNO 10.7 / truth 3.6 Mpc). Open: Gompertz midpoint vs lo-z-crossing step as training target; handling mostly-NaN late reionizers (mask-weighted loss vs cone filtering).
- **Warped-grid evaluation on real cones** ([[Warped LOS Grid Plan]]): run `los_grid_evaluation.py` on the cluster, pick the winner (warped vs envelope90 vs uniform-χ, budgets 256/512), rebuild the cube cache with `--target-z`, retrain the U-FNO benchmark with `LOSS_LOS_VOLUME_WEIGHTS=1`.
- **Smooth-target ceiling check** ([[Smooth-Target Reparametrization Plan]]): the full front-width version (reconstruct truth $x_\text{HI}$ and measure L²/H¹/front width) is still open; the global-history version is done and passes ([[Lightcone z_re Map Target]]).
- **Finish the Local-FNO run** ([[Windowed Local-FNO U-Net Findings]]): carry `lfno-run-6-6-12` from 21 → full 70 epochs (cosine-annealed) and re-run the boundary diagnostic before a final verdict — current numbers are undertrained. Then ablate: widen local modes `(8,8,16)` / smaller window, global-bottleneck on/off, boundary-aware loss, and a Local-FNO + real-space conv-path hybrid.
- Run the boundary-band + $P(k)$/$r(k)$ high-$k$ diagnostic on the existing SirenFNO checkpoint — does the flat spectrum buy bubble-wall fidelity even where whole-volume L² doesn't move?
- Build a **SirenFNO × U-Net hybrid** as the controlled test of "does removing spectral bias help, given the local path?"
- Still pending from the prior thread: the global-pooling residual (missing cone-level context) and the boundary-distance error diagnostic.
- Any SIREN-based win must lower held-out H¹ without degrading L², $P(k)$, $r(k)$, or the global ionization history.
- P1 remains focused on renormalized EFT coefficient extraction and cross-simulator validity.
