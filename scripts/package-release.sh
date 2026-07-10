#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VERSION="$(python3 -c "import json; print(json.load(open('manifest.json'))['version'])")"
NAME="soundscript-wordbank-v${VERSION}"
STAGING="/tmp/${NAME}"
ARCHIVE="/tmp/${NAME}.zip"

rm -rf "$STAGING" "$ARCHIVE"
mkdir -p "$STAGING"

cp manifest.json LICENSE LICENSE-POLICY.md README.md CHANGELOG.md CONTRIBUTING.md "$STAGING/"
cp -r schema data corpus fixtures docs "$STAGING/"

(
  cd /tmp
  zip -rq "$ARCHIVE" "$NAME"
)

echo "Created $ARCHIVE"
echo "Attach to GitHub Release tag v${VERSION}"
