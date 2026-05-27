# Production RAG Runbook

Use this runbook when a RAG system produces bad, slow, stale, unsafe, or expensive answers.

## Failure Mode Map

| Failure | Likely Cause | First Controls |
|---|---|---|
| Wrong answer with confident tone | Weak evidence, missing abstention, poor faithfulness checks. | Inspect retrieved chunks, citation support, and evaluator scores. |
| Right source exists but was not retrieved | Parser, chunker, embedding, BM25, metadata filter, or query rewrite issue. | Run retrieval evals and compare lexical, dense, and hybrid candidates. |
| Source retrieved but ignored | Context packing, chunk order, prompt constraints, or lost-in-the-middle sensitivity. | Inspect final context packet and evidence ordering. |
| Citation does not support claim | Citation verifier missing or too weak. | Add claim-to-source support checks and citation-level evals. |
| Unauthorized evidence appears | Policy applied too late or inconsistently across retrievers/caches. | Enforce tenant and ACL filters before retrieval and test cache boundaries. |
| Stale answer | Index freshness, source deletion, or version propagation issue. | Check source timestamps, index version, tombstones, and deletion proof. |
| Cost spike | Too many retries, broad retrieval, expensive judges, or unbounded agent loops. | Add route budgets, retry caps, model routing, and spend alerts. |
| Latency spike | Slow parser, retrieval backend, reranker, model, or judge. | Break p50/p95/p99 latency down by stage. |

## Trace Fields to Inspect

- user and tenant envelope
- query and rewritten queries
- route and retriever selection
- filters and policy decision
- candidate IDs and scores
- reranker output
- context size and dropped chunks
- prompt and model version
- citations
- evaluator outputs
- latency and cost by stage

## Escalation Rules

- If evidence is missing, abstain or ask for clarification.
- If permissions are uncertain, deny retrieval and log the policy failure.
- If freshness is uncertain for high-risk answers, route to live source or mark the answer stale.
- If judge confidence is low, return a bounded response with cited uncertainty.
- If loop limits are reached, stop and explain the failed stage.
