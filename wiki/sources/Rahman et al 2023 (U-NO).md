---
type: source
title: "Rahman, Ross & Azizzadenesheli 2023 — U-NO: U-shaped Neural Operators"
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
  - "Md Ashiqur Rahman"
  - "Zachary E. Ross"
  - "Kamyar Azizzadenesheli"
date_published: 2023
url: "https://arxiv.org/abs/2204.11127"
arxiv: "2204.11127"
published_in: "Transactions on Machine Learning Research (TMLR), 04/2023"
pdf: ".raw/articles/2204.11127v3 - Rahman et al 2023 (U-NO).pdf"
confidence: high
key_claims:
  - "U-NO adapts the U-Net encoder-decoder architecture to function spaces (neural operators), enabling deeper and more memory-efficient operator learning than standard FNO"
  - "U-NO achieves 26% improvement over FNO on high-resolution Darcy flow, 44% on Navier-Stokes, and 37% on 3D spatiotemporal operator learning"
  - "Skip connections between encoder and decoder layers allow information bypass, recovering spatial detail lost at the bottleneck"
  - "First neural operator trained for mapping between function spaces with 3D domains — prior 3D work required reducing to 2D or time-discretization-dependent tricks"
  - "Allows 3× deeper, 25× more parameters than FNO with smaller memory footprint, owing to progressive domain contraction in the encoder"
  - "U-NO is robust to hyperparameter choices and faster to train than FNO"
related:
  - "[[Fourier Neural Operator]]"
  - "[[Lu et al 2020 (DeepONet)]]"
  - "[[Duruisseaux et al 2026 (FNO)]]"
  - "[[Inference and ML]]"
---

# Rahman, Ross & Azizzadenesheli 2023 — U-NO: U-shaped Neural Operators

> [!key-insight]
> U-NO extends [[Fourier Neural Operator|FNO]] by wrapping it in a U-Net encoder-decoder structure, progressively contracting the domain (shrinking spatial resolution) in the encoder and expanding it back in the decoder with skip connections. This allows much deeper networks with far more parameters while reducing memory, and yields 26–44% performance gains over FNO on standard PDE benchmarks.

## Citation

Rahman, M. A., Ross, Z. E., & Azizzadenesheli, K. (2023). "U-NO: U-shaped Neural Operators." *Transactions on Machine Learning Research*, 04/2023. arXiv:2204.11127.

## Context in the Neural Operator Landscape

Standard [[Fourier Neural Operator|FNO]] layers preserve the domain and co-domain of the function space throughout all layers — every layer maps functions on domain $D$ to functions on the same domain $D$. This is analogous to a plain ResNet where every layer operates at the same spatial resolution. The consequence is **high memory usage** from the global Fourier integration at each layer, which limits depth.

U-NO solves this by borrowing the U-Net principle: progressively compress the spatial domain (encoder), reach a compact bottleneck, then expand back (decoder), using skip connections to preserve fine-scale information. This is mathematically non-trivial in function spaces (unlike finite-dimensional U-Nets), and the paper provides a rigorous formulation.

## Architecture

### Formal Setup

A neural operator layer computes:
$$G_i v_i(x) = \sigma\!\left(\int \kappa_i(x,y)\, v_i(y)\,d\mu_i(y) + W_i v_i(x)\right)$$

where $\kappa_i$ is an integral kernel (implemented as Fourier spectral multiplication, as in FNO), $W_i$ is a pointwise linear map, and $\sigma$ is a nonlinearity.

### U-NO Encoder

The first $L_1$ layers **contract the domain**:
$$G_i: \{v_i : D_i \to \mathbb{R}^{d_i}\} \to \{v_{i+1} : D_{i+1} \to \mathbb{R}^{d_{i+1}}\}$$

with $\mu(D_i) \geq \mu(D_{i+1})$ (shrinking domain) and $d_{i+1} \geq d_i$ (growing channel dimension). This is exactly the encoder half of a U-Net: spatial compression, channel expansion.

At fixed sampling rate, smaller domains mean **fewer grid points**, so the Fourier integral is computed over a smaller grid — lower memory per layer.

### U-NO Decoder

The next $L_2$ layers **expand the domain back**:

$$G_{L_1 + i}: \{v' : D_{L_1+i} \to \mathbb{R}^{d'}\} \to \{v : D_{L_1+i+1} \to \mathbb{R}^{d''}\}$$

with $\mu(D_{L_1+i+1}) \geq \mu(D_{L_1+i})$ (expanding domain) and decreasing channel dimension. Each decoder layer receives a **skip connection** from the corresponding encoder layer: it concatenates $v_{L_1+i}$ (from decoder) with $v_{L_1-i}$ (from encoder) channel-wise before applying the operator.

### Lifting and Projection

- **Lifting** $P$: pointwise map from input function channels to high-dimensional embedding ($d_0 \gg d_\text{in}$)
- **Projection** $Q$: pointwise map from final embedding back to output channels ($d_\text{out} \ll d_L$)

These are identical to standard FNO.

### Integral Operator Choice

U-NO is architecture-agnostic in its choice of integral operator. In this paper, FNO's Fourier spectral convolution is used within each U-NO layer:
$$\hat{v}_{l+1}(\mathbf{k}) = R_l(\mathbf{k}) \cdot \hat{v}_l(\mathbf{k}) \quad \text{(truncated to } k \leq k_\text{max}\text{)}$$

This means **U-NO strictly generalises FNO**: standard FNO is the special case $L_1 = L_2 = 0$ (no domain contraction or expansion).

## Benchmark Results

### Darcy Flow ($-\nabla \cdot (a \nabla u) = f$ on $[0,1]^2$)

