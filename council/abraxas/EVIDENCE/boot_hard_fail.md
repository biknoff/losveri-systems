# Boot hard-fail on the constitution — source excerpt

**What this is:** the file-existence gate near the top of `tools/abraxas` (the CLI launcher, bash), run before any model call is made. Every summon of ABRAXAS requires eight canonical files to exist on disk — the constitution (`FIVE_PRINCIPLES.md`), the continuity manifest, the agent-topology definition, and five ecological-memory index files. If any is missing, the wrapper exits `1` with a named error before `gsd` (the launcher CLI) is ever invoked — the model is never called.

**Redactions:** none — paths shown are directory-structure only, no credentials or personal content.

---

```bash
ROOT="<workspace-root>"
...
BOOTSTRAP_FILE="$ROOT/Agents/ABRAXAS_GSD_BOOTSTRAP.md"
CONTINUITY_FILE="$ROOT/Agents/ABRAXAS_CONTINUITY_MANIFEST.md"
PILLAR_FILE="$ROOT/FIVE_PRINCIPLES.md"
ECOLOGICAL_MODEL_FILE="$ROOT/Shared Knowledge/4th House/LOS_VERI_ECOLOGICAL_MEMORY_MODEL.md"
ECOLOGICAL_MANIFEST_FILE="$ROOT/memory/MANIFEST.json"
MACROSYSTEM_FILE="$ROOT/memory/macrosystem/current_phase.json"
CHRONOSYSTEM_FILE="$ROOT/memory/chronosystem/family_arc.json"
...

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

require_file "$BOOTSTRAP_FILE" "bootstrap file"
require_file "$AGENTS_FILE" "agents file"
require_file "$CONTINUITY_FILE" "continuity manifest"
require_file "$PILLAR_FILE" "pillar file"
require_file "$ECOLOGICAL_MODEL_FILE" "ecological model file"
require_file "$ECOLOGICAL_MANIFEST_FILE" "ecological manifest file"
require_file "$MACROSYSTEM_FILE" "macrosystem file"
require_file "$CHRONOSYSTEM_FILE" "chronosystem file"
```

Later, the pillar file's full text is read into the prompt verbatim, wrapped in explicit delimiters, ahead of the user's own message:

```bash
pillar_prompt="$(<"$PILLAR_FILE")"
...
printf -v final_prompt '%s\n\n...\n--- BEGIN PILLAR ---\n%s\n--- END PILLAR ---\n...' \
  "$bootstrap_prompt" "$pillar_prompt" ...
```

**What this proves and what it does not:** the gate is a real, unconditional precondition on the *process* — ABRAXAS will not boot at all without the constitution file present on disk. It says nothing about whether the model, once booted, actually obeys the principles it was handed — that part is a prompt convention the model can in principle ignore, not a code-enforced constraint. See the README's honesty section.
