# DMML v2.0 (Domain Model Markup Language) Specification

DMML v2.0 is a deterministic, machine-verifiable YAML specification for strategic and tactical Domain-Driven Design models. Every model file in `.ddd/04-models/<context>.yaml` must conform to this schema and pass `scripts/dmml_linter.py`.

---

## Complete YAML Schema Reference

```yaml
version: "2.0"

bounded_context:
  name: "PlaybackContext"
  type: "CoreDomain" # CoreDomain | SupportingDomain | GenericSubdomain
  owner_team: "PlayerCoreTeam"
  architecture_profile: "client_runtime" # distributed | modular_monolith | client_runtime
  description: "Manages media playback state, timeline alignment, and player lifecycle."
  dependencies:
    - context: "HostAdapterContext"
      relationship: "AntiCorruptionLayer" # Partnership | SharedKernel | CustomerSupplier | Conformist | AntiCorruptionLayer | OpenHostService
      upstream_or_downstream: "downstream"

ubiquitous_language:
  - term: "TimelineSession"
    definition: "An active viewing session bound to a verified media fingerprint and player instance."
    synonyms: ["ActivePlayback"]
    forbidden_terms: ["VideoTab", "DOMPlayer"]
    traces_to: ["EVT-001", "FACT-001"]

aggregates:
  - name: "TimelineSession"
    root_entity: "TimelineSession"
    contention_profile: "single_actor" # high_concurrency | moderate | single_actor
    description: "Guarantees atomic consistency between playback cursor and anchor checkpoints."

    invariants:
      - id: "INV-001"
        tier: "hard_invariant" # hard_invariant | compliance_gate
        assertion: "current_time_ms >= 0 and current_time_ms <= total_duration_ms"
        description: "Playback cursor can never be negative or exceed media duration."
        traces_to: ["EVT-001", "FACT-001"]

    entities:
      - name: "TimeAnchor"
        identifier: "anchor_id"
        properties:
          - name: "anchor_id"
            type: "string"
          - name: "timestamp_ms"
            type: "integer"
          - name: "author_user_id" # Cross-aggregate reference MUST use scalar *_id
            type: "string"

    value_objects:
      - name: "VideoFingerprint"
        immutable: true
        properties:
          - name: "content_hash"
            type: "string"
          - name: "total_duration_ms"
            type: "integer"

    state_machine:
      initial_state: "IDLE"
      terminal_states: ["TERMINATED"]
      states: ["IDLE", "BUFFERING", "PLAYING", "PAUSED", "SEEKING", "TERMINATED"]
      transitions:
        - from: "IDLE"
          to: "BUFFERING"
          trigger: "LoadMediaCommand"
          guard: "fingerprint.total_duration_ms > 0"
          emits: ["MediaLoadingStarted"]
        - from: "BUFFERING"
          to: "PLAYING"
          trigger: "BufferReadyEvent"
          guard: "buffer_health_ms >= 500"
          emits: ["PlaybackStarted"]
        - from: "PLAYING"
          to: "PAUSED"
          trigger: "PausePlaybackCommand"
          guard: "current_time_ms <= total_duration_ms"
          emits: ["PlaybackPaused"]
        - from: "PAUSED"
          to: "PLAYING"
          trigger: "ResumePlaybackCommand"
          guard: "session_active == true"
          emits: ["PlaybackResumed"]
        - from: "PLAYING"
          to: "SEEKING"
          trigger: "SeekTimelineCommand"
          guard: "target_time_ms >= 0 and target_time_ms <= total_duration_ms"
          emits: ["TimelineSeekInitiated"]
        - from: "SEEKING"
          to: "PLAYING"
          trigger: "SeekCompletedEvent"
          guard: "true"
          emits: ["TimelineSeekCompleted"]
        - from: "PAUSED"
          to: "TERMINATED"
          trigger: "CloseSessionCommand"
          guard: "true"
          emits: ["PlaybackSessionClosed"]
        - from: "PLAYING"
          to: "TERMINATED"
          trigger: "CloseSessionCommand"
          guard: "true"
          emits: ["PlaybackSessionClosed"]

    commands:
      - name: "PausePlaybackCommand"
        actor: "Viewer"
        payload: ["session_id", "paused_at_ms", "trigger_reason"]
        preconditions: ["state in ['PLAYING', 'SEEKING']"]
        emits_events: ["PlaybackPaused"]
        traces_to: ["EVT-001", "FACT-001"]

    domain_events:
      - name: "PlaybackPaused"
        payload: ["session_id", "paused_at_ms", "trigger_reason", "occurred_at"]
        consumers: ["CommentStreamContext", "TrendAnalyticsContext"]
        traces_to: ["EVT-001", "FACT-001"]

policies:
  - id: "POL-001"
    name: "PlaybackSpeedStepPolicy"
    tier: "configurable_policy"
    trigger: "ChangePlaybackRateCommand"
    rule: "allowed_rates in configured_rate_table"
    configurable_parameters: ["allowed_rates"]
    traces_to: ["EVT-002", "FACT-002"]

domain_services:
  - name: "TimelineDriftCompensator"
    description: "Computes clock drift between host video element and anchor stream."
    inputs: ["local_timestamp_ms", "host_frame_rate"]
    output: "corrected_timestamp_ms"
    traces_to: ["EVT-001"]

sagas:
  - name: "CrossTabSessionHandoffSaga"
    trigger_event: "PlaybackPaused"
    steps:
      - "Persist checkpoint via StorageAdapter"
      - "Broadcast CheckpointUpdated to peer tabs"
    compensation_strategy: "Fallback to last verified local anchor if storage quota is exceeded"
    traces_to: ["EVT-001"]

read_models:
  - name: "TimelineHeatmapProjection"
    consumer: "ViewerOverlayUI"
    freshness_sla: "eventual_5s"
    source_events: ["PlaybackPaused", "CommentAnchored"]
    projected_fields: ["bucket_second", "pause_density_score", "top_comment_preview"]
    traces_to: ["EVT-001"]
```

---

## Mandatory Structural Invariants (Enforced by `dmml_linter.py`)

1. **Identity-Only Cross-References**:
   - Every property in `entities[].properties` referencing another Aggregate Root or foreign Entity **must** end with `_id` or `_ids` and use a scalar/ID type (`string`, `uuid`, `integer`, `array<string>`), never a direct Aggregate or Entity type name.
2. **Acyclic Context Topology**:
   - `bounded_context.dependencies` across `.ddd/04-models/*.yaml` must form a Directed Acyclic Graph (DAG) unless explicitly declared as `SharedKernel` or `Partnership`.
3. **Closed & Deterministic State Machine**:
   - `initial_state` and all `terminal_states` must belong to `states`.
   - Every state in `states` must be reachable from `initial_state` via `transitions`.
   - Every non-terminal state must have at least one outbound transition.
   - Multiple transitions sharing the same `(from, trigger)` pair must each define a non-empty, distinct `guard` expression.
4. **Lineage & Validity Integrity**:
   - Every `invariant`, `command`, `domain_event`, `policy`, and `read_model` must include a non-empty `traces_to` list pointing to valid `EVT-xxx` or `FACT-xxx` IDs.
   - No element may trace to an event or fact marked `status: "INVALIDATED"` in `.ddd/02-events.yaml`.
