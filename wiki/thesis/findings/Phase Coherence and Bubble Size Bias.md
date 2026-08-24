---
type: finding
title: "Phase Coherence and Bubble Size Bias"
created: 2026-08-23
updated: 2026-08-23
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - concept/morphology
  - concept/diagnostic
  - concept/spectral-bias
  - architecture/whno
  - architecture/sirenfno
  - architecture/local-fno
  - finding/positive
status: active
verdict: complete
related:
  - "[[3-D Operator Matrix Final Results]]"
  - "[[Bubble Size Distribution]]"
  - "[[Mean Free Path]]"
  - "[[Cross-Power Spectrum]]"
  - "[[Power Spectrum Error]]"
  - "[[Ionization Morphology]]"
  - "[[Structured-Transform Operator Findings]]"
  - "[[Walsh-Hadamard Neural Operator]]"
  - "[[Granulometry (BSD) Auxiliary Loss]]"
  - "[[Square-Wave Basis for Ionization Fields]]"
sources:
  - "`figures/final_eval/matrix/ps/ps_results.npz` (stage-resolved $r(k)$, $P_\\text{pred}/P_\\text{true}$, $\\Delta^2$ medians)"
  - "`figures/final_eval/matrix/bsd/bubble_size_metrics.csv` (MFP metrics per model per stage)"
  - "`figures/final_eval/matrix/rmse/rmse_r2.csv` (pooled RMSE / $R^2$, for the partial correlations)"
  - "`viz/bubble_size_evaluation.py` (estimator definition)"
  - "`Poster/euCAIF/make_coh_bsd_fig.py`, `Poster/euCAIF/make_mechanism_fig.py` (analysis + figures, 2026-08-23)"
---

# Phase Coherence and Bubble Size Bias

A reanalysis of the existing 3-D matrix eval outputs — no new runs. It answers a
question left open by [[3-D Operator Matrix Final Results]] §5 and §7, which
noted that the Walsh cells "get the right amount of small-scale power in the
wrong places" and undersize bubbles, but attributed the bubble-size control to
the *local operator slot*.

**The controlling variable is not the operator slot and not the small-scale
amplitude — it is small-scale phase accuracy.** Cross-correlation $r(k)$ at
$k > 1\,\text{Mpc}^{-1}$ predicts the mean-free-path bubble-size bias across the
matrix at $\rho = +0.88$; the small-scale amplitude ratio predicts nothing once
$r$ is controlled for.

All numbers below are the **active band** $0.05 < \bar{x}_\text{HI} < 0.95$,
200 held-out cones, and the **9 `localop` cells** — U-FNO is carried as the dense
reference and excluded from every fit (see [[3-D Operator Matrix Final Results]]
on why it is not a matched cell).

## 1. The correlation

Coherence is summarised as $\langle r(k)\rangle$ over the three $k$ bins above
$1\,\text{Mpc}^{-1}$. BSD quality is the estimator's `relative_mean_bias` — the
**per-cone median** of $\lambda_\text{pred}/\lambda_\text{true} - 1$ — and its
Jensen–Shannon divergence.

| local / global | $\langle r\rangle_{k>1}$ | ratio $_{k>1}$ | $\nu_\text{pred}/\nu_\text{true}$ | BSD bias | JS | RMSE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| U-FNO *(ref.)* | 0.726 | 0.505 | 0.843 | +0.057 | 0.006 | 0.0578 |
| cnn / swhno | **0.714** | 0.525 | 0.867 | **+0.006** | **0.007** | 0.0618 |
| cnn / whno | **0.714** | 0.506 | 0.853 | -0.009 | 0.008 | 0.0613 |
| sfno / swhno | 0.687 | 0.713 | 1.008 | -0.074 | 0.008 | 0.0591 |
| whno / swhno | 0.655 | 0.877 | 1.170 | -0.179 | 0.024 | 0.0654 |
| fno / whno | 0.652 | 0.644 | 0.992 | -0.212 | 0.018 | 0.0759 |
| swhno / swhno | 0.651 | 0.890 | 1.185 | -0.206 | 0.027 | 0.0663 |
| fno / fno (bsd) | 0.650 | **0.908** | 1.047 | -0.141 | 0.020 | 0.0799 |
| whno / whno | 0.638 | 0.840 | 1.163 | -0.251 | 0.030 | 0.0741 |
| wno / whno | 0.567 | 0.611 | 1.057 | -0.313 | 0.041 | 0.0893 |

$\nu = \sigma_1/\sigma_0$ is the level-crossing rate defined in §4.3.

- $\langle r\rangle_{k>1}$ vs BSD bias: **Spearman $+0.88$** ($p = 0.0016$),
  Pearson $+0.94$, linear fit $R^2 = 0.88$,
  $\text{bias} = -1.657 + 2.284\,r$, crossing zero at $r \approx 0.726$.
- $\langle r\rangle_{k>1}$ vs JS divergence: $\rho = -0.92$ ($p = 0.0005$).
- It holds in every stage taken separately: $\rho = +0.58,\,+0.92,\,+0.72,\,+0.83,\,+0.60$
  for the five $\bar{x}_\text{HI}$ bands (three of the five reach $p < 0.05$ at $n = 9$).

