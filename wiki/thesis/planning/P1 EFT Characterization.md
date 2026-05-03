---
type: meta
title: "P1 — EFT Characterization: Step-by-Step Plan"
created: 2026-04-21
updated: 2026-04-21
tags:
  - domain/thesis
  - domain/planning
  - domain/eft
status: developing
related:
  - "[[Effective Field Theory]]"
  - "[[Simulation and Codes]]"
  - "[[McQuinn & D'Aloisio 2018]]"
  - "[[Thesis Work]]"
---

# P1 — EFT Characterization: Step-by-Step Plan

**Objective:** Measure the EFT bias coefficients $\{b_1^x, b_2^x, b_{\nabla^2}^x, P_{\varepsilon\varepsilon}\}$ of the ionization field $x_\text{HII}$ across 21cmFAST and BEoRN with matched initial conditions. Map the regime of validity and interpret the differences in EFT language.

**Timeline estimate:** ~10 weeks (see [[Thesis Work]] for the month-by-month schedule)

---

## Step 0 — Anchor the Physics Before Writing Any Code

*Before touching a terminal, be able to answer these questions on paper. This ensures every downstream coding decision is grounded.*

### What are we measuring?

The ionization field $x_\text{HII}(\mathbf{x}, z)$ is a biased tracer of the underlying matter field. On scales larger than a typical ionized bubble, its fluctuation $\delta_x \equiv x_\text{HII} - \bar{x}_\text{HII}$ must be expressible as a sum of operators built from $\delta_m$:

$$
\delta_x(\mathbf{x}, z) = b_1^x\,\delta_m + \frac{b_2^x}{2}\,[\delta_m^2]_\text{renorm} + b_{\nabla^2}^x\,\nabla^2\delta_m + \varepsilon^x(\mathbf{x}, z)
$$

The four terms encode:

| Term | Symbol | Physical meaning |
|------|--------|-----------------|
| Linear bias | $b_1^x$ | Correlation of ionized regions with matter overdensity; driven by source clustering |
| Quadratic bias | $b_2^x$ | Non-linear response; patchiness and overlap of ionized bubbles |
| Derivative (scale) bias | $b_{\nabla^2}^x$ | Non-locality at scale $R_\text{eff}$; encodes effective bubble size via $b_{\nabla^2}^x \approx -R_\text{eff}^2/3$ |
| Stochastic term | $\varepsilon^x$ | Everything the EFT cannot predict; encodes bubble discreteness and sub-grid physics |

### Why does the stochastic term exist?

$\varepsilon^x$ is not noise in the measurement — it is a real physical term. It arises because individual bubble positions are not deterministically set by $\delta_m$ alone; there is inherent scatter from the discrete nature of halos and radiative processes. Its power spectrum $P_{\varepsilon\varepsilon}(k)$ should be:
- Approximately **white (scale-independent)** on large scales (shot noise of bubbles)
- Rising at small scales as bubble geometry matters more
- **Different between codes** because each code has a different sub-bubble implementation

### Why will the coefficients differ between codes?

All simulators must produce a $\delta_x$ that is *describable* by the same operator basis (symmetry argument). But the *values* of the coefficients at each redshift will differ because:
- $b_1^x$ depends on how source clustering is treated (halo mass function, $T_\text{vir}$ mapping)
- $b_2^x$ depends on the non-linear ionization response (bubble overlap physics)
- $b_{\nabla^2}^x$ depends on the effective bubble size, which is set by $R_\text{mfp}$ and recombination treatment
- $P_{\varepsilon\varepsilon}$ depends on discreteness of the bubble field, which is algorithm-specific

### What is the expected size of these differences?

Informed by McQuinn & D'Aloisio 2018 (which compared RT codes):
- $b_1^x$: 10–20% variation across codes (large-scale physics, well-constrained)
- $b_2^x$: 20–40% variation (non-linear response, model-dependent)
- $b_{\nabla^2}^x$: 20–50% variation (bubble morphology, most code-dependent)
- $P_{\varepsilon\varepsilon}$: factor 2–3 variation (shot noise, implementation-specific)

---

## Step 1 — Environment and Code Setup

*Goal: Both simulators running; verified to produce physically reasonable outputs.*

### 1a. Install 21cmFAST in the dedicated conda environment

