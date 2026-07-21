---
created_at: '2026-07-21T16:21:23.554195Z'
entities:
- hexagonal architecture
- ports and adapters
- LLM
- vector database
- SQL
- event sourcing
- message broker
id: 01KY2QPRF25CBMRSWEQA1CF33D
language: en
source:
  end_turn: 2
  session_id: 01KY2QMQK6BHQ9AZCK7H30NRG0
  start_turn: 0
tags:
- architecture
- hexagonal-architecture
- agent
- ports-and-adapters
- testing
- observability
- adapters
title: 'Decision: use hexagonal (ports & adapters) architecture for agentic system'
type: decision
---

Decision: build the agentic system using hexagonal architecture (ports & adapters). The agent core will be the pure domain: intentions, belief/state model, action selection logic (policy/planner), memory access logic and the reasoning loop. The core must not perform network, file I/O, or direct hardware calls; it consumes immutable perception events and returns high-level actions or queries.

Defined ports (interfaces) to implement: Perception (ingest sensory events/messages, normalized DTOs with timestamps and provenance); Action (emit high-level commands, device-agnostic); Memory (abstract store for episodic/semantic memory and retrieval); Planning/Policy (optional port to treat planners as swappable adapters); Observation/Telemetry (traces, logs, explainability hooks). Design ports as versioned interfaces so adapters can evolve safely.

Adapters (concrete integrations): Sensor adapters (translate raw inputs → perception DTOs); Actuator adapters (translate high-level commands → device/API calls with retries, throttling, auth, and hard-stop enforcement); Model adapters (LLMs/ML models exposing a uniform interface so providers can be swapped or mocked); Storage adapters (SQL, vector DB, or file-based replay with deterministic replay capability); Human adapter (human-in-the-loop flows presented like other adapters).

Event loop and runtime: use an explicit event-driven loop or message broker; make messages idempotent and self-describing; core treats perceptions as immutable events and performs no side effects. Adapters handle retries, circuit breakers, rate-limits, and return sanitized success/failure signals to the core.

Testing and observability: unit-test core with fake adapters and mock LLMs; run integration tests with simulated sensors and test DBs; run replay tests using recorded perception streams to validate deterministic behavior across planner/LLM changes. Standardize a trace/event schema to reconstruct decisions and surface intermediate reasoning steps (memory queries, candidate scoring) via the telemetry port.

Design patterns and operational notes: consider adapter-as-a-service, command pattern for actions (queue/retry/undo), strategy pattern for runtime planner swaps, and replayable event-sourcing for determinism. Keep adapters thin/stateless where possible and move long-lived state into the memory port.

Open questions / next steps: define the minimal core responsibilities precisely; classify integrations as ephemeral vs long-lived; decide required offline testability/replay fidelity; decide if hot-swapping planners/LLMs at runtime is needed; pick the implementation tech stack and sketch component diagrams or minimal interfaces (TypeScript/Go/Python).