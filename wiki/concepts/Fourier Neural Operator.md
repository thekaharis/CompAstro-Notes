---
type: concept
title: "Fourier Neural Operator"
created: 2026-04-14
updated: 2026-04-16
tags:
  - concept/ml
  - domain/inference
status: seed
complexity: advanced
domain: "[[Inference and ML]]"
aliases:
  - "FNO"
  - "Neural Operator"
related:
  - "[[Training Set Generation]]"
  - "[[Simulation-Based Inference]]"
sources:
  - "[[Duruisseaux et al 2026 (FNO)]]"
---

# Fourier Neural Operator

## Definition: Operators vs. Neural Networks

A crucial distinction underpins the Fourier Neural Operator (FNO) framework:

### Standard Neural Networks

A standard neural network is a **function** mapping vectors to vectors:

$$f: \mathbb{R}^{n_{\text{in}}} \to \mathbb{R}^{n_{\text{out}}}$$

The network is trained on fixed-size inputs and outputs. If you change the input size (e.g., from 128×128 images to 256×256 images), you must retrain the network — the weights don't transfer.

Example: A CNN trained on $128^3$ density fields cannot evaluate on $256^3$ fields without retraining.

### Operators

An **operator** is a map between **function spaces** rather than finite-dimensional vector spaces:

$$\mathcal{G}: u(x) \mapsto v(x)$$

An operator takes an entire function (defined on a continuum of points) and maps it to another function. This is fundamentally more general than a neural network's vector-to-vector map.

**Key advantage**: An operator is **resolution-invariant**. If you learn an operator on a discretized representation with $N = 128^3$ grid points, the same learned operator can be applied to a finer discretization with $N = 256^3$ grid points, without retraining.

### Intuition via Physics

In physics, Green's functions are operators: given a source distribution $\rho(x)$, the gravitational potential $\Phi(x)$ is computed via convolution with the Green's function:

$$\Phi(x) = \int G(x - x') \rho(x') d^3 x'$$

This is an operator that maps the source field to the potential field, independent of discretization. FNOs essentially learn to approximate such operator relationships directly in Fourier space.

## Mathematical Form: The FNO Architecture

### Components of an FNO Layer

Each FNO layer computes:

$$v_{l+1}(\mathbf{x}) = \sigma\left(W_l\, v_l(\mathbf{x}) + \mathcal{F}^{-1}\left[R_l(\mathbf{k})\cdot \mathcal{F}[v_l](\mathbf{k})\right](\mathbf{x})\right)$$

where:
- **$v_l(\mathbf{x})$**: The field representation at layer $l$ (spatial or real-space form)
- **$\mathcal{F}$**: The **Fourier transform** operator
- **$\mathcal{F}[v_l](\mathbf{k})$**: Fourier coefficients of the input field at wavenumber $\mathbf{k}$
- **$R_l(\mathbf{k})$**: A **learnable spectral filter** in Fourier space (weight matrix in frequency domain); values at different wavenumbers are independent parameters
- **$\mathcal{F}^{-1}[\cdot](\mathbf{x})$**: **Inverse Fourier transform**, returning to real space
- **$W_l\, v_l(\mathbf{x})$**: A **pointwise linear transformation** (bypass term) that handles local structure
- **$\sigma$**: A **nonlinear activation** (ReLU or similar)

Breaking this down:

1. **Fourier transform**: Convert input to frequency domain
2. **Spectral filtering**: Multiply by learned filter $R_l(\mathbf{k})$; this couples all spatial locations simultaneously (global interaction)
3. **Inverse transform**: Return to real space
4. **Add local pathway**: Add the pointwise linear term $W_l v_l$ to capture local features that spectral truncation misses
5. **Nonlinearity**: Apply activation

### Why Spectral Filtering Works

Many physical processes (heat diffusion, wave propagation, gravity) can be naturally expressed as convolutions in real space, which become **multiplications in Fourier space**. The Green's function for a PDE is a convolution kernel; learning it in Fourier space via multiplication is elegant and efficient.

For a linear PDE solved via Green's function:
$$v(\mathbf{x}) = \int G(\mathbf{x} - \mathbf{x}') u(\mathbf{x}') d^3\mathbf{x}'$$

In Fourier space, this becomes:
$$\widehat{v}(\mathbf{k}) = G(\mathbf{k}) \widehat{u}(\mathbf{k})$$

The spectral filter $G(\mathbf{k})$ is the Fourier transform of the Green's function. FNOs essentially learn these filters directly as parameters $R_l(\mathbf{k})$.

