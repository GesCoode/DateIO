#!/usr/bin/env bash
# Idempotent repository bootstrap for the Cloud Agent environment.
# Installs Node dependencies for the SvelteKit app. System packages
# (PostgreSQL) are provided by the base snapshot; runtime service
# initialization lives in start.sh.
set -euo pipefail

cd "$(dirname "$0")/.."

npm ci
