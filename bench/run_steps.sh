#!/bin/sh
# usage: [SRC=<dejabug checkout>] bench/run_steps.sh <videos dir> <out dir> [extra dejabug args]; 3 at a time
# SRC pins the code under test so edits made during a run don't leak into it
here=$(cd "$(dirname "$0")/.." && pwd)

export PY="${SRC:-$here}/.venv/bin/python"
videos=$1; out=$2; shift 2
export EXTRA="$*" VIDEOS="$videos" OUT="$out"
mkdir -p "$out"
ls "$videos" | xargs -P "${JOBS:-3}" -I{} sh -c 'f="{}"; id="${f%.*}"; "$PY" -P -m dejabug.cli steps "$VIDEOS/$f" -o "$OUT/$id" $EXTRA > "$OUT/$id.log" 2>&1; echo "$id done"'
