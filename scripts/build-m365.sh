#!/usr/bin/env bash
# Build Microsoft 365 Copilot (Cowork) packages from the Claude plugins.
#
# Usage:
#   PRIVACY_URL=https://example.com/privacy \
#   TERMS_URL=https://example.com/terms \
#   WEBSITE_URL=https://example.com \
#     scripts/build-m365.sh [plugin-name ...]
#
# Output: build/m365/<plugin-name>.zip. Upload each zip in the Microsoft 365
# admin center under Manage apps > Upload custom app.
#
# Requires: python3, node, and @microsoft/m365agentstoolkit-cli 1.1.12 or later
#   npm install -g @microsoft/m365agentstoolkit-cli
#
# Steps per plugin:
#   1. atk import openplugin   converts the Claude plugin to a Microsoft project
#   2. patch manifest          sets schema v1.28 and the display name
#   3. atk validate            checks the manifest against the schema
#   4. atk package             writes the zip

set -euo pipefail

: "${PRIVACY_URL:?Set PRIVACY_URL to the privacy policy URL}"
: "${TERMS_URL:?Set TERMS_URL to the terms of use URL}"
: "${WEBSITE_URL:?Set WEBSITE_URL to the company website URL}"

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="${root}/build/m365"

if ! command -v atk >/dev/null 2>&1; then
  echo "error: atk not found. Run: npm install -g @microsoft/m365agentstoolkit-cli" >&2
  exit 1
fi

if [ "$#" -gt 0 ]; then
  plugins=("$@")
else
  mapfile -t plugins < <(find "${root}/plugins" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort)
fi

mkdir -p "${out}"

for plugin in "${plugins[@]}"; do
  src="${root}/plugins/${plugin}"
  project="${out}/${plugin}-project"

  if [ ! -d "${src}" ]; then
    echo "error: plugin '${plugin}' not found in plugins/" >&2
    exit 1
  fi

  echo "Building ${plugin}"
  rm -rf "${project}"

  atk import openplugin \
    --path "${src}" \
    --output "${project}" \
    --privacy-url "${PRIVACY_URL}" \
    --terms-url "${TERMS_URL}" \
    --website-url "${WEBSITE_URL}"

  # The importer writes a devPreview manifest and derives the display name from
  # the plugin name ("Hr Recruiting"). Use schema v1.28 and the displayName.
  python3 - "${src}/.claude-plugin/plugin.json" "${project}/appPackage/manifest.json" <<'PY'
import json
import sys

plugin_path, manifest_path = sys.argv[1:3]
plugin = json.load(open(plugin_path, encoding="utf-8"))
manifest = json.load(open(manifest_path, encoding="utf-8"))

manifest["manifestVersion"] = "1.28"
manifest["$schema"] = "https://developer.microsoft.com/json-schemas/teams/v1.28/MicrosoftTeams.schema.json"
display = plugin.get("displayName") or manifest["name"]["short"]
manifest["name"] = {"short": display, "full": display}

with open(manifest_path, "w", encoding="utf-8") as handle:
    json.dump(manifest, handle, indent=2)
    handle.write("\n")
PY

  # atk package must run inside the project folder (it needs m365agents.yml).
  (
    cd "${project}"
    atk validate --manifest-file ./appPackage/manifest.json
    atk package \
      --manifest-file ./appPackage/manifest.json \
      --output-package-file ./appPackage/build/appPackage.zip \
      --output-folder ./appPackage/build
  )

  cp "${project}/appPackage/build/appPackage.zip" "${out}/${plugin}.zip"
done

echo "Packages written to ${out}"
