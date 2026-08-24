# LearnLog roadmap

Work proceeds in phases. Each phase should land as a reviewable increment with
tests. Do not skip ahead unless a later phase is blocked.

## Phase 1 — Foundation

Complete.

## Phase 2 — Domain models

Complete. Pydantic models with open-string providers.

## Phase 3 — Storage layer

Complete. `data/entries/YYYY/MM/DD/<slug>.md`

## Phase 4 — Markdown generation

Complete.

## Phase 5 — Local processing

Complete. `learnlog add`

## Phase 6 — Statistics and indexing

Complete. `learnlog stats` and `data/generated/index.json`

## Phase 7 — CLI

Complete. `add`, `list`, `search`, `show`, `stats`, `achievement add|list`

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
