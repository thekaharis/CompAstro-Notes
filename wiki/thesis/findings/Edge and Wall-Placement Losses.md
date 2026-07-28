---
type: finding
title: "Edge and Wall-Placement Losses"
created: 2026-07-28
updated: 2026-07-28
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - concept/loss-design
  - concept/sharp-fronts
  - finding/positive
status: active
related:
  - "[[Hedged Edges vs Blurred Edges]]"
  - "[[Sliced Wasserstein Edge Loss]]"
  - "[[Contrast Map Investigation]]"
  - "[[Structured-Transform Operator Findings]]"
  - "[[Smooth-Target Reparametrization Plan]]"
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[Bubble Size Distribution]]"
sources:
  - "[[.raw/reports/NOTES-contrast-map.md]]"
  - "losses.py (SlicedWassersteinEdges, HighKPowerRatio, WallPlacementLoss, ExponentialWallDistance, H1Seminorm)"
  - "figures/xhi2d_all_variants.md (29 runs, 384 shared held-out slices)"
---

# Edge and Wall-Placement Losses

> **Purpose:** the constructive follow-up to [[Contrast Map Investigation]]. If the front-width deficit is **hedging** rather than blur ([[Hedged Edges vs Blurred Edges]]), the fix has to live in the objective. Four new loss terms were built and swept on the 2-D $x_\text{HI}$ task. The headline: an **exponential-in-distance absolute-error** term reaches truth-like front width (**1.16 px vs truth 1.46**, against ~2.9 px for every RMSE-optimal model) at a cost of ~22% RMSE. For the first time in the campaign there is a knob that actually moves front sharpness.

## 1. The displacement-blindness measurement

The premise, measured on a displaced step edge. Going from 4 px to 48 px of misplacement changes:

| loss | change over 4 px → 48 px |
|---|---|
| L² | 3.5× |
| H¹ | 2.9× |
| **H¹ seminorm** | **1.00×** |
| **H²** | **1.00×** |
| signed-distance wall loss | **144×** |

**Gradient-only losses are completely blind to misplacement.** H¹'s entire sensitivity comes from the L² term inside it — `neuralop.H1Loss` is *not* L²-free, it sums $\|u-v\|^2$ and $\|\nabla u - \nabla v\|^2$. (`H1Seminorm` was implemented to make this testable; it has constants in its null space, so any uniform offset is free.)

This is why the campaign's H¹-heavy objectives never bought front sharpness, and — with the loss-weight audit in [[z_re Map Training Results]] showing H¹ was supplying 99.4% of the 3-D training loss — it explains the long-standing puzzle of 12–14 Mpc fronts against a 3.6 Mpc truth *despite* an apparently gradient-dominated loss.

## 2. The four terms

### `SlicedWassersteinEdges` (SWD)
Optimal-transport distance between predicted and true **edge measures** $|\nabla x_\text{HI}|$, each normalized to unit mass. Scores *where* transitions sit and leaves *how much* edge to a spectral term. Full construction in [[Sliced Wasserstein Edge Loss]].

### `HighKPowerRatio` (highK)
Squared log-ratio of radially binned power above $k_\text{min}$ (default 0.2 cycles/px $\approx 0.9\ \text{Mpc}^{-1}$ on the 200 Mpc / 140 px grid, where the cylindrical $P(k)$ diagnostics show the deficit setting in). Being computed from $|\text{FFT}|^2$ it is **translation invariant**, so unlike any pointwise loss it cannot be reduced by hedging on edge position — it only asks for the right *amount* of structure at each scale. Deliberately paired with SWD, which is blind to the amplitude highK constrains.

### `WallPlacementLoss` — linear, and it collapses
$$L = \text{mean}\big(\phi \cdot (\hat{u} - u)\big), \qquad \phi = \text{signed distance of the truth to the wall}$$
with $\phi < 0$ inside neutral regions, $>0$ outside, computed by iterative 3×3 min-propagation on the GPU (chessboard rather than Euclidean distance — immaterial for penalising misplacement, and it avoids a ~27% epoch overhead from a CPU `scipy` EDT round trip). `cap` bounds the per-pixel weight, hence the gradient.

