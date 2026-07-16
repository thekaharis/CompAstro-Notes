---
type: finding
title: "Windowed Local-FNO U-Net Findings"
created: 2026-06-28
updated: 2026-07-16
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - architecture/local-fno
  - architecture/u-fno
  - concept/spectral-bias
  - finding/negative
status: active
related:
  - "[[Windowed Local-FNO U-Net Plan]]"
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Siren3D Residual Refinement Plan]]"
  - "[[Fourier Neural Operator]]"
  - "[[Wen et al 2022 (U-FNO)]]"
  - "[[Inference and ML]]"
  - "[[P1 EFT Characterization]]"
sources:
  - "[[Thesis/FNOs/LocalFNO/LOCAL_FNO.md]]"
  - "[[Thesis/FNOs/LocalFNO/lfno-run-6-6-12.jsonl]]"
  - "run_info: lfno-run-6-6-12 (local modes (6,6,12), 21 epochs)"
---

# Windowed Local-FNO U-Net Findings

> **Purpose:** Record the first training run of the [[Windowed Local-FNO U-Net Plan]] — a U-FNO whose encoder/decoder spectral mixing happens inside small overlapping Hann windows, with one retained global Fourier bottleneck — and its head-to-head boundary-band comparison against the [[FNO Lightcone Experimental Findings|U-FNO benchmark]]. The architecture was designed specifically to sharpen bubble walls; this first run does **not** deliver that. At the epoch-20 checkpoint the Local-FNO produces a *broader, smoother* ionization front and *higher* error at the wall than the U-FNO, on both whole-volume and boundary-localized diagnostics. This is a negative result against the design hypothesis, with one important caveat: the run is short (21 epochs, still descending) versus the converged U-FNO baseline.

This note covers the run logged in `lfno-run-6-6-12.jsonl` (local modes `(6,6,12)`, the default config) on the same density → x_HI lightcone task and split as the rest of the campaign (cube **140 × 140 × 256**, 6600 cones, 80/10/10 by cone, seed 42, 4× H200 DDP).

---

## Headline Result

The Local-FNO was filed as the **third attack on the bubble-wall floor** (after [[SirenFNO Spectral Bias Investigation|SirenFNO]] and [[Siren3D Residual Refinement Plan|Siren3D]]). Its success criterion, set in the plan, was:

> improved boundary-band H¹ and 10–90% front width over the strongest U-FNO baseline, with ≤5% val-L² regression and no visible patch seams.

**On this first run it fails that criterion on every axis that matters.** The boundary diagnostic (`boundary_band_overlay.png`, computed against the U-FNO benchmark on the test split) shows the Local-FNO is the *worse* model at the front:

| Boundary diagnostic | U-FNO (benchmark) | **Local-FNO (ep 20)** | Verdict |
|---|---|---|---|
| 10–90% front width *(truth = 3.6 Mpc)* | **10.7 Mpc** | **32.2 Mpc** | **3× broader — much worse** |
| Peak RMSE at the front | ≈ 0.28 | ≈ 0.32 | Worse |
| Peak gradient error `RMS \|∇(x̂−x)\|` | ≈ 0.16 | ≈ 0.19 | Worse (the H¹ metric the design targets) |

The whole-volume metrics tell the same story relative to the benchmark, though the gap there is smaller and partly attributable to the short run:

| Metric | FNO (100 ep) | **U-FNO (30 ep, benchmark)** | SirenFNO (70 ep) | **Local-FNO (21 ep)** |
|---|---|---|---|---|
| val L² | 0.0561 | **0.0418** | — | 0.0593 |
| val H¹ | 11.36 | **8.27** | — | 10.59 |
| test L² | 0.0570 | **0.0408** | 0.050 | 0.0569 |
| test H¹ | 11.64 | **8.27** | 9.82 | 10.25 |

So after 21 epochs the Local-FNO sits roughly at the **plain-FNO L² level** (≈ 0.057) and between FNO and SirenFNO on H¹ — well short of the U-FNO floor it was meant to break, and the boundary-band diagnostic it was explicitly built for is moving in the *wrong direction*.

---

## Update (2026-07-05 results, filed 2026-07-16): epoch-38 checkpoint + parity diagnostic

Follow-up diagnostics from the Binac figure backup (`band_out/`, `parity_out/`; localfno at **epoch 38**, 167 test cones):