The group's dedicated environment is `21cmfast` (see vault `CLAUDE.md` for rebuild instructions). Do not install outside it.

```bash
conda activate 21cmfast
python -c "import py21cmfast; print(py21cmfast.__version__)"
# Expected: 4.1.1 or newer
```

### 1b. Install BEoRN

BEoRN is a pure Python package. Install into the existing `21cmfast` conda environment:

```bash
conda activate 21cmfast
pip install git+https://github.com/cosmic-reionization/BEoRN.git
# Or clone for development:
# git clone https://github.com/cosmic-reionization/BEoRN.git && cd BEoRN && pip install -e .
python -c "import beorn; print(beorn.__version__)"
```

**Verify BEoRN installation:**

```python
import beorn
# Run the minimal example from the BEoRN docs / repo README
# Confirm output ionization maps show patchy structure at z ~ 8
# and global history xHII(z) is in a physically plausible range
```

> [!note]
> SCRIPT (Charlotte Mason, Cambridge) was the originally planned secondary code but is no longer publicly accessible. BEoRN is the designated replacement. It is a better fit in any case: it is Python-native and — crucially — accepts 21cmFAST density fields and halo catalogs directly as input (see Step 2).

### 1c. Verify 21cmFAST produces sensible outputs

Run a minimal test simulation and check:

```python
import py21cmfast as p21c
coeval = p21c.run_coeval(
    redshift=8.0,
    user_params={"HII_DIM": 128, "BOX_LEN": 200},
    cosmo_params=p21c.CosmoParams(SIGMA_8=0.815),
    astro_params=p21c.AstroParams(HII_EFF_FACTOR=30.0, ION_Tvir_MIN=4.69897)
)
# Check: coeval.xH_box has values between 0 and 1
# Check: mean neutral fraction is plausible at z=8
print(f"Mean neutral fraction at z=8: {coeval.xH_box.mean():.3f}")
# Expected: ~0.3-0.7 for typical parameters
```

> [!gap]
> BEoRN uses different parameter names and conventions from 21cmFAST. Key mappings:
> - 21cmFAST `HII_EFF_FACTOR` $\approx \zeta$ — no direct BEoRN equivalent; the effective ionizing efficiency emerges from `f_star_10` × `Nion`
> - 21cmFAST `ION_Tvir_MIN` (= $\log_{10}(T_\text{vir}/\text{K})$) — BEoRN uses `M_min` (minimum halo mass in $M_\odot$) as the analogous threshold
> - 21cmFAST `R_BUBBLE_MAX` — BEoRN has no direct free mean-free-path parameter; effective bubble sizes emerge from the profile width
> Document the mapping and calibrated parameter values in a `parameter_mapping.py` file before running the full grid.

---

## Step 2 — Matched Initial Conditions Pipeline

*Goal: Both codes run from the same density field realization, so differences in output are purely from the reionization model, not cosmic variance.*

### 2a. Why matched ICs are straightforward with BEoRN

A key design feature of BEoRN is that it **consumes 21cmFAST outputs directly** — the density field and halo catalog produced by 21cmFAST are BEoRN's native inputs. There is no format conversion or custom glue code. The workflow is:

1. Run 21cmFAST with a fixed `random_seed` to produce $\delta_m(\mathbf{x})$ and halo catalogs
2. Pass the 21cmFAST output directory to BEoRN
3. BEoRN evolves its own source and IGM model on top of the identical density and halo field

This guarantees sub-percent agreement in the matter power spectrum between the two codes by construction.

### 2b. Generating 21cmFAST initial conditions and halo catalogs

```python
import py21cmfast as p21c
import numpy as np

# Generate initial conditions (density field + halo catalogs)
ics = p21c.initial_conditions(
    user_params={"HII_DIM": 256, "BOX_LEN": 300, "USE_FFTW_WISDOM": True},
    cosmo_params=p21c.CosmoParams(SIGMA_8=0.815, hlittle=0.678, OMm=0.308),
    random_seed=42,
    write=True   # write to cache so BEoRN can read the same files
)

# Also run 21cmFAST to produce the perturbed field (includes halo positions)
pt_field = p21c.perturb_field(
    redshift=8.0,
    init_boxes=ics,
    write=True
)

# Save the density field separately if needed
np.save("density_field_seed42.npy", ics.lowres_density)
print(f"Density field shape: {ics.lowres_density.shape}")
print(f"Density field rms: {ics.lowres_density.std():.4f}  (expect ~0.3–0.5)")
```

