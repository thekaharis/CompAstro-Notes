---
type: plan
title: "Windowed Local-FNO U-Net Plan"
created: 2026-06-21
updated: 2026-06-21
tags:
  - domain/thesis
  - domain/planning
  - domain/ml
  - domain/operator-learning
  - architecture/local-fno
  - architecture/u-fno
  - concept/spectral-bias
status: draft
related:
  - "[[Spectral Mode Cutoff in FNOs]]"
  - "[[SirenFNO Spectral Bias Investigation]]"
  - "[[FNO Lightcone Experimental Findings]]"
  - "[[Siren3D Residual Refinement Plan]]"
  - "[[FNO Approach for 21cm Emulation]]"
  - "[[Fourier Neural Operator]]"
  - "[[Ionization Morphology]]"
  - "[[Inference and ML]]"
sources:
  - "[[Thesis/FNOs/LOCAL_FNO.md]]"
---

# Windowed Local-FNO U-Net Plan

> **Decision:** Test a **windowed Local-FNO U-Net** — a U-FNO in which the encoder/decoder spectral mixing happens inside small, overlapping spatial windows rather than over the whole volume, with a single global low-resolution Fourier bottleneck retained. The hypothesis is that *localizing* the Fourier transform gives cheap access to high effective frequencies and confines Gibbs ringing around bubble walls, without abandoning the global morphology that the standard FNO captures.

This is a third attack on the same bottleneck documented in [[Spectral Mode Cutoff in FNOs]] and measured in [[SirenFNO Spectral Bias Investigation]]: the U-FNO error floor (val L² = 0.0418, H¹ = 8.27 in [[FNO Lightcone Experimental Findings]]) is concentrated at ionization fronts, where a truncated *global* Fourier basis smooths sharp edges. The two prior approaches change *what the kernel can represent* — [[SirenFNO Spectral Bias Investigation|SirenFNO]] generates every mode with a hypernetwork; the [[Siren3D Residual Refinement Plan]] bolts a sinusoidal residual head onto a frozen U-FNO. The Local-FNO instead changes *where the transform is applied*: a low mode inside a 16-voxel window is a much higher effective frequency on the full grid.

This first version predicts on the original grid. "Higher resolution" therefore means higher **effective spectral** resolution, not spatial super-resolution.

## Motivation

The standard FNO performs spectral mixing over the complete lightcone volume. This efficiently captures long-range structure, but a truncated global Fourier representation can smooth sharp ionization fronts and introduce Gibbs-like ringing around bubble walls — exactly the failure mode behind the measured low-frequency weight collapse.

The Local-FNO applies shared Fourier layers to small, overlapping spatial windows. A low Fourier mode inside a small window represents a much higher effective frequency on the full grid, giving the model economical access to localized fine structure. A global low-resolution Fourier bottleneck is retained so independently processed regions stay consistent with the large-scale reionization morphology.

The complementary roles:

- **Local Fourier layers** resolve sharp, spatially confined structure (bubble walls).
- **Global Fourier layers** coordinate large bubbles and long-range morphology.
- **U-Net skip connections** preserve high-resolution information otherwise lost during downsampling.

## Architecture

Selected with:

```bash
MODEL_KIND=localfno python fno_21cm_3d.py
```

Default data flow:

```text
Input: (B, C, 140, 140, 256)
        |
        | 1x1x1 lifting
        v
Local spectral block, width 16 ---------------------------- skip 0
        |
        | anti-aliased average pooling + 1x1x1 projection
        v
Local spectral block, width 32 ---------------------- skip 1
        |
        | anti-aliased average pooling + 1x1x1 projection
        v
Two global residual FNO blocks, width 64
        |
        | trilinear upsampling + skip 1 concatenation
        v
1x1x1 fusion + local spectral block, width 32
        |
        | trilinear upsampling + skip 0 concatenation
        v
1x1x1 fusion + local spectral block, width 16
        |
        | pointwise projection + sigmoid
        v
Output: (B, 1, 140, 140, 256)
```

After two downsampling stages the production bottleneck has spatial size approximately `35 x 35 x 64`; two whole-volume FNO blocks operate there to capture global bubble topology and long-range dependencies. The default model has ≈**10.2 M** trainable parameters with 13 input channels (roughly a third of the ~28 M U-FNO baseline).

