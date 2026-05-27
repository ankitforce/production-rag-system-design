# RAG Architecture Taxonomy

Use this map to choose the simplest RAG architecture that addresses the measured failure mode.

| Pattern | Use When | Main Tradeoff |
|---|---|---|
| Naive RAG | Direct lookup over a small, clean corpus is enough. | Fast to build, but weak on permissions, ranking, evals, and citations. |
| Advanced RAG | Baseline retrieval misses or misranks evidence. | Better quality through hybrid search, reranking, compression, and evals, with more latency and moving parts. |
| Modular RAG | The workflow needs routing, branching, or multiple retrieval sources. | Flexible, but harder to test and observe. |
| Graph RAG | Answers depend on relationships, communities, or corpus-level synthesis. | Adds entity extraction, canonicalization, graph lifecycle, and graph-specific evals. |
| Multimodal RAG | Evidence lives in tables, figures, scans, forms, screenshots, or layouts. | Requires visual parsing, layout preservation, and multimodal retrieval/evaluation. |
| Agentic RAG | The task needs planning, retries, tool use, or multi-step workflows. | Powerful, but harder to bound for cost, latency, permissions, and safety. |

## Decision Rule

Start with the least complex architecture that can be measured and operated:

1. Build a measurable hybrid retrieval baseline.
2. Add reranking and context assembly when ranking quality is the bottleneck.
3. Add query rewrite or decomposition for known query failure classes.
4. Add graph, multimodal, or agentic patterns only when evals show the simpler system cannot meet requirements.

## Anti-Patterns

- Adding agents before retrieval, ACLs, and evals are stable.
- Using a vector database as the whole architecture.
- Post-filtering unauthorized chunks after retrieval.
- Optimizing generation before measuring retrieval quality.
- Treating large context windows as a replacement for ranking.
