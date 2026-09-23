# Windowed Local-FNO U-Net

## Motivation

The standard Fourier Neural Operator performs spectral mixing over the complete
lightcone volume. This efficiently captures long-range structure, but truncated
global Fourier representations can smooth sharp ionization fronts and introduce
Gibbs-like ringing around bubble walls.

The Local-FNO addresses this by applying shared Fourier layers to small,
overlapping spatial windows. A low Fourier mode inside a small window represents
a much higher effective frequency on the full grid, giving the model economical
access to localized fine structure. A global low-resolution Fourier bottleneck
is retained so that independently processed regions remain consistent with the
large-scale reionization morphology.

This first version predicts on the original grid. “Higher resolution” therefore
means higher effective spectral resolution, not spatial super-resolution.

## Architecture

The model is selected with:

```bash
MODEL_KIND=localfno python fno_21cm_3d.py
```

Its default data flow is:

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

After two downsampling stages, the production bottleneck has spatial size
approximately `35 x 35 x 64`. Two whole-volume FNO blocks operate there to
capture global bubble topology and long-range dependencies.

The default model contains approximately 10.2 million trainable parameters
with 13 input channels.

## Local Fourier block

Each local block processes overlapping windows using one shared set of Fourier
weights:

- Window size: `(16, 16, 32)`
- Stride: `(8, 8, 16)`, giving 50% overlap
- Retained local modes: `(6, 6, 12)`
- Spectral channel rank: `16`
- Default patch chunk size: `128`

For each window, the block:

1. Projects the feature channels into the lower spectral rank.
2. Multiplies the patch by a separable square-root periodic Hann window.
3. Computes a 3-D real FFT.
4. Applies learned complex channel-mixing weights to four signed X/Y frequency
   quadrants and the non-negative Z spectrum.
5. Computes the inverse FFT.
6. Reconstructs the volume through normalized overlap-add.
7. Projects back to the block width.
8. Adds a real-space `1x1x1` branch.
9. Applies GroupNorm, GELU, and a pointwise residual MLP.

The square-root Hann window is used for both analysis and synthesis. Their
product forms the overlap weights, and normalization by their accumulated sum
prevents visible patch seams.

Patch positions are processed in chunks instead of materializing every patch at
once. Changing the chunk size affects memory and runtime but does not change
the learned model or checkpoint parameters.

## Shifted window grids

Successive local blocks alternate between:

```text
Unshifted offset: (0, 0, 0)
Shifted offset:   (4, 4, 8)
```

The shift equals half of the patch stride. Consequently, a feature lying near a
window boundary in one block lies closer to a window center in the next block.
This encourages communication across the artificial patch partition and reduces
grid-aligned artifacts.

## Boundary handling

The lightcone axes are not physically equivalent:

- X and Y are periodic transverse simulation axes.
- Z is the finite redshift/line-of-sight direction.

Local patches therefore wrap X/Y indices periodically. Z indices outside the
volume use the nearest endpoint value when forming a patch, but those
out-of-domain positions are masked during overlap-add and never contribute to
the reconstructed output.

The patch grid includes halo and trailing positions, so arbitrary spatial sizes,
including odd dimensions, remain fully covered.

## Global Fourier bottleneck

The bottleneck uses two residual Fourier blocks over the complete downsampled
volume. Its retained modes are controlled by the existing variables:

```bash
N_MODES_X=16
N_MODES_Y=16
N_MODES_Z=16
```

This branch complements the localized encoder and decoder:

- Local Fourier layers resolve sharp, spatially confined structure.
- Global Fourier layers coordinate large bubbles and long-range morphology.
- U-Net skip connections preserve high-resolution information that would
  otherwise be lost during downsampling.

## Configuration

The Local-FNO-specific environment variables are:

| Variable | Default | Meaning |
|---|---:|---|
| `LOCALFNO_WINDOW_X` | `16` | Window extent along X |
| `LOCALFNO_WINDOW_Y` | `16` | Window extent along Y |
| `LOCALFNO_WINDOW_Z` | `32` | Window extent along Z |
| `LOCALFNO_MODES_X` | `6` | Retained local X modes |
| `LOCALFNO_MODES_Y` | `6` | Retained local Y modes |
| `LOCALFNO_MODES_Z` | `12` | Retained local Z modes |
| `LOCALFNO_BASE_WIDTH` | `16` | First U-Net width; later widths are 2x and 4x |
| `LOCALFNO_SPECTRAL_RANK` | `16` | Channel rank used inside Fourier layers |
| `LOCALFNO_PATCH_CHUNK_SIZE` | `128` | Number of patch positions processed together |
| `LOCALFNO_LEARNING_RATE` | `1e-4` | Base learning rate before DDP scaling |
| `LOCALFNO_H1_WARMUP_EPOCHS` | `5` | Linear H1 loss warmup |
| `LOCALFNO_GRAD_CLIP_NORM` | `1.0` | Gradient clipping norm |

