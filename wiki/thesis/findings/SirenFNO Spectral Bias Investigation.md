---
type: finding
title: "SirenFNO Spectral Bias Investigation"
created: 2026-06-21
updated: 2026-06-21
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - architecture/siren
  - architecture/u-fno
  - concept/spectral-bias
  - finding/diagnostic
status: active
related:
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Shi et al 2025 (SirenFNO)]]"
  - "[[Siren3D Residual Refinement Plan]]"
  - "[[Windowed Local-FNO U-Net Plan]]"
  - "[[Fourier Neural Operator]]"
  - "[[Wen et al 2022 (U-FNO)]]"
  - "[[Inference and ML]]"
sources:
  - "[[Thesis/FNOs/SIRENFNO results]]"
  - "run_info: sirenfno-detailed_20260621-191553_job3999451"
---

# SirenFNO Spectral Bias Investigation

> **Purpose:** Document (1) a new *mode-weight visualisation* diagnostic that makes the FNO/U-FNO low-frequency spectral bias directly measurable, (2) the quantified bias for U-FNO at 32 and 64 LOS modes, and (3) the 3-D SirenFNO experiment built to mitigate it. Result in one line: **SirenFNO removes the low-frequency collapse (its learned spectrum stays essentially flat across all modes), and beats the plain FNO on held-out error, but does not yet beat the U-FNO floor on aggregate metrics.**

This extends [[FNO Lightcone Experimental Findings]] (the density → $x_\text{HI}$ lightcone campaign) and gives the first *direct* measurement behind [[Spectral Mode Cutoff in FNOs]]. Same data, split (seed 42, 80/10/10 by cone), and infrastructure as that campaign.

---

## 1. The diagnostic: spectral mode-weight visualisation

The repeated mode-count null results in the main campaign told us *increasing* bandwidth didn't help, but not *how the model uses* the bandwidth it has. I instrumented every spectral layer to log the **per-mode RMS of the learned spectral-convolution weights** $R_\phi(k)$ at each epoch (CSV: `epoch, layer, axis, mode, rms_weight`; init logged as epoch −1). Three derived diagnostics:

- **LOS Fourier-weight profile** — RMS weight vs. mode index per layer; a flat profile = uniform use of the spectrum, a down-sloping profile = low-frequency preference.
- **Cutoff ratio** — high-mode RMS / low-mode RMS (outer-quarter vs. inner-quarter of the band). 1.0 = uniform; ≪1 = low-frequency collapse.
- **Low-25% fraction** — share of total spectral weight held by the lowest quarter of modes. 0.25 = uniform; →1 = collapse.

At initialisation all models sit at the uniform baseline (low-25% = 0.250) by construction; the question is what training does to it.

---

## 2. The bias is real and it develops during training (U-FNO)

The learnable per-mode weights of the U-FNO **collapse toward low modes within the first epoch** and stay there.

| Run (axis = LOS $k_z$) | mode-0 frac | low-25% frac @ init | low-25% frac @ ep0 | low-25% frac @ final | half-energy mode | peak mode |
|---|---:|---:|---:|---:|---:|---:|
| **U-FNO, 32 z-modes** | 0.094 | 0.250 | 0.603 | **0.521** | 7 / 31 | 1 |
| **U-FNO, 64 z-modes** | 0.055 | 0.250 | 0.731 | **0.357** | 27 / 63 | 0 |
| **SirenFNO, 64 modes** | 0.016 | 0.250 | 0.250 | **0.250** | 31 / 63 | flat |

Reading this: for the 32-mode U-FNO, the lowest **8 of 32** LOS modes carry **52%** of the spectral weight at convergence, and half the energy is reached by mode 7. The profile is steeply down-sloping with a deep mid-band trough; per layer the collapse ranges from `body.conv5` (mildest) to `body.conv3` (cutoff ratio reaching ≈0.10 — high modes ten times weaker than low modes).

![U-FNO 32-mode LOS Fourier-weight profiles — blue dashed = uniform init, red = final epoch; high modes collapse far below init](figures/sirenfno-spectral-bias_20260621/ufno32_z_profiles.png)

![U-FNO 32-mode cutoff diagnostic — high/low-mode RMS ratio falls from 1.0 (uniform) toward 0.1–0.45 over training](figures/sirenfno-spectral-bias_20260621/ufno32_z_cutoff_ratio.png)

