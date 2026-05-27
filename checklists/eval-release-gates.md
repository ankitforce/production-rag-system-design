# Evaluation Release Gates

Use this as the minimum gate set before shipping or changing a production RAG system.

## Retrieval Gates

| Gate | What It Measures | Example Threshold |
|---|---|---|
| Recall@k | Whether the right evidence appears in candidates. | Critical questions meet target recall at k=20 or k=50. |
| MRR / nDCG | Whether relevant evidence is ranked early. | Top-ranked results improve over baseline. |
| Context precision | Whether final context avoids irrelevant chunks. | Irrelevant context rate stays below review threshold. |
| Exact-term recall | Whether identifiers, clauses, and error codes are found. | Lexical or hybrid retrieval beats dense-only baseline. |
| Permission correctness | Whether only authorized evidence is retrieved. | Zero known cross-tenant or ACL violations. |

## Answer Gates

| Gate | What It Measures | Example Threshold |
|---|---|---|
| Faithfulness | Claims are supported by retrieved evidence. | Unsupported factual claims stay below threshold. |
| Citation support | Citations actually support attached claims. | Citation verifier passes critical answer set. |
| Negative rejection | System abstains when evidence is absent or weak. | Unanswerable set does not produce confident answers. |
| Completeness | Answer covers the required evidence. | Human or judge score meets launch bar. |
| Safety | Answer avoids forbidden disclosure or actions. | Red-team set has zero high-severity failures. |

## Operational Gates

| Gate | What It Measures |
|---|---|
| Latency by stage | p50, p95, and p99 for retrieval, reranking, generation, judging, and total route. |
| Cost by stage | Token and infrastructure cost by route, model, user, tenant, and retry path. |
| Freshness | Index age and deletion propagation by source system. |
| Regression stability | New version does not regress critical golden cases. |
| Observability | Failed answers can be traced to the responsible stage. |

## Required Eval Slices

- Common questions
- Critical/high-risk questions
- Rare identifiers and exact-match queries
- Long documents and boundary-spanning evidence
- Tables and layout-sensitive evidence
- Unanswerable questions
- Stale or deleted documents
- Cross-tenant and unauthorized queries
- Prompt-injection documents
- Production failures from previous releases
