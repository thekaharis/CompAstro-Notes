---
type: finding
title: "Structured-Transform Operator Findings"
created: 2026-07-28
updated: 2026-07-28
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - architecture/wno
  - architecture/whno
  - architecture/local-fno
  - finding/positive
status: active
related:
  - "[[Loss Objective and Operator Basis Sweep]]"
  - "[[Structured Transform Neural Operators]]"
  - "[[Fourier Neural Operator]]"
  - "[[Windowed Local-FNO U-Net Findings]]"
  - "[[z_re Map Training Results]]"
  - "[[Edge and Wall-Placement Losses]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[Bubble Size Distribution]]"
  - "[[FNO Lightcone Experimental Findings]]"
sources:
  - "[[.raw/reports/FINDINGS-2026-07-26.md]]"
  - "figures/xhi2d_all_variants.md (29 runs, 384 shared held-out slices)"
  - "figures/operator_variant_benchmark.json (A30 throughput benchmark)"
---

# Structured-Transform Operator Findings

> **Relation to [[Loss Objective and Operator Basis Sweep]]:** that note is the consolidated 2026-07-26 summary across all three tasks. This one is the detailed companion — it carries the per-run tables, the diagnostics, and the figures, and extends past 07-26 with material the summary predates.

> **Purpose:** results from making the operator basis a *slot* rather than an architectural commitment ([[Structured Transform Neural Operators]]). Wavelet (Haar) and Walsh–Hadamard operators are competitive with Fourier on the 2-D $x_\text{HI}$ task, and the best model so far uses **Walsh–Hadamard in the global bottleneck only**. The sharper structural result is that *which slot* gets the non-Fourier operator matters more than *which basis* it is.

## 1. Clean architecture comparison — 2-D $x_\text{HI}$ slices

All models trained and evaluated on the same 2-D task, split, and resolution (native slice prediction, **no z-interpolation**), 30 epochs each. `val/train` is the generalization gap.

| run | local / global | width | rank | lr | val RMSE | test RMSE | val/train |
|---|---|---|---|---|---|---|---|
| `whno_glob_lr3e4` | **fourier / hadamard** | 32 | 16 | 3e-4 | **0.1453** | **0.1502** | 1.01× |
| `localfno_lr3e4_e30` | fourier / fourier | 32 | 16 | 3e-4 | 0.1487 | 0.1540 | 1.08× |
| `whno_both_lr3e4` | hadamard / hadamard | 32 | 16 | 3e-4 | 0.1501 | 0.1550 | 1.01× |
| `localwno_lr3e4_w48r24` | wavelet / fourier | 48 | 24 | 3e-4 | 0.1502 | 0.1549 | 1.08× |
| `whno_loc_w48r24` | hadamard / fourier | 48 | 24 | 3e-4 | 0.1515 | 0.1561 | 1.10× |
| `whno_loc_natural` | hadamard / fourier *(natural order)* | 32 | 16 | 3e-4 | 0.1520 | 0.1582 | 1.06× |
| `whno_loc_lr3e4` | hadamard / fourier | 32 | 16 | 3e-4 | 0.1533 | 0.1601 | 1.07× |
| `localwno_lr3e4_r32` | wavelet / fourier | 32 | 32 | 3e-4 | 0.1563 | 0.1627 | 1.13× |
| `ufno_lr3e4_e30` | **U-FNO** | 32 | – | 3e-4 | 0.1595 | 0.1648 | **1.19×** |

### 1.1 The local/global split matters more than the basis

Six Walsh–Hadamard configurations varied which U-Net slot gets the operator (local, global, both), local mode count (6 vs 12), width (32 vs 48), and coefficient ordering (sequency vs natural).

- **Sequency vs natural ordering**: 0.1520 vs 0.1533 — a small effect.
- **Moving the operator from local-only to global-only**: ~5% — **more than any other knob in the sweep**.
- Every *local*-slot-Hadamard variant sits **below** plain LocalFNO (0.151–0.153); `localop(fourier/hadamard)` and `localop(hadamard/hadamard)` sit above it.

Combined with LocalWNO (wavelet-local, Fourier-global) landing *close to* rather than clearly ahead of LocalFNO, the pattern holds across both structured-transform families: **the global whole-field bottleneck is where a well-chosen non-Fourier operator pays off on this task, not the windowed local branches.**

This is a satisfying inversion of the original design intuition. The windowed local branches were introduced ([[Windowed Local-FNO U-Net Plan]]) precisely to buy sharp local structure — but they already see a *small* patch, where Fourier's global-smoothness prior does little damage. It is the whole-field bottleneck, where Fourier has to represent an entire 200 Mpc slice's worth of step functions in one basis, that a square-wave basis relieves.

