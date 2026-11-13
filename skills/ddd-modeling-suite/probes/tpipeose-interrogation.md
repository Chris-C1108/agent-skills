# Human-Centric BA Elicitation: T-P-I-P-O-S-E, CRUDA & 0/1/N Probes

This probe governs how the Agent extracts tacit domain rules from human stakeholders without causing cognitive overload, defensive stonewalling, or confabulation.

---

## 1. Human-Factors Interview Protocol (Cognitive & Social Guardrails)

### Rule 1: Story First, Schema Second (Polanyi's Paradox Mitigation)
Human domain experts store 90% of tacit knowledge in **episodic memory** (concrete incidents), not **semantic memory** (abstract state machines).
- `FORBIDDEN: Asking abstract meta-model questions like "What are the preconditions, implicit inputs, and idempotency invariants of this command?"`
- `USE: Critical Incident Technique (CIT) & Example Mapping — ask the user to walk through a concrete recent case (especially a failure, refund, manual fix, or dispute), then silently map their story into T-P-I-P-O-S-E slots.`

### Rule 2: Strict Turn Budget (3-Question Ceiling + Anchored Options)
- Ask **at most 2–3 focused questions per turn**.
- Frame every question with **2–3 concrete business options (A / B / C) + a recommended industry default**, turning high-friction open recall into low-friction recognition.
- Always permit the **Parking Lot escape hatch**: if the user is unsure or needs another department's input, log the item into `.ddd/00-parking-lot.md` with a `TODO_ASSUMPTION` tag and continue.

### Rule 3: Non-Judgmental Shadow Workflow Discovery
Operational users often hide offline Excel sheets, WeChat approvals, or manual database tweaks out of fear of blame.
- Ask: *"When the current system or standard workflow gets stuck under time pressure, how does the team currently work around it (e.g., temporary spreadsheet, manual override) to get the job done?"*
- Treat every workaround as a high-value signal of a missing domain capability or overly rigid invariant.

---

## 2. The 7-Step T-P-I-P-O-S-E Causal Probe

Use these 7 slots as your **internal completeness checklist** for every domain action:

### 1. T — Trigger (触发源)
- **Internal Goal**: Distinguish synchronous user commands, scheduled timers, DOM mutations, and asynchronous upstream events.
- **Human-Friendly Prompt**: *"What kicks this off in the real world? (A) A user clicking a button, (B) An automatic timer/deadline, or (C) A notification from another system?"*

### 2. P — Preconditions (前置守卫条件)
- **Internal Goal**: Extract state machine guards and eligibility gates.
- **Human-Friendly Prompt**: *"Before this action is allowed, what must already be true? Under what situation should the system immediately block the user and say 'You can't do this right now'?"*

### 3. I — Implicit Inputs (隐式输入与环境上下文)
- **Internal Goal**: Uncover hidden decision inputs omitted from UI forms (server clock, tenant quota, operator role, device/host environment, exchange rate snapshot).
- **Human-Friendly Prompt**: *"Besides what the user types on screen, what background facts does the system need to check silently (e.g., current time window, VIP tier, host page version, quota balance)?"*

### 4. P — Process & Atomic Invariants (核心规则与原子不变量)
- **Internal Goal**: Identify the exact conservation law or consistency rule that defines the Aggregate Root boundary.
- **Human-Friendly Prompt**: *"During this step, what is the 'iron rule' that must never be broken—even if two people click at the exact same millisecond?"*

### 5. O — Primary Output (直接状态结果)
- **Internal Goal**: Define the immediate state transition and synchronous return contract.
- **Human-Friendly Prompt**: *"Right after this succeeds, what status does the item move into, and what immediate confirmation does the caller see?"*

### 6. S — Side Effects (派生事件与下游副作用)
- **Internal Goal**: Identify Domain Events emitted to trigger downstream aggregates, notifications, or external webhooks.
- **Human-Friendly Prompt**: *"Once this is done, who else or what other module needs to be notified (e.g., billing, audit log, trend counter, email)? Can that notification happen a second later, or must it succeed together?"*

### 7. E — Exceptions, Idempotency & Fallbacks (异常、幂等与降级补偿)
- **Internal Goal**: Define retry safety, duplicate submission handling, and partial failure recovery.
- **Human-Friendly Prompt**: *"If the network lags and the user double-clicks, or if an external API times out halfway through, should we: (A) Reject the duplicate via request ID, (B) Auto-retry in background, or (C) Roll back and alert an operator?"*

