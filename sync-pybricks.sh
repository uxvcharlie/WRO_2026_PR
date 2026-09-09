#!/usr/bin/env bash
# Trae el codigo exportado desde Pybricks Code al repo.
#
# Uso:
#   ./sync-pybricks.sh              -> usa el .zip mas reciente de ~/Downloads
#   ./sync-pybricks.sh archivo.zip  -> usa el zip que le indiques
#
# No commitea solo: te muestra el diff y vos decidis.

set -euo pipefail
cd "$(dirname "$0")"

ZIP="${1:-}"
if [ -z "$ZIP" ]; then
    ZIP=$(ls -t ~/Downloads/*.zip 2>/dev/null | head -1)
    [ -n "$ZIP" ] || { echo "No encontre ningun .zip en ~/Downloads"; exit 1; }
fi
[ -f "$ZIP" ] || { echo "No existe: $ZIP"; exit 1; }

echo "Usando: $ZIP"
echo "        ($(date -r "$ZIP" '+%Y-%m-%d %H:%M'))"
echo

if [ -n "$(git status --porcelain)" ]; then
    echo "OJO: tenes cambios sin commitear. Commitealos o guardalos antes."
    git status --short
    exit 1
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
unzip -q "$ZIP" -d "$TMP"

# Los .py pueden venir en la raiz del zip o en una subcarpeta.
SRC=$(dirname "$(find "$TMP" -name '*.py' -print -quit)")
[ -n "$SRC" ] || { echo "El zip no trae archivos .py"; exit 1; }

n=0
for f in "$SRC"/*.py; do
    name=$(basename "$f")
    if [ ! -f "$name" ]; then
        echo "  + $name (nuevo)"
        cp "$f" "$name"; n=$((n+1))
    elif ! diff -q "$f" "$name" >/dev/null; then
        echo "  ~ $name"
        cp "$f" "$name"; n=$((n+1))
    fi
done

echo
if [ "$n" -eq 0 ]; then
    echo "Todo igual, no habia nada nuevo."
    exit 0
fi

git diff --stat
echo
echo "Listo. Si te convence:"
echo "  git add -A && git commit -m 'Sincronizar cambios hechos en Pybricks Code' && git push"