### 2c. Running BEoRN on the same ICs

BEoRN is configured via a parameter dictionary and told where to find the 21cmFAST cache:

```python
import beorn

# Point BEoRN at the 21cmFAST output directory containing the halo catalogs
# Exact API: consult beorn docs / README for current parameter names
param = beorn.Bunch({
    # Cosmology (must match 21cmFAST exactly)
    'Om': 0.308, 'Ob': 0.0484, 'h0': 0.678, 'sigma8': 0.815, 'ns': 0.968,

    # Box geometry (must match 21cmFAST)
    'Lbox': 300,    # Mpc
    'Nbox': 256,

    # Source model: calibrate to match 21cmFAST global history
    # These are adjusted so xHII(z) matches 21cmFAST at each redshift
    'f_star_10': 0.05,     # stellar fraction at halo mass 10^10 Msun
    'alpha_star': 0.5,     # power-law slope of f_star(M_h)
    'Nion': 5000,          # ionizing photons per stellar baryon

    # Path to 21cmFAST halo catalogs
    'halo_catalog_dir': p21c.config['direc'],   # 21cmFAST cache directory
    'random_seed': 42,
})

# Run BEoRN at the same redshifts as 21cmFAST
grid = beorn.Grid(param)
grid.solve(zstart=12.0, zend=6.0, dz=-0.5)

# Access outputs
xHII_beorn = grid.xHII    # ionization field, shape (N_z, N, N, N)
```

> [!key-insight]
> BEoRN uses the **same halo catalog** produced by 21cmFAST for the given `random_seed`. This means any difference in ionization maps between the two codes arises purely from the ionization prescription — not from different halo populations or density realizations.

### 2d. Calibrating BEoRN to match the global history

BEoRN's source parameters (`f_star_10`, `Nion`, etc.) must be adjusted so that $\bar{x}_\text{HII}(z)$ for BEoRN matches the 21cmFAST global history at each redshift. This is essential for comparing coefficients at the same *physical state* of reionization.

```python
from scipy.optimize import minimize_scalar

# 21cmFAST global history (from a reference run)
xHII_21cmfast = np.array([...])   # at each redshift in REDSHIFTS

def mismatch(log_Nion):
    param.Nion = 10**log_Nion
    grid = beorn.Grid(param)
    grid.solve(zstart=12.0, zend=6.0, dz=-0.5)
    return np.mean((grid.xHII_mean - xHII_21cmfast)**2)

result = minimize_scalar(mismatch, bounds=(3.0, 4.5), method='bounded')
param.Nion = 10**result.x
print(f"Calibrated Nion = {param.Nion:.0f}")
```

### 2e. Sanity check for matched ICs

```python
# Matter power spectra must agree at sub-percent level
P_mm_21cmfast = compute_power_spectrum(ics.lowres_density)
P_mm_beorn    = compute_power_spectrum(grid.density[0])    # first redshift slice

ratio = P_mm_21cmfast / P_mm_beorn
assert np.allclose(ratio, 1.0, rtol=5e-3), \
    f"Matter PS mismatch! Max deviation: {np.abs(ratio - 1).max():.4f}"

# Global reionization histories should also agree after calibration
print("xHII mismatch:", np.abs(grid.xHII_mean - xHII_21cmfast).max())
# Expect < 0.02 (2 percentage points)
```

---

## Step 3 — Define the Simulation Grid

*Goal: Decide which astrophysical parameter combinations to run, and run them.*

### 3a. Parameter space

Use a regular or Latin Hypercube grid over the three main astrophysical parameters. The goal is ~30–40 points for the P1 characterization (enough to see trends, not yet a training set):

| Parameter | Symbol | Range | Points |
|-----------|--------|-------|--------|
| Ionizing efficiency | $\zeta$ | $[10, 50]$ | 4–5 |
| Minimum virial temperature | $T_\text{vir}$ | $[10^4, 10^5]\,\text{K}$ | 3–4 |
| Mean free path | $R_\text{mfp}$ | $[10, 50]\,\text{Mpc}$ | 3–4 |

**Latin Hypercube Sampling (recommended):**