![[matrix_coherence_vs_bsd_bias.png]]

## 2. Amplitude carries no independent signal

This is the part that revises §7's framing. The two "small-scale fidelity" axes
behave completely differently:

| predictor | $\rho$ with BSD bias | partial, controlling for $\langle r\rangle_{k>1}$ |
| --- | ---: | ---: |
| $\langle r\rangle_{k>1}$ (phase) | **+0.88** ($p = 0.002$) | — |
| $\langle P_\text{pred}/P_\text{true}\rangle_{k>1}$ (amplitude) | -0.27 ($p = 0.49$) | +0.35 ($p = 0.35$) |
| incoherent power fraction | -0.68 ($p = 0.042$) | — |

where the incoherent fraction is
$\int_{k>0.3} \Delta^2_\text{pred}(1 - r^2)\,\mathrm{d}\ln k \big/ \int_{k>0.3} \Delta^2_\text{true}\,\mathrm{d}\ln k$
— 0.21 for the CNN cells against 0.33–0.37 for the Walsh and Fourier cells.

**"More small-scale detail" is not what fixes the BSD.** `fno/fno` has the
flattest amplitude ratio in the matrix (0.908) and still undersizes by 14%;
`cnn/whno` is missing half its small-scale power (0.506) and is within 1%.

Worth keeping in mind: $r(k)$ is **invariant under any deterministic linear
filter** of the prediction. Blurring changes the amplitude ratio and leaves $r$
alone; only *adding decorrelated power* lowers $r$. So the CNN cells' higher $r$
is not a smoothing artifact — the two axes are genuinely separable, and the
matrix's apparent phase/amplitude anti-correlation is a property of the
architectures, not of the metrics ($\rho = -0.47$, $p = 0.21$, not significant).

## 3. Not an RMSE proxy, and not a global-slot effect

- Partial rank correlation of $\langle r\rangle_{k>1}$ with BSD bias
  **controlling for pooled RMSE**: $+0.71$ ($p = 0.034$).
- Partial controlling for **ionized-fraction error**: $+0.79$ ($p = 0.012$).
  (The ionized-fraction error does correlate with the bias on its own,
  $\rho = 0.67$, but it does not explain it — see §4.2.)
- Clean within-family control, global slot **fixed at `swhno`**, only the local
  slot swapped: `cnn` 0.714 / +0.006, `sfno` 0.687 / -0.074, `whno` 0.655 /
  -0.179, `swhno` 0.651 / -0.206 — monotone in 4/4.

The §5 conclusion that "the local operator, not the global basis, sets bubble
size" survives as an *observation about this matrix*, but the mechanism is
one level down: the local slots differ in how much wrong-phase small-scale power
they inject.

## 4. Why $k > 1$ — the estimator is a first-passage statistic

The BSD estimator (`viz/bubble_size_evaluation.py`, see [[Mean Free Path]]) is a
transverse periodic **mean free path**: threshold at $x_\text{HI} = 0.5$, cast
rays from ionized cells, record the distance to the *first* neutral cell.
First-passage rates add reciprocally, $1/\lambda = \sum_i 1/\lambda_i$, so the
**shortest obstruction scale present dominates the mean** regardless of how
little volume it occupies. A diagnostic with a ~10 Mpc mean is therefore
controlled by structure at $\lambda \lesssim 6\,\text{Mpc}$, i.e. $k > 1$.

Three checks, none of which assume the mechanism:

### 4.1 The signal sharpens with $k$ — it is not a proxy for overall coherence

Correlating $r$ in **each $k$ bin separately** against the BSD bias:

| $k$ [Mpc$^{-1}$] | 0.036 | 0.112 | 0.349 | 0.615 | 0.816 | 1.083 | 1.438 | 1.909 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $\rho$ | +0.73 | +0.83 | +0.82 | +0.82 | +0.90 | +0.90 | +0.88 | **+0.97** |

Monotone rise toward the smallest measured scale. Large-scale coherence
correlates too, but only because the cells that are decoherent at high $k$ are
mildly decoherent everywhere.

### 4.2 It is topology, not ionized volume

At stage $\bar{x}_\text{HI} = 0.40$–$0.60$ **every** cell reproduces the ionized
area fraction to within 1–3% — `whno/swhno` is off by $+0.8\%$ — while the MFP
bias spans $-0.006$ (`cnn/swhno`) to $-0.487$ (`wno/whno`):

| local / global | $\bar{x}_\text{ion,pred}/\bar{x}_\text{ion,true}$ | MFP bias |
| --- | ---: | ---: |
| cnn / swhno | 1.035 | -0.006 |
| cnn / whno | 1.027 | -0.033 |
| sfno / swhno | 1.018 | -0.142 |
| whno / swhno | **1.008** | -0.346 |
| whno / whno | 0.988 | -0.346 |
| swhno / swhno | 0.975 | -0.372 |
| wno / whno | **0.999** | **-0.487** |

