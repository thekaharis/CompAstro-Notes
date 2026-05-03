---
type: source
title: "Deistler et al. 2025 — Simulation-Based Inference: A Practical Guide"
created: 2026-04-20
updated: 2026-04-20
tags:
  - source/paper
  - domain/inference
  - domain/sbi
  - methods
status: mature
source_type: paper
author:
  - "Deistler, Michael"
  - "Boelts, Jan"
  - "Steinbach, Peter"
  - "Moss, Guy"
  - "Moreau, Thomas"
  - "Gloeckler, Manuel"
  - "Rodrigues, Pedro L. C."
  - "Linhart, Julia"
  - "Lappalainen, Janne K."
  - "Miller, Benjamin Kurt"
  - "Gonçalves, Pedro J."
  - "Lueckmann, Jan-Matthis"
  - "Schröder, Cornelius"
  - "Macke, Jakob H."
date_published: 2025
url: "https://arxiv.org/abs/2508.12939"
confidence: high
key_claims:
  - "SBI enables posterior inference from stochastic simulators without likelihood evaluations via neural networks trained on (θ, x) pairs"
  - "Four major SBI algorithms: NPE (Neural Posterior Estimation), NLE (Likelihood Estimation), NRE (Ratio Estimation), and sequential variants"
  - "Amortized inference: once trained, the network performs inference on any new observation without retraining"
  - "Workflow stages: simulator setup → prior → data representation → inference algorithm → diagnostics → scientific analysis"
  - "Key diagnostics: posterior predictive checks, expected coverage, simulation-based calibration (SBC)"
related:
  - "[[Simulation-Based Inference]]"
  - "[[Neural Posterior Estimation]]"
  - "[[Inference and ML]]"
  - "[[Pietschke et al 2025 (EoRFlow)]]"
  - "[[Training Set Generation]]"
---

# Deistler et al. 2025 — SBI: A Practical Guide

> [!key-insight]
> A comprehensive tutorial on simulation-based inference (SBI) by the core developers of the `sbi` Python package (Macke lab, Tübingen). Covers the full workflow from simulator setup to posterior validation. Highly practical for P2 implementation — this is the canonical methods reference for applying NPE/NLE/NRE to reionization inference.

## Citation

Deistler, M., Boelts, J., et al. (2025). "Simulation-Based Inference: A Practical Guide." arXiv:2508.12939 [stat.ML].

## What This Paper Is