### 1.2 U-FNO generalizes worst

val/train 1.19× vs ~1.01–1.08× for the local models — consistent with the same ordering on the $z_\text{re}$ task ([[z_re Map Training Results]]) and in 3-D. The U-FNO wins on absolute 3-D floor and loses on generalization gap everywhere it is measured.

### 1.3 Retraction: the earlier 2-D-vs-3-D LocalWNO lead was inflated

The earlier figures compared a 2-D LocalWNO against 3-D U-FNO/LocalFNO whose predictions were **z-interpolated onto each slice** — a handicap on the 3-D models. Out-of-sample WNO still led there (test-cone RMSE 0.214 vs U-FNO 0.241), but the same-task numbers above are the fair comparison and the lead largely evaporates.

WNO's robust advantage is **stage-localized**: strongest where the field is mostly neutral with sparse compact bubbles (wavelet sparsity is real there), weakest or negative in the nearly-fully-ionized regime. This is the same stage-dependence seen in [[Bubble Size Distribution]] and in the contrast-map band analysis.

## 2. Cost: parameters and inference throughput

Benchmark on an A30, batch 32, resolution 140, 13 input channels, 30 repeats (`figures/operator-benchmark_20260728/`):

| variant | params | ms/batch | slices/s | peak MiB | vs FNO |
|---|---|---|---|---|---|
| FNO (plain) | 17,878,209 | 44.2 | 724 | 1194 | 1.00× |
| U-FNO | **25,617,601** | 44.4 | 720 | 1157 | 1.01× |
| local fno / global fno | 932,321 | 52.7 | 608 | 696 | 1.19× |
| local fno / global wno | **411,617** | 53.2 | 602 | 694 | 1.20× |
| local fno / global whno | 539,105 | 52.8 | 606 | 695 | 1.20× |
| local wno / global fno | 792,033 | 67.6 | 473 | 696 | **1.53×** |
| local wno / global whno | 398,817 | 67.8 | 472 | 694 | 1.53× |
| **local whno / global fno** | 821,729 | **46.4** | **690** | 696 | **1.05×** |
| local whno / global whno | 428,513 | 46.4 | 689 | 694 | 1.05× |
| local sirenfno / global sirenfno | 470,433 | 55.3 | 578 | 695 | 1.25× |
| local cnn / global fno | 2,245,729 | **40.7** | **787** | 836 | **0.92×** |

Three things worth carrying forward:

1. **The local models are 20–60× smaller than the U-FNO** at better or equal accuracy, and use ~40% less peak memory. For a forward model that will be called inside an SBI loop ([[P2 Cross-Simulator Inference]]), this is the number that matters.
2. **Walsh–Hadamard is nearly free** (1.05× FNO) — no complex arithmetic. **Wavelet in the local slot is the expensive one** (1.53×), because the multilevel Haar decomposition runs inside every window.
3. **The CNN pairing is the fastest of all** (0.92× FNO) and much larger in parameters — a reminder that the real-space conv path is cheap in time and expensive in weights, the opposite trade to the spectral operators.

![[operator_params_vs_throughput.png]]

## 3. All 29 2-D runs on shared slices

A single re-evaluation of every completed 2-D run on the same 384 held-out test slices (`figures/operator-benchmark_20260728/xhi2d_all_variants_table.md`) is now the canonical 2-D leaderboard. It carries `wall`, `expwall`, `width`, and `blur` columns alongside RMSE, so accuracy and sharpness can be read together — see [[Edge and Wall-Placement Losses]], which is where the sharpness columns become the point.

> [!key-insight]
> The table's `width` column against its `TRUTH` row (1.46 px) is the single most useful summary the campaign has produced: **every** RMSE-competitive model sits at 2.7–3.1 px, and the only runs that reach truth-like width (1.16–1.43 px) are the ones that sacrificed RMSE to a wall-placement loss. There is no configuration yet that has both.

## 4. Open

- Does global-only Walsh–Hadamard transfer to **3-D** and to $z_\text{re}$? Untested — and the §1.3 lesson is explicit that a 2-D win is not a reliable predictor.
- The `cnn` operator in either slot has not been run to convergence as a baseline, despite being the cheapest and the one the [[Windowed Local-FNO U-Net Findings]] interpretation implicates ("the U-FNO's edge comes from its real-space conv path").
- Ordering (sequency vs natural) at larger truncation fractions.
