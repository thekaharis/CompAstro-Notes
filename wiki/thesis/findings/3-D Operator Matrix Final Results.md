---
type: finding
title: "3-D Operator Matrix Final Results"
created: 2026-08-17
updated: 2026-08-17
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - architecture/u-fno
  - architecture/whno
  - architecture/sirenfno
  - architecture/local-fno
  - concept/loss-design
  - concept/boundary-sharpness
  - concept/spectral-bias
  - finding/positive
  - finding/negative
status: active
verdict: complete
related:
  - "[[Loss Objective and Operator Basis Sweep]]"
  - "[[Structured-Transform Operator Findings]]"
  - "[[Walsh-Hadamard Neural Operator]]"
  - "[[Granulometry (BSD) Auxiliary Loss]]"
  - "[[U-FNO BatchNorm Train-Eval Mismatch]]"
  - "[[LOS-Monotone Theta Key in 3-D]]"
  - "[[Edge and Wall-Placement Losses]]"
  - "[[Hedging Bias of Pointwise Losses]]"
  - "[[Warped LOS Grid Evaluation]]"
  - "[[Bubble Size Distribution]]"
  - "[[Square-Wave Basis for Ionization Fields]]"
  - "[[LOS Bandwidth as the 3-D Bottleneck]]"
sources:
  - "`checkpoints/checkpoints_3d_*/metrics.jsonl` (27 completed 3-D matrix runs)"
  - "`figures/final_eval/matrix/{rmse,bsd,edge3d,edgeslice,parity,ps}/` (final eval suite, jobs 4580652-4580663)"
  - "`figures/final_eval/matrix/speed/` (inference timing, job 4584895, A100 80GB)"
  - "`figures/final_eval/lossaxis/{edge3d,edgeslice}/` (loss-axis edge comparison)"
  - "`figures/edge_metrics_out/tsw_*_slice/` (transverse-only edge runs)"
  - "`figures/operator_variant_benchmark.json` (23-variant cost benchmark, a30, regenerated 2026-08-16)"
  - "`viz/rmse_r2_eval.py`, `viz/plot_params_vs_accuracy.py`, `slurm/final_eval_suite.sbatch`"
  - "`viz/inference_speed_eval.py`, `viz/plot_inference_speed.py` (added 2026-08-17)"
---

# 3-D Operator Matrix Final Results

The campaign result for the 3-D task: **density cube → $x_\text{HI}$ cube**,
`uniform_z_256` cache, batch size 1, **20-epoch budget for every cell** (one exception, §2). This
page carries the final held-out evaluation of the whole matrix; the mid-campaign
state and the $z_\text{re}$ / 2-D axes live in
[[Loss Objective and Operator Basis Sweep]].

Two axes were swept. The **architecture axis** is the `localop` local/global
operator pair (plus U-FNO as the dense reference); the **loss axis** is
plain L² / hybrid / BSD / expwall / expwall+theta, with a late transverse-only
variant. 27 cells completed.

> **Parameter counts on this page count complex Fourier weights as two real
> numbers.** `numel()` on a complex tensor counts one, which halves every
> FNO-family number and makes the Fourier and Walsh families incomparable.
> U-FNO is 202.9 M real (102.2 M complex-counted), `fno/fno` 20.4 M (10.2 M),
> `fno/whno` 5.71 M (3.94 M). All Walsh/wavelet models are real-valued and
> unaffected.

## 1. Held-out leaderboard — 200 test cones, 1.0 x 10^9 voxels

One best-in-class checkpoint per architecture combination, scored by
`viz/rmse_r2_eval.py` in a single streaming pass. `R2` is pooled over all
voxels; `R2_cone` is the per-cone mean with p16/p84, which is the honest
spread because the pooled figure is inflated by cone-to-cone timing variance.