A 40-page tutorial/guide, not a primary research paper. It is the companion document to the [`sbi` Python package](https://github.com/sbi-dev/sbi), written by its lead developers at the University of Tübingen and Max Planck Institute. It covers SBI theory, workflow, algorithms, and practical guidance with examples from astrophysics, neuroscience, and psychophysics.

## Core SBI Framework

### The Problem

Given a stochastic simulator $x \sim p(x|\theta)$ and observed data $x_o$, recover the posterior $p(\theta | x_o)$. Classical Bayesian methods (MCMC) require evaluating $p(x|\theta)$ — often intractable for complex simulators. SBI learns this from simulations.

### Neural SBI Approach

1. **Simulate**: draw $(\theta_i, x_i) \sim p(\theta) \cdot p(x|\theta)$ for $N$ samples
2. **Train**: fit an inference network $q_\phi(\theta|x)$ on these pairs
3. **Infer**: evaluate $q_\phi(\theta|x_o)$ at observation — gives posterior approximation without any additional simulations

The training loss for NPE is:
$$\mathcal{L}(\phi) = \mathbb{E}_{(\theta,x)\sim p(\theta,x)}[-\log q_\phi(\theta|x)]$$

### Amortization

Once trained, the network can perform inference on **any** $x_o$ without new simulations. Critical for reionization inference where a single training run covers the full parameter space and is then applied to many observations.

## Four SBI Algorithms

| Algorithm | What it learns | Pros | Cons |
|---|---|---|---|
| **NPE** (Neural Posterior Estimation) | $q_\phi(\theta\|x) \approx p(\theta\|x)$ | Direct posterior; amortized | Requires many simulations up front |
| **NLE** (Neural Likelihood Estimation) | $q_\phi(x\|\theta) \approx p(x\|\theta)$ | More flexible; can use MCMC after | Not directly amortized; MCMC at test time |
| **NRE** (Neural Ratio Estimation) | $\log p(\theta\|x)/p(\theta)$ | Works with weak simulator coupling | Typically sequential (not amortized) |
| **Sequential variants** (SNPE/SNLE/SNRE) | Same as above but iteratively | More simulation-efficient | Breaks amortization; one observation only |

**For P2**: EoRFlow uses NPE (amortized, direct posterior). The `sbi` package provides implementations of all four.

## Data Representation

Three options for representing simulator output:

1. **Raw data**: feed full 3D 21cm field directly to network (very high-dimensional)
2. **Hand-crafted summary statistics**: e.g., power spectrum $P(k,z)$ — reduces dimension but may lose information
3. **Learned embedding networks**: train a neural embedding alongside the inference network — learns optimal compression

**For reionization**: EoRFlow uses 2DPS as summary statistic. SKATR uses a learned ViT embedding. P2 decision: whether EFT coefficients (already compressed, physically motivated) serve as the summary statistic, or whether an embedding network learns to predict EFT coefficients from raw 21cm data.

## SBI Workflow (Section-by-Section)

### 1. Problem Setup
- Define simulator parameters $\theta$ (astrophysical parameters, or EFT coefficients for P2)
- Define prior $p(\theta)$ — range and distribution of parameter values
- Define observable $x$ — what the simulator outputs (21cm map, power spectrum, EFT coefficients)

### 2. Algorithm and Network Choice
- Choice of NPE/NLE/NRE based on simulation budget and amortization need
- Choice of inference network architecture (normalizing flow for NPE is standard)

### 3. Simulation
- Run simulator to generate training set $\{(\theta_i, x_i)\}_{i=1}^N$
- For 21cm: N ~ 10,000–100,000 simulations typically needed for NPE

### 4. Training
- Train inference network on $(θ, x)$ pairs
- Monitor training loss; validate on held-out simulations

### 5. Diagnostics (Critical Section for P2)
- **Posterior predictive checks**: sample $\theta \sim q_\phi(\theta|x_o)$, simulate $x' \sim p(x|\theta)$, check $x' \approx x_o$
- **Expected coverage / TARP**: test whether posteriors are calibrated — e.g., 90% credible intervals should contain the truth 90% of the time
- **Simulation-Based Calibration (SBC)**: generate many $(θ, x)$ pairs, check whether $q_\phi(θ|x)$ is consistent with $p(θ|x)$

### 6. Scientific Analysis
- Interpret posteriors; propagate uncertainty to derived quantities
- For P2: interpret EFT coefficient posteriors → what do they imply about ionization physics?

## Practical Guidance Relevant to Thesis (P2)

### Simulation Budget
- NPE typically needs $N \sim 10^4$–$10^5$ samples for good posterior approximation
- Sequential methods (SNPE) are more sample-efficient but break amortization
- For P2: if simulation budget is limited, consider SNPE for single-observation inference

### Prior Choice
- Prior should cover the physically plausible range of EFT coefficients
- For $b_1^x$: range approximately $[-1, 2]$ (from McQuinn & D'Aloisio 2018 and Qin et al. 2022)
- For $b_{\nabla^2}^x$: negative (smoothing), range approximately $[-10, 0]$ (h/Mpc)²
- For $P_{\varepsilon\varepsilon}$: positive-definite stochastic power

### Cross-Simulator Validation
- The guide emphasizes that if the simulator used for training differs from the data-generating process, posteriors can be miscalibrated
- This is the thesis problem stated in SBI language: P2 addresses cross-simulator calibration via EFT re-targeting

### Normalizing Flows
- NPE uses normalizing flows as the inference network (maps from data to posterior parameters)
- Standard choices: Masked Autoregressive Flows (MAF), Real-NVP, Neural Spline Flows
- `sbi` package handles this automatically; manual implementation not needed

## Connection to Existing Reionization SBI

| Paper | SBI Approach | Summary Statistic | Simulator |
|---|---|---|---|
| [[Pietschke et al 2025 (EoRFlow)]] | NPE (EoRFlow) | 2DPS | 21cmFAST |
| [[Ore et al 2025 (SKATR)]] | NPE + self-supervised embedding | SKATR ViT features | 21cmFAST → cross-sim |
| [[Schosser et al 2025 (Starobinsky)]] | NPE | 2DPS + CMB | 21cmFAST |
| **P2 (Thesis)** | NPE (target: EFT coefficients) | TBD (2DPS or learned) | 21cmFAST + SCRIPT |

## Open Questions

> [!gap]
> **EFT coefficients as summary statistic vs. inference target**: In P2, are EFT coefficients the *target* (the $\theta$ we infer) or the *summary statistic* (a compressed representation of the 21cm field used to infer astrophysical parameters)? The SBI guide clarifies these are distinct roles — P2 may need to decide between them.

> [!gap]
> **Calibration under simulator mismatch**: The guide's diagnostic tools (SBC, TARP) assume training and test simulators are the same. P2's cross-simulator validation requires extended diagnostics — how to quantify calibration when the "test" simulator is different from training?
