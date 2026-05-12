---
type: source
title: "Byrne, D'Addario, Jacobs & Hallinan 2026 — Systematic Spectral Distortion from Digital Whitening in Radio Telescopes"
created: 2026-05-12
updated: 2026-05-12
tags:
  - source/paper
  - domain/21cm
  - instrumentation
  - systematics
status: seed
source_type: paper
author:
  - "Byrne, Ruby"
  - "D'Addario, Larry R."
  - "Jacobs, Daniel C."
  - "Hallinan, Gregg"
date_published: 2026
url: "https://arxiv.org/abs/2605.05489"
confidence: medium
key_claims:
  - "Digital whitening followed by re-quantization in wide-bandwidth radio telescopes induces a systematic, subtle distortion of the gain-vs-frequency function"
  - "The distortion produces measurable systematic error in the measured spectra, with direct implications for 21 cm cosmology experiments"
  - "Mitigation requires careful accounting in the signal-processing pipeline; the distortion is not removed by standard bandpass calibration"
related:
  - "[[21cm Cosmology]]"
  - "[[HERA]]"
  - "[[SKA]]"
  - "[[MWA]]"
  - "[[Foreground Wedge]]"
---

# Byrne, D'Addario, Jacobs & Hallinan 2026 — Systematic Spectral Distortion from Digital Whitening

> [!key-insight]
> Digital whitening + re-quantization — a standard combination in modern wide-bandwidth interferometer signal chains — induces a subtle gain-vs-frequency distortion that is not removed by ordinary bandpass calibration. The effect is small but systematic, and shows up in measured spectra at a level that matters for 21 cm power-spectrum experiments.

## Citation

Byrne, R., D'Addario, L. R., Jacobs, D. C., & Hallinan, G. (2026). "Systematic Spectral Distortion from Digital Whitening in Radio Telescopes and Implications for 21 cm Cosmology." arXiv:2605.05489.

## Core Claim

Wide-bandwidth telescopes (HERA, MWA, SKA) often have large variation of signal power across frequency. To represent the channelized signal in a small number of bits for downstream processing, modern signal chains apply a "whitening" filter that flattens the spectrum, then re-quantize. The combination of flattening plus re-quantization induces a subtle, frequency-dependent distortion of the measured gain. Standard bandpass calibration does not remove it, because the distortion depends on the input signal statistics rather than being a static instrumental gain.

## Why It Matters for This Thesis

This is an instrumentation paper, not directly relevant to EFT or simulator dependence. It is filed because:

1. **Forecast realism**. Any P2 forecast that uses HERA/SKA noise models needs to account for systematic floors of this kind in addition to thermal noise and foregrounds. If a digital-whitening systematic propagates into the EoR window at a level comparable to the EFT bias-coefficient signal, it sets a floor on the achievable inference precision.

2. **Foreground wedge interaction**. Systematic spectral distortions can leak power from the foreground-dominated regions into the EoR window, effectively widening the wedge. Worth referencing when designing the observational layer of the P2 forward model.

3. **Not urgent**. The thesis is primarily theoretical / methodological; the practical effect on EFT-coefficient inference depends on whether HERA / SKA pipelines mitigate the effect in standard data products. Park this paper as a "check before publishing forecasts" item rather than a critical-path read.

## Connections

- Sits alongside the foreground-wedge literature (see [[Foreground Wedge]] concept).
- Relevant only at the observational-layer end of the forward chain in [[FNO Approach for 21cm Emulation]].

## Citation Stub

```
Byrne, R., D'Addario, L. R., Jacobs, D. C., Hallinan, G. "Systematic Spectral Distortion from Digital Whitening in Radio Telescopes and Implications for 21 cm Cosmology." arXiv:2605.05489 (2026).
```
