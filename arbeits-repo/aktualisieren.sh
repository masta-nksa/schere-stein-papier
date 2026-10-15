#!/usr/bin/env bash
# Überträgt die Arbeitsordner aus dem Material-Repo ins Arbeits-Repo der SuS.
# Aufruf: bash arbeits-repo/aktualisieren.sh <Material-Ordner> <Arbeits-Repo-Ordner>
# Wird von .github/workflows/arbeits-repo.yml bei jedem Push aufgerufen. Löscht im Ziel nur die
# Ordner, die es selbst wieder füllt (und nie den Ordner .git).
set -euo pipefail

QUELLE="$1"
ZIEL="$2"
ORDNER="ki microbit beispiele vorlagen"

for d in $ORDNER; do
  rm -rf "$ZIEL/$d"
  cp -r "$QUELLE/$d" "$ZIEL/$d"
done

# Nur für die Lehrperson: Tests nicht ins Arbeits-Repo
rm -rf "$ZIEL/ki/test"
find "$ZIEL" -name "__pycache__" -type d -prune -exec rm -rf {} +

cp "$QUELLE/arbeits-repo/README.md" "$ZIEL/README.md"
cp "$QUELLE/arbeits-repo/gitignore" "$ZIEL/.gitignore"
mkdir -p "$ZIEL/.vscode"
cp "$QUELLE/arbeits-repo/vscode-extensions.json" "$ZIEL/.vscode/extensions.json"

echo "Arbeits-Repo aktualisiert: $ORDNER, README.md, .gitignore, .vscode/extensions.json"
