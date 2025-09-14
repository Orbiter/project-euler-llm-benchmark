#!/usr/bin/env bash
set -euo pipefail
if [ $# -ne 2 ]; then
  echo "Usage: $0 <PORT> <MODEL>"
  exit 1
fi

VENV_DIR="$HOME/.venv/mlx"
if [ ! -d "$VENV_DIR" ]; then
  python3.12 -m venv "$VENV_DIR"
  source "$VENV_DIR/bin/activate"
  python3.12 -m pip install --upgrade pip
  pip install mlx-lm
else
  source "$VENV_DIR/bin/activate"
fi

PORT="$1"
MODEL="$2"
exec mlx_lm.server --host 0.0.0.0 --port "$PORT" --model "$MODEL" --use-default-chat-template