| Model | Relative $L^2$ Error | Notes |
|-------|----------------------|-------|
| FNO | baseline | Standard 4-layer |
| U-NO | **−26%** vs FNO | High-resolution simulation |

U-NO's skip connections preserve fine-scale permeability structure that FNO's flat architecture struggles to reconstruct.

### Navier-Stokes (2D turbulence, $\nu = 10^{-3}$)

| Model | Relative $L^2$ Error |
|-------|----------------------|
| FNO | baseline |
| U-NO | **−44%** (best: −51%) |

At high Reynolds numbers, the flow has sharp gradients. The hierarchical representation in U-NO captures these better than flat FNO.

### Navier-Stokes 3D Spatiotemporal

U-NO is **the first neural operator to natively handle 3D spatiotemporal domains** without reducing to 2D or discretizing time. It achieves:
- **−37%** over FNO on the 3D task
- Training with only a few thousand data points
- Allows 3× deeper models with 25× more parameters vs. FNO, within the same GPU memory budget

Prior 3D FNO work required treating time as a batch dimension (time-discretization dependent) or collapsing the 3D problem to 2D — both of which discard temporal structure.

### Zero-Shot Super-Resolution

Like FNO, U-NO is resolution-invariant and demonstrates zero-shot super-resolution: train on coarse grids, evaluate on fine grids without retraining. U-NO maintains or improves upon FNO's super-resolution performance.

## Why U-NO Matters for 3D Cosmological Fields

21cm simulation boxes are inherently **3D spatial + 1D redshift** — a 4D problem. The standard approach in the literature (EoRFlow, SKATR, most CNN-based work) either:
1. Slices along the line of sight and processes 2D slabs independently
2. Compresses to summary statistics (power spectrum) first

U-NO's native 3D spatiotemporal capability suggests a path to **full 4D operator learning** — mapping the matter density field $\delta_m(\mathbf{x}, z)$ directly to the ionization field $x_\text{HII}(\mathbf{x}, z)$ as a joint spatial-redshift operator. This is architecturally cleaner than processing redshift slices independently and could capture redshift-direction correlations (lightcone effects) that slice-by-slice approaches miss.

## Memory and Efficiency Analysis

### Why Domain Contraction Saves Memory

At the encoder's innermost layer (bottleneck), the function is defined on the smallest domain $D_\text{bottleneck}$. If the original grid is $N^3$ and the bottleneck reduces this by factor $r$ per dimension, the FFT at the bottleneck costs:

$$\mathcal{O}\!\left(\left(\frac{N}{r^{L_1}}\right)^3 \log\!\left(\frac{N}{r^{L_1}}\right)^3\right)$$

versus $\mathcal{O}(N^3 \log N^3)$ for a flat FNO layer at the same resolution. For $L_1 = 3$ encoder layers with $r = 2$, this is $8^3 = 512\times$ cheaper at the bottleneck.

The skip connections add memory for storing intermediate activations, but this is much cheaper than running deep FNO at full resolution.

### Overparameterisation and Generalisation

The paper demonstrates that U-NO's architecture enables **overparameterised** models (25× more parameters than standard FNO) while maintaining or improving generalisation. This is consistent with the double-descent phenomenon in deep learning — larger models generalise better when trained on sufficient data.

For 21cm applications with limited simulation budgets (100–500 reference runs), this suggests U-NO may achieve better accuracy per training sample than FNO.

## Relevance to This Thesis

### FNO Planning Note

See [[FNO Approach for 21cm Emulation]] for the operational plan using neural operators in this thesis. U-NO is the preferred architecture over vanilla FNO for the following reasons:

1. **3D native**: 21cmFAST boxes are $128^3$–$256^3$ voxels; U-NO can operate on these 3D fields without slicing
2. **Memory efficient**: Domain contraction makes deep models feasible on a single GPU
3. **Better accuracy**: 26–44% gains over FNO on comparable physics tasks (fluid PDEs)
4. **Hyperparameter robust**: Easier to tune in practice (important for thesis timeline)

### Connection to EFT

The U-NO encoder-decoder structure has an appealing EFT interpretation:

- **Encoder** (coarse scales): compresses the field to large-scale modes — analogous to the EFT's truncation to $k < k_\text{max}$
- **Bottleneck**: the most compact representation, corresponding to EFT operators (linear, quadratic, derivative)
- **Decoder** (fine scales): reconstructs the field by expanding back, analogous to evaluating the EFT prediction at the original grid resolution

The skip connections parallel the EFT's stochastic term $\varepsilon^x$: they carry fine-scale information that the low-mode bottleneck cannot represent.

This is not a rigorous correspondence, but it provides interpretive framing for understanding what a trained U-NO is doing physically.

## Open Questions

> [!gap]
> **21cm application**: U-NO has been tested on fluid PDEs. Has it been applied to any cosmological field emulation task? If not, the 3D spatiotemporal capability makes it an attractive first application.

> [!gap]
> **Sharp ionization fronts**: Navier-Stokes turbulence has sharp gradients analogous to ionization fronts. The 44% gain over FNO on turbulence suggests U-NO may handle ionization morphology better than FNO — but this needs empirical testing.

> [!gap]
> **Lightcone operator**: Can U-NO learn the full lightcone operator $\delta_m(\mathbf{x}, z) \to T_b(\mathbf{x}, z)$ as a 4D spatiotemporal map? This would be a novel result if demonstrated.

> [!gap]
> **Transfer across simulators**: If U-NO is trained on 21cmFAST outputs, does the encoder bottleneck converge to representations that transfer to BEoRN? The bottleneck's compact representation is reminiscent of EFT coefficient compression — testing this would directly probe the thesis hypothesis.
