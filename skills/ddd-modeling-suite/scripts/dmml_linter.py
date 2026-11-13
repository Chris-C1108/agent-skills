#!/usr/bin/env python3
"""
dmml_linter.py (V2)
Deterministic static graph & invariant analyzer for DMML domain model files.
Enforces:
  1. Cross-context DAG check (circular dependency detection).
  2. Identity-only cross-aggregate/entity reference rule.
  3. Complete state machine graph verification (BFS reachability, ghost states, dead ends, guard determinism).
  4. Lineage traceability (traces_to) & INVALIDATED upstream event/fact interception.
"""

import argparse
import ast
import glob
import os
import re
import sys
from collections import deque
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


DEFAULT_TERMINAL_NAMES = {
    "TERMINATED",
    "COMPLETED",
    "CLOSED",
    "CANCELLED",
    "CANCELED",
    "ARCHIVED",
    "FAILED",
    "VOIDED",
    "EXPIRED",
}

SCALAR_TYPES = {
    "string",
    "str",
    "int",
    "integer",
    "long",
    "float",
    "double",
    "decimal",
    "number",
    "bool",
    "boolean",
    "uuid",
    "date",
    "datetime",
    "timestamp",
    "bytes",
    "json",
    "map",
}


def _parse_scalar(val_str: str) -> Any:
    val_str = val_str.strip()
    if not val_str:
        return ""
    if val_str in ("true", "True"):
        return True
    if val_str in ("false", "False"):
        return False
    if val_str in ("null", "None", "~"):
        return None
    if (val_str.startswith('"') and val_str.endswith('"')) or (
        val_str.startswith("'") and val_str.endswith("'")
    ):
        return val_str[1:-1]
    if val_str.startswith("[") and val_str.endswith("]"):
        try:
            return ast.literal_eval(val_str)
        except Exception:
            inner = val_str[1:-1].strip()
            if not inner:
                return []
            return [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
    if val_str.startswith("{") and val_str.endswith("}"):
        try:
            return ast.literal_eval(val_str)
        except Exception:
            return {}
    if re.fullmatch(r"-?\d+", val_str):
        return int(val_str)
    return val_str


def _strip_inline_comment(line: str) -> str:
    in_single = False
    in_double = False
    for idx, ch in enumerate(line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            if idx == 0 or line[idx - 1].isspace():
                return line[:idx].rstrip()
    return line.rstrip()


def fallback_parse_yaml(content: str) -> Any:
    """
    Lightweight indentation-based YAML subset parser for DMML files when PyYAML is unavailable.
    Supports nested dicts, lists of dicts, lists of scalars, and inline arrays.
    """
    cleaned_lines: List[Tuple[int, str]] = []
    for raw in content.splitlines():
        stripped_comment = _strip_inline_comment(raw)
        if not stripped_comment.strip():
            continue
        indent = len(stripped_comment) - len(stripped_comment.lstrip(" "))
        cleaned_lines.append((indent, stripped_comment.strip()))

    if not cleaned_lines:
        return {}

    def parse_node(index: int, min_indent: int) -> Tuple[Any, int]:
        if index >= len(cleaned_lines):
            return {}, index
        first_indent, first_text = cleaned_lines[index]
        if first_indent < min_indent:
            return {}, index

        if first_text.startswith("- ") or first_text == "-":
            result_list: List[Any] = []
            while index < len(cleaned_lines):
                ind, txt = cleaned_lines[index]
                if ind < first_indent or not (txt.startswith("- ") or txt == "-"):
                    break
                if ind > first_indent:
                    break
                item_body = txt[1:].strip()
                index += 1
                if not item_body:
                    sub_val, index = parse_node(index, ind + 1)
                    result_list.append(sub_val)
                elif ":" in item_body and not (
                    item_body.startswith('"') or item_body.startswith("'")
                ):
                    k, v = item_body.split(":", 1)
                    k = k.strip().strip("'\"")
                    v = v.strip()
                    item_dict: Dict[str, Any] = {}
                    if v:
                        item_dict[k] = _parse_scalar(v)
                    else:
                        sub_val, index = parse_node(index, ind + 1)
                        item_dict[k] = sub_val
                    if index < len(cleaned_lines) and cleaned_lines[index][0] > ind:
                        extra_dict, index = parse_node(index, ind + 1)
                        if isinstance(extra_dict, dict):
                            item_dict.update(extra_dict)
                    result_list.append(item_dict)
                else:
                    result_list.append(_parse_scalar(item_body))
            return result_list, index
        else:
            result_dict: Dict[str, Any] = {}
            while index < len(cleaned_lines):
                ind, txt = cleaned_lines[index]
                if ind < first_indent or txt.startswith("- ") or txt == "-":
                    break
                if ind > first_indent:
                    break
                if ":" not in txt:
                    index += 1
                    continue
                k, v = txt.split(":", 1)
                k = k.strip().strip("'\"")
                v = v.strip()
                index += 1
                if v:
                    result_dict[k] = _parse_scalar(v)
                else:
                    sub_val, index = parse_node(index, ind + 1)
                    result_dict[k] = sub_val
            return result_dict, index

    parsed, _ = parse_node(0, 0)
    return parsed


def load_yaml_file(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if yaml is not None:
        return yaml.safe_load(content)
    return fallback_parse_yaml(content)


def load_events_ledger(events_file: Optional[str]) -> Tuple[Set[str], Set[str]]:
    """
    Returns (valid_ids, invalidated_ids) from .ddd/02-events.yaml if available.
    """
    valid_ids: Set[str] = set()
    invalidated_ids: Set[str] = set()
    if not events_file or not os.path.exists(events_file):
        return valid_ids, invalidated_ids

    try:
        data = load_yaml_file(events_file)
    except Exception:
        return valid_ids, invalidated_ids

    if not isinstance(data, dict):
        return valid_ids, invalidated_ids

    for ev in data.get("events", []) or []:
        if not isinstance(ev, dict):
            continue
        evt_id = str(ev.get("id", "")).strip()
        fact_id = str(ev.get("fact_id", "")).strip()
        status = str(ev.get("status", "ACTIVE")).strip().upper()
        for identifier in (evt_id, fact_id):
            if identifier:
                valid_ids.add(identifier)
                if status == "INVALIDATED":
                    invalidated_ids.add(identifier)
        for tr in ev.get("traces_to", []) or []:
            tr_str = str(tr).strip()
            if tr_str:
                valid_ids.add(tr_str)
                if status == "INVALIDATED":
                    invalidated_ids.add(tr_str)

    for rm in data.get("read_models", []) or []:
        if isinstance(rm, dict) and rm.get("id"):
            valid_ids.add(str(rm["id"]).strip())

    return valid_ids, invalidated_ids


def extract_base_type(type_expr: str) -> str:
    """Extract inner type from expressions like 'list<Order>' or 'Order[]'."""
    cleaned = type_expr.strip()
    generic_match = re.match(r"^(?:list|array|set|collection)<(.+)>$", cleaned, re.IGNORECASE)
    if generic_match:
        return generic_match.group(1).strip()
    if cleaned.endswith("[]"):
        return cleaned[:-2].strip()
    return cleaned


def detect_context_cycles(context_deps: Dict[str, List[str]]) -> List[List[str]]:
    """Run DFS cycle detection across Bounded Context dependency graph."""
    visited: Set[str] = set()
    stack: Set[str] = set()
    path: List[str] = []
    cycles: List[List[str]] = []

    def dfs(node: str) -> None:
        visited.add(node)
        stack.add(node)
        path.append(node)
        for neighbor in context_deps.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in stack:
                idx = path.index(neighbor)
                cycles.append(path[idx:] + [neighbor])
        stack.remove(node)
        path.pop()

    for ctx in list(context_deps.keys()):
        if ctx not in visited:
            dfs(ctx)
    return cycles


def check_traces(
    file_path: str,
    scope_label: str,
    item: Dict[str, Any],
    valid_ids: Set[str],
    invalidated_ids: Set[str],
    errors: List[str],
    warnings: List[str],
) -> None:
    traces = item.get("traces_to")
    if not traces or not isinstance(traces, list):
        warnings.append(
            f"{file_path} [{scope_label}]: Missing 'traces_to' lineage array (e.g. ['EVT-001', 'FACT-001'])."
        )
        return
    for ref in traces:
        ref_str = str(ref).strip()
        if ref_str in invalidated_ids:
            errors.append(
                f"{file_path} [{scope_label}]: Traces to INVALIDATED upstream fact/event '{ref_str}'. Recalculate this model slice."
            )
        elif valid_ids and ref_str not in valid_ids:
            warnings.append(
                f"{file_path} [{scope_label}]: Traces to unknown ID '{ref_str}' not found in events ledger."
            )


def lint_models(
    model_files: List[str], events_file: Optional[str] = None
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    valid_ids, invalidated_ids = load_events_ledger(events_file)

    parsed_models: List[Tuple[str, Dict[str, Any]]] = []
    all_aggregate_names: Dict[str, str] = {}  # agg_name -> context_name
    all_entity_names: Dict[str, str] = {}  # entity_name -> agg_name
    context_deps: Dict[str, List[str]] = {}

    # Pass 1: Load files and collect global symbol table (Contexts, Aggregates, Entities)
    for file_path in model_files:
        try:
            data = load_yaml_file(file_path)
        except Exception as exc:
            errors.append(f"{file_path}: YAML parse error: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{file_path}: Root document must be a YAML mapping/dictionary.")
            continue

        parsed_models.append((file_path, data))
        bc = data.get("bounded_context")
        ctx_name = bc.get("name") if isinstance(bc, dict) else None
        if ctx_name:
            deps_list: List[str] = []
            for dep in bc.get("dependencies", []) or []:
                if isinstance(dep, dict) and dep.get("context"):
                    rel = str(dep.get("relationship", "")).strip()
                    # Partnership / SharedKernel are symmetric by nature; still check directed cycles for others
                    if rel not in ("Partnership", "SharedKernel"):
                        deps_list.append(str(dep["context"]).strip())
            context_deps[ctx_name] = deps_list

        for agg in data.get("aggregates", []) or []:
            if not isinstance(agg, dict):
                continue
            agg_name = agg.get("name")
            if agg_name:
                all_aggregate_names[str(agg_name)] = str(ctx_name or file_path)
            root_ent = agg.get("root_entity")
            if root_ent:
                all_aggregate_names[str(root_ent)] = str(ctx_name or file_path)
            for ent in agg.get("entities", []) or []:
                if isinstance(ent, dict) and ent.get("name"):
                    all_entity_names[str(ent["name"])] = str(agg_name or "<UnknownAggregate>")

    # Pass 2: Cross-Context Circular Dependency Check
    cycles = detect_context_cycles(context_deps)
    for cycle in cycles:
        cycle_str = " -> ".join(cycle)
        errors.append(f"[Cross-Context Cycle] Circular dependency detected: {cycle_str}")

    # Pass 3: Detailed Tactical Linting per File
    for file_path, data in parsed_models:
        bc = data.get("bounded_context")
        if not bc or not isinstance(bc, dict) or not bc.get("name"):
            errors.append(f"{file_path}: Missing required 'bounded_context.name'.")
            ctx_name = "<UnknownContext>"
        else:
            ctx_name = str(bc["name"])

        ul = data.get("ubiquitous_language", [])
        if not ul or not isinstance(ul, list):
            warnings.append(f"{file_path} [{ctx_name}]: 'ubiquitous_language' glossary is empty.")

        aggregates = data.get("aggregates", [])
        read_models = data.get("read_models", [])
        if (not aggregates or not isinstance(aggregates, list)) and (
            not read_models or not isinstance(read_models, list)
        ):
            errors.append(
                f"{file_path} [{ctx_name}]: Model must declare at least one entry in 'aggregates' or 'read_models'."
            )
            continue

        for agg in aggregates or []:
            if not isinstance(agg, dict):
                continue
            agg_name = str(agg.get("name", "<UnnamedAggregate>"))
            root_entity = agg.get("root_entity")
            if not root_entity:
                errors.append(f"{file_path} [{agg_name}]: Aggregate missing 'root_entity'.")

            local_vo_names: Set[str] = {
                str(vo.get("name"))
                for vo in (agg.get("value_objects", []) or [])
                if isinstance(vo, dict) and vo.get("name")
            }
            local_entity_names: Set[str] = {
                str(ent.get("name"))
                for ent in (agg.get("entities", []) or [])
                if isinstance(ent, dict) and ent.get("name")
            }

            # 3.1 Invariants & Lineage check
            invariants = agg.get("invariants", [])
            if not invariants or not isinstance(invariants, list):
                errors.append(
                    f"{file_path} [{agg_name}]: Aggregate must define at least one atomic invariant in 'invariants'."
                )
            else:
                for inv in invariants:
                    if not isinstance(inv, dict):
                        continue
                    inv_id = inv.get("id", "<UnnamedInvariant>")
                    if not inv.get("assertion"):
                        errors.append(
                            f"{file_path} [{agg_name}.{inv_id}]: Invariant missing 'assertion' expression."
                        )
                    check_traces(
                        file_path,
                        f"{agg_name}.{inv_id}",
                        inv,
                        valid_ids,
                        invalidated_ids,
                        errors,
                        warnings,
                    )

            # 3.2 ID-Only Reference Check on Entities
            for ent in agg.get("entities", []) or []:
                if not isinstance(ent, dict):
                    continue
                ent_name = str(ent.get("name", "<UnnamedEntity>"))
                if not ent.get("identifier"):
                    errors.append(
                        f"{file_path} [{agg_name}.{ent_name}]: Entity missing 'identifier' field."
                    )
                for prop in ent.get("properties", []) or []:
                    if not isinstance(prop, dict):
                        continue
                    prop_name = str(prop.get("name", "")).strip()
                    prop_type = str(prop.get("type", "")).strip()
                    base_type = extract_base_type(prop_type)

                    # Check if base_type directly references another Aggregate Root or foreign Entity
                    is_foreign_agg = (
                        base_type in all_aggregate_names and base_type != agg_name and base_type != root_entity
                    )
                    is_foreign_entity = (
                        base_type in all_entity_names and base_type not in local_entity_names
                    )
                    if (is_foreign_agg or is_foreign_entity) and base_type not in local_vo_names:
                        errors.append(
                            f"{file_path} [{agg_name}.{ent_name}.{prop_name}]: Direct object reference to "
                            f"Aggregate/Entity type '{prop_type}' violates ID-Only rule. Use scalar identity (e.g. '{prop_name}_id: string')."
                        )
                    elif (
                        base_type.lower() not in SCALAR_TYPES
                        and base_type not in local_vo_names
                        and base_type not in local_entity_names
                        and not prop_name.endswith("_id")
                        and not prop_name.endswith("_ids")
                    ):
                        # Heuristic check: property named after another aggregate or object type without _id suffix
                        if any(
                            agg_candidate.lower() == base_type.lower()
                            for agg_candidate in all_aggregate_names
                        ):
                            errors.append(
                                f"{file_path} [{agg_name}.{ent_name}.{prop_name}]: Cross-aggregate reference '{prop_name}: {prop_type}' "
                                "must use scalar ID suffix ('*_id')."
                            )

            # 3.3 State Machine Verification (Reachability, Ghost States, Dead Ends, Determinism)
            sm = agg.get("state_machine")
            if sm and isinstance(sm, dict):
                raw_states = sm.get("states", []) or []
                states: Set[str] = {str(s) for s in raw_states}
                initial = str(sm.get("initial_state", "")).strip()
                raw_terminals = sm.get("terminal_states")
                if isinstance(raw_terminals, list) and raw_terminals:
                    terminal_states: Set[str] = {str(s) for s in raw_terminals}
                else:
                    terminal_states = {s for s in states if s.upper() in DEFAULT_TERMINAL_NAMES}

                if not initial:
                    errors.append(f"{file_path} [{agg_name}]: State machine missing 'initial_state'.")
                elif initial not in states:
                    errors.append(
                        f"{file_path} [{agg_name}]: initial_state '{initial}' is not listed in 'states'."
                    )

                for term in terminal_states:
                    if term not in states:
                        errors.append(
                            f"{file_path} [{agg_name}]: terminal_state '{term}' is not listed in 'states'."
                        )

                transitions = sm.get("transitions", []) or []
                adj: Dict[str, Set[str]] = {s: set() for s in states}
                outbound_distinct: Dict[str, Set[str]] = {s: set() for s in states}
                trigger_guards: Dict[Tuple[str, str], List[str]] = {}

                for tr in transitions:
                    if not isinstance(tr, dict):
                        continue
                    f_state = str(tr.get("from", "")).strip()
                    t_state = str(tr.get("to", "")).strip()
                    trigger = str(tr.get("trigger", "")).strip()
                    guard = str(tr.get("guard", "")).strip()

                    if f_state not in states:
                        errors.append(
                            f"{file_path} [{agg_name}]: Transition 'from: {f_state}' references undeclared state."
                        )
                    if t_state not in states:
                        errors.append(
                            f"{file_path} [{agg_name}]: Transition 'to: {t_state}' references undeclared state."
                        )
                    if not trigger:
                        errors.append(
                            f"{file_path} [{agg_name}]: Transition {f_state} -> {t_state} is missing 'trigger'."
                        )

                    if f_state in states and t_state in states:
                        adj[f_state].add(t_state)
                        if t_state != f_state:
                            outbound_distinct[f_state].add(t_state)

                    if f_state and trigger:
                        trigger_guards.setdefault((f_state, trigger), []).append(guard)

                # Non-deterministic branching check
                for (f_state, trigger), guards in trigger_guards.items():
                    if len(guards) > 1:
                        if any(not g or g.lower() == "true" for g in guards) or len(set(guards)) < len(guards):
                            errors.append(
                                f"{file_path} [{agg_name}]: Non-deterministic transitions from state '{f_state}' on trigger '{trigger}' "
                                "require mutually exclusive, non-empty 'guard' conditions."
                            )

                # BFS Reachability from initial_state
                if initial and initial in states:
                    reachable: Set[str] = {initial}
                    queue: deque[str] = deque([initial])
                    while queue:
                        curr = queue.popleft()
                        for nxt in adj.get(curr, set()):
                            if nxt not in reachable:
                                reachable.add(nxt)
                                queue.append(nxt)

                    unreachable = sorted(states - reachable)
                    for u_state in unreachable:
                        errors.append(
                            f"{file_path} [{agg_name}]: State '{u_state}' is unreachable from initial_state '{initial}'."
                        )

                # Dead-end check for non-terminal states
                if len(states) > 1:
                    for s in sorted(states):
                        if s not in terminal_states and not outbound_distinct.get(s):
                            warnings.append(
                                f"{file_path} [{agg_name}]: Non-terminal state '{s}' has no outbound transition to another state (dead-end)."
                            )

            # 3.4 Commands & Domain Events Lineage Check
            for cmd in agg.get("commands", []) or []:
                if isinstance(cmd, dict):
                    cmd_name = cmd.get("name", "<UnnamedCommand>")
                    check_traces(
                        file_path,
                        f"{agg_name}.{cmd_name}",
                        cmd,
                        valid_ids,
                        invalidated_ids,
                        errors,
                        warnings,
                    )

            for evt in agg.get("domain_events", []) or []:
                if isinstance(evt, dict):
                    evt_name = evt.get("name", "<UnnamedEvent>")
                    if not str(evt_name)[0:1].isupper():
                        warnings.append(
                            f"{file_path} [{agg_name}.{evt_name}]: Domain event should use PascalCase past-tense naming."
                        )
                    check_traces(
                        file_path,
                        f"{agg_name}.{evt_name}",
                        evt,
                        valid_ids,
                        invalidated_ids,
                        errors,
                        warnings,
                    )

        # 3.5 Policies & Read Models Lineage Check
        for pol in data.get("policies", []) or []:
            if isinstance(pol, dict):
                pol_name = pol.get("name") or pol.get("id") or "<UnnamedPolicy>"
                check_traces(
                    file_path,
                    f"Policy:{pol_name}",
                    pol,
                    valid_ids,
                    invalidated_ids,
                    errors,
                    warnings,
                )

        for rm in read_models or []:
            if isinstance(rm, dict):
                rm_name = rm.get("name", "<UnnamedReadModel>")
                check_traces(
                    file_path,
                    f"ReadModel:{rm_name}",
                    rm,
                    valid_ids,
                    invalidated_ids,
                    errors,
                    warnings,
                )

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic Linter for DMML v2 Domain Models")
    parser.add_argument(
        "--models-dir",
        required=True,
        help="Directory containing DMML .yaml files (.ddd/04-models/)",
    )
    parser.add_argument(
        "--events-file",
        required=False,
        default=None,
        help="Optional path to .ddd/02-events.yaml for lineage & invalidation verification",
    )
    args = parser.parse_args()

    if not os.path.exists(args.models_dir):
        print(f"[ERROR] Models directory not found: {args.models_dir}", file=sys.stderr)
        sys.exit(1)

    yaml_files = sorted(
        glob.glob(os.path.join(args.models_dir, "*.yaml"))
        + glob.glob(os.path.join(args.models_dir, "*.yml"))
    )

    if not yaml_files:
        print(f"[ERROR] No DMML YAML files found in {args.models_dir}", file=sys.stderr)
        sys.exit(1)

    events_file = args.events_file
    if not events_file:
        candidate = os.path.abspath(os.path.join(args.models_dir, "..", "02-events.yaml"))
        if os.path.exists(candidate):
            events_file = candidate

    all_errors, all_warnings = lint_models(yaml_files, events_file)

    print("=== DMML Deterministic Linter Report (v2.0) ===")
    print(f"Models scanned: {len(yaml_files)}")
    if events_file and os.path.exists(events_file):
        print(f"Lineage ledger: {events_file}")

    for w in all_warnings:
        print(f"[WARN]  {w}")
    for e in all_errors:
        print(f"[ERROR] {e}")

    if all_errors:
        print(f"\n[FAILED] Found {len(all_errors)} error(s) and {len(all_warnings)} warning(s).")
        sys.exit(1)

    print(f"\n[PASSED] All {len(yaml_files)} DMML model(s) passed deterministic verification ({len(all_warnings)} warning(s)).")
    sys.exit(0)


if __name__ == "__main__":
    main()
