# Production Readiness Checklist

Use this before moving a RAG system from prototype to production.

## Evidence and Data Plane

- [ ] Every source document has a stable document ID, source URI, source system, version, hash, author or owner, timestamp, and deletion state.
- [ ] Every chunk has a stable chunk ID, parent document ID, section path, page or offset range, parser version, chunker version, embedding model, and citation metadata.
- [ ] The system preserves tables, code blocks, figures, captions, and layout-sensitive evidence when those artifacts matter.
- [ ] The ingestion pipeline records parse failures and routes them to review.
- [ ] The system can prove a deleted document no longer appears in indexes, caches, prompts, or traces.

## Retrieval and Ranking

- [ ] Dense retrieval and lexical retrieval are both measured separately.
- [ ] Hybrid retrieval uses explicit fusion, deduplication, and candidate-depth controls.
- [ ] Reranking is evaluated for quality, latency, and cost before launch.
- [ ] Context assembly records which candidates were included, compressed, dropped, or reordered.
- [ ] The retrieval stack has tests for exact identifiers, acronyms, policy clauses, error codes, and rare names.

## Generation and Grounding

- [ ] Prompts require source-grounded answers and abstention when evidence is weak.
- [ ] Citations are checked against the claims they support.
- [ ] Unanswerable questions are included in evals.
- [ ] The model is not asked to infer policy, identity, or permissions from prompt text.
- [ ] The answer path can degrade safely when retrieval or model providers fail.

## Evaluation and Release Gates

- [ ] Golden eval sets cover common, critical, long-tail, unanswerable, stale, and adversarial questions.
- [ ] Retrieval metrics and answer metrics are tracked separately.
- [ ] Production failures are promoted into regression cases.
- [ ] Releases have pass/fail gates for retrieval recall, context precision, faithfulness, citation support, negative rejection, latency, cost, and security.
- [ ] Eval reports include examples, not only aggregate scores.

## Operations

- [ ] Traces capture query, identity envelope, route, rewritten queries, filters, retrieved IDs, scores, reranker output, context size, prompt version, model version, citations, evaluator scores, latency, token count, and cost.
- [ ] p50, p95, and p99 latency are visible by stage.
- [ ] Cost is tracked by user, tenant, endpoint, route, model, retriever, and evaluation step.
- [ ] Index versions can be rolled back.
- [ ] Alerting covers index freshness, retrieval errors, policy denials, provider failures, cost spikes, and eval regressions.
