# RAG System Design: Build It as an Evidence Supply Chain

This is the long-form guide behind the repo. Use the README, checklists, schemas, and templates when you need operational artifacts quickly.

Most teams start their RAG journey with a simple diagram:

```
Documents -> vector database -> prompt -> LLM -> answer
```

That diagram is useful for demos. It is dangerous for production.

Retrieval-Augmented Generation, or RAG, is no longer just "search a vector database and paste chunks into a prompt." In serious systems, RAG is a distributed architecture that combines data engineering, search, ranking, policy enforcement, prompt orchestration, model inference, evaluation, observability, and security.

The simplest way to say it:

> RAG should be designed as an evidence supply chain.

![RAG evidence supply chain hero](../diagrams/rag-evidence-supply-chain-hero.png)

The offline side turns messy source material into governed, queryable evidence. The online side turns a user request into ranked, policy-compliant, source-labeled context. The generation side turns that context into an answer. The evaluation side continuously checks whether the system retrieved the right evidence and used it faithfully.

That framing changes almost every design decision.

The short version:

- Start with ingestion, parsing, lineage, and permissions.
- Use hybrid retrieval, not vectors alone.
- Treat reranking and context assembly as ranking problems.
- Measure retrieval quality and answer faithfulness separately.
- Make policy, identity, and tenant isolation part of the architecture.
- Add GraphRAG, multimodal RAG, or agentic loops only when the failure mode demands it.

## How to Use This as a System Design Guide

This post is meant to be more than a tour of RAG techniques. Use it as a learning resource for designing a real RAG system from first principles.

By the end, you should be able to:

- explain why RAG is not just a vector database feature
- draw the offline indexing, online serving, and evaluation loops
- choose a chunking and retrieval strategy for a specific corpus
- defend when to use hybrid search, reranking, GraphRAG, multimodal RAG, or agentic RAG
- define the data model and metadata needed for citations, freshness, and access control
- design evals for retrieval quality, faithfulness, citation support, and security
- reason about latency, cost, tenancy, observability, and failure handling

If you have 30 minutes, read the system design view, ingestion, retrieval, evaluation, security, and production checklist sections.

If you have 60 minutes, also read the architecture-family, chunking, reranking, context assembly, hallucination, and build-order sections.

If you want to use this for interview prep or an architecture review, start with the problem statement below, sketch your own design, then compare it against the reference architecture and checklist.

## The System Design Problem

Design a production RAG system for an enterprise knowledge assistant.

The assistant must answer questions over internal documents such as policies, PDFs, tickets, wiki pages, product docs, support notes, and database-backed records. It must cite sources, respect permissions, handle stale documents, avoid unsupported claims, and produce traces that engineers can debug.

Functional requirements:

- ingest documents from multiple source systems
- search across text, tables, and structured metadata
- answer natural-language questions with citations
- abstain when evidence is missing or insufficient
- support document updates and deletions
- enforce user, group, tenant, role, and document-level permissions
- collect feedback and production failures for evaluation

Non-functional requirements:

- low-latency answers for common questions
- high recall for critical evidence
- strong citation support for factual claims
- tenant isolation and least-privilege retrieval
- reproducible traces for every answer
- measurable cost per request, user, tenant, route, and model
- safe degradation when retrieval, indexing, or model providers fail

The rest of the article is one way to solve that system design problem.

## The System Design View

A production RAG system has at least three loops: indexing, answering, and evaluation.

![Production RAG reference architecture](../diagrams/rag-reference-architecture.png)

```
OFFLINE INDEXING PLANE

Sources
  -> connectors and crawlers
  -> parsing and normalization
  -> chunking and metadata enrichment
  -> embeddings + sparse terms + graph extraction
  -> vector index + lexical index + graph store + lineage catalog

ONLINE INFERENCE PLANE

User query + identity
  -> policy gateway
  -> query rewrite / decomposition / routing
  -> hybrid retrieval
  -> fusion and reranking
  -> context compression
  -> grounded prompt assembly
  -> LLM generation
  -> faithfulness, citation, and safety checks
  -> answer, abstain, or escalate

EVALUATION LOOP

Traces + user feedback + failures
  -> golden datasets
  -> retrieval evals
  -> answer evals
  -> regression gates
  -> better ingestion, retrieval, prompts, and policies
```

This is the difference between a prototype and a system you can operate.

The online path deserves its own system-design view. A user request should move through authentication, authorization, query planning, retrieval, reranking, context packing, generation, verification, and tracing as separate control points.

![Online RAG serving request path](../diagrams/rag-online-serving-request-path.png)

