---
type: meta
title: "Hot Cache"
updated: 2026-09-13T00:00:00
---

# Recent Context

## Last Updated

2026-09-13 — Wrote [[Learned Waveform Basis Operator]]: given a learned basis, the model **rediscovers Fourier** from four different starts, and the adaptive basis has no headroom on 2-D $x_\text{HI}$. On 2026-09-12, settled whether the U-FNO's 3-D gains were line-of-sight gains: **they are not** — see [[3-D Operator Matrix Final Results]] §7.1. On 2026-08-23, reanalysed the completed matrix evaluation and wrote [[Phase Coherence and Bubble Size Bias]]: small-scale **phase** accuracy, rather than small-scale amplitude, controls bubble morphology. On 2026-08-17, the 3-D architecture × loss matrix was fully evaluated on held-out cones; the results are in [[3-D Operator Matrix Final Results]]. Earlier in this cycle, I wrote up [[Granulometry (BSD) Auxiliary Loss]], [[U-FNO BatchNorm Train-Eval Mismatch]], and [[LOS-Monotone Theta Key in 3-D]].

## Key Facts From The Matrix (2026-08-17)

- **Small models have the best accuracy per parameter.** `sfno/swhno` (SIREN-Fourier local, SIREN-Walsh global) has **RMSE 0.0591 versus U-FNO's 0.0578 at 271x fewer parameters** (748 k versus 202.9 M), on 200 test cones / 10^9 voxels. `swhno/swhno` at 678 k (299x smaller) is 15% behind. Ranks 2–6 are all under 3.5 M parameters.
- **The Walsh-Hadamard global slot transfers to 3-D**, and SIREN-generating its weights beats plain Walsh by 11% *while being smaller* (1.05 M vs 2.61 M). Best global operator tested on either task.
- **Parameter counts were wrong by ~2× for the whole FNO family** — `numel()` counts a complex weight as one number. U-FNO is **202.9 M**, not 102.2 M. Walsh/wavelet models are real and unaffected, so earlier size comparisons favoured Fourier.
- **Model size does not predict wall-clock time.** U-FNO is the largest model but the third fastest. `sfno/swhno` is 271× smaller and 2.6× slower because SIREN regenerates the kernel on every pass. The wavelet local slot takes **460 min/epoch**, is last in the table, and was the only cell that missed its 20-epoch budget.
- **Auxiliary losses cost `val_l2` in the same order across all four architectures** (plain < hybrid < bsd < expwall; only the theta cell is inconsistently ordered) — and two of them still deliver: **hybrid halves the U-FNO front width, 16.32 -> 8.72 Mpc** (truth 3.60) for 4% val_l2, and BSD halves bubble-size bias. Pure expwall without an L2 anchor loses on *both* axes.
- **The four metric families have different leaders**: RMSE -> U-FNO; bubble size -> `cnn/swhno` (within 2% at every stage, versus U-FNO +5.7%); $P(k)$ amplitude -> `swhno/swhno` (6.5% versus U-FNO 48%); $P(k)$ coherence -> U-FNO. **Phase coherence and amplitude fidelity are anti-correlated**, which motivates the untried FNO+WHNO ensemble.
- **The local operator sets bubble size**, not the global basis: U-FNO oversizes, every Walsh-global/no-CNN-local model undersizes by 35-43%, only the CNN local slot gets the scale right.
- **Every model is +0.19 biased high at true $x_\text{HI} \approx 0.05$** and unbiased above 0.90, flipping sign at 0.40-0.56. The ordering tracks RMSE exactly — nothing in the sweep trades accuracy for calibration in ionized gas.
- **Transverse-only edge losses**: nothing for U-FNO (8.728 -> 8.736 Mpc for 4.7% val_l2), 22% width gain for `fno/whno`. Unexplained asymmetry.

## Inference Cost (2026-08-17)

