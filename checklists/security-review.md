# Security Review Checklist

Use this to review RAG systems that retrieve private, tenant-scoped, regulated, or operationally sensitive evidence.

## Authorization Plane

- [ ] Authentication happens before query planning or retrieval.
- [ ] The request includes a verified identity envelope, not just a display name in the prompt.
- [ ] The policy decision resolves tenant, groups, roles, entitlements, relationship permissions, classification clearance, purpose of use, and obligations.
- [ ] Tenant and ACL filters are applied before retrieval.
- [ ] The same policy envelope applies to vector search, lexical search, graph retrieval, SQL retrieval, live APIs, caches, and tool calls.
- [ ] Rerankers only see permitted candidates.
- [ ] Context compression only sees permitted candidates.
- [ ] Caches are keyed by corpus version, tenant, ACL scope, policy version, and sensitivity requirements.

## Isolation Tests

- [ ] Tenant B cannot retrieve tenant A chunks through dense retrieval.
- [ ] Tenant B cannot retrieve tenant A chunks through lexical retrieval.
- [ ] Tenant B cannot retrieve tenant A chunks through reranking, compression, cache hits, graph traversal, or generated citations.
- [ ] Deleted or revoked documents disappear from indexes, caches, traces, and generated answers.
- [ ] Redaction obligations are enforced before context reaches the model.

## Prompt Injection and Data Poisoning

- [ ] Retrieved text is treated as untrusted input.
- [ ] System and developer instructions are isolated from retrieved evidence.
- [ ] The model is instructed to ignore source text that asks it to change rules, reveal secrets, bypass policy, or call tools.
- [ ] The corpus has tests for indirect prompt injection embedded in documents, tickets, web pages, and comments.
- [ ] Tool calls require policy checks independent of model reasoning.
- [ ] High-impact actions require human approval or step-up authentication.

## Auditability

- [ ] Every answer records policy decision, filters, selected chunks, dropped chunks, citations, model version, prompt version, and evaluator outputs.
- [ ] Security incidents can be reproduced from traces without exposing more data than necessary.
- [ ] Logs avoid storing raw secrets, access tokens, passwords, private cookies, and unnecessary PII.
- [ ] Audit traces preserve enough source IDs to investigate answers after index updates.