- **The front-width gap shrank a lot with training but did not close.** Boundary run `4204953`: Local-FNO 10–90% front width **18.5 Mpc vs U-FNO 13.9 Mpc** (truth 3.6) — down from 32.2 vs 10.7 at epoch 20. *Caveat:* the U-FNO reference also reads differently here (13.9 vs 10.7 in the first run), so this evaluation's window/config differs from the original; compare within-run, not across runs.
- **Still significantly worse, but the margin collapsed ~8×.** Paired bootstrap on boundary-band H¹ (band ±2 cells): mean_diff +0.0031, CI95 (+0.0022, +0.0042), P(localfno better) = 0.000 — versus +0.0247 at epoch 20 (`4005674`) and +0.0167 at an intermediate checkpoint (`4010669`). Direction unchanged: the U-FNO stays ahead at the wall.
- **The one-sided ionized-wall loss experiment failed.** A 10-epoch run with the new `LOSS_IONIZED_WALL_WEIGHT` penalty (`4014918`) was the *worst* of all checkpoints (H¹_band2 mean_diff +0.0359) — the wall-side penalty did not sharpen the front at that budget.
- **New parity diagnostic directly measures the hedging bias.** `parity_diagnostic.py` (jobs `4205004/4205005`): in nearly-ionized bins (true $x_\text{HI} \in [0.02, 0.08)$, ~10⁵–10⁶ voxels/bin) **both** models over-predict — U-FNO median pred ≈ 0.11–0.14 vs true 0.03–0.07 (bias ≈ +0.17, RMSE ≈ 0.30); Local-FNO worse (bias ≈ +0.20–0.21, RMSE ≈ 0.32–0.33). Same picture restricted to z = 6–12. This is the plan-level "hedging" failure mode of [[Smooth-Target Reparametrization Plan]] made quantitative: even the best architecture refuses to commit ionized voxels to 0.

**Verdict so far:** more epochs help the Local-FNO substantially but the ordering never flips, and the parity bias is common to both architectures — strengthening the case that the target, not the basis, is the binding constraint (→ [[Lightcone z_re Map Target]], [[Warped LOS Grid Plan]]).

---

## Architecture and Setup (as run)

The model is the default Local-FNO from [[Windowed Local-FNO U-Net Plan]] / `LOCAL_FNO.md`:

| Component | Value |
|---|---|
| Window size / stride | `(16, 16, 32)` / `(8, 8, 16)` (50% overlap) |
| Retained **local** modes | `(6, 6, 12)` — hence the run name |
| Spectral channel rank | 16 |
| U-Net widths | 16 → 32 → 64 (two anti-aliased downsamples) |
| Global bottleneck modes | `(16, 16, 16)`, two residual FNO blocks at ≈ `35×35×64` |
| Shifted window grids | alternating offset `(0,0,0)` / `(4,4,8)` |
| Boundary handling | periodic wrap in X/Y, masked nearest-endpoint in Z |
| Parameters | ≈ 10.2 M (vs ≈ 28 M U-FNO, ≈ 9.5 M plain FNO) |
| `in_channels` | 13 (density/10 + 1/(1+z) + 11 z-scored astro params) |
| Output | sigmoid → `[0,1]` |
| Loss | `0.5·L²_abs + 0.5·H¹_abs + 0.0·BCE`, H¹ linearly warmed over epochs 0–5 |
| Hardware | 4× H200 NVL, DDP |

This is a deliberate **architecture-only** comparison: same inputs, same modes-for-the-global-path, same loss recipe as the U-FNO benchmark. The only structural change is *where* the Fourier transform is applied (small windows vs whole volume).

Runtime: ≈ **1093 s/epoch** (≈ 18 min), ≈ 4.83 samples/s, peak ≈ 48 GB CUDA. That is ~2.1× the U-FNO's per-epoch cost (522 s) and ~5.7× the plain FNO (192 s) — the patch FFTs are expensive, as the plan anticipated.

---

## Training Trajectory

`lfno-run-6-6-12.jsonl`, 21 epochs (0–20). Key milestones:

| Epoch | train_err | val L² | val H¹ | test L² | test H¹ | H¹ weight | Comment |
|---|---|---|---|---|---|---|---|
| 0 | 0.235 | 0.1640 | 17.93 | 0.1727 | 17.51 | 0.0 | random init; H¹ not yet on |
| 2 | 6.137 | 0.1076 | 14.19 | 0.1104 | 13.92 | 0.2 | H¹ ramping in |
| 5 | 12.701 | 0.0808 | 12.61 | 0.0812 | 12.39 | 0.5 | H¹ fully weighted from here |
| 10 | 11.212 | 0.0673 | 11.40 | 0.0659 | 11.12 | 0.5 | crosses plain-FNO H¹ floor |
| 15 | 10.613 | 0.0623 | 10.85 | 0.0618 | 10.63 | 0.5 | — |
| 18 | 10.374 | 0.0607 | 10.64 | 0.0586 | 10.30 | 0.5 | — |
| **20** | **10.218** | **0.0593** | **10.59** | **0.0569** | **10.25** | 0.5 | **final logged epoch — still descending** |

Two things to read off the trajectory:

1. **The run is not converged.** val L² fell from 0.0607 → 0.0593 over the last three epochs and val H¹ is still trending down. The U-FNO benchmark, by contrast, is the converged 30-epoch best checkpoint. Part of the whole-volume gap (0.0593 vs 0.0418) is therefore undertraining — but the *front-width* gap (32.2 vs 10.7 Mpc) is far too large to be explained by ~10 missing epochs.
2. **The model is learning bimodality, slowly.** Saturation fractions (`pred_sat_low`/`high`) climb from ≈ 0 to ≈ 0.028 / 0.038 by epoch 20 — the network is beginning to commit voxels to 0 and 1. But the front it draws is still much smoother than the U-FNO's, so the local windows are not yet buying the sharp-wall behaviour they were designed for.

![[fno_training_trajectories.png]]
*Benchmark trajectories (FNO / U-FNO / SirenFNO) for context; the Local-FNO run above is logged separately in `lfno-run-6-6-12.jsonl`.*

---

## The Boundary Diagnostic (the key result)

`boundary_band_diagnostic.py` bins every voxel by signed distance to the true ionization front (− = ionized side, + = neutral side) over 200 test cones, with the U-FNO as the reference checkpoint.

![[localfno_boundary_band_overlay.png]]

**Left — error localized at the front.** RMSE-per-voxel peaks right at the wall for both models, but the Local-FNO (orange) sits *above* the U-FNO (blue) at essentially every distance, peaking ≈ 0.32 just inside the ionized side vs ≈ 0.28 for U-FNO. The Local-FNO is worse on both sides of the front, and the excess is largest deep on the ionized side (−30 Mpc: ≈ 0.18 vs ≈ 0.10) — i.e. inside bubbles, where it should be confidently 0.

**Middle — front sharpness.** Stacking the predicted ⟨x_HI⟩ profiles across the front gives a 10–90% transition width. Truth = **3.6 Mpc**; U-FNO recovers **10.7 Mpc**; Local-FNO smears it to **32.2 Mpc**. The Local-FNO front is ~9× the true width and ~3× broader than the U-FNO's — the opposite of the design goal.

**Right — gradient error (where the H¹ win lives).** `RMS |∇(x̂−x)|` peaks at the front for both; Local-FNO ≈ 0.19 vs U-FNO ≈ 0.16. Since H¹ penalizes exactly this gradient mismatch, the broader front and higher gradient error are two views of the same deficiency.

There were **no obvious grid-aligned patch seams** in the overlay (the seam-suppression machinery — sqrt-Hann analysis/synthesis + normalized overlap-add + shifted window grids — appears to be doing its job); the failure is a smooth, global over-broadening of the front, not a patch artefact.

---

## Interpretation

The premise of the Local-FNO ([[Spectral Mode Cutoff in FNOs]]) is sound: a low mode inside a 16-voxel window represents a much higher effective frequency on the full grid, so windowed mixing *should* give cheap access to sharp, localized structure. This run shows that the premise, on its own, is **not sufficient** to beat the U-FNO at the wall. Candidate reasons, in rough priority:

1. **Undertraining is real but partial.** 21 vs 30 (converged) epochs explains some of the L² gap but cannot explain a 3× front-width gap. The architecture is genuinely behind on the boundary metric at this checkpoint, not merely behind on the clock.
2. **Retained local modes may be too few.** `(6,6,12)` inside a `(16,16,32)` window keeps a modest fraction of each window's spectrum; the Hann taper further suppresses the window edges where the sharpest gradients live. The very mechanism that kills patch seams (the taper) may also be smoothing the front. This is the first ablation to run (the plan lists window size and local/global mode allocation as ablations 3–4).
3. **The U-FNO's real-space conv path is doing the sharpening.** The U-FNO breakthrough in [[FNO Lightcone Experimental Findings]] was attributed to a *local 3-D convolution* path that is Gibbs-free at the filter scale. The Local-FNO replaces that with windowed Fourier mixing — still a Fourier basis, just localized — which retains Gibbs behaviour *within* each window. So this run is also evidence that **windowed-Fourier ≠ real-space convolution** for step-like walls: the thing that sharpened the U-FNO was the conv path, not merely locality.
4. **No boundary-aware loss yet.** By design this run used the plain `0.5·L²+0.5·H¹` objective for a clean comparison; the plan defers an edge-weighted loss to ablation 5. With error this concentrated at the front, boundary oversampling/weighting is a natural next lever.

Net: this is the "local path control" implied by [[SirenFNO Spectral Bias Investigation]], and it lands as a **negative result** — removing the global-only spectral bias *via windowing* does not, by itself, reproduce the U-FNO's wall sharpness, and currently underperforms it.

---

## What to Try Next

In priority order, tracking the ablation list in [[Windowed Local-FNO U-Net Plan]]:

1. **Finish the run.** Carry `lfno-run-6-6-12` to the full 70 epochs (and ideally cosine-annealed) before drawing a final whole-volume verdict — the trajectory is still descending. Re-run the boundary diagnostic on the converged checkpoint.
2. **Widen the local mode budget.** Raise retained local modes (e.g. `(8,8,16)`) and/or shrink the window so a given mode count covers more of each window's spectrum; test whether the front sharpens. (plan ablations 3–4)
3. **Global bottleneck on/off.** Run the with/without-global-bottleneck ablation (plan ablation 1) to confirm the smoothing is coming from the local path and not the low-resolution global block.
4. **Add a boundary-aware loss** (plan ablation 5) only after the architecture-only comparison is converged — oversample/upweight voxels near the front.
5. **Hybrid with a real-space conv path.** Given interpretation (3), the cleanest test is Local-FNO **plus** the U-FNO's local conv path, isolating whether the conv path is the actual source of wall sharpness.

---

## Connection to Other Thesis Threads

| Thread | How this connects |
|---|---|
| [[FNO Lightcone Experimental Findings]] | Supplies the U-FNO benchmark (val L² = 0.0418, H¹ = 8.27; front width 10.7 Mpc) this run is measured against. The Local-FNO does not yet reach that floor. |
| [[SirenFNO Spectral Bias Investigation]] | SirenFNO removes the global spectral bias but lacks a local path; the Local-FNO is the local-path control. Neither yet beats the U-FNO — consistent with the U-FNO's edge coming from its real-space conv path. |
| [[Spectral Mode Cutoff in FNOs]] | The "low mode in a small window = high effective frequency" premise is correct in principle but, per this run, insufficient in practice for wall sharpness. |
| [[P1 EFT Characterization]] | The current best field-level baseline remains the U-FNO residual; the Local-FNO does not change that until it converges and beats the benchmark. |

---

## Reproducibility

- Architecture spec: `Thesis/FNOs/LocalFNO/LOCAL_FNO.md`; implementation `local_fno_3d.py` + `modeling.py`. Selected with `MODEL_KIND=localfno`. All settings persisted to `run_metadata.json`; viz/diagnostics reconstruct the model from metadata, not the shell env.
- Run log: `Thesis/FNOs/LocalFNO/lfno-run-6-6-12.jsonl` (21 epochs; one JSON line/epoch with `train_err`, per-split `l2`/`h1`/`bce`, `pred_sat_*`, `last_grad_norm`, `peak_cuda_memory_gb`).
- Boundary comparison: `boundary_band_diagnostic.py --checkpoints ufno=… localfno=… --reference ufno --split test --n-cones 200` → `boundary_band_overlay.png`.
- Split reproducibility: `SPLIT_SEED = 42`, val_frac = test_frac = 0.1 — same held-out cones as every other run in the campaign, so the comparison is direct.