| rank | local / global | loss | params | RMSE | R² | R²_cone (p16–p84) |
| --- | --- | --- | ---: | ---: | ---: | --- |
| 1 | **U-FNO** (dense ref.) | plain | 202,902,721 | **0.05781** | 0.9508 | 0.878 (0.798–0.965) |
| 2 | **sfno / swhno** | plain | **747,841** | **0.05914** | 0.9485 | 0.875 (0.786–0.967) |
| 3 | cnn / whno | plain | 3,468,081 | 0.06134 | 0.9446 | 0.844 (0.768–0.964) |
| 4 | cnn / swhno | plain | 1,405,921 | 0.06184 | 0.9437 | 0.842 (0.764–0.963) |
| 5 | whno / swhno | plain | 1,050,241 | 0.06544 | 0.9369 | 0.860 (0.736–0.963) |
| 6 | swhno / swhno | plain | 677,857 | 0.06632 | 0.9352 | 0.857 (0.729–0.962) |
| 7 | whno / whno | plain | 2,609,137 | 0.07405 | 0.9192 | 0.804 (0.671–0.949) |
| 8 | fno / whno | plain | 5,705,713 | 0.07594 | 0.9150 | 0.786 (0.682–0.942) |
| 9 | fno / fno | bsd | 20,385,777 | 0.07989 | 0.9060 | 0.795 (0.680–0.940) |
| 10 | wno / whno | plain | 2,182,129 | 0.08933 | 0.8824 | 0.754 (0.639–0.923) |

**The headline is rank 2.** `sfno/swhno` — a SIREN-generated Fourier local slot
against a SIREN-generated Walsh–Hadamard global slot — is **2.3% behind U-FNO on
RMSE with 271x fewer parameters**. `swhno/swhno` at 678 k params (299x smaller)
is 15% behind. The accuracy-per-parameter frontier is not close: every model
between ranks 2 and 6 is under 3.5 M parameters, and the two largest models in
the sweep sit at ranks 1 and 9.

**Read that as a statement about storage, not about compute.** §2.1 measures
inference on the same checkpoints: `sfno/swhno` is the **second slowest model in
the matrix**, 1.7x slower than the U-FNO it undercuts by 271x on parameters. If
the argument for a small operator was that it would be cheap to run, that
argument does not survive the measurement — the parameter saving is storage,
and the SIREN pays it back in compute by regenerating its kernel every forward
pass.

![[matrix_params_vs_rmse.png]]

![[matrix_params_vs_r2.png]]

**The Walsh–Hadamard global slot transfers to 3-D.** This was the open question
left by [[Square-Wave Basis for Ionization Fields]] and the 2-D result in
[[Structured-Transform Operator Findings]]. It holds: every `*/whno` and
`*/swhno` pairing beats the `fno/fno` cell, and the SIREN-generated variant
(`swhno`) beats the plain Walsh one in the global slot at matched local slot
(`whno/swhno` 0.0654 vs `whno/whno` 0.0741, **-11%**, while being *smaller*:
1.05 M vs 2.61 M). Sequency-truncated Walsh weights generated by a SIREN are
the best global operator tested on this task.

**The wavelet local slot is the worst cell and by far the most expensive**:
`wno/whno` is last on RMSE and took **460 min/epoch**, 7.2x the U-FNO and 3.8x
the Walsh cells, for 92 h of A100 time to reach the bottom of the table.

## 2. Cost

### 2.0 Training

Median epoch wall-clock over each run, one A100 (H200 for two late cells):

| local / global | params | min/epoch | epochs | total (h) |
| --- | ---: | ---: | ---: | ---: |
| cnn / swhno | 1,405,921 | 25.4 | 20 | 8.5 |
| cnn / whno | 3,468,081 | 25.4 | 20 | 8.5 |
| ufno | 202,902,721 | 63.6 | 20 | 21.2 |
| whno / swhno | 1,050,241 | 134.8 | 20 | 44.9 |
| swhno / swhno | 677,857 | 137.3 | 20 | 45.8 |
| fno / whno | 5,705,713 | 150.7 | 20 | 50.2 |
| fno / fno | 20,385,777 | 152.9 | 20 | 50.9 |
| sfno / swhno | 747,841 | 167.8 | 20 | 55.9 |
| wno / whno | 2,182,129 | 459.7 | **12** | 91.9 |

**The `wno` row is the one cell that did not get its 20 epochs.** At 7.7 h per
epoch it was cut at 12; its leaderboard entry is therefore a 12-epoch
checkpoint and its last place is not fully earned. It was also improving as
slowly as the others, so the conclusion is unlikely to move, but the row is not
budget-matched.

