---
type: concept
title: "FiLM Conditioning"
created: 2026-05-11
updated: 2026-05-11
tags:
  - concept/ml
  - concept/architecture
  - domain/inference
status: seed
complexity: intermediate
domain: "[[Inference and ML]]"
aliases:
  - "FiLM"
  - "Feature-wise Linear Modulation"
  - "Feature-wise Linear Modulation (FiLM)"
related:
  - "[[Fourier Neural Operator]]"
  - "[[FNO Approach for 21cm Emulation]]"
  - "[[Training Set Generation]]"
sources: []
---

# FiLM Conditioning

**FiLM** (Feature-wise Linear Modulation) is a lightweight mechanism for injecting global conditioning information — here, cosmological / astrophysical / EFT parameters $\theta$ — into a neural network that processes a spatial field. It applies a per-channel affine transformation whose scale and shift are themselves produced by a small MLP from $\theta$.

In this thesis, FiLM is the candidate conditioning mechanism for the FNO/U-NO surrogate of $T_b$ and $x_\text{HI}$ described in [[FNO Approach for 21cm Emulation]] (Strategy B).

## The Affine Transformation

### Tensor shapes

Inside an FNO/U-NO block, after the lift, activations live in

$$h \in \mathbb{R}^{B \times C \times N_x \times N_y \times N_z}$$

for a 3D reionization box (batch $B$, $C$ lifted channels, spatial grid $N_x N_y N_z$). The conditioning vector

$$\theta \in \mathbb{R}^{B \times P}$$

is one $P$-dimensional parameter vector per sample, with $P$ being the number of parameters being conditioned on — e.g. $(\Omega_m, \sigma_8, h, n_s, \zeta, T_\text{vir}, R_\text{mfp}, b_1, b_2, b_{\nabla^2}, z)$.

A small MLP $g_\ell$ (one per block $\ell$) maps $\theta \mapsto (\gamma_\ell, \beta_\ell)$, each of shape $\mathbb{R}^{B \times C}$. **No spatial axes** — that's the whole trick.

### The FiLM operation

Writing $i$ for batch, $c$ for channel, and $x$ for the multi-index of spatial position:

$$\big(\text{FiLM}_\theta(h)\big)_{i,c,x} \;=\; \gamma_{\ell,\,i,c}(\theta_i)\cdot h_{i,c,x} \;+\; \beta_{\ell,\,i,c}(\theta_i)$$

Two things to internalize from this:

1. $\gamma$ and $\beta$ depend on $\theta_i$ (sample-specific) and on the channel $c$.
2. They are **constant in $x$** — every voxel of channel $c$ in sample $i$ gets the same scale and shift.

In code it is literally a broadcast:

```python
gamma, beta = mlp(theta).chunk(2, dim=-1)        # (B, C)
gamma = gamma.view(B, C, 1, 1, 1) + 1.0           # identity-init trick
beta  = beta.view(B, C, 1, 1, 1)
h = gamma * h + beta
```

### "Affine" only along the channel axis

Flattening the spatial axes to a length-$M = N_x N_y N_z$ vector per channel, the operation reads

$$\underbrace{h}_{C \times M} \;\mapsto\; \underbrace{\text{diag}(\gamma)}_{C \times C} \cdot h \;+\; \beta\,\mathbf{1}_M^\top.$$

