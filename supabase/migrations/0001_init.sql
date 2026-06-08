-- Initial schema for rig-tools on Supabase.
--
-- Tables: profiles (mirrors auth.users), app_settings, projects, wells.
-- Auth identities live in auth.users (managed by GoTrue); profiles holds the
-- app-specific role/flags/preferences. RLS is enabled on every table as
-- defense-in-depth. Server code uses the service-role key (bypasses RLS); the
-- authenticated policies below scope per-user access for any future JWT client.

-- ── helpers ──────────────────────────────────────────────────────────────────
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- ── profiles ─────────────────────────────────────────────────────────────────
create table public.profiles (
    id          uuid primary key references auth.users (id) on delete cascade,
    username    text unique,
    full_name   text not null default '',
    role        text not null default 'viewer',
    is_active   boolean not null default true,
    preferences jsonb not null default '{}'::jsonb,
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now()
);

create trigger profiles_set_updated_at
    before update on public.profiles
    for each row execute function public.set_updated_at();

-- Seed a profile row whenever a new auth user is created. Role/username/full_name
-- are taken from the metadata supplied by the (trusted, service-role) admin call
-- that creates the user, defaulting to a viewer when absent.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id, username, full_name, role)
  values (
    new.id,
    new.raw_user_meta_data ->> 'username',
    coalesce(new.raw_user_meta_data ->> 'full_name', ''),
    coalesce(new.raw_user_meta_data ->> 'role', 'viewer')
  );
  return new;
end;
$$;

create trigger on_auth_user_created
    after insert on auth.users
    for each row execute function public.handle_new_user();

-- ── app_settings ─────────────────────────────────────────────────────────────
create table public.app_settings (
    id                   text primary key default 'global',
    app_name             text not null default 'Rig Tools',
    default_color_scheme text not null default 'light',
    default_accent       text not null default 'blue',
    default_units        text not null default 'imperial',
    updated_at           timestamptz not null default now()
);

create trigger app_settings_set_updated_at
    before update on public.app_settings
    for each row execute function public.set_updated_at();

insert into public.app_settings (id) values ('global') on conflict (id) do nothing;

-- ── projects ─────────────────────────────────────────────────────────────────
create table public.projects (
    id           uuid primary key default gen_random_uuid(),
    name         text not null,
    project_type text not null default 'single',
    description  text,
    status       text not null default 'planned',
    owner_id     uuid references auth.users (id) on delete set null,
    created_at   timestamptz not null default now(),
    updated_at   timestamptz not null default now()
);

create index projects_owner_id_idx on public.projects (owner_id);

create trigger projects_set_updated_at
    before update on public.projects
    for each row execute function public.set_updated_at();

-- ── wells ────────────────────────────────────────────────────────────────────
create table public.wells (
    id          uuid primary key default gen_random_uuid(),
    project_id  uuid references public.projects (id) on delete cascade,
    well_name   text not null,
    api_number  text,
    status      text not null default 'Planning',
    well_type   text not null default 'Horizontal',
    document    jsonb not null,
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now()
);

create index wells_project_id_idx on public.wells (project_id);
create index wells_api_number_idx on public.wells (api_number);

create trigger wells_set_updated_at
    before update on public.wells
    for each row execute function public.set_updated_at();

-- ── row level security ───────────────────────────────────────────────────────
-- Enabled everywhere. Server-side service-role operations bypass these; the
-- policies scope access for authenticated JWT clients (admin-wide operations are
-- performed via the service-role client, which is not subject to RLS).
alter table public.profiles     enable row level security;
alter table public.app_settings enable row level security;
alter table public.projects     enable row level security;
alter table public.wells        enable row level security;

-- profiles: a user may read and update only their own profile.
create policy "profiles_select_own" on public.profiles
    for select to authenticated
    using ((select auth.uid()) = id);

create policy "profiles_update_own" on public.profiles
    for update to authenticated
    using ((select auth.uid()) = id)
    with check ((select auth.uid()) = id);

-- app_settings: readable by any authenticated user; writes are service-role only.
create policy "app_settings_select_all" on public.app_settings
    for select to authenticated
    using (true);

-- projects: owners have full access to their own projects.
create policy "projects_select_own" on public.projects
    for select to authenticated
    using ((select auth.uid()) = owner_id);

create policy "projects_insert_own" on public.projects
    for insert to authenticated
    with check ((select auth.uid()) = owner_id);

create policy "projects_update_own" on public.projects
    for update to authenticated
    using ((select auth.uid()) = owner_id)
    with check ((select auth.uid()) = owner_id);

create policy "projects_delete_own" on public.projects
    for delete to authenticated
    using ((select auth.uid()) = owner_id);

-- wells: access is gated through ownership of the parent project.
create policy "wells_select_via_project" on public.wells
    for select to authenticated
    using (exists (
        select 1 from public.projects p
        where p.id = wells.project_id and p.owner_id = (select auth.uid())
    ));

create policy "wells_insert_via_project" on public.wells
    for insert to authenticated
    with check (exists (
        select 1 from public.projects p
        where p.id = wells.project_id and p.owner_id = (select auth.uid())
    ));

create policy "wells_update_via_project" on public.wells
    for update to authenticated
    using (exists (
        select 1 from public.projects p
        where p.id = wells.project_id and p.owner_id = (select auth.uid())
    ))
    with check (exists (
        select 1 from public.projects p
        where p.id = wells.project_id and p.owner_id = (select auth.uid())
    ));

create policy "wells_delete_via_project" on public.wells
    for delete to authenticated
    using (exists (
        select 1 from public.projects p
        where p.id = wells.project_id and p.owner_id = (select auth.uid())
    ));
