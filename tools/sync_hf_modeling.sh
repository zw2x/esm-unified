#!/usr/bin/env bash
# Re-vendor ESM-C / ESMFold2 modeling code from the patched transformers fork.
#
# The vendored tree is a verbatim copy — no import rewriting — because
# esm/transformers/ mirrors the transformers package root. See
# esm/transformers/VENDORED.md.
#
# Usage:
#   tools/sync_hf_modeling.sh              # re-fetch the currently pinned commit
#   tools/sync_hf_modeling.sh <commit-sha> # bump the pin to a new commit
#
# After running, review with:  git diff esm/transformers/models

set -euo pipefail

REPO="https://github.com/Biohub/transformers.git"
PINNED="ef32577f55da19a4989cd7b22e004dc43a4998cb"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/esm/transformers/models"
SHA="${1:-$PINNED}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Fetching $SHA from $REPO ..."
git init -q "$TMP"
git -C "$TMP" remote add origin "$REPO"
git -C "$TMP" sparse-checkout init --cone
git -C "$TMP" sparse-checkout set src/transformers/models/esmc src/transformers/models/esmfold2
git -C "$TMP" fetch -q --depth 1 origin "$SHA"
git -C "$TMP" checkout -q FETCH_HEAD

SRC="$TMP/src/transformers/models"
for m in esmc esmfold2; do
    if [ ! -d "$SRC/$m" ]; then
        echo "error: $m missing from upstream at $SHA" >&2
        exit 1
    fi
done

echo "Replacing $DEST/{esmc,esmfold2} ..."
rm -rf "$DEST/esmc" "$DEST/esmfold2"
cp -r "$SRC/esmc" "$SRC/esmfold2" "$DEST/"

# The vendored tree must not carry compiled artefacts.
find "$DEST" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true

if [ "$SHA" != "$PINNED" ]; then
    echo
    echo "Pin changed. Update PINNED in $0 and the commit in esm/transformers/VENDORED.md:"
    echo "  $PINNED"
    echo "  -> $SHA"
fi

echo
echo "Done. Files: $(find "$DEST" -name '*.py' | wc -l)"
echo "Review with: git diff esm/transformers/models"