The 64-mode U-FNO shows the same qualitative collapse (low modes dominant, sharp mid-band dip), only spread over more modes so the *low-25%* number is smaller in relative terms. The bias is not an initialisation artefact — it is **learned**, immediately, and is robust to giving the model more modes to work with. This is the mechanism behind the Act-3/Act-6/Act-7 null results: extra modes get down-weighted rather than used.

![U-FNO 64-mode LOS Fourier-weight profiles — same down-sloping collapse over a wider band](figures/sirenfno-spectral-bias_20260621/ufno64_z_profiles.png)

---

## 3. SirenFNO mitigates it: full-frequency learning

Following [[Shi et al 2025 (SirenFNO)]], I implemented a **3-D SirenFNO**: the Fourier kernel $R_\phi(k)$ is no longer a per-mode learnable table but is **generated mode-wise by a SIREN hypernetwork over the full grid**, so there is no truncation. Config (`run_info`): `modes=(64,64,64)`, hidden=32, 4 layers, SIREN hidden=64 / feature-dim=16 / ff-sigma=128 / ω₀=30, sigmoid output with temperature 2, LOS padding 8, same 13 input channels (density/10 + 1/(1+z) + 11 z-scored params).

The diagnostic on the same axes:

- **Low-25% fraction stays pinned at 0.250** across *every* epoch and every axis ($k_x,k_y,k_z\approx0.247$–0.250; radial shell 0.268) — i.e. the learned spectrum remains **uniform across all modes**, never collapsing to low frequencies.
- **Cutoff ratio hovers at ≈1.0** for $k_x,k_y,k_z$ (the per-layer radial-shell ratio dips modestly to ~0.7), versus the U-FNO's 0.1–0.45.
- The mode profiles are **flat** and sit *above* the initialisation line at all mode indices — the model lifts the whole spectrum rather than the low end.

![SirenFNO Fourier-weight profiles (k_x, k_y, k_z, radial shell) — essentially flat across the entire mode range at every logged epoch](figures/sirenfno-spectral-bias_20260621/sirenfno_profiles.png)

![SirenFNO cutoff diagnostic — outer-quarter/inner-quarter ratio stays near 1.0 (k_x/k_y/k_z); only radial-shell layers dip to ~0.7](figures/sirenfno-spectral-bias_20260621/sirenfno_cutoff_ratio.png)

![SirenFNO weight evolution heatmap — colour is roughly constant along the mode axis, varying mainly with epoch; no low-mode hot stripe](figures/sirenfno-spectral-bias_20260621/sirenfno_evolution.png)

**Verdict on the bias:** the SIREN kernel parameterization does exactly what the paper advertises — it eliminates the low-frequency collapse that the standard learnable-table FNO/U-FNO exhibit. Caveat: part of this flatness is *structural* (a smooth SIREN over $k$ resists concentrating on a few modes), so the right reading is "SirenFNO does not develop the bias," not "SirenFNO was pushed flat by the loss."

---

## 4. But it does not (yet) beat U-FNO on aggregate error

Held-out metrics, all on the identical seed-42 test split:

| Model | modes | epochs | test L² | test H¹ | test BCE | epoch time |
|---|---|---:|---:|---:|---:|---:|
| **Standard FNO** (+BCE) | (16,16,16) | 100 | 0.0570 | 11.64 | 0.0440 | 192 s |
| **SirenFNO** (stable) | (64,64,64) | 70 | **0.0501** | **9.82** | **0.0412** | 1015 s |
| **U-FNO** benchmark | (16,16,16) | 100 | 0.0397 | 7.87 | 0.0355 | 522 s |

So SirenFNO lands **between** the two: ~12% better L² and ~16% better H¹ than the plain FNO, but clearly above the U-FNO floor (which this 100-epoch benchmark pushes to test L² 0.0397 / H¹ 7.87, consistent with the Act-5 U-FNO at (0.0408, 8.27)). Field-level predictions are qualitatively good — bubble morphology and timing are captured (test cone 1: R² = 0.93, RMSE = 0.088).

![SirenFNO vs truth, test cone 1 — density, true x_HI, predicted x_HI, residual across redshift slices](figures/sirenfno-spectral-bias_20260621/sirenfno_comparison_test_cone1.png)

![SirenFNO scatter, test cone 1 — R² = 0.93, RMSE = 0.088](figures/sirenfno-spectral-bias_20260621/sirenfno_scatter_test_cone1.png)