## Spectral Truncation at $k_{\max}$

A crucial practical detail: FNOs don't use all $N_{\text{grid}}$ Fourier modes. Instead, they **truncate** to the first $N_{\text{modes}}$ lowest-wavenumber modes:

$$R_l(\mathbf{k}) \in \mathbb{C}^{N_{\text{modes}} \times N_{\text{modes}}}$$

For a 3D problem with $N_{\text{grid}} = 256^3$ voxels, one might use $N_{\text{modes}} = 32^3$ or $64^3$ modes, discarding higher-frequency information.

### Why Truncate?

1. **Noise dominance**: Higher-frequency modes are dominated by noise and sub-grid-scale physics; they don't contain robust signal
2. **Computational cost**: Keeping all $N_{\text{grid}}$ modes makes each layer $\mathcal{O}(N_{\text{grid}} \log N_{\text{grid}})$; truncating to $N_{\text{modes}} \ll N_{\text{grid}}$ reduces cost to $\mathcal{O}(N_{\text{modes}}^2 \log N_{\text{modes}})$
3. **Generalization**: High-frequency modes are often simulator-specific; truncating forces the model to focus on large-scale, physics-based features

### The Number of Learned Parameters

For each layer $l$, the spectral filter $R_l(\mathbf{k})$ has:
$$\text{Parameters per layer} = N_{\text{modes}} \times N_{\text{modes}} \times \text{channels}_l^2$$

(The $\text{channels}^2$ factor arises because there can be multiple input and output channels, and the filter acts on the tensor product.)

For $N_{\text{modes}} = 32$ and 64 channels:
$$\text{Parameters} \sim 32^2 \times 64^2 \sim 4 \times 10^6$$

This is large but still manageable for GPU training. The key insight is that the spectral filter has **no spatial locality assumption** — each Fourier mode can interact with all other modes, yielding a fully general operator in that reduced basis.

## Key Properties of FNOs

### 1. Resolution Invariance (Demonstrated)

A remarkable empirical finding: **train on $64^3$ grid, infer on $256^3$ grid** using the same learned weights, with minimal performance degradation.

**How this works**:
- Training on $64^3$: Learn filters $R_l(\mathbf{k})$ for $N_{\text{modes}}$ low modes
- Inference on $256^3$: Compute Fourier transform of the input (now finer resolution), apply the same learned filters to the low modes, invert
- The high-resolution information is encoded in the fine scales of the input; the learned filters operate on the same low-mode subspace regardless of overall resolution

This is a major advantage over neural networks or CNNs, which are discretization-specific.

### 2. Global Receptive Field via Spectral Convolution

The spectral multiplication in Fourier space couples **all spatial locations simultaneously**:
$$\widehat{v}_{l+1}(\mathbf{k}) = R_l(\mathbf{k}) \widehat{v}_l(\mathbf{k})$$

In real space, this corresponds to a non-local convolution with a global support. There is no "local neighborhood" in the FNO operation — every point interacts with every other point at each layer, encoded by the coupling via Fourier modes.

This global interaction is achieved with $\mathcal{O}(N \log N)$ complexity via FFT, compared to $\mathcal{O}(N^2)$ for explicit attention mechanisms.

### 3. Computational Advantage: FFT Speed

The **Fast Fourier Transform (FFT)** is the enabling technology:
$$\text{FFT complexity} = \mathcal{O}(N \log N) \quad \text{for } N \text{ grid points}$$

Compare to:
- **Spectral filtering** (if done naively): $\mathcal{O}(N^2)$ for a full matrix-vector product in Fourier space
- **Attention** (as in ViTs): $\mathcal{O}(N^2)$ for pairwise interactions
- **Convolution** (as in CNNs): $\mathcal{O}(N \times \text{kernel size}^d)$, roughly $\mathcal{O}(N)$ for fixed kernel size

For $N = 256^3 = 16 \times 10^6$ voxels:
- **FFT**: $16 \times 10^6 \times \log(16 \times 10^6) \sim 4 \times 10^8$ operations (milliseconds on GPU)
- **Attention**: $(16 \times 10^6)^2 \sim 2.5 \times 10^{14}$ operations (hours on GPU)
- **FNO can be 100–1000× faster than ViT** for field-level inference

## The Local Bypass: Why $W_l$ Matters

A naive spectral-only FNO (no $W_l$ term) would have a critical flaw: **spectral truncation loses sharp local features**.

### The Problem with Pure Spectral Filtering

