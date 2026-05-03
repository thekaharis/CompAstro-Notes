---
type: plan
title: "FNO Approach for 21cm Emulation"
created: 2026-04-28
updated: 2026-04-28
tags:
  - domain/thesis
  - domain/planning
  - domain/ml
  - domain/operator-learning
  - domain/inference
status: draft
related:
  - "[[Fourier Neural Operator]]"
  - "[[Duruisseaux et al 2026 (FNO)]]"
  - "[[Rahman et al 2023 (U-NO)]]"
  - "[[Lu et al 2020 (DeepONet)]]"
  - "[[P1 EFT Characterization]]"
  - "[[P2 Cross-Simulator Inference]]"
  - "[[Inference and ML]]"
  - "[[Effective Field Theory]]"
---

# FNO Approach for 21cm Emulation

> **Purpose:** Detail how Fourier Neural Operators (and their variants — U-NO, DeepONet) can be used to learn two key mappings in this thesis: (1) **brightness temperature from linear density field + cosmological parameters**, and (2) **neutral hydrogen fraction $x_\text{HI}(z)$ from matter density** — and how the second connects naturally to the EFT framework of P1.

This note is forward-looking. It documents a concrete FNO-based approach that could accelerate both P1 (cheap EFT training data) and P2 (fast likelihood emulation), and identifies what would need to be demonstrated for this to count as a novel contribution.

---

## Why Neural Operators for 21cm?

The core bottleneck in both P1 and P2 is **simulation throughput**:

- P1 needs hundreds of 21cmFAST runs at matched ICs to build a reliable EFT training set
- P2 needs thousands of forward-model evaluations inside an SBI posterior loop

Running 21cmFAST at full resolution takes ~5 minutes per box. A trained neural operator emulator evaluates the same mapping in **~1–10 ms** — a speedup of $10^4$–$10^5\times$.

