# Agent Instructions

These instructions apply to the whole repository.

## Purpose

This repo is a production RAG system design kit. Use it to help humans design, review, evaluate, and harden Retrieval-Augmented Generation systems. Do not treat it as a generic AI article archive.

## Read Order

Agents should read these files first:

1. `agent/manifest.json`
2. `README.md`
3. The task-specific file in `agent/tasks.md`
4. The relevant checklist or template
5. `docs/system-design-guide.md` only when deeper context is needed

Use `docs/technical-paper.md` when the task asks for deeper technical comparisons, taxonomy, metrics, or implementation tradeoffs.

## What Agents Can Do

Agents may:

- Fill out architecture reviews using `templates/architecture-review-template.md`.
- Create eval plans using `templates/eval-plan-template.md`.
- Score a proposed system against `checklists/production-readiness.md`.
- Score authorization, tenancy, and prompt-injection risks using `checklists/security-review.md`.
- Draft chunk metadata or trace examples using the JSON schemas.
- Generate diagrams by running `scripts/generate_rag_images.py`.
- Write outputs under an `outputs/` folder.

Agents must not:

- Invent claims that are not supported by the docs or sources.
- Treat this kit as production code.
- Add secrets, cookies, API keys, private URLs, subscriber data, or draft IDs.
- Publish, sync, or update Substack content.
- Copy private working transcripts into public docs.
- Change license terms without explicit human instruction.

## Output Style

Prefer actionable artifacts over summaries:

- Architecture review
- Risk register
- Eval plan
- Launch checklist
- Metadata schema recommendation
- Trace logging recommendation
- Build-order recommendation

When making recommendations, separate:

- `Finding`
- `Why it matters`
- `Evidence from this repo`
- `Suggested action`
- `Confidence`

## Invariants

- Authorization belongs before retrieval.
- Unauthorized chunks must not enter candidate pools, prompts, caches, or evaluator traces.
- Retrieval quality and answer faithfulness should be measured separately.
- Reranking improves precision but adds latency and cost.
- Large context windows do not remove the need for retrieval and ranking.
- Advanced architectures should be added only when a measured failure mode demands them.