Consider an **ionization front** (a sharp boundary where $x_\text{HI}$ transitions from ~1 to ~$10^{-3}$ over ~1 kpc). This sharp feature has high-frequency Fourier components. If these high frequencies are truncated, the reconstructed field becomes blurry — the I-front is smoothed out.

### The Solution: Pointwise Linear Transform

The term $W_l v_l(\mathbf{x})$ is a **pointwise linear operation**: at each location $\mathbf{x}$, apply a fixed linear transformation to the field value(s):

$$[W_l v_l](\mathbf{x}) = W_l v_l(\mathbf{x})$$

This is applied **after** the spectral filtering in the layer. The pointwise transform can learn to enhance or suppress features at specific locations, adding back local detail that was lost due to spectral truncation.

**Combined form**:
$$v_{l+1}(\mathbf{x}) = \sigma\left(\underbrace{\mathcal{F}^{-1}[R_l(\mathbf{k}) \mathcal{F}[v_l]](\mathbf{x})}_{\text{global spectral}} + \underbrace{W_l v_l(\mathbf{x})}_{\text{local pointwise}}\right)$$

This combination is called a **U-Net-like connection** in FNO literature: the global operator (spectral) is supplemented by a local pathway (pointwise) for fine-scale detail.

## Why FNOs Are Suited to Physics/PDEs

### Green's Function Perspective

Many physical processes are governed by linear PDEs with Green's function solutions:
$$v(\mathbf{x}) = \int G(\mathbf{x}, \mathbf{x}') f(\mathbf{x}') d^3\mathbf{x}'$$

**Examples**:
- **Gravity**: Potential $\Phi$ from density $\rho$ via Newton's law
- **Electromagnetism**: Fields $\mathbf{E}, \mathbf{B}$ from charge/current distributions
- **Heat diffusion**: Temperature $T$ from heat source distribution

For these problems, the Green's function encodes all the physics. In Fourier space, the Green's function becomes a multiplicative operator (simple filter). **FNOs directly learn this filter**, making them naturally suited to such problems.

### Generalization to Nonlinear Problems

While pure Green's function problems are linear, FNOs can approximate nonlinear PDEs by stacking multiple layers (each layer = one time step or iteration). The nonlinearity in the activation functions allows the model to approximate complex solution operators.

### Example: Predicting Reionization Field Evolution

A speculative application: given the ionization field at redshift $z_1$, predict it at redshift $z_2$. This is operationally similar to integrating a PDE forward in time. An FNO could learn to approximate this evolution operator, mapping $(x_\text{HI}(z_1), \text{density}(z_1), \text{rates}(z_1)) \to x_\text{HI}(z_2)$ at arbitrary resolution.

## Practical Application to 21cm Cosmology: Surrogate Models

### The Emulation Problem

Full [[Radiative Transfer]] simulations cost ~100 GPU-hours per box. This makes parameter exploration expensive: a grid of 10,000 parameter sets would require $10^6$ GPU-hours.

**Semi-numerical codes** like 21cmFAST reduce cost to ~5 minutes per realization, but even 10,000 runs take ~833 hours on a laptop.

### FNO as a Surrogate

An FNO could learn to map:
$$(z, \Omega_m, \sigma_8, \zeta, T_\text{vir}, R_\text{mfp}) \to x_\text{HI}(\mathbf{x}, z)$$

more precisely, after embedding redshift and parameters, the FNO learns:
$$\mathcal{G}: (\delta(\mathbf{x}), \theta) \to x_\text{HI}(\mathbf{x})$$

where $\delta$ is the density field, $\theta$ are parameters, and the output is the full ionization field.

**Cost comparison**:
- Training FNO: 100 simulations × 5 minutes = 500 minutes + 10 GPU-hours for training = negligible
- FNO evaluation: 1 millisecond per prediction (1000 predictions per second on 1 GPU)

**Speed gain**: Instead of 5 minutes to run 21cmFAST, a trained FNO evaluates in 1 millisecond — a factor $\sim 10^5$ speedup.

### Use Case: Parameter Sweep for EFT Training

The [[Effective Field Theory]] framework requires generating a large training set of $(x_\text{HI}, \text{power spectrum, EFT prediction})$ tuples to calibrate the EFT coefficients. Running 21cmFAST for thousands of cosmological parameter sets is expensive. An FNO surrogate would accelerate this dramatically:

1. Generate 100 21cmFAST simulations at selected parameter points
2. Train FNO on these 100 simulations
3. Use FNO to generate 10,000 synthetic simulations by interpolating the FNO across the parameter space (fast)
4. Use these 10,000 samples to train the EFT model (P2)

