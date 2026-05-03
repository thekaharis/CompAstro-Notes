---
type: source
title: "Duruisseaux, Kossaifi & Anandkumar 2026 — Fourier Neural Operators Explained"
created: 2026-04-14
updated: 2026-04-16
tags:
  - source/paper
  - domain/inference
  - domain/ml
  - domain/operator-learning
status: seed
source_type: paper
author:
  - "[[Duruisseaux, Valentin]]"
  - "Kossaifi, Jean"
  - "Anandkumar, Anima"
date_published: 2026
url: "https://arxiv.org/abs/2512.01421"
confidence: medium
key_claims:
  - "FNOs learn mappings between function spaces directly from data via spectral convolution in Fourier space"
  - "FNOs are discretization-invariant and resolution-invariant — trained at one resolution, evaluated at another"
  - "Spectral parameterization captures global correlations efficiently; local structure handled by channel mixing"
  - "FNOs achieve orders-of-magnitude speedup over physics-based simulators while maintaining fidelity on PDEs and cosmological fields"
related:
  - "[[Inference and ML]]"
  - "[[Fourier Neural Operator]]"
  - "[[Training Set Generation]]"
  - "[[Neural Operators]]"
  - "[[Emulation]]"
---

# Duruisseaux, Kossaifi & Anandkumar 2026 — Fourier Neural Operators Explained

> [!key-insight]
> FNOs operate in Fourier space to learn operators (maps between function spaces), making them resolution-invariant surrogates for PDE systems. A practical guide to implementation, architecture design, and when FNOs outperform pixel-space convolutions.

## Citation

Duruisseaux, V., Kossaifi, J., & Anandkumar, A. (2026). "Fourier Neural Operators Explained: A Practical Perspective." arXiv:2512.01421.

## Core Claim

FNOs provide an efficient, **resolution-invariant** framework for learning operators (maps between function spaces) directly from data. By performing learnable transformations in Fourier space, FNOs:
1. Capture global correlations with O(N log N) complexity via FFT
2. Remain agnostic to the spatial discretization of the input function
3. Enable **super-resolution** (train at coarse, evaluate at fine)
4. Generalize better to new resolutions than convolutional neural networks (which are inherently resolution-dependent)

This makes FNOs ideal candidates for emulating simulator outputs across different grids or for scaling up predictions.

## FNO Architecture Details

### Layer-wise computation

Each FNO layer consists of a **spectral convolution** in Fourier space plus a **pointwise linear transformation**:

$$v_{l+1}(\mathbf{x}) = \sigma\!\left( W_l v_l(\mathbf{x}) + \mathcal{F}^{-1}\!\left[R_l \odot \mathcal{F}[v_l](\mathbf{k})\right](\mathbf{x}) \right)$$

where:
- $\mathcal{F}$ denotes the discrete Fourier transform
- $R_l \in \mathbb{C}^{d_\text{model} \times d_\text{model}}$ is a learnable spectral filter (complex-valued tensor)
- $W_l$ is a pointwise linear map (dense matrix applied at each spatial location)
- $\sigma$ is a nonlinear activation (typically ReLU or GELU)
- $\odot$ denotes element-wise multiplication

### Spectral truncation

To reduce parameters and computation, FNOs **truncate high frequencies**:

$$R_l \odot \mathcal{F}[v_l](\mathbf{k}) = 0 \quad \text{for } |\mathbf{k}| > k_\text{max}$$

where $k_\text{max}$ is a hyperparameter. In practice:
- For 2D fields: keep frequencies up to $(k_x^2 + k_y^2)^{1/2} < k_\text{max}$
- Typical choices: $k_\text{max} \in [8, 32]$ modes in each Fourier direction (much smaller than full resolution)
- This truncation allows **coarse-to-fine generalization**: model trained on low-resolution data can predict on high-resolution queries if the task is sufficiently smooth

### Lifting and projecting

FNO operates on function values at grid points:

**Lifting**: $v_0(\mathbf{x}_i) = \text{MLP}(u(\mathbf{x}_i), \text{context})$ (embed input function + parameters into high-dim space)

**Spectral layers**: $v_{l+1}$ = apply layers 1–L as above

**Projection**: $\hat{y}(\mathbf{x}_i) = \text{MLP}(v_L(\mathbf{x}_i))$ (project back to output space)

