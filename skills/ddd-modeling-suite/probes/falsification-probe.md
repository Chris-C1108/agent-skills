# 4-Tier Rule Epistemology, Chesterton's Fence & Cross-Domain Triangulation Probe

Domain models are institutional contracts, not physical laws of nature. Naive Popperian falsification (*"If removing this rule doesn't crash the system today, delete it"*) destroys regulatory compliance, audit trails, and historical risk guardrails (**Chesterton's Fence**), while aggressive interrogation triggers user confabulation.

Use this protocol to classify domain rules accurately and resolve cross-context contradictions safely.

---

## 1. Non-Adversarial Counterfactual Probe & 4-Tier Classification

When a stakeholder states a rule, constraint, or mandatory field, avoid adversarial interrogation. Ask a collaborative counterfactual question:

> *"To make sure we put this rule in the right architectural layer: if this rule were bypassed or changed next quarter, what kind of impact would happen first?"*
> - *(A) Immediate data corruption, negative balance, or broken core math*
> - *(B) Legal/regulatory violation, failed security audit, or broken contract with an external partner*
> - *(C) Business strategy shift (e.g., different rules for VIP tiers, regions, or promotional campaigns)*
> - *(D) Visual layout inconvenience or user-experience friction*

### The 4-Tier Architectural Routing Matrix

| Tier | Classification | Diagnostic Criteria | Target DMML Construct |
| :--- | :--- | :--- | :--- |
| **Tier 1** | `hard_invariant` (物理/数学/账务硬不变量) | Violation corrupts state integrity, causes double-spending, or violates conservation laws within a single transaction. | `aggregates[].invariants` (Enforced atomically inside the Aggregate Root). |
| **Tier 2** | `compliance_gate` (切斯特顿栅栏：合规/审计/风控底线) | Removing it does **not** crash the technical happy path, but violates law, GxP/SOX audit, security, or historical incident guardrails. | `aggregates[].invariants` or `policies[]` marked `tier: compliance_gate` (Protected against silent deletion). |
| **Tier 3** | `configurable_policy` (可变业务策略/运营规则) | Varies by tenant, market, season, or operational experiment (e.g., discount thresholds, retry limits, risk scoring weights). | `policies[]` (Strategy / Specification pattern injected into domain services; never hardcoded as immutable entity logic). |
| **Tier 4** | `ui_convention` (表现层交互约定) | Purely ergonomic or visual formatting preference with zero domain state impact. | Excluded from core domain model; delegated to Frontend/UI layer specs. |

### Chesterton's Fence Safeguard
- If the current interviewee says *"I don't know why this rule exists, it was there before I joined"*, **DO NOT classify it as Tier 4 accidental noise**.
- Tag it as `tier: compliance_gate (pending_verification)` and log an item in `.ddd/00-parking-lot.md` to verify with the owning team or legacy commit blame.

---

## 2. Cross-Domain Triangulation & RACI Authority Protocol

When an assertion in **Context B** contradicts an established fact or invariant in **Context A**, execute this 4-step protocol instead of blindly overwriting Context A:

### Step 1: Homonym vs. True Conflict Triangulation
Present the conflict neutrally:
> *"In [Context A], `{Term}` was defined with rule `[X]`, whereas in [Context B] `{Term}` requires `[Y]`. Are we looking at:*
> *1. **Homonyms (同名异义)**: Two distinct business concepts sharing the same casual word across departments (e.g., Merchandising `Product` vs. Warehouse `PhysicalSKU`)?*
> *2. **True Rule Change (全局规则修正)**: The original rule `[X]` in [Context A] is actually outdated or mistaken?"*

### Step 2: RACI & Ownership Authority Gate
If the user selects **Option 2 (True Rule Change)**:
- Check `OwnerTeam` and `EvidenceTier` of the original fact in `.ddd/01-raw-facts.md` / `.ddd/02-events.yaml`.
- **Authority Guardrail**: If the contradicted fact is a `hard_invariant` or `compliance_gate` owned by **Team A** (e.g., Finance/Legal), and the current interviewee belongs to **Team B** (e.g., Marketing/Frontend), **do not silently invalidate Team A's invariant**.
- Record a `[RACI_CONFLICT]` in `.ddd/00-parking-lot.md` and ask for joint sign-off from Team A's owner.

### Step 3: Lineage-Based Invalidation
Once authorized:
1. Update the superseded fact in `.ddd/01-raw-facts.md` (`Status: INVALIDATED`) and re-run `scripts/compile_events.py` (or mark `status: "INVALIDATED"` in `.ddd/02-events.yaml`).
2. Append a new replacement fact (`[FACT-xxx]`) with `Rationale` explaining why the prior rule was superseded.

### Step 4: Targeted Slice Recalculation
Run `python scripts/dmml_linter.py --models-dir .ddd/04-models/ --events-file .ddd/02-events.yaml`.
- The linter automatically flags every Aggregate invariant, Command, Event, Policy, or Read Model whose `traces_to` array references the `INVALIDATED` ID.
- Re-run Phase 4 tactical assembly **only** for the flagged Bounded Context slices.