- **Parameter count says nothing about inference cost.** Pearson(log params, throughput) = **0.011**; rank correlation mildly *positive*. U-FNO is **299x** the parameters of `swhno/swhno` and **60% faster**.
- **The parameter-efficiency headline is storage-only.** `sfno/swhno` (271x smaller, +2.3% RMSE) is the **second slowest model in the matrix**. On inference cost at equal accuracy the answer is **`cnn/whno`** — 2.4x faster than U-FNO, 2.4x less peak memory, +6.1% RMSE.
- **Speed-accuracy Pareto front = {`cnn/whno`, U-FNO}** only. Every Walsh/SIREN cell is beaten on both axes.
- **The global operator is free**: `fno/fno` and `fno/whno` differ by 0.005% in time across 14.7 M parameters. Cost lives in the local slot — which §5 also finds sets bubble size.
- Memory tracks activation shape, not weights: U-FNO 10.3 GB, the ~1 M-param `bw48om60` cells 8.3 GB, the 2.6 M-param `whno/whno` 3.8 GB.

## Learned Waveform Basis (2026-09-13)

- **The learned basis converges to Fourier from every init tried.** Identity local slot, so the global operator is the only one left: sine is a fixed point, square 0.914 → **0.9997**, sawtooth 0.781 → **0.9995**, random partial (one axis 0.9972). Both spatial axes agree to four decimals.
- **Not an artifact**: 15 harmonics kept at $k=1$ (full Nyquist for 31 bins) so a square was representable throughout; table norm conserved to 1.5-5% while the peak goes 1.0 → 1.42 $\approx\sqrt{2}$, the equal-RMS sine.
- **No headroom**: every arm within 0.0013 of a plain FNO (0.1113-0.1126), at 715 k vs 779 k parameters. Positive result about the *problem*, negative result for the *method*.
- **The square-wave intuition fails.** Given the freedom to build a two-phase basis for a two-phase field, the model discards it — so the Walsh wins elsewhere are not evidence for a square basis.
- **The discontinuity was never the barrier — the local branch was.** Sawtooth travelled furthest and still arrived; with a windowed local branch present it stalls at ~0.89 across three seeds. (This falsified my own prediction.)
- **Separate analysis/synthesis banks: null** (+0.0002 / -0.0005, inside the floor) *despite* real divergence — r = 0.67 at encoder0, 0.99 at the bottleneck. Freedom used where it does not matter.
- **The windowed local branch costs ~4x wall clock** (1:20-1:33 vs 5:54-6:18) and 13% of parameters for at most one floor width.
- **Replicate noise floor for 2-D: sd 0.0002-0.0009 val_l2**, from a 21-run seeded control matrix. Every claim above is judged against it.
- Caveat throughout: **single seed per identity arm**, 2-D and bottleneck only.

## Anisotropy of the U-FNO Advantage (2026-09-12)

- **The U-FNO's 3-D spectral advantage is transverse, not line-of-sight.** Decomposing its cylindrical advantage over the other eight matrix models: $k_\parallel$ explains **under 14.9% in all 18 comparisons** (usually under 7%), $k_\perp$ **43–94%**.
- The amplitude gain is a horizontal band (flat in $k_\parallel$); the coherence gain is a vertical stripe at $k_\perp \gtrsim 1$. That is the **transpose** of the pattern a LOS-concentrated gain would make.
- **Closes the transverse-only asymmetry** (§3): the U-Net path has already saturated the transverse direction, so a transverse-only term has nothing left to buy on U-FNO (8.728 → 8.736) while `fno/whno` gained 22%.
- Consistent with the `cnn` local slot winning on **Darcy**, which has no line of sight — the mechanism is isotropic local bandwidth. $z$ is where this dataset has the headroom, not what the architecture is doing.
- **Limit**: $k_\parallel$ only sampled to $0.16\ h\,$Mpc$^{-1}$ (vs 1.9 for $k_\perp$). The small-scale LOS band is untested — finer LOS binning is the follow-up.
- U-FNO is **not** the cylindrical leader: `cnn/swhno` and `cnn/whno` beat it on amplitude; it still leads all nine on decoherence.

## Phase / BSD Connection (2026-08-23)

