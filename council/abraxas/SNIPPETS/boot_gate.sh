#!/usr/bin/env bash
# Excerpt from tools/abraxas — the CLI launcher.
# Full source discussed in EVIDENCE/boot_hard_fail.md.
# Redactions: none (paths only, no credentials).
set -euo pipefail

ROOT="<workspace-root>"
GSD_BIN="${GSD_BIN:-/opt/homebrew/bin/gsd}"
BOOTSTRAP_FILE="$ROOT/Agents/ABRAXAS_GSD_BOOTSTRAP.md"
AGENTS_FILE="${ABRAXAS_AGENTS_FILE:-<agents-config>}"
CONTINUITY_FILE="$ROOT/Agents/ABRAXAS_CONTINUITY_MANIFEST.md"
PILLAR_FILE="$ROOT/FIVE_PRINCIPLES.md"
ECOLOGICAL_MODEL_FILE="$ROOT/Shared Knowledge/4th House/LOS_VERI_ECOLOGICAL_MEMORY_MODEL.md"
ECOLOGICAL_MANIFEST_FILE="$ROOT/memory/MANIFEST.json"
MACROSYSTEM_FILE="$ROOT/memory/macrosystem/current_phase.json"
CHRONOSYSTEM_FILE="$ROOT/memory/chronosystem/family_arc.json"

require_file() {
  local path="$1"
  local label="$2"
  if [[ ! -f "$path" ]]; then
    echo "abraxas: $label missing at $path" >&2
    exit 1
  fi
}

if [[ ! -x "$GSD_BIN" ]]; then
  echo "abraxas: gsd not found at $GSD_BIN" >&2
  exit 1
fi

# Boot hard-fails here — before any model call — if the constitution
# or any of the memory-index files are missing from disk.
require_file "$BOOTSTRAP_FILE" "bootstrap file"
require_file "$AGENTS_FILE" "agents file"
require_file "$CONTINUITY_FILE" "continuity manifest"
require_file "$PILLAR_FILE" "pillar file"
require_file "$ECOLOGICAL_MODEL_FILE" "ecological model file"
require_file "$ECOLOGICAL_MANIFEST_FILE" "ecological manifest file"
require_file "$MACROSYSTEM_FILE" "macrosystem file"
require_file "$CHRONOSYSTEM_FILE" "chronosystem file"

# ... later, once boot passes, the pillar is read in full and injected
# into the prompt inside explicit delimiters, ahead of the user's turn:
#
#   pillar_prompt="$(<"$PILLAR_FILE")"
#   printf -v final_prompt '...--- BEGIN PILLAR ---\n%s\n--- END PILLAR ---...' \
#     "$pillar_prompt" ...
#
# This is a prompt-injection convention, not a code-validated constraint on
# the model's output — see the README's "Enforcement, honestly" section.
