# Haris' Thesis Wiki — LLM Wiki

Mode: E (Research)
Purpose: Persistent, compounding knowledge base for a Master's thesis on EFT-based simulator-robust 21 cm reionization inference.
Owner: Haris
Created: 2026-04-14

## Structure

```
Uni/Thesis/
├── .raw/              # Source documents — never modify
│   ├── articles/
│   ├── transcripts/
│   ├── screenshots/
│   ├── data/
│   └── assets/
├── wiki/
│   ├── index.md           # Master catalog of all pages
│   ├── log.md             # Append-only operation log
│   ├── hot.md             # ~500-word recent context cache
│   ├── overview.md        # Executive summary of entire wiki
│   ├── papers/            # One summary per paper (key claims, methodology)
│   ├── sources/           # General source summaries
│   ├── concepts/          # Ideas, models, mathematical objects
│   ├── entities/          # People, codes, datasets, telescopes
│   ├── domains/           # Top-level topic areas
│   ├── thesis/            # Evolving synthesis and working notes
│   ├── gaps/              # Open questions and contradictions
│   ├── comparisons/       # Side-by-side analyses
│   ├── questions/         # Filed answers to queries
│   └── meta/              # Dashboards, lint reports
├── _templates/
├── _attachments/
└── WIKI.md                # Full schema reference
```

## Conventions

- All notes use YAML frontmatter: type, status, created, updated, tags (minimum)
- Wikilinks use [[Note Name]] format — filenames are unique, no paths needed
- .raw/ contains source documents — never modify them
- wiki/index.md is the master catalog — update on every ingest
- wiki/log.md is append-only — new entries go at the TOP, never edit past entries
- Atomic notes: one concept per page; if it covers two things, split it

## Operations

- Ingest: drop source in .raw/, say "ingest [filename]"
- Query: ask any question — read hot.md first, then index.md, then drill in
- Lint: say "lint the wiki" to run a health check
- Scaffold: already done — structure is live

## Domain Overview

| Domain | Folder | Description |
|--------|--------|-------------|
| 21cm Cosmology | domains/21cm Cosmology.md | Signal physics, brightness temperature, HERA/SKA |
| Reionization Physics | domains/Reionization Physics.md | EoR history, bubble morphology, neutral fraction |
| Effective Field Theory | domains/Effective Field Theory.md | Bias expansion, perturbation theory, EFT operators |
| Simulation & Codes | domains/Simulation and Codes.md | 21cmFAST, SCRIPT, THESAN, radiative transfer |
| Inference & ML | domains/Inference and ML.md | SBI, neural networks, emulators, parameter estimation |
| Thesis Work | domains/Thesis Work.md | Research log, methodology, timeline, deliverables |
