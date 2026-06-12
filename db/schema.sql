CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE waitlist_signups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_waitlist_signups_created_at ON waitlist_signups(created_at);