The window dimensions must be divisible by four. Local modes must fit the FFT
limits of their windows, and the spectral rank cannot exceed the base width.

All architecture settings are written to `run_metadata.json`. Visualization and
diagnostic scripts reconstruct the model from this metadata rather than relying
on the current shell environment.

## Training objective

The controlled baseline uses the same objective as the existing models:

```text
0.5 * absolute L2 + 0.5 * absolute H1 + 0.0 * BCE
```

The H1 loss:

- Uses periodic centered differences along X and Y.
- Uses centered interior-only differences along Z.
- Does not connect the physically unrelated lightcone endpoints.
- Ramps from zero to its configured weight over the first five epochs.

No dedicated edge loss is enabled in the initial experiment. This keeps the
comparison focused on the architectural effect of localized Fourier processing.

The output is passed through a sigmoid because the neutral fraction must remain
in `[0, 1]`.

## Training and visualization

Run a one-epoch, four-H200 smoke test first:

```bash
sbatch slurm/smoke_localfno_h200_4gpu.sbatch
```

The training metrics include epoch time, samples per second, gradient norm, and
peak allocated CUDA memory. Inspect these before launching the complete run.

Start the default 70-epoch production run with:

```bash
sbatch slurm/train_localfno_h200_4gpu.sbatch
```

Render standard and detailed results with:

```bash
sbatch slurm/viz_localfno.sbatch
sbatch slurm/viz_localfno_detailed.sbatch
```

The visualization jobs default to a smaller patch chunk size of 64 for A30
memory limits. The checkpoint metadata still controls the actual architecture.

The default output directory is:

```text
checkpoints_3d_localfno/
```

It contains the best and final model states, run metadata, epoch metrics, and
spectral-weight history.

## Evaluation

Whole-volume L2 can be dominated by fully neutral or fully ionized regions.
Bubble-wall fidelity should therefore be evaluated with both global and
front-localized diagnostics:

- Validation/test absolute L2
- Validation/test absolute H1
- Power spectra
- Fourier cross-correlation, especially at high wave numbers
- Boundary-band RMSE
- Boundary-band H1
- Predicted 10–90% bubble-front width
- Visual inspection for grid-aligned patch seams

Example paired boundary comparison:

```bash
python boundary_band_diagnostic.py --checkpoints \
  ufno=checkpoints_3d_ufno/best_model_state_dict.pt \
  localfno=checkpoints_3d_localfno/best_model_state_dict.pt \
  --reference ufno \
  --split test \
  --n-cones 200 \
  --out band_out/localfno
```

Each checkpoint is reconstructed using its own metadata, allowing different
architectures to be compared safely in one process.

The initial success criterion is improved boundary-band H1 and front width over
the strongest U-FNO baseline, with no more than a 5% regression in validation
L2 and no measurable or visible patch-grid seams.

## Implementation and verification

The main implementation is in `local_fno_3d.py`, with model construction and
metadata integration in `modeling.py`.

Tests cover:

- Exact overlap-add reconstruction of constant, impulse, and random fields
- Shifted and unshifted patch grids
- Periodic X/Y and finite Z behavior
- Odd spatial dimensions
- Finite forward and backward passes
- Gradients for all four Fourier quadrants
- Sigmoid output range
- Configuration and metadata round trips
- Checkpoint reconstruction
- Mixed local/global spectral-history recording
- Explicit checkpoint loading for visualization

The production-shape CUDA test is gated behind:

```bash
RUN_LOCALFNO_PRODUCTION_SHAPE=1 pytest tests/test_local_fno_3d.py
```

It should be run on an H200 node because it performs a complete
`(1, 13, 140, 140, 256)` forward pass.

## Limitations and likely follow-up experiments

- Fourier bases still approximate true discontinuities continuously. Local
  transforms confine ringing and make high frequencies cheaper, but cannot
  guarantee perfectly discontinuous walls.
- Patch FFTs add execution overhead compared with a single global transform.
- The current decoder restores the original grid rather than producing a
  super-resolved grid.
- Shared local weights assume that the same local operator is useful throughout
  the lightcone; global coordinates and redshift input channels provide context,
  but the spectral weights themselves are spatially shared.

Useful follow-up ablations include:

1. Local-FNO with and without the global bottleneck.
2. Fixed versus shifted window grids.
3. Different window sizes and LOS anisotropy.
4. Different local/global mode allocations.
5. A boundary-aware loss added only after the architecture-only comparison.
6. Explicit spatial super-resolution in the decoder.