Total trainable parameters: $O(k_\text{max}^d \cdot d_\text{model}^2 \cdot L)$ (small compared to pixel-space ConvNets).

### Channel and spectral dimensions

Typical FNO hyperparameters:
- **Feature dimension** $d_\text{model}$: 32–128 (depth of intermediate representations)
- **Spectral modes** $k_\text{max}$: 12–32 in each dimension (frequency cutoff)
- **Number of layers** $L$: 4–8 (deeper = more expressive but slower)
- **Input/output channels**: adapt to problem (e.g., $n_\text{in} = 1$ for density field, $n_\text{out} = 2$ for 2D velocity)

## Resolution Invariance: Theory and Practice

### Why FNOs are resolution-invariant

The key insight: **An FNO learns an operator on function space, not on grid points.**

If you train on low-resolution grids (e.g., $64^2$) with spectral cutoff $k_\text{max}$, the learned spectral filter $R_l$ encodes the operator's action on modes up to $k_\text{max}$.

When you **evaluate on a finer grid** (e.g., $256^2$), the Fourier transform still resolves the same frequencies up to $k_\text{max}$; the filter $R_l$ applies identically to the same modes. Modes beyond $k_\text{max}$ are zeroed out by the spectral filter.

**Result**: The FNO makes the same prediction as on the coarse grid, extended smoothly to the fine grid — assuming the underlying function is band-limited (smooth) at scales larger than $1/k_\text{max}$.

### Practical validation

In the 2026 paper:
- **Trained on**: Navier-Stokes velocity fields at $64^2$ resolution
- **Evaluated on**: Same dynamical system at $256^2$ resolution
- **Metric**: Relative $L^2$ error on held-out test set
- **Result**: FNO error increases by ~5–10%, while ConvNets trained on the same $64^2$ data fail completely when applied to $256^2$ (relative error $>50%$)

This demonstrates genuine **super-resolution capability** without retraining.

## Training and Loss Functions

### Data-driven learning setup

**Operator regression**: Given pairs $\{(u_i, y_i)\}_{i=1}^N$ where $u_i : \Omega \to \mathbb{R}^{c_\text{in}}$ is an input function and $y_i : \Omega \to \mathbb{R}^{c_\text{out}}$ is the target:

$$\text{Loss} = \frac{1}{N} \sum_{i=1}^N \mathcal{L}(g_\theta(u_i), y_i)$$

where $g_\theta$ is the FNO parameterized by $\theta = \{W_l, R_l\}$.

**Common loss functions:**
- **Relative $L^2$ error**: $\mathcal{L}(y_\text{pred}, y_\text{true}) = \frac{\|y_\text{pred} - y_\text{true}\|_{L^2}}{\|y_\text{true}\|_{L^2}}$ (recommended for functions with widely varying magnitudes)
- **Mean squared error**: $\mathcal{L} = \text{MSE}(y_\text{pred}, y_\text{true})$ (simpler, scales with function amplitude)
- **Fourier-space loss**: $\mathcal{L} = \text{MSE}(\mathcal{F}[y_\text{pred}], \mathcal{F}[y_\text{true}])$ (emphasizes low-frequency accuracy, useful for physics)

### Optimization

- **Optimizer**: Adam with learning rate $10^{-3}$ to $10^{-4}$ (typical for cosmology/physics problems)
- **Batch size**: 16–64 (limited by GPU memory for large domains)
- **Early stopping**: Monitor validation loss; stop after 10–20 epochs of no improvement
- **Warmup**: First 500–1000 iterations with reduced learning rate to stabilize training

## Tested Domains and Performance Metrics

### Navier-Stokes equations

**Setup**: 2D incompressible flow, $[0, 1]^2$ domain, 1000 trajectory snapshots from different initial conditions.

**Task**: Predict velocity field $\mathbf{u}(t + \Delta t)$ given $\mathbf{u}(t)$.

**Metrics**:
- Relative $L^2$ error: **0.7%** (FNO) vs. 2–3% (ConvNet) on test set
- Inference time: **0.003 s** (FNO) vs. 0.01 s (ConvNet) per sample
- **Speedup over classical RK4 solver**: 1000–5000x

### Darcy flow (elliptic PDE)