The original RAG paper described a model that combines parametric memory in a seq2seq model with non-parametric memory in a dense vector index ([Lewis et al., 2020](https://arxiv.org/abs/2005.11401)). In application architectures, that idea becomes a full pipeline. LangChain describes the split as indexing versus retrieval-and-generation, while Microsoft frames advanced RAG around ingestion, inference, and evaluation phases ([LangChain RAG docs](https://docs.langchain.com/oss/python/langchain/rag), [Microsoft Advanced RAG](https://learn.microsoft.com/en-us/azure/developer/ai/advanced-retrieval-augmented-generation)).

Learning checkpoint:

- Draw the three loops without looking: indexing, answering, and evaluation.
- Label where identity, authorization, retrieval, reranking, context assembly, generation, verification, tracing, and feedback happen.
- Ask which parts must be synchronous in the request path and which can run offline.

## RAG Has Evolved Into an Architecture Family

The field did not jump straight to agentic GraphRAG. It moved in layers.

- **Retrieve-then-read:** Systems like DrQA retrieved documents and used a reader to extract answers. Search and reading were separate stages.
- **Dense retrieval:** DPR and REALM made learned dense retrieval central to open-domain QA. Retrieval became semantic, not only lexical.
- **Canonical RAG:** The generator used retrieved passages as non-parametric memory. Retrieval became part of generation.
- **Advanced RAG:** Query rewriting, hybrid search, reranking, compression, and verification were added. RAG became a multi-stage ranking and control system.
- **Modular RAG:** Routing, branching, loops, fusion, tools, and verifiers became composable modules. RAG became a graph of operators.
- **Graph RAG:** Entity, relation, and community indexes were added for corpus-level questions. Retrieval expanded from chunks to relationships.
- **Multimodal RAG:** Systems began retrieving images, page renders, tables, and visual layouts. Evidence was no longer just text.
- **Agentic RAG:** Agents decide when to retrieve, which tool to call, and whether to iterate. Retrieval became one operation inside a planning loop.

Sources worth reading include [DrQA](https://arxiv.org/abs/1704.00051), [DPR](https://arxiv.org/abs/2004.04906), [REALM](https://www.microsoft.com/en-us/research/publication/realm-retrieval-augmented-language-model-pre-training/), [the original RAG paper](https://arxiv.org/abs/2005.11401), [Modular RAG](https://arxiv.org/abs/2407.21059), [Self-RAG](https://arxiv.org/abs/2310.11511), [CRAG](https://arxiv.org/abs/2401.15884), [Microsoft GraphRAG](https://arxiv.org/abs/2404.16130), [ColPali](https://arxiv.org/abs/2407.01449), and the [Agentic RAG survey](https://arxiv.org/abs/2501.09136).

The important point is not that every system needs the newest architecture. Most do not.

The important point is that RAG has become a design space.

Simple RAG is right for direct evidence lookup. Advanced RAG is right when the baseline misses or misranks evidence. Graph RAG is useful when answers depend on relationships and distributed themes. Multimodal RAG matters when the source material lives in tables, figures, slides, scans, and layouts. Agentic RAG helps when the task itself requires multiple steps.

## The Hidden Center of RAG: Ingestion

Most RAG failures are born before the user asks a question.

Bad parsing destroys evidence. Bad chunking separates the answer from its qualifier. Missing metadata breaks filtering. Stale indexes answer from old truth. Weak lineage makes citations vague. Broken ACLs leak private documents.

A serious ingestion pipeline should preserve:

- source URI
- document ID
- source system
- source hash
- document version
- page numbers
- section hierarchy
- line or character offsets
- table boundaries
- figure captions
- code block boundaries
- author and timestamps
- tenant and ACL labels
- sensitivity classification
- parser version
- chunker version
- embedding model and dimension

If that feels excessive, remember what production RAG is being asked to do: answer with authority, cite sources, respect permissions, stay fresh, survive audits, and debug failures.

That is impossible if every chunk is just:

```json
{
  "text": "...",
  "embedding": [...]
}
```

Design exercise:

- Pick one corpus: policy PDFs, support tickets, source code, research papers, sales contracts, or customer-account records.
- Define the canonical document model you would store before chunking.
- Include source URI, version, ACLs, section hierarchy, timestamps, parser version, chunker version, and citation offsets.
- Decide what must be queryable as metadata versus what should only live in the text span.

## Chunking Is a Product Decision, Not a Preprocessing Detail

Chunking defines what your system can retrieve and what your model can cite.

Common chunking choices:

- **Fixed-size chunks:** Useful for fast baselines, logs, and homogeneous text. The risk is cutting through meaning, tables, and exceptions.
- **Recursive chunks:** Useful for general documents. Boundaries are better than fixed splitting, but still not layout-aware.
- **Structure-aware chunks:** Useful for Markdown, HTML, PDFs, code, and policy docs. Parser quality becomes the bottleneck.
- **Sliding-window chunks:** Useful for dense prose with boundary-spanning answers. The tradeoff is more duplicates, storage, and retrieval noise.
- **Semantic chunks:** Useful for mixed-topic long documents. They are more expensive and embedding-model dependent.
- **Parent-child chunks:** Useful for manuals, policies, and legal docs. They require lineage and context-budget management.
- **Proposition-level chunks:** Useful for factoid QA and compliance checks. Atomic facts can lose context or qualifications.
- **Late chunking:** Useful for long documents that need global context. It requires long-context embedding mechanics.

LangChain documents recursive splitting as a common baseline, LlamaIndex supports semantic splitting, AWS Bedrock Knowledge Bases supports hierarchical chunking, and research like Dense X and Late Chunking explores proposition-level and long-context-aware approaches ([LangChain splitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter), [LlamaIndex semantic splitter](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/), [AWS Bedrock chunking](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html), [Dense X](https://arxiv.org/abs/2312.06648), [Late Chunking](https://arxiv.org/abs/2409.04701)).

My default recommendation:

> Chunk by document structure first. Fall back to recursive/token chunking. Embed child chunks. Keep parent context available. Store lineage and ACL metadata on every chunk.

That usually beats blind fixed-size chunking.

Decision drill:

- Use fixed-size chunking only when the corpus is homogeneous and low-risk.
- Use structure-aware chunking when documents have headings, tables, sections, or policy exceptions.
- Use parent-child retrieval when answers need small searchable spans plus larger surrounding context.
- Use proposition-level chunks when factual precision matters more than narrative flow.
- Use late chunking or long-context embedding strategies when global document context materially improves retrieval.

## Vector Search Is Not Enough

Dense retrieval is powerful because it can match meaning, not just words. But many enterprise questions depend on exact words:

- error codes
- product names
- API names
- legal clauses
- SKUs
- acronyms
- customer IDs
- file paths
- ticket numbers
- policy identifiers

This is why production RAG usually needs hybrid search: dense vector retrieval plus sparse lexical retrieval.

```
Query
  -> BM25 / lexical search
  -> dense vector search
  -> optional graph / SQL / live-source retrieval
  -> reciprocal rank fusion
  -> dedupe
  -> rerank
  -> compress
  -> prompt
```

Azure AI Search uses Reciprocal Rank Fusion for hybrid queries. Qdrant and Pinecone both document hybrid dense/sparse patterns ([Azure hybrid ranking](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking), [Qdrant hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/), [Pinecone relevance guide](https://docs.pinecone.io/guides/optimize/increase-relevance)).

The retrieval stack should be treated like a ranking system.

- **Lexical retrieval** catches exact terms and identifiers.
- **Dense retrieval** catches paraphrase and semantic intent.
- **Fusion** merges different ranking signals without brittle score normalization.
- **Reranking** moves truly relevant chunks to the top.
- **Compression** extracts only the spans needed for generation.
- **Context assembly** packages evidence with source IDs, order, and constraints.

The mistake is optimizing only the vector database and ignoring the rest of the ranking stack.

Interview checkpoint:

- If the user asks for "error E-1042 in the EU refunds policy," explain why dense retrieval alone may miss or misrank the answer.
- Propose a hybrid strategy that combines BM25, dense search, metadata filters, RRF, deduplication, reranking, and context compression.
- State what you would measure before and after adding each stage.

## Reranking Is Where Many RAG Systems Start Getting Good

Initial retrieval should optimize recall. Final context should optimize precision.

Those are different jobs.

A good retriever may bring back 50 to 200 candidate chunks. A good reranker decides which 5 to 12 chunks deserve to enter the prompt.

- **No reranker:** Simple, fast, and lowest cost. Best for small, clean corpora.
- **RRF:** Cheap rank fusion across retrievers with very low cost. Best for hybrid search and multi-query retrieval.
- **Cross-encoder:** Strong query-passage relevance scoring with medium to high cost. Best for reranking the top 20-200 candidates.
- **ColBERT / late interaction:** Token-level matching with higher index complexity. Best for high-recall passage retrieval.
- **LLM reranker:** Flexible zero-shot ranking with the highest cost. Best for small final pools or offline distillation.

Cross-encoders jointly score a query and passage, which often improves relevance over bi-encoder retrieval, but every query-passage pair requires computation ([Sentence Transformers CrossEncoder docs](https://sbert.net/docs/cross_encoder/usage/usage.html)). LLM rerankers like RankGPT can be strong, but their latency and token cost usually make them late-stage or experimental tools ([RankGPT](https://arxiv.org/abs/2304.09542)).

The practical default:

```python
def retrieve_for_rag(query):
    lexical = bm25_search(query, k=100)
    dense = vector_search(embed(query), k=100)
    fused = reciprocal_rank_fusion([lexical, dense])
    candidates = dedupe(fused)[:80]
    reranked = cross_encoder_rerank(query, candidates)
    evidence = compress_to_relevant_spans(reranked[:10])
    return evidence
```

That small pattern solves many real-world failures.

## Query Transformation Should Be Used Like Medicine

Query rewriting, multi-query expansion, HyDE, decomposition, and routing are powerful. They also add latency, cost, and new failure modes.

Use them when they address a known problem.

- **Query rewrite:** Use when the user query is conversational or underspecified. Risk: the rewrite removes an important constraint.
- **Multi-query expansion:** Use when corpus vocabulary differs from user vocabulary. Risk: more noisy candidates.
- **HyDE:** Use when the query is too short or abstract for dense retrieval. Risk: hypothetical text can bias retrieval.
- **Decomposition:** Use when the question needs multiple evidence hops. Risk: subanswers may merge incorrectly.
- **Routing:** Use when different retrievers serve different domains or tools. Risk: the router sends the query to the wrong place.
- **Active retrieval:** Use when long-form generation needs evidence during writing. Risk: the control loop gets slow and hard to test.

HyDE generates a hypothetical document or answer, embeds it, and retrieves real documents similar to it ([HyDE](https://arxiv.org/abs/2212.10496)). FLARE retrieves during generation when upcoming content appears uncertain ([FLARE](https://arxiv.org/abs/2305.06983)). These are useful techniques, but they should be justified by evals.

Do not add orchestration because it feels clever. Add it because a measured failure class needs it.

## More Context Is Not Automatically Better

Large context windows are useful. They do not remove the need for retrieval.

Stuffing more text into the prompt can make answers worse:

- irrelevant chunks distract the model
- duplicate chunks waste budget
- conflicting chunks create ambiguity
- citations become vague
- key evidence gets buried

"Lost in the Middle" showed that models can perform worse when relevant information is placed in the middle of long context ([Liu et al., 2023](https://arxiv.org/abs/2307.03172)).

Context assembly should be a deliberate step:

```
Evidence block:

[S1] title=..., source=..., section=..., page=..., score=...
Relevant span...

[S2] title=..., source=..., section=..., page=..., score=...
Relevant span...

Instructions:
- Answer only from provided evidence.
- Cite each factual claim.
- Prefer primary and newer sources when evidence conflicts.
- If evidence is insufficient, say what is missing.
```

This is not just prompt engineering. It is evidence packaging.

## RAG Reduces Hallucination. It Does Not Eliminate It.

RAG can still hallucinate.

The model can retrieve weak evidence and overstate it. It can answer from stale sources. It can cite a source that does not support the sentence. It can ignore a qualifier. It can combine conflicting documents into a confident falsehood. It can answer when it should abstain.

RAGTruth studies unsupported and contradictory claims in RAG outputs, while attribution work such as AIS and ALCE focuses on whether generated claims are supported by sources ([RAGTruth](https://arxiv.org/abs/2401.00396), [AIS](https://arxiv.org/abs/2112.12870), [ALCE](https://arxiv.org/abs/2305.14627)).

The hallucination controls should map to the failure mode:

- **Missing evidence:** Measure Recall@k and evidence hit rate. Mitigate with better parsing, chunking, hybrid retrieval, and query rewrite.
- **Distractor evidence:** Measure context precision and nDCG. Mitigate with reranking, compression, dedupe, and filtering.
- **Unsupported claim:** Measure faithfulness, groundedness, and FActScore-style checks. Mitigate with claim-level verification and grounded prompts.
- **Bad citation:** Measure citation support. Mitigate with sentence-level source validation.
- **Stale evidence:** Measure freshness. Mitigate with version metadata and recency-aware retrieval.
- **Unanswerable answered:** Measure negative rejection. Mitigate with an evidence sufficiency gate and abstention policy.
- **Prompt injection:** Measure red-team and policy eval performance. Mitigate by treating retrieved text as untrusted data.

The key is accepting that hallucination is not one bug. It is a family of failure modes across retrieval, ranking, context assembly, and generation.

## Evaluation Is the Control System

Without evals, RAG optimization is vibes.

You need component evals and end-to-end evals.

![RAG retrieval and evaluation loop](../diagrams/rag-retrieval-eval-loop.png)

Component evals answer:

- Did we retrieve the right documents?
- Did the relevant chunk appear in the top 5 or top 10?
- Did reranking improve the order?
- Did filters enforce permissions?
- Did chunking preserve the answer span?

End-to-end evals answer:

- Did the answer address the question?
- Was it grounded in retrieved evidence?
- Were citations correct?
- Did the system abstain when evidence was insufficient?
- Did it remain safe and policy-compliant?
- Did latency and cost stay within budget?

Core metrics:

- **Recall@k:** Whether the retriever found the evidence.
- **Precision@k:** Whether retrieved context is mostly relevant.
- **MRR:** Whether useful evidence appears early.
- **nDCG:** Whether ranking quality improves.
- **Context precision/recall:** Whether retrieved context supports the expected answer.
- **Faithfulness/groundedness:** Whether answer claims are supported by context.
- **Citation support:** Whether cited sources support cited claims.
- **Negative rejection:** Whether the system refuses unanswerable questions.
- **Latency/cost:** Whether the system can operate in production.

RAGAS, ARES, TruLens, Phoenix, LangSmith, LlamaIndex evals, DeepEval, BEIR, KILT, RAGTruth, ALCE, and AIS are all useful references depending on which part of the system you are testing ([RAGAS](https://arxiv.org/abs/2309.15217), [ARES](https://arxiv.org/abs/2311.09476), [TruLens](https://www.trulens.org/), [Phoenix](https://arize.com/docs/phoenix/retrieval/quickstart-retrieval), [LangSmith](https://docs.langchain.com/langsmith/evaluation), [LlamaIndex retrieval eval](https://developers.llamaindex.ai/python/examples/evaluation/retrieval/retriever_eval/), [BEIR](https://arxiv.org/abs/2104.08663), [KILT](https://arxiv.org/abs/2009.02252), [RAGTruth](https://arxiv.org/abs/2401.00396), [ALCE](https://arxiv.org/abs/2305.14627)).

A practical release gate might look like this:

- **Retrieval recall:** No more than a 2 percentage point drop in Recall@5.
- **Faithfulness:** At least 0.90 on critical answerable cases.
- **Citation support:** At least 0.95 for cited factual claims.
- **Negative rejection:** Zero critical unsafe answers on high-risk unanswerable prompts.
- **Security:** Zero cross-tenant retrievals in adversarial tests.
- **Latency:** p95 under product SLA.
- **Cost:** Token and retrieval cost within budget.
- **Freshness:** Indexed documents inside the required sync window.

The exact numbers depend on risk. A casual internal FAQ assistant and a healthcare workflow should not share the same bar.

Evaluation lab:

- Create 50 representative questions from real user tasks.
- Add 10 unanswerable questions where the correct behavior is abstention.
- Add 10 permission-boundary questions where the system must not retrieve restricted documents.
- For each answerable question, label the source document, section, expected evidence span, and acceptable answer.
- Track retrieval recall separately from answer faithfulness so you know which stage failed.

## RAG Is Also a Security Architecture

RAG has a strange security property: untrusted retrieved text gets placed near trusted instructions inside the model context.

That means retrieved documents can carry:

- sensitive data
- stale claims
- malicious instructions
- poisoned content
- unauthorized tenant data
- irrelevant but persuasive text

OWASP's Top 10 for LLM Applications includes prompt injection, sensitive information disclosure, data and model poisoning, supply-chain risks, and excessive agency ([OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)). Microsoft has specific guidance on defending against indirect prompt injection in systems that consume untrusted content ([Microsoft indirect prompt injection guidance](https://learn.microsoft.com/en-us/security/zero-trust/sfi/defend-indirect-prompt-injection)).

The first rule:

> Do not retrieve unauthorized context and hope the model ignores it.

Authorization belongs before retrieval, not after generation.

### Policy and Identity: the Authorization Plane

Production RAG needs a dedicated authorization plane. The system should not treat identity as a user name in the prompt. It should propagate a verified identity token through the request path, resolve that identity into tenant, groups, roles, entitlements, document permissions, sensitivity clearance, and purpose of use, and convert those facts into retrieval filters before any context reaches the model.

The secure path looks like this:

![RAG policy and identity authorization plane](../diagrams/rag-policy-authorization-plane.png)

User or agent identity
  -> authentication gateway
  -> identity and group resolver
  -> policy decision point
  -> tenant-scoped / ACL-scoped retrievers
  -> reranker over permitted candidates only
  -> context builder with source, ACL, and sensitivity metadata
  -> grounded answer
  -> policy, citation, and audit checks

There are several layers:

- Authentication: Proves who the user, service, or agent is.
- RBAC: Maps that identity to coarse permissions such as employee, support agent, finance analyst, physician, admin, or external partner. NIST's RBAC work is still the canonical access-control foundation here ([NIST RBAC](https://csrc.nist.gov/Projects/role-based-access-control/faqs)).
- ABAC: Adds attributes such as region, department, data classification, business purpose, device posture, and time window.
- ReBAC: Handles relationship-based permissions, such as whether this user can access documents owned by accounts they manage. Google's Zanzibar paper is the classic reference design for large-scale relationship authorization ([Google Zanzibar](https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/)).
- Document ACLs: Attach allowed users, groups, roles, tenants, and deny rules to every source document and chunk.
- Policy as code: Keeps authorization logic outside prompts and application glue. A policy engine such as OPA can act as the policy decision point for structured requests ([Open Policy Agent](https://www.openpolicyagent.org/docs/latest)).

The retriever should execute with a policy envelope:

```json
{
  "subject": {
    "user_id": "u123",
    "tenant": "acme",
    "groups": ["finance"],
    "roles": ["analyst"]
  },
  "action": "rag.retrieve",
  "resource": {
    "corpus": "financial_policies",
    "classification_lte": "confidential"
  },
  "purpose": "employee_policy_question"
}
```

The policy engine should return allowed namespaces, filters, and obligations:

```json
{
  "allow": true,
  "filters": {
    "tenant": "acme",
    "allowed_groups": ["finance"],
    "classification": ["public", "internal", "confidential"]
  },
  "obligations": ["redact_pii", "log_sources", "cite_every_claim"]
}
```

Then every retrieval backend should enforce those filters: vector search, BM25, graph retrieval, SQL retrieval, cache lookup, and tool calls. Post-filtering after retrieval is weaker because unauthorized chunks may already have influenced reranking, compression, or prompt assembly. The safest pattern is pre-filter, retrieve, rerank, re-check, assemble, answer, and audit.

Security controls should include:

- **Unauthorized retrieval:** Enforce ACLs and tenant filters before search.
- **Cross-tenant leakage:** Use tenant namespaces, shards, or indexes; test negative cases.
- **Prompt injection:** Treat retrieved text as data, isolate it from instructions, and gate tools.
- **Data poisoning:** Control ingestion sources, scan content, and preserve provenance.
- **PII/PHI disclosure:** Redact, classify, minimize, log, and enforce least privilege.
- **Stale/deleted data:** Track tombstones, source versions, and deletion propagation.
- **Excessive agency:** Bound tools, loop counts, actions, approvals, and spend.

Azure AI Search documents document-level access control for RAG and agentic systems. Pinecone and Weaviate both document multi-tenancy isolation patterns ([Azure document-level ACLs](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview), [Pinecone multitenancy](https://docs.pinecone.io/guides/index-data/implement-multitenancy), [Weaviate multitenancy](https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy)).

For SaaS and enterprise platforms, multi-tenancy and freshness are not deployment details. They decide how indexes are partitioned, how deletes propagate, whether caches can be shared, when live source retrieval is required, and how negative access-control tests should be designed.

![Multi-tenant and freshness-aware RAG architecture](../diagrams/rag-multitenant-freshness-architecture.png)

Threat-model exercise:

- Write five questions that user A is allowed to ask and user B is not.
- Add poisoned source text that tries to override system instructions.
- Add a deleted or stale document that used to contain the right answer.
- Add a cross-tenant query that should return no evidence.
- Verify the retriever, reranker, context builder, model response, and logs all preserve the boundary.

## Where RAG Actually Shows Up in Production

The best use cases involve valuable knowledge that is external to the model, changes over time, needs citations, or must respect access control.

- **Enterprise knowledge assistants:** RAG helps answer over internal docs, policies, tickets, and collaboration tools. Watch for ACL leaks, stale docs, and weak citations.
- **Customer support:** RAG helps ground answers in KBs, orders, policies, and tickets. Watch for hallucinated policies, bad escalation, and tool misuse.
- **Legal and compliance:** RAG helps answer from authoritative legal and policy sources. Watch for wrong jurisdiction, weak citation, and missing qualifiers.
- **Healthcare operations:** RAG helps search across clinical docs, policies, and research. Watch for PHI disclosure, unsafe clinical inference, and audit gaps.
- **Finance/advisor tools:** RAG helps summarize research, risk notes, and client records. Watch for suitability, entitlements, retention, and explainability.
- **Code assistants:** RAG helps retrieve code, docs, APIs, issues, and symbols. Watch for secret leakage, stale branch context, and license/IP issues.
- **Search augmentation:** RAG adds synthesis and citations to traditional search. Watch for latency, ranking quality, and unsupported summaries.

Public examples and docs include Morgan Stanley's internal assistant work with OpenAI, Klarna's AI assistant, Thomson Reuters CoCounsel, GitHub Copilot repository indexing, Sourcegraph Cody context, Azure AI Search, and Google Vertex AI Search ([Morgan Stanley/OpenAI](https://openai.com/customer-stories/morgan-stanley), [Klarna AI assistant](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/), [Thomson Reuters CoCounsel](https://legal.thomsonreuters.com/en/products/cocounsel-core), [GitHub Copilot repository indexing](https://docs.github.com/en/enterprise-cloud%40latest/copilot/using-github-copilot/copilot-chat/indexing-repositories-for-copilot-chat), [Sourcegraph Cody](https://sourcegraph.com/docs/cody/core-concepts/context), [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search), [Google Vertex AI Search](https://cloud.google.com/enterprise-search)).

## A Technical Feature Map for Production RAG

If I were turning this into an engineering roadmap, I would track features by layer, not by vendor.

- **Ingestion and indexing:** incremental connectors, deletion tombstones, parser/chunker/embedding versioning, document lineage, and layout-aware extraction for PDFs, slides, tables, and images. Tools such as Docling show why document conversion is part of retrieval quality, not a preprocessing footnote ([Docling](https://github.com/docling-project/docling)).
- **Retrieval planning:** classify each query by intent, source, freshness, modality, and complexity; route to vector, BM25, SQL, graph, multimodal, web, or no-retrieval paths. Azure AI Search's agentic retrieval documents the move from one query to query planning, subqueries, and reranking ([Azure AI Search agentic retrieval](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview)).
- **Candidate generation:** run hybrid dense plus sparse search, metadata filters, graph or SQL retrieval when structure matters, and contextual retrieval when chunks lose document-level meaning. Anthropic's contextual retrieval prepends chunk-specific context before embedding and BM25 indexing, and reports large retrieval-failure reductions when combined with reranking ([Anthropic Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval)).
- **Ranking and context construction:** use RRF, cross-encoder or LLM rerankers, diversity and freshness boosts, parent-child expansion, compression, citation-support checks, and source-labeled prompt packaging.
- **Policy and identity:** propagate user, tenant, role, group, purpose, auth strength, delegation, and workload identity across retrieval, reranking, caches, tools, and logs. Enforce RBAC/ABAC/ReBAC with policy enforcement points before retrieval, prompt assembly, tool calls, and response return.
- **Evaluation and operations:** maintain golden and production-derived eval sets; measure recall@k, nDCG, faithfulness, citation support, refusal quality, access-control failures, latency, and cost. Use canary indexes, rollback, drift/freshness monitors, and trace spans for authorize, rewrite, retrieve, rerank, build_prompt, generate, verify_citations, and respond. OpenTelemetry's GenAI conventions are useful as a starting point for this trace vocabulary ([OpenTelemetry GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/)).
- **Agent and tool safety:** put tools behind a gateway with per-tool scopes, risk tiers, approval gates, loop/action budgets, and tool-call evals. This matters once RAG stops answering and starts acting.

The rule is simple: add a feature only when it maps to a measured failure class. If the evals cannot name the failure, the roadmap is probably theater.

## The Production Runbook Most RAG Demos Skip

The video and transcript review mostly confirms the shape of this architecture, but it adds one useful warning: most RAG demos do not fail because the model is weak. They fail because the system has no operational runbook.

The recurring failure modes are concrete:

- **Bad chunking:** Use structure-aware chunking first, overlap as boundary insurance, and semantic chunking only when it improves measured retrieval.
- **Embedding mismatch:** Keep indexing and query embeddings on the same model/version; test retrieval before blaming generation.
- **Retrieval noise:** Use hybrid retrieval, metadata filters, reranking, deduplication, and context compression.
- **Context overflow:** Enforce token budgets before LLM calls; pack evidence by relevance, diversity, source authority, and citation need.
- **Hallucination:** Grade evidence relevance and answer groundedness; abstain or retry when evidence is weak.

The operational controls are just as important as retrieval quality. Cache at the right layer: query-answer pairs for stable FAQs, embeddings for repeated text, retrieval result sets for repeated searches, and generated answers only when corpus version, ACL scope, and policy version match. Put token-budget gates before model calls, not after the bill arrives. Track cost per user, endpoint, tenant, model, and route so runaway usage is visible.

Failure handling also needs design. If vector retrieval fails, fall back to lexical search or direct source snippets. If the LLM provider is unavailable, return a useful degraded response rather than a blank error. If retrieval relevance is low, rewrite once or twice, then stop with a clear abstention. Infinite "try harder" loops are not intelligence; they are a cost incident.

Debugging should start from traces, not vibes. For every answer, capture the query, route, rewritten queries, retrieved IDs, scores, filters, reranker output, context size, prompt version, model version, citations, token count, latency, policy decision, and final evaluator scores. The question is not only "was the answer good?" It is "which stage made it good or bad?" ([Production RAG full course](https://www.youtube.com/watch?v=mHxLXzYjQRE), [RAG crash course](https://www.youtube.com/watch?v=swvzKSOEluc), [RAG from Scratch](https://github.com/langchain-ai/rag-from-scratch)).

GraphRAG, agentic RAG, and multimodal RAG still matter, but they are not badges. GraphRAG is a graph lifecycle: extract entities and relations, canonicalize duplicates, store edge confidence/source/time/ACL metadata, then support local neighborhood search and global community summaries. Agentic RAG is a control loop: route, retrieve, grade, rewrite, retry, answer, or abstain. Multimodal RAG is for evidence that text extraction damages: tables, diagrams, charts, signatures, forms, scans, and page layout ([IBM GraphRAG](https://www.ibm.com/think/topics/graphrag), [IBM Agentic RAG](https://www.ibm.com/think/topics/agentic-rag), [GraphRAG video](https://www.youtube.com/watch?v=Aw7iQjKAX2k), [RAG vs Agentic AI](https://www.youtube.com/watch?v=fB2JQXEH_94)).

## A Practical Build Order

If I were building a production RAG system from scratch, I would not start with agents.

I would build in four phases.

### Phase 1: Measurable baseline

- Pick a few authoritative corpora.
- Build connectors and raw artifact storage.
- Parse into a canonical document model.
- Use structure-aware or recursive chunking.
- Store source metadata and ACL labels.
- Build dense and BM25 indexes.
- Implement hybrid retrieval with RRF.
- Generate answers with citations.
- Create a small golden eval set.
- Trace every request.

### Phase 2: Quality hardening

- Add parent-child retrieval for long documents.
- Add cross-encoder reranking.
- Add context compression.
- Add query rewrite/decomposition for known failures.
- Add abstention rules for weak evidence.
- Add faithfulness, citation, and unanswerable evals.
- Promote production failures into evals.

### Phase 3: Production governance

- Enforce document-level ACLs before retrieval.
- Add tenant isolation tests.
- Add prompt-injection red-team tests.
- Add PII/sensitivity classification.
- Add index versioning and rollback.
- Add freshness monitors.
- Define release gates.
- Build runbooks for bad answers, ACL incidents, index failures, and deletion requests.

### Phase 4: Advanced architectures

- Add graph retrieval for relationship-heavy questions.
- Add multimodal retrieval for visual documents.
- Add live API/database retrieval for volatile data.
- Add agentic loops for multi-step workflows.
- Add cost-aware routing and early exits.
- Distill expensive rerankers or judges where possible.

That order matters. Advanced orchestration will not rescue a system with broken parsing, missing ACLs, no evals, and weak retrieval.

## RAG System Design Interview Cheat Sheet

When someone asks you to design RAG, clarify the problem before naming tools.

Start with requirements:

- What corpus are we answering from?
- How large is it?
- How often does it change?
- What source systems own the truth?
- Who is allowed to see which documents?
- Do answers need citations?
- Are there unanswerable or high-risk questions?
- What latency, cost, freshness, and audit constraints matter?

Then propose the architecture:

- offline ingestion plane for connectors, parsing, chunking, metadata, embeddings, indexes, ACLs, lineage, and freshness
- online serving plane for auth, policy, query planning, hybrid retrieval, fusion, reranking, context assembly, generation, citation verification, and response
- evaluation loop for golden sets, production failures, retrieval metrics, faithfulness metrics, security tests, release gates, and regression checks
- observability layer for traces, retrieved IDs, scores, prompt versions, model versions, policy decisions, costs, and evaluator scores

Define the data model:

- document ID, source URI, source system, version, hash, author, timestamp, tenant, ACLs, sensitivity, deletion state
- chunk ID, parent document ID, section path, page number, offsets, parser version, chunker version, embedding model, sparse terms, graph entities, citation metadata
- query trace, route, filters, candidate IDs, reranker scores, final context, answer, citations, evaluator outputs

Call out the tradeoffs:

- fixed-size chunks are easy but often break meaning
- vectors catch semantic similarity but miss exact identifiers
- hybrid search improves recall but needs fusion and deduplication
- reranking improves precision but adds latency and cost
- large context windows help but do not replace ranking
- GraphRAG helps relationship-heavy questions but adds graph lifecycle complexity
- agentic RAG helps multi-step workflows but is harder to test and bound
- post-filtering unauthorized chunks is weaker than pre-filtering retrieval

Name the release gates:

- retrieval recall and ranking quality
- answer faithfulness and citation support
- abstention quality on unanswerable questions
- cross-tenant and document-level access-control tests
- prompt-injection and poisoning tests
- p50, p95, and p99 latency by stage
- cost per route, tenant, model, and user
- freshness and deletion-propagation checks

Strong RAG system design answers sound less like "use a vector DB" and more like "build a governed evidence pipeline, measure each stage, and only add complexity when a failure mode proves it is needed."

## Glossary

- **RAG:** Retrieval-Augmented Generation, a pattern where a model answers using retrieved external evidence rather than only parametric memory.
- **Chunk:** A searchable unit derived from a source document. Chunk design determines what the system can retrieve and cite.
- **Embedding:** A vector representation of text, image, table, or another artifact used for semantic similarity search.
- **BM25:** A lexical ranking method that is strong for exact terms, identifiers, and keyword-heavy queries.
- **Hybrid retrieval:** A retrieval strategy that combines dense semantic search with sparse lexical search.
- **RRF:** Reciprocal Rank Fusion, a simple way to merge ranked results from multiple retrievers.
- **Reranker:** A second-stage ranking model that scores candidate passages against the query with more precision.
- **Context assembly:** The step that selects, orders, compresses, labels, and packages retrieved evidence for the model.
- **Faithfulness:** Whether generated claims are supported by retrieved evidence.
- **Citation support:** Whether a cited source actually supports the sentence or claim attached to it.
- **Negative rejection:** Whether the system refuses to answer when the evidence is missing, weak, or unauthorized.
- **GraphRAG:** RAG that uses entity, relationship, or community structures to answer relationship-heavy or corpus-level questions.
- **Agentic RAG:** RAG inside a planning loop where an agent decides when to retrieve, rewrite, retry, call tools, answer, or abstain.
- **Policy envelope:** The identity, tenant, role, group, clearance, purpose, and obligations used to restrict retrieval and generation.

## The Production Checklist

Before shipping a RAG system, ask:

- Can every answer be traced back to source chunks?
- Are source chunks tied to document versions?
- Are permissions enforced before retrieval?
- Can the system abstain when evidence is weak?
- Are citations validated?
- Are unanswerable questions in the eval set?
- Are prompt-injection attacks in the eval set?
- Can you reproduce an answer from logs?
- Do you know p50, p95, and p99 latency by stage?
- Do you know cost per request by stage?
- Can you roll back an index?
- Can you delete a source document and prove it no longer appears?
- Can you explain why a particular chunk was retrieved?
- Are production failures automatically promoted into future test cases?

If the answer is no, you do not have a production RAG system yet. You have a promising prototype.

## The Takeaway

RAG started as a way to connect generative models to external memory. It has become an architecture discipline.

The best production systems do not treat RAG as "vector search plus prompt." They treat it as an evidence supply chain:

1. Parse documents into a structure-preserving representation.
2. Chunk by document structure with smart fallbacks.
3. Store lineage, metadata, ACLs, and versions.
4. Retrieve with hybrid dense plus sparse search.
5. Fuse and rerank a broad candidate pool.
6. Compress evidence into source-labeled context.
7. Generate with citation and abstention constraints.
8. Verify faithfulness and citation support.
9. Trace every stage.
10. Continuously evaluate against golden, synthetic, adversarial, and production-derived tests.

The future of RAG is not one architecture. It is a toolbox.

Use simple RAG when direct lookup is enough. Use advanced RAG when retrieval quality matters. Use Graph RAG when relationships and corpus-level synthesis matter. Use multimodal RAG when the evidence is visual. Use agentic RAG when the workflow itself requires planning and iteration.

The discipline is knowing which system you are building, and proving it works with evidence.

## Source List

- Original RAG paper: https://arxiv.org/abs/2005.11401
- Microsoft Advanced RAG: https://learn.microsoft.com/en-us/azure/developer/ai/advanced-retrieval-augmented-generation
- AWS RAG options and architectures: https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/introduction.html
- LangChain RAG docs: https://docs.langchain.com/oss/python/langchain/rag
- DrQA: https://arxiv.org/abs/1704.00051
- DPR: https://arxiv.org/abs/2004.04906
- REALM: https://www.microsoft.com/en-us/research/publication/realm-retrieval-augmented-language-model-pre-training/
- Modular RAG: https://arxiv.org/abs/2407.21059
- Self-RAG: https://arxiv.org/abs/2310.11511
- CRAG: https://arxiv.org/abs/2401.15884
- Microsoft GraphRAG: https://arxiv.org/abs/2404.16130
- GraphRAG docs: https://microsoft.github.io/graphrag/
- IBM GraphRAG: https://www.ibm.com/think/topics/graphrag
- ColPali: https://arxiv.org/abs/2407.01449
- Agentic RAG survey: https://arxiv.org/abs/2501.09136
- IBM Agentic RAG: https://www.ibm.com/think/topics/agentic-rag
- LangChain RAG from Scratch: https://github.com/langchain-ai/rag-from-scratch
- Anthropic Contextual Retrieval: https://www.anthropic.com/engineering/contextual-retrieval
- Azure AI Search agentic retrieval: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview
- Docling: https://github.com/docling-project/docling
- Video: RAG Crash Course for Beginners: https://www.youtube.com/watch?v=swvzKSOEluc
- Video: Learn RAG From Scratch: https://www.youtube.com/watch?v=sVcwVQRHIc8
- Video: What is Agentic RAG?: https://www.youtube.com/watch?v=0z9_MhcYvcY
- Video: GraphRAG vs Traditional RAG: https://www.youtube.com/watch?v=Aw7iQjKAX2k
- Video: RAG vs Agentic AI: https://www.youtube.com/watch?v=fB2JQXEH_94
- Video: Production RAG with LangChain & Vector Databases: https://www.youtube.com/watch?v=mHxLXzYjQRE
- LangChain recursive splitter: https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter
- LlamaIndex semantic splitter: https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/
- AWS Bedrock chunking: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html
- Dense X Retrieval: https://arxiv.org/abs/2312.06648
- Late Chunking: https://arxiv.org/abs/2409.04701
- Azure hybrid ranking: https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking
- Qdrant hybrid queries: https://qdrant.tech/documentation/search/hybrid-queries/
- Pinecone relevance guide: https://docs.pinecone.io/guides/optimize/increase-relevance
- Sentence Transformers CrossEncoder docs: https://sbert.net/docs/cross_encoder/usage/usage.html
- RankGPT: https://arxiv.org/abs/2304.09542
- HyDE: https://arxiv.org/abs/2212.10496
- FLARE: https://arxiv.org/abs/2305.06983
- Lost in the Middle: https://arxiv.org/abs/2307.03172
- RAGTruth: https://arxiv.org/abs/2401.00396
- AIS: https://arxiv.org/abs/2112.12870
- ALCE: https://arxiv.org/abs/2305.14627
- RAGAS: https://arxiv.org/abs/2309.15217
- ARES: https://arxiv.org/abs/2311.09476
- TruLens: https://www.trulens.org/
- Phoenix: https://arize.com/docs/phoenix/retrieval/quickstart-retrieval
- LangSmith evaluation: https://docs.langchain.com/langsmith/evaluation
- LlamaIndex retrieval eval: https://developers.llamaindex.ai/python/examples/evaluation/retrieval/retriever_eval/
- BEIR: https://arxiv.org/abs/2104.08663
- KILT: https://arxiv.org/abs/2009.02252
- OpenTelemetry GenAI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Microsoft indirect prompt injection guidance: https://learn.microsoft.com/en-us/security/zero-trust/sfi/defend-indirect-prompt-injection
- NIST RBAC: https://csrc.nist.gov/Projects/role-based-access-control/faqs
- Google Zanzibar: https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/
- Open Policy Agent: https://www.openpolicyagent.org/docs/latest
- Azure document-level ACLs: https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview
- Pinecone multitenancy: https://docs.pinecone.io/guides/index-data/implement-multitenancy
- Weaviate multitenancy: https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy
- Morgan Stanley/OpenAI: https://openai.com/customer-stories/morgan-stanley
- Klarna AI assistant: https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/
- Thomson Reuters CoCounsel: https://legal.thomsonreuters.com/en/products/cocounsel-core
- GitHub Copilot repository indexing: https://docs.github.com/en/enterprise-cloud%40latest/copilot/using-github-copilot/copilot-chat/indexing-repositories-for-copilot-chat
- Sourcegraph Cody context: https://sourcegraph.com/docs/cody/core-concepts/context
- Azure AI Search: https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search
- Google Vertex AI Search: https://cloud.google.com/enterprise-search
