# RAG Architecture Review

## System Summary

- Product or workflow:
- Primary users:
- Corpus:
- Source systems:
- Answer risk level:
- Required freshness:
- Required citations:
- Tenant or permission model:

## Proposed Architecture

Describe the offline indexing plane, online serving plane, and evaluation loop.

## Requirements Check

| Area | Current Design | Gap | Decision |
|---|---|---|---|
| Ingestion |  |  |  |
| Parsing |  |  |  |
| Chunking |  |  |  |
| Metadata and lineage |  |  |  |
| Permissions |  |  |  |
| Retrieval |  |  |  |
| Reranking |  |  |  |
| Context assembly |  |  |  |
| Generation |  |  |  |
| Citation verification |  |  |  |
| Evaluation |  |  |  |
| Observability |  |  |  |
| Failure handling |  |  |  |

## Key Design Decisions

| Decision | Selected Option | Alternatives | Reason |
|---|---|---|---|
| Chunking strategy |  |  |  |
| Retrieval strategy |  |  |  |
| Reranking strategy |  |  |  |
| Access-control enforcement |  |  |  |
| Freshness model |  |  |  |
| Eval release gates |  |  |  |

## Risks

| Risk | Severity | Evidence | Mitigation |
|---|---|---|---|
| Unauthorized retrieval | High |  |  |
| Unsupported claims | High |  |  |
| Stale answers | Medium |  |  |
| Cost runaway | Medium |  |  |
| Latency regression | Medium |  |  |

## Launch Recommendation

Choose one:

- Ready for limited beta
- Ready after required fixes
- Not ready for production

Required fixes before launch:

1. 
2. 
3. 
