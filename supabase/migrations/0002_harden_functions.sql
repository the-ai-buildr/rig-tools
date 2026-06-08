-- Security hardening for the initial schema (addresses db advisors):
--   * pin search_path on set_updated_at (function_search_path_mutable)
--   * revoke EXECUTE on the SECURITY DEFINER trigger function so it cannot be
--     called directly via the Data API (anon/authenticated rpc).

create or replace function public.set_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

revoke execute on function public.handle_new_user() from public, anon, authenticated;
