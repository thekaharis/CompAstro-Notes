
This pipeline turns the lightcones produced by the **21cmFAST App**
(`Code/21cmfFAST App/data/outputs/sim_*/lightcone.h5`) into training data
for the 3-D **Fourier Neural Operator** under `Code/FNO/`.

The immediate target mapping is

$$
  \mathcal{G}: \delta_m(\mathbf{x},z) \;\longrightarrow\; x_{\mathrm{HI}}(\mathbf{x},z),
$$

i.e. the *matter density* lightcone (`density`) is the input field and
the *neutral hydrogen fraction* lightcone (`neutral_fraction`) is the
target. Everything below is field-level, in real space, on the same
LOS-rectified grid that `RectilinearLightconer` writes.

---

## Layout

```
Code/FNO/
├── fno_test.py                # original 2-D FNO smoke (Darcy)
├── fno_test_mps.py            # original 2-D FNO training loop
├── PIPELINE.md                # this file
└── pipeline/
    ├── __init__.py            # public re-exports
    ├── loader.py              # h5py reader for *.h5 lightcones
    ├── manifest.py            # discover + index lightcone files
    ├── splits.py              # group-aware train/val/test splits
    ├── normalize.py           # streaming Welford z-score standardiser
    ├── dataset.py             # torch Dataset of LOS chunks
    ├── model.py               # neuralop.FNO 3-D factory
    ├── train.py               # CLI: end-to-end training
    └── predict.py             # CLI: stitched lightcone inference
```

The pipeline depends only on `numpy`, `h5py`, `torch`, and `neuralop`.
It does **not** import `py21cmfast`, so it can run from inside any
Python env that has the FNO stack (`FNO_env` on this machine), even
when the simulator env (`21cmfast`) is not active.

---

## Data layout assumed

A 21cmFAST v4 lightcone HDF5 file looks like:

```
/lightcones/density           (HII_DIM, HII_DIM, n_los) float32
/lightcones/neutral_fraction  (HII_DIM, HII_DIM, n_los) float32
/lightcones/brightness_temp   (HII_DIM, HII_DIM, n_los) float64
/lightcones/los_velocity      (HII_DIM, HII_DIM, n_los) float32
/lightcone_distances          (n_los,) float64        [comoving Mpc]
/InputParameters/...                                  [attrs only]
```

The transverse plane is square and periodic, the LOS axis is the third
axis. The pipeline asserts this convention at load time.

---

## Step 1 — Manifest

`pipeline.manifest.build_manifest(root)` walks `root` for
`*/lightcone.h5`, opens each file, and produces a `LightconeManifest`
with one `LightconeRecord` per simulation:

```python
LightconeRecord(
    sim_id="sim_00014",
    path=".../sim_00014/lightcone.h5",
    fields=["brightness_temp", "density", "los_velocity", "neutral_fraction"],
    transverse=64,
    n_los=682,
    box_len=150.0,
    cell_size=2.34375,
    z_min=5.96,
    z_max=11.89,
)
```

Records are filtered before training:

```python
m = build_manifest(root)
m = m.filter(transverse=64,
             required_fields=("density", "neutral_fraction"),
             min_los=64)
```

This removes runs at the wrong transverse resolution (so a batch can be
stacked) and runs whose LOS is shorter than the chunk size.

The manifest is serialised to `runs/<run-name>/manifest.json` so the
training set can be reproduced exactly.

---

## Step 2 — Splits

`pipeline.splits.split_records` partitions **simulations**, never
chunks, into `train / val / test` (default `0.7 / 0.15 / 0.15`). A
single lightcone can produce dozens of chunks; splitting by record
guarantees that no chunk from a held-out simulation is ever seen during
training.

---

## Step 3 — Normalisation

`pipeline.normalize.FieldStandardizer.fit(records, fields)` streams a
handful of LOS chunks per record through a Welford accumulator and
records pooled mean/std for each field. Stats are computed from the
**training** split only.

* `density` — δ has zero mean by construction; the standardiser
  rescales it to unit variance.
* `neutral_fraction` — bounded in [0,1]; the z-score keeps the FNO loss
  scale-invariant against the global ionisation fraction.

The fitted standardiser is saved alongside the model so prediction
denormalises with the exact same constants.

---

## Step 4 — Chunking dataset

`pipeline.dataset.LightconeChunkDataset` is a `torch.utils.data.Dataset`
that yields `(input, target)` chunks shaped `(1, Nx, Ny, Nz)`.

* `Nx = Ny = transverse` — the full transverse plane is kept so the
  FFT inside the FNO sees the periodic box.
* `Nz = chunk_los` — user-chosen LOS depth (default 64). Each chunk is
  a self-contained sub-volume.
