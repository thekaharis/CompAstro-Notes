---
type: source
title: "Lu, Jin & Karniadakis 2020 — DeepONet: Learning Nonlinear Operators"
created: 2026-04-28
updated: 2026-04-28
tags:
  - source/paper
  - domain/inference
  - domain/ml
  - domain/operator-learning
status: ingested
source_type: paper
author:
  - "Lu Lu"
  - "Pengzhan Jin"
  - "[[Karniadakis, George Em]]"
date_published: 2020
url: "https://arxiv.org/abs/1910.03193"
arxiv: "1910.03193"
pdf: ".raw/articles/1910.03193v3 - Lu et al 2020 (DeepONet).pdf"
confidence: high
key_claims:
  - "A neural network with a single hidden layer can approximate any nonlinear continuous operator — the universal approximation theorem for operators (Chen & Chen 1995)"
  - "DeepONet's branch-trunk architecture directly implements this theorem, encoding the input function at fixed sensors (branch) and the output query locations (trunk)"
  - "DeepONet reduces generalization error significantly compared to plain FNNs for operator learning"
  - "High-order convergence observed: polynomial rates (½ to 4th order) and even exponential convergence with training set size"
  - "Number of sensors required for ODE operators scales as O(m^{-2l^2}) for GRF input functions with length scale l"
related:
  - "[[Fourier Neural Operator]]"
  - "[[Inference and ML]]"
  - "[[Rahman et al 2023 (U-NO)]]"
  - "[[Duruisseaux et al 2026 (FNO)]]"
---

# Lu, Jin & Karniadakis 2020 — DeepONet

> [!key-insight]
> DeepONet implements the universal approximation theorem for operators via a branch-trunk architecture: the **branch net** encodes the input function at fixed sensor locations, the **trunk net** encodes the query location, and their inner product yields the output. Achieves rapid convergence vs. training set size for ODE and PDE operators.

## Citation

Lu, L., Jin, P., & Karniadakis, G. E. (2020). "DeepONet: Learning nonlinear operators for identifying differential equations based on the universal approximation theorem of operators." arXiv:1910.03193.

## Context in the Neural Operator Landscape

DeepONet is the **first practical realisation** of the theoretical result that neural networks are universal approximators of operators, not just functions. It predates the [[Fourier Neural Operator]] (Li et al. 2020) and takes a complementary approach: rather than operating in Fourier space, DeepONet learns the operator via an inner product between two sub-networks. [[Rahman et al 2023 (U-NO)]] and FNO both cite DeepONet as foundational motivation.

## Core Architecture

### The Problem Setup

An operator $G: u \mapsto G(u)$ maps an input function $u$ defined over domain $\mathcal{X}$ to an output function $G(u)$ over domain $\mathcal{Y}$.

Both input and output are infinite-dimensional, but in practice the input is discretized at $m$ fixed **sensor points** $\{x_1, \ldots, x_m\}$, so the input to the network is the vector $[u(x_1), \ldots, u(x_m)]^T$.

The output $G(u)(y)$ is evaluated at arbitrary query locations $y \in \mathcal{Y}$ (not on a grid).

### Branch-Trunk Decomposition

From the theorem (Chen & Chen 1995), any operator $G$ can be approximated as:

$$G(u)(y) \approx \sum_{k=1}^p b_k(u) \cdot t_k(y)$$

where $b_k$ are scalar functions of the input function and $t_k$ are basis functions of the output location. DeepONet implements this directly:

- **Branch net**: takes $[u(x_1), \ldots, u(x_m)]^T \in \mathbb{R}^m$ and outputs $[b_1, \ldots, b_p]^T \in \mathbb{R}^p$
- **Trunk net**: takes $y \in \mathbb{R}^d$ and outputs $[t_1, \ldots, t_p]^T \in \mathbb{R}^p$
- **Output**: $G(u)(y) \approx \sum_k b_k t_k + b_0$ (inner product plus bias)

Two variants:
- **Stacked DeepONet**: $p$ separate branch networks, each outputting a scalar — faithful to the theorem but expensive
- **Unstacked DeepONet**: a single branch network outputs all $p$ values simultaneously — equally expressive, much more efficient

Both use simple FNNs as sub-networks; the architecture is agnostic to the inner network type (could be CNN or attention).

### Key Advantage: Arbitrary Output Locations

Unlike CNNs or FNOs, the output of DeepONet is queried at **arbitrary points** $y$ — the trunk net is continuous. This means:
- No requirement for the output to live on a grid
- Can evaluate at scattered points, along curves, or at user-specified locations
- Naturally handles irregular observational geometries (e.g., telescope pointing patterns)

