---
created_at: '2026-07-21T16:29:51.969600Z'
entities:
- LangChain
- current project (unnamed)
id: 01KY2R68Z138H5Q0Q9NVYJ74QJ
language: en
source:
  end_turn: 0
  session_id: 01KY2R4XKT5ZGD8FNHZ4T4C494
  start_turn: 0
tags:
- decision
- tooling
- langchain
- dependencies
- project-planning
title: 'Decision: do not use LangChain for the current project'
type: decision
---

I decided not to use LangChain for the current project. The choice is explicit: LangChain will not be adopted as a dependency or orchestration layer for the work I'm doing on this project. The brief original note used the phrase "save that," which is ambiguous; at minimum it confirms a negative decision about LangChain, but I still need to clarify whether that excludes every LangChain component or only its high-level orchestration features.

Implications and immediate actions I should take: update the project's dependency list and architecture notes to remove LangChain, inform any collaborators of this constraint, and run a dependency audit to ensure no transitive imports of LangChain remain. I need to pick alternatives for functionality I might have otherwise used LangChain for (prompt management, chains, tool routing, retrievers). If I plan to reimplement similar features, I should specify scope (simple SDK calls, small custom utilities, or another library) and estimate the implementation cost versus reintroducing an external framework.

Open questions to resolve: Do I want to allow inspiration from LangChain patterns (reimplemented locally) or ban any code derived from its patterns? Are there specific LangChain features I might still accept? Who else on the team needs to be notified? Next concrete steps: (1) clarify the meaning of "save that" and document the exact constraint, (2) list required features and evaluate lightweight alternatives, (3) update project docs and notify stakeholders.