- **$r(k)$ at $k > 1$ predicts bubble-size bias at $\rho = +0.88$** ($R^2 = 0.88$, zero bias at $r \approx 0.73$); JS divergence at $-0.92$. Survives controlling for RMSE ($+0.71$) and ionized-fraction error ($+0.79$).
- **Small-scale amplitude predicts nothing** ($-0.27$, $p = 0.49$; partial $+0.35$ given $r$). "More detail" does not fix the BSD — the detail the Walsh cells add is wrong-phase power. This **revises the §5 reading**: the local slot appeared to set bubble size because local slots differ in how much decorrelated power they inject.
- **Fragmentation, not under-ionization**: at $\bar{x}_\text{HI} = 0.4$–$0.6$ every cell gets the ionized area right to 1–3% while the MFP bias spans $-0.006$ to $-0.487$.
- **Mediator is the $k^2$-weighted level-crossing rate** $\nu = \sigma_1/\sigma_0$, $\rho = -0.83$ against the MFP ratio. MFP is a first-passage statistic — the shortest obstruction dominates the mean, which is why $k > 1$ is the band that matters.
- Caveat: the CNN cells' near-zero bias is **partly cancellation** ($\nu \approx 0.86$, too few boundaries); quote their JS/Wasserstein instead.

## Earlier Context (2026-07-28)

2026-07-28 — Two parallel write-up passes covered the same period. The 07-26/27 pass produced [[Loss Objective and Operator Basis Sweep]], [[Contrast Map Sharpening]], [[Hedging Bias of Pointwise Losses]], [[Contrast Map]], [[Walsh-Hadamard Neural Operator]], and three gaps. The 07-28 pass added [[Edge and Wall-Placement Losses]], [[Warped LOS Grid Evaluation]], [[Bubble Size Distribution]], [[Sliced Wasserstein Edge Loss]], [[Structured Transform Neural Operators]], and two detailed companions ([[z_re Map Training Results]], [[Structured-Transform Operator Findings]]). Duplicate entries were consolidated under the earlier names.

## Key Recent Facts

- **The source of the softness is now understood.** [[Hedging Bias of Pointwise Losses]] shows that L² is *minimised* by a hedged ramp when edge position is uncertain, and H¹ repeats the same behaviour one derivative up. The same sharpening map fixes band-limited truth (**−9.28%**) but does **exactly nothing** to the model (**+0.00%**) at matched width, so the softness is not ordinary blur. About 86% of the model's error is not blur.
- **One loss does move the front width.** [[Edge and Wall-Placement Losses]]: `ExponentialWallDistance` reaches **1.16 px against truth 1.46**, where every RMSE-optimal model sits at ~2.9, for ~22% RMSE and high-$k$ power ratio 0.51 → 0.82. The earlier expectation that SWD would be the winner was wrong. The important distinction is *absolute* rather than *squared* error: a weighted conditional **median**, which is binary for a binary field, makes the loss pick a side instead of averaging. Hedging is a property of pointwise **squared** losses, not pointwise losses in general.
- **Displacement blindness, quantified.** Over 4 → 48 px of wall misplacement, L² changes by 3.5×, H¹ by 2.9×, **H¹ seminorm and H² by 1.00×**, and signed-distance by 144×. H¹'s entire placement sensitivity comes from the L² term inside it.
- **The nominal loss weights were misleading.** With absolute-mode weights of 0.5/0.5, **H¹ supplies 99.4%** of the 3-D loss; every archived "L²+H¹" 3-D run was H¹-dominated. On $z_\text{re}$, **pure L² beats L²+H¹ by ~35% for every architecture — and improves the H¹ metric itself.**
- **The best 2-D model uses Walsh–Hadamard only in the *global* slot** (0.1453 versus LocalFNO 0.1487 and U-FNO 0.1595); the local/global split matters more than the basis. Local models are **20–60× smaller than the U-FNO** at better accuracy and ~40% less peak memory ([[Structured-Transform Operator Findings]]).
- **SIREN weights rescue the Local-FNO** on $z_\text{re}$ (0.305 → 0.123, gap 3.0× → 1.2×) at 54× fewer params than the U-FNO.
- **The cube cache discards most of the fronts before training sees them.** [[Warped LOS Grid Evaluation]]: `uniform_z_256` recovers **12.7%** of true front sharpness and misses **11.7%** of fronts; `warped_256` gets 33.2% / 4.9% at the same budget and **beats uniform-$z$ at 512 slices**. This bound is independent of the objective problem — both are real.
- **The morphology check is in.** [[Bubble Size Distribution]] finds that the best U-FNO makes bubbles **+6.8% / +9.3% too large** at $\bar{x}_\text{HI}$ 0.02–0.20 / 0.20–0.40, crossing to −2.6% at the end. JS ≤ 0.017 throughout, so the shape is right while the scale drifts.
- **LOS is the one axis where bandwidth may still bind**: edge/peak mode weight 0.60–0.78 on $z$ vs 0.03–0.20 transverse ([[LOS Bandwidth as the 3-D Bottleneck]]).

