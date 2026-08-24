# LearnLog roadmap

Work proceeds in phases. Each phase should land as a reviewable increment with
tests. Do not skip ahead unless a later phase is blocked.

## Phase 1 — Foundation (current)

- Repository layout
- `pyproject.toml`, pytest, Ruff
- README and architecture docs
- Example entry and achievement files
- Example settings

**Not in this phase:** models, CLI, GitHub Actions, website, AI.

## Phase 2 — Domain models

- `Resource`, `LearningEntry`, `Achievement`
- Validation (Pydantic only if it clearly helps)
- Unit tests for required fields, visibility, multi-resource entries

## Phase 3 — Storage layer

- Load/save Markdown entries with YAML frontmatter
- Load/save achievement YAML
- Slug generation and `data/entries/YYYY/MM/DD/` paths

## Phase 4 — Markdown generation

- `LearningEntry` → Markdown with valid frontmatter
- Structured body sections matching `examples/learning-entry.md`

## Phase 5 — Local processing

- Accept structured input
- Validate, generate, and write an entry to the date-based path

## Phase 6 — Statistics and indexing

- Topic, skill, and provider indexes
- Learning and achievement counts
- Generated JSON under `data/generated/`

## Phase 7 — CLI

- `learnlog add`, `list`, `search`, `stats`
- `learnlog achievement add`
- CLI calls services only; no domain logic in the CLI module

## Phase 8 — GitHub integration

- Issue form → Actions → processor → Markdown commit
- Mark issues processed
- Workflows such as `process-learning.yml`, `generate-indexes.yml`, `validate.yml`

## Phase 9 — Public portfolio

- Filter `visibility == public`
- Static site (GitHub Pages, MkDocs Material, Astro, or similar)
- Timeline, topics, skills, achievements, badges, stats, search

## Phase 10 — Optional AI

- User-configurable providers (OpenAI, Anthropic, Gemini, Ollama, …)
- Summaries, flashcards, quizzes, gap analysis, next-step suggestions
- Product remains useful with AI disabled