**Parameter count and wall-clock are nearly uncorrelated here.** U-FNO is the
largest model and the third *fastest*; `sfno/swhno` is 271x smaller and 2.6x
slower per epoch, because the SIREN hypernetwork regenerates the kernel every
forward pass. The `cnn` local slot (U-FNO's own U-Net path, unwindowed) is 2.5x
faster than U-FNO at 1.7% of the size. The windowed local operators pay for the
window loop, not for their weights.

The separate throughput benchmark (23 variants, matched a30, inference only)
agrees and isolates the same effect:

![[operator_params_vs_throughput.png]]

### 2.1 Inference

Training wall-clock confounds the optimiser, the data pipeline and the loss.
This is the clean measurement: the same trained checkpoints, forward pass only,
one A100 80GB, batch 1, whole 140x140x256 cubes, `LOCALFNO_PATCH_CHUNK_SIZE=64`
for every windowed model, median of 15 timed passes after 3 warmup with
`cuda.synchronize()` around each. Run-to-run spread is under 0.5% p16-p84 for
every model, so the ordering is not noise.

| local / global | params | ms/cube | slices/s | RMSE | peak MiB |
| --- | ---: | ---: | ---: | ---: | ---: |
| **cnn / whno** | 3,468,081 | **115.9** | **2208** | 0.06134 | 4345 |
| cnn / swhno | 1,405,921 | 116.2 | 2203 | 0.06184 | 4338 |
| **U-FNO** | 202,902,721 | 274.1 | 934 | **0.05781** | 10271 |
| whno / whno | 2,609,137 | 279.9 | 915 | 0.07405 | 3847 |
| fno / fno | 20,385,777 | 347.1 | 738 | 0.07989 | 3915 |
| fno / whno | 5,705,713 | 347.1 | 738 | 0.07594 | 3859 |
| whno / swhno | 1,050,241 | 389.6 | 657 | 0.06544 | 8283 |
| swhno / swhno | 677,857 | 437.4 | 585 | 0.06632 | 8282 |
| sfno / swhno | 747,841 | 458.1 | 559 | 0.05914 | 8285 |
| wno / whno | 2,182,129 | 625.2 | 410 | 0.08933 | 3846 |

![[matrix_inference_speed_vs_size.png]]

**Parameter count carries no information about inference cost.** Pearson
correlation between $\log_{10}$ params and throughput is **0.011**. The rank
correlation is not merely absent but mildly *positive* (Spearman **0.53**) — if
anything the larger models are the faster ones. U-FNO carries **299x** the
parameters of `swhno/swhno` and runs **60% faster**. The intuition that a
smaller operator is a cheaper one is simply false on this task, in both
directions.

**The global operator is free.** `fno/fno` and `fno/whno` time at **347.07 and
347.06 ms** — identical to 0.005% — across a 14.7 M parameter difference. That
is the 2-D benchmark's "<1% between global slots" reproduced on trained 3-D
cubes, and it explains the null correlation above: essentially all of the cost
lives in the local slot, which is also the slot §5 finds sets bubble size. The
local/global split governs cost and morphology; the global basis governs
accuracy.

**What the windowed operators pay for is the window loop.** Every windowed
local slot (`whno`, `swhno`, `sfno`, `wno`) is slower than the unwindowed dense
U-FNO despite being 2-3 orders of magnitude smaller, and the `cnn` local slot —
U-FNO's own U-Net path without the window machinery — is **2.4x faster than
U-FNO at 1.7% of its size**. `LOCALFNO_PATCH_CHUNK_SIZE` is a real tuning knob
that only these models have, so their timings are movable in a way U-FNO's and
the CNN's are not; it was held fixed at the eval-config value rather than tuned
per model.

**Memory does not track parameters either.** U-FNO peaks at 10.3 GB, 2.4x the
`cnn` cells, but the `bw48om60` cells at ~1 M parameters peak at 8.3 GB — 2.2x
the 2.6 M-parameter `whno/whno`. Activation shape and window chunking set peak
memory, not weight count.

![[matrix_inference_speed_vs_rmse.png]]

**The speed-accuracy Pareto front has only two members: `cnn/whno` and
U-FNO.** Everything else is beaten on both axes at once — including all four
Walsh/SIREN cells that lead the parameter-efficiency ranking. `cnn/whno` is
2.4x faster than U-FNO, third on RMSE (+6.1%), and 2.4x lighter on peak memory;
U-FNO buys the last 6% of accuracy for 2.4x the time and 2.4x the memory.

**This reorders the practical recommendation from §1.** On parameters the answer
was `sfno/swhno`; on inference cost at equal accuracy it is `cnn/whno`. The two
disagree because they measure different scarcities, and for a forward model
called repeatedly inside an SBI loop it is throughput, not checkpoint size, that
binds.

## 3. Loss axis, on matched architecture

All 20-epoch, seed-matched within an architecture row. `val_l2` at best epoch:

| local / global | plain | hybrid | bsd | expwall | expwall+theta |
| --- | ---: | ---: | ---: | ---: | ---: |
| ufno (gnorm) | **0.0471** | 0.0490 | 0.0502 | 0.0592 | 0.0616 |
| fno / whno | **0.0611** | 0.0650 | — | 0.0721 | 0.0689 |
| whno / whno | **0.0591** | 0.0647 | 0.0643 | 0.0704 | — |
| wno / whno (12 ep) | **0.0701** | 0.0730 | — | 0.0780 | — |

**The ordering plain < hybrid < bsd < expwall is consistent across all four
architectures.** Every added term costs whole-volume accuracy, in the same
sequence, regardless of the operator. The one exception to a fully monotone
ordering is the theta cell: it is the *worst* on U-FNO (0.0616) but slightly
*better* than plain expwall on `fno/whno` (0.0689 vs 0.0721) — consistent with
[[LOS-Monotone Theta Key in 3-D]]'s finding that the two architectures fit
opposite theta schedules on the same data, i.e. the fit is unconstrained. This
is not a tuning failure — it is what a pointwise L² metric is supposed to do
when the extra term pulls the prediction off the conditional mean
([[Hedging Bias of Pointwise Losses]]).

**But whole-volume accuracy was the wrong scoreboard for these terms.** Judged
on what they were designed to do, two of them work — see §5 and
[[Granulometry (BSD) Auxiliary Loss]].

### Transverse-only (XY-slice) edge losses

Added late, on the hypothesis that per-slice sharpness is the real target and
LOS sharpness is secondary. `transverse_signed_distance` folds the LOS axis into
the batch dimension so the distance transform is computed per XY slice.

| run | val_l2 | slice-mode front width (Mpc) |
| --- | ---: | ---: |
| ufno hybrid (3-D wall) | 0.0490 | 8.728 |
| ufno hybrid (transverse) | 0.0513 | 8.736 |
| fno/whno hybrid (3-D wall) | 0.0650 | 25.345 |
| fno/whno hybrid (transverse) | 0.0683 | 19.861 |

**Negative for U-FNO, mildly positive for fno/whno.** Restricting the wall term
to XY slices changes the U-FNO front width by 0.008 Mpc (nothing) while costing
4.7% val_l2. On fno/whno it buys a real 22% width reduction for 5% val_l2. The
asymmetry is unexplained; the plausible reading is that the U-FNO's U-Net path
already resolves the transverse direction, so the restriction removes gradient
signal without adding any.

## 4. The metric that the loss work was actually aimed at

`front_width` is the 10–90% rise distance across the ionization front, measured
in slice mode against **truth 3.60 Mpc**. This is the number the expwall family
was built for, and it was not measured until the end of the campaign — the loss
variants were being judged by `val_l2`, which is the metric they are guaranteed
to lose on.

| run | loss | val_l2 | front width (Mpc) |
| --- | --- | ---: | ---: |
| ufno | plain | **0.0471** | 16.32 |
| ufno | **hybrid** | 0.0490 | **8.72** |
| ufno | expwall | 0.0592 | 12.47 |
| fno/whno | plain | **0.0611** | (no fit) |
| fno/whno | hybrid | 0.0650 | 25.34 |
| fno/whno | expwall | 0.0721 | 23.32 |

**Hybrid halves the U-FNO front width — 16.32 → 8.72 Mpc — for 4% of val_l2.**
Pure expwall, without the L² anchor, is *worse* than hybrid on both axes at
once, which is the same anchoring result found for the BSD term: transport-style
and morphological terms need a pointwise anchor and are not viable alone.

That leaves an explicit frontier rather than a winner: **0.0471 at width 16.3,
or 0.0490 at width 8.7.** For a forward model feeding SBI on summary statistics
the second point is very likely the better one, and the thesis should choose it
deliberately.

**The ceiling is the cache, not the loss.** [[Warped LOS Grid Evaluation]]
measured that `uniform_z_256` recovers only **12.7% of true front sharpness**
and misses 11.7% of fronts outright. 8.72 Mpc against truth 3.60 Mpc is
therefore not obviously far from what this cache can represent, and no loss
term can close the remainder. The warped-cache comparison **on reconstructed
front width** is still the unrun experiment that would settle this.

## 5. Morphology — bubble size distribution

Relative mean bubble-size bias per reionization stage
(`figures/final_eval/matrix/bsd/`), 200 cones, restricted-mean estimator:

| local / global | 0.02–0.20 | 0.20–0.40 | 0.40–0.60 | 0.60–0.80 | active 0.05–0.95 | JS (active) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| cnn / swhno | +0.037 | **-0.018** | **-0.006** | **-0.012** | **+0.006** | 0.0069 |
| cnn / whno | **+0.014** | -0.046 | -0.033 | -0.032 | -0.009 | 0.0078 |
| ufno | +0.092 | +0.082 | +0.085 | +0.048 | +0.057 | **0.0064** |
| sfno / swhno | +0.030 | -0.061 | -0.142 | -0.149 | -0.074 | 0.0085 |
| fno / fno (bsd) | -0.134 | -0.236 | -0.238 | -0.209 | -0.141 | 0.0199 |
| whno / swhno | +0.056 | -0.052 | -0.346 | -0.414 | -0.179 | 0.0242 |
| swhno / swhno | +0.054 | -0.134 | -0.372 | -0.434 | -0.206 | 0.0274 |
| whno / whno | -0.121 | -0.177 | -0.346 | -0.414 | -0.251 | 0.0305 |
| fno / whno | -0.130 | -0.269 | -0.272 | -0.304 | -0.212 | 0.0180 |
| wno / whno | -0.073 | -0.269 | -0.487 | -0.443 | -0.313 | 0.0415 |

![[matrix_bsd_summary.png]]

**The RMSE ranking and the morphology ranking are different rankings.** The
`cnn` local slot is third and fourth on RMSE but produces by far the most
faithful bubble sizes — `cnn/swhno` is within 2% of truth at every stage from
0.20 to 0.80 and +0.6% on the active band, against U-FNO's +5.7%. The pure Walsh
models (`whno/whno`, `swhno/swhno`) systematically **undersize** bubbles by 35–43%
in mid-reionization while scoring respectably on RMSE, and `wno/whno` is wrong
by half.

The sign is informative: U-FNO makes bubbles **too large**, everything with a
Walsh global slot and no CNN local slot makes them **too small**. Only the CNN
local slot gets the scale right, which points at the local operator — not the
global basis — as what sets bubble size.

## 6. Parity — the hedging bias, everywhere

Conditional prediction distribution binned by true $x_\text{HI}$
(`figures/final_eval/matrix/parity/`):

| local / global | bias, true $x_\text{HI}$ 0.02–0.10 | bias, > 0.90 | sign flip at |
| --- | ---: | ---: | ---: |
| ufno | **+0.188** | -0.003 | 0.42 |
| sfno / swhno | +0.197 | -0.003 | 0.40 |
| cnn / swhno | +0.202 | -0.003 | 0.56 |
| cnn / whno | +0.205 | -0.003 | 0.56 |
| whno / swhno | +0.218 | -0.004 | 0.42 |
| swhno / swhno | +0.229 | -0.004 | 0.42 |
| fno / fno (bsd) | +0.226 | -0.003 | 0.56 |
| whno / whno | +0.240 | -0.005 | 0.52 |
| fno / whno | +0.249 | -0.005 | 0.54 |
| wno / whno | +0.289 | -0.006 | 0.56 |

![[matrix_parity_overlay.png]]

**Every model in the matrix is strongly biased high in nearly-ionized gas and
essentially unbiased in neutral gas.** The best model has a **+0.19 bias at true
$x_\text{HI}$ ≈ 0.05** — a factor of ~4 error in the quantity — while its bias
above 0.90 is -0.003. This is exactly the asymmetric hedge predicted by
[[Hedging Bias of Pointwise Losses]]: most of the volume is neutral, so the
conditional mean in a mostly-neutral neighbourhood is pulled up, and the models
never commit to "ionized" until the truth is past ~0.4–0.56.

**The ordering of this bias tracks the RMSE ordering almost perfectly.** That
is the uncomfortable part: nothing in the matrix trades RMSE for calibration in
the low-$x_\text{HI}$ regime — the better models are simply better everywhere,
and none of them are *unbiased* where it matters for the ionized-bubble
interiors.

## 7. Power spectrum

Two different things are measured and they disagree about who is best
(`figures/final_eval/matrix/ps/`, active band 0.05–0.95):

| local / global | $k$ where $r < 0.9$ | ratio err, $k > 1$ |
| --- | ---: | ---: |
| ufno | **0.184** | 0.477 |
| cnn / swhno | 0.180 | 0.454 |
| cnn / whno | 0.140 | 0.475 |
| sfno / swhno | 0.115 | 0.266 |
| fno / whno | 0.071 | 0.345 |
| fno / fno (bsd) | 0.064 | **0.075** |
| wno / whno | 0.055 | 0.359 |
| whno / swhno | 0.048 | 0.072 |
| swhno / swhno | 0.036* | 0.065 |
| whno / whno | 0.036* | 0.122 |

\* floored — already below $r = 0.9$ in the first measured $k$ bin.

![[matrix_ps_overlay.png]]

**Phase coherence and amplitude fidelity are anti-correlated across the matrix.**
U-FNO holds cross-correlation to the highest $k$ but is wrong about small-scale
*amplitude* by 48%; the BSD-trained `fno/fno` and the Walsh models reproduce
amplitude to within 6–12% while losing coherence almost immediately. The Walsh
models get the right amount of small-scale power **in the wrong places** —
consistent with the BSD undersizing in §5 and with a square-wave basis producing
plausible-looking but misregistered structure.

For SBI on power-spectrum summaries this is the more relevant axis than RMSE,
and it inverts the leaderboard. **No model in the matrix is good at both.**

## 8. What this establishes

1. **The Walsh–Hadamard global slot transfers from 2-D to 3-D**, and the SIREN
   -generated variant is the best global operator tested.
2. **271x fewer parameters costs 2.3% RMSE** — but that is a storage result,
   not a compute one. `sfno/swhno` at 748 k wins accuracy-per-parameter and is
   the **second slowest model in the matrix**. On inference cost at equal
   accuracy the answer is instead **`cnn/whno`**: 2.4x faster than U-FNO, 2.4x
   lighter on memory, +6.1% RMSE. `cnn/whno` and U-FNO are the only two members
   of the speed-accuracy Pareto front.
3. **Parameter count predicts neither wall-clock nor memory.** Pearson
   correlation between log-params and inference throughput is **0.011**, and
   the rank correlation is mildly *positive*. Cost is set by the window loop
   and by SIREN kernel regeneration; the **global operator is free** (`fno/fno`
   and `fno/whno` are identical to 0.005% across 14.7 M parameters).
4. **Auxiliary loss terms all cost val_l2, consistently, across four
   architectures** — and two of them deliver on their own axis anyway: hybrid
   halves front width (§4), BSD halves bubble-size bias
   ([[Granulometry (BSD) Auxiliary Loss]]).
5. **The four metric families rank the models differently.** RMSE, bubble size,
   $P(k)$ amplitude and $P(k)$ coherence produce four different leaders. The
   thesis has to pick a scoreboard on physical grounds rather than inherit
   `val_l2`.
6. **Universal high bias in nearly-ionized gas** (+0.19 at best), untouched by
   any architecture or loss in the sweep.

## Open

- **Warped cache vs uniform cache on reconstructed front width.** Still the
  single most valuable unrun experiment: §4's frontier is bounded by a 12.7%
  sharpness ceiling that no loss can lift.
- **`cnn/swhno` + hybrid.** The CNN local slot has the best morphology and the
  hybrid term has the best front width; the combination was never run.
- **Why transverse-only helps `fno/whno` and not U-FNO** (§3).
- **The FNO+WHNO ensemble** proposed by [[Pérez Cuadrado et al 2025 (WHNO)]] is
  still untried, and §7's coherence/amplitude anti-correlation is now a concrete
  motivation for it — the two bases fail in complementary ways.
- Longer budgets. Every number here is a 20-epoch number and no cell had
  visibly converged.
