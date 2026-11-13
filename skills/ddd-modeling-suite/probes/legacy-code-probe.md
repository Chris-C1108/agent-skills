# Legacy Codebase & Database Reverse-Engineering Probe (Brownfield DDD)

When reverse-engineering a legacy codebase into DDD, two fatal traps must be avoided:
1. **Data-Driven Mirroring**: Turning relational database tables 1:1 into Anemic Aggregates.
2. **Transaction Survivor Bias**: Assuming existing `@Transactional` annotations represent true business invariants (in legacy code, `@Transactional` often wraps 3,000-line God methods mutating 5 unrelated domains, or is missing entirely).

Follow this 5-step behavioral forensics sequence instead.

---

## 1. Reconstruct Implicit State Machines & Concurrency Locks

Do not start with column lists. Search for **state transitions** and **contention guards**:
1. **State & Lifecycle Columns**:
   - Locate `status`, `state`, `phase`, `step`, `is_deleted`, `flag` fields across persistence models.
   - Trace every conditional guard (`if (order.status != PAID)`, `WHERE status = 1 AND version = ?`) to reconstruct the real State Machine and its transition guards.
2. **True Contention Boundaries (Locks & CAS)**:
   - Locate `SELECT ... FOR UPDATE`, `@Version` (optimistic locking), distributed locks (`RedisLock`, `Mutex`), and atomic compare-and-swap (`UPDATE ... SET quota = quota - 1 WHERE quota >= 1`).
   - **Insight**: Wherever legacy engineers were forced to add a lock or CAS update is where a real **Tier 1 Hard Invariant** lives.

---

## 2. Transaction Smell & Mutation Graph Audit

Audit every `@Transactional` block, `BEGIN...COMMIT` scope, or Unit-of-Work:
1. **Extract the Co-Mutation Set**:
   - List all tables/entities mutated (`INSERT`, `UPDATE`, `DELETE`) inside the same transaction.
2. **Challenge God Transactions**:
   - If a single transaction mutates entities across distinct business concepts (e.g., `Order` + `Inventory` + `LoyaltyPoints` + `NotificationLog` + synchronous HTTP RPC call), classify it as a **God Transaction Smell**, NOT a single Aggregate.
   - Apply the **Contention & Ownership Split Test**:
     - Do these tables share the same lifecycle and same team owner?
     - Does business correctness require millisecond-level atomic rollback, or was synchronous coupling merely coding convenience?
   - Split weakly coupled mutations into separate Bounded Contexts connected via Domain Events or Outbox Sagas.

---

## 3. Trace Entrypoints (Commands) & Outbound Seams (Domain Events)

1. **Inbound Entrypoints -> Commands & Actors**:
   - Inspect HTTP Controllers (`POST/PUT/PATCH/DELETE`), RPC handlers, CLI commands, and cron jobs.
   - Map each state-mutating entrypoint to a **Command**, its **Actor**, and its **Precondition guards**.
2. **Outbound Side Effects -> Domain Events**:
   - Trace message broker producers (`kafka.send`, `rabbitTemplate.convertAndSend`), webhook dispatches, event buses, and critical audit logs (`logger.info("Order settled: ...")`).
   - Map each side effect to a past-tense **Domain Event**.

---

## 4. Separate Query SQL into CQRS Read Models

Legacy repositories often mix complex multi-table `JOIN` reporting queries with entity mutation methods:
- Isolate all multi-table `SELECT ... JOIN ... GROUP BY` queries, dashboard endpoints, and export jobs.
- Map them to **`read_models[]`** in DMML rather than polluting Aggregate Root structure with read-only join fields.

---

## 5. Isolate Legacy Technical Debt Behind an Anti-Corruption Layer (ACL)

1. Identify God classes (`CommonUtil`, `BaseManager`), 50-column wide tables shared across departments, or third-party vendor payloads with cryptic field names (`ext_fld_01`).
2. Never allow legacy naming or wide-table schemas to leak into the new Ubiquitous Language.
3. Define an explicit `AntiCorruptionLayer` dependency in the Context Map and DMML specification to translate between legacy persistence/APIs and clean domain models.
