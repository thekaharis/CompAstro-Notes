---
type: finding
title: "Multi-Field 21cmFAST Data"
created: 2026-09-24
updated: 2026-09-24
tags:
  - domain/thesis
  - domain/simulation
  - domain/reionization
  - domain/ml
  - concept/data
  - finding/infrastructure
status: active
verdict: established
related:
  - "[[Native LOS Window Training]]"
  - "[[Warped LOS Grid Evaluation]]"
  - "[[Spin Temperature]]"
  - "[[Mesinger et al 2010 (21cmFAST)]]"
sources:
  - "`fno-21cm/notes/multifield-data-configuration.md` (configuration agreed with Codex, 2026-09-14)"
  - "`fno-21cm/experiments/multifield/pilot_report.md` (pilot, exclusion, full build, 2026-09-16 correction)"
  - "`fno-21cm/experiments/multifield/{nonfinite_report,raw_axis_audit,roundtrip_bound}.json`"
  - "`fno-21cm/tools_roundtrip_bound.py`, `tools_build_native_mirror.py`"
  - "Jobs 4923961 (aborted build), 4929874 (full 256-grid cache), 5144754 (native mirror), 5144829 (windowed multi-field preparation)"
---

# Multi-Field 21cmFAST Data

What the raw 21cmFAST lightcones contain beyond density and $x_\text{HI}$, what
their conventions are, and the two training datasets built from them: a
256-point resampled cache and a chunked native-resolution mirror. Several
properties of the data found here -- box tiling, exact zeros, the dv/dr
correction -- matter for any model trained on it.

## 1. Inventory

- **6,600 simulations**, `21cmfast_11d_sample000000.h5` ... `006599.h5`, ~7.6 TB,
  21cmFAST **4.1.1**, schema `raw_lightcone_v2.0`, source model **E-INTEGRAL**,
  `hii_filter = sharp-k`, 11 sampled parameters, box 200 Mpc on 140 cells.
- Full 3-D lightcone fields: `density`, `neutral_fraction`, `brightness_temp`,
  `los_velocity`, **`tau_21`**, and a `*_with_rsds` counterpart of each.
- Global histories only (101 node redshifts, z = 4-35.2, shared by every
  simulation): spin and kinetic temperature, mean free path, ionisation rate,
  cumulative recombinations, $x_\text{HI}$, $\tau_{21}$, $z_\text{re}$ and more.
  **Spin temperature is not stored as a 3-D field**, but it is recoverable per
  cell from `brightness_temp` and `tau_21`.
- Native LOS length varies with cosmology: 2,074-2,919 cells (846 distinct
  lengths), always at 1.428571 Mpc spacing, the transverse cell size.

## 2. Conventions established

**Velocity.** `los_velocity` is the **comoving peculiar velocity $dx/dt$ in
Mpc/s**. No unit attribute or installed source was available; the evidence is a
Fourier linear-theory fit across z = 6-15, where the fitted coefficient over
$fH$ is **0.997-0.998 and flat in z**, while over $faH$ it scales as $(1+z)$.
Proper velocity is $v[\text{km/s}] = \text{los\_velocity} \times 3.0857\times10^{19}/(1+z)$,
giving $\sigma_v$ = 93-141 km/s. The native values (~$10^{-17}$) are kept as
stored and standardized with training statistics.

**Real space, but with the optical-depth correction.** The plain fields are
**not** remapped to redshift space (plain and `_with_rsds` differ even for
density), but plain `brightness_temp` **already includes the $dv/dr$ term** in
$\tau_{21}$ (producer attribute `include_dvdr_in_tau21=True`). Regressing $T_b$
on the analytic structure confirms it: $R^2$ = 0.765 from $x_\text{HI}(1+\delta)$,
0.893 adding $dv/dr$, 0.945 adding their interaction. Never apply the gradient
correction a second time. The remaining ~5-90% of $T_b$ variance (redshift
dependent) is the spin-temperature factor, which none of the four fields carry.

**Exact zeros.** Ionized cells have $x_\text{HI}$ **exactly 0**, not small
positive values. Partially ionized values appear mainly where the lightcone
interpolates between two coeval node boxes.

**Box tiling.** Each lightcone repeats **one periodic 200 Mpc box along the
LOS**: density correlation **0.9965 at a lag of exactly 140 cells** and 0.987 at
280, so a ~3,300 Mpc cone contains ~16 copies of one box at growing amplitude.
Consequences: any 140 consecutive LOS cells form a full (cyclically shifted)
box, so a periodic 3-D FFT over them reproduces coeval filtering (used by
[[Excursion-Set Diagnostic]]); a 256-cell training window already contains the
whole box, which is consistent with coarse LOS context adding nothing
([[Native LOS Window Training]]).

## 3. Non-finite brightness temperature