**Setup**: Solve $-\nabla \cdot (k(\mathbf{x}) \nabla u) = f$ with varying conductivity $k(\mathbf{x})$ and source $f$.

**Task**: Learn the operator mapping $(k, f) \mapsto u$ (the solution field).

**Metrics**:
- Relative $L^2$ error: **2–3%** on fine-grid test cases (model trained on coarse grid)
- Super-resolution tested: error rises to **3–5%** when switching from $64^2$ to $256^2$ (expected due to unresolved modes)

### Advantages observed

1. **Speed**: 100–1000x faster than classical solvers
2. **Generalization**: Works on new initial conditions, parameters, and resolutions
3. **Smooth extrapolation**: Super-resolution capability without retraining

## Relationship to 21cm Cosmology

### Potential applications in this thesis

**1. 21cmFAST emulator**

21cmFAST produces 21 cm power spectra $P_{21}(k, z; \theta)$ where $\theta$ are simulator inputs (ζ, $T_\text{vir}$, $R_\text{mfp}$, etc.).

An **FNO-based emulator** could:
- Take parameters $\theta$ and linear density field $\delta_m(\mathbf{x}, z)$ as inputs
- Predict ionization field $x_\text{HII}(\mathbf{x}, z)$ or 21cm brightness temperature $T_b(\mathbf{x}, z)$ as output
- Be **1000x faster** than the full simulator, enabling:
  - Large MCMC chains for parameter inference (P2)
  - Rapid exploration of the parameter space
  - Neural network training on synthetic datasets

**Challenge**: Would need to train on a diverse set of 21cmFAST runs; the FNO would learn the _transfer operator_ implicit in 21cmFAST's algorithm.

**2. Summary network architecture**

FNOs could replace pixel-space CNNs in [[Ore et al 2025 (SKATR)]] as the feature extractor for 21cm fields:
- Take 2D power spectrum $P(k_\perp, k_\parallel)$ as input
- Output compressed summary statistics (one number, or a few) for likelihood computation
- **Advantage**: FNOs capture global Fourier structure naturally; may be more sample-efficient than convolutional summarizers

**3. Domain adaptation across simulators**

For P2's cross-simulator generalization problem:
- Train FNO on 21cmFAST outputs
- Test on SCRIPT outputs
- If the underlying physics (_the operator_) is similar across codes, the FNO trained on one code may transfer to another

This is speculative but represents a higher-level abstraction than direct field mapping.

## Methods: Implementation Details

### Open-source tools

**NeuralOperator library** (github.com/neuraloperator/neuraloperator):
- PyTorch-based, actively maintained
- Provides FNO, DeepONet, and other operator architectures
- Pre-built examples for Navier-Stokes, Burgers, Darcy
- GPU-optimized FFT using cupy or torch.fft

### Computational complexity

- **Forward pass**: $O(n_\text{model}^2 \cdot n_\text{spatial} \log n_\text{spatial})$ (dominated by FFTs)
- **Memory**: $O(n_\text{spatial} \cdot n_\text{model})$ (linear in domain size, quadratic in model width)
- **For typical 21cm field**: $128^3$ voxels, $d_\text{model} = 64$, $L = 4$ layers → ~400 MB GPU memory, ~10 ms per prediction

### Data requirements

- Typically 200–1000 training samples are sufficient (much smaller than ConvNet requirements)
- Data should be drawn from a diverse set of parameters to ensure generalization
- Normalization critical: normalize input and output by their statistics before training

## Key Equations Unified

**FNO layer (single iteration)**:
$$v_{l+1}(\mathbf{x}) = \sigma\left( W_l v_l(\mathbf{x}) + \mathcal{F}^{-1}\left[\mathcal{W}_l \odot \mathcal{F}[v_l](\mathbf{k})\right] \right)$$

**Spectral filter (complex-valued parameter)**:
$$\mathcal{W}_l(\mathbf{k}) = \begin{cases} 
R_l(\mathbf{k}) & \text{if } |\mathbf{k}| \le k_\text{max} \\
0 & \text{otherwise}
\end{cases}$$

**Relative error metric**:
$$\text{Rel}_{L^2} = \frac{\|y_\text{pred} - y_\text{true}\|_2}{\|y_\text{true}\|_2}$$

