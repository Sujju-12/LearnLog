# LearnLog

**Git-native Personal Learning Diary and Learning Portfolio.**

LearnLog helps you capture what you learn from courses, docs, labs, AI chats,
and projects — then keep that knowledge as plain Markdown in Git. Use it as a
private diary. Publish selected entries and credentials as a public portfolio
when you are ready.

The same repository layout is meant to be **forked or copied** so other people
can run their own learning OS with zero infrastructure cost.

## Why LearnLog

Learning is scattered across IBM, OpenAI, Anthropic, AWS, Azure, Google Cloud,
YouTube, Udemy, Coursera, GitHub, books, blogs, and labs. LearnLog is the place
those sessions become:

1. What you learned  
2. When you learned it  
3. Topics and skills  
4. Multiple resources in one session  
5. Your own understanding  
6. Key concepts  
7. Hands-on work  
8. Questions and gaps  
9. Next steps  
10. Achievements, badges, and certificates  
11. Public or private visibility  

Data stays **yours**: Git + Markdown + YAML. No database and no SaaS required.

## Core features (product)

| Area | Intent |
| --- | --- |
| Learning entries | Markdown files with YAML frontmatter |
| Multi-source sessions | Many resources per entry |
| Achievements | YAML records for certs and badges |
| Visibility | `private` / `public` on every record |
| Local processing | Validate → model → files → Git |
| Future CLI | Add, list, search, stats |
| Future GitHub flow | Issue form → Actions → committed entry |
| Future site | Static portfolio from public records only |
| Optional AI | Later, and always off by default |

**Phase 1** ships the repository, packaging, and documentation. Runtime models
and commands start in Phase 2.

## Zero-cost philosophy

The MVP runs with:

- Python 3.11+
- Git
- A text editor (or a future CLI)

It does **not** require paid APIs, a hosted database, or a cloud backend.
GitHub’s free tier is enough for optional CI later. AI providers (OpenAI,
Anthropic, Gemini, Ollama, and others) are optional in Phase 10.

## Architecture overview

```
USER  →  GitHub Form / CLI / future UI
      →  validation  →  domain model
      →  Markdown/YAML  →  Git repository
      →  generated indexes
      →  private diary  +  public static portfolio
```

Domain code must not depend on GitHub. Adapters stay at the edges. See
[docs/architecture.md](docs/architecture.md) and
[docs/data-model.md](docs/data-model.md).

## Repository structure

```
learnlog/
├── .github/                 # Issue templates and workflows (later)
├── config/                  # Example settings
├── data/
│   ├── entries/             # YYYY/MM/DD/*.md
│   ├── achievements/        # <slug>.yaml
│   ├── resources/           # Optional shared resources
│   └── generated/           # Derived JSON (do not edit)
├── docs/                    # Architecture, data model, roadmap
├── examples/                # Sample entry and achievement
├── src/learnlog/            # Python package (src layout)
├── templates/               # Markdown templates (later)
├── tests/
├── Makefile
├── pyproject.toml
└── README.md
```

## Installation

Requires **Python 3.11 or newer**.

```bash
git clone https://github.com/Sujju-12/LearnLog.git
cd LearnLog
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

Copy [config/settings.example.yaml](config/settings.example.yaml) when you
start customizing paths. Default layout matches this repository.

## Development

```bash
make install   # editable install + pytest + ruff
make test      # pytest
make lint      # ruff check
make format    # ruff format + auto-fix
make check     # lint then test
```

Equivalent without Make:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check src tests
python -m ruff format src tests
```

## Roadmap

1. **Foundation** — this repository  
2. **Domain models** — Resource, LearningEntry, Achievement  
3. **Storage** — load/save Markdown and YAML  
4. **Markdown generation** — frontmatter + sections  
5. **Local processing** — validate and write dated paths  
6. **Indexes and stats** — generated JSON  
7. **CLI** — add / list / search / stats  
8. **GitHub** — issue form and Actions  
9. **Public portfolio** — static site from public records  
10. **Optional AI** — summaries, flashcards, quizzes  

Details: [docs/roadmap.md](docs/roadmap.md).

## Future vision

LearnLog should become a reusable **personal learning operating system**: a
private Git diary, a public evidence-based portfolio, and automation that
turns a learning session into a structured, searchable record — without locking
anyone into a vendor database.

## License

[MIT](LICENSE)
