---
type: plan
title: "P2 Cross-Simulator Inference"
created: 2026-04-21
updated: 2026-04-21
tags:
  - domain/thesis
  - domain/planning
  - domain/sbi
  - domain/eft
depends_on: "[[P1 EFT Characterization]]"
---

# P2 — Cross-Simulator Inference

> **Goal:** Train simulation-based inference (SBI) on EFT-coefficient targets extracted by the P1 pipeline, then test whether the resulting posterior generalises to a held-out simulator (BEoRN). Compare against a native-parameter baseline trained on 21cmFAST alone.

This document is a step-by-step operational plan. Each step includes the physics motivation, the concrete computation, runnable code patterns, sanity checks, and failure-mode interpretation. Read [[P1 EFT Characterization]] first — this plan consumes its outputs directly.

---

## Why EFT Coefficients as Inference Targets?

Standard SBI trains a neural posterior estimator (NPE) to learn $p(\theta \mid \mathbf{d})$ where $\theta$ are the simulator's native parameters (e.g.\ $\zeta, T_\text{vir}, R_\text{mfp}$ in 21cmFAST). This works well *within* the simulator it was trained on, but fails when applied to data from a different code. The posterior it has learned is shaped by the specific morphology 21cmFAST produces for a given parameter combination — not by the underlying physics.

EFT coefficients $\{b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon}\}$ are physical. If two simulators with matched ICs produce different ionization fields, that difference is captured by different coefficient values, not by a change in the *definition* of the parameters. A model that learns to infer EFT coefficients from an observable (the 21cm power spectrum) is learning a physical summary — one that a BEoRN observation should also be interpretable in.

The hypothesis of P2 is: **inference in EFT-coefficient space is more simulator-agnostic than inference in native-parameter space.**

---

## Inputs from P1

Before starting P2, the following P1 outputs must exist:

| Artifact | Description |
|---|---|
| `coefficients_21cmFAST.hdf5` | Extracted EFT coefficients for all training simulations |
| `coefficients_BEoRN.hdf5` | Coefficients for the matched BEoRN test set |
| `kmax_validity_21cmFAST.npy` | Per-simulation $k_\text{max}$ from the regime-of-validity analysis |
| Power spectrum datacubes | $P(k, z)$ arrays for all 21cmFAST training runs |
| BEoRN test power spectra | $P(k, z)$ for the 50 matched test runs |

If any of these are missing, complete the relevant P1 step first.

---

## Step 0 — Conceptual Map

Before writing a single line of training code, sketch the full inference pipeline:

```
Training simulator (21cmFAST, ~500 runs)
    ↓
[P1 pipeline: matched ICs → EFT extraction]
    ↓
Training set: {P(k,z), θ_EFT} pairs   ←→   Baseline: {P(k,z), θ_native} pairs
    ↓                                              ↓
NPE model (B): swyft/TMNRE              NPE model (A): swyft/TMNRE
learn p(θ_EFT | P(k,z))                learn p(θ_native | P(k,z))
    ↓                                              ↓
        Cross-simulator test (BEoRN, 50 runs)
                ↓
        Apply both models to BEoRN observables
                ↓
        Compare posteriors: coverage, bias, R²
```

The key comparison is the *transfer test*: how well does each model generalise when the test data comes from a different simulator?

---

## Step 1 — Training Set Design

### 1.1 Parameter Coverage

Use the same Latin Hypercube Sampling (LHS) grid as P1, extended to ~500 runs for sufficient coverage of the 3D parameter space $(\zeta, T_\text{vir}, R_\text{mfp})$.

```python
from scipy.stats import qmc
import numpy as np

N_TRAIN = 500

sampler = qmc.LatinHypercube(d=3, seed=1)      # different seed from P1's 36-run grid
sample  = sampler.random(n=N_TRAIN)

l_bounds = [10,   1e4,  10]    # [zeta,  T_vir,  R_mfp]
u_bounds = [80,   3e5,  60]    # extended upper bounds relative to P1

params   = qmc.scale(sample, l_bounds, u_bounds)
# params.shape == (500, 3)

np.save("training_params.npy", params)
```

