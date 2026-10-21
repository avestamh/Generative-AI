# Agentic AI / GenAI Interview Prep: 80 Questions + Practical Answers (with End-to-End Project Playbook)


Reviewed: **October 20, 2026**. Answers describe engineering tradeoffs, not universal guarantees. Framework/API status is date-sensitive; official references appear alongside version-sensitive guidance. The existing filename is retained to preserve inbound links.

Use this guide by answering each question aloud, then adding a concrete example, a failure mode, and how you would measure success. Q1–Q50 cover agent systems; Q51–Q80 extend GenAI fundamentals and current production topics.

## Table of Contents

- [Core Agent Patterns](#core-agent-patterns)
- [80 Interview Questions + Practical Answers](#80-interview-questions--practical-answers)
  - [1) Foundations](#1-foundations-q1q10)
  - [2) Memory & RAG](#2-memory--rag-q11q20)
  - [3) Tool Use, Routing & Execution](#3-tool-use-routing--execution-q21q30)
  - [4) Multi-Agent Orchestration](#4-multi-agent-orchestration-q31q40)
  - [5) Reliability, Safety, Cost & Evaluation](#5-reliability-safety-cost--evaluation-q41q50)
  - [6) GenAI Fundamentals and Adaptation](#6-genai-fundamentals-and-adaptation-q51q60)
  - [7) Context, Retrieval and Interoperability](#7-context-retrieval-and-interoperability-q61q70)
  - [8) Production Design and Current Tooling](#8-production-design-and-current-tooling-q71q80)
- [Tooling Status and Migration Notes](#tooling-status-and-migration-notes)
- [Official References](#official-references)
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

### Pattern C: **Choose the simplest control structure**

- Compare a fixed workflow, one tool-using agent, and delegated workers against the same task suite.
- Use explicit transitions, permissions, and budgets where needed. Orchestration applies to single-agent and multi-agent designs; additional agents are not an automatic upgrade.

### Pattern D: **Retrieve evidence → Check support → Query live state**

- Choose document retrieval or live SQL/APIs based on the question; combine them when useful.
- “Validated RAG” and “tool-driven RAG” are descriptive labels here, not mandatory stages or standard maturity levels.

---

## 80 Interview Questions + Practical Answers

### 1) Foundations (Q1–Q10)

**Q1. What is an agent in Agentic AI?**  
**A.** An agent is a system in which a model selects actions or tools and adapts subsequent steps using observations to pursue a goal. Explicit planning, retrieval, persistent memory, and multiple agents are optional design choices. A fixed sequence containing an LLM is usually better described as a workflow. See [agent/workflow distinctions](https://www.anthropic.com/research/building-effective-agents).

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

**Q7. When should you use a workflow instead of an autonomous agent?**  
**A.** Use a predefined workflow when steps, rules, and success conditions are known, such as validating an invoice and routing it for approval. Use an agent when the next step depends on information discovered during execution. Compare both against a simple baseline; flexibility must justify additional latency, cost, and failure modes.

**Q8. What is “agent orchestration”?**  
**A.** Orchestration is controlling the order of steps, state transitions, tool calls, retries, and branching across components/agents. A graph/state-machine approach makes it predictable and observable.

**Q9. What is tool calling?**  
**A.** The model proposes a named operation and arguments; application code authorizes, validates, executes it, and returns the result under the matching call ID. Tools can be nondeterministic, stateful, or unavailable. A model requesting a tool does not prove that it ran or succeeded.

**Q10. Why do agentic systems fail in practice?**  
**A.** Common reasons: unclear goals, weak retrieval grounding, hallucinated tool arguments, unbounded loops, poor validation, brittle tool integrations, missing observability, and lack of evaluation against realistic tasks.

---

### 2) Memory & RAG (Q11–Q20)

**Q11. What is short-term memory?**  
**A.** Task- or thread-scoped messages, observations, and workflow state. Short-term describes scope, not necessarily storage durability: a production checkpointer can persist it across process restarts. It differs from the limited context actually sent to the model. See [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence).

**Q12. What is long-term memory?**  
**A.** Information retained across tasks or sessions, such as preferences and verified facts, stored in ordinary databases, files, or search indexes. Embeddings support lookup; they are not the memory itself. Define who may write, correct, retrieve, and delete each item.

**Q13. When do you use long-term vs short-term memory?**  
**A.** Short-term for the current task’s reasoning and steps; long-term for personalization and knowledge recall across sessions (with access control and privacy constraints).

**Q14. What is RAG?**  
**A.** Retrieval-Augmented Generation: the system retrieves relevant external context (documents/snippets) and supplies it to the LLM to produce a grounded answer.

**Q15. What is “validated RAG”?**  
**A.** A descriptive label for adding evidence checks to RAG, not a universally standardized architecture. Check retrieval relevance, freshness, provenance, and answer support. Relevant documents do not guarantee correct synthesis; evaluate whether each important claim follows from its cited evidence.

**Q16. How do retrieval and live tools complement each other?**  
**A.** Retrieve policies and explanatory documents; query scoped APIs or databases for current operational facts. “Tool-driven RAG” is an informal label for some such designs. A successful SQL/API response can still reflect stale data, a wrong query, or insufficient permissions, so validate its meaning and provenance.

**Q17. How do you integrate RAG into multi-step workflows?**  
**A.** Retrieval becomes a step in the plan, typically before drafting an answer or deciding an action. In multi-agent systems, a dedicated “research/retrieval agent” can handle it.

**Q18. What retrieval pitfalls do you watch for?**  
**A.** Parsing and OCR errors, stale documents, missing permissions, poor chunk boundaries, embedding/query mismatch, and irrelevant context. Distinguish missing evidence from generation errors. Treat retrieved instructions as untrusted data and apply tenant/access filters before context reaches the model.

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
**A.** Validate input types and structure using JSON Schema, Pydantic, or Zod. Then separately enforce business constraints, identity, ownership, permissions, and allowed destinations. Even schema-constrained generation can contain semantically wrong values; schema compliance is not authorization. See [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

**Q24. How do you prevent hallucinated tool calls?**  
**A.** Maintain a strict tool registry, require schema validation, disallow unknown tools, add guardrails/critics for tool selection, and bound retries.

**Q25. How do you design tools for reliability?**  
**A.** Idempotent writes, clear error semantics, timeouts, retries with backoff, circuit breakers, and structured outputs. Tools should be small and single-purpose.

**Q26. How do you handle partial failures in multi-step tool workflows?**  
**A.** Persist step status and operation IDs; retry only safe operations. A timeout after a write means its outcome may be unknown: query status or reuse the same idempotency key before resending. Use compensations where valid; some effects cannot be undone. Escalate unresolved outcomes rather than claiming success.

**Q27. How do you ensure the agent doesn’t spam APIs?**  
**A.** Rate limiting, caching, bounded loops, max tool calls per run, and observability metrics. The orchestrator enforces budgets and stops runaway executions.

**Q28. What is validation after tool execution?**  
**A.** Check response shape, operation status, and domain postconditions. For a ticket update, verify the intended ticket and fields actually changed. Use calibrated scores only where supported by evaluation; a model's verbal confidence is not a reliable probability. Distinguish safe read retries from potentially duplicating writes.

**Q29. How do you log tool calls safely?**  
**A.** Structured logs with request IDs, timestamps, tool name, status, latency; redact sensitive data; store audit trails with least-privilege access.

**Q30. What is a good fallback strategy?**  
**A.** Retry (bounded), alternate tool/source, ask user for clarification, degrade gracefully (read-only mode), or escalate to a human review step.

---

### 4) Multi-Agent Orchestration (Q31–Q40)

**Q31. What is a multi-agent system?**  
**A.** Multiple specialized agents collaborate on a task (e.g., planner, researcher, coder, validator). Coordination is managed by an orchestrator.

**Q32. When should you use multiple agents?**  
**A.** Consider them for independently executable subtasks, isolated context, or distinct trust/tool boundaries. Compare task success, cost, and latency with a single-agent baseline. A reviewer agent may share the same blind spots as the author, so extra agents alone do not establish correctness.

**Q33. What are downsides of multi-agent systems?**  
**A.** Increased latency/cost, coordination complexity, harder debugging, and more failure modes. Start simple; add agents only when it improves reliability or modularity.

**Q34. What is an orchestrator?**  
**A.** A controller (often a graph/state machine) that routes messages, triggers tool calls, and enforces constraints (max steps, approvals, retries).

**Q35. Describe a common three-agent pattern.**  
**A.** A researcher gathers evidence, a writer drafts, and a reviewer checks it against a rubric. Bound revision rounds and total budget; unresolved disputes go to a defined fallback. Check facts against source evidence or executable tests because a critic's approval is not a guarantee.

**Q36. How do you prevent agents from looping or “arguing”?**  
**A.** Deterministic transitions, max-turn limits, explicit stopping criteria, and a single authoritative orchestrator that controls progression and termination.

**Q37. What is hierarchical delegation?**  
**A.** A manager/planner agent assigns subtasks to worker agents, evaluates their results, and merges outputs into a final response.

**Q38. How do you handle conflicting agent outputs?**  
**A.** Compare source evidence, assumptions, timestamps, and reproducible checks. Ask for concise justifications and citations rather than private chain-of-thought. Voting is weak when agents share correlated errors. If evidence remains insufficient, expose the uncertainty or escalate according to task requirements.

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
**A.** Retrieve authoritative evidence, validate tool results, constrain outputs, and allow abstention when evidence is insufficient. Test citation support and factual accuracy separately. Critics and RAG reduce some errors but can also repeat misinformation; neither guarantees truth.

**Q44. What safety controls do you implement for tool-using agents?**  
**A.** Enforce authorization outside the model, least privilege, sandboxing, destination/egress restrictions, and risk-appropriate approvals. Treat documents, tool descriptions/results, and other-agent messages as untrusted inputs. Add audit trails and adversarial tests; text sanitization or a stronger prompt alone does not stop prompt injection.

**Q45. How do you control costs in agentic systems?**  
**A.** Enforce token, step, tool, and wall-clock budgets; measure cost per successful task. Evaluate smaller models, shorter context, and caching with freshness/access rules. Parallelism can reduce elapsed time while increasing total spend. Include retries, retrieval, judge calls, and infrastructure in the cost.

**Q46. What observability is important?**  
**A.** Traces across nodes, tool call latency/error rates, token usage, step counts, success/failure reasons, and user feedback signals.

**Q47. What does “idempotency” mean and why does it matter?**  
**A.** Repeating a request has the same effect as doing it once. This is essential for retries in distributed tool workflows to prevent duplicate writes.

**Q48. How do you test agents reliably?**  
**A.** Use deterministic unit tests for contracts and policies, sandbox integration tests for real tools, and repeated task-level evaluations for stochastic behavior. Grade outcomes and permitted state changes rather than requiring identical prose or one exact tool path. Keep held-out and adversarial cases separate from development examples.

**Q49. What is human-in-the-loop (HITL)?**  
**A.** A checkpoint where a person reviews or edits a proposed action. Present exact arguments, targets, and consequences; bind approval to that proposal and recheck permissions/preconditions on resume. Persist pending approvals and expire stale ones. A vague approval should not authorize a changed action.

**Q50. Give an end-to-end example: customer support agent.**  
**A.** Authenticate the user → classify the issue → retrieve authorized policy evidence → read current order status → draft an answer or proposed action → validate policy and permissions → obtain approval if required → perform an idempotent update → verify its result → report the outcome. Retain only necessary memory and audit data.

---

### 6) GenAI Fundamentals and Adaptation (Q51–Q60)

**Q51. How do pretraining, instruction tuning, and preference optimization differ?**  
**A.** Pretraining learns broad statistical patterns from large datasets. Supervised instruction tuning trains on task demonstrations; preference optimization uses comparisons or reward signals to favor desired responses. These stages improve different behaviors and do not guarantee factuality or application-specific correctness.

**Q52. What do tokens, context windows, and embeddings represent?**  
**A.** Tokens are model input/output units, not necessarily words. A context window bounds the sequence available for a model call, with input/output accounting depending on the API. Embeddings map inputs to vectors useful for similarity; they do not provide a truth score or guarantee semantic equivalence.

**Q53. How does self-attention help a language model?**  
**A.** Attention lets each position combine information from other allowed positions using learned query/key/value projections. Causal masking prevents access to future tokens during next-token prediction. Long contexts still have computation and quality costs; capacity to accept a document does not ensure reliable use of every detail.

**Q54. What do temperature and top-p control?**  
**A.** They change how output tokens are sampled: temperature rescales logits, while top-p restricts sampling to a cumulative-probability set. Low temperature does not guarantee determinism or factuality. Supported controls vary by model; tune them on task evaluations rather than assuming one setting works everywhere.

**Q55. When would you choose prompting, RAG, or fine-tuning?**  
**A.** Start with prompting for task specification. Use retrieval or tools for changing, private, or attributable knowledge. Consider fine-tuning for persistent behavior, format, or domain patterns when sufficient representative data exists. They can be combined; fine-tuning is not a substitute for access control or live knowledge.

**Q56. What are LoRA, QLoRA, and quantization?**  
**A.** LoRA trains small low-rank adapters while freezing base weights. QLoRA combines adapter training with a quantized base to reduce memory requirements. Quantization lowers numerical precision and can affect quality or hardware compatibility. Benchmark the deployed setup, including adapters and inference kernels. See [PEFT quantization](https://huggingface.co/docs/peft/en/developer_guides/quantization).

**Q57. How do SFT and preference methods such as DPO differ?**  
**A.** Supervised fine-tuning (SFT) learns from desired responses. Direct Preference Optimization (DPO) learns from chosen/rejected response pairs relative to a reference policy; RLHF approaches can instead train with a learned reward model. Data quality, coverage, and held-out evaluations matter more than choosing a fashionable acronym.

**Q58. What is knowledge distillation?**  
**A.** Train a student model using a teacher's outputs or other training signals to reproduce useful behavior at lower deployment cost. Filter incorrect teacher data and test difficult cases independently. Check data permissions, model terms, and whether savings outweigh training and maintenance costs.

**Q59. How do reasoning models change agent design?**  
**A.** They may improve difficult planning or problem solving by using additional inference computation. They still require grounded inputs, bounded execution, and external authorization. Compare task quality, latency, and total cost with simpler models; request concise explanations or verifiable artifacts rather than private chain-of-thought.

**Q60. What changes when inputs are multimodal?**  
**A.** Images, audio, and video introduce parsing, alignment, transcription/OCR, temporal context, and modality-specific failures. Preserve provenance such as page regions or timestamps. Test real input conditions, including blurry scans and noisy audio; instructions embedded in media remain untrusted data.

---

### 7) Context, Retrieval and Interoperability (Q61–Q70)

**Q61. What is context engineering?**  
**A.** It is selecting and maintaining the instructions, evidence, tools, history, and state supplied to each model call. Budget context for relevant information, load details when needed, and avoid redundant or conflicting material. Prompt wording is one part of that broader design. See [context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents).

**Q62. How do you manage long-running agent context?**  
**A.** Keep durable task state and artifacts outside the prompt; summarize older interaction while preserving constraints, decisions, source links, and pending actions. Retrieve details on demand and test whether compaction loses important information. A summary is a lossy view, so it should not become the sole record of permissions or completed writes.

**Q63. What are hybrid retrieval and reranking?**  
**A.** Hybrid retrieval combines lexical matching, useful for exact terms/IDs, with dense semantic retrieval. Fuse candidates and optionally rerank query-document pairs before selecting context. Measure retrieval recall, answer quality, and latency on your corpus; no fixed fusion method or top-k is optimal everywhere. See [contextual retrieval](https://www.anthropic.com/research/contextual-retrieval).

**Q64. How do you choose chunking and evaluate retrieval?**  
**A.** Respect document structure and keep enough local context for interpretation. Preserve source IDs, versions, and access metadata. Compare chunk sizes, overlap, and parent/child strategies using labeled queries; inspect recall@k and ranking quality such as MRR/nDCG. Diagnose parsing and retrieval separately from generation.

**Q65. Does a long context window make RAG obsolete?**  
**A.** No. Supplying complete small documents can be effective, while retrieval helps select relevant, current, authorized evidence from large corpora. Compare both on cost, latency, citation support, and answer accuracy. A long context window does not ensure the model attends to all evidence.

**Q66. When would you use agentic RAG or GraphRAG?**  
**A.** Agentic retrieval allows iterative query reformulation or source selection; GraphRAG uses graph relationships or summaries for connected information. Consider them when multi-hop questions or corpus-level synthesis defeat a simpler baseline. Include graph construction, freshness, latency, and added failure modes in the evaluation.

**Q67. What is MCP, and how does it relate to tool calling?**  
**A.** Model Context Protocol standardizes connections between a host application, its clients, and servers exposing capabilities such as tools and contextual resources. Tool calling is the model/application interaction; MCP can supply the integration layer. It does not replace an agent runtime or grant permission to act. See the [MCP specification](https://modelcontextprotocol.io/specification/latest).

**Q68. What security issues matter for MCP integrations?**  
**A.** Authenticate clients and enforce per-user scopes on the server; validate token audience rather than forwarding arbitrary bearer tokens. Review server provenance, tool changes, outbound destinations, and local process privileges. MCP connectivity is not a trust guarantee. See [MCP security practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices).

**Q69. How does A2A differ from MCP?**  
**A.** A2A supports interoperability between agents, including discovery and task-oriented communication. MCP primarily connects applications to tools and context. They can coexist: an agent may use MCP tools while collaborating through A2A. Authentication, permissions, and task lifecycle handling still belong in the implementation. See [A2A overview](https://a2a-protocol.org/latest/topics/what-is-a2a/).

**Q70. What are Agent Skills, and are they model training?**  
**A.** Agent Skills package task instructions in a SKILL.md file, with optional scripts, references, and assets loaded as needed. They add procedural context without changing model weights. Review executable content and apply the runtime's permission rules; installing a skill is not blanket authorization. See [Agent Skills](https://agentskills.io/home).

---

### 8) Production Design and Current Tooling (Q71–Q80)

**Q71. How do structured outputs differ from JSON mode and tool calling?**  
**A.** JSON mode targets valid JSON; schema-constrained output targets a supported schema. Tool calling expresses a proposed operation with arguments. They solve related but different interface problems. Handle refusals, truncation, and validation errors explicitly; correct structure does not establish true values. See [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

**Q72. What is durable execution, and does a checkpoint prevent duplicate actions?**  
**A.** Durable execution persists enough workflow state to resume after interruptions. A checkpoint alone cannot make an external side effect exactly once: a process may crash after the write but before recording it. Use stable operation IDs, idempotency keys, transactional boundaries where available, and reconciliation for uncertain outcomes.

**Q73. How do you evaluate outcomes versus trajectories?**  
**A.** Outcome grading checks the final answer or external state; trajectory grading inspects tool choices, permissions, intermediate errors, and unnecessary work. Accept multiple valid execution paths. Combine deterministic checks with rubric-based graders and human calibration; keep the grader and task environment versioned. See [agent evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

**Q74. What do pass@k and pass^k measure?**  
**A.** pass@k asks whether at least one of k attempts succeeds; pass^k asks whether all k succeed. Under an independent, equal-success-probability model with probability p, these are 1−(1−p)^k and p^k. State sampling assumptions and repeated-trial protocol; a best-of-many result is different from first-attempt reliability. See [evaluation metrics](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

**Q75. What can go wrong with an LLM-as-judge?**  
**A.** Judges can favor verbosity, position, or familiar styles and can be manipulated by candidate text. Use explicit rubrics, representative human-labeled calibration cases, blinded comparisons, and executable checks where possible. Track disagreement and grader drift; treat generated confidence as uncalibrated unless measured.

**Q76. How do you prevent cross-tenant leakage through RAG, memory, and caches?**  
**A.** Derive tenant/user scope from authenticated server context. Enforce authorization when reading sources, retrieving chunks, loading memory, and returning cached results. Include permission scope and relevant versions in cache keys, and invalidate on access/data changes. Test revoked access and identical queries from different tenants.

**Q77. What is an agent harness?**  
**A.** The runtime around a model that manages tools, permissions, state, context, budgets, execution, and verification. Model quality and harness quality interact, so evaluate the deployed combination. For long tasks, persist artifacts and progress, support cancellation/recovery, and verify actual results before reporting completion.

**Q78. How should you choose an agent framework today?**  
**A.** Start with required control flow, persistence, tool integration, provider support, deployment, and observability. A direct SDK loop may suffice. LangChain create_agent offers a higher-level agent interface; LangGraph supports explicit graph orchestration. Evaluate Microsoft Agent Framework where its ecosystem fits. Verify versions and maintenance rather than copying old tutorials. See the tooling notes below.

**Q79. How would you diagnose a slow, expensive agent?**  
**A.** Trace model time, tool latency, context size, retries, and redundant steps. Optimize the largest measured contributor: use narrower retrieval, fewer calls, calibrated model routing, safe caching, or independent-call parallelism. Rerun the same task suite and compare p95 latency and cost per successful task while checking quality and safety.

**Q80. Design an enterprise research assistant with citations and optional actions.**  
**A.** Clarify users, data sensitivity, allowed actions, and acceptance metrics. Begin with permission-filtered retrieval and source-linked answers, then add tools behind external policy checks. Persist task state, verify citations and action postconditions, and evaluate missing evidence, injected content, stale data, API failures, and revoked access. Roll out with measured success thresholds, monitoring, and rollback.

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
  - Retrieval method (lexical, dense, or hybrid search + permission filters; evaluate reranking)
- Do we need tool-driven grounding (SQL/APIs) for canonical truth?

**Deliverable:**
- Knowledge map (sources + owners + refresh cadence)
- Data access and permissions plan

---

## Phase 3: Architecture & Component Design

**Goal:** Choose the right architecture for reliability.

### Choose one of these patterns (start simple):

- **Fixed workflow or direct model call** (baseline when steps are known)
- **Chat + RAG** (when external document evidence is needed)
- **Single agent with tools** (moderate complexity)
- **Graph-based workflow/agent** (explicit transitions; reliability still depends on validation, persistence, and recovery)
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
- Preserve source/version IDs and answer citations; check that citations support claims
- Enforce source access before retrieval/context assembly and invalidate stale/deleted content

### Step 3: Add Tools

- Create small tools with strict schema:
  - read-only tools first
  - write tools only with guardrails/approvals
- Add server-side authorization, validation, timeouts, and stable operation IDs
- Reconcile unknown write outcomes before retrying; verify postconditions

### Step 4: Add Orchestration

- Start with simple: single-pass plan + execute
- Upgrade to graph/state machine if needed:
  - bounded loops
  - retry policies
  - fallback and HITL checkpoints

### Step 5: Frontend

- Minimal UI: input box, results, citations, tool actions (if any)
- Keep detailed traces behind developer permissions; show users concise progress and verified outcomes

**Deliverable:**
- Working MVP with one end-to-end flow

---

## Phase 5: Evaluation & Safety

**Goal:** Measure task quality and safety against explicit acceptance criteria, and document residual failure modes.

### Evaluation checklist

- Task success tests with outcome-based rubrics and repeated trials
- Held-out cases separate from development examples; compare with a simple baseline
- Retrieval relevance tests
- Tool correctness tests (with mocks)
- Regression tests for known failures

### Safety checklist

- PII detection/redaction if required
- Prompt injection defenses:
  - separate system/developer instructions from retrieved text
  - treat retrieved docs as untrusted
- Tool permission scoping and allowlists
- Risk-appropriate approval bound to the exact action/arguments; recheck authorization on resume
- Adversarial tests for injection, cross-tenant access, revoked permissions, and data exfiltration

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

- Tracing across agent steps with trace/run IDs and model, prompt, tool, and dataset versions
- Redacted payloads with retention/access controls; avoid recording secrets or private reasoning
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
  - rollout strategy (A/B or staged), rollback, and regression gates
  - dependency locks and official deprecation/changelog reviews
- Define cancellation, reconciliation, and incident response procedures

**Deliverable:**
- Roadmap + operational maturity plan

---

## Reference Tech Stack (Python + TypeScript + AWS/Azure)

These are example building blocks, not a mandatory stack. Select supported versions using workload evaluations, deployment constraints, and your team's operating experience.

### Backend (API + Agent Runtime)

- **Python:** FastAPI, Pydantic, httpx, asyncio
- **TypeScript:** Node.js, zod, undici/axios

### Retrieval / RAG

- Local similarity index: FAISS (access control, persistence, and serving need application support)
- Search/storage options: OpenSearch, Pinecone, or PostgreSQL with pgvector; choose by filtering, hybrid search, scale, and operations needs
- Embeddings: choose a supported embedding model for your platform
- Document loaders: PDF/DOCX/PPTX parsers + chunking utilities

### Orchestration / Agent Graph

- Start with a direct SDK workflow or tool loop; use a framework when its control/persistence features help.
- For current framework entry points and migration caveats, see [tooling status](#tooling-status-and-migration-notes).
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

## Tooling Status and Migration Notes

Reviewed **October 20, 2026**. These notes extend the original guide, which did not contain deprecated API code. They distinguish actual API migration from architectural choices that remain useful.

| Topic | Guidance | Official source |
| --- | --- | --- |
| LangChain agents | For LangChain v1, use `langchain.agents.create_agent`; the migration guide replaces `langgraph.prebuilt.create_react_agent`. Legacy chain APIs moved to `langchain-classic`. This is package/API evolution, not evidence that the ReAct pattern is obsolete. | [v1 migration](https://docs.langchain.com/oss/python/migrate/langchain-v1) |
| OpenAI Assistants API | Sunset August 26, 2026 and no longer available. Use Responses for new integrations; migrate from application-retained history following the official guide. This does not mean every other OpenAI API is deprecated. | [Assistants migration](https://developers.openai.com/api/docs/assistants/migration) |
| Microsoft ecosystem | Include Microsoft Agent Framework in new evaluations. Check supported language, feature, and migration documentation for your existing stack; do not assume every older AutoGen or Semantic Kernel component is obsolete. | [Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/) |
| MCP and A2A | Interoperability protocols complement runtimes. Pin/test compatible protocol and SDK versions and verify authorization behavior. They do not replace RAG, tools, or application policies. | [MCP](https://modelcontextprotocol.io/specification/latest), [A2A](https://a2a-protocol.org/latest/topics/what-is-a2a/) |
| RAG, fine-tuning, and multi-agent designs | None is universally obsolete. Choose by task evidence, update needs, cost, and operational complexity. Additional agents and larger contexts require measured justification. | See Q55, Q65–Q66, and Q78. |
| Models and dependencies | Record the exact model identifier, provider, supported capabilities, dependency lock, and evaluation date. Re-evaluate upgrades; avoid claims that one model or framework is always best. | Provider changelogs and package release notes for the deployed versions. |

## Official References

Use these to verify implementation details; examples and availability change over time.

- [Agent/workflow patterns](https://www.anthropic.com/research/building-effective-agents) — architectural foundations; its older tooling examples require current documentation.
- [Context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) and [contextual retrieval](https://www.anthropic.com/research/contextual-retrieval).
- [Agent evaluation](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).
- [LangChain v1 migration](https://docs.langchain.com/oss/python/migrate/langchain-v1) and [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence).
- [MCP specification](https://modelcontextprotocol.io/specification/latest) and [security practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices).
- [A2A overview](https://a2a-protocol.org/latest/topics/what-is-a2a/) and [Agent Skills](https://agentskills.io/home).
- [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) and [Assistants migration](https://developers.openai.com/api/docs/assistants/migration).
- [PEFT quantization and adapter training](https://huggingface.co/docs/peft/en/developer_guides/quantization).
- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/).

---

## Closing Notes (Anti-Hallucination / Anti-Guessing)

When requirements are vague, the biggest risk is “inventing constraints.” A reliable approach:
- Makes assumptions explicit
- Validates with stakeholders early
- Uses evidence-based evaluation (tests and metrics)
- Adds safety gates before write actions
- Instruments everything for debugging and accountability