## Local Fourier block

Each local block processes overlapping windows with one **shared** set of Fourier weights:

| Setting | Value |
|---|---|
| Window size | `(16, 16, 32)` |
| Stride | `(8, 8, 16)` — 50% overlap |
| Retained local modes | `(6, 6, 12)` |
| Spectral channel rank | `16` |
| Default patch chunk size | `128` |

Per window, the block:

1. Projects feature channels into the lower spectral rank.
2. Multiplies the patch by a separable square-root periodic Hann window.
3. Computes a 3-D real FFT.
4. Applies learned complex channel-mixing weights to the four signed X/Y frequency quadrants and the non-negative Z spectrum.
5. Computes the inverse FFT.
6. Reconstructs the volume via normalized overlap-add.
7. Projects back to the block width.
8. Adds a real-space `1x1x1` branch.
9. Applies GroupNorm, GELU, and a pointwise residual MLP.

The **square-root Hann window** is used for both analysis and synthesis; their product forms the overlap weights, and normalization by their accumulated sum prevents visible patch seams. Patch positions are processed in chunks rather than materializing every patch at once — chunk size affects memory/runtime but not the learned model or checkpoint parameters.

## Shifted window grids

Successive local blocks alternate window offsets:

```text
Unshifted offset: (0, 0, 0)
Shifted offset:   (4, 4, 8)
```

The shift equals half the patch stride, so a feature near a window boundary in one block sits closer to a window center in the next. This encourages communication across the artificial patch partition and reduces grid-aligned artifacts (the same Swin-style motivation, applied in the spectral encoder).

## Boundary handling

The lightcone axes are not physically equivalent:

- **X, Y** — periodic transverse simulation axes → patches wrap indices periodically.
- **Z** — finite redshift / line-of-sight direction → indices outside the volume use the nearest endpoint when forming a patch, but those out-of-domain positions are masked during overlap-add and never contribute to the output.

The patch grid includes halo and trailing positions, so arbitrary spatial sizes — including odd dimensions — remain fully covered.

## Global Fourier bottleneck

Two residual Fourier blocks over the complete downsampled volume, modes controlled by the existing variables:

```bash
N_MODES_X=16
N_MODES_Y=16
N_MODES_Z=16
```

## Configuration

Local-FNO-specific environment variables:

| Variable | Default | Meaning |
|---|---:|---|
| `LOCALFNO_WINDOW_X` | `16` | Window extent along X |
| `LOCALFNO_WINDOW_Y` | `16` | Window extent along Y |
| `LOCALFNO_WINDOW_Z` | `32` | Window extent along Z |
| `LOCALFNO_MODES_X` | `6` | Retained local X modes |
| `LOCALFNO_MODES_Y` | `6` | Retained local Y modes |
| `LOCALFNO_MODES_Z` | `12` | Retained local Z modes |
| `LOCALFNO_BASE_WIDTH` | `16` | First U-Net width; later widths are 2x and 4x |
| `LOCALFNO_SPECTRAL_RANK` | `16` | Channel rank inside Fourier layers |
| `LOCALFNO_PATCH_CHUNK_SIZE` | `128` | Patch positions processed together |
| `LOCALFNO_LEARNING_RATE` | `1e-4` | Base LR before DDP scaling |
| `LOCALFNO_H1_WARMUP_EPOCHS` | `5` | Linear H1 loss warmup |
| `LOCALFNO_GRAD_CLIP_NORM` | `1.0` | Gradient clipping norm |

Constraints: window dimensions must be divisible by four; local modes must fit each window's FFT limits; spectral rank cannot exceed base width. All architecture settings are written to `run_metadata.json`, and visualization/diagnostic scripts reconstruct the model from this metadata rather than the current shell environment.

## Training objective

The controlled baseline reuses the existing models' objective so the comparison isolates the architecture:

```text
0.5 * absolute L2 + 0.5 * absolute H1 + 0.0 * BCE
```

The H1 loss uses periodic centered differences along X/Y, centered interior-only differences along Z (never connecting the physically unrelated lightcone endpoints), and ramps from zero to its configured weight over the first five epochs. No dedicated edge loss in the initial experiment — keeping the comparison focused on the architectural effect of localized Fourier processing. The output passes through a sigmoid so the neutral fraction stays in `[0, 1]` (see [[Neutral Fraction]]).