Neural operators are the right tool here because:
1. The map $(\delta_m, \theta) \to x_\text{HII}$ is an **operator** (function-to-function), not a finite-dimensional map
2. 21cmFAST boxes come at various resolutions ($64^3$, $128^3$, $256^3$); FNO/U-NO are **resolution-invariant**
3. The underlying physics is spectral (power spectrum, bias expansion, Green's function structure in density evolution), matching FNO's Fourier inductive bias

Preferred architecture: **U-NO** over vanilla FNO, because:
- 3D native (no slicing needed along the redshift direction)
- 26–44% better accuracy on comparable PDE benchmarks (Darcy, Navier-Stokes)
- Much deeper models fit in GPU memory via encoder domain contraction
- More hyperparameter robust — important for thesis timeline

Fallback: **DeepONet** if irregular observational geometries (interferometric $uv$-plane coverage) need to be handled — its trunk net evaluates at arbitrary output points without interpolation to a grid.

---

## Task 1 — Brightness Temperature from Linear Density + Parameters

### What the Operator Does

$$\mathcal{G}_1: \bigl(\delta_m^\text{lin}(\mathbf{x}, z),\, \theta\bigr) \;\longmapsto\; T_b(\mathbf{x}, z)$$

where:
- $\delta_m^\text{lin}(\mathbf{x}, z)$ is the **linear matter density field** at redshift $z$, drawn from Gaussian initial conditions (cheap to generate with CAMB + 21cmFAST's own IC generator)
- $\theta = (\zeta, T_\text{vir}, R_\text{mfp}, \Omega_m, \sigma_8, \ldots)$ are the cosmological and astrophysical parameters
- $T_b(\mathbf{x}, z)$ is the **21cm brightness temperature field** as produced by 21cmFAST

This is a surrogate for the full 21cmFAST forward model. It takes the cheap linear density as input (bypassing the N-body evolution step) and predicts the full nonlinear brightness temperature field.

### Why Linear Density as Input

Two reasons:

**Computational**: Generating $\delta_m^\text{lin}$ from a power spectrum is essentially free (FFT of Gaussian random field). The expensive parts of 21cmFAST are the Zel'dovich approximation step (density evolution) and the excursion-set ionization solver. The FNO learns to implicitly emulate both steps simultaneously.

**EFT-motivated**: The EFT of the ionization field (P1) is built on the premise that $x_\text{HII}$ is a biased, local functional of the *linear* density $\delta_m^\text{lin}$ — not the fully nonlinear field. If the FNO can learn a good mapping from linear density to $T_b$, it is implicitly learning what the EFT tries to describe analytically. The two approaches are complementary: FNO is a black box, EFT is interpretable.

### Brightness Temperature as a Function of $x_\text{HI}$ and Density

Recall:
$$T_b(\mathbf{x}, z) \approx 27\,x_\text{HI}(\mathbf{x},z)\,(1 + \delta_m(\mathbf{x},z))\left(\frac{1+z}{10}\right)^{1/2} \text{ mK}$$

(in the limit $T_S \gg T_\text{CMB}$, which holds during most of reionization). So $T_b$ is a **product field**: the FNO must implicitly model both $x_\text{HI}$ and the density contrast. It cannot learn $T_b$ without learning something about the ionization morphology.

### Implementation Plan

#### Data Generation

```python
# For each simulation i:
# 1. Draw parameters theta_i ~ prior
# 2. Generate linear density delta_lin(x, z) via 21cmFAST IC generator
# 3. Run 21cmFAST to get T_b(x, z)
# 4. Save pair (delta_lin, theta_i, T_b)
```

**Dataset size**: 200–500 simulation pairs. FNOs typically generalise well from ~200 samples for physics PDEs; cosmological fields may require more due to parameter diversity.

**Redshift snapshots**: Train on 5–10 redshifts spanning $z = 6$–$12$ (the EoR window). Either train a separate FNO per redshift, or treat $z$ as an additional input channel (letting the FNO learn time evolution jointly).

#### Network Architecture (U-NO)

```
Input channels:  delta_lin(x, z)  [1 field]
                 + theta embedded pointwise [d_theta channels]
                 + z embedded pointwise [1 channel]

Lifting P:       MLP(1 + d_theta + 1) → 64 channels

Encoder layers:  3 U-NO layers, domain contracts by 2× per layer
                 Channels: 64 → 128 → 256
                 Spectral modes: 32, 16, 8

Bottleneck:      U-NO layer at 1/8 resolution, 256 channels

Decoder layers:  3 U-NO layers with skip connections from encoder
                 Channels: 256 + 256 → 128 → 64

Projection Q:    MLP(64) → 1 channel

Output:          T_b(x, z)  [1 field, same spatial resolution as input]
```

#### Training

- **Loss**: Relative $L^2$ in real space + optional Fourier-space loss to emphasise low-$k$ accuracy:

$$\mathcal{L} = \frac{\|T_b^\text{pred} - T_b^\text{true}\|_2}{\|T_b^\text{true}\|_2} + \lambda \cdot \frac{\|\hat{T}_b^\text{pred} - \hat{T}_b^\text{true}\|_2}{\|\hat{T}_b^\text{true}\|_2}$$

with $\lambda \sim 0.1$ to balance real-space morphology and spectral accuracy.

- **Optimizer**: Adam, lr $= 10^{-3}$ with cosine annealing
- **Batch size**: 4–8 (limited by GPU memory for $128^3$ boxes)
- **Epochs**: 200–500, early stopping on validation loss

#### Evaluation Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Relative $L^2$ error on $T_b$ | $< 5\%$ | Field-level accuracy |
| Power spectrum ratio $P^\text{FNO}/P^\text{true}$ | $1 \pm 2\%$ for $k < 1\,h$/Mpc | Key for inference |
| Cross-correlation $r(k)$ | $> 0.99$ for $k < 0.5\,h$/Mpc | Field coherence |
| Parameter extrapolation error | $< 10\%$ at $2\sigma$ from training | OOD robustness |

### Connection to P2

A trained $\mathcal{G}_1$ can be used as the **forward model inside the SBI loop** of P2. Instead of calling 21cmFAST at each posterior sample, call the FNO emulator (milliseconds vs. minutes). This enables:
- MCMC chains of $10^6$ samples in reasonable time
- Nested sampling with 500–1000 live points
- Ensemble SBI training with diverse parameter sets

The critical validation: confirm that the SBI posterior using the FNO forward model matches the posterior from direct 21cmFAST runs on a held-out test set.

---

## Task 2 — $x_\text{HI}(z)$ from Matter Density: Connection to EFT

### What the Operator Does

$$\mathcal{G}_2: \bigl(\delta_m(\mathbf{x}, z),\, \theta\bigr) \;\longmapsto\; x_\text{HI}(\mathbf{x}, z)$$

where:
- $\delta_m(\mathbf{x}, z)$ is the matter density field (linear or mildly nonlinear, i.e., Zel'dovich-approximated)
- $x_\text{HI} = 1 - x_\text{HII}$ is the **neutral hydrogen fraction field** (the field directly targeted by the EFT in P1)
- $\theta$ contains astrophysical parameters (primarily $\zeta$, $T_\text{vir}$, $R_\text{mfp}$)

This is the **EFT-relevant mapping**: the EFT of the ionization field posits that $\delta_x = x_\text{HII} - \bar{x}_\text{HII}$ is a local functional of $\delta_m$. Task 2 asks an FNO to learn this functional directly.

### Why This Maps Onto the EFT

The EFT bias expansion is:

$$\delta_x(\mathbf{x}, z) = b_1^x\,\delta_m + \frac{b_2^x}{2}\,[\delta_m^2]_R + b_{\nabla^2}^x\,\nabla^2\delta_m + \varepsilon^x$$

This is a truncated expansion valid at large scales ($k < k_\text{max}^\text{EFT}$). On small scales, the expansion breaks down and the stochastic term $\varepsilon^x$ dominates.

The FNO mapping $\mathcal{G}_2$ learns **the same functional**, but without truncation: it is a full operator from $\delta_m$ to $x_\text{HI}$, implicitly encoding all bias orders and all scale-dependent effects. The relationship between the two approaches is:

$$\underbrace{x_\text{HI}^\text{FNO}(\mathbf{x})}_{\text{full operator}} = \underbrace{(1 - \bar{x}_\text{HII})\left(1 - b_1^x\delta_m - \frac{b_2^x}{2}[\delta_m^2] - \ldots\right)}_{\text{EFT: large-scale, interpretable}} + \underbrace{\varepsilon^x_\text{FNO}(\mathbf{x})}_{\text{FNO residual: small-scale, learned}}$$

The FNO learns a richer map than the EFT, but the EFT extracts the **physically interpretable** part. These are complementary:

| Approach | Large scales | Small scales | Interpretability | Cross-simulator |
|----------|-------------|-------------|-----------------|----------------|
| EFT (P1) | Analytic, bias coefficients | Absorbed into $P_{\varepsilon\varepsilon}$ | High — coefficients have physical meaning | Hypothesis: coefficients match across codes |
| FNO (Task 2) | Learned implicitly | Learned implicitly | Low — black box | Unknown — must test |

### Using FNO to Probe EFT Validity

A trained $\mathcal{G}_2$ can be used to **validate and extend** the EFT analysis of P1:

**Step 1 — Train FNO on 21cmFAST data**: learn $\mathcal{G}_2$ on the same simulation set used for P1 EFT extraction.

**Step 2 — Extract EFT coefficients from FNO predictions**: run the P1 extraction pipeline on the FNO output $x_\text{HI}^\text{FNO}$ instead of the true 21cmFAST output. The resulting coefficients $\{b_1^{x,\text{FNO}}, \ldots\}$ should match the ones extracted from the true simulation.

**Step 3 — Test cross-code transfer**: apply $\mathcal{G}_2$ (trained on 21cmFAST) to BEoRN density fields. Compare:
- FNO's $x_\text{HI}^\text{FNO}$ vs. BEoRN's true $x_\text{HI}^\text{BEoRN}$
- EFT coefficients extracted from each

If the FNO's prediction matches BEoRN better than expected from a naive transfer, it suggests the FNO has learned a **physics-based functional** (independent of code-specific morphology). If it fails, the failure modes will be informative: do the EFT large-scale coefficients still match, even if the small-scale details differ? That would support the EFT approach over the FNO approach for cross-code generalisation.

### Scale Decomposition: Where FNO Agrees with EFT

The EFT is valid at large scales ($k < k_\text{max}^\text{EFT} \sim 0.3$–$0.8\,h$/Mpc). The FNO with spectral truncation at $k_\text{max}^\text{FNO}$ learns the operator over a broad range of scales. We can decompose the FNO output:

$$x_\text{HI}^\text{FNO}(\mathbf{x}) = \underbrace{x_\text{HI}^\text{FNO,large}(\mathbf{x})}_{\text{low-pass filtered, } k < k_\text{EFT}} + \underbrace{x_\text{HI}^\text{FNO,small}(\mathbf{x})}_{\text{high-pass, } k > k_\text{EFT}}$$

**Prediction**: At large scales ($k < k_\text{EFT}$), the FNO and EFT should agree — both are learning the same operator on the same scales. At small scales, only the FNO (or the stochastic EFT term $P_{\varepsilon\varepsilon}$) captures the signal. Verifying this scale decomposition would constitute a **non-trivial consistency check** between the two approaches.

### Implementation Plan

#### Input Encoding

Parameters $\theta$ can be injected via two strategies:

**Strategy A — Concatenation**: embed $\theta$ as a spatially constant field and concatenate with $\delta_m$ as additional input channels. Simple, but the FNO must learn to use the parameter information across layers.

**Strategy B — FiLM conditioning**: use Feature-wise Linear Modulation — at each U-NO layer, the parameter embedding $\theta_\text{embed} = \text{MLP}(\theta)$ modulates the spectral filter:

$$R_l(\mathbf{k}; \theta) = \gamma_l(\theta) \cdot R_l^0(\mathbf{k}) + \beta_l(\theta)$$

This allows parameters to control *how* the operator acts at each scale, rather than simply providing additional input channels. Physically motivated: $\zeta$ and $T_\text{vir}$ control the ionizing efficiency (should modulate large-scale modes), $R_\text{mfp}$ controls bubble sizes (should modulate intermediate-scale modes).

**Recommendation**: start with Strategy A (simpler baseline), then try Strategy B if performance is insufficient.

#### Redshift Evolution

Two options:

**Option A — Single-redshift FNO**: train a separate $\mathcal{G}_2^z$ for each redshift $z$. Simple, but doesn't capture the causal evolution $x_\text{HI}(z)$ depends on the history of ionizing photon production.

**Option B — Temporal FNO**: treat redshift as a pseudo-time axis and train a U-NO on the 4D field $\delta_m(\mathbf{x}, z)$ (3 spatial + 1 redshift). U-NO's 3D spatiotemporal capability (its key novelty) makes this feasible. The output is the full $x_\text{HI}(\mathbf{x}, z)$ lightcone.

**Recommendation**: Option B, using U-NO's 3D spatiotemporal native capability. This is the scientifically richer approach and aligns with the reionization history context of the thesis.

#### Evaluation

Beyond field-level accuracy metrics (same as Task 1), evaluate specifically:

1. **EFT coefficient consistency**: Extract $b_1^x$, $b_2^x$, $b_{\nabla^2}^x$, $P_{\varepsilon\varepsilon}$ from FNO output using the P1 pipeline. Compare to ground-truth (directly extracted from 21cmFAST). This is the key diagnostic for EFT–FNO coherence.

2. **Cross-power spectrum $r_{xm}(k)$**: The cross-correlation between FNO-predicted $x_\text{HII}$ and true $x_\text{HII}$, analogous to P1's diagnostic of EFT validity.

3. **Ionization history $\bar{x}_\text{HI}(z)$**: Globally averaged neutral fraction as a function of redshift. Must be accurate at the percent level for SBI use.

4. **Bubble size distribution**: Morphological check — does the FNO preserve the characteristic bubble size scale that $b_{\nabla^2}^x \approx -R_\text{eff}^2/3$ encodes?

---

## Relation to Existing Work

| Paper | What it does | Gap for thesis |
|-------|-------------|---------------|
| [[Duruisseaux et al 2026 (FNO)]] | Pedagogical FNO guide; Navier-Stokes, Darcy applications | No 21cm application |
| [[Rahman et al 2023 (U-NO)]] | U-NO architecture; 3D spatiotemporal | No cosmological application |
| [[Lu et al 2020 (DeepONet)]] | DeepONet; arbitrary output locations | No cosmological application |
| [[Pietschke et al 2025 (EoRFlow)]] | SBI on 21cm with normalizing flows | Uses power spectrum, not field-level; no FNO |
| [[Ore et al 2025 (SKATR)]] | ViT summary network for 21cm | Cross-simulator tested; no FNO |
| [[Baradaran et al 2024 (Hybrid EFT)]] | N-body + EFT ionization painting | Closest analogue; analytic rather than learned |

**Gap**: No published work uses FNO/U-NO to learn the operator $\delta_m \to x_\text{HI}$ in a 21cm reionization context. This is the novel contribution enabled by this planning note.

---

## Risks and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| FNO fails to capture sharp ionization fronts | Medium | Medium | Use U-NO (better at sharp gradients); increase $k_\text{max}$ |
| Too few training simulations (200 not enough) | Medium | High | Start with 100, validate early; use data augmentation (rotations, reflections) |
| 3D U-NO runs out of GPU memory | Medium | Medium | Start at $64^3$, scale up; use gradient checkpointing |
| FNO cross-code transfer fails | High | Low | Expected — failure modes are still informative for comparing with EFT approach |
| EFT coefficients extracted from FNO output are biased | Low | High | Validate on same simulations used for FNO training first |

---

## Suggested Timeline

| Week | Task |
|------|------|
| 1–2 | Generate 100 21cmFAST training runs; write data pipeline |
| 3–4 | Train Task 1 FNO ($\delta_m^\text{lin} \to T_b$) at $64^3$; validate field-level accuracy |
| 5–6 | Train Task 2 U-NO ($\delta_m \to x_\text{HI}$) at $64^3$; extract EFT coefficients from FNO output |
| 7 | Scale to $128^3$; add FiLM conditioning (Task 2 Strategy B) |
| 8 | Cross-code transfer test: apply 21cmFAST-trained FNO to BEoRN density fields |
| 9 | Integrate Task 1 FNO into P2 SBI loop; compare posteriors vs. direct 21cmFAST |
| 10 | Analysis, write-up |

This is aspirational — the FNO work sits **outside** the core P1+P2 scope and should be pursued only if P1 is on track. The primary deliverable remains the EFT characterisation of P1 and the inference comparison of P2.

---

## Key References

- [[Fourier Neural Operator]] — concept note with FNO architecture details and 21cm relevance
- [[Duruisseaux et al 2026 (FNO)]] — FNO pedagogical guide; architecture equations
- [[Rahman et al 2023 (U-NO)]] — U-NO; 3D native capability; 26–44% gains over FNO
- [[Lu et al 2020 (DeepONet)]] — DeepONet; arbitrary output locations; alternative for irregular geometries
- [[McQuinn & D'Aloisio 2018]] — EFT bias expansion; the analytic counterpart to Task 2
- [[Baradaran et al 2024 (Hybrid EFT)]] — closest existing work (analytic ionization painting)
- [[P1 EFT Characterization]] — supplies the EFT pipeline that Task 2's evaluation calls
- [[P2 Cross-Simulator Inference]] — consumes Task 1's FNO as a fast forward model