* `stride_los` — distance between consecutive chunk starts. Default
  equals `chunk_los` (non-overlapping).

`ChunkSpec.starts(n_los)` enumerates LOS start indices for one
lightcone, and the dataset flattens these into a single global index.

For small datasets, pass `cache_in_ram=True` to load every selected
lightcone into memory once; for larger sweeps, leave it off and the
loader will re-open the HDF5 lazily per `__getitem__`.

### Why chunk?

A real lightcone has hundreds to thousands of LOS pixels. Training on
the full thing would waste GPU memory on data that doesn't fit and
would couple the loss across redshift epochs that the FNO has no reason
to share state on. Chunking gives many i.i.d. samples per simulation
and matches the FNO inductive bias of locality in physical space.

---

## Step 5 — Model

`pipeline.model.build_fno3d` is a thin wrapper around
`neuralop.models.FNO`:

```python
build_fno3d(
    n_modes=(16, 16, 16),
    in_channels=1,
    out_channels=1,
    hidden_channels=32,
    n_layers=4,
)
```

Spectral modes per axis (`n_modes`) act as a low-pass band; choose
`n_modes ≤ chunk_size / 2`. Hidden channels and layer count trade
expressiveness for compute. Defaults sit well below typical GPU
memory limits at `chunk_los = 64`.

---

## Step 6 — Training

```bash
cd Code/FNO
python -m pipeline.train \
    --data-root "../21cmfFAST App/data/outputs" \
    --out-dir   runs/run01 \
    --transverse 64 \
    --chunk-los  64 \
    --epochs     30 \
    --batch-size 2 \
    --n-modes    16 \
    --hidden-channels 32 \
    --n-layers   4 \
    --device     cpu
```

The trainer:

1. builds the manifest, filters by `--transverse`,
2. splits records,
3. fits the standardiser on the train split,
4. trains the FNO with `LpLoss(d=3, p=2)` (relative L²),
5. cosine-anneals the learning rate,
6. saves `fno3d_best.pth`, `manifest.json`, `standardizer.json`,
   `history.json` to `--out-dir`,
7. early-stops on validation loss.

The checkpoint records the standardiser stats, the training arguments,
and the model state dict, so prediction is fully reproducible.

---

## Step 7 — Prediction (full lightcone, stitched)

```bash
python -m pipeline.predict \
    --checkpoint runs/run01/fno3d_best.pth \
    --lightcone  "../21cmfFAST App/data/outputs/sim_00031/lightcone.h5" \
    --out        runs/run01/predictions/sim_00031.h5 \
    --overlap    8
```

`predict.py` chunks the lightcone with `stride = chunk_los - overlap`,
runs each chunk through the FNO, and blends overlapping outputs with a
1-D Hann window along LOS. The result is written next to the input
field and the ground truth so downstream analysis (power spectra,
ionisation history, $r_{xm}(k)$, EFT bias extraction, …) can read
prediction and truth from the same HDF5.

---

## Notes on resolution invariance

FNO spectral filters are resolution-independent in principle. The
training spec fixes the *transverse* resolution because batches must
stack into a tensor; lightcones at e.g. `HII_DIM = 50` and `64` cannot
be mixed in one batch. Two clean options if needed later:

* maintain one trained model per `HII_DIM` (current pipeline),
* or, after training at `HII_DIM = 64`, evaluate on `HII_DIM = 128`
  lightcones directly — `predict.py` happily takes any transverse
  size since the convolutions all live in Fourier space.

The LOS depth `chunk_los` can be varied at prediction time
independently of training (see `--chunk-los` on `predict.py`); the
neural operator generalises across LOS extent up to the band-limit
imposed by the training data.

---

## Extending to brightness temperature (Task 1)

To switch to the $\delta_m^{\mathrm{lin}} \to T_b$ task from the
planning note, change two flags:

```bash
--input-field  density          # or a separate IC field if available
--target-field brightness_temp
```

Everything else (manifest, splits, standardiser, dataset, model,
trainer) is field-agnostic.

---

## Smoke-test reference run

A minimal run that proves the pipeline end-to-end on the existing
`data/outputs` directory:

```bash
python -m pipeline.train \
    --data-root "../21cmfFAST App/data/outputs" \
    --out-dir runs/smoke \
    --transverse 64 \
    --chunk-los 32 \
    --epochs 2 \
    --batch-size 2 \
    --n-modes 8 \
    --hidden-channels 16 \
    --n-layers 3 \
    --cache-ram
```

This is **not** a science run; it is the integration test that should
be re-run any time the pipeline changes. With the four 64-transverse
lightcones currently in `data/outputs` the trainer splits 2 / 1 / 1
and one full epoch fits on CPU in well under a minute.