**Why LHS?** It guarantees uniform marginal coverage: every slice of parameter space is sampled. Simple random sampling clusters, leaving corners of the volume poorly covered. With 500 runs over 3 dimensions this is sufficient.

**Why extend the bounds slightly beyond P1?** P1 uses a conservative range to keep simulations in a well-understood regime. P2 benefits from some boundary coverage so the posterior estimator doesn't extrapolate abruptly near the edges.

### 1.2 Sanity check on the LHS grid

```python
import matplotlib.pyplot as plt

labels = [r'$\zeta$', r'$T_\mathrm{vir}$', r'$R_\mathrm{mfp}$']
fig, axes = plt.subplots(3, 3, figsize=(9, 9))
for i in range(3):
    for j in range(3):
        if i == j:
            axes[i, j].hist(params[:, i], bins=20)
            axes[i, j].set_xlabel(labels[i])
        else:
            axes[i, j].scatter(params[:, j], params[:, i], s=4, alpha=0.5)
            axes[i, j].set_xlabel(labels[j])
            axes[i, j].set_ylabel(labels[i])
plt.tight_layout()
plt.savefig("lhs_coverage.png", dpi=150)
```

✓ Each 1D marginal should look approximately uniform. If it looks clustered, the sampler seed is bad — try another.

### 1.3 Running the simulations

Batch-run 21cmFAST over all 500 parameter combinations:

```python
import py21cmfast as p21c
import h5py, os

# Load precomputed ICs (one shared density field for matched runs)
ics = p21c.initial_conditions(
    user_params={"HII_DIM": 256, "BOX_LEN": 300},
    cosmo_params=p21c.CosmoParams(SIGMA_8=0.815, hlittle=0.678, OMm=0.308),
    random_seed=42,
    write=True
)

REDSHIFTS = [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0]
OUTPUT_DIR = "sims_training/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for idx, (zeta, T_vir, R_mfp) in enumerate(params):
    fname = f"{OUTPUT_DIR}/run_{idx:04d}.h5"
    if os.path.exists(fname):
        continue   # resume-friendly

    lc = p21c.run_lightcone(
        redshift=min(REDSHIFTS),
        max_redshift=max(REDSHIFTS),
        user_params={"HII_DIM": 256, "BOX_LEN": 300},
        astro_params=p21c.AstroParams(
            HII_EFF_FACTOR=zeta,
            ION_Tvir_MIN=T_vir,
            R_BUBBLE_MAX=R_mfp
        ),
        init_box=ics,
        lightcone_quantities=("brightness_temp",),
    )

    with h5py.File(fname, "w") as f:
        f.create_dataset("bt", data=lc.brightness_temp, compression="gzip")
        f.attrs["zeta"]  = zeta
        f.attrs["T_vir"] = T_vir
        f.attrs["R_mfp"] = R_mfp
    
    print(f"  run {idx+1}/{N_TRAIN} done")
```

**Compute budget:** Each 21cmFAST run at 256³ resolution takes ~5–10 min on a modern CPU. 500 runs ≈ 40–80 CPU-hours. This is parallelisable: submit as a Slurm array or use `multiprocessing.Pool`.

---

## Step 2 — EFT Coefficient Extraction (Batch)

Apply the P1 pipeline to every training simulation. This produces the *labels* for model (B).

```python
from p1_pipeline import extract_eft_coefficients   # your P1 module
import h5py, numpy as np, glob, tqdm

output_file = "coefficients_21cmFAST_train.hdf5"
sim_files   = sorted(glob.glob("sims_training/run_*.h5"))

with h5py.File(output_file, "w") as out:
    for idx, fpath in enumerate(tqdm.tqdm(sim_files)):
        with h5py.File(fpath, "r") as f:
            bt      = f["bt"][:]
            zeta    = f.attrs["zeta"]
            T_vir   = f.attrs["T_vir"]
            R_mfp   = f.attrs["R_mfp"]
        
        # extract_eft_coefficients returns a dict with keys:
        # b1, b2, b_nabla2, P_eps, kmax_valid
        # evaluated at each redshift snapshot
        coeffs = extract_eft_coefficients(bt, redshifts=REDSHIFTS)
        
        grp = out.create_group(f"run_{idx:04d}")
        grp.attrs["zeta"]  = zeta
        grp.attrs["T_vir"] = T_vir
        grp.attrs["R_mfp"] = R_mfp
        for key, val in coeffs.items():
            grp.create_dataset(key, data=val)
```

