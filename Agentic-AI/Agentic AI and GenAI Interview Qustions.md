# Agentic AI / GenAI Interview Prep: 50 Questions + Gold-Standard Answers (with End-to-End Project Playbook)


## Table of Contents

- [Core Agent Patterns](#core-agent-patterns)
- [50 Interview Questions + Gold-Standard Answers](#50-interview-questions--gold-standard-answers)
  - [1) Foundations](#1-foundations-q1q10)
  - [2) Memory & RAG](#2-memory--rag-q11q20)
  - [3) Tool Use, Routing & Execution](#3-tool-use-routing--execution-q21q30)
  - [4) Multi-Agent Orchestration](#4-multi-agent-orchestration-q31q40)
  - [5) Reliability, Safety, Cost & Evaluation](#5-reliability-safety-cost--evaluation-q41q50)
- [How to Run an End-to-End GenAI/AI Project with Minimal Requirements](#how-to-run-an-end-to-end-genaiai-project-with-minimal-requirements)
  - [Phase 0: Clarify the Ask](#phase-0-clarify-the-ask)
  - [Phase 1: Define MVP + Success Metrics](#phase-1-define-mvp--success-metrics)
  - [Phase 2: Data + Knowledge Strategy](#phase-2-data--knowledge-strategy)
  - [Phase 3: Architecture & Component Design](#phase-3-architecture--component-design)
  - [Phase 4: Build Plan (Full-Stack + AI)](#phase-4-build-plan-full-stack--ai)
  - [Phase 5: Evaluation & Safety](#phase-5-evaluation--safety)
  - [Phase 6: Deployment & Observability](#phase-6-deployment--observability)
  - [Phase 7: Iteration, Governance, and Scale](#phase-7-iteration-governance-and-scale)
  - [Reference Tech Stack (Python + TypeScript + AWS/Azure)](#reference-tech-stack-python--typescript--awsazure)

---

## Core Agent Patterns

Most agentic interview questions fit one of these patterns. Use them to structure answers:

### Pattern A: **Understand → Plan → Retrieve → Act**
1. **Understand** the user goal + constraints  
2. **Plan** steps (task decomposition)  
3. **Retrieve** knowledge (RAG/memory) when needed  
4. **Act** via tools/APIs  
5. (Often) **Validate** results and **loop** until done

### Pattern B: **Tool Selection → Execution → Validation**
1. Choose the correct tool  
2. Execute with schema-validated inputs  
3. Validate outputs; retry/fallback if needed

### Pattern C: **Single Agent → Multi-Agent → Orchestrator**
- Start with one agent, then split into specialized agents (planner/researcher/executor/critic)
- Use an orchestrator (graph/state machine) to coordinate flow and retries

### Pattern D: **RAG → Validated RAG → Tool-Driven RAG**
- Basic retrieval → add relevance checks → ground answers via deterministic tools (SQL/APIs)

---

## 50 Interview Questions + Gold-Standard Answers

### 1) Foundations (Q1–Q10)

**Q1. What is an agent in Agentic AI?**  
**A.** An agent is a system that can **interpret a goal**, **plan**, **use tools**, **track state**, and **iterate** (plan → act → observe → adjust) until completion. Compared to a plain chatbot, an agent is designed to *take actions*, not just generate text.

**Q2. What’s the difference between an LLM and an agent?**  
**A.** An LLM generates a response from context. An agent adds: **planning**, **tool calls**, **memory/state**, **execution loops**, and often **validation**. The agent uses the LLM as a reasoning component inside a controlled workflow.

**Q3. What is planning in agent systems?**  
**A.** Planning is decomposing a goal into smaller, executable steps with dependencies and stopping conditions. In production, planning is constrained (finite steps, allowed tools, safe actions).

**Q4. Name typical components of an agentic system.**  
**A.** Common components: input interpreter, planner, tool router, retriever (RAG), executor, validator/critic, memory/state store, and an orchestrator controlling transitions, retries, and timeouts.

**Q5. What is an agent execution loop?**  
**A.** A repeated cycle: **plan → act → observe → re-plan**, continuing until success, failure, or a max-steps limit. Loops must be bounded to avoid infinite retries and cost explosions.

**Q6. Explain Understand → Plan → Retrieve → Act with an example.**  
**A.** For “automate customer support”: understand issue type; plan steps (fetch customer record, find policy, draft response); retrieve KB articles; act (create ticket, send email); validate response and log outcome.

**Q7. Why do interviews emphasize clarity over deep expertise?**  
**A.** Agentic AI is evolving quickly. Interviewers typically want to see whether you can articulate a correct workflow, choose tools appropriately, and reason about reliability, safety, and evaluation—more than framework trivia.

**Q8. What is “agent orchestration”?**  
**A.** Orchestration is controlling the order of steps, state transitions, tool calls, retries, and branching across components/agents. A graph/state-machine approach makes it predictable and observable.

**Q9. What is “tool calling”?**  
**A.** Tool calling lets the model request deterministic functions (APIs/DB queries/actions). A safe system validates tool inputs, enforces permissions, and logs calls for auditability.

**Q10. Why do agentic systems fail in practice?**  
**A.** Common reasons: unclear goals, weak retrieval grounding, hallucinated tool arguments, unbounded loops, poor validation, brittle tool integrations, missing observability, and lack of evaluation against realistic tasks.

---

### 2) Memory & RAG (Q11–Q20)

**Q11. What is short-term memory?**  
**A.** Ephemeral context for the current run: user messages, intermediate results, current plan/state. Usually stored in the workflow state and/or conversation context.

**Q12. What is long-term memory?**  
**A.** Persisted information across sessions: user preferences, past tasks, organizational knowledge, summaries, embeddings. Implemented via databases and/or vector stores.

**Q13. When do you use long-term vs short-term memory?**  
**A.** Short-term for the current task’s reasoning and steps; long-term for personalization and knowledge recall across sessions (with access control and privacy constraints).

**Q14. What is RAG?**  
**A.** Retrieval-Augmented Generation: the system retrieves relevant external context (documents/snippets) and supplies it to the LLM to produce a grounded answer.

**Q15. What is “validated RAG”?**  
**A.** A RAG pipeline that checks retrieval quality (relevance, recency, duplication, source trust) before the LLM finalizes an answer.

**Q16. What is “tool-driven RAG”?**  
**A.** Instead of relying on text retrieval alone, the system uses deterministic tools (SQL, APIs) to fetch canonical data, reducing hallucination risk for factual answers.

**Q17. How do you integrate RAG into multi-step workflows?**  
**A.** Retrieval becomes a step in the plan, typically before drafting an answer or deciding an action. In multi-agent systems, a dedicated “research/retrieval agent” can handle it.

**Q18. What retrieval pitfalls do you watch for?**  
**A.** Stale or irrelevant docs, chunking errors, missing metadata, over-retrieval (noise), embedding mismatch, and prompt leakage that causes the LLM to ignore evidence.

**Q19. How do you store memory safely?**  
**A.** Store only what’s needed, partition per user/tenant, enforce RBAC, encrypt at rest/in transit, set retention rules, and avoid storing secrets. Consider redaction/PII detection.

**Q20. How do you evaluate RAG quality?**  
**A.** Evaluate retrieval (precision/recall@k), context relevance, groundedness of answers, and end-task success. Use test sets with known answers, plus human review for critical paths.

---

### 3) Tool Use, Routing & Execution (Q21–Q30)

**Q21. When should the agent use a tool vs. the LLM alone?**  
**A.** Use tools for real-time facts, deterministic operations, state changes, and sensitive actions requiring control. Use the LLM for interpretation, summarization, planning, and natural language generation.

**Q22. What is tool routing?**  
**A.** Deciding which tool to call (and with what arguments). Routing can be rule-based, LLM-based, or hybrid. Hybrid typically validates LLM suggestions before execution.

**Q23. What is schema validation for tool calls?**  
**A.** Enforcing strict input types/constraints (e.g., JSON schema, Pydantic in Python, Zod in TypeScript). Reject or correct invalid calls before hitting external systems.

**Q24. How do you prevent hallucinated tool calls?**  
**A.** Maintain a strict tool registry, require schema validation, disallow unknown tools, add guardrails/critics for tool selection, and bound retries.

**Q25. How do you design tools for reliability?**  
**A.** Idempotent writes, clear error semantics, timeouts, retries with backoff, circuit breakers, and structured outputs. Tools should be small and single-purpose.

**Q26. How do you handle partial failures in multi-step tool workflows?**  
**A.** Use compensating actions when safe, store checkpoints, and design steps to be idempotent. If risk is high, require human approval before irreversible actions.

**Q27. How do you ensure the agent doesn’t spam APIs?**  
**A.** Rate limiting, caching, bounded loops, max tool calls per run, and observability metrics. The orchestrator enforces budgets and stops runaway executions.

**Q28. What is “validation” after tool execution?**  
**A.** Checking the tool result matches expectations: schema, business rules, cross-checks, and confidence thresholds. If validation fails, retry with constraints or fallback.

**Q29. How do you log tool calls safely?**  
**A.** Structured logs with request IDs, timestamps, tool name, status, latency; redact sensitive data; store audit trails with least-privilege access.

**Q30. What is a good fallback strategy?**  
**A.** Retry (bounded), alternate tool/source, ask user for clarification, degrade gracefully (read-only mode), or escalate to a human review step.

---

### 4) Multi-Agent Orchestration (Q31–Q40)

**Q31. What is a multi-agent system?**  
**A.** Multiple specialized agents collaborate on a task (e.g., planner, researcher, coder, validator). Coordination is managed by an orchestrator.

**Q32. When should you use multiple agents?**  
**A.** When tasks have clear sub-roles, you need a critic/reviewer for reliability, or the domain demands different tool access and prompts per responsibility.

**Q33. What are downsides of multi-agent systems?**  
**A.** Increased latency/cost, coordination complexity, harder debugging, and more failure modes. Start simple; add agents only when it improves reliability or modularity.

**Q34. What is an orchestrator?**  
**A.** A controller (often a graph/state machine) that routes messages, triggers tool calls, and enforces constraints (max steps, approvals, retries).

**Q35. Describe a common 3-agent pattern.**  
**A.** Researcher retrieves evidence; Writer composes output; Critic checks groundedness, structure, and policy compliance. Orchestrator loops until the critic approves.

**Q36. How do you prevent agents from looping or “arguing”?**  
**A.** Deterministic transitions, max-turn limits, explicit stopping criteria, and a single authoritative orchestrator that controls progression and termination.

**Q37. What is hierarchical delegation?**  
**A.** A manager/planner agent assigns subtasks to worker agents, evaluates their results, and merges outputs into a final response.

**Q38. How do you handle conflicting agent outputs?**  
**A.** Use a validator to compare evidence, require citations/structured reasoning, and fall back to deterministic tools for disputed facts.

**Q39. How do you parallelize safely?**  
**A.** Parallelize independent retrieval/tool calls, then join results. Ensure shared state is consistent (transaction IDs, optimistic concurrency, or immutable state snapshots).

**Q40. What are “planning nodes” and “execution nodes”?**  
**A.** Planning nodes create or update the plan; execution nodes run tools/steps. Keeping them separate improves reliability and observability.

---

### 5) Reliability, Safety, Cost & Evaluation (Q41–Q50)

**Q41. How do you evaluate an agent?**  
**A.** Task success rate, groundedness, tool correctness, latency, cost per task, and failure types. Use offline test suites and, if applicable, online A/B testing.

**Q42. What is a “hallucination cascade”?**  
**A.** A single incorrect assumption leads to a wrong plan and multiple wrong actions. Mitigated by retrieval grounding, validation gates, and deterministic tools.

**Q43. How do you reduce hallucinations?**  
**A.** Ground answers with RAG/tool-driven data, require evidence for claims, add critic validation, constrain tool calls, and use refusal/clarification for uncertain cases.

**Q44. What safety controls do you implement for tool-using agents?**  
**A.** Least privilege tool scopes, approval checkpoints for risky actions, input sanitization, output filters, PII redaction, and detailed audit logs.

**Q45. How do you control costs in agentic systems?**  
**A.** Limit steps/tool calls, use smaller models for routing/summarization, cache retrieval results, parallelize where safe, and enforce token/latency budgets.

**Q46. What observability is important?**  
**A.** Traces across nodes, tool call latency/error rates, token usage, step counts, success/failure reasons, and user feedback signals.

**Q47. What does “idempotency” mean and why does it matter?**  
**A.** Repeating a request has the same effect as doing it once. This is essential for retries in distributed tool workflows to prevent duplicate writes.

**Q48. How do you test agents reliably?**  
**A.** Deterministic mocks for tools, fixed test corpora, golden outputs, property-based tests for tool inputs, and regression suites for previously failing cases.

**Q49. What is human-in-the-loop (HITL)?**  
**A.** A workflow checkpoint where a human approves or edits decisions, especially before irreversible actions (payments, deletions, notifications to customers).

**Q50. Give an end-to-end example: customer support agent.**  
**A.** Understand issue → plan steps → retrieve policy docs/ticket history → call CRM/ticket tools → draft response → validate groundedness & safety → update ticket → store summary in memory → return response.

---

# How to Run an End-to-End GenAI/AI Project with Minimal Requirements

Below is a practical playbook for when a manager assigns a project with little detail. This avoids “hallucinating requirements” by turning ambiguity into a structured discovery process.

## Phase 0: Clarify the Ask

**Goal:** Convert a vague request into a clear problem statement.

**Actions:**
- Identify the **primary user** and **core job-to-be-done**
- Capture assumptions explicitly (and mark them as assumptions)
- Ask for constraints: timeline, budget, risk tolerance, data access
- Define what “done” means

**Output (1 page):**
- Problem statement
- Users/personas
- Constraints
- Risks
- Success criteria (initial)

---

## Phase 1: Define MVP + Success Metrics

**Goal:** Pick the smallest useful system you can ship.

**MVP definition:**
- 1–2 core user flows
- 1–2 data sources
- Clear “happy path” and “failure path”

**Metrics:**
- Task success rate (primary)
- Latency target (p95)
- Cost per successful task
- Safety metrics (e.g., PII leakage rate, unsafe tool calls)

**Deliverable:**
- MVP scope + acceptance criteria
- What’s explicitly out of scope

---

## Phase 2: Data + Knowledge Strategy

**Goal:** Decide what knowledge the system needs and how to retrieve it safely.

**Questions:**
- Is the knowledge **static** (docs) or **dynamic** (DB/APIs)?
- Do we need RAG? If yes:
  - Document formats, chunking strategy, metadata (source, date, owner)
  - Retrieval method (vector search + filters)
- Do we need tool-driven grounding (SQL/APIs) for canonical truth?

**Deliverable:**
- Knowledge map (sources + owners + refresh cadence)
- Data access and permissions plan

---

## Phase 3: Architecture & Component Design

**Goal:** Choose the right architecture for reliability.

### Choose one of these patterns (start simple):
- **Chat + RAG** (lowest complexity)
- **Single agent with tools** (moderate complexity)
- **Graph-based agent** (high reliability, bounded loops)
- **Multi-agent** (only if needed)

### Recommended baseline architecture (production-minded):
- **Frontend:** TypeScript (React/Next.js) or simple web UI
- **Backend:** Python (FastAPI) or TypeScript (Node) API layer
- **LLM integration:** model gateway + prompt templates + tool registry
- **Retrieval:** vector store + metadata filters
- **Memory:** short-term state + long-term store (optional)
- **Observability:** logs + traces + metrics
- **Security:** auth, RBAC, prompt/tool guardrails

**Deliverable:**
- System diagram (boxes + arrows)
- Data flow diagram (what data moves where)
- Threat model (high-level)

---

## Phase 4: Build Plan (Full-Stack + AI)

**Goal:** Implement the system incrementally with testability.

### Step 1: Skeleton API
- Create `POST /chat` (or `/agent/run`)
- Add request IDs and structured logging
- Define tool schemas and tool registry (even if empty)

### Step 2: Add Retrieval (if needed)
- Ingest documents
- Chunk + embed + index
- Add `retrieve(query) -> contexts`
- Add citations into responses (or at least keep doc IDs)

### Step 3: Add Tools
- Create small tools with strict schema:
  - read-only tools first
  - write tools only with guardrails/approvals
- Add validation and timeouts

### Step 4: Add Orchestration
- Start with simple: single-pass plan + execute
- Upgrade to graph/state machine if needed:
  - bounded loops
  - retry policies
  - fallback and HITL checkpoints

### Step 5: Frontend
- Minimal UI: input box, results, citations, tool actions (if any)
- Add “trace view” for debugging (optional but great for demos)

**Deliverable:**
- Working MVP with one end-to-end flow

---

## Phase 5: Evaluation & Safety

**Goal:** Prove it works and won’t do unsafe things.

### Evaluation checklist
- Task success tests (goldens)
- Retrieval relevance tests
- Tool correctness tests (with mocks)
- Regression tests for known failures

### Safety checklist
- PII detection/redaction if required
- Prompt injection defenses:
  - separate system/developer instructions from retrieved text
  - treat retrieved docs as untrusted
- Tool permission scoping and allowlists
- Human approval for irreversible actions

**Deliverable:**
- Evaluation report + known limitations
- Safety gates documented

---

## Phase 6: Deployment & Observability

**Goal:** Make it operable and monitorable.

### Deployment options (generic)
- **Containerize** (Docker) the backend
- Deploy to:
  - AWS: Lambda (serverless), ECS/Fargate, or EKS
  - Azure: Functions, Container Apps, AKS
- Store secrets in a managed secret store
- Add CI/CD:
  - lint, tests, build, deploy

### Observability
- Tracing across agent steps (node-by-node)
- Tool call metrics (latency, errors)
- Token usage + cost estimates
- User feedback and failure tracking

**Deliverable:**
- Runbook + dashboards + alerts

---

## Phase 7: Iteration, Governance, and Scale

**Goal:** Improve quality and expand safely.

- Add more tools and sources gradually
- Add caching and batching to cut cost/latency
- Expand test suite as new failures appear
- Implement model/version governance:
  - prompt versioning
  - tool contract versioning
  - rollout strategy (A/B or staged)

**Deliverable:**
- Roadmap + operational maturity plan

---

## Reference Tech Stack (Python + TypeScript + AWS/Azure)

This is a generic “safe default” set of tools that maps to common modern stacks:

### Backend (API + Agent Runtime)
- **Python:** FastAPI, Pydantic, httpx, asyncio
- **TypeScript:** Node.js, zod, undici/axios

### Retrieval / RAG
- Vector DB options: FAISS (local), OpenSearch, Pinecone, pgvector
- Embeddings: choose a supported embedding model for your platform
- Document loaders: PDF/DOCX/PPTX parsers + chunking utilities

### Orchestration / Agent Graph
- Graph/state machine approach (framework-agnostic):
  - nodes: plan, retrieve, tool_call, validate, respond
  - bounded retries + timeouts

### Frontend
- React/Next.js, TypeScript
- Simple trace viewer (optional)

### Cloud Deployment
- **AWS:** Lambda + API Gateway, ECS/Fargate, EKS
- **Azure:** Functions, Container Apps, AKS
- Storage: S3/Azure Blob
- Secrets: Secrets Manager/Key Vault
- Observability: CloudWatch/App Insights + OpenTelemetry

### CI/CD
- GitHub Actions:
  - unit tests
  - lint/format
  - build docker image
  - deploy

---

## Closing Notes (Anti-Hallucination / Anti-Guessing)

When requirements are vague, the biggest risk is “inventing constraints.” A reliable approach:
- Makes assumptions explicit
- Validates with stakeholders early
- Uses evidence-based evaluation (tests and metrics)
- Adds safety gates before write actions
- Instruments everything for debugging and accountability

