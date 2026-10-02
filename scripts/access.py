#!/usr/bin/env python3
"""Check and explain the Enterprise plugin access policy.

The policy lives in enterprise/plugin-access.yaml. It records what an admin sets
in Claude's Organization settings > Plugins & skills on Enterprise.

Usage:
    uv run scripts/access.py check                       # validate the policy
    uv run scripts/access.py matrix                      # print the access matrix
    uv run scripts/access.py matrix --write              # regenerate docs/enterprise/access-matrix.md
    uv run scripts/access.py matrix --check              # fail if that file is out of date
    uv run scripts/access.py resolve claude-hr claude-sales   # what a member of these groups gets
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / "enterprise" / "plugin-access.yaml"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
MATRIX_DOC = ROOT / "docs" / "enterprise" / "access-matrix.md"

# Most permissive first. Claude applies the most permissive value across a member's groups.
LEVELS = ["required", "installed-by-default", "available-to-install", "not-available"]
RANK = {level: len(LEVELS) - i for i, level in enumerate(LEVELS)}
# A pilot plugin is hidden from everyone except pilot groups. Promotion to released
# is a reviewed change to this field plus the department grants.
STAGES = ("pilot", "released")
# Labels as the Claude admin console shows them.
LABEL = {
    "required": "Required",
    "installed-by-default": "Installed by default",
    "available-to-install": "Available to install",
    "not-available": "Not available",
}


def load_policy(path: Path = POLICY) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def marketplace_plugins() -> list[str]:
    data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    return [entry["name"] for entry in data.get("plugins", [])]


def check_policy(policy: dict, plugins: list[str]) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for the policy against the marketplace plugin list."""
    errors: list[str] = []
    warnings: list[str] = []
    where = "enterprise/plugin-access.yaml"

    if policy.get("version") != 1:
        errors.append(f"{where}: version must be 1")
    groups = policy.get("groups") or {}
    rules = policy.get("plugins") or {}
    if not groups:
        errors.append(f"{where}: no groups defined")

    for name in plugins:
        if name not in rules:
            errors.append(f"{where}: plugin '{name}' has no access rule. Add it, even if only a default.")
    for name in rules:
        if name not in plugins:
            errors.append(f"{where}: plugin '{name}' is not in marketplace.json. Remove the rule or add the plugin.")

    pilot_groups = {g for g, meta in groups.items() if (meta or {}).get("pilot")}
    used_groups: set[str] = set()
    for name, rule in rules.items():
        rule = rule or {}
        default = rule.get("default")
        if default not in RANK:
            errors.append(f"{where}: {name}: default '{default}' must be one of {', '.join(LEVELS)}")
            continue
        overrides = rule.get("groups") or {}
        stage = rule.get("stage", "released")
        if stage not in STAGES:
            errors.append(f"{where}: {name}: stage '{stage}' must be one of {', '.join(STAGES)}")
        elif stage == "pilot":
            if default != "not-available":
                errors.append(f"{where}: {name}: stage pilot needs default: not-available")
            outside = [g for g in overrides if g not in pilot_groups]
            if outside:
                errors.append(
                    f"{where}: {name}: stage pilot may grant only pilot groups, not {', '.join(outside)}. "
                    "Set stage: released to grant departments."
                )
            if not any(g in pilot_groups for g in overrides):
                errors.append(f"{where}: {name}: stage pilot needs a grant to a pilot group")
        for group, level in overrides.items():
            used_groups.add(group)
            if group not in groups:
                errors.append(f"{where}: {name}: group '{group}' is not defined under groups")
            if level not in RANK:
                errors.append(f"{where}: {name}: {group} '{level}' must be one of {', '.join(LEVELS)}")
                continue
            if RANK[level] < RANK[default]:
                errors.append(
                    f"{where}: {name}: {group} is '{level}', narrower than the default '{default}'. "
                    "A member in any other group still gets the default, because the most permissive "
                    "value wins. Set default: not-available and grant the groups that need it."
                )
            if level == default:
                warnings.append(f"{where}: {name}: {group} override equals the default. Remove it.")
        levels = [default, *overrides.values()]
        if "required" in levels:
            hooks = (ROOT / "plugins" / name / "hooks").exists()
            note = " It has hooks/: review them first." if hooks else ""
            warnings.append(
                f"{where}: {name}: 'required' also installs it in Claude Code, where members cannot "
                f"disable it and its hooks and MCP servers run on their machine.{note}"
            )

    for group in groups:
        if group not in used_groups and group not in pilot_groups:
            warnings.append(f"{where}: group '{group}' is not used by any plugin rule")
    return errors, warnings