---

## 3. CRUDA Full-Lifecycle Probe

Never stop at Happy-Path Creation (`Create`). Walk every core business concept through the remaining lifecycle stages:

| Stage | Internal Probe Target | Human-Friendly Question Pattern |
| :--- | :--- | :--- |
| **C — Create** | Initialization defaults, uniqueness constraints, factory validation | *"Can two items be created with the same name/key, or how do we tell duplicates apart?"* |
| **R — Read / View** | Cross-entity projections, permission masking, sorting/filtering | *"Who views this data later, what summary metrics do they need, and which sensitive fields must be masked?"* |
| **U — Update / Merge** | Overwrite vs. append-only history, state-locked fields, concurrent edits | *"Once created, which fields are frozen forever, and if updated, do we overwrite in place or keep a versioned audit trail?"* |
| **D — Delete / Void** | Hard delete vs. soft delete (`VOIDED`/`CANCELLED`), cascading impact | *"When a user 'deletes' this, is it physically erased (GDPR) or marked as Voided/Cancelled with a reversal record?"* |
| **A — Archive / Compensate** | Cold storage TTL, mid-flight cancellation, refund/undo Saga | *"If someone cancels after downstream steps already started, how do we undo or compensate the finished steps?"* |

---

## 4. 0 / 1 / N Cardinality & Concurrency Fracture Probe

Test boundary fractures where naive models break in production:

1. **Zero (Empty / Cold-Start Boundary)**:
   - What happens when the collection has `0` items, a required external feed returns empty, or a new user has zero history?
2. **One (Singleton / Exclusivity Boundary)**:
   - Can an actor hold only `1` active instance at a time (e.g., single active playback session, single default address)? When a second arrives, do we reject the new one or preempt/close the old one?
3. **Many (N-Scale / Bulk & Pagination Boundary)**:
   - Is `N` bounded (e.g., max 50 slides per deck, max 500 items per order)? When `N` reaches 10,000+, how is it chunked, paginated, or rate-limited?
4. **Simultaneous Contention (Race Arbitration)**:
   - When Actor A and Actor B mutate the same target within 5ms:
     - **Option A**: First-write-wins (Optimistic Concurrency fails second writer).
     - **Option B**: Last-write-wins (Idempotent state overwrite).
     - **Option C**: Domain merge / commutative accumulation (e.g., CRDT or atomic counter delta).

---

## 5. CQRS Read-Model & Decision View Probe

Do not force complex queries, dashboards, or cross-context reports into Write Aggregates:
- Whenever a requirement describes **listing, searching, aggregating, charting, or comparing across multiple records**, classify it as a **`ReadModel` (Query Projection)** rather than an Aggregate invariant.
- Record:
  1. **Target Decision / Consumer**: Who reads this view and what decision does it drive?
  2. **Source Events / Contexts**: Which domain events or upstream contexts feed this view?
  3. **Freshness SLA**: Real-time synchronous read vs. eventual consistency (e.g., 5s delay or daily snapshot).

---

## 6. Canonical Output Schema for `.ddd/01-raw-facts.md`

Write Phase 1 discoveries into `.ddd/01-raw-facts.md` using the following deterministic Markdown block structure so `scripts/compile_events.py` parses every field losslessly:

```markdown
# Raw Domain Facts & Elicitation Ledger

## [FACT-001] PlaybackPaused
- Command: PausePlaybackCommand
- Event: PlaybackPaused
- Actor: Viewer
- OwnerTeam: PlayerCoreTeam
- Context: PlaybackContext
- TargetConcept: TimelineSession
- Trigger: User clicks pause button or window loses visibility focus
- Precondition: Session state must be PLAYING or SEEKING
- ImplicitInput: Current media element timestamp_ms, browser tab visibility state
- Invariant: current_time_ms >= 0 and current_time_ms <= total_duration_ms
- EvidenceTier: hard_invariant
- Rationale: Negative or out-of-bounds timestamps corrupt timeline anchor synchronization across tabs.
- Payload: session_id, paused_at_ms, trigger_reason
- SideEffect: Persist last checkpoint to local storage; emit PlaybackPaused event
- Exception: If media element is detached from DOM, transition to TERMINATED and trigger HostAdapter reconnect
- Status: ACTIVE
```
