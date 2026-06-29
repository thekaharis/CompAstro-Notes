---
type: meta
title: "Hot Cache"
updated: 2026-06-28T00:00:00
---

# Recent Context

## Last Updated

2026-06-28 — Filed [[Windowed Local-FNO U-Net Findings]]: the first Local-FNO run is in, and it's a **negative result** against the design hypothesis. Previously (2026-06-21): filed the [[Windowed Local-FNO U-Net Plan]], [[SirenFNO Spectral Bias Investigation]], and [[Shi et al 2025 (SirenFNO)]].

## Key Recent Facts

- **Local-FNO does not (yet) sharpen bubble walls — it broadens them.** First run [[Windowed Local-FNO U-Net Findings]] (local modes `(6,6,12)`, 21 epochs): boundary-band diagnostic vs the U-FNO benchmark shows the Local-FNO 10–90% front width = **32.2 Mpc** vs U-FNO **10.7 Mpc** (truth 3.6) — ~3× *broader*, plus higher RMSE (0.32 vs 0.28) and gradient error (0.19 vs 0.16) at the wall. Whole-volume (test L² 0.057 / H¹ 10.2) is at the plain-FNO level, short of the U-FNO floor (0.0418 / 8.27). Run is **undertrained/still descending** (caveat), but the front-width gap is too big for that alone. No patch seams.
- **Implication:** windowed-Fourier mixing is still a Fourier basis (Gibbs within each window); the U-FNO's wall sharpness likely comes from its **real-space conv path**, not from locality per se. Both Local-FNO and SirenFNO (the two "remove the global spectral bias" attacks) currently fail to beat the U-FNO floor → next clean test is a local-path/conv hybrid.

- **The spectral bias is now directly measured.** A new per-mode RMS weight diagnostic ([[SirenFNO Spectral Bias Investigation]]) shows the U-FNO learned spectrum **collapses onto low modes within epoch 0**: at 32 LOS modes the lowest 8/32 modes hold 52% of the weight (uniform = 25%), cutoff ratio falls from 1.0 to 0.1–0.45. This is the mechanism behind every mode-count null in [[FNO Lightcone Experimental Findings]].
- **SirenFNO removes the collapse.** Following [[Shi et al 2025 (SirenFNO)]], a 3-D SirenFNO parameterizes the Fourier kernel with a SIREN hypernetwork over all modes; its measured spectrum stays flat (low-quarter pinned at 0.25, cutoff ratio ≈1.0) at every epoch — full-frequency learning confirmed.
- **But it doesn't beat U-FNO yet.** Held-out: SirenFNO (modes 64, 70 ep) test L²=0.050 / H¹=9.82 beats plain FNO (0.057 / 11.64) but trails the U-FNO benchmark (modes 16, 100 ep) at 0.040 / 7.87. SirenFNO has **no local U-Net path**, so this is not yet apples-to-apples.
- [[FNO Lightcone Experimental Findings]] (seven acts): parameter conditioning was necessary; U-FNO + SyncBN reached val L² = 0.0418, H¹ = 8.27; the floor survived more LOS modes, GroupNorm, H¹ reweighting, larger LOS receptive field.
- [[Spectral Mode Cutoff in FNOs]] now carries both the interpretation (`n_modes` truncates only learned global spectral communication, not output bandwidth) and the new measurement of the weight collapse.
- Two distinct SIREN attacks on the boundary problem: **SirenFNO** (replace the kernel) vs **[[Siren3D Residual Refinement Plan]]** (residual head on frozen U-FNO).
- **A third attack is now filed: [[Windowed Local-FNO U-Net Plan]].** Instead of changing *which modes* the kernel represents, it changes *where the transform is applied* — spectral mixing inside small overlapping Hann windows (a low mode in a 16-voxel window = a high effective frequency on the full grid), plus one retained global Fourier bottleneck. ~10.2 M params, original-grid output, same `0.5·L²+0.5·H¹` objective for an architecture-only comparison. This is the "local U-Net path" control implied by the SirenFNO result.

## Active Threads

- **Finish the Local-FNO run** ([[Windowed Local-FNO U-Net Findings]]): carry `lfno-run-6-6-12` from 21 → full 70 epochs (cosine-annealed) and re-run the boundary diagnostic before a final verdict — current numbers are undertrained. Then ablate: widen local modes `(8,8,16)` / smaller window, global-bottleneck on/off, boundary-aware loss, and a Local-FNO + real-space conv-path hybrid.
- Run the boundary-band + $P(k)$/$r(k)$ high-$k$ diagnostic on the existing SirenFNO checkpoint — does the flat spectrum buy bubble-wall fidelity even where whole-volume L² doesn't move?
- Build a **SirenFNO × U-Net hybrid** as the controlled test of "does removing spectral bias help, given the local path?"
- Still pending from the prior thread: the global-pooling residual (missing cone-level context) and the boundary-distance error diagnostic.
- Any SIREN-based win must lower held-out H¹ without degrading L², $P(k)$, $r(k)$, or the global ionization history.
- P1 remains focused on renormalized EFT coefficient extraction and cross-simulator validity.
