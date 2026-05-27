# Agent Task Cards

Use these task cards to turn the repo into action. Each task should produce a file under `outputs/` unless the human asks for a different destination.

## Task: Architecture Review

Purpose: Review a proposed RAG system design.

Inputs to request from the human:

- Corpus and source systems
- User roles and tenants
- Freshness requirements
- Permission model
- Latency and cost constraints
- Current retrieval and generation architecture
- Known failure modes

Procedure:

1. Read `templates/architecture-review-template.md`.
2. Read `checklists/production-readiness.md`.
3. Read `checklists/security-review.md`.
4. Use `docs/architecture-taxonomy.md` to decide whether the proposed architecture is overbuilt or underbuilt.
5. Produce `outputs/architecture-review.md`.

Output sections:

- Executive summary
- Architecture fit
- Critical gaps
- Security and authorization risks
- Evaluation gaps
- Build-order recommendation
- Launch recommendation

## Task: Production Readiness Score

Purpose: Score whether a RAG system is ready for beta, limited production, or broad launch.

Procedure:

1. Read `checklists/production-readiness.md`.
2. Score each checklist category as `pass`, `partial`, or `missing`.
3. Highlight all launch blockers.
4. Produce `outputs/production-readiness-score.md`.

Scoring rule:

- `Ready for limited beta`: no high-severity security gaps, basic evals exist, traces exist, and citations work.
- `Ready for production`: authorization, eval gates, traces, rollback, deletion proof, and operational budgets all pass.
- `Not ready`: any cross-tenant risk, no eval gates, no traceability, or no abstention path.

## Task: Security Review

Purpose: Find authorization, isolation, prompt-injection, and auditability risks.

Procedure:

1. Read `checklists/security-review.md`.
2. Inspect the proposed policy flow.
3. Verify that policy is enforced before retrieval and across all retrievers, caches, rerankers, and tools.
4. Produce `outputs/security-review.md`.

Output format per finding:

- Finding
- Severity
- Why it matters
- Evidence
- Suggested action
- Confidence

## Task: Evaluation Plan

Purpose: Create an evaluation plan for a RAG launch or architecture change.

Procedure:

1. Read `templates/eval-plan-template.md`.
2. Read `checklists/eval-release-gates.md`.
3. Select eval slices that match the corpus and risk level.
4. Produce `outputs/eval-plan.md`.

Required gates:

- Retrieval recall
- Context precision
- Faithfulness
- Citation support
- Negative rejection
- Permission correctness
- p95 latency
- Cost per route
- Freshness and deletion propagation

## Task: Metadata Schema Design

Purpose: Recommend metadata fields for chunks and documents.

Procedure:

1. Read `schemas/chunk-metadata.schema.json`.
2. Read `templates/chunk-metadata.example.json`.
3. Map the human's corpus to required metadata fields.
4. Produce `outputs/metadata-schema-recommendation.md`.

Minimum output:

- Document-level metadata
- Chunk-level metadata
- ACL and tenant metadata
- Freshness and deletion metadata
- Citation metadata
- Fields needed for eval/debugging

## Task: Trace Logging Design

Purpose: Design trace fields for debugging, evaluation, cost control, and auditability.

Procedure:

1. Read `schemas/rag-trace.schema.json`.
2. Read `templates/rag-trace.example.json`.
3. Read `docs/production-runbook.md`.
4. Produce `outputs/trace-logging-design.md`.

Minimum output:

- Required trace fields
- Optional trace fields
- Fields that must be redacted or hashed
- Retention recommendations
- Example trace

## Task: Build Order Recommendation

Purpose: Recommend a phased implementation plan.

Procedure:

1. Read the build-order sections in `docs/system-design-guide.md`.
2. Map the human's current system to the four phases: measurable baseline, quality hardening, production governance, advanced architectures.
3. Produce `outputs/build-order.md`.

Rule:

Do not recommend GraphRAG, multimodal RAG, or agentic RAG until baseline retrieval, permissions, traces, and evals exist.