The approach trades small computational cost (100 reference simulations) for massive speedup (10,000 FNO predictions vs. 10,000 direct simulations).

## FNO vs. Other Emulator Approaches

### Supervised Neural Network Emulators

Codes like **21cmEMU** (Kern et al. 2017) use supervised neural networks to emulate 21cmFAST outputs:
- **Input**: Cosmological parameters $(\Omega_m, \sigma_8, \tau, \ldots)$
- **Output**: A **compressed representation** of the power spectrum or summary statistics (not the full field)

**Advantages**:
- Works with very little training data (50–100 reference simulations)
- Outputs are compressed (power spectrum, a few numbers), easy to work with

**Disadvantages**:
- Doesn't output the full 21cm field
- Lossy compression (squeezes out fine-scale information)
- Unclear what information is being lost (black-box compression)

### FNO as a Full-Field Emulator

FNO goes beyond 21cmEMU by:
- Operating on the **full 21cm field** (all spatial structure preserved)
- Outputting resolution-invariant predictions (same model works for fine and coarse grids)
- Retaining all information for downstream statistical analysis

**Trade-off**: FNO requires training on full fields (higher computational cost) but retains more information.

### Comparison to Other Operators

- **CNN**: Local receptive field; resolution-specific; $\mathcal{O}(N)$ cost per layer but requires many layers for global context
- **ViT**: Global attention; $\mathcal{O}(N^2)$ cost per layer; good for classification but expensive for dense predictions
- **FNO**: Global via Fourier; $\mathcal{O}(N \log N)$ cost per layer; ideal for full-field emulation
- **U-Net**: Hierarchical; $\mathcal{O}(N \log N)$ cost; good for tasks like segmentation where spatial structure matters

For the specific task of field-level emulation, **FNO is fastest** and most elegant because:
1. Physics is naturally spectral (Green's functions)
2. FFT is highly optimized and fast
3. Resolution invariance is built in

## Theoretical Motivation: Universal Approximation

FNOs inherit universal approximation properties from neural networks. Loosely:

> A sufficiently deep and wide FNO can approximate any continuous operator mapping between Hilbert spaces (function spaces with inner products), with arbitrary accuracy.

The depth (number of layers) controls the complexity of the operator. Empirically, FNOs with 4–8 layers suffice for physics applications.

## Current State and Future Directions

### Current Use Cases

FNOs have been successfully applied to:
- **Turbulent flows** (2D/3D Navier-Stokes)
- **Diffusion processes** (heat, smoke)
- **Inverse problems** (tomography, imaging)
- **PDE solvers** (learning surrogates for expensive simulations)

Not yet widely applied to 21cm cosmology, but the physics is conducive (Green's functions, global structure, need for speed).

### Why FNO Hasn't Dominated 21cm Yet

1. **Relative novelty**: FNOs are ~3 years old (as of 2026); many code bases still use older methods
2. **Field-level inference is hard**: Most 21cm inference focuses on power spectrum or summary statistics, not full fields. For summary statistics, simpler methods suffice.
3. **Training data requirements**: FNO requires diverse training simulations across parameter space. Generating 100+ reference simulations is expensive but achievable.

### Future Potential

As the field moves toward **field-level inference** (using all the information in 21cm maps, not just power spectrum), FNOs will become increasingly attractive:
- **Parameter estimation from observed 21cm**: Train FNO emulator, then use it in an [[Simulation-Based Inference]] pipeline to estimate $(\Omega_m, \sigma_8, \ldots)$ from MWA/HERA observations
- **Cross-simulator robustness**: Train FNO on semi-numerical codes, validate on full-RT codes, use for actual inference
- **Accelerated [[Effective Field Theory|EFT]] training**: Use FNO to generate cheap training samples for EFT coefficient calibration

## Connections to This Thesis

While FNOs are not the primary focus of this thesis, they represent a complementary approach to [[Vision Transformer]] and other ML methods:

- **FNO vs. ViT**: FNO is 100–1000× faster for full-field emulation; ViT is more flexible and easier to apply to diverse tasks
- **Use in EFT training**: FNO surrogates could accelerate [[Training Set Generation]] for the EFT model (P2)
- **Resolution invariance**: FNO's built-in invariance to resolution changes is valuable for handling simulators that produce outputs at different resolutions
- **Future direction**: As 21cm inference becomes more field-level and computationally demanding, FNOs will likely become more central to the toolkit

The FNO framework highlights an important principle: **leveraging physics structure (Green's functions, spectral methods) in neural network architecture leads to better generalization and efficiency than purely generic deep learning**.
