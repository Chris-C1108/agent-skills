#!/usr/bin/env python3
"""
compile_events.py (V2)
Deterministic compiler that transforms raw domain discovery facts (.ddd/01-raw-facts.md)
into a lineage-preserving, schema-validated YAML event ledger (.ddd/02-events.yaml).
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple


VALID_TIERS = {
    "hard_invariant",
    "compliance_gate",
    "configurable_policy",
    "ui_convention",
}


def yaml_quote(value: Any) -> str:
    """Safely serialize any string/scalar as a valid YAML double-quoted scalar."""
    if value is None:
        return '""'
    text = str(value).strip()
    return json.dumps(text, ensure_ascii=False)


def split_items(raw_val: str) -> List[str]:
    """Split comma/semicolon lists when appropriate, or keep single assertion intact."""
    cleaned = raw_val.strip().strip("[]")
    if not cleaned:
        return []
    if "," in cleaned and not any(op in cleaned for op in [">=", "<=", "==", "!=", " and ", " or "]):
        return [item.strip().strip("'\"") for item in re.split(r"[,;，；]", cleaned) if item.strip()]
    return [cleaned]


def clean_markdown_key(raw_key: str) -> str:
    """Normalize markdown bullet key (strip *, `, whitespace, lower-case)."""
    cleaned = re.sub(r"[*_`~]", "", raw_key).strip().lower()
    cleaned = re.sub(r"[\s\-_]+", "_", cleaned)
    return cleaned