## Theory: Universal Approximation for Operators

**Theorem (Chen & Chen 1995, Theorem 1 in paper)**:

For any continuous nonlinear operator $G: V \to C(K_2)$ where $V$ is compact in $C(K_1)$, and any $\varepsilon > 0$, there exist constants and network parameters such that the inner product sum above approximates $G(u)(y)$ to within $\varepsilon$ uniformly over $u \in V$ and $y \in K_2$.

This is the operator analogue of the universal approximation theorem for functions — it guarantees that DeepONet is expressive enough in principle. The paper then provides practical bounds on how the **generalization error** and **sensor count** scale with the problem.

### Number of Sensors

For ODE operators with GRF input (RBF kernel, length scale $l$):

$$\text{Sensors required: } m \sim l^{-2} \cdot \varepsilon^{-1/2}$$

Smooth inputs (large $l$) require fewer sensors; rough inputs require more. This matches the intuition that the sensor resolution needs to resolve the input function's characteristic scale.

## Experiments and Results

### Operators Tested

| Problem | Operator | Input Space | Key Result |
|---------|----------|-------------|------------|
| ODE: simple system | $u \to s(T)$ (solution at time $T$) | GRF | 4th-order convergence vs. training set |
| ODE: Lorenz-like | $u \to s(t)$ | GRF | Exponential convergence |
| PDE: diffusion-reaction | $u \to s(x, T)$ | Chebyshev polynomials | Low error at 1000 training pairs |
| PDE: Burgers | $u(x,0) \to u(x, T)$ | GRF | $<1\%$ relative $L^2$ error |

### Error Convergence

The paper shows **polynomial-to-exponential convergence** of the relative $L^2$ error as training set size increases — rates from $N^{-1/2}$ to $N^{-4}$ and even $\exp(-cN)$ for smooth operators.

This empirical convergence is much faster than naive function approximation, validating the hypothesis that the inductive bias of the branch-trunk architecture matches the structure of operator learning.

## Comparison to FNO

| Aspect | DeepONet | FNO |
|--------|----------|-----|
| Discretization requirement | Input at **fixed** sensor points; output at arbitrary query points | Input/output on same grid (resolution-invariant across grids, but grid-based) |
| Physics inductive bias | General operators; no spectral assumption | Spectral structure (Fourier convolution); ideal for PDEs with Green's functions |
| Memory scaling | $O(m \cdot p)$ (sensors × basis functions) | $O(N \log N)$ (FFT) |
| Irregular geometries | Natural (trunk net evaluates anywhere) | Requires interpolation to/from a grid |
| 3D extensions | Straightforward (trunk net takes 3D $y$) | Memory-intensive (FFT on 3D grids) |

For 21cm cosmology on regular simulation grids, FNO is typically more efficient. For irregular observational data (e.g., HERA pointing patterns), DeepONet's arbitrary-output capability could be advantageous.

## Relevance to This Thesis

### Potential Role in P1/P2

DeepONet's branch-trunk structure has a natural reading in the EFT context:

- **Branch net** $\equiv$ encodes the matter density field $\delta_m(\mathbf{x})$ evaluated at sensor points
- **Trunk net** $\equiv$ encodes the query location (either spatial position or Fourier wavenumber $k$)
- **Output** $\equiv$ the EFT prediction: $\delta_x(y)$ or the power spectrum $P_{x,\text{EFT}}(k)$

This is speculative, but DeepONet could serve as an alternative architecture to FNO for mapping $\delta_m \to x_\text{HII}$ in an emulator context, with the advantage of evaluating predictions at arbitrary $k$ without resampling.

### Comparison to the FNO Approach (Planning Note)

See [[FNO Approach for 21cm Emulation]] for the operational FNO plan. DeepONet is noted there as an alternative architecture if FNO's grid-based structure proves limiting.

## Open Questions

> [!gap]
> Has DeepONet been tested on cosmological fields (21cm brightness temperature, matter density, ionization fraction)? The irregular-output capability would be valuable for evaluating on observational $uv$-plane coverage.

> [!gap]
> Can the branch-trunk decomposition be interpreted as a physical basis expansion? If so, are the basis functions $t_k(y)$ analogous to EFT bias operators evaluated at wavenumber $k$?

> [!gap]
> How does DeepONet compare to FNO on a specific task: mapping $\delta_m(\mathbf{x}) \to x_\text{HII}(\mathbf{x})$ for 21cmFAST outputs? No published benchmark appears to exist.
