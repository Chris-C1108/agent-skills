---
name: ddd-modeling-suite
description: Interactive Domain-Driven Design (DDD) elicitation, reverse-engineering, and modeling suite. Combines cognitive-safe BA story probes (CIT, T-P-I-P-O-S-E, CRUDA, 0/1/N concurrency), 4-tier rule epistemology, strategic/tactical DMML v2 modeling (Aggregates, Policies, Sagas, CQRS Read Models), deterministic graph linting, and AGENTS.md constitution injection.
triggers:
  - ddd modeling
  - domain-driven design
  - bounded context
  - event storming
  - dmml
  - 领域建模
  - 限界上下文
  - 事件风暴
  - 聚合根设计
  - 需求深度挖掘
---

# DDD Modeling Suite (V2)

End-to-end methodology and deterministic harness for eliciting tacit domain knowledge, reverse-engineering legacy systems, assembling strategic/tactical DDD models (DMML v2), and enforcing architectural boundaries in `AGENTS.md`.

---

## Core Axioms & Guardrails

1. **Internal Schema vs. External Dialogue Separation**:
   - `FORBIDDEN: Interrogating humans with raw DDD/meta-model jargon (T-P-I-P-O-S-E, Aggregate, Idempotency) or dumping >3 questions per turn -> USE: Concrete story walkthroughs (Critical Incident Technique / Example Mapping) with <=3 multiple-choice anchored questions per turn.`
2. **4-Tier Epistemology & Chesterton's Fence**:
   - `FORBIDDEN: Discarding regulatory, audit, or safety rules merely because removing them does not immediately crash the happy path -> USE: Classify every rule into Tier 1 (Hard Invariant), Tier 2 (Compliance/Regulatory Gate), Tier 3 (Configurable Policy), or Tier 4 (UI Convention).`
3. **Iterative Thin-Slicing & Parking Lot**:
   - `FORBIDDEN: Blocking modeling progress when a stakeholder is uncertain about an edge case -> USE: Record unresolved items in .ddd/00-parking-lot.md with a safe TODO_ASSUMPTION tag and proceed with the active vertical slice.`
4. **Lossless Provenance Distillation**:
   - `FORBIDDEN: Passing raw conversational transcripts to downstream modeling subagents or stripping rule rationale during compaction -> USE: Distill into .ddd/02-events.yaml preserving fact_id, traces_to lineage, evidence_tier, rationale, and source_actor.`
5. **Contention-Based Aggregate Boundaries & CQRS Parity**:
   - `FORBIDDEN: Splitting low-contention or client-side entities into micro-aggregates solely on a mechanical 1-second delay rule, or forcing reporting queries into write aggregates -> USE: Size aggregates by atomic invariant contention and model queries as explicit Read Models.`

---

## 7-Phase Execution State Machine

All artifacts persist in `.ddd/` at the target repository root:

```text
[Phase 0: Charter & Scope]    ──► .ddd/00-context-charter.md & .ddd/00-parking-lot.md
        │
[Phase 1: BA / Legacy Probe]  ──► .ddd/01-raw-facts.md
        │
[Phase 2: Event Distillation] ──(compile_events.py)──► .ddd/02-events.yaml
        │
[Phase 3: Strategic Mapping]  ──► .ddd/03-context-map.md ──► [Human Gate 1]
        │
[Phase 4: Tactical Assembly]  ──(slice per Bounded Context)──► .ddd/04-models/*.yaml
        │
[Phase 5: Deterministic Lint] ──(dmml_linter.py)──► audit_passed ──► [Human Gate 2]
        │
[Phase 6: Constitution Sync]  ──► AGENTS.md (DDD-DOMAIN-CONSTITUTION block)
```

---

## Phase 0: Context Charter, Value Stream & Slice Selection

Before probing actions, align on scope in 1 turn:
1. Identify **Core Business Goal**, **Primary Actors**, and **Organizational Ownership (Conway Boundaries / RACI)**.
2. Select execution mode: **Thin Vertical Slice** (recommended for fast iteration) or **Full Domain Discovery**.
3. Initialize `.ddd/00-context-charter.md` and `.ddd/00-parking-lot.md`.

---

## Phase 1: Cognitive-Safe BA Elicitation & Legacy Reverse-Engineering

### 1. Greenfield / Stakeholder Elicitation
Load and follow `(probes/tpipeose-interrogation.md)` and `(probes/falsification-probe.md)`:
- Anchor on a concrete recent incident or user story first; extract **T-P-I-P-O-S-E** slots silently in the background.
- Probe full lifecycle (**CRUDA**: Create, Read/Projection, Update/Merge, Delete/Soft-delete, Archive/Compensate) and **0/1/N Cardinality & Concurrency Fractures**.
- Uncover **Shadow Workflows** (offline spreadsheets, manual overrides) without triggering defensive blame.