Same ionized volume, chopped into more and smaller pieces. The failure is
**fragmentation of the ionized regions**, not under-ionization.

### 4.3 The mediator is the boundary-crossing rate

For a field, the density of level crossings is $\nu = \sigma_1/\sigma_0$ with
$\sigma_n^2 = \int k^{2n}\Delta^2(k)\,\mathrm{d}\ln k$ — a **$k^2$-weighted**
functional, so it is dominated by high $k$ by construction. That is the formal
reason the $k > 1$ band is the one that matters. Measured $\nu$ ratios against
the mean-MFP ratio $\lambda_\text{pred}/\lambda_\text{true}$:

- $\rho = -0.83$ ($p = 0.005$), Pearson on logs $-0.85$, log-log slope $-2.6$
  (steeper than the naive $\lambda \propto 1/\nu$, so the 2-D ray geometry
  amplifies rather than merely tracks the crossing rate).
- Walsh/SIREN cells sit at $\nu = 1.16$–$1.19$: **too many boundaries**, bubbles
  too small. CNN cells and U-FNO at $\nu = 0.84$–$0.87$: slightly too few, hence
  bias $\ge 0$ (U-FNO overshoots at $+0.057$).
- Against the per-cone median bias instead of the aggregate ratio the link is
  weaker, $\rho = -0.60$ ($p = 0.088$) — the two BSD summaries are not the same
  reduction (median of ratios vs ratio of medians).

![[matrix_bsd_mechanism.png]]

### 4.4 The bias is multiplicative, not a fixed blocker density

Fitting $1/\lambda_\text{pred} = 1/\lambda_\text{true} + 1/\lambda_\text{noise}$
per stage gives a $\lambda_\text{noise}$ that **scales with** $\lambda_\text{true}$
(e.g. `whno/swhno`: 55 → 10 → 5.6 Mpc across the 0.40–0.60, 0.60–0.80, 0.80–0.98
stages) rather than staying constant. So it is not a fixed spatial density of
spurious neutral cells; it is a fixed *fractional* boundary error per scale —
which is why each cell's relative bias is roughly stage-independent.

## 5. The chain

$$\text{wrong-phase power at } k>1 \;\rightarrow\; \text{extra threshold crossings} \;\rightarrow\; \text{spurious neutral cells and pinched boundaries} \;\rightarrow\; \text{rays terminate early} \;\rightarrow\; \lambda_\text{MFP} \text{ biased low}$$

## 6. Caveats

- $n = 9$ cells, and they are **not independent** — `sfno/swhno` and
  `swhno/swhno` share a design, four cells share the `swhno` global slot.
  Treat the correlations as descriptive of this matrix.
- The CNN cells' near-zero bias is **partly cancellation**: they *under*-produce
  boundaries ($\nu \approx 0.86$) and land near zero rather than being right for
  the right reason. Their real evidence of BSD quality is the JS / Wasserstein
  (0.007–0.008, lowest in the matrix), not the bias alone.
- Pooling model–stage pairs **across** stages inverts the sign
  ($\rho = -0.30$) — a Simpson's paradox, stage dominates both variables. The
  correlation must always be computed within a stage.
- The two earliest stages ($\bar{x}_\text{HI} < 0.4$) are heavily censored at the
  box length (40%+ of rays in the first band), which compresses the bias there
  and weakens the correlation in those bands.
- $\nu$ is computed from the median $\Delta^2$ of each field, and the Rice
  formula it borrows is exact only for Gaussian fields — the ionization field is
  not one. It is used here as a diagnostic ordering, not a prediction.

## 7. What this changes

- [[3-D Operator Matrix Final Results]] §7's "no model is good at both" stands,
  but the two axes are **not symmetric in value**: for morphology only the phase
  axis matters, so the amplitude leader (`fno/fno`, `swhno/swhno`) has no BSD
  claim to make.
- Anything that judges an emulator on ionization *morphology* should report
  $r(k)$ at $k > 1$, not the small-scale amplitude ratio.
- For [[Granulometry (BSD) Auxiliary Loss]]: a loss that pushes small-scale
  amplitude toward truth without constraining phase should be expected to make
  the BSD **worse**, which is consistent with `fno/fno (bsd)` still sitting at
  $-0.141$.

## Open

- Does a coherence-targeted auxiliary loss (penalising $1 - r(k)$ in the top
  $k$ bins) move the BSD, or does it just trade against RMSE like every other
  auxiliary term in [[3-D Operator Matrix Final Results]] §3?
- The $-2.6$ log-log slope in §4.3 is unexplained; a toy model (Gaussian field +
  independent small-scale noise, thresholded) would say whether the excess is
  ray geometry or the non-Gaussianity of the ionization field.
- Does the same $r$–BSD relation hold across the **loss** axis at fixed
  architecture, where the confound with capacity and basis disappears entirely?

---

*Analysis and figures: `wiki/thesis/findings/figures/phase-bsd_20260823/`
(`make_coh_bsd_fig.py`, `make_mechanism_fig.py`; both take `MATRIX_DIR` and
`OUT` environment variables and read the final-eval outputs directly).*