So FiLM is the cheapest possible per-channel affine: a diagonal linear map plus a rank-1 bias. No mixing between channels (that is what the FNO's $W$ and $R$ already do) and no spatial structure (that is what the FFT and the 1×1 conv do). FiLM is doing one thing: re-weighting the relative importance of channels and shifting their baseline as a function of $\theta$.

### Why this beats the alternatives

A fully affine layer that conditioned each voxel separately would have $\gamma, \beta \in \mathbb{R}^{C \times N_x \times N_y \times N_z}$ — impractical, and would bake the resolution into the conditioning, **killing FNO's discretization-invariance**.

A purely scalar modulation $\gamma(\theta) \in \mathbb{R}$ would scale the whole tensor uniformly — too blunt, since different channels in the FNO carry different physical content (large-scale modes, small-scale features, etc.).

Channel-wise affine is the sweet spot.

## Placement Inside an FNO/U-NO Block

The standard placement is *after* the spectral+skip sum and *before* the nonlinearity:

$$h_{\ell+1} \;=\; \sigma\Big(\text{FiLM}_\theta\big(W_\ell h_\ell + \mathcal{F}^{-1}(R_\ell \cdot \mathcal{F}(h_\ell))\big)\Big)$$

That gives the conditioning a chance to gate or amplify particular channels of the mixed spatial+spectral representation before the activation squashes them. Each block gets its own FiLM head (its own MLP outputs), so the network can re-condition at each scale.

### Variants worth knowing

| Variant | Where modulation acts | Cost | Notes |
|--------|----------------------|------|-------|
| **Channel-wise FiLM** (standard) | $\gamma_c(\theta), \beta_c(\theta)$ on spatial features | low | Default. Per-block conditioning. |
| **Pre-lift FiLM only** | Once on lifted features at input | very low | Too weak for strong parameter dependence (e.g. $\zeta$, $T_\text{vir}$ in reionization). |
| **Spectral FiLM** | $R_\theta = R \odot \gamma(\theta)$ in Fourier space | medium | Lets $\theta$ reweight modes per $k$. More expressive, less stable. |
| **AdaGN** | FiLM fused with GroupNorm | low | Drop-in if the block already uses GroupNorm. |
| **Hypernetwork over $R$** | MLP emits the spectral weights directly | high | Most expressive, most params, hardest to train. Treat as v3. |

The escalation path for this thesis: **channel-wise FiLM → spectral FiLM → hypernetwork**, escalating only when the previous tier saturates.

## The Conditioning MLP

For a block with $C$ channels and a parameter vector of dimension $P$:

$$\theta \;\xrightarrow{P \to H}\; \cdot \;\xrightarrow{\text{SiLU}}\; \cdot \;\xrightarrow{H \to H}\; \cdot \;\xrightarrow{\text{SiLU}}\; \cdot \;\xrightarrow{H \to 2C}\; (\gamma^{\text{raw}}, \beta^{\text{raw}})$$

with $H \sim 128\text{–}256$. Then operationally

$$\gamma = 1 + \gamma^{\text{raw}}, \qquad \beta = \beta^{\text{raw}},$$

with the **final linear layer zero-initialized**. The block is then exactly an unmodulated FNO block at init, and the MLP only starts deviating from "identity FiLM" as gradient signal accumulates. This is the same identity-init trick that stabilizes diffusion U-Nets and ControlNets, and matters here for the same reason — without it, FiLM perturbations at initialization throw off the residual structure of the FNO.

### Sharing across blocks

You can share the MLP *trunk* across all blocks and give each block its own small head (cuts parameter count, often helps generalization), or give every block its own MLP. Both work; the shared-trunk version is the standard recipe.

### Input preparation

- **Standardize $\theta$** to roughly $\mathcal{N}(0,1)$ over the training prior. Reionization parameters span very different magnitudes — $\zeta \sim 10$s, $T_\text{vir} \sim 10^4$ K, EFT bias coefficients $\mathcal{O}(1)$ — so without rescaling the MLP wastes capacity learning units.
- **Categorical / non-Gaussian inputs** (e.g. a discrete scenario flag): embed separately, then concatenate with continuous parameters before the MLP.
- **Redshift** goes through the *same* FiLM channel — don't build a parallel mechanism for it; it is just one more entry in $\theta$. This is also what enables a single trained model to predict at multiple redshifts.

## Fourier-Space Interpretation

Because FiLM is applied after the $W_\ell h_\ell + \mathcal{F}^{-1}(R_\ell \cdot \mathcal{F}(h_\ell))$ sum, in Fourier space its action on channel $c$ is

$$\widetilde{h}_c(\mathbf{k}) \;\mapsto\; \gamma_c(\theta)\cdot\widetilde{h}_c(\mathbf{k}) \;+\; \beta_c(\theta)\cdot\delta(\mathbf{k}).$$

So:

- $\gamma_c(\theta)$ is a **wavenumber-independent gain** — it rescales *every* mode of channel $c$ by the same factor.
- $\beta_c(\theta)$ adds a **DC offset** to that channel.

FiLM by itself **cannot reshape the spectral profile** of a channel — that is $R_\ell$'s job. What it *can* do is, conditional on parameters, change which channels dominate; and through subsequent FNO blocks (where channels get mixed and re-Fourier'd) those parameter-dependent channel weightings translate into parameter-dependent power-spectrum responses. This is exactly the kind of "amplitude knob per scale" behaviour that maps cleanly onto how astro parameters such as $\zeta$ and $T_\text{vir}$ shift the 21cm power spectrum.

