#!/usr/bin/env bash
# Claude Code hook: format + lint Python with the project's own Ruff.
#
#   PostToolUse (Write|Edit)  -> formats the edited file, then exits 2 with any
#                               remaining violations on stderr.
#   Stop (--all-check)        -> repo-wide check; exits 2 to keep the turn going
#                               until Ruff is clean.
#
# Exit 2 is deliberate: on PostToolUse and Stop it is the only exit code whose
# stderr Claude actually reads. Exit 1 is reported as a non-blocking hook error
# and the model never sees the lint output.
#
# See https://code.claude.com/docs/en/hooks-guide

set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-.}"
cd "$ROOT" || exit 0

if ! command -v uv >/dev/null 2>&1; then
  # No toolchain: stay silent rather than breaking the session.
  exit 0
fi

json_field() {
  # json_field <stdin-json> <python-expr-key>
  local json="$1" key="$2"
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$json" | jq -r "$key // empty" 2>/dev/null
  else
    printf '%s' "$json" | python3 -c "
import json,sys
try: d = json.load(sys.stdin)
except Exception: sys.exit(0)
keys = '$key'.lstrip('.').split('.')
cur = d
for k in keys:
    if not isinstance(cur, dict): cur = None; break
    cur = cur.get(k)
if cur is True: print('true')
elif cur is False: print('false')
elif cur is None: print('')
else: print(cur)
" 2>/dev/null
  fi
}

stdin_json="$(cat 2>/dev/null || true)"

# ---------------------------------------------------------------- Stop event
if [[ "${1:-}" == "--all-check" ]]; then
  # Claude caps consecutive Stop blocks, but bail out early so a violation the
  # model cannot fix does not burn the whole budget.
  if [[ "$(json_field "$stdin_json" '.stop_hook_active')" == "true" ]]; then
    exit 0
  fi

  if out="$(uv run ruff check . 2>&1)" && fmt="$(uv run ruff format --check . 2>&1)"; then
    exit 0
  fi
  {
    echo "Ruff is not clean. Fix these before finishing:"
    printf '%s\n' "${out:-}" "${fmt:-}"
    echo "Run: uv run ruff check --fix . && uv run ruff format ."
  } >&2
  exit 2
fi

# ---------------------------------------------------------- PostToolUse event
path="$(json_field "$stdin_json" '.tool_input.file_path')"
if [[ -z "$path" ]]; then
  path="$(json_field "$stdin_json" '.tool_input.path')"
fi

case "${path:-}" in
  *.py|*.pyi) ;;
  *) exit 0 ;;
esac
[[ -f "$path" ]] || exit 0

uv run ruff format "$path" >/dev/null 2>&1

if remaining="$(uv run ruff check --fix "$path" 2>&1)"; then
  exit 0
fi

{
  echo "Ruff still reports issues in $path after auto-fix:"
  printf '%s\n' "$remaining"
} >&2
exit 2
