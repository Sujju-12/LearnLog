# LearnLog architecture

LearnLog is a **Git-native personal learning operating system**. Users own their
data as Markdown and YAML in a Git repository. Processing is local Python. No
database, cloud backend, or paid API is required for the core product.

## Design principle

Learning data stays portable. The repository is the source of truth:

| Kind | Format | Location |
| --- | --- | --- |
| Learning entries | Markdown + YAML frontmatter | `data/entries/YYYY/MM/DD/` |
| Achievements | YAML | `data/achievements/` |
| Shared resources (later) | YAML | `data/resources/` |
| Indexes and stats | Generated JSON | `data/generated/` |
| User settings | YAML | `config/` |

JSON is reserved for generated indexes. Users should not edit files under
`data/generated/`.

## High-level flow

```
USER
  |
  +-- GitHub Form (Phase 8)
  +-- CLI (Phase 7)
  +-- Future Web UI (later)
  |
  v
RAW LEARNING INPUT
  |
  v
VALIDATION LAYER
  |
  v
LEARNING DOMAIN MODEL
  |
  v
MARKDOWN / YAML GENERATION
  |
  v
GIT REPOSITORY
  |
  v
GENERATED KNOWLEDGE
  |
  +-- PRIVATE LEARNING (full diary)
  +-- PUBLIC PORTFOLIO (visibility == public)
  |
  v
STATIC WEBSITE (Phase 9, not in this phase)
```

Input adapters (CLI, GitHub Actions, UI) must stay thin. Domain models and
services must not import GitHub-specific APIs.

## Package layout

```
src/learnlog/
  models/      Domain types (Phase 2)
  services/    Load, save, generate, index (Phases 3–6)
  utils/       Slugs, dates, paths
```

Tests live under `tests/` and should exercise the core without network access.

## Public vs private

Every learning entry and achievement carries `visibility: private | public`.

A later publishing pipeline will:

1. Read entries and achievements from the Git tree.
2. Keep private records in the personal repository (or omit them from the site).
3. Emit a static site from public records only (GitHub Pages, MkDocs Material,
   Astro, or similar).

The storage layout is stable enough that the site generator can consume files
without rewriting the domain model.

## Zero-cost MVP

- Python 3.11+
- Git + Markdown + YAML
- GitHub free tier for optional automation later
- Optional AI (OpenAI, Anthropic, Gemini, Ollama) is Phase 10 and must remain
  off by default

## Out of scope for Phase 1

Phase 1 ships structure, packaging, and documentation only. Models, storage,
CLI, GitHub Actions, the website, and AI are later phases.