### 2.1 Quality cuts

Not all simulations produce ionization fields within the EFT regime of validity. Flag and remove runs where:

- $\bar{x}_\text{HII} < 0.05$ at $z = 6$ (not yet reionizing)
- $\bar{x}_\text{HII} > 0.99$ at $z = 12$ (fully ionized too early)
- $k_\text{max,valid} < 0.1\,h/\text{Mpc}$ at any target redshift

```python
flags = []
with h5py.File(output_file, "r") as f:
    for key in f.keys():
        grp = f[key]
        xHII_low  = grp["xHII"][REDSHIFTS.index(6.0)]
        xHII_high = grp["xHII"][REDSHIFTS.index(12.0)]
        kmax_min  = np.min(grp["kmax_valid"][:])
        
        bad = (xHII_low < 0.05) or (xHII_high > 0.99) or (kmax_min < 0.1)
        flags.append(bad)

n_removed = sum(flags)
print(f"Quality cut: {n_removed}/{N_TRAIN} runs removed ({100*n_removed/N_TRAIN:.1f}%)")
# Expect < 10% removal for well-chosen parameter bounds
```

---

## Step 3 — Summary Statistic

The observable fed into the NPE is the **21cm brightness temperature power spectrum** $P_{21}(k, z)$. This is a natural choice because:

- It compresses the 3D field (256³ floats ≈ 128 MB) to a manageable vector (~30 $k$-bins × 11 redshifts = 330 numbers)
- It is directly measurable with radio interferometers (HERA, SKA)
- Both simulators output brightness temperature, so the observable is code-agnostic

### 3.1 Computing $P_{21}(k, z)$ for each run

```python
import numpy as np

def power_spectrum_1d(field, box_len, n_bins=30, k_min=0.05, k_max=2.0):
    """
    Compute spherically-averaged 1D power spectrum.
    field: 3D array of shape (N, N, N)
    box_len: physical size in Mpc
    Returns: k_centers, P(k)
    """
    N = field.shape[0]
    dk = 2 * np.pi / box_len
    
    # FFT
    fft = np.fft.rfftn(field) / N**3
    
    # Wavenumber grid
    ki = np.fft.fftfreq(N, d=1.0/N).astype(int)
    kj = np.fft.fftfreq(N, d=1.0/N).astype(int)
    kl = np.arange(N//2 + 1)
    ki3d, kj3d, kl3d = np.meshgrid(ki, kj, kl, indexing='ij')
    kmag = dk * np.sqrt(ki3d**2 + kj3d**2 + kl3d**2)
    
    # Bin
    bins   = np.logspace(np.log10(k_min), np.log10(k_max), n_bins + 1)
    k_cen  = 0.5 * (bins[:-1] + bins[1:])
    Pk     = np.zeros(n_bins)
    
    fft_sq = (np.abs(fft)**2) * (box_len**3)   # units: Mpc³
    
    for ib in range(n_bins):
        mask      = (kmag >= bins[ib]) & (kmag < bins[ib+1])
        Pk[ib]    = np.mean(fft_sq[mask]) if mask.any() else np.nan
    
    return k_cen, Pk

# For each simulation, compute P21 at all redshifts
BOX_LEN = 300.0   # Mpc

# Store as matrix: shape (N_TRAIN, N_z, N_k)
N_K = 30
P21_train = np.zeros((N_TRAIN, len(REDSHIFTS), N_K))

for idx, fpath in enumerate(sim_files):
    with h5py.File(fpath, "r") as f:
        bt = f["bt"][:]    # shape: (N_z, N, N, N) — lightcone slices
    
    for iz, z in enumerate(REDSHIFTS):
        k_cen, Pk = power_spectrum_1d(bt[iz], BOX_LEN)
        P21_train[idx, iz, :] = Pk

np.save("P21_train.npy", P21_train)
np.save("k_centers.npy", k_cen)
```

### 3.2 Log-transform before feeding to the network

Power spectra span many orders of magnitude. Always feed $\log_{10} P_{21}(k, z)$ to the network, not $P_{21}$ directly.

