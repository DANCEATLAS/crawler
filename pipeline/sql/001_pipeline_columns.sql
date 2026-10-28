-- Dancing Atlas pipeline v3 — run once in the Supabase SQL editor (idempotent).
-- Adds the columns the pipeline writes and two small operational tables.

alter table public.dances
  add column if not exists profile_long        text,
  add column if not exists research            jsonb,
  add column if not exists research_gate       text,
  add column if not exists qc                  jsonb,
  add column if not exists qc_score            numeric,
  add column if not exists albums              jsonb,
  add column if not exists album_candidates    jsonb,
  add column if not exists images              jsonb,
  add column if not exists sacred_note         text,
  add column if not exists hero_qc             jsonb,
  add column if not exists last_researched_at  timestamptz,
  add column if not exists pipeline_version    text;

create index if not exists dances_research_gate_idx on public.dances (research_gate);
create index if not exists dances_publish_gate_idx  on public.dances (publish_gate);

create table if not exists public.pipeline_runs (
  id           bigserial primary key,
  run_date     date,
  stage        text,
  started_at   timestamptz,
  finished_at  timestamptz,
  counters     jsonb,
  errors       jsonb,
  version      text,
  created_at   timestamptz default now()
);

create table if not exists public.qc_queue (
  slug         text primary key,
  gate         text,
  score        numeric,
  reasons      text,
  duplicate_of text,
  updated_at   timestamptz
);

alter table public.pipeline_runs enable row level security;
alter table public.qc_queue      enable row level security;
-- service role bypasses RLS; readers of the app do not need these tables.

-- Child tables must have unique keys for the upserts (no-op if already present).
do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'dance_aliases_dance_id_alias_key') then
    alter table public.dance_aliases add constraint dance_aliases_dance_id_alias_key unique (dance_id, alias);
  end if;
exception when others then raise notice 'dance_aliases unique: %', sqlerrm; end $$;
do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'dance_sources_dance_id_url_key') then
    alter table public.dance_sources add constraint dance_sources_dance_id_url_key unique (dance_id, url);
  end if;
exception when others then raise notice 'dance_sources unique: %', sqlerrm; end $$;
do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'dance_edges_src_dst_rel_key') then
    alter table public.dance_edges add constraint dance_edges_src_dst_rel_key unique (src_id, dst_id, relation);
  end if;
exception when others then raise notice 'dance_edges unique: %', sqlerrm; end $$;

-- Public, app-facing view: only what the website should show.
create or replace view public.dances_public as
  select slug, name, country, country_code, region, era, tagline, insight, profile,
         case when research_gate = 'publish' then profile_long else null end as profile_long,
         case when research_gate = 'publish' then research else null end as research,
         albums, images, hero_video_youtube_id, video_stack, tutorials, wikipedia_url, wikidata_qid,
         unesco, ich_ref, is_sacred, sacred_note, lat, lng, form_id, tier, publish_gate, qc_score, hero_qc, updated_at
  from public.dances
  where coalesce(publish_gate, 'publish') <> 'reject';
grant select on public.dances_public to anon, authenticated;
