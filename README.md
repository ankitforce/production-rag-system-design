# Production RAG System Design Kit

A practical companion repo for the Substack essay ["RAG Is Not a Feature. It Is an Evidence Supply Chain"](https://ankitkumar3514.substack.com/p/rag-is-not-a-feature-it-is-an-evidence).

This is not a mirror of the blog. It is a reusable architecture kit for engineers, technical product leaders, and agentic coding/research tools that need to design, review, or evaluate production Retrieval-Augmented Generation systems.

![Production RAG reference architecture](diagrams/rag-reference-architecture.png)

## What This Repo Contains

- Reference architecture diagrams for offline indexing, online serving, evaluation, policy, tenancy, and freshness.
- A long-form system design guide and a deeper technical paper.
- Production checklists for readiness, security, and evaluation release gates.
- JSON schemas and examples for chunk metadata and RAG traces.
- Architecture and evaluation templates that teams can copy into design docs.
- Agent instructions and task cards so AI agents can navigate the repo and produce useful outputs.

## Start Here

| Goal | Use |
|---|---|
| Understand the architecture | [`docs/system-design-guide.md`](docs/system-design-guide.md) |
| Go deeper technically | [`docs/technical-paper.md`](docs/technical-paper.md) |
| Review a system before launch | [`checklists/production-readiness.md`](checklists/production-readiness.md) |
| Review authorization and isolation | [`checklists/security-review.md`](checklists/security-review.md) |
| Define eval gates | [`checklists/eval-release-gates.md`](checklists/eval-release-gates.md) |
| Start an architecture review | [`templates/architecture-review-template.md`](templates/architecture-review-template.md) |
| Ask an agent to use the repo | [`AGENTS.md`](AGENTS.md) and [`agent/tasks.md`](agent/tasks.md) |

## Core Principle

Production RAG is an evidence supply chain:

1. Parse documents into structure-preserving representations.
2. Chunk by document structure with recursive fallbacks.
3. Store lineage, metadata, ACLs, versions, and freshness state.
4. Retrieve with hybrid dense and sparse search.
5. Fuse and rerank a broad candidate pool.
6. Assemble source-labeled, policy-compliant context.
7. Generate with citation and abstention constraints.
8. Verify faithfulness and citation support.
9. Trace every stage.
10. Continuously evaluate with golden, synthetic, adversarial, and production-derived cases.

## Agent-Friendly Use

This repo is designed so an agent can do more than summarize it. Agents should:

- Read [`AGENTS.md`](AGENTS.md) first.
- Load [`agent/manifest.json`](agent/manifest.json) to discover canonical files and allowed task types.
- Use the checklists and schemas as operating constraints.
- Produce outputs in `outputs/` when run locally.
- Avoid changing source docs unless explicitly asked.

Suggested agent prompts:

```text
Use this repo to review my RAG architecture. Start from AGENTS.md, then fill out templates/architecture-review-template.md using my design notes.
```

```text
Use this repo to create an eval plan for an enterprise RAG assistant. Follow agent/tasks.md and use schemas/rag-trace.schema.json.
```

## Repository Boundaries

Included:

- Public-facing docs, diagrams, checklists, templates, schemas, and a reproducible diagram script.

Excluded:

- Substack cookies, `.env` files, draft IDs, local browser automation, raw working transcripts, and private publishing scripts.

## Regenerate Diagrams

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 scripts/generate_rag_images.py
```

## License

Unless otherwise noted:

- Written content and diagrams are licensed under Creative Commons Attribution 4.0 International.
- Code is licensed under MIT.

See [`LICENSE.md`](LICENSE.md).
