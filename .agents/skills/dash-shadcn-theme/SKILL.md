---
name: dash-shadcn-theme
description: 'Apply shadcn/ui styling to a Dash Plotly + Dash Mantine Components project by translating shadcn tokens into Mantine theme values and CSS variables. Use for full visual reskins, token audits, light/dark consistency fixes, and Plotly/DMC style alignment.'
argument-hint: 'Target scope (full app or specific pages/components) and whether to keep blue primary or use monochrome'
user-invocable: true
disable-model-invocation: false
---

# Dash Shadcn Theme Migration

## What This Skill Produces
This skill converts an existing Dash app that uses Dash Mantine Components (DMC) into a shadcn-style visual system without adding React, Tailwind, or shadcn component packages.

Outputs:
- Updated `styles/flowtides_theme.py` token and component defaults aligned to shadcn semantics
- Updated `assets/styles.css` with shadcn semantic CSS variables and Mantine variable remaps
- Optional targeted updates in UI components where local styles fight the theme
- Verification checklist covering light/dark mode and Plotly figure consistency

## When to Use
Use this skill when any of these appear:
- "make Dash UI look like shadcn"
- "translate shadcn tokens into Mantine"
- "remove glow/tactical theme and use neutral modern styling"
- "align Plotly charts with app theme"
- "normalize card/input/nav/button styles across pages"

Do not use this skill for:
- Database/auth/backend changes
- New page feature implementation unrelated to theming
- Tailwind or React migration

## Procedure
1. Confirm scope and constraints.
2. Build token mapping from shadcn semantics to Mantine + CSS vars.
3. Update theme source of truth.
4. Update CSS variable remaps and interaction styles.
5. Touch up components that override theme defaults.
6. Align Plotly templates.
7. Validate all key UI surfaces and interaction states.

## Step-by-Step Workflow

### 1. Confirm Scope and Constraints
- Confirm this is a visual migration only (no route/model/data changes).
- Confirm target is all Dash/DMC surfaces in app shell and pages.
- Confirm whether to keep brand primary as blue or switch to shadcn monochrome primary.
- Confirm whether monospace should remain only for numeric data cells or be removed globally.

Completion check:
- Migration boundaries are explicit and non-visual changes are excluded.

### 2. Build Token Mapping
Use shadcn semantic tokens as source of truth:
- `background`, `foreground`, `card`, `popover`
- `primary`, `primary-foreground`
- `secondary`, `accent`, `muted`, `muted-foreground`
- `border`, `input`, `ring`, `destructive`, `radius`

Map to Mantine variables:
- `--mantine-color-body` -> `hsl(var(--background))`
- `--mantine-color-text` -> `hsl(var(--foreground))`
- `--mantine-color-default` -> `hsl(var(--card))`
- `--mantine-color-default-border` -> `hsl(var(--border))`
- `--mantine-color-dimmed` -> `hsl(var(--muted-foreground))`
- primary filled + hover + focus ring -> shadcn `primary` and `ring`

Completion check:
- Every semantic token has an implementation target in theme or CSS.

### 3. Update `styles/flowtides_theme.py`
- Rebuild color arrays to match shadcn-like slate neutrals and blue primary scale.
- Set `primaryShade` for light/dark coherence.
- Set radius scale so default cornering trends toward shadcn's 8px feel.
- Replace heavy glow shadows with subtle Tailwind-like shadows.
- Normalize typography to sans-first defaults.
- Keep existing exported helper names stable to avoid breaking page imports.

Completion check:
- Theme object remains API-compatible for existing imports.
- App does not require component tree rewrites to receive new style language.

### 4. Update `assets/styles.css`
- Add `:root` and dark-scheme shadcn semantic token blocks.
- Remap Mantine CSS variables to semantic tokens.
- Replace glow-based hover states with subtle border/background shifts.
- Ensure keyboard focus-visible uses a clear `ring` outline.
- Preserve reduced-motion behavior if already present.

Completion check:
- Light and dark mode both use semantic token system.
- Hover/focus behavior is subtle and accessible.

### 5. Component Touch-Ups (Only Where Needed)
Audit and adjust components that hardcode old visual language:
- app shell header/sidebar/nav
- metric/stat cards
- settings/theme controls
- shared inline style helpers in theme file

Rules:
- Prefer removing local style overrides instead of adding more custom CSS.
- Keep behavior and callback wiring unchanged.

Completion check:
- No remaining electric/glow look where shadcn neutral style is expected.

### 6. Plotly Alignment
- Update light/dark Plotly templates so chart backgrounds, gridlines, text, and colorway align with the same semantic tokens.
- Ensure chart contrast remains readable in both schemes.

Completion check:
- Charts visually belong to the same design system as cards and controls.

### 7. Verification Checklist
Run app and verify:
- Header, navbar, nav active/hover states
- Buttons, inputs, selects, textareas, popovers/tooltips
- Cards/tables/badges across at least home, tools, settings pages
- Plotly figures in light and dark
- Focus ring visibility with keyboard navigation
- No regressions in layout spacing or callbacks

## Decision Points and Branching Logic
- Primary brand strategy:
  - If product identity requires brand continuity, keep blue primary.
  - If strict shadcn default look is required, use near-monochrome primary.

- Numeric typography:
  - If users scan dense numeric tables, keep mono only in data cells.
  - Otherwise use sans universally for full shadcn consistency.

- Radius softness:
  - If team wants original tactical sharpness, use smaller radius scale.
  - If team wants authentic shadcn softness, use 8px default corners.

## Quality Criteria
- Consistency: no mixed old/new visual language on primary surfaces.
- Accessibility: readable contrast and visible focus rings.
- Maintainability: token-driven theming in central files, minimal one-off overrides.
- Compatibility: existing Python imports, callback wiring, and page layouts remain intact.

## Ambiguity Review Prompts (Ask After Draft)
Use these prompts to finalize weak points:
1. Should primary remain blue or switch to shadcn monochrome?
2. Should monospace be retained for KPI/table numeric cells?
3. Should default radius be 8px everywhere or partially reduced for dense tables?
4. Should nav active state be muted/accent style or retain stronger brand emphasis?

## Example Prompts
- `/dash-shadcn-theme Apply shadcn styling to the full app, keep blue primary, keep mono only in numeric cells.`
- `/dash-shadcn-theme Reskin only dashboard shell and shared cards first, then charts.`
- `/dash-shadcn-theme Audit current theme and produce minimal diff plan before editing.`
