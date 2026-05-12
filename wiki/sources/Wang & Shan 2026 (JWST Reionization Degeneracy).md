---
type: source
title: "Wang & Shan 2026 — The JWST early galaxy crisis resolved by a reionization degeneracy"
created: 2026-05-12
updated: 2026-05-12
tags:
  - source/paper
  - domain/reionization
  - degeneracy
  - jwst
status: seed
source_type: paper
author:
  - "Wang, Zihan"
  - "Shan, Huanyuan"
date_published: 2026
url: "https://arxiv.org/abs/2605.03635"
confidence: medium
key_claims:
  - "Global reionization observables constrain only the product f_esc * f_star,0, not the two parameters individually — a structural degeneracy in the reionization equations"
  - "The JWST z>10 'bright galaxy crisis' and the long-standing factor-of-four spread in f_esc estimates are two faces of the same degeneracy"
  - "Using the shape of the JWST UV luminosity function as an independent constraint on f_star,0 breaks the degeneracy and yields robust bounds on f_esc"
  - "The proposed JWST crisis threshold is excluded at 4.5 sigma; stochastic star formation histories strengthen rather than weaken standard reionization models"
related:
  - "[[Reionization Physics]]"
  - "[[Choudhury 2022 (Reionization Intro)]]"
  - "[[Ferrara & Pandolfi (IGM Reionization)]]"
---

# Wang & Shan 2026 — The JWST early galaxy crisis resolved by a reionization degeneracy

> [!key-insight]
> Global reionization observables (Thomson optical depth $\tau$, redshift of half-ionization, neutral-fraction evolution) depend on the product $f_\text{esc} \times f_{\star,0}$ rather than each factor separately. JWST's UV luminosity-function *shape* breaks the degeneracy by independently constraining $f_{\star,0}$, and once it's broken the proposed "z > 10 too-bright crisis" disappears (excluded at 4.5$\sigma$).

## Citation

Wang, Z., & Shan, H. (2026). "The JWST early galaxy crisis resolved by a reionization degeneracy." arXiv:2605.03635.

## Core Claim

The standard global reionization model writes the ionizing-photon production rate as
$$
\dot n_\text{ion}(z) \;\propto\; f_\text{esc} \cdot f_{\star,0} \cdot \rho_\text{UV}(z),
$$
with the UV LF integral standing in for $\rho_\text{UV}$. Two consequences follow:

1. **The product is constrained, the factors aren't.** $\tau$, the midpoint of reionization, and the late-time global $\bar x_\text{HII}(z)$ all fix the *product* $f_\text{esc} \cdot f_{\star,0}$. Individually, $f_\text{esc}$ and $f_{\star,0}$ can roam over more than a factor of four without breaking the global fit. This explains why the literature on $f_\text{esc}(z>6)$ has spanned a factor of ~4 for over a decade.

2. **The JWST "crisis" is the same degeneracy.** Claims that the JWST z>10 UV LF requires $f_{\star,0}$ above $\Lambda$CDM thresholds were drawn from the *normalization* of the high-z LF. The *shape* of the LF, however, fixes $f_{\star,0}$ independently. Once you use shape as well as normalization, the standard model fits without crisis: the "crisis threshold" is excluded at 4.5$\sigma$ in a joint profile-likelihood analysis. Stochastic star-formation histories strengthen this conclusion rather than rescuing the crisis claim.

## Why It Matters for This Thesis

Two reasons to file this, neither of them about EFT or simulators directly:

1. **What 21 cm alone can constrain**. The thesis pipeline ultimately wants to constrain astrophysical parameters from 21 cm data. This paper makes explicit that global / large-scale observables alone do not pin down $f_\text{esc}$ and $f_{\star,0}$ separately — a structural degeneracy from the equations, not a measurement-precision issue. The 21 cm power spectrum at high z carries some morphological information that the global signal does not, but for the part of parameter space the thesis will explore it's worth flagging that *all* of P2's posterior intervals on $f_\text{esc}, f_{\star,0}$ are likely to come out elongated along the same product direction unless one of the two is fixed by an external prior. Adding a UV LF shape prior to the inference is a clean way to break it.

2. **Prior on $f_{\star,0}$.** If a UV-LF-shape prior is available (the paper provides one), P2 can plug it in as an external Gaussian prior on $f_{\star,0}$ and read off $f_\text{esc}$ from the EFT-coefficient posterior plus that prior. Worth keeping in the back pocket for the P2 inference design.

## Connections

- Sits alongside [[Choudhury 2022 (Reionization Intro)]] — Choudhury's pedagogical treatment of the global reionization equation makes the degeneracy obvious in retrospect; this paper is the empirical follow-through with JWST data.
- Not relevant to EFT coefficient extraction itself, but relevant to *what astrophysics the EFT coefficients ultimately map to*.

## Open Questions

> [!gap]
> Is the $f_\text{esc} \cdot f_{\star,0}$ degeneracy actually broken by the 21 cm *power spectrum* (as opposed to the global signal)? Different combinations of the two factors that match the same product can still produce different bubble morphologies and patchiness. If so, then 21 cm imaging adds a fundamentally new direction — worth checking explicitly in P2's information-content analysis.

## Citation Stub

```
Wang, Z., Shan, H. "The JWST early galaxy crisis resolved by a reionization degeneracy." arXiv:2605.03635 (2026).
```
