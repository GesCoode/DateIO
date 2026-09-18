#!/usr/bin/env bash
# Per-boot runtime initialization for the Cloud Agent environment.
# Starts PostgreSQL, ensures the visagely role/database/schema exist,
# and writes a local .env so the SvelteKit dev server can connect.
# Safe to run repeatedly: every step is guarded / idempotent.
set -euo pipefail

cd "$(dirname "$0")/.."

PG_USER="visagely"
PG_PASSWORD="visagely"
PG_DB="visagely"
DATABASE_URL="postgres://${PG_USER}:${PG_PASSWORD}@localhost:5432/${PG_DB}"

echo "[start] Ensuring PostgreSQL cluster is running..."
if ! sudo pg_isready -q 2>/dev/null; then
  sudo pg_ctlcluster 16 main start || true
  # Wait for the server to accept connections.
  for _ in $(seq 1 30); do
    if sudo pg_isready -q 2>/dev/null; then break; fi
    sleep 1
  done
fi
sudo pg_isready

echo "[start] Ensuring role '${PG_USER}' exists..."
sudo -u postgres psql -v ON_ERROR_STOP=1 <<SQL
DO \$\$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '${PG_USER}') THEN
    CREATE ROLE ${PG_USER} LOGIN PASSWORD '${PG_PASSWORD}';
  END IF;
END \$\$;
SQL

echo "[start] Ensuring database '${PG_DB}' exists..."
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${PG_DB}'" | grep -q 1; then
  sudo -u postgres createdb -O "${PG_USER}" "${PG_DB}"
fi

echo "[start] Ensuring schema is applied..."
TABLE_EXISTS=$(sudo -u postgres psql -d "${PG_DB}" -tAc "SELECT to_regclass('public.waitlist_signups') IS NOT NULL")
if [ "${TABLE_EXISTS}" != "t" ]; then
  sudo -u postgres psql -d "${PG_DB}" -v ON_ERROR_STOP=1 -f db/schema.sql
fi

echo "[start] Ensuring privileges for '${PG_USER}'..."
sudo -u postgres psql -d "${PG_DB}" -v ON_ERROR_STOP=1 <<SQL
GRANT ALL ON SCHEMA public TO ${PG_USER};
GRANT ALL ON ALL TABLES IN SCHEMA public TO ${PG_USER};
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO ${PG_USER};
SQL

if [ ! -f .env ]; then
  echo "[start] Writing local development .env..."
  cat > .env <<ENV
ORIGIN=http://localhost:5173
POSTGRES_PASSWORD=${PG_PASSWORD}
DATABASE_URL=${DATABASE_URL}
ENV
fi

echo "[start] Environment ready."
