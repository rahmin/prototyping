#!/usr/bin/env bash
#
# Sync browser edits of the invitation page back into this repo.
#
#   1. Open bloom-civic-host-invitation-editable.html in a browser
#   2. Double-click any text to edit it
#   3. Click "Save editable copy"  (NOT "Download clean copy")
#   4. Run this script
#
# It picks up the newest matching file from ~/Downloads, regenerates the clean
# (editor-stripped) copy from it so the two never drift, shows you the diff,
# then commits and pushes.
#
# Usage:
#   ./sync-edits.sh                      review the diff, then confirm
#   ./sync-edits.sh -y                   skip the confirmation prompt
#   ./sync-edits.sh "Tighten hero copy"  use your own commit subject

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOWNLOADS="${HOME}/Downloads"
EDITABLE="bloom-civic-host-invitation-editable.html"
CLEAN="bloom-civic-host-invitation.html"
PAGES_URL="https://rahmin.github.io/prototyping"

AUTO_YES=0
MSG=""
while (( $# )); do
  case "$1" in
    -y|--yes)   AUTO_YES=1 ;;
    -h|--help)  sed -n '3,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)          MSG="$1" ;;
  esac
  shift
done

cd "$REPO"

# --- find the newest downloaded editable copy --------------------------------
# Browsers rename repeat downloads variously: " (1)", "-1", "_2", etc.
shopt -s nullglob
candidates=("$DOWNLOADS"/bloom-civic-host-invitation-editable*.html)
shopt -u nullglob

if (( ${#candidates[@]} == 0 )); then
  echo "No downloaded editable copy found in $DOWNLOADS"
  echo
  echo "Open $EDITABLE in a browser, make your edits, then click"
  echo "\"Save editable copy\" and run this again."
  exit 1
fi

newest=""
newest_mtime=0
for f in "${candidates[@]}"; do
  m="$(stat -f %m "$f")"
  if (( m > newest_mtime )); then
    newest_mtime="$m"
    newest="$f"
  fi
done

echo "Source:  $(basename "$newest")"
echo "Saved:   $(date -r "$newest_mtime" '+%Y-%m-%d %H:%M')"
echo

# --- sanity-check it before overwriting anything -----------------------------
if ! grep -q "BLOOM Civic Host Cohort" "$newest"; then
  echo "Refusing to sync: that file doesn't look like the BLOOM invitation page." >&2
  exit 1
fi

if ! grep -q 'id="editor-script"' "$newest"; then
  echo "That file has no editor block, so it's a \"Download clean copy\" export." >&2
  echo "Use \"Save editable copy\" instead — this script derives the clean copy" >&2
  echo "from the editable one, so it needs the editable version as input." >&2
  exit 1
fi

# --- update the editable copy, then regenerate the clean copy from it --------
cp "$newest" "$EDITABLE"
python3 make-clean.py "$EDITABLE" "$CLEAN"

# --- show what changed, confirm, commit -------------------------------------
if git diff --quiet -- "$EDITABLE" "$CLEAN"; then
  echo "No changes — the repo already matches that download."
  exit 0
fi

git --no-pager diff --stat -- "$EDITABLE" "$CLEAN"
echo
echo "Copy changes (clean file, word-level):"
git --no-pager diff --word-diff -- "$CLEAN" | sed -n '/^@@/,$p' | head -60
echo

if (( ! AUTO_YES )); then
  read -r -p "Commit and push? [y/N] " reply
  if [[ ! "$reply" =~ ^[Yy]$ ]]; then
    echo
    echo "Not committed. Your edits are still in the working tree —"
    echo "run 'git checkout -- $EDITABLE $CLEAN' to discard them."
    exit 0
  fi
fi

git add "$EDITABLE" "$CLEAN"
git commit -q -F - <<EOF
${MSG:-Sync browser edits to the invitation page}

Applied from $(basename "$newest") via sync-edits.sh.
EOF
git push -q

echo
echo "Pushed. Live in about a minute:"
echo "  $PAGES_URL/$CLEAN"
