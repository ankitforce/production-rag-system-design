# RAG Evaluation Plan

## Scope

- System:
- Corpus:
- User roles:
- Release version:
- Eval owner:

## Eval Sets

| Set | Purpose | Size | Source |
|---|---|---|---|
| Common questions | Everyday quality |  |  |
| Critical questions | High-impact correctness |  |  |
| Unanswerable questions | Abstention behavior |  |  |
| Exact identifier queries | Lexical recall |  |  |
| Permission tests | Tenant and ACL isolation |  |  |
| Prompt-injection tests | Indirect injection resistance |  |  |
| Production failures | Regression prevention |  |  |

## Metrics

| Metric | Component | Target | Blocking |
|---|---|---|---|
| Recall@k | Retrieval |  | Yes |
| Context precision | Retrieval/context assembly |  | Yes |
| Faithfulness | Answer generation |  | Yes |
| Citation support | Answer generation |  | Yes |
| Negative rejection | Abstention |  | Yes |
| p95 latency | Operations |  | Yes |
| Cost per request | Operations |  | No |

## Review Procedure

1. Freeze corpus version, index version, prompt version, model version, and policy version.
2. Run retrieval-only evals and inspect failed examples.
3. Run end-to-end answer evals.
4. Run permission, deletion, and prompt-injection tests.
5. Compare against previous release.
6. Promote failures into future regression sets.
7. Make a release decision with required fixes listed.

## Release Decision

- Ship:
- Block:
- Ship behind feature flag:
- Required fixes:
