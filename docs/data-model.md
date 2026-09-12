# LearnLog data model

## Conventions

- Identifiers are stable, URL-safe slugs (often date-prefixed for entries).
- Dates use ISO-8601 calendar dates (`YYYY-MM-DD`) unless a later phase needs
  timestamps.
- `visibility` is `private` or `public`. Unknown values fail validation.
- Lists are unordered unless a later UX needs ordering; processors should
  preserve author order.
- Providers and resource types are **open strings** with documented examples.
  New providers must not require a code change.

## Resource

A resource is one source used during learning. A single `LearningEntry` may
include many resources.

| Field | Required | Notes |
| --- | --- | --- |
| `provider` | yes | e.g. IBM, OpenAI, Anthropic, AWS, Azure, Google Cloud, YouTube, GitHub, Udemy, Coursera, Personal, Other |
| `type` | yes | e.g. documentation, article, video, course, book, ai_conversation, github_repository, hands_on_lab, blog, project |
| `title` | yes | Human-readable source title |
| `url` | no | Empty string allowed when the source has no URL |
| `notes` | no | Why this source mattered |
| `author` | no | When applicable |
| `accessed_date` | no | When the learner used the source |

Reusable global resources may later live at `data/resources/<resource-slug>.yaml`.
Until then, resources are embedded on the learning entry.

## LearningEntry

Primary unit of captured learning. Stored as Markdown with YAML frontmatter.

### Required

| Field | Notes |
| --- | --- |
| `id` | Unique, e.g. `2026-08-24-kubernetes-services` |
| `title` | Short title |
| `date` | Learning date |
| `visibility` | `private` or `public` |
| `summary` | Short description of what was learned (frontmatter). Longer narrative lives in the Markdown body. |

### Optional

| Field | Notes |
| --- | --- |
| `topics` | Coarse subjects (`kubernetes`, `networking`) |
| `skills` | Concrete skills (`clusterip`, `nodeport`) |
| `learning_type` | How learning happened (`documentation`, `hands-on`, `ai-assisted`) |
| `status` | Capture lifecycle (`captured`, `reviewed`, …) — keep a small enum in Phase 2 |
| `resources` | List of `Resource` |
| `key_concepts` | May also appear as Markdown sections |
| `understanding` | Learner’s own explanation |
| `hands_on_work` | Labs, commands, experiments |
| `knowledge_gaps` | Open questions |
| `next_steps` | Follow-up learning |
| `tags` | Free-form labels |
| `related_projects` | Slugs or names |
| `related_achievements` | Achievement ids |

### Storage path

```
data/entries/YYYY/MM/DD/<slug>.md
```

Example: `data/entries/2026/08/24/kubernetes-services.md`

Frontmatter holds structured metadata. The Markdown body holds human-readable
sections (what was learned, understanding, hands-on work, gaps, next steps).
The generator’s section headings match `examples/learning-entry.md`.

## Achievement

Certifications, badges, and other credentials. Stored as YAML:

```
data/achievements/<achievement-slug>.yaml
```

| Field | Required | Notes |
| --- | --- | --- |
| `id` | yes | Slug, e.g. `aws-certified-cloud-practitioner` |
| `title` | yes | Display name |
| `provider` | yes | Issuer |
| `date_earned` | yes | ISO date |
| `visibility` | yes | `private` or `public` |
| `credential_url` | no | Verify link |
| `skills` | no | Skills demonstrated |
| `related_topics` | no | Topics |
| `badge_image` | no | Path or URL |
| `certificate_file` | no | Path in-repo or URL |
| `status` | no | e.g. `earned`, `in_progress`, `expired` |
| `notes` | no | Context |

## Generated data

Indexes and statistics (topic pages, provider counts, public timelines) will be
written under `data/generated/` as JSON. Those files are derived; they are not
the source of truth.

## Publishing filter

Public portfolio (Phase 9) includes records where `visibility == public`.
Private records remain in Git for the owner and are excluded from the site.
Changing visibility must not require renaming files.

## Assumptions

- `summary` in frontmatter is the required short description; body sections hold
  the narrative.
- Resource `provider` / `type` are unconstrained strings with examples, not a
  closed enum in code.
- Entry `id` is `{date}-{slug}`; the filename slug omits the date because the
  path already has `YYYY/MM/DD`.
