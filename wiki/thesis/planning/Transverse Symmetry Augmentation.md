---
type: plan
title: "Transverse Symmetry Augmentation"
created: 2026-09-24
updated: 2026-09-24
tags:
  - domain/thesis
  - domain/ml
  - concept/augmentation
  - concept/symmetry
status: active
related:
  - "[[Native LOS Window Training]]"
  - "[[Multi-Field 21cmFAST Data]]"
sources:
  - "`fno-21cm/dataset/los_windows.py` (`transverse_augment`), `--augment transverse` in `fno_multifield.py`"
  - "commit e25fb06 on `codex/frequency-mixing-transform`; test run job 5148158"
---

# Transverse Symmetry Augmentation

Each training window gets a random element of the sky-plane symmetry group:
one of 4 rotations by 90 degrees, an optional reflection, and a random periodic
shift in x and y (140 x 140 options) -- about 157,000 variants per window. The
LOS axis is never touched. **Test run queued, no results yet.**

## Why these are exact symmetries

- The transverse planes of a 21cmFAST lightcone are the faces of a **periodic**
  box, so a periodic shift just picks a different origin in the same box.
- The statistics are isotropic across the sky.
- Every field used is a scalar or the **LOS** velocity component, which is
  unchanged by transverse rotations and reflections. A transverse velocity
  component would change sign; the code refuses to augment if one is present.

The LOS is excluded: redshift, and with it the reionization stage, evolves along
it.

## Implementation

- Inputs, targets and the coarse-context input get the identical transform; fine
  shifts are restricted to multiples of the context pooling so the two grids stay
  aligned block for block (verified: pooled fine window equals the context to
  ~1e-9 after augmentation).
- Drawn from the window's own RNG **after** the window centre, so an augmented run
  sees exactly the same window positions as its unaugmented twin.
- Training only; validation and test cones are evaluated unaltered, so metrics
  stay comparable. Default off.

## Expected effect

More effective variety from the same 1,600 simulations, and the symmetry
enforced on the parts of the model that do not have it built in (CNN layers and
their edge padding; spectral layers already handle shifts). It adds no new
physics, helps most if the model overfits, and may slow convergence per epoch.

**Test (job 5148158)**: `cnn/whno` + augmentation, identical seed and windows to
the finished baseline (test MSE 0.00716).
