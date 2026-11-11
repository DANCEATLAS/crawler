-- Private AI handoff mirror. Does not change application tables or API schemas.
-- Verified absent before first application, 2026-11-11.
begin;
create schema if not exists dance_atlas_internal;
revoke all on schema dance_atlas_internal from public, anon, authenticated;
create table if not exists dance_atlas_internal.ai_context (
  context_key text primary key,
  vision_revision text not null,
  canonical_url text not null,
  content_sha256 text not null,
  body text not null,
  updated_at timestamptz not null default now()
);
alter table dance_atlas_internal.ai_context enable row level security;
revoke all on table dance_atlas_internal.ai_context from public, anon, authenticated;
comment on table dance_atlas_internal.ai_context is
  'Private AI continuation ledger. GitHub DANCEATLAS/crawler is authoritative; read canonical links. No learner records or secrets.';
commit;
