---
type: meta
title: "Hot Cache"
updated: 2026-06-20T00:00:00
---

# Recent Context

## Last Updated

2026-06-20 — Consolidated the mode-cutoff findings and filed the [[Siren3D Residual Refinement Plan]].

## Key Recent Facts

- [[FNO Lightcone Experimental Findings]] now contains seven acts. Parameter conditioning was necessary; U-FNO + SyncBN was the architectural breakthrough, reaching val L² = 0.0418 and val H¹ = 8.27.
- The U-FNO floor survived asymmetric LOS modes ($m_z:16\to32$), GroupNorm, stronger H¹ weighting, and a doubled LOS U-Net receptive field. These interventions converged to the same or slightly worse held-out floor.
- [[Spectral Mode Cutoff in FNOs]] records the key interpretation: `n_modes` truncates only learned global spectral communication. It is not a hard output band-limit because pointwise, nonlinear, and U-Net paths can generate full-resolution structure.
- On the anisotropic lightcone, 16 modes correspond nominally to very different physical edges: about $0.50\ \mathrm{Mpc}^{-1}$ transversely and $0.030\ \mathrm{Mpc}^{-1}$ along the LOS. The evolving LOS is not a stationary periodic axis, so this is not a clean cosmological $k_{\max}$.
- [[Siren3D Residual Refinement Plan]] proposes a frozen-U-FNO, coordinate-conditioned sinusoidal logit-residual head. It targets boundary detail while preserving U-FNO's global context and must beat parameter-matched ReLU, Fourier-feature, and convolutional controls.

## Active Threads

- Run the global-pooling residual first; it tests missing cone-level context and is orthogonal to the failed mode/LOS experiments.
- Quantify error versus distance to ionization boundaries before committing compute to Siren3D.
- A Siren3D win must lower held-out H¹ without degrading L², $P(k)$, $r(k)$, or global ionization history.
- P1 remains focused on renormalized EFT coefficient extraction and cross-simulator validity.
