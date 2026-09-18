#!/usr/bin/env bash
# Idempotent repository bootstrap for the Cloud Agent environment.
# Ensures PostgreSQL is installed (the app's datastore) and installs the
# SvelteKit app's Node dependencies. Runtime service startup lives in
# start.sh. Safe to run repeatedly.
set -euo pipefail

cd "$(dirname "$0")/.."

# PostgreSQL is a stable system dependency. Install it once; on hosts where
# it is already present (e.g. a warm snapshot) this is a fast no-op.
if ! command -v pg_ctlcluster >/dev/null 2>&1; then
  echo "[install] Installing PostgreSQL..."
  export DEBIAN_FRONTEND=noninteractive
  sudo apt-get update -qq
  sudo apt-get install -y -qq postgresql postgresql-contrib
else
  echo "[install] PostgreSQL already installed."
fi

echo "[install] Installing Node dependencies..."
npm ci