```python
from scipy.stats import qmc

sampler = qmc.LatinHypercube(d=3, seed=0)
sample = sampler.random(n=36)
# Scale to physical ranges
l_bounds = [10,  1e4,  10]  # [zeta, T_vir, R_mfp]
u_bounds = [50,  1e5,  50]
params = qmc.scale(sample, l_bounds, u_bounds)
# params.shape = (36, 3)
```

### 3b. Redshift outputs

Save outputs at enough redshifts to trace the full reionization history, while keeping storage manageable:

```python
redshifts = [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0]
# Roughly: z=6 is end of reionization, z=12 is early
```

At each redshift, save:
- $x_\text{HII}(\mathbf{x}, z)$ — the ionization field (primary target)
- $\delta_m(\mathbf{x}, z)$ — evolved matter density (for EFT basis computation)
- $\bar{x}_\text{HII}(z)$ — global mean (for $\delta_x = x_\text{HII} - \bar{x}_\text{HII}$)

### 3c. Box size and resolution

| Parameter | Recommended | Minimum | Reason |
|-----------|-------------|---------|--------|
| Box length | 300 Mpc | 200 Mpc | Must contain many bubble scales; $R_\text{mfp} \sim 50$ Mpc |
| Grid dimension | 256³ | 128³ | Need $k_\text{max} \sim 1\,h/\text{Mpc}$ to probe EFT breakdown |
| Cell size | ~1.2 Mpc | ~1.5 Mpc | Below typical bubble scale |

> [!gap]
> Memory: 256³ float32 array = 64 MB per field per redshift. 40 parameter sets × 11 redshifts × 2 codes × 2 fields = ~70 GB. Plan disk usage accordingly.

---

## Step 4 — Compute the Perturbative Operator Basis

*Goal: For each simulation, construct the four fields that form the right-hand side of the bias expansion.*

### Why this step is separate

The bias expansion is not fit to the simulation outputs directly — it is fit to a specific set of **perturbative operators** evaluated from the matter density field. These operators must be computed carefully:

- $\delta_m^{(1)}$: linear density field (the actual field from 21cmFAST/BEoRN is already partially non-linear; need to isolate the linear part)
- $\delta_m^{(2)}$: second-order density (gravity-induced mode coupling)
- $[\delta_m^2]_\text{renorm}$: renormalized quadratic field (removes UV divergence)
- $\nabla^2 \delta_m^{(1)}$: Laplacian of linear field (encodes non-locality)

### 4a. Getting $\delta_m^{(1)}$ — the linear density field

