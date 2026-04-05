#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/ErikinBC/SurvSet.git"
REF="${1:-main}"

if [[ "${REF}" == "-h" || "${REF}" == "--help" ]]; then
  cat <<'EOF'
Usage:
  scripts/smoke_install_ref.sh [git-ref]

Examples:
  scripts/smoke_install_ref.sh
  scripts/smoke_install_ref.sh main
  scripts/smoke_install_ref.sh bb65b13
  scripts/smoke_install_ref.sh fix/issue-5-module-not-found
EOF
  exit 0
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required but not found in PATH." >&2
  exit 1
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "[1/4] Creating fresh virtual environment..."
python3 -m venv "${TMP_DIR}/venv"

echo "[2/4] Installing SurvSet from ref '${REF}'..."
"${TMP_DIR}/venv/bin/pip" install --no-cache-dir "SurvSet @ git+${REPO_URL}@${REF}" >/tmp/survset_smoke_install.log

echo "[3/4] Verifying installed loader fallback source..."
"${TMP_DIR}/venv/bin/python" - <<'PY'
import inspect
import SurvSet.data as data
print(inspect.getsource(data.SurvLoader._resource_root))
PY

echo "[4/4] Running package entrypoint..."
"${TMP_DIR}/venv/bin/python" -m SurvSet

echo "PASS: Smoke install test succeeded for ref '${REF}'."