It is linear in the prediction, so its gradient never vanishes, and it is minimised exactly at $\hat{u} = u$ for a binary target — unlike SWD/highK, which fix neither level nor position.

**But it must not be used alone.** Its gradient is the constant $\phi$, which never diminishes near the optimum, so through a sigmoid output it drives the logits straight into saturation. Run alone it collapsed to a **uniform field of 1.0 (std 0, 100% saturated) by epoch 0** and never moved again. The intended partner is BCE, whose gradient $\sigma(z) - y$ is maximal exactly for a confidently wrong pixel — and BCE is not an L² term, so "no L² anchor" survives.

### `ExponentialWallDistance` (expwall) — the one that works
$$L = \frac{\text{mean}\big(w(\phi)\,|\hat{u} - u|\big)}{\text{mean}(w)}, \qquad w = \exp(|\phi| / \text{scale})$$

Two deliberate choices, and both matter:

- **Exponential in distance.** A pixel wrong far from any true wall is punished exponentially harder than one wrong at the boundary. A hedged ramp is wrong over a *wide* band, so its tails land in the expensive region; a sharp wall misplaced by $d$ is wrong over a band of width $d$, costing $\sim \text{scale}\,(e^{d/\text{scale}} - 1)$. **Both blur and displacement are punished, and neither saturates.**
- **Absolute error, not squared.** This is what *removes* hedging rather than merely discouraging it. The minimiser of a weighted squared error is a weighted conditional **mean** — exactly the blurred compromise L² and BCE both converge to. The minimiser of a weighted absolute error is a weighted conditional **median**, and the median of a binary field is binary: **under uncertainty this loss picks a side instead of averaging.**

It also fixes `WallPlacementLoss`'s collapse: the gradient $w \cdot \text{sign}(\hat{u} - u)$ has the same non-vanishing magnitude but **reverses** at $\hat{u} = u$, so the optimum is a fixed point rather than something the optimiser sails through.

## 3. Results — 29 runs on 384 shared held-out slices

Selected rows; `width` and `blur` are to be compared against the **TRUTH** row, not between models. Full table: `wiki/thesis/findings/figures/operator-benchmark_20260728/xhi2d_all_variants_table.md`.

| run | train loss | best val L² | RMSE | wall | expwall | **width** | blur |
|---|---|---|---|---|---|---|---|
| `whno_glob_lr3e4` | 1·L² | 0.1060 | **0.14479** | 0.00587 | 0.02566 | 2.89 | 0.2027 |
| `whno_glob_h1semi` | 1·H¹semi | 0.1083 | 0.14540 | 0.00488 | 0.02907 | 3.14 | 0.1967 |
| `whno_glob_swd` | 1·L² + 140·SWD | 0.1072 | 0.14666 | 0.00498 | 0.02554 | 2.66 | 0.1939 |
| `whno_glob_highk` | 0.12·highK + 1·L² | 0.1083 | 0.14686 | 0.00447 | 0.02559 | 2.18 | 0.1874 |
| `whno_glob_edge` | 0.12·highK + 1·L² + 140·SWD | 0.1089 | 0.14905 | 0.00403 | 0.02559 | 2.15 | 0.1831 |
| `ufno_lr3e4_e30` | 1·L² | 0.1132 | 0.15587 | 0.00657 | 0.02878 | 2.77 | 0.1926 |
| **`whno_glob_expwall16`** | **1·expwall** (scale 16) | 0.1273 | 0.17671 | **0.00261** | **0.02097** | **1.16** | **0.0963** |
| `whno_glob_expwall8` | 1·expwall (scale 8) | 0.1470 | 0.19672 | 0.00268 | 0.02738 | 1.36 | 0.1060 |
| `whno_glob_expwall4` | 1·expwall (scale 4) | 0.3040 | 0.52212 | 0.04207 | 0.15547 | 0.13 | 0.0092 |
| `whno_glob_edgeonly` | 0.12·highK + 140·SWD | 0.8462 | 0.91965 | 0.36791 | 0.94746 | 1.43 | 0.1468 |
| **TRUTH** | | | | | | **1.46** | **0.1014** |

