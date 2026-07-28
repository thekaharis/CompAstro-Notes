---
type: finding
title: "z_re Map Training Results"
created: 2026-07-28
updated: 2026-07-28
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - architecture/local-sirenfno
  - concept/target-reparametrization
  - finding/positive
  - finding/negative
status: active
related:
  - "[[Lightcone z_re Map Target]]"
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
  - "[[Windowed Local-FNO U-Net Findings]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Structured-Transform Operator Findings]]"
  - "[[Hedged Edges vs Blurred Edges]]"
  - "[[Shi et al 2025 (SirenFNO)]]"
sources:
  - "[[.raw/reports/FINDINGS-2026-07-26.md]]"
  - "checkpoints_zre_* (26 completed runs, 660 held-out cones)"
---

# z_re Map Training Results

> **Purpose:** first training results for the [[Lightcone z_re Map Target]] — the 2-D problem density lightcone $\to z_\text{re}(x,y)$ map. 26 completed runs across five architectures, evaluated on 660 held-out cones. Three findings that reach well beyond this task: **pure L² beats L²+H¹ by ~35%**, **SIREN-generated spectral weights rescue the Local-FNO**, and **the nominal loss weights everyone has been quoting were badly misleading**.

## 1. Headline results

**Metric convention.** `RMSE(z)` is pooled over all pixels in redshift units; `masked` restricts to pixels whose transition actually falls inside the cone. $R^2_\text{struct}$ is measured against the **within-cone** variance (the spatial pattern of the front); $R^2_\text{total}$ uses total variance, which is dominated by cone-to-cone timing and therefore saturates near 1 for every model — **only the struct column is informative**.

| run | kind | width | $\omega$ | lr | epochs | loss | RMSE(z) | masked | $R^2_\text{struct}$ | test/train | params |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `fno_l2only` | FNO | 64 | – | 5e-4 | 200 | **L²-only** | **0.1168** | 0.1634 | 0.766 | 1.19× | 17.9 M |
| `localsirenfno_l2only_bw32lr3e4` | LocalSirenFNO | 32 | 30 | 3e-4 | 300 | L²-only | **0.1233** | 0.1739 | 0.740 | 1.23× | **0.47 M** |
| `localsirenfno_l2only_bw32om60lr2e4` | LocalSirenFNO | 32 | 60 | 2e-4 | 300 | L²-only | 0.1262 | 0.1786 | 0.727 | 1.28× | 0.47 M |
| `sirenfno_l2only` | SirenFNO | 64 | 30 | 1e-4 | 200 | L²-only | 0.1344 | 0.1884 | 0.691 | 1.24× | 2.26 M |
| `localwno_bw32_l2_lr3e4` | LocalWNO | 32 | – | 3e-4 | 100 | L²-only | 0.1500 | 0.2180 | 0.615 | 1.29× | 0.79 M |
| `ufno_l2only` | U-FNO | 32 | – | 1e-4 | 200 | L²-only | 0.1505 | 0.2090 | 0.612 | 1.43× | 25.6 M |
| `checkpoints_zre` | FNO | 64 | – | 5e-4 | 200 | **L²+H¹** | 0.1822 | 0.2580 | 0.432 | 2.68× | 17.9 M |
| `ufno` | U-FNO | 32 | – | 1e-4 | 200 | **L²+H¹** | 0.2381 | 0.3378 | 0.029 | 1.79× | 25.6 M |
| `localfno_l2only` | LocalFNO | 16 | – | 1e-4 | 200 | L²-only | 0.3047 | 0.4206 | **−0.589** | 3.01× | 0.74 M |
| `localfno` | LocalFNO | 16 | – | 1e-4 | 200 | L²+H¹ | 0.3022 | 0.4113 | −0.563 | 2.24× | 0.74 M |

*(Full 26-row table in `.raw/reports/FINDINGS-2026-07-26.md`.)*

### 1.1 Pure L² beats L²+H¹ by ~35% — for every architecture