The first full build (job 4923961) aborted at cone 72 on 9 NaN voxels. An
exhaustive full-resolution scan of all 6,600 cones found the defect **only in
`brightness_temp`**: 33 cones (0.50%), 242 voxels, 1-30 per cone. **All 33 are
excluded uniformly** so every field mapping shares one simulation set; repair
by interpolation was rejected as altering simulator output. In the 2,000-cone
subset the excluded sample IDs are 72, 168, 385, 428, 457, 1150, 1589, 1794.

The pilot missed it for two reasons worth remembering: cones were selected by
geometry and cosmology, not by value pathology, and the finiteness check read a
`[::4, ::4]` subsample, which cannot see a 9-voxel defect.

A heavy tail also exists: cone 5984 reaches 25,575 mK (median of order 10 mK),
genuine simulator output that sets the scale of any standardization.

## 4. The 256-point resampled cache

`data/compressed/multifield_z256.h5`: 6,567 cones x 4 fields x 140x140x256 on
z = 5.001-24.97 (linear in z), 398 GiB, 12 h build. `cone_id` holds the true
sample IDs (gaps at the exclusions), patched from the source paths.

**The grid, not the model, dominates end-to-end error.** Round trip native ->
256 -> native on four held-out cones: the grid alone loses 0.09-0.24 relative L2
in $x_\text{HI}$ and 0.22-0.47 in $T_b$, and **60-98% of the end-to-end error of
a trained model is this grid loss**. Density retains essentially none of its
LOS structure at 256 points (relative L2 1.00). Only the most ionized cone
(541, mean $x_\text{HI}$ 0.72) is model-limited.

*Correction (2026-09-16):* the pilot first reported $x_\text{HI}$ round-tripping
at 0.0037 and concluded it was preserved almost exactly. That cone (2299) had
mean $x_\text{HI}$ 0.9996 -- a featureless neutral field. On ionized cones the
loss is 25-64x larger. Pilot cones must span the target's own dynamic range,
not only the metadata.

First model on this cache, `mf_cnn_fno` (density + velocity -> $x_\text{HI}$ +
$T_b$, 20 epochs): test $x_\text{HI}$ MSE 0.00367 (r 0.976) and $T_b$ MSE
339 mK$^2$ (r 0.935), **both measured on the 256 grid**, so not comparable to
native-resolution numbers.

## 5. The native chunked mirror

The native-resolution training ([[Native LOS Window Training]]) reads 256-cell
windows from the raw files, which are gzip-compressed in **9x9x307 chunks**: one
window decompresses ~500 chunks and costs about as much as the whole field.

`data/native_mirror_4f/` rewrites the four fields of each cone in **140x140x64
uncompressed chunks**, everything else copied verbatim (16-way array, 248
cones/min, **1,992 cones, 1.3 TB**, 8 non-finite cones omitted):

| layout | 4-field size / cone | 2-field window read |
|---|---:|---:|
| raw (gzip 9x9x307) | -- | 270.2 ms |
| 140x140x32, none | 0.72 GiB | 24.0 ms |
| 140x140x32, lzf | 0.55 GiB | 43.0 ms |
| **140x140x64, none** | **0.73 GiB** | **13.8 ms** |

Fields, redshifts and parameters are **byte-identical** to the raw files
(checked on cones 0 and 1000). End to end, a 4-field training sample loads in
**592 ms instead of 2,590 ms** (4.4x): the rest is CPU work broadcasting the 11
conditioning parameters over the full window.

The windowed multi-field preparation on the mirror
(`experiments/los_windows/preparation_multifield_2000.json`): 1,594 / 199 / 199
cones, train-only statistics for all four fields.

**Cone numbering.** Native datasets number cones by position in the file list;
the mirror skips 8 files, so from row 72 onward **row != sample ID**. The
mapping is in `preparation_multifield_2000_sample_ids.json`. The split differs
from the $x_\text{HI}$ study's: only **39 test cones are shared**, and some
$x_\text{HI}$-study test cones are multi-field training cones, so cone-by-cone
comparison between the studies is valid on those 39 only.

## 6. Evaluation pitfalls found while building the visualizations

- `np.polyfit` on float32 with millions of points uses a default `rcond` of
  about `len(x)*eps` ~ 0.3 and silently corrupts the fit: cone 1625's parity
  slope is 0.965, not the 0.497 first reported. Use a closed-form float64 fit.
- `sbatch --export` splits values on commas; figure titles passed that way were
  truncated.
- A figure concatenated truth and prediction along the wrong axis and stacked
  the pairs vertically rather than side by side; lightcone strips cropped each
  cone to its own band in index space, so the stated front redshifts for cones
  47/444 (z ~ 10-10.5) were wrong -- they are at z ~ 6.5. Both fixed.
