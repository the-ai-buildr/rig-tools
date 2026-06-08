---
name: dmc-component-guide
description: 'Design and implement Dash Mantine Components (DMC) UI in this rig-tools repo. Use when building or refactoring page layouts, forms, navigation, cards, tables, and interactive controls with repo-consistent theming and callback wiring.'
argument-hint: 'What DMC UI are you building and on which page/file?'
user-invocable: true
disable-model-invocation: false
---

# DMC Component Guide

Build or refactor UI using `dash_mantine_components` (`dmc`) while staying aligned with this repository's architecture and theme conventions.

## When To Use
- Creating a new page under `pages/`
- Replacing `dash.html` usage with DMC equivalents
- Adding cards, KPI blocks, forms, tables, drawers, or navigation controls
- Applying consistent spacing, typography, and color from `styles/flowtides_theme.py`
- Wiring component IDs to callbacks in `callbacks/`

## Required Constraints
- Prefer DMC components for layout/UI whenever an equivalent exists.
- Allow minimal `dash.html` wrappers only when DMC has no practical equivalent or when a small semantic/container wrapper clearly reduces complexity.
- Use `dash_iconify.DashIconify` with `tabler:*` icons.
- Use `color="blue"` unless a semantic status color is required (`green`, `yellow`, `red`).
- Prefer theme defaults from `styles/flowtides_theme.py` over repeated inline props.

## Inputs To Collect First
1. Target file(s) to create or edit.
2. User intent: new page, component enhancement, or migration from non-DMC UI.
3. Interaction needs: static display vs callback-driven state.
4. Data source: local constants, repository layer, or API route.
5. Responsive expectation: mobile-only, desktop-first, or fully responsive.

## Workflow
1. Inspect existing structure.
   - Confirm route/page location in `pages/`.
   - Check if nav entry is needed in `components/ui/nav_links.py`.
   - Identify required callbacks and registration in `callbacks/register.py`.
2. Choose layout primitives.
   - Use `dmc.Stack` for vertical sections.
   - Use `dmc.Group` for horizontal controls/actions.
   - Use `dmc.Grid` and `dmc.GridCol` with repo span helpers for responsiveness.
3. Select component pattern.
   - Metrics: card + label/value + badge trend pattern.
   - Forms: DMC inputs and buttons with clear IDs and labels.
   - Data display: `dmc.Table` with mono-style values when numeric-heavy.
   - Overlays: `dmc.Drawer`/`dmc.Modal` for secondary workflows.
4. Apply theme and visual consistency.
   - Keep `color="blue"` for primary actions and active states.
   - Reuse style helpers (for KPI value, labels, featured cards) where applicable.
   - Keep spacing consistent with existing page rhythm.
5. Wire interactions.
   - Add deterministic IDs for any interactive component.
   - Implement callbacks in the relevant `callbacks/*.py` module.
   - Register callback module via `callbacks/register.py` if new.
6. Validate and polish.
   - Check mobile and desktop structure.
   - Verify no unnecessary `dash.html` wrappers remain.
   - Confirm callbacks are connected and no duplicate IDs exist.

## Decision Branches
- If building a new route:
  - Register with `dash.register_page(...)` and export `layout`.
  - Add navigation item under `components/ui/nav_links.py`.
- If editing an existing page:
  - Preserve IDs relied on by existing callbacks, or refactor callbacks in lockstep.
- If the UI is mostly static:
  - Favor simple composition and avoid adding callback complexity.
- If the UI is stateful:
  - Keep callback boundaries feature-focused (one module per feature when possible).
- If style drift appears:
  - Update defaults in `styles/flowtides_theme.py` instead of repeating per-instance overrides.
- If a non-DMC element is proposed:
   - Keep it minimal, document why it is needed, and confirm no DMC equivalent is suitable.

## Completion Criteria
- Page renders using DMC components for layout and controls.
- Primary actions and active states follow repo color/theme conventions.
- Required route/nav/callback wiring is complete.
- IDs are stable and unique.
- Implementation is responsive and readable on small screens.
- No regressions introduced in surrounding layout behavior.

## Quick Self-Review Checklist
- Did I use DMC equivalents instead of `dash.html` where possible?
- Are icon choices from `tabler:*` and visually consistent?
- Are spacing and typography aligned with existing pages?
- Is callback registration updated when introducing new callback modules?
- Is there any repeated style that should move to `styles/flowtides_theme.py`?
