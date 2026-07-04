#!/usr/bin/env bash
set -euo pipefail

# Make sure we are running from the directory of setup.sh
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$DIR"

echo "==> Running isfa-ai setup..."

if [ ! -f .env ]; then
  if [ -f env.example ]; then
    cp env.example .env
    echo "[!] Created .env from env.example."
    echo "[!] Please edit the `.env` file at the root of the project to add your API keys and Telegram tokens."
    echo "[!] Then run this script again."
    exit 0
  else
    echo "[ERROR] env.example not found. Please restore it."
    exit 1
  fi
fi

python3 setup.py