### 3.1 `expwall` scale is a genuine sharpness dial

Scale 16 lands front width at **1.16 px** and blur at **0.0963** against truth 1.46 / 0.1014 — the first model in the campaign to reach truth-like sharpness statistics *from training* rather than from post-processing. It also has the best `wall` and `expwall` scores of any run, i.e. it is the best-*placed* field, not merely the sharpest.

Scale 8 overshoots slightly and costs more; **scale 4 is a hard failure** (width 0.13, RMSE 0.52) — the weight grows too fast and the field binarises into confidently wrong regions. The scale parameter is not forgiving.

The high-$k$ evidence agrees: `expwall16` reaches high-$k$ power ratio **0.82** against the L² baseline's **0.51** (1.0 = correct small-scale power), i.e. it recovers most of the missing small-scale amplitude. The cost shows up in high-$k$ cross-correlation, **0.58 vs 0.70** — sharper and better-amplituded, but with somewhat less phase agreement.

> [!key-insight]
> There is now an **explicit accuracy-vs-sharpness frontier**, not a free lunch. RMSE 0.1448 at width 2.89, or RMSE 0.1767 at width 1.16. Which end is right depends on the deliverable: for a forward model feeding SBI on summary statistics ([[P2 Cross-Simulator Inference]]), truth-like $P(k)$ and [[Bubble Size Distribution]] plausibly matter more than per-pixel RMSE. **This is a choice the thesis now has to make explicitly rather than inherit from the loss default.**

### 3.2 An L² (or BCE) anchor is not optional

`edgeonly` (highK + SWD, no L²) failed outright at RMSE 0.9197, never beating its epoch-0 value. Neither SWD nor highK constrains absolute level or position. Same lesson as `WallPlacementLoss` alone.

### 3.3 SWD is the cheapest edge term; highK the most effective per unit L²

SWD costs ~1.1% L² for width 2.89 → 2.66. highK costs ~2.2% for 2.89 → 2.18. Combined (`edge`) gives 2.15 at ~2.7% — barely more than highK alone, so the two are not additive in the way the design hoped. None of them approaches expwall.

### 3.4 Contrast schedule + edge losses

Pairing the per-$\bar{x}_\text{HI}$-bin contrast schedule with SWD (`ctrrefit_swd`) or with expwall (`ew16_step14`, `ew16_step14_band`) does not change the verdict of either component: the contrast schedule stays at ~identity on the L² runs and the expwall runs stay at their expwall accuracy/sharpness point. Diagnostic value only — the two mechanisms do not compose.

![[xhi2d_wall_models_grid_v2.png]]

## 4. Engineering notes

- **Silent rank broadcast bug (fixed 2026-07-28).** The wall losses build $\phi$ from a channel-dropped target and multiply it against a channelled prediction; without an explicit rank match the broadcast silently produced the wrong shape. `_match_rank` now restores the channel axis.
- **`ScheduledWeightedLoss`** ramps selected terms in over early epochs; the wall terms are paired with the schedule so they do not dominate before the field has any structure to place.
- **The 3-D extension is merged** (`WallPlacementLoss` / `ExponentialWallDistance` accept $(N,D,H,W)$ cubes; the chamfer propagation switches to `max_pool3d`). Note the distance is in **voxels**, and for a lightcone the transverse and LOS axes are not on the same physical scale — the penalty is mildly anisotropic in Mpc. **No 3-D expwall run has completed yet.**

## 5. Open

- **Run expwall in 3-D.** This is the priority item: the front-width defect is worse there (~3.5×), the loss is merged, and the anisotropic-voxel caveat needs measuring rather than arguing about.
- Sweep `scale` more finely between 8 and 16, and try `expwall + λ·L²` to see whether the frontier can be bent rather than merely traversed.
- Test `WallPlacementLoss + BCE` — the designed pairing, still unrun.
- Re-check [[Bubble Size Distribution]] on an expwall model: does truth-like front width also fix the systematically-too-large bubbles?
