---
type: comparison
status: draft
created: 2026-07-22
updated: 2026-07-22
tags: [FNO, UFNO, LocalFNO, reionization, benchmarks, power-spectrum]
---

# Density → x_HI: UFNO / LocalFNO vs. state of the art

Comparison of my FNO surrogates for the **matter density → neutral fraction
(x_HI)** map against published deep-learning / ML emulators of the reionization
field. Source metrics: `FNOs/ps_metrics.csv` (200 test cones, 15 k-bins,
z = 7/9/11), from `viz.power_spectrum_evaluation`.

## Metric definitions

- `abs_ratio_err` = |P_pred(k)/P_true(k) − 1|, transverse power spectrum. Lower = better.
- `1 − r` = cross-correlation deficit, r(k) = P_x / sqrt(P_pred P_true). Lower = better.
- `k_r_below_0.9` = wavenumber (h/Mpc) where r first drops below 0.9. Higher = better.
- Scale bins: large k < 0.3, mid 0.3–1, small k > 1 (h/Mpc).
- Stage = binned by mean neutral fraction x̄_HI (0.02–0.20 = late/mostly ionized;
  0.80–0.98 = early/mostly neutral).

## My models — aggregated "active" stage (x̄_HI 0.05–0.95)

| Metric | UFNO | LocalFNO |
|---|---|---|
| P(k) ratio err, large (k<0.3) | **0.126** | 0.208 |
| P(k) ratio err, mid (0.3–1) | **0.239** | 0.280 |
| P(k) ratio err, small (k>1) | **0.390** | 0.416 |
| r, large | **0.950** | 0.926 |
| r, mid | **0.874** | 0.852 |
| r, small | **0.772** | 0.751 |
| k where r<0.9 (h/Mpc) | **0.295** | 0.176 |

UFNO wins on every aggregate spectral metric.

## Stage dependence (UFNO)

| Stage (x̄_HI) | ratio err large | r large | ratio err small | r small |
|---|---|---|---|---|
| 0.02–0.20 (late) | 0.266 | 0.806 | 0.843 | 0.330 |
| 0.20–0.40 | 0.193 | 0.882 | 0.759 | 0.444 |
| 0.40–0.60 | 0.142 | 0.936 | 0.687 | 0.550 |
| 0.60–0.80 | 0.103 | 0.963 | 0.527 | 0.677 |
| 0.80–0.98 (early) | **0.062** | **0.980** | 0.268 | 0.860 |

Best in the mostly-neutral early regime; worst near full ionization (small
residual ionized structures dominate). Same qualitative behaviour for LocalFNO.

## Field-level metrics (training log, UFNO best epoch 26)

Relative L2 = 0.041, H1 = 8.28, BCE = 0.036 (test). LocalFNO field-level
metrics: see `checkpoints/checkpoints_3d_localfno/metrics.jsonl` on the cluster
(not synced locally).

## Literature comparison

| Work | Target | Large-scale P(k) | Coherence r | Notes |
|---|---|---|---|---|
| **UFNO (mine)** | density → x_HI | 12.6% (6.2% neutral stage) | 0.95 | 3D lightcone, FNO+U-net |
| **LocalFNO (mine)** | density → x_HI | 20.8% | 0.926 | windowed local Fourier U-net |
| Pundir+ 2024 (JCAP) | density δ → HI/HII | ≲10% for k≲1; HII <10% all scales | — | GPR f_coll + semi-numerical |
| CosmoUiT (Posture+ 2025, JCAP) | density+halo+params → 21cm | ~percent, both scales | — | ViT–U-Net hybrid |
| Masipa+ 2023 | density → ionization | "recovered well over all scales" | — | denoising U-Net; qualitative |
| Chardin+ 2019 (CRADLE, MNRAS) | star+gas density → t_reion | large near-perfect, small poor | — | autoencoder CNN |
| Diao+ 2025 (ApJ) | params → 21cm lightcone | ~percent small k, tens-% large k | — | multifidelity GAN |
| Bidenko+ 2024 | 21cm Tb → xHI (inverse) | — | >0.95 for k<0.5 | inverse direction |

## Takeaways

1. UFNO > LocalFNO on all aggregate spectral metrics; UFNO is the model to report.
2. UFNO is just behind the best density→field emulators (Pundir ~10% large-scale;
   CosmoUiT ~percent), and competitive with them in the mostly-neutral regime
   (6% ratio, r=0.98).
3. Small scales (k>1) are the weak spot — universal in this literature. CosmoUiT's
   percent-level small-scale result (attention mechanism) is the main thing beating
   UFNO there; a plausible direction for improvement.

## Caveats

- Paper numbers are largely as reported in abstracts; Masipa & Chardin are
  qualitative — exact per-scale values need the PDFs.
- Targets differ (HI density vs binary x_HI vs t_reion vs 21cm Tb); cross-rows
  are indicative, not identical benchmarks.