FNO 0.1822 → 0.1168; U-FNO 0.2381 → 0.1505. And critically, **dropping H¹ improved the H¹ metric itself**, so the H¹ term was not buying gradient fidelity — it was just a badly-scaled competing objective. The generalization gap collapses too (FNO 2.68× → 1.19×).

### 1.2 SIREN-generated weights transform the Local-FNO

The Local-FNO is the *worst* model on this task (RMSE 0.305, $R^2_\text{struct}$ negative — worse than predicting the cone mean, with a 3.0× train→test gap). Swapping its Fourier kernel for a SIREN hypernetwork ([[Shi et al 2025 (SirenFNO)]]) moves it to **second best** (0.123) and collapses the gap to 1.2×. This is by far the largest architectural effect measured anywhere in the campaign, and it does it with **54× fewer parameters than the U-FNO**.

> [!key-insight]
> The Local-FNO's problem was never locality — it was the low-frequency weight collapse documented in [[SirenFNO Spectral Bias Investigation]], which the windowed formulation inherits inside each window. Removing the collapse fixes the architecture. This substantially rehabilitates the negative verdict in [[Windowed Local-FNO U-Net Findings]].

### 1.3 The loss weights were lying

With absolute-mode losses at nominal 0.5 / 0.5, the H¹ term supplies **99.4%** of the 3-D training loss (raw H¹ $\approx$ 180× raw L²); in relative mode it is ~88%. **Every archived "L²+H¹" 3-D run is effectively H¹-dominated.** A genuinely balanced L²+H¹ has never been tested in 3-D. This retroactively reinterprets several earlier "H¹ reweighting did nothing" nulls in [[FNO Lightcone Experimental Findings]]: the reweightings were perturbations on an already saturated term.

## 2. Local-SirenFNO sweep (14 runs)

- **Width saturates at 32.** bw16 → bw24 → bw32 improves monotonically; **bw48 is consistently worse than bw32** at matched settings, even on 300-epoch schedules. Capacity is the strongest hyperparameter on this task — up to a hard ceiling.
- **Higher LR wins at higher width, but only over a full schedule.** At epoch ~50 the lr 1e-4 run led; the final ordering at bw32 is 3e-4 > 2e-4 > 1e-4. **Mid-run LR comparisons are unreliable** — a methodological lesson for the whole campaign.
- **$\omega = 60$ helps at low width, not high**: −6.5% at bw16, −2.4% at bw32/lr2e-4, neutral at bw48. $\omega = 15$ is clearly worse than the $\omega = 30$ default.
- **Bandwidth knobs hurt.** Local modes 6→8 (`m88`) and window 16→32 with 12 modes (`win32m1212`) both land below baseline.
- **Best config**: bw32, $\omega = 30$, lr 3e-4, pure L², 300 epochs → RMSE(z) 0.1233, beating the U-FNO baseline by 18% with ~54× fewer parameters. The plain FNO still leads by 5.6%.

> [!gap]
> **Do not transfer the bandwidth null to 3-D.** The $z_\text{re}$ target has 7–11× *less* small-scale transverse power than an $x_\text{HI}$ slice, so a bandwidth ceiling here says nothing about the 3-D task. The per-branch mode-weight diagnostic (§3) says the opposite for 3-D.

## 3. Mode-weight diagnostics — the LOS axis is the binding constraint in 3-D

A per-branch version of the mode-weight diagnostic from [[SirenFNO Spectral Bias Investigation]] was run on the 3-D and $z_\text{re}$ LocalFNO checkpoints (`figures/localfno-mode-weights_20260720/`). Edge/peak weight ratio:

| axis | ratio (bottleneck + decoders) | reading |
|---|---|---|
| x, y (transverse) | 0.03–0.20 | comfortably inside the retained band — headroom unused |
| **z (line of sight)** | **0.60–0.78** | **weight is pressed against the truncation edge** |