## Training and visualization

Smoke test first (one epoch, 4× H200) — inspect epoch time, samples/s, gradient norm, peak CUDA memory before the full run:

```bash
sbatch slurm/smoke_localfno_h200_4gpu.sbatch
```

Default 70-epoch production run, then standard + detailed viz:

```bash
sbatch slurm/train_localfno_h200_4gpu.sbatch
sbatch slurm/viz_localfno.sbatch
sbatch slurm/viz_localfno_detailed.sbatch
```

Viz jobs default to patch chunk size 64 for A30 memory limits; checkpoint metadata still controls the actual architecture. Default output directory `checkpoints_3d_localfno/` holds best/final states, run metadata, epoch metrics, and spectral-weight history (so the per-mode weight diagnostic from [[SirenFNO Spectral Bias Investigation]] can be re-run here).

## Evaluation and success criteria

Whole-volume L² is dominated by fully neutral/ionized regions, so bubble-wall fidelity needs front-localized diagnostics alongside global ones: validation/test absolute L² and H¹, power spectra, Fourier cross-correlation (especially high-$k$), boundary-band RMSE and H¹, predicted 10–90% bubble-front width, and visual inspection for grid-aligned patch seams.

Example paired boundary comparison against the U-FNO baseline:

```bash
python boundary_band_diagnostic.py --checkpoints \
  ufno=checkpoints_3d_ufno/best_model_state_dict.pt \
  localfno=checkpoints_3d_localfno/best_model_state_dict.pt \
  --reference ufno \
  --split test \
  --n-cones 200 \
  --out band_out/localfno
```

Each checkpoint is reconstructed from its own metadata, so different architectures can be compared safely in one process.

> **Initial success criterion:** improved boundary-band H¹ and front width over the strongest U-FNO baseline, with **no more than 5% regression in validation L²** and no measurable or visible patch-grid seams.

## Implementation and verification

Main implementation in `local_fno_3d.py`; model construction and metadata integration in `modeling.py`. Tests cover exact overlap-add reconstruction (constant/impulse/random fields), shifted and unshifted patch grids, periodic X/Y and finite Z behavior, odd spatial dimensions, finite forward/backward passes, gradients for all four Fourier quadrants, sigmoid output range, config/metadata round trips, checkpoint reconstruction, mixed local/global spectral-history recording, and explicit checkpoint loading for visualization.

The production-shape CUDA test runs a full `(1, 13, 140, 140, 256)` forward pass and should run on an H200 node:

```bash
RUN_LOCALFNO_PRODUCTION_SHAPE=1 pytest tests/test_local_fno_3d.py
```

## Limitations and follow-up ablations

- Fourier bases still approximate true discontinuities continuously: local transforms confine ringing and make high frequencies cheaper, but cannot guarantee perfectly discontinuous walls (the same caveat that limits [[SirenFNO Spectral Bias Investigation|SirenFNO]] and the [[Siren3D Residual Refinement Plan|Siren3D head]]).
- Patch FFTs add execution overhead vs. a single global transform.
- The decoder restores the original grid rather than producing a super-resolved one.
- Shared local weights assume the same local operator is useful throughout the lightcone; global coordinates and redshift channels provide context, but the spectral weights themselves are spatially shared.

Useful follow-up ablations:

1. Local-FNO with vs. without the global bottleneck.
2. Fixed vs. shifted window grids.
3. Different window sizes and LOS anisotropy.
4. Different local/global mode allocations.
5. A boundary-aware loss added **only after** the architecture-only comparison.
6. Explicit spatial super-resolution in the decoder.

## How it fits the thread

This is the controlled "local path" experiment hinted at in [[SirenFNO Spectral Bias Investigation]]: SirenFNO removes the spectral bias but lacks a local U-Net path and so does not yet beat the U-FNO floor. The Local-FNO keeps the U-Net structure and instead localizes the Fourier transform, testing whether *where* the spectral mixing happens — not just *which modes* it can represent — is what buys bubble-wall fidelity. Run order: smoke test → 70-epoch run → boundary-band/$P(k)$/$r(k)$ diagnostics vs. the U-FNO benchmark → then weigh Local-FNO against the SirenFNO and Siren3D branches.
