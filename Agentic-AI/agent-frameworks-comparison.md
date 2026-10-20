# CrewAI vs. LangGraph vs. Pydantic AI

Reference notes based on official documentation reviewed October 19, 2026.

## Are they in the same category?

Yes. All three are frameworks for building AI agents and agent workflows. They overlap, but emphasize different abstractions. They are not LLMs: you connect them to a model provider or a compatible local model.

| Framework | Main question it helps answer | Core abstractions |
|---|---|---|
| **CrewAI** | How do I organize agents into a team and coordinate their tasks? | Agents, roles, tasks, crews, flows |
| **LangGraph** | How do I control execution and shared state across a workflow? | State, nodes, edges, routing, checkpoints, interrupts |
| **Pydantic AI** | How do I build agents with clear Python types and validated data contracts? | Agents, typed tools, dependencies, structured outputs, validators |

These are differences in emphasis, not exclusive capabilities. CrewAI Flows support state and conditional execution. Pydantic AI supports multi-agent delegation and graph orchestration. LangGraph supports single-agent and multi-agent applications.

## Differences and tradeoffs

| Framework | Especially useful when | Main tradeoff |
|---|---|---|
| **CrewAI** | Work naturally divides into specialist roles, such as researcher, analyst, and reviewer | Team and task abstractions may add overhead when execution needs a very specific custom pattern |
| **LangGraph** | Branching, loops, persistent state, human approval, and recovery are central requirements | More explicit design work for state, transitions, and execution behavior |
| **Pydantic AI** | An agent must integrate cleanly with a Python backend and return structured business objects | Complex workflow control still needs deliberate orchestration using application code, graphs, or another runtime |

No framework automatically guarantees reliable outputs, secure tool use, or correct business decisions. Those require application design, evaluation, and operational controls.

## One use case implemented three ways

Consider a maintenance notification assistant that retrieves equipment information, drafts a notification, validates it, requests engineer approval, and submits it to SAP.

### CrewAI: organize the specialists

- Define an equipment researcher, notification writer, and reviewer.
- Give each agent tasks and tools.
- Use a Flow to coordinate the work and approval process.

The central design question is: **Who does each job?**

### LangGraph: define the execution path

- Implement equipment lookup, drafting, validation, approval, and submission as nodes.
- Use conditional edges to return incomplete drafts for revision.
- Configure checkpointing and interrupts to pause for approval and resume later.
- Keep SAP submission behind explicit approval and make writes safe to retry.

The central design question is: **What executes next, and what state does it need?**

A node can contain ordinary Python, an API call, or an agent. Not every workflow step needs an LLM.

### Pydantic AI: define the agent's contracts

- Define tools for equipment lookup.
- Define a structured output model such as `MaintenanceNotification`.
- Supply services through typed dependencies.
- Validate outputs and coordinate approval and submission through application code or a graph.

The central design question is: **What can the agent call, and what must it return?**

Schema validation checks structure and declared constraints. It does not prove that equipment identification or a maintenance recommendation is factually correct.

## What to use when

The following are architecture recommendations, not hard limits of the frameworks.

| Situation | Starting choice | Why |
|---|---|---|
| Research, analysis, and report generation with specialist roles | CrewAI | Crew and task abstractions match the work |
| Enterprise workflow with approval, revision loops, and persistent state | LangGraph | Explicit execution control is central |
| Backend agent calling tools and returning a validated business object | Pydantic AI | Typed interfaces simplify integration |
| Straightforward extraction or summarization | Direct model SDK plus Pydantic may suffice | A full agent framework may add little value |

### Recommendation for existing LangGraph applications

Keep LangGraph when the existing system benefits from routing, validation loops, business rules, and human decisions. Switching frameworks should address a concrete limitation rather than follow popularity.

Explore Pydantic AI by implementing one small agent that returns a validated maintenance notification. It can also run inside a LangGraph node, although combining frameworks adds dependencies and integration work.

Use CrewAI when its specialist-team model makes the application easier to build and maintain.

## Are they free?

The core CrewAI, LangGraph, and Pydantic AI libraries are open source under the MIT license. They can be used for personal and commercial applications without a framework subscription, subject to the license terms, including retaining required notices.

| Component | Cost consideration |
|---|---|
| Core framework libraries | No framework license fee |
| LLM API calls | Model-provider usage charges may apply |
| Hosting and infrastructure | Compute, databases, storage, and networking may cost money |
| Optional managed products | Separate pricing and terms may apply |
| Local models | Can avoid API charges, but still require hardware and compute; model licenses vary |

For example, self-hosting LangGraph with AWS Bedrock means paying for Bedrock and the AWS infrastructure used by the application. The open-source LangGraph library itself adds no license fee.

## Pydantic vs. Pydantic AI

- **Pydantic** provides data validation and serialization using Python type hints.
- **Pydantic AI** provides an agent framework built around typed tools, dependencies, and outputs.
- Using a Pydantic model in LangGraph does **not** mean the application uses Pydantic AI.

## Which one do you choose for your agentic AI tasks?

> I choose based on execution control, agent collaboration, and data contracts. LangGraph emphasizes stateful orchestration, CrewAI emphasizes role-based teams and flows, and Pydantic AI emphasizes typed agent development. I then assess recovery, approvals, observability, evaluation, and integration requirements against the actual use case.

## Official references

- [CrewAI Crews](https://docs.crewai.com/en/concepts/crews)
- [CrewAI Flows](https://docs.crewai.com/en/concepts/flows)
- [CrewAI repository and license](https://github.com/crewAIInc/crewAI)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph repository and license](https://github.com/langchain-ai/langgraph)
- [Pydantic AI documentation](https://ai.pydantic.dev/)
- [Pydantic AI repository and license](https://github.com/pydantic/pydantic-ai)

Features and commercial offerings evolve. Check the official documentation and licenses before adopting a specific release.