The binding bandwidth constraint in 3-D is the **line-of-sight direction** — exactly the axis the 2-D $z_\text{re}$ task cannot inform. `LOCALFNO_MODES_Z` (12, cap 17) and the bottleneck z modes (16, cap 33) both have headroom that has never been spent. This is the clearest untested 3-D-specific lever the campaign currently has, and it connects to the physical argument behind [[Warped LOS Grid Evaluation]] (LOS resolution is where the fronts live).

![[mode_weight_profiles_3d.png]]

## 4. Failure modes found

- **SirenFNO NaN (2-D).** Mostly-zero target → sigmoid saturation (100% of outputs at the rails by batch ~40) → on fully-clamped cones prediction and target are both exactly 0 → the L² *norm* is exactly 0 → `PowBackward0` (the sqrt) returns NaN → weights poisoned. **Loss-agnostic** (pure L² fails too), and gradient clipping cannot help because NaN clips to NaN. Fixes: decouple the DC mode from the SIREN-generated weights, and use a **linear output head** (`SIREN_OUTPUT_SIGMOID=0`, now the default).
- **Relative-mode L1+H2 froze.** Loss 2e11 at epoch 0, then constant 6.562121 from epoch 2 on: relative normalisation divides by a near-zero target norm, blows up the weights, saturates, and the gradients die. **Use absolute mode for L1/H2 on this target.**

Both failures share one root cause: the fitted $z_\text{re}$ map is mostly-clamped-to-zero on late reionizers (the sentinel problem flagged in [[Lightcone z_re Map Target]]), and near-zero target norms are poison for anything that normalises by them.

## 5. Infrastructure

- **z_re input cache** (`dataset/zre_input_cache.py`): per-cone density slices + params in one HDF5. Startup drops from ~2 h (re-reading 6600 raw lightcones) to minutes; verified byte-identical to raw reads.
- **`metrics.jsonl` + `run_metadata.json` for z_re runs** (`ZreLoggingTrainer`) so they appear on the dashboard; dashboard gained per-task pages (21 cm 3-D / z_re) and a config-comparison table that highlights only the parameters differing across selected runs.
- **Metadata backfill** (`util/backfill_zre_metadata.py`) reconstructs architecture fields for historical runs from job logs. $\omega$ was never logged, so it is inferred from the directory name and flagged `siren_omega_inferred_from_dirname` — a caveat on the historical sweep rows.
- `fno_zre.py` now records full architecture per model kind, supports `RESUME_DIR`, and applies `GRAD_CLIP_NORM` (default 1.0 for SIREN kinds).

![[fno_l2only_maps_sample000406.png]]

## 6. What this settles and what it does not

**Settles:**
- H¹ as configured was actively harmful, not merely neutral. Every future run should default to pure L² unless a balanced weighting is deliberately constructed.
- The Local-FNO family is viable — with SIREN weights.
- The LOS axis is where the 3-D bandwidth budget is actually tight.

**Does not settle:** whether the $z_\text{re}$ reparametrization achieves what [[Smooth-Target Reparametrization Plan]] wanted. **These numbers are in $z_\text{re}$-space, not reconstructed $x_\text{HI}$-space.** The plan's own success criterion — reconstructed 10–90% front width below the U-FNO's 10.7 Mpc, against truth 3.6 Mpc — has still not been evaluated. Until it is, the smooth-target thread is unresolved rather than successful.

## 7. Open questions

- Does pure L² also win in 3-D? (Being measured: `checkpoints_3d_localsirenfno` vs `..._l2only`.)
- Does the width saturation transfer? bw32/bw48 with $\omega = 60$ are running on the 3-D task.
- A **balanced** L²+H¹ in 3-D: queued as `..._bw32om60_relbal` (relative mode, weights 0.5 / 0.07).
- Spend the LOS bandwidth headroom (`LOCALFNO_MODES_Z`).
- LocalFNO (non-SIREN) overfitting: augmentation (random transverse rolls + D4 symmetries) and AdamW remain untried.
- **Run the reconstruction evaluation.** This is the one that decides the thread.
