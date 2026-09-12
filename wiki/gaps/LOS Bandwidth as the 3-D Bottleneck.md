---
type: gap
title: "LOS Bandwidth as the 3-D Bottleneck"
created: 2026-07-27
updated: 2026-09-12
tags:
  - gap/open-question
  - domain/operator-learning
  - concept/spectral-bias
status: open
priority: medium
domain: "[[Inference and ML]]"
related:
  - "[[Loss Objective and Operator Basis Sweep]]"
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
  - "[[Windowed Local-FNO U-Net Findings]]"
  - "[[Warped LOS Grid Plan]]"
  - "[[3-D Operator Matrix Final Results]]"
---

# LOS Bandwidth as the 3-D Bottleneck

## The question

Is the **line-of-sight mode count** the binding bandwidth constraint in 3-D — and does raising `LOCALFNO_MODES_Z` (and the bottleneck z modes) move the U-FNO floor?

## The evidence pointing here

Mode-weight profiles on the 3-D Local-FNO ([[Loss Objective and Operator Basis Sweep]], §3):

| axis | edge/peak weight ratio |
|---|---|
| x, y (transverse) | 0.03–0.20 |
| **z (LOS)** | **0.60–0.78** |

A low edge/peak ratio means the retained modes near the cutoff carry little weight — the truncation is not binding. **On the LOS axis it is 3–20× higher**: the model is pushing weight right up against the cutoff. Both knobs have headroom: `LOCALFNO_MODES_Z` is 12 with a cap of 17, the bottleneck z modes are 16 with a cap of 33.

## Why it has not been tested

The 2-D $z_\text{re}$ sweep, which is where most recent hyperparameter effort went, **structurally cannot inform this** — it has no LOS axis. Worse, the $z_\text{re}$ sweep produced a clear *negative* bandwidth result (local modes 6→8 and window 16→32 both hurt), which is **not transferable**: the $z_\text{re}$ target has 7–11× *less* small-scale transverse power than $x_\text{HI}$ slices. Reading that null as "bandwidth doesn't matter" would be the wrong lesson.

## Caveats

- This is a **bandwidth** lever, and the front-width defect is an **objective** problem ([[Hedging Bias of Pointwise Losses]]) — so raising LOS modes should not be expected to sharpen walls. The plausible payoff is whole-volume L²/R2_struct, not front width.
- It partly overlaps the data-side [[Warped LOS Grid Plan]]: if the cube cache's LOS grid is itself the limiting resolution (~37 Mpc at low z), extra LOS modes have nothing to resolve. **Sequence matters** — settle the grid question first, or at least interpret the two together.

## Note added 2026-09-12 — this is not an explanation of the U-FNO

It is tempting to read this page as saying the U-FNO wins in 3-D *because* its
U-Net path supplies the LOS bandwidth the spectral slots lack. The cylindrical
decomposition in [[3-D Operator Matrix Final Results]] §7.1 rules that out:
$k_\parallel$ explains under 15% of U-FNO's advantage over every other matrix
model, $k_\perp$ 43–94%.

The two findings are compatible and say different things. **This page is about
where the *target* has structure that the truncation cannot represent** — a
property of the data and the mode budget, still untested. **§7.1 is about where
one architecture beats another**, and that is transverse. A LOS-bandwidth
experiment remains worth running on its own terms; it just should not be
motivated as "explaining the U-FNO gap".

One caveat cuts both ways: §7.1's cylindrical grid only reaches
$k_\parallel = 0.16\ h\,$Mpc$^{-1}$, so it cannot see a small-scale LOS effect
— which is precisely the band this page's mode-budget argument is about.

## Next step

Single-variable runs at `LOCALFNO_MODES_Z` 12 → 17 and bottleneck z modes 16 → 24/33 on the 3-D task, with the mode-weight diagnostic re-run to confirm the edge/peak ratio drops. Cheap, and the diagnostic makes the result interpretable either way.
