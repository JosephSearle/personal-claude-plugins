#!/usr/bin/env python3
"""Package Claude plugins as zips for upload in claude.ai.

A pilot tester uploads the zip for themselves (Customize > Plugins) to try a
change before it merges. An admin can upload one to an organization marketplace.

Usage:
    uv run scripts/package-plugin.py hr-recruiting core       # named plugins
    uv run scripts/package-plugin.py --changed --base origin/main   # plugins changed on this branch

Output: build/claude/<plugin>-<version>.zip, with .claude-plugin/ and skills/ at
the zip root.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
OUT = ROOT / "build" / "claude"
MAX_BYTES = 200 * 1024 * 1024  # claude.ai upload limit
SKIP = {".DS_Store", "__pycache__"}


def changed_plugins(base: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD", "--", "plugins/"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(f"error: cannot diff against '{base}': {result.stderr.strip()}")
    names = {Path(line).parts[1] for line in result.stdout.splitlines() if len(Path(line).parts) > 2}
    return sorted(n for n in names if (PLUGINS / n).is_dir())


def package(name: str) -> Path:
    src = PLUGINS / name
    manifest = src / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        sys.exit(f"error: plugins/{name}/.claude-plugin/plugin.json not found")
    version = json.loads(manifest.read_text(encoding="utf-8"))["version"]
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{name}-{version}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(src.rglob("*")):
            if path.is_file() and not SKIP.intersection(path.parts):
                zf.write(path, path.relative_to(src).as_posix())
    if target.stat().st_size > MAX_BYTES:
        sys.exit(f"error: {target.name} exceeds the 200 MB upload limit")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("plugins", nargs="*", help="plugin names under plugins/")
    parser.add_argument("--changed", action="store_true", help="package plugins changed since --base")
    parser.add_argument("--base", default="origin/main", help="Git ref for --changed (default: origin/main)")
    args = parser.parse_args()

    names = changed_plugins(args.base) if args.changed else args.plugins
    if not names:
        print("No plugins to package.")
        return 0
    for name in names:
        if not (PLUGINS / name).is_dir():
            sys.exit(f"error: plugin '{name}' not found in plugins/")
        print(f"Wrote {package(name).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