21cmFAST uses first-order Lagrangian perturbation theory (1LPT / Zel'dovich approximation) internally. You can extract the linear density field from the initial conditions:

```python
# The initial conditions object already contains the linear density field
# at high z before shell-crossing
delta_linear = ics.lowres_density  # This IS delta_m^(1) at z_init

# To get it at redshift z, scale by the linear growth factor D(z):
from astropy.cosmology import Planck18
import numpy as np

def growth_factor(z, cosmo=Planck18):
    """Linear growth factor D(z), normalized to D(0) = 1."""
    from scipy.integrate import quad
    def integrand(zp):
        return (1 + zp) / cosmo.H(zp).value**3
    result, _ = quad(integrand, z, np.inf)
    norm, _ = quad(integrand, 0, np.inf)
    return result / norm

D_z = growth_factor(z=8.0)
D_0 = growth_factor(z=0.0)
delta_m_linear_z8 = delta_linear * (D_z / D_0)
```

### 4b. Getting $\delta_m^{(2)}$ — second-order density

The second-order correction from gravity is:

$$
\delta_m^{(2)}(\mathbf{k}) = \int \frac{d^3 q}{(2\pi)^3} F_2(\mathbf{q}, \mathbf{k} - \mathbf{q})\, \delta_m^{(1)}(\mathbf{q})\, \delta_m^{(1)}(\mathbf{k} - \mathbf{q})
$$

where $F_2(\mathbf{k}_1, \mathbf{k}_2) = \frac{5}{7} + \frac{1}{2}\frac{\mathbf{k}_1 \cdot \mathbf{k}_2}{k_1 k_2}\!\left(\frac{k_1}{k_2} + \frac{k_2}{k_1}\right) + \frac{2}{7}\left(\frac{\mathbf{k}_1 \cdot \mathbf{k}_2}{k_1 k_2}\right)^{\!2}$ is the gravitational coupling kernel.

In practice, compute in position space using the relation between the displacement fields:

```python
def compute_delta2(delta1_k, kgrid):
    """
    Second-order density from SPT.
    delta1_k: FFT of linear density field
    kgrid: (kx, ky, kz) arrays in Fourier space
    """
    kx, ky, kz = kgrid
    k2 = kx**2 + ky**2 + kz**2
    k2[k2 == 0] = 1  # avoid division by zero at k=0

    # Compute Phi_ij = (ki*kj/k^2) * delta1_k for each pair (i,j)
    # Then delta2 = sum_ij Phi_ij^2 - (sum_i Phi_ii)^2 / ... (tidal field approach)
    # See Baldauf et al. 2016 for the exact implementation
    ...
```

> [!key-insight]
> Computing $\delta^{(2)}$ correctly is non-trivial. Follow the implementation in **Baldauf et al. 2016** (arXiv:1511.01311) exactly. A simpler but less accurate approach: if 21cmFAST uses 2LPT internally (check the source), you can extract $\delta^{(2)}$ directly from the 2LPT displacement field.

### 4c. Computing $[\delta_m^2]_\text{renorm}$ — renormalized quadratic field

The raw square $(\delta_m^{(1)})^2$ has a UV (small-scale) dependence that blows up as resolution increases. Renormalization removes this:

$$
[\delta_m^2]_\text{renorm}(\mathbf{x}) = \left(\delta_m^{(1)}(\mathbf{x})\right)^2 - \sigma^2_L
$$

where $\sigma^2_L = \langle (\delta_m^{(1)})^2 \rangle$ is the **linear variance** (i.e., the mean of the squared linear field over the whole box). This subtracts the UV-divergent constant, leaving only the spatially varying part.

A more complete renormalization that also removes the second-order contribution:

$$
[\delta_m^2]_\text{renorm} = (\delta^{(1)} + \delta^{(2)})^2 - (\delta^{(2)})^2 - \frac{68}{21}\sigma^2_L\,\delta^{(1)}
$$

The factor $68/21$ comes from integrating the $F_2$ kernel. In practice for a first pass, the simpler $(\delta^{(1)})^2 - \sigma^2_L$ is a reasonable approximation.

```python
sigma2_L = np.mean(delta_m_linear**2)
delta2_renorm = delta_m_linear**2 - sigma2_L
# Simple version; for publication use full expression above
```

### 4d. Computing $\nabla^2 \delta_m^{(1)}$ — the Laplacian

In Fourier space, $\nabla^2 \leftrightarrow -k^2$, so this is simply:

```python
import numpy as np

def compute_laplacian(delta_x, box_len):
    """Compute nabla^2 delta in Fourier space."""
    delta_k = np.fft.rfftn(delta_x)
    
    # Build k^2 grid
    n = delta_x.shape[0]
    dk = 2 * np.pi / box_len
    kvals = np.fft.rfftfreq(n, d=box_len/n) * 2 * np.pi
    kx = np.fft.fftfreq(n, d=box_len/n) * 2 * np.pi
    ky = np.fft.fftfreq(n, d=box_len/n) * 2 * np.pi
    kz = kvals
    
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
    k2 = KX**2 + KY**2 + KZ**2
    
    # Laplacian = -k^2 * delta_k in Fourier space
    laplacian_k = -k2 * delta_k
    laplacian_x = np.fft.irfftn(laplacian_k, s=delta_x.shape)
    return laplacian_x
```

> [!key-insight]
> The Laplacian operator has units of $[\text{length}]^{-2}$. When you extract $b_{\nabla^2}^x$, it will have units of $[\text{length}]^2$ (Mpc² or $h^{-2}$ Mpc²). The effective bubble radius is related by $b_{\nabla^2}^x \approx -R_\text{eff}^2 / 3$.

---

## Step 5 — EFT Coefficient Extraction

*Goal: Given $\delta_x$ (from simulation) and the four operator fields (from Step 4), fit the bias coefficients via linear regression in Fourier space.*

### 5a. Why Fourier space?

The bias expansion is a relation between fields. In principle, you can fit it in position space. But Fourier space has two advantages:
1. **Different $k$-modes are independent** under the Gaussian approximation → linear regression is well-behaved
2. **Scale-dependence is explicit** → you can check whether the coefficients are truly constant as a function of $k$ (they should be on large scales, within the EFT regime)

### 5b. Cross-spectrum estimator

The cleanest extraction uses the cross-spectrum between $\delta_x$ and each basis operator. For a basis $\{O_i\}$, the coefficients $b_i$ satisfy:

$$
P_{\delta_x O_j}(k) = \sum_i b_i\, P_{O_i O_j}(k) + P_{\varepsilon O_j}(k)
$$

Since $\varepsilon^x$ is uncorrelated with $\delta_m$ by construction, $P_{\varepsilon O_j} = 0$, so:

$$
\mathbf{b}(k) = \mathbf{C}(k)^{-1}\, \mathbf{p}(k)
$$

where $C_{ij}(k) = P_{O_i O_j}(k)$ (operator cross-spectra matrix) and $p_j(k) = P_{\delta_x O_j}(k)$ (ionization-operator cross-spectra). This is solved at each $k$-bin.

```python
import numpy as np
from powerbox import get_power

def extract_eft_coefficients(delta_x, delta1, delta2_renorm, nabla2_delta1, box_len):
    """
    Extract EFT bias coefficients using cross-spectrum estimator.
    
    Returns: b1, b2, b_nabla2 as arrays over k-bins, plus k values
    """
    operators = [delta1, delta2_renorm, nabla2_delta1]
    names = ['delta1', 'delta2_renorm', 'nabla2_delta1']
    n_ops = len(operators)
    
    # Compute all cross-spectra between operators
    # C_ij = P(O_i, O_j) and p_j = P(delta_x, O_j)
    # Using powerbox for binning
    
    # Get k-bin centers from a fiducial power spectrum call
    P_ref, k_bins = get_power(delta_x, boxlength=box_len)
    n_k = len(k_bins)
    
    C = np.zeros((n_ops, n_ops, n_k))
    p = np.zeros((n_ops, n_k))
    
    for i, Oi in enumerate(operators):
        # Cross of delta_x with each operator
        p[i], _ = get_power(delta_x, Oi, boxlength=box_len)
        for j, Oj in enumerate(operators):
            # Cross of operators with each other
            C[i, j], _ = get_power(Oi, Oj, boxlength=box_len)
    
    # Solve C @ b = p at each k-bin
    b = np.zeros((n_ops, n_k))
    for ik in range(n_k):
        try:
            b[:, ik] = np.linalg.solve(C[:, :, ik], p[:, ik])
        except np.linalg.LinAlgError:
            b[:, ik] = np.nan
    
    b1 = b[0]        # linear bias
    b2 = b[1]        # quadratic bias (note: already 1/2 in expansion)
    b_nabla2 = b[2]  # derivative bias
    
    return b1, b2, b_nabla2, k_bins
```

### 5c. Large-scale averaging

The coefficients should be **approximately constant** over a range of large-scale $k$-bins (the EFT regime). Report the mean over $k \in [0.05, 0.15]\,h/\text{Mpc}$ as the value at each redshift:

```python
k_min, k_max = 0.05, 0.15  # h/Mpc; well within EFT regime
mask = (k_bins >= k_min) & (k_bins <= k_max)

b1_mean   = np.mean(b1[mask])
b2_mean   = np.mean(b2[mask])
b_n2_mean = np.mean(b_nabla2[mask])
```

> [!gap]
> If the coefficients show significant $k$-dependence even at large scales, this signals either:
> 1. A bug in the operator computation (most common)
> 2. Higher-order EFT terms are needed
> 3. The EFT regime is not reached at the available box size
> 
> Diagnose by plotting $b_i(k)$ — it should plateau at large scales before rising or falling at small $k$.

### 5d. What to store

For each (parameter set, code, redshift), store a row in a results table:

```python
results = {
    'code': '21cmFAST',
    'zeta': 30.0,
    'T_vir': 3e4,
    'R_mfp': 30.0,
    'redshift': 8.0,
    'x_HII_mean': 0.65,
    'b1': -0.8,
    'b2': 0.3,
    'b_nabla2': -8.5,   # in (Mpc/h)^2
    'P_ee_amplitude': 1.2e-4,  # see Step 6
    'k_max_eft': 0.28,  # see Step 7
}
```

Save the full table as a pandas DataFrame to HDF5 or CSV:
```python
import pandas as pd
df = pd.DataFrame(results_list)
df.to_hdf('eft_coefficients.h5', key='results', mode='w')
```

---

## Step 6 — Stochastic Term Analysis

*Goal: Measure $P_{\varepsilon\varepsilon}(k, z)$ from the residuals, and compare between codes.*

### 6a. Computing the residuals

After fitting the coefficients, reconstruct the EFT prediction and subtract:

```python
def compute_residuals(delta_x, b1, b2, b_nabla2, delta1, delta2_renorm, nabla2_delta1):
    """
    delta_epsilon = delta_x - (EFT prediction)
    """
    eft_prediction = b1 * delta1 + (b2/2) * delta2_renorm + b_nabla2 * nabla2_delta1
    return delta_x - eft_prediction
```

### 6b. Measuring $P_{\varepsilon\varepsilon}$

```python
delta_epsilon = compute_residuals(...)
P_ee, k_bins = get_power(delta_epsilon, boxlength=box_len)
```

### 6c. What to expect and how to interpret

**Ideal (large-scale) behavior:** $P_{\varepsilon\varepsilon}(k)$ should be approximately flat (white noise) at small $k$. This is the shot noise of the bubble field. The amplitude encodes bubble discreteness.

**Small-scale behavior:** $P_{\varepsilon\varepsilon}(k)$ will rise at $k \gtrsim 1/R_\text{eff}$ as bubble structure becomes resolved.

**Code comparison:** This is the most sensitive diagnostic. If 21cmFAST and BEoRN have different bubble discreteness (different number density of HII regions at the same $\bar{x}_\text{HII}$), they will have different $P_{\varepsilon\varepsilon}$ amplitudes.

```python
# Expected: P_ee ~ constant at large scales
# A shot-noise estimate for N bubbles in volume V:
# P_ee^(shot) ~ V / N_bubbles ~ (4pi/3) R_eff^3
# If P_ee amplitude differs by factor >2 between codes, it indicates
# fundamentally different bubble number densities
```

> [!key-insight]
> $P_{\varepsilon\varepsilon}$ is the novel diagnostic of this thesis. McQuinn & D'Aloisio 2018 measured EFT coefficients but did not systematically compare $P_{\varepsilon\varepsilon}$ across codes. This is where your work goes beyond theirs.

---

## Step 7 — Regime of Validity Mapping

*Goal: Quantify where (in $k$ and $z$) the EFT approximation breaks down.*

### 7a. Definition of EFT power spectrum error

The EFT model prediction for the ionization power spectrum is:

$$
P_{\delta_x}^\text{EFT}(k) = \sum_{i,j} b_i b_j P_{O_i O_j}(k) + P_{\varepsilon\varepsilon}(k)
$$

The error is:
$$
P_\text{err}(k) \equiv P_{\delta_x}^\text{measured}(k) - P_{\delta_x}^\text{EFT}(k)
$$

The **regime of validity** is where $P_\text{err}/P_{\delta_x} < 0.10$ (10% threshold, following McQuinn & D'Aloisio 2018).

### 7b. Computing the error

```python
def compute_eft_power(b1, b2, b_nabla2, P_ee, C, k_bins):
    """
    P_EFT(k) = b1^2 * P_O1O1 + 2*b1*b2 * P_O1O2 + ... + P_ee
    where C[i,j] = P_OiOj
    """
    b = np.array([b1, b2, b_nabla2])
    P_eft = np.einsum('i,ij,j->...', b, C, b) + P_ee
    return P_eft

P_measured, _ = get_power(delta_x, boxlength=box_len)
P_eft = compute_eft_power(...)
P_err = P_measured - P_eft

P_err_frac = np.abs(P_err) / P_measured  # fractional error
k_max_eft = k_bins[np.where(P_err_frac > 0.10)[0][0]]  # first k exceeding threshold
```

### 7c. Building validity maps

Do this across all redshifts and parameter combinations to build a map of $k_\text{max}(z, \zeta, T_\text{vir}, R_\text{mfp})$:

**Physical expectation:**
- $k_\text{max}$ tracks the inverse bubble size: as bubbles grow larger (late reionization), $k_\text{max}$ decreases (EFT breaks down at smaller $k$)
- $R_\text{mfp}$ controls $k_\text{max}$ most directly (larger $R_\text{mfp}$ → larger bubbles → smaller $k_\text{max}$)

---

## Step 8 — Comparison of Coefficient Trajectories Between Codes

*Goal: Produce the core P1 scientific result — how EFT coefficients differ between 21cmFAST and BEoRN.*

### 8a. Matching global histories

Compare coefficients **at the same $\bar{x}_\text{HII}$** (not the same redshift), because different codes may reach the same mean ionization fraction at different times. This is the correct way to compare:

```python
# Interpolate b1(z) onto a common x_HII_mean grid
from scipy.interpolate import interp1d

xHII_grid = np.linspace(0.1, 0.9, 20)

for code in ['21cmFAST', 'BEoRN']:
    xHII_of_z = results[code]['xHII']
    b1_of_z   = results[code]['b1']
    b1_interp = interp1d(xHII_of_z, b1_of_z, bounds_error=False)
    b1_on_grid[code] = b1_interp(xHII_grid)
```

### 8b. Key plots to produce

1. **Coefficient trajectories:** $b_1^x(\bar{x}_\text{HII})$, $b_2^x(\bar{x}_\text{HII})$, $b_{\nabla^2}^x(\bar{x}_\text{HII})$ for both codes on the same axes. Color: 21cmFAST vs BEoRN; shading: variation across parameter grid.

2. **Ratio panels:** $(b_i^\text{BEoRN} - b_i^\text{21cmFAST}) / b_i^\text{21cmFAST}$ — fractional difference, shows where codes disagree most.

3. **$P_{\varepsilon\varepsilon}$ comparison:** Stochastic power amplitude vs $\bar{x}_\text{HII}$ for both codes.

4. **Validity maps:** $k_\text{max}(z)$ for both codes and its dependence on $R_\text{mfp}$.

### 8c. Physical interpretation

For each difference observed, ask: *which aspect of the code implementation is responsible?*

| Observation | Likely cause |
|-------------|-------------|
| $b_1^x$ agrees, $b_{\nabla^2}^x$ differs | Bubble morphology differs (BEoRN profile model vs excursion-set) |
| $b_1^x$ differs significantly | Source clustering treated differently (different halo mass functions or $T_\text{vir}$ mapping) |
| $P_{\varepsilon\varepsilon}$ differs strongly | Discrete bubble number density differs |
| $k_\text{max}$ systematically lower for one code | That code produces larger bubbles (different $R_\text{mfp}$ effective scale) |

---

## Step 9 — Sanity Checks and Known Failure Modes

Run these checks **throughout** the pipeline, not just at the end.

| Check | How to verify | What failure means |
|-------|---------------|-------------------|
| ICs are matched | $P_{mm}^\text{21cmFAST} / P_{mm}^\text{BEoRN} = 1.000 \pm 0.001$ | IC pipeline broken |
| EFT coefficients are $k$-independent at large scales | Plot $b_i(k)$; should plateau for $k < 0.1\,h/\text{Mpc}$ | Operator basis computed incorrectly |
| $b_1^x$ sign and magnitude reasonable | At $\bar{x}_\text{HII} = 0.5$: $b_1^x \approx -0.5 $ to $+0.5$ (near zero during mid-reionization by construction) | Major bug in regression |
| $\sigma^2_L$ subtraction has removed UV divergence | Confirm $\langle [\delta^2]_\text{renorm} \rangle \approx 0$ | Renormalization wrong |
| $P_\text{err}/P_{21} < 10\%$ at large scales | Must hold by construction if fitting is done right | Overfitting or underfitting |
| Stochastic power is roughly white on large scales | Plot $P_{\varepsilon\varepsilon}(k)$; should be flat for $k < k_\text{max}$ | Subtraction of EFT prediction is wrong |

---

## Outputs of P1

At the end of this work package, you will have:

- `eft_coefficients.h5` — full results table with $\{b_i, P_{\varepsilon\varepsilon}, k_\text{max}\}$ for all (code, params, redshift)
- Plots: coefficient trajectories, ratio panels, $P_{\varepsilon\varepsilon}$ comparison, validity maps
- A calibrated matched-IC pipeline usable by P2
- ~30–40 paired 21cmFAST + BEoRN simulations with matched ICs

These directly feed into [[P2 Cross-Simulator Inference]] — the training set for P2 begins from the P1 pipeline.