The moment you want $\theta$ to **directly reshape the spectral profile** (e.g. $R_\text{mfp}$ shifting characteristic bubble scales), graduate to **spectral FiLM** or a **hypernetwork over $R$**.

## Why FiLM Is the Right Default for Parameter-Conditioned Field Emulation

| Alternative | Issue |
|-------------|-------|
| Concatenating $\theta$ as constant input channels | Wastes capacity — every Fourier layer has to relearn that those channels are spatially constant; no natural per-layer conditioning. |
| Pure hypernetwork over $R$ | More expressive but many more weights, higher variance, careful regularization needed. |
| Per-voxel affine | Breaks resolution invariance. |
| Scalar modulation | Too coarse — cannot select channels. |

FiLM gives ~95% of the benefit of a hypernetwork at a small fraction of the cost. It is the standard choice for parameter-conditioned PDE-style emulators in the recent literature, and it is the natural fit for the cosmological/EFT-parameter inputs needed for [[FNO Approach for 21cm Emulation]].

## Application to This Thesis

The intended architecture for both emulation tasks in [[FNO Approach for 21cm Emulation]] is:

> Input: initial linear density box (1 channel) → lift to $C$ channels → $N$ FNO/U-NO blocks, each with channel-wise FiLM driven by $\theta = (\Omega_m, \sigma_8, h, n_s, \zeta, T_\text{vir}, R_\text{mfp}, b_1, b_2, b_{\nabla^2}, \ldots, z)$ → project to output ($T_b$ for Task 1, $x_\text{HI}$ for Task 2).

Conditioning on $z$ via FiLM avoids training a separate model per redshift and is compatible with U-NO's native 3D spatiotemporal mode.

### Pitfall: degeneracy masking

EFT bias coefficients are degenerate with each other and with simulation parameters in ways that depend on the field statistics. If FiLM is too expressive, the network may memorize through it and mask physical degeneracies. Diagnostic once training is stable: check whether $\gamma, \beta$ vary smoothly with $\theta$ (good) or pathologically (bad — overfitting the prior). This matters specifically for Task 2, where extracting EFT coefficients from FNO output is the validation step.

## Open Questions

- Does channel-wise FiLM saturate before reaching the EFT-comparison goal of Task 2? If yes, the escalation is to spectral FiLM (parameter-dependent $R_\ell$) so $\theta$ can reweight modes at specific $k$.
- Should EFT bias coefficients $(b_1, b_2, b_{\nabla^2})$ be among the FiLM inputs (i.e. condition the FNO on bias) or held out as targets to be recovered post-hoc from FNO output? The latter is needed for the EFT–FNO consistency check; the former might make training easier but blurs the test.
- Does identity-init FiLM still help if the underlying FNO uses GroupNorm? (If yes, prefer AdaGN over a separate FiLM layer.)