### 2. Brownfield / Legacy Code Reverse-Engineering
Load and follow `(probes/legacy-code-probe.md)`:
- `FORBIDDEN: Treating raw DDL tables or coarse @Transactional service methods as true aggregate boundaries -> USE: Audit actual state mutations, optimistic/pessimistic locks, and WHERE status guards while isolating God Transactions behind an Anti-Corruption Layer (ACL).`

**Deliverable**: Write structured fact blocks (`## [FACT-001] ...`) to `.ddd/01-raw-facts.md` following the exact schema in `(probes/tpipeose-interrogation.md)`.

---

## Phase 2: Lineage-Preserving Event Distillation

Convert `.ddd/01-raw-facts.md` into a deterministic YAML artifact:

```bash
python scripts/compile_events.py --input .ddd/01-raw-facts.md --output .ddd/02-events.yaml
```

Verify that `.ddd/02-events.yaml` retains `id`, `traces_to`, `event_name`, `command`, `evidence_tier`, `rationale`, `source_actor`, `invariants`, `payload_fields`, and `status: ACTIVE`.

---

## Phase 3: Strategic Design & Conway-Aware Context Mapping

Start a clean context consuming **only** `.ddd/00-context-charter.md` and `.ddd/02-events.yaml`:
1. **Ubiquitous Language Glossary**: Define canonical terms, synonyms, and cross-context forbidden homonyms.
2. **Subdomain & Conway Classification**: Classify into `CoreDomain`, `SupportingDomain`, or `GenericSubdomain`; align boundaries with team ownership and data sovereignty.
3. **Context Map**: Define upstream/downstream relationships (`CustomerSupplier`, `Conformist`, `AntiCorruptionLayer`, `OpenHostService`, `SharedKernel`, `Partnership`) with a Mermaid topology diagram.

**Deliverable**: `.ddd/03-context-map.md`.
**[Human Gate 1]**: Present the Context Map, Ubiquitous Language, and Parking Lot assumptions. Wait for explicit human approval before Phase 4.

---

## Phase 4: Tactical DMML v2 Assembly

Slice `.ddd/02-events.yaml` per Bounded Context (parallelizable via stateless subagents). Generate `.ddd/04-models/<context-name>.yaml` strictly conforming to `(references/dmml-specification.md)`:
1. **Aggregates & Entities**: Bound by true atomic invariants and contention profile (`distributed` vs. `modular_monolith` vs. `client_runtime`). Reference external aggregates strictly by scalar ID (`*_id`).
2. **Deterministic State Machines**: Declare `initial_state`, `terminal_states`, `states`, and `transitions` with explicit `guard` expressions and `emits` events.
3. **Policies, Sagas & Read Models**:
   - Place Tier 3 configurable rules into `policies[]`.
   - Place cross-aggregate eventual consistency flows and compensations into `sagas[]`.
   - Place multi-entity queries, dashboards, and aggregations into `read_models[]`.
4. **Lineage Binding**: Every invariant, command, event, policy, and read model must declare `traces_to: ["EVT-xxx", "FACT-xxx"]`.

---

## Phase 5: Deterministic Graph & Invariant Linting

Run the static analyzer across all generated DMML models and the event ledger:

```bash
python scripts/dmml_linter.py --models-dir .ddd/04-models/ --events-file .ddd/02-events.yaml
```

The linter deterministically blocks:
- Cross-context circular dependency cycles (DFS graph check).
- Direct entity/aggregate object references violating ID-only isolation.
- State machine unreachable islands (BFS from `initial_state`), undeclared states, unguarded non-deterministic transitions, and non-terminal dead ends.
- Missing lineage (`traces_to`) or references to `INVALIDATED` facts/events.

Fix all errors and re-run until exit code is `0`.
**[Human Gate 2]**: Present the verified DMML models and linter report for sign-off.

---

## Phase 6: Executable Constitution Injection into `AGENTS.md`

1. Load `(references/agents-md-template.md)`.
2. Target root `AGENTS.md` (or update existing `agents.md` / `CLAUDE.md` in place without creating duplicate case-variant files).
3. Idempotently inject/update the `DDD-DOMAIN-CONSTITUTION` block, binding each Bounded Context to its source directory, DMML model path, and pre-implementation verification checklist.

---

## Cross-Domain Conflict & RACI Resolution Protocol

When a newly discovered fact in Context B contradicts an established rule in Context A:
1. **Homonym Triangulation**: Determine whether Context A and Context B use the same word for distinct concepts. If so, fork the term in the Ubiquitous Language Glossary (`ContextA.Term` vs. `ContextB.Term`).
2. **RACI Authority Check**: If it is a true contradiction against a `hard_invariant` or `compliance_gate` owned by another stakeholder/team, flag an **Authority Escalation** rather than allowing an unauthorized role to overwrite it silently.
3. **Targeted Lineage Invalidation**: Mark superseded entries in `.ddd/02-events.yaml` as `status: INVALIDATED`.
4. **Deterministic Slice Recalculation**: Run `dmml_linter.py` to locate exact downstream models referencing the invalidated IDs via `traces_to`, and re-synthesize only the affected Bounded Context slice.