## Open Questions and Next Experiments

**Completed recently:** the epoch-29 sharpness table (the 29-run shared-slice leaderboard with `width`/`blur`), the transport-versus-steepness comparison (expwall, not SWD), the warped-grid real-cone evaluation, and the first $z_\text{re}$ training runs.

- ~~**Run expwall in 3-D.**~~ **Done** — see [[3-D Operator Matrix Final Results]] §3-4. Expwall alone costs 26% val_l2 and is beaten on *both* axes by the hybrid, which halves front width (16.32 → 8.72 Mpc) for 4%. The transverse-only variant is a null for U-FNO.
- ~~**Does global-slot WHNO transfer to 3-D?**~~ **Yes** — every `*/whno`/`*/swhno` cell beats `fno/fno`; SIREN-generated Walsh is the best global operator tested. The FNO+WHNO **ensemble** is still untried and is motivated by the coherence/amplitude anti-correlation.
- **Run the $z_\text{re}$ reconstruction evaluation.** All 26 runs are scored in $z_\text{re}$-space; [[Smooth-Target Reparametrization Plan]]'s actual criterion — reconstructed front width versus U-FNO 10.7 / truth 3.6 Mpc — is still unrun. **The target-side question remains open; there is no result yet.**
- **Pick the LOS grid and rebuild the cache** (`crop15_chi_256` for simplicity, `warped_256` for low-$z$ fidelity), then the **common-grid re-evaluation** that makes warped-cache training numbers comparable, then the U-FNO benchmark with `LOSS_LOS_VOLUME_WEIGHTS=1`.
- **LOS mode count** ([[LOS Bandwidth as the 3-D Bottleneck]]): single-variable runs at `LOCALFNO_MODES_Z` 12 → 17 and bottleneck z 16 → 24/33 with the diagnostic re-run — but interpret with [[Warped LOS Grid Evaluation]]: extra modes resolve nothing if the cache is the limit.
- **3-D confirmations still to run**: pure L² (`checkpoints_3d_localsirenfno` vs `_l2only`), width bw32/bw48 at ω=60, and the first genuinely balanced 3-D L²+H¹ (`_bw32om60_relbal`, 0.5/0.07).
- **Does global-slot WHNO transfer to $z_\text{re}$?** (3-D is answered.) Plus the shift-consistency test for the dyadic-convolution caveat, now diagnostic rather than precautionary given the Walsh undersizing ([[Square-Wave Basis for Ionization Fields]]).
- **`cnn/swhno` + hybrid** — best morphology crossed with best front width, never run.
- Untried and cheap: `WallPlacementLoss` + BCE (the designed pairing), the `cnn` operator as a converged baseline, Local-FNO transverse-roll/D4 augmentation and AdamW.
- Re-check [[Bubble Size Distribution]] on an expwall model — does truth-like front width fix the too-large bubbles?
- Boundary-band + $P(k)$/$r(k)$ on the SirenFNO checkpoint; the SirenFNO × U-Net hybrid; the global-pooling residual.
- **The experiments now trace an explicit accuracy-versus-sharpness frontier** (RMSE 0.1448 at width 2.89, or 0.1767 at 1.16). For a forward model feeding SBI on summary statistics, truth-like $P(k)$ and BSD plausibly beat per-pixel RMSE; the thesis has to choose a point deliberately rather than inherit the loss default.
- P1 remains focused on renormalized EFT coefficient extraction and cross-simulator validity.
