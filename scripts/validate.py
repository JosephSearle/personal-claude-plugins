#!/usr/bin/env python3
"""Validate the plugin marketplace.

Checks the rules both Claude org sync and Microsoft 365 Copilot (Cowork)
enforce, plus repo governance rules.

Usage:
    python scripts/validate.py
    python scripts/validate.py --base origin/main   # also require version bumps
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CODEOWNERS = ROOT / ".github" / "CODEOWNERS"

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_SKILLS_M365 = 20
RECOMMENDED_SKILLS = 10

# Components that Copilot (Cowork) does not load. Essential logic must live in skills.
UNSUPPORTED_IN_COPILOT = ("commands", "agents", "hooks")

SECRET_PATTERNS = {
    "email address": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "API key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "credential assignment": re.compile(
        r"(?i)\b(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_-]{8,}"
    ),
    "UK National Insurance number": re.compile(r"\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b"),
}

# Placeholder domains used in documentation examples; not real addresses.
PLACEHOLDER_EMAIL_DOMAINS = ("example.com", "example.org", "example.net", "project.org")

# Phrases that tell Claude when to load a skill.
TRIGGER_PHRASE = re.compile(r"\b(use (this skill )?when(ever)?|triggers?|whenever|asks? (to|for)|wants? (to|a))\b", re.I)

errors: list[str] = []
warnings: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        error(f"{path.relative_to(ROOT)}: file not found")
    except json.JSONDecodeError as exc:
        error(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
    return {}


def check_name(kind: str, name: str, where: str) -> None:
    if not KEBAB.match(name):
        error(f"{where}: {kind} name '{name}' must be kebab-case")
    if len(name) > MAX_NAME:
        error(f"{where}: {kind} name '{name}' exceeds {MAX_NAME} characters")


def check_skill(skill_dir: Path, where: str) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        error(f"{where}: {skill_dir.name} has no SKILL.md")
        return
    match = FRONTMATTER.match(skill_file.read_text(encoding="utf-8"))
    if not match:
        error(f"{skill_file.relative_to(ROOT)}: missing YAML frontmatter")
        return
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        error(f"{skill_file.relative_to(ROOT)}: invalid frontmatter ({exc})")
        return

    name = meta.get("name")
    description = meta.get("description")
    if not name:
        error(f"{skill_file.relative_to(ROOT)}: missing 'name'")
    else:
        check_name("skill", str(name), str(skill_file.relative_to(ROOT)))
        if name != skill_dir.name:
            error(f"{skill_file.relative_to(ROOT)}: name '{name}' must match folder '{skill_dir.name}'")
    if not description:
        error(f"{skill_file.relative_to(ROOT)}: missing 'description'")
    else:
        text = str(description).strip()
        if not 1 <= len(text) <= MAX_DESCRIPTION:
            error(f"{skill_file.relative_to(ROOT)}: description must be 1-{MAX_DESCRIPTION} characters")
        if not TRIGGER_PHRASE.search(text):
            warn(f"{skill_file.relative_to(ROOT)}: description has no trigger phrases (e.g. 'Use when ...')")


def check_plugin(entry: dict, seen: set[str]) -> None:
    name = entry.get("name", "")
    where = f"marketplace entry '{name}'"
    check_name("plugin", name, where)
    if name in seen:
        error(f"{where}: duplicate plugin name")
    seen.add(name)

    source = entry.get("source", "")
    if not str(source).startswith("./"):
        error(f"{where}: source must be a relative path starting with './'")
        return
    plugin_dir = ROOT / source
    if not plugin_dir.is_dir():
        error(f"{where}: source '{source}' does not exist")
        return

    manifest = load_json(plugin_dir / ".claude-plugin" / "plugin.json")
    if manifest.get("name") != name:
        error(f"{where}: plugin.json name '{manifest.get('name')}' does not match marketplace name")
    version = manifest.get("version", "")
    if not SEMVER.match(str(version)):
        error(f"{where}: plugin.json version '{version}' must be MAJOR.MINOR.PATCH")
    if "version" in entry:
        error(f"{where}: set version in plugin.json only, not in marketplace.json")
    if not manifest.get("description"):
        error(f"{where}: plugin.json needs a description")

    if (plugin_dir / "bin").exists():
        error(f"{where}: top-level bin/ is rejected by Claude and Copilot")

    for component in UNSUPPORTED_IN_COPILOT:
        if (plugin_dir / component).exists():
            warn(f"{where}: {component}/ is not loaded by Copilot. Keep essential logic in skills.")

    skills_dir = plugin_dir / "skills"
    skills = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    if not skills:
        error(f"{where}: no skills found")
    if len(skills) > MAX_SKILLS_M365:
        error(f"{where}: {len(skills)} skills exceeds the Copilot limit of {MAX_SKILLS_M365}")
    elif len(skills) > RECOMMENDED_SKILLS:
        warn(f"{where}: {len(skills)} skills. Split plugins above {RECOMMENDED_SKILLS}.")
    for skill in skills:
        check_skill(skill, where)


def check_codeowners(plugin_names: list[str]) -> None:
    if not CODEOWNERS.exists():
        error(".github/CODEOWNERS: file not found")
        return
    text = CODEOWNERS.read_text(encoding="utf-8")
    for name in plugin_names:
        if f"/plugins/{name}/" not in text:
            error(f".github/CODEOWNERS: no owner entry for /plugins/{name}/")


def check_secrets() -> None:
    suffixes = {".md", ".json", ".yml", ".yaml", ".txt", ".py", ".sh"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix not in suffixes:
            continue
        # The scanner defines the patterns it searches for.
        if path == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(text):
                if label == "email address" and match.group(0).lower().endswith(PLACEHOLDER_EMAIL_DOMAINS):
                    continue
                error(f"{path.relative_to(ROOT)}: possible {label}")
                break


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout


def check_version_bumps(base: str, plugin_names: list[str]) -> None:
    try:
        changed = git("diff", "--name-only", f"{base}...HEAD").splitlines()
    except RuntimeError as exc:
        error(f"cannot diff against '{base}': {exc}")
        return
    for name in plugin_names:
        prefix = f"plugins/{name}/"
        touched = [f for f in changed if f.startswith(prefix)]
        if not touched:
            continue
        manifest_path = f"{prefix}.claude-plugin/plugin.json"
        try:
            old = json.loads(git("show", f"{base}:{manifest_path}")).get("version")
        except (RuntimeError, json.JSONDecodeError):
            continue  # new plugin, nothing to compare
        new = load_json(ROOT / manifest_path).get("version")
        if old == new:
            error(f"plugins/{name}: files changed but version is still {new}. Bump it in plugin.json.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Git ref to compare against for version bumps")
    args = parser.parse_args()

    marketplace = load_json(MARKETPLACE)
    check_name("marketplace", marketplace.get("name", ""), "marketplace.json")
    if not marketplace.get("owner", {}).get("name"):
        error("marketplace.json: owner.name is required")

    entries = marketplace.get("plugins", [])
    if not entries:
        error("marketplace.json: no plugins listed")
    seen: set[str] = set()
    for entry in entries:
        check_plugin(entry, seen)

    names = [e.get("name", "") for e in entries]
    check_codeowners(names)
    check_secrets()
    if args.base:
        check_version_bumps(args.base, names)

    for message in warnings:
        print(f"warning: {message}")
    for message in errors:
        print(f"error: {message}")
    print(f"\n{len(entries)} plugins checked. {len(errors)} errors, {len(warnings)} warnings.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