```python
log_P21_train = np.log10(P21_train + 1e-10)   # small offset guards against zeros
```

---

## Step 4 — swyft Setup

[swyft](https://swyft.readthedocs.io) implements Truncated Marginal Neural Ratio Estimation (TMNRE). The idea: train a classifier to distinguish joint samples $(x, \theta)$ from marginal samples $(x, \theta')$, where $x$ is the observation and $\theta$ are the parameters. The classifier's log-ratio is the log-likelihood ratio, from which posterior marginals are extracted.

### 4.1 Install and verify

```bash
conda activate 21cmfast
pip install swyft
python -c "import swyft; print(swyft.__version__)"
```

### 4.2 Defining the swyft store and dataset

```python
import swyft
import torch

# Flatten the summary statistic: (N_z, N_k) → (N_z * N_k,)
X = log_P21_train.reshape(N_TRAIN, -1)   # shape: (500, 330)

# Target labels for model (B): EFT coefficients
# We use redshift-averaged b1, b2, b_nabla2, P_eps (4 numbers per run)
# Or: full redshift sequence (4 × N_z numbers) — start with averaged scalars

with h5py.File("coefficients_21cmFAST_train.hdf5", "r") as f:
    keys = [k for k in f.keys() if not any(k in flags_list)]   # exclude flagged runs
    b1       = np.array([np.mean(f[k]["b1"][:])       for k in keys])
    b2       = np.array([np.mean(f[k]["b2"][:])       for k in keys])
    b_nabla2 = np.array([np.mean(f[k]["b_nabla2"][:]) for k in keys])
    log_Peps = np.array([np.log10(np.mean(f[k]["P_eps"][:])) for k in keys])

theta_EFT    = np.stack([b1, b2, b_nabla2, log_Peps], axis=1)   # (N_train, 4)
theta_native = params[~np.array(flags), :]                        # (N_train, 3)

# Normalise parameters to zero mean, unit variance (swyft best practice)
from sklearn.preprocessing import StandardScaler

scaler_EFT    = StandardScaler().fit(theta_EFT)
scaler_native = StandardScaler().fit(theta_native)
scaler_X      = StandardScaler().fit(X)

theta_EFT_n    = scaler_EFT.transform(theta_EFT)
theta_native_n = scaler_native.transform(theta_native)
X_n            = scaler_X.transform(X)
```

### 4.3 Model architecture

swyft's `RatioEstimator` wraps a neural network that takes $(x, \theta)$ pairs and outputs log-ratios per parameter marginal. The recommended architecture for 1D power spectrum data is a simple MLP:

```python
class SummaryNet(torch.nn.Module):
    """Optional: compress X further before feeding to ratio estimator."""
    def __init__(self, in_dim, out_dim=32):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(in_dim, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, out_dim),
        )
    def forward(self, x):
        return self.net(x)
```

The actual `RatioEstimator` is built using swyft's API:

```python
# Model (B): EFT coefficient targets
simulator_B = swyft.Simulator(
    # swyft expects a callable that maps params → observation
    # here we use the precomputed dataset directly (offline mode)
)

# Use swyft's offline dataset API
class EFTDataset(torch.utils.data.Dataset):
    def __init__(self, X, theta):
        self.X     = torch.tensor(X,     dtype=torch.float32)
        self.theta = torch.tensor(theta, dtype=torch.float32)
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return {"x": self.X[idx], "z": self.theta[idx]}

dataset_B = EFTDataset(X_n, theta_EFT_n)
dataset_A = EFTDataset(X_n, theta_native_n)
```

### 4.4 Training

```python
from torch.utils.data import DataLoader, random_split

def train_model(dataset, n_params, lr=3e-4, n_epochs=50, batch_size=64):
    N    = len(dataset)
    N_tr = int(0.8 * N)
    N_va = N - N_tr
    ds_tr, ds_va = random_split(dataset, [N_tr, N_va])
    
    dl_tr = DataLoader(ds_tr, batch_size=batch_size, shuffle=True)
    dl_va = DataLoader(ds_va, batch_size=batch_size)
    
    in_dim = dataset[0]["x"].shape[0]   # 330
    model  = torch.nn.Sequential(
        torch.nn.Linear(in_dim + n_params, 256),
        torch.nn.ReLU(),
        torch.nn.Linear(256, 128),
        torch.nn.ReLU(),
        torch.nn.Linear(128, n_params),   # one ratio per parameter marginal
    )
    
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    
    train_losses, val_losses = [], []
    for epoch in range(n_epochs):
        model.train()
        epoch_loss = 0.0
        for batch in dl_tr:
            x, z = batch["x"], batch["z"]
            # Binary cross-entropy loss on joint vs marginal pairs
            z_shuffle = z[torch.randperm(len(z))]
            logr_joint    = model(torch.cat([x, z],         dim=1))
            logr_marginal = model(torch.cat([x, z_shuffle], dim=1))
            loss = -torch.mean(
                torch.log_sigmoid(logr_joint) + torch.log_sigmoid(-logr_marginal)
            )
            opt.zero_grad(); loss.backward(); opt.step()
            epoch_loss += loss.item() * len(x)
        
        train_losses.append(epoch_loss / N_tr)
        
        # Validation
        model.eval()
        with torch.no_grad():
            val_loss = 0.0
            for batch in dl_va:
                x, z = batch["x"], batch["z"]
                z_sh  = z[torch.randperm(len(z))]
                lr_j  = model(torch.cat([x, z],  dim=1))
                lr_m  = model(torch.cat([x, z_sh], dim=1))
                loss  = -torch.mean(torch.log_sigmoid(lr_j) + torch.log_sigmoid(-lr_m))
                val_loss += loss.item() * len(x)
        val_losses.append(val_loss / N_va)
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch:3d}: train={train_losses[-1]:.4f}  val={val_losses[-1]:.4f}")
    
    return model, train_losses, val_losses

model_A, losses_A_tr, losses_A_va = train_model(dataset_A, n_params=3)
model_B, losses_B_tr, losses_B_va = train_model(dataset_B, n_params=4)

torch.save(model_A.state_dict(), "model_A_native.pt")
torch.save(model_B.state_dict(), "model_B_eft.pt")
```

### 4.5 Training sanity checks

**Check 1 — Learning curves:** Validation loss should decrease and plateau. If it diverges from training loss: model is overfitting. Fix: reduce network size or add dropout.

**Check 2 — Posterior on training set:** Sample from the learned posterior for a training-set observation. The true parameter value should lie within the 68% credible interval ~68% of the time.

**Check 3 — Prior recovery:** Feed observations simulated far from the training distribution. The posterior should broaden toward the prior — the network should not hallucinate spurious constraints.

---

## Step 5 — In-Distribution Evaluation

Before the cross-simulator test, verify both models perform well on held-out 21cmFAST simulations.

### 5.1 Point-estimate accuracy: $R^2$

```python
from sklearn.metrics import r2_score
import numpy as np

def point_estimate(model, X_obs, scaler_theta, n_samples=1000):
    """Draw samples from the learned posterior and return the median."""
    model.eval()
    x_t = torch.tensor(X_obs, dtype=torch.float32).unsqueeze(0)
    
    # Sample theta from the prior, compute log-ratio, accept/reject (MCMC or IS)
    # Simplified: grid over parameter space and find argmax of logr
    theta_prior = torch.randn(n_samples, scaler_theta.n_features_in_)
    logr = model(torch.cat([x_t.repeat(n_samples, 1), theta_prior], dim=1))
    weights = torch.softmax(logr.squeeze(), dim=0).detach().numpy()
    theta_np = theta_prior.detach().numpy()
    
    # Weighted median (approximate posterior mean for small variance)
    estimate = np.average(theta_np, weights=weights, axis=0)
    return scaler_theta.inverse_transform(estimate.reshape(1, -1)).squeeze()

# Evaluate on validation set
val_indices = range(int(0.8 * N_TRAIN), N_TRAIN)
theta_pred_A = np.array([point_estimate(model_A, X_n[i], scaler_native) for i in val_indices])
theta_pred_B = np.array([point_estimate(model_B, X_n[i], scaler_EFT)    for i in val_indices])

theta_true_A = theta_native[list(val_indices)]
theta_true_B = theta_EFT[list(val_indices)]

r2_A = r2_score(theta_true_A, theta_pred_A, multioutput='raw_values')
r2_B = r2_score(theta_true_B, theta_pred_B, multioutput='raw_values')

print("Model A (native) R²:", r2_A)           # expect > 0.85 for in-dist
print("Model B (EFT)    R²:", r2_B)           # expect > 0.80 for in-dist
```

### 5.2 Coverage test

A well-calibrated posterior should satisfy: the true value falls inside the $\alpha\%$ credible interval exactly $\alpha\%$ of the time (over the ensemble of test observations).

```python
def coverage_fraction(model, X_test, theta_test_n, alpha=0.68, n_samples=2000):
    """
    For each test observation, draw samples from the posterior.
    Check what fraction of true values fall within the alpha-CI.
    """
    inside = 0
    n      = len(X_test)
    for i in range(n):
        x_t   = torch.tensor(X_test[i], dtype=torch.float32).unsqueeze(0)
        theta_true = theta_test_n[i]
        
        theta_samp = torch.randn(n_samples, theta_test_n.shape[1])
        logr       = model(torch.cat([x_t.repeat(n_samples, 1), theta_samp], dim=1))
        weights    = torch.softmax(logr.detach().squeeze(), dim=0).numpy()
        
        # Estimate CI via weighted quantiles
        for j in range(theta_test_n.shape[1]):
            lo = np.quantile(theta_samp[:, j].numpy(), (1 - alpha)/2, weights=weights)
            hi = np.quantile(theta_samp[:, j].numpy(), (1 + alpha)/2, weights=weights)
            if lo <= theta_true[j] <= hi:
                inside += 1

    return inside / (n * theta_test_n.shape[1])

cov_A = coverage_fraction(model_A, X_n[list(val_indices)], theta_native_n[list(val_indices)])
cov_B = coverage_fraction(model_B, X_n[list(val_indices)], theta_EFT_n[list(val_indices)])

print(f"Model A 68% coverage: {cov_A:.3f}  (target: 0.68)")
print(f"Model B 68% coverage: {cov_B:.3f}  (target: 0.68)")
```

✓ Coverage should be 0.68 ± 0.05 for a well-calibrated model.

---

## Step 6 — Cross-Simulator Transfer Test

This is the core experiment of P2.

### 6.1 BEoRN test set

The BEoRN test set consists of ~50 simulations with:
- Matched initial conditions (same 21cmFAST density field + halo catalogs, seed 42)
- Parameter combinations from the P1 test grid (a subset of the P1 36-run grid, or a new 50-run LHS)
- EFT coefficients already extracted by the P1 pipeline
- BEoRN source parameters calibrated to match 21cmFAST global histories (see P1 Step 2d)

```python
# Load BEoRN observables and labels
with h5py.File("P21_BEoRN_test.hdf5", "r") as f:
    X_script   = f["P21"][:]          # (50, N_z, N_k)
    params_script = f["params"][:]    # (50, 3): zeta, T_vir, R_mfp

with h5py.File("coefficients_BEoRN.hdf5", "r") as f:
    keys_sc    = list(f.keys())
    b1_sc      = np.array([np.mean(f[k]["b1"][:])       for k in keys_sc])
    b2_sc      = np.array([np.mean(f[k]["b2"][:])       for k in keys_sc])
    b_nabla2_sc= np.array([np.mean(f[k]["b_nabla2"][:]) for k in keys_sc])
    log_Peps_sc= np.array([np.log10(np.mean(f[k]["P_eps"][:])) for k in keys_sc])

theta_EFT_script    = np.stack([b1_sc, b2_sc, b_nabla2_sc, log_Peps_sc], axis=1)
theta_native_script = params_script   # native params are the same by design

# Preprocess using the *training* scalers (do NOT refit)
log_P21_script = np.log10(X_script.reshape(50, -1) + 1e-10)
X_script_n     = scaler_X.transform(log_P21_script)
theta_EFT_sc_n = scaler_EFT.transform(theta_EFT_script)
theta_nat_sc_n = scaler_native.transform(theta_native_script)
```

### 6.2 Evaluate both models on BEoRN data

```python
# Point estimates on BEoRN
theta_pred_A_sc = np.array([point_estimate(model_A, X_script_n[i], scaler_native) for i in range(50)])
theta_pred_B_sc = np.array([point_estimate(model_B, X_script_n[i], scaler_EFT)    for i in range(50)])

r2_A_sc = r2_score(theta_native_script, theta_pred_A_sc, multioutput='raw_values')
r2_B_sc = r2_score(theta_EFT_script,    theta_pred_B_sc, multioutput='raw_values')

print("BEoRN — Model A (native) R²:", r2_A_sc)
print("BEoRN — Model B (EFT)    R²:", r2_B_sc)

# Coverage on BEoRN
cov_A_sc = coverage_fraction(model_A, X_script_n, theta_nat_sc_n)
cov_B_sc = coverage_fraction(model_B, X_script_n, theta_EFT_sc_n)

print(f"BEoRN — Model A 68% coverage: {cov_A_sc:.3f}")
print(f"BEoRN — Model B 68% coverage: {cov_B_sc:.3f}")
```

### 6.3 Interpreting the results

| Scenario | Model A $R^2$ drops | Model B $R^2$ drops | Interpretation |
|---|---|---|---|
| ✓ Hypothesis confirmed | Yes (large) | No (small) | EFT space is simulator-agnostic |
| ✗ Both drop equally | Yes | Yes | EFT coefficients do not help; morphology dependence persists in the observable |
| ✗ B drops more | No | Yes | EFT coefficients are themselves simulator-dependent to a degree that confuses the network |
| ? A and B both hold | No | No | Both simulators are too similar at this resolution to distinguish |

The last row can be diagnosed by plotting EFT coefficient distributions from both codes — if they overlap completely, the simulators are degenerate in EFT space and the test is underpowered.

---

## Step 7 — Bias and Posterior Width Analysis

Beyond $R^2$, examine the structure of errors:

### 7.1 Systematic bias

```python
# Bias: mean(prediction - truth) over the 50 BEoRN test runs
bias_A = np.mean(theta_pred_A_sc - theta_native_script, axis=0)
bias_B = np.mean(theta_pred_B_sc - theta_EFT_script,    axis=0)

labels_A = [r'$\zeta$', r'$T_\mathrm{vir}$', r'$R_\mathrm{mfp}$']
labels_B = [r'$b_1$',   r'$b_2$',            r'$b_{\nabla^2}$',   r'$\log P_{\varepsilon\varepsilon}$']

print("Model A bias:", dict(zip(labels_A, bias_A)))
print("Model B bias:", dict(zip(labels_B, bias_B)))
```

A non-zero bias indicates that the model has learned simulator-specific features. Model B should have smaller bias than Model A on BEoRN data.

### 7.2 Posterior width

Wide posteriors on BEoRN data (relative to the training distribution) indicate honest uncertainty — the model knows it is out of distribution. Narrow posteriors with high bias are dangerous: the model is confidently wrong.

```python
def posterior_std(model, X_obs, n_samples=2000):
    x_t  = torch.tensor(X_obs, dtype=torch.float32).unsqueeze(0)
    theta = torch.randn(n_samples, model_B.weight_dims)
    logr  = model(torch.cat([x_t.repeat(n_samples, 1), theta], dim=1))
    w     = torch.softmax(logr.detach().squeeze(), dim=0).numpy()
    return np.sqrt(np.cov(theta.T.numpy(), aweights=w + 1e-10))

# Compare posterior widths: 21cmFAST val set vs BEoRN test set
# Model B posteriors should be wider on BEoRN if transfer is imperfect
```

---

## Step 8 — Comparison to Published Baselines

### 8.1 Solt et al. 2026

[SKATR](https://arxiv.org/abs/...) trains a self-supervised Vision Transformer on 21cmFAST 21cm maps and then fine-tunes for parameter inference. It is the closest analogue to our approach — also tested on cross-simulator generalisation.

- Reproduce their reported $R^2$ or coverage figures for the parameters in common ($\zeta$, $T_\text{vir}$)
- Compare side-by-side with Model A's performance on BEoRN data
- Expected: SKATR's representation is richer (full map, not PS) but may be more simulator-specific

### 8.2 EoRFlow (Pietschke et al. 2025)

EoRFlow uses a normalising flow on 3D ionization cubes. Its training set is also 21cmFAST. Its reported cross-code generalisation (if any) provides a reference for how much performance degradation is typical.

### 8.3 Reporting format

For the thesis, present a table:

| Model | Target | Data | $R^2_{\zeta}$ | Coverage 68% | Bias |
|---|---|---|---|---|---|
| A (ours) | native $\theta$ | 21cmFAST (in-dist) | — | — | — |
| A (ours) | native $\theta$ | BEoRN (transfer) | — | — | — |
| B (ours) | EFT $\{b_i\}$ | 21cmFAST (in-dist) | — | — | — |
| B (ours) | EFT $\{b_i\}$ | BEoRN (transfer) | — | — | — |
| SKATR | native $\theta$ | 21cmFAST / BEoRN | — | — | — |

---

## Step 9 — Sanity Checks

| Check | Method | Failure interpretation |
|---|---|---|
| Power spectrum dimensionless | Confirm $P(k) k^3 / (2\pi^2)$ is order unity at $k \sim 0.1\,h/\text{Mpc}$ | Unit error in FFT normalisation |
| Normalisation applied to test with training scalers | Re-apply `scaler_X` without refitting | If refitted, comparison is invalid — the network sees a different input distribution |
| Posterior is proper (integrates to 1) | Check that importance weights sum to 1 | Numerical overflow in softmax — use log-sum-exp |
| Native params are same on both sides | Confirm that the 50 BEoRN test runs used identical calibrated parameters as the matched 21cmFAST runs (see P1 Step 2d) | Parameter mismatch invalidates the comparison |
| Quality of EFT fit | Run the P1 EFT sanity checks on BEoRN data; reject if $k_\text{max,valid} < 0.1$ | If EFT fails on BEoRN, the labels $\theta_\text{EFT}$ are ill-defined |
| No data leakage | Verify validation/test indices do not overlap with training indices | Overly optimistic in-distribution numbers |

---

## Step 10 — Decision Tree

```
Run P2 training
    ↓
In-distribution R² > 0.80 for both models?
    ├── No → increase training set size (add 200 more sims); or simplify summary stat
    └── Yes ↓
Cross-simulator R² (model B) > 0.60?
    ├── No → EFT space has residual simulator dependence
    │         → inspect which coefficient drives the failure
    │         → consider adding 2D PS (k_perp, k_par) for more information
    └── Yes ↓
Model B better than model A on BEoRN?
    ├── No → result is negative; write up null finding with proper analysis
    └── Yes → core hypothesis confirmed
                → tune architecture for best coverage calibration
                → write up
```

---

## Output Files

| File | Contents |
|---|---|
| `P21_train.npy` | Power spectra for all 500 training runs |
| `coefficients_21cmFAST_train.hdf5` | EFT coefficients for training set |
| `model_A_native.pt` | Trained NPE for native parameter inference |
| `model_B_eft.pt` | Trained NPE for EFT coefficient inference |
| `results_indist.npz` | $R^2$, bias, coverage on 21cmFAST validation set |
| `results_transfer.npz` | $R^2$, bias, coverage on BEoRN test set |
| `comparison_table.csv` | Summary table for thesis chapter |

---

## Compute Requirements

| Stage | Runtime | Hardware |
|---|---|---|
| 500 21cmFAST runs (256³) | ~60 CPU-hours | cluster array job |
| EFT extraction (batch P1) | ~2 CPU-hours | single machine |
| NPE training (model A + B) | ~30 min each | GPU (RTX 3080 or V100) |
| Cross-simulator evaluation | ~10 min | CPU |

GPU is strongly recommended for training. On CPU, training 50 epochs over 400 samples takes ~2 hours per model — feasible but slow.

---

## See Also

- [[P1 EFT Characterization]] — upstream pipeline
- [[McQuinn & D'Aloisio 2018]] — EFT coefficient extraction methodology
- [[Pietschke et al 2025 (EoRFlow)]] — normalising flow baseline
- [[Ore et al 2025 (SKATR)]] — self-supervised ViT baseline
- [[Thesis Work]] — high-level timeline and milestones
