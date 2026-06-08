-- Security hardening (addresses db advisors 0028/0029):
--   * revoke EXECUTE on the SECURITY DEFINER event-trigger function
--     public.rls_auto_enable() so it cannot be invoked via the Data API
--     (anon/authenticated rpc). Event-trigger functions are fired by DDL
--     and should never be callable directly.

revoke execute on function public.rls_auto_enable() from public, anon, authenticated;
