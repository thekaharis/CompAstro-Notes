---
type: plan
title: "Excursion-Set Input Layer"
created: 2026-09-24
updated: 2026-09-24
tags:
  - domain/thesis
  - domain/ml
  - domain/operator-learning
  - domain/reionization
  - concept/physics-informed
  - concept/architecture
status: active
related:
  - "[[Excursion-Set Diagnostic]]"
  - "[[Excursion Set Formalism]]"
  - "[[Native LOS Window Training]]"
  - "[[Simulator Dependence]]"
sources:
  - "`fno-21cm/multifield_model.py` (`ExcursionSetFeatures`), `modeling.py` (`excursion_set*` config fields)"
  - "`experiments/los_windows/model_cnn_whno_es.json`; job 5149043 (queued 2026-09-23)"
  - "commit d34c2f1 on `codex/frequency-mixing-transform`"
---

# Excursion-Set Input Layer

A soft, differentiable version of 21cmFAST's ionization rule, added as extra
input channels to a field model. Motivation and ceilings:
[[Excursion-Set Diagnostic]]. **Test run queued, no results yet.**

## Design

`ExcursionSetFeatures`, applied by `MultiFieldModel` to each native LOS window
before the backbone:

1. **Filter bank.** FFT of the density window; for 12 fixed radii (0.9-20 Mpc,
   geometric) keep modes with $|k|R \le 1$ and transform back, giving
   $\delta_1 \ldots \delta_N$. Transverse is exactly periodic; the LOS is
   reflect-padded by 64 cells before the FFT so window ends do not wrap onto each
   other (the 32-cell halos absorb the rest). The cell size is read from the
   relative-LOS-distance input channel.
2. **Barrier.** A small MLP maps each LOS slice's $(1/(1+z), \theta)$ to $(a, b)$
   in the EPS shape $B = a - b\,s_R$; the barrier therefore varies along the LOS
   within a window, as z does. Initialized at the diagnostic's typical fit
   ($a \approx 0.3$, $b \approx 0.2$).
3. **Soft OR.** Margins $m_R = (\delta_R + b\,s_R - a)/T$, combined by
   log-sum-exp over radii, then a sigmoid. Temperature $T$ is learned.
4. **Output.** Two channels -- the ionization probability and $\tanh(\text{score}/8)$
   -- concatenated to the backbone input. The backbone learns only the residual
   and can ignore the channels where they do not help (early reionization).

5,123 parameters. Settings live in `ModelConfig` (`excursion_set` = `none` |
`es` | `bank`), so checkpoints restore the layer; `bank` feeds the raw filter
bank as an ablation (multi-scale inputs without barrier or OR).

## Verification

- Filter bank vs the diagnostic's periodic 140-cell filtering: correlation
  0.97-0.9995 at most radii, 0.92-0.98 at the largest.
- **At initialization, untrained**, ionized-region IoU on real windows:
  0.915 / 0.852 / 0.777 against the diagnostic's 0.906 / 0.869 / 0.800
  (late / mid / early).
- Gradients reach every barrier parameter; checkpoint reload is exact.

## Test (job 5149043)

`cnn/whno` + excursion-set channels, identical seed and training windows to the
finished `cnn/whno` baseline (test MSE 0.00716). Expected: gains late in
reionization, no loss early. Evaluation: full test set plus the diagnostic re-run
on its predictions for per-stage IoU. Planned ablation: `bank` mode.

## Risks

- **Simulator specificity.** Sharp-k is a 21cmFAST choice; radiative-transfer
  codes produce multi-scale behaviour without this exact filter. For the
  thesis's simulator-robust goal, a hard-coded 21cmFAST rule could tighten the
  model's dependence on 21cmFAST ([[Simulator Dependence]]). Keeping it as an optional input,
  and making the filter shape learnable, mitigates this.
- Same timing problem as the network: the barrier offset $a(z,\theta)$ is learned
  from the same 1,600 cones and may regress to the mean at the prior's edges.
  One option is to set $a$ per slice so the ionized fraction matches the
  [[Global Reionization History Emulator]].
