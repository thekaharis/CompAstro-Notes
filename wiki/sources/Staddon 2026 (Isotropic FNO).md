---
type: source
title: "Staddon 2026 — Isotropic Fourier Neural Operators"
created: 2026-05-12
updated: 2026-05-12
tags:
  - source/paper
  - domain/inference
  - domain/ml
  - domain/operator-learning
  - symmetry
status: seed
source_type: paper
author:
  - "Staddon, Michael F."
date_published: 2026
url: "https://arxiv.org/abs/2605.02597"
confidence: medium
key_claims:
  - "Standard FNOs do not respect rotational symmetry of isotropic physical systems; the learned spectral kernel can be direction-dependent"
  - "Constraining the spectral kernel R(k) to depend only on |k| yields a rotationally equivariant operator at no loss in expressivity for isotropic forward problems"
  - "Parameter count drops by up to 16x in 2D and 96x in 3D vs the standard FNO at matched or improved accuracy"
  - "Equivariance acts as free data augmentation; sample efficiency improves correspondingly"
related:
  - "[[Fourier Neural Operator]]"
  - "[[FNO Approach for 21cm Emulation]]"
  - "[[Duruisseaux et al 2026 (FNO)]]"
  - "[[Rahman et al 2023 (U-NO)]]"
  - "[[Redshift Space Distortions]]"
---

# Staddon 2026 — Isotropic Fourier Neural Operators

> [!key-insight]
> Standard FNOs learn a spectral kernel $R(\mathbf{k})$ that can carry directional dependence the underlying physics doesn't have. Constraining $R(\mathbf{k}) = R(|\mathbf{k}|)$ gives a rotationally **equivariant** operator and a ~16x (2D) / ~96x (3D) cut in parameter count, with matched or better accuracy on isotropic forward problems. The constraint is on the operator class, not on the data — anisotropic inputs still produce anisotropic outputs.

## Citation

Staddon, M. F. (2026). "Isotropic Fourier Neural Operators." arXiv:2605.02597.

## Core Claim

Most physical systems whose forward map an FNO is being trained to emulate are rotationally symmetric — the operator $\mathcal{G}: u \mapsto v$ commutes with rotations of the input field. A vanilla FNO does not enforce this: the spectral filter $R_\ell(\mathbf{k})$ has independent parameters at each Fourier mode $\mathbf{k}$, so the network is free to learn a kernel that prefers directions the physics does not.

Staddon proposes parameterizing $R_\ell$ as a function of the radial wavenumber only:
$$
R_\ell(\mathbf{k}) \;=\; R_\ell(|\mathbf{k}|),
$$
implemented by binning Fourier modes by $|\mathbf{k}|$ and sharing parameters within each bin. Because Fourier multiplication is pointwise, $R_\ell(|\mathbf{k}|)$ commutes with rotations applied to the input — the resulting operator is exactly $SO(d)$-equivariant.

## Reported Numbers

- **2D**: ~16x reduction in spectral-layer parameters at matched accuracy.
- **3D**: ~96x reduction (gain scales with the surface area / shell volume ratio).
- **Sample efficiency**: training converges with materially less data, consistent with equivariance acting as built-in rotational data augmentation.
- **Accuracy**: equal to or better than the unconstrained FNO baseline on the isotropic-PDE benchmarks reported in the paper.

## Equivariance vs Invariance — Why This Doesn't Break for Anisotropic Observables

A natural objection for 21 cm work: the **observed** 21 cm field is anisotropic (RSD, light-cone evolution, foreground wedge), so why impose isotropy?

The constraint is on the **operator**, not on the **output field**.

- $R_\ell(|\mathbf{k}|)$ acts multiplicatively in Fourier space. An anisotropic input produces an anisotropic output; the operator just does not itself prefer a direction.
- The symmetry being imposed is **rotational equivariance**: rotate the input field, the output field rotates the same way. This is the correct symmetry of the *physical* forward map, even when observation breaks isotropy downstream.
- Anisotropies enter the data either through symmetry-breaking inputs (peculiar velocity field, line-of-sight unit vector) or through downstream operations (light-coning, RSD, beam convolution, foreground filtering). These belong **outside** the isotropic FNO core.

For a 21 cm forward chain the right factorization is:

1. Isotropic FNO core: $(\delta_m(\mathbf{x}), \theta) \to (x_\text{HI}(\mathbf{x}), T_b^\text{real}(\mathbf{x}))$ in comoving real space at fixed $z$.
2. Explicit symmetry-breaking layers downstream: RSD using $\mathbf{v}_\text{pec}$, light-cone interpolation along the LOS, beam / wedge / instrument response.

Anisotropies show up at the right point in the pipeline without being baked into the part of the network that does not need them.

## Failure Mode to Track

If the isotropic FNO is asked to predict the *observed* (post-RSD, post-instrument) field end-to-end without being given the LOS as an explicit input, the rotational-equivariance constraint will actively hurt: the $\mu^2$ Kaiser term and any other direction-dependent feature will be averaged away. Equivariant architectures only handle the redshift-space map cleanly when the symmetry-breaking vector (LOS, beam axis) is passed in as a network input.

## Connection to Thesis

### Direct Relevance to [[FNO Approach for 21cm Emulation]]

The planning note's Task 1 (brightness temperature surrogate $\mathcal{G}_1$) and Task 2 (neutral fraction operator $\mathcal{G}_2$ with EFT connection) both live at the comoving real-space level — exactly the regime where the isotropic constraint is correct. Adopting an isotropic FNO would:

1. **Cut parameters by ~10–100x**, directly reducing the training-set generation burden (the 21cmFAST simulation cost is the practical bottleneck).
2. **Improve sample efficiency** via implicit rotational augmentation, which matters when training cubes are individually expensive.
3. **Sharpen the EFT bridge**: EFT is built on respecting the underlying symmetries of the physics and isolating symmetry-breaking through explicit operators (velocity field, LOS, bias coefficients). Putting the same symmetry logic in the surrogate keeps the two halves of the thesis ideologically consistent.

### Escalation Path Update

The planning note currently mentions "channel-wise FiLM → spectral FiLM → hypernetwork" for parameter conditioning. Add: "vanilla FNO → isotropic FNO → equivariant FNO" as the symmetry-axis escalation, with the isotropic variant as the natural first step for the comoving forward map.

### What Stays Vanilla

The downstream layers — RSD, light-cone, beam, foreground wedge — must remain direction-aware. An isotropic FNO is the wrong tool for the observed power spectrum $P(k_\parallel, k_\perp)$. The architecture is well-matched to the simulator-surrogate role, not the full observation operator.

## Open Questions

> [!gap]
> Does the parameter saving translate cleanly to U-NO ([[Rahman et al 2023 (U-NO)]])? The U-NO encoder bottleneck mixes spatial coordinates non-trivially via skip connections — verify whether the radial-binning trick survives the U-shape.

> [!gap]
> What is the right way to pass the LOS unit vector into an equivariant FNO so that the redshift-space map is representable? A separate (non-isotropic) head fed by the velocity field is the obvious answer; the experiment to confirm is not in this paper.

> [!gap]
> Statistical isotropy of the 21 cm field on large scales is broken weakly by the light-cone effect (signal evolves along LOS at fixed observer frequency). Is the equivariance violation small enough at the comoving level that the isotropic FNO is still appropriate within a single coeval cube, even if not across a lightcone? Almost certainly yes within one cube, but worth a sanity check.

## Citation Stub

```
Staddon, M. F. "Isotropic Fourier Neural Operators." arXiv:2605.02597 (2026).
```