def parse_markdown_facts(content: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Extract structured event tuples and optional read models from Markdown text.
    Supports both '## [FACT-001] Title' blocks and standard '## Title' blocks,
    with ASCII ':' or Chinese '：' key-value bullets.
    """
    events: List[Dict[str, Any]] = []
    read_models: List[Dict[str, Any]] = []
    current_block: Dict[str, Any] = {}
    current_kind = "event"

    def flush_block() -> None:
        nonlocal current_block, current_kind
        if not current_block:
            return
        if current_kind == "read_model":
            has_substance = any(
                current_block.get(k) for k in ("name", "consumer", "freshness_sla", "context_candidate")
            )
        else:
            has_substance = any(
                current_block.get(k)
                for k in (
                    "event_name",
                    "command",
                    "target_concept",
                    "invariants",
                    "trigger",
                    "preconditions",
                    "payload_fields",
                )
            )
        if has_substance:
            if current_kind == "read_model":
                read_models.append(current_block)
            else:
                events.append(current_block)
        current_block = {}
        current_kind = "event"

    header_pattern = re.compile(
        r"^#{2,4}\s*(?:\[(?P<id>[A-Za-z]+-\d+)\])?\s*(?P<title>.+?)\s*$"
    )
    kv_pattern = re.compile(r"^[-*+]\s*(?P<key>[^:：]+?)\s*[:：]\s*(?P<val>.+?)\s*$")

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("<!--"):
            continue

        header_match = header_pattern.match(line)
        if header_match:
            flush_block()
            explicit_id = header_match.group("id")
            raw_title = header_match.group("title").strip()

            # Skip pure document section headers that have no fact ID and look like generic headings
            lower_title = raw_title.lower()
            if not explicit_id and any(
                skip in lower_title
                for skip in (
                    "raw domain facts",
                    "elicitation ledger",
                    "overview",
                    "table of contents",
                )
            ):
                continue

            if explicit_id and explicit_id.upper().startswith("READ-"):
                current_kind = "read_model"
                current_block["read_model_id"] = explicit_id.upper()
                current_block["name"] = re.sub(r"[^a-zA-Z0-9_]", "", raw_title) or raw_title
            else:
                current_kind = "event"
                if explicit_id:
                    current_block["fact_id"] = explicit_id.upper()
                current_block["raw_title"] = raw_title
                sanitized = re.sub(r"[^a-zA-Z0-9_]", "", raw_title)
                if sanitized:
                    current_block["event_name"] = sanitized
            continue

        kv_match = kv_pattern.match(line)
        if kv_match:
            key = clean_markdown_key(kv_match.group("key"))
            val = kv_match.group("val").strip()
            if not val:
                continue

            if key in ("fact_id", "id"):
                current_block["fact_id"] = val.upper()
            elif key in ("event", "event_name", "domain_event", "事件", "领域事件"):
                current_block["event_name"] = val
            elif key in ("command", "command_name", "命令", "触发命令"):
                current_block["command"] = val
            elif key in ("trigger", "触发源", "触发条件"):
                current_block["trigger"] = val
            elif key in ("actor", "role", "user", "执行者", "角色"):
                current_block["actor"] = val
            elif key in ("owner_team", "owner", "team", "raci_owner", "归属团队", "负责团队"):
                current_block["owner_team"] = val
            elif key in ("context", "bounded_context", "context_candidate", "限界上下文", "所属上下文"):
                current_block["context_candidate"] = val
            elif key in ("target_concept", "aggregate", "entity", "target", "目标概念", "聚合根"):
                current_block["target_concept"] = val
            elif key in ("evidence_tier", "tier", "rule_tier", "规则层级", "证据等级"):
                norm_tier = val.lower().strip().replace(" ", "_")
                current_block["evidence_tier"] = (
                    norm_tier if norm_tier in VALID_TIERS else val
                )
            elif key in ("rationale", "reason", "why", "falsification_proof", "业务动机", "证伪依据"):
                current_block["rationale"] = val
            elif key in ("status", "状态"):
                current_block["status"] = val.upper()
            elif key in ("precondition", "preconditions", "guard", "前置条件", "守卫条件"):
                current_block.setdefault("preconditions", []).append(val)
            elif key in ("implicit_input", "implicit_inputs", "env_input", "隐式输入", "环境输入"):
                current_block.setdefault("implicit_inputs", []).extend(split_items(val))
            elif key in ("invariant", "invariants", "rule", "process", "不变量", "核心规则"):
                current_block.setdefault("invariants", []).append(val)
            elif key in ("payload", "payload_fields", "input", "inputs", "parameters", "参数", "输入载荷"):
                current_block.setdefault("payload_fields", []).extend(split_items(val))
            elif key in ("output", "primary_output", "直接产出", "输出结果"):
                current_block["primary_output"] = val
            elif key in ("side_effect", "side_effects", "副作用", "派生影响"):
                current_block.setdefault("side_effects", []).append(val)
            elif key in ("exception", "exceptions", "fallback", "异常", "降级策略"):
                current_block.setdefault("exceptions", []).append(val)
            elif key in ("traces_to", "lineage", "溯源"):
                current_block.setdefault("traces_to", []).extend(split_items(val))
            elif key in ("consumer", "consumers", "消费方"):
                current_block["consumer"] = val
            elif key in ("freshness_sla", "sla", "时效要求"):
                current_block["freshness_sla"] = val

    flush_block()
    return events, read_models


def emit_yaml(
    events: List[Dict[str, Any]],
    read_models: List[Dict[str, Any]],
    output_path: str,
) -> None:
    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Compiled Domain Events & Lineage Ledger (Generated by compile_events.py v2.0)\n")
        f.write("# Downstream Strategic & Tactical Agents consume ONLY this distilled artifact.\n\n")
        f.write('version: "2.0"\n')
        f.write("events:\n")

        for idx, ev in enumerate(events, 1):
            evt_id = f"EVT-{idx:03d}"
            fact_id = ev.get("fact_id", f"FACT-{idx:03d}")
            name = ev.get("event_name") or ev.get("command") or f"DiscoveredFact_{idx}"
            cmd = ev.get("command", f"Trigger{name}Command")
            trigger = ev.get("trigger", "Manual/User")
            actor = ev.get("actor", "User")
            owner_team = ev.get("owner_team", "UnassignedTeam")
            target = ev.get("target_concept", "DomainEntity")
            ctx = ev.get("context_candidate", "UnassignedContext")
            tier = ev.get("evidence_tier", "hard_invariant")
            rationale = ev.get("rationale", "Extracted from Phase 1 BA elicitation.")
            status = ev.get("status", "ACTIVE").upper()
            traces = ev.get("traces_to", [])
            if fact_id not in traces:
                traces = [fact_id] + traces

            f.write(f"  - id: {yaml_quote(evt_id)}\n")
            f.write(f"    fact_id: {yaml_quote(fact_id)}\n")
            f.write(f"    status: {yaml_quote(status)}\n")
            f.write(f"    event_name: {yaml_quote(name)}\n")
            f.write(f"    command: {yaml_quote(cmd)}\n")
            f.write(f"    trigger: {yaml_quote(trigger)}\n")
            f.write(f"    actor: {yaml_quote(actor)}\n")
            f.write(f"    owner_team: {yaml_quote(owner_team)}\n")
            f.write(f"    target_concept: {yaml_quote(target)}\n")
            f.write(f"    context_candidate: {yaml_quote(ctx)}\n")
            f.write(f"    evidence_tier: {yaml_quote(tier)}\n")
            f.write(f"    rationale: {yaml_quote(rationale)}\n")

            f.write("    traces_to:\n")
            for t in traces:
                f.write(f"      - {yaml_quote(t)}\n")

            for list_key, default_item in (
                ("preconditions", None),
                ("implicit_inputs", None),
                ("invariants", "State transition must be valid"),
                ("payload_fields", "entity_id"),
                ("side_effects", None),
                ("exceptions", None),
            ):
                items = ev.get(list_key, [])
                f.write(f"    {list_key}:\n")
                if items:
                    for item in items:
                        f.write(f"      - {yaml_quote(item)}\n")
                elif default_item is not None:
                    f.write(f"      - {yaml_quote(default_item)}\n")
                else:
                    f.write("      []\n")

        if read_models:
            f.write("\nread_models:\n")
            for idx, rm in enumerate(read_models, 1):
                rm_id = rm.get("read_model_id", f"READ-{idx:03d}")
                f.write(f"  - id: {yaml_quote(rm_id)}\n")
                f.write(f"    name: {yaml_quote(rm.get('name', f'ReadModel_{idx}'))}\n")
                f.write(f"    context_candidate: {yaml_quote(rm.get('context_candidate', 'UnassignedContext'))}\n")
                f.write(f"    consumer: {yaml_quote(rm.get('consumer', 'User'))}\n")
                f.write(f"    freshness_sla: {yaml_quote(rm.get('freshness_sla', 'eventual'))}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile raw domain discovery facts into structured YAML event tuples."
    )
    parser.add_argument("--input", required=True, help="Path to raw facts markdown file (.ddd/01-raw-facts.md)")
    parser.add_argument("--output", required=True, help="Path to output YAML file (.ddd/02-events.yaml)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[ERROR] Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print(f"[ERROR] Input file '{args.input}' is empty.", file=sys.stderr)
        sys.exit(1)

    events, read_models = parse_markdown_facts(content)
    if not events:
        print(
            f"[ERROR] 0 domain facts/events could be parsed from '{args.input}'.\n"
            "Ensure '.ddd/01-raw-facts.md' uses '## [FACT-001] <EventName>' blocks with '- Key: Value' bullets.",
            file=sys.stderr,
        )
        sys.exit(1)

    emit_yaml(events, read_models, args.output)
    print(
        f"[OK] Distilled {len(events)} domain event(s) and {len(read_models)} read model(s) into {args.output}"
    )


if __name__ == "__main__":
    main()