def resolve(rule: dict, member_groups: list[str]) -> str:
    """Effective access for a member of member_groups."""
    default = rule["default"]
    overrides = rule.get("groups") or {}
    if not member_groups:
        return default
    values = [overrides.get(group, default) for group in member_groups]
    return max(values, key=lambda level: RANK[level])


def render_matrix(policy: dict) -> str:
    groups = list(policy["groups"])
    rules = policy["plugins"]
    lines = [
        "# Plugin access matrix",
        "",
        "Generated from [`enterprise/plugin-access.yaml`](../../enterprise/plugin-access.yaml) by "
        "`uv run scripts/access.py matrix --write`. Do not edit by hand.",
        "",
        "Each cell is what a member of only that group gets. **Bold** is a group override; "
        "plain text is the org default. A member in several groups gets the most permissive cell "
        "in their row.",
        "",
        "Most to least permissive: Required > Installed by default > Available to install > Not available.",
        "",
        "| Plugin | Stage | Org default | " + " | ".join(f"`{g}`" for g in groups) + " |",
        "| --- | --- | --- | " + " | ".join("---" for _ in groups) + " |",
    ]
    for name, rule in rules.items():
        overrides = rule.get("groups") or {}
        cells = []
        for group in groups:
            level = resolve(rule, [group])
            cells.append(f"**{LABEL[level]}**" if group in overrides else LABEL[level])
        stage = rule.get("stage", "released")
        lines.append(f"| `{name}` | {stage} | {LABEL[rule['default']]} | " + " | ".join(cells) + " |")

    lines += ["", "## Console settings", "", "Set these in Organization settings > Plugins & skills > Inventory.", ""]
    for name, rule in rules.items():
        lines.append(f"- `{name}`: Default access **{LABEL[rule['default']]}**.")
        for group, level in (rule.get("groups") or {}).items():
            lines.append(f"  - Group access: `{group}` **{LABEL[level]}**.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="validate the policy")
    matrix = sub.add_parser("matrix", help="print or write the access matrix")
    mode = matrix.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help=f"write {MATRIX_DOC.relative_to(ROOT)}")
    mode.add_argument("--check", action="store_true", help="fail if the written matrix is out of date")
    res = sub.add_parser("resolve", help="show what a member of the given groups gets")
    res.add_argument("groups", nargs="*", help="group names; none means a member in no group")
    args = parser.parse_args()

    policy = load_policy()
    errors, warnings = check_policy(policy, marketplace_plugins())

    if args.command == "check":
        for message in warnings:
            print(f"warning: {message}")
        for message in errors:
            print(f"error: {message}")
        print(f"\n{len(errors)} errors, {len(warnings)} warnings.")
        return 1 if errors else 0

    if errors:
        for message in errors:
            print(f"error: {message}")
        print("Fix the policy first: uv run scripts/access.py check")
        return 1

    if args.command == "matrix":
        text = render_matrix(policy)
        if args.write:
            MATRIX_DOC.parent.mkdir(parents=True, exist_ok=True)
            MATRIX_DOC.write_text(text, encoding="utf-8")
            print(f"Wrote {MATRIX_DOC.relative_to(ROOT)}")
        elif args.check:
            current = MATRIX_DOC.read_text(encoding="utf-8") if MATRIX_DOC.exists() else ""
            if current != text:
                print(f"error: {MATRIX_DOC.relative_to(ROOT)} is out of date. Run: uv run scripts/access.py matrix --write")
                return 1
            print(f"{MATRIX_DOC.relative_to(ROOT)} is up to date.")
        else:
            print(text, end="")
        return 0

    unknown = [g for g in args.groups if g not in policy["groups"]]
    if unknown:
        print(f"error: unknown group(s): {', '.join(unknown)}. Defined: {', '.join(policy['groups'])}")
        return 1
    who = ", ".join(args.groups) if args.groups else "no groups"
    print(f"Member of: {who}\n")
    width = max(len(name) for name in policy["plugins"])
    for name, rule in policy["plugins"].items():
        print(f"  {name.ljust(width)}  {LABEL[resolve(rule, args.groups)]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