### Caveats on the comparison (not yet apples-to-apples)

- **No local path.** SirenFNO here has *no* U-Net branch. The U-FNO's edge is its Gibbs-free local-convolution path — the very thing Act 5 identified as the lever. A fair test of "does removing spectral bias help?" needs **SirenFNO + U-Net** vs **U-FNO**.
- **Different mode count / epochs / per-epoch cost.** SirenFNO ran 64 modes × 70 epochs at ~2× the U-FNO's per-epoch cost; it had not fully plateaued.
- **Aggregate metrics hide where the error lives.** Whether full-frequency learning sharpens *bubble walls* specifically needs the boundary-band L²/H¹ and $P(k)$/$r(k)$ high-$k$ diagnostics from the [[Siren3D Residual Refinement Plan]] Stage-0 protocol — not just whole-volume L².

---

## 5. Interpretation and where this leaves the thread

The mode-weight diagnostic upgrades [[Spectral Mode Cutoff in FNOs]] from an *inference* ("extra modes didn't help, so they must be down-weighted") to a *measurement* ("the learned weights demonstrably collapse onto the lowest ~25% of modes within one epoch"). That is a genuinely new, citable result for the thesis: the FNO/U-FNO low-frequency bias on the 21cmFAST lightcone is now quantified, not assumed.

SirenFNO is the cleanest available demonstration that the bias is *fixable at the source* — a SIREN-parameterized full-grid kernel keeps the spectrum flat. What it has **not** yet shown is that fixing the bias improves the physically relevant target (sharp ionization fronts). On aggregate held-out error it sits below U-FNO, plausibly because it lacks the local path rather than because full-frequency learning is unhelpful.

### Next steps

1. **Boundary-aware evaluation** of the existing SirenFNO checkpoint: distance-to-front error histogram, boundary-band H¹, $P(k)$ and $r(k)$ vs $k$ and $z$. This tells us whether the flat spectrum buys high-$k$ fidelity even where whole-volume L² doesn't move. *Tool ready:* `Code/FNO v3/boundary_band_diagnostic.py` — signed-distance-to-front profiling (2-D per-slice transverse, physical Mpc), boundary-band L²/H¹, front 10–90 width, saturation calibration, and a paired cone-bootstrap to compare FNO/U-FNO/SirenFNO on the same split (`--checkpoints …` on the cluster, or `--manifest` on saved cubes; `--selftest` verifies the engine).
2. **SirenFNO + U-Net hybrid** — combine full-frequency global kernel learning with the Gibbs-free local path. This is the controlled test of the actual hypothesis.
3. Reconcile with the **[[Siren3D Residual Refinement Plan]]**: SirenFNO (replace the kernel) and Siren3D (residual head on frozen U-FNO) are two different SIREN-based attacks on the same boundary problem; results here favour running the boundary diagnostic *first* before committing compute to either.
4. Longer SirenFNO schedule and the **tensor-decomposed (CP/TT/Tucker) kernels** from the paper to cut the 64-mode cost.

---

## Reproducibility

Artifacts under `Thesis/FNOs/SIRENFNO results/`:

| Item | Contents |
|---|---|
| `Stable Siren Run/` | SirenFNO `metrics.jsonl` (70 ep) + `run_metadata.json` (model config, param normalisation, split) |
| `ufno benchmark run/` | U-FNO `metrics.jsonl` (100 ep, modes 16) + metadata |
| `standard FNO bce run benchmark/` | plain FNO `metrics.jsonl` (100 ep) + checkpoint |
| `spectral-weights-z_ufno-32modes/`, `…-64modes/` | per-mode RMS weight history (CSV) + profile/cutoff/evolution PNGs for U-FNO |
| `spectral-weights_SIRENFNO/` | same diagnostic for SirenFNO (all axes + radial shell) |
| `sirenfno-detailed_20260621-191553_job3999451/` | per-cone comparison/scatter/lightcone PNGs, `run_info.txt`, `z_cutoffs.txt` |

Curated figures copied into `wiki/thesis/findings/figures/sirenfno-spectral-bias_20260621/`. Metrics keys per epoch: `val_l2/h1/bce`, `test_l2/h1/bce`, `*_pred_mean/std/sat_low/sat_high`, `active_*_weight`, `last_grad_norm`.