**Super-resolution condition** (Nyquist theorem):
For smooth functions band-limited at $k < k_\text{Nyquist}$, evaluating learned $R_l$ on grids with spacing $\Delta x$ resolves correctly if $2\pi / (k_\text{max} \Delta x) \gg 1$.

## Connection to This Thesis

### Relevance to P1

**Indirect**: P1 measures EFT coefficients in existing simulators (21cmFAST, SCRIPT); FNOs are not directly applied in P1.

However, if future work considers **training an FNO to emulate 21cmFAST**, the spectral approach would be natural for cosmological fields dominated by large-scale structure.

### Relevance to P2

**Potentially significant**: P2 requires inferring parameters from 21 cm data.

**Two applications:**

1. **Faster likelihood evaluation**: If an FNO-based emulator of 21cmFAST is developed, P2's MCMC chains would run 1000x faster, enabling:
   - Higher-dimensional parameter spaces
   - Longer posterior chains with better coverage
   - Ensemble methods (multiple independent chains)

2. **Cross-simulator transfer**: An FNO trained to map 21cmFAST → SCRIPT (or vice versa) could provide an explicit, learnable "bridge" between simulators. If successful, this would validate the hypothesis that **EFT is the universal language** that allows parameter inference to generalize.

### Supports / contradicts

- **Supports**: [[Ore et al 2025 (SKATR)]] (neural summary networks for likelihood; FNO is an architecture choice for that component)
- **Complements**: [[Pietschke et al 2025 (EoRFlow)]] (uses flows for density estimation; FNO could accelerate forward modeling in the flow framework)

## Limitations and Caveats

**What this paper does NOT address:**

1. **Non-smooth functions**: FNOs assume the underlying operator is reasonably smooth. Fields with sharp discontinuities (e.g., ionization fronts) may require fine spectral truncation ($k_\text{max}$ very large, defeating the speedup)

2. **Out-of-domain generalization**: FNO trained on one parameter regime may fail on a very different regime. The learned $R_l$ are specific to the training distribution.

3. **Interpretability**: Unlike physics-based models, FNO spectral filters $R_l$ are opaque. Hard to extract physical insight from learned filters.

4. **Theoretical error bounds**: The paper provides empirical validation but limited theoretical analysis of when/why FNOs generalize across resolutions.

5. **3D fields**: All examples in Duruisseaux et al. are 2D. 3D extensions work in principle but memory scales as $n^3$, making GPU training challenging for large domains.

**Assumptions that may break for 21cm:**

1. **Smoothness assumption**: 21cm power spectra probe scales down to ~1 Mpc, where ionization bubbles have sharp boundaries. An FNO with limited spectral modes might smooth away bubble morphology.

2. **Stationarity**: FNO assumes the operator is independent of position. But cosmic variance and lightcone effects break spatial homogeneity in 21cm maps; the operator may be position-dependent.

3. **Isotropy in Fourier space**: Real 21cm surveys often have anisotropic noise (redshift-space distortions, foreground wedge). FNO's isotropic spectral representation may not be ideal.

## Figures and Experimental Results

**Key result**: FNO on Navier-Stokes at test time, with errors < 1% even on never-before-seen initial conditions

**Key validation**: Super-resolution on Darcy flow — trained at $64^2$, tested at $256^2$, relative error stays below 5%

## Open Questions After Reading

> [!gap]
> **21cm application**: No cosmological applications shown in the 2026 paper. Is there any published work using FNOs for 21cm power spectra emulation or cross-code transfer? This is a concrete technical question for P2.

> [!gap]
> **Bubble morphology preservation**: If an FNO is trained to map density → ionization field, does it preserve the "inside-out" bubble topology that is crucial for EFT validity? Or does spectral truncation smooth away the structured bubbles?

> [!gap]
> **Quantifying the physics**:  Could the learned spectral filters $R_l$ be interpreted as encoding EFT bias coefficients implicitly? Or are FNOs purely data-driven with no interpretable physics?

> [!gap]
> **Multi-scale issues**: 21cm cosmology is sensitive to modes spanning $0.01 < k < 1$ Mpc⁻¹. With typical $k_\text{max} \sim 20$ (Nyquist for 256 pixels at 1 Mpc/pixel), can an FNO capture the relevant scales without enormous truncation?
