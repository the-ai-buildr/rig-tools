# Plan: Adopt shadcn/ui Visual Language in the Mantine (DMC) Theme

Branch: `feat/shadcn-theme`

Goal: re-skin the existing Dash Mantine Components UI to match the **shadcn/ui**
design system, using shadcn's **Tailwind CSS design tokens as the only reference**.
We are **not** introducing Tailwind, React, or the shadcn component library — we are
translating shadcn's token system into Mantine's theme object + CSS variables so the
existing DMC component tree renders with a shadcn look.

---

## 1. Evaluation of Current Styles

Source of truth today: [styles/flowtides_theme.py](../styles/flowtides_theme.py) +
[assets/styles.css](../assets/styles.css), wired in [app.py](../app.py) via
`MantineProvider(theme=dmc_theme)`.

### What exists

| Area | Current state (FlowTides) | shadcn target |
|------|---------------------------|---------------|
| **Aesthetic** | Dark-first, "tactical", electric-blue glow, high-density | Calm, neutral, flat, low-contrast borders, minimal shadow |
| **Primary color** | `blue` (`#2579FF`, custom electric scale) | `blue` (`hsl(221 83% 53%)`) — close, needs hue/shade retune |
| **Neutrals** | `dark` palette is pure near-black (`#141414` body, `#242424` card); separate `slate` scale | shadcn `slate` (cool gray) for both bg + borders |
| **Radius** | `defaultRadius="sm"` (4px), sharp/tactical | shadcn `--radius: 0.5rem` → default 8px (`rounded-md`) |
| **Typography** | `FONT_DISPLAY/BODY/MONO` all set to `'Sans Sherif','IBM Plex Mono'` (note: the AGENTS.md mentions Barlow/DM Sans/JetBrains but the theme actually collapses all three to one stack) | Single sans stack (Inter / Geist / system-ui), no condensed display, no mono-everywhere |
| **Shadows** | Heavy multi-layer + accent `glow` shadow | Subtle: `sm` ≈ `0 1px 2px rgba(0,0,0,.05)` |
| **Borders** | `1px` slate, sometimes glowing | `1px` `--border` (very low contrast) |
| **Component defaults** | Card `radius=md padding=lg`, Badge `radius=sm`, Input mono font, NavLink subtle blue | Buttons solid primary w/ `primary-foreground`, focus ring `--ring` 2px, muted secondary surfaces |
| **Dark/light switch** | `forceColorScheme` via `color-scheme-switch` in [callbacks/theme.py](../callbacks/theme.py) | Keep mechanism; just swap token values |
| **Plotly templates** | `PLOTLY_TEMPLATE_DARK/LIGHT` keyed off slate/blue | Retune to shadcn neutral bg + blue colorway |
| **Custom CSS** | NavLink hover/active, `.metric-card` hover glow | Replace glow with shadcn hover (muted bg / subtle border) |

### Files that consume styling (impact surface)

- [app.py](../app.py) — passes `dmc_theme`, sets AppShell padding/header/navbar.
- [components/layouts/dashboard.py](../components/layouts/dashboard.py) — header, sidebar, NavLink colors.
- [components/ui/metric_card.py](../components/ui/metric_card.py) — `.metric-card` class, ThemeIcon.
- [components/ui/theme_toggle.py](../components/ui/theme_toggle.py) — color-scheme switch.
- [components/ui/nav_links.py](../components/ui/nav_links.py), [components/ui/settings_popover.py](../components/ui/settings_popover.py).
- All `pages/**` — consume helpers (`style_kpi_value`, `SPAN_*`, `color="blue"`).
- [styles/flowtides_theme.py](../styles/flowtides_theme.py) — central token store + helpers.

Because nearly everything reads from `flowtides_theme.py` and `styles.css`, **most of
the re-skin happens in those two files** plus light edits to the CSS-consuming widgets.

---

## 2. shadcn Token Reference (Tailwind source of truth)

shadcn's `globals.css` exposes HSL design tokens. We adopt the **slate + blue** variant
(closest to the current brand and to a data dashboard).

### Light (`:root`)
```
--background:           0 0% 100%;      /* #FFFFFF */
--foreground:           222.2 84% 4.9%; /* near-black slate */
--card:                 0 0% 100%;
--card-foreground:      222.2 84% 4.9%;
--popover:              0 0% 100%;
--popover-foreground:   222.2 84% 4.9%;
--primary:              221.2 83.2% 53.3%;  /* blue-600-ish */
--primary-foreground:   210 40% 98%;
--secondary:            210 40% 96.1%;
--secondary-foreground: 222.2 47.4% 11.2%;
--muted:                210 40% 96.1%;
--muted-foreground:     215.4 16.3% 46.9%;
--accent:               210 40% 96.1%;
--accent-foreground:    222.2 47.4% 11.2%;
--destructive:          0 84.2% 60.2%;
--destructive-foreground:210 40% 98%;
--border:               214.3 31.8% 91.4%;
--input:                214.3 31.8% 91.4%;
--ring:                 221.2 83.2% 53.3%;
--radius:               0.5rem;
```

### Dark (`.dark`)
```
--background:           222.2 84% 4.9%;
--foreground:           210 40% 98%;
--card:                 222.2 84% 4.9%;
--card-foreground:      210 40% 98%;
--popover:              222.2 84% 4.9%;
--popover-foreground:   210 40% 98%;
--primary:              217.2 91.2% 59.8%;
--primary-foreground:   222.2 47.4% 11.2%;
--secondary:            217.2 32.6% 17.5%;
--secondary-foreground: 210 40% 98%;
--muted:                217.2 32.6% 17.5%;
--muted-foreground:     215 20.2% 65.1%;
--accent:               217.2 32.6% 17.5%;
--accent-foreground:    210 40% 98%;
--destructive:          0 62.8% 30.6%;
--destructive-foreground:210 40% 98%;
--border:               217.2 32.6% 17.5%;
--input:                217.2 32.6% 17.5%;
--ring:                 224.3 76.3% 48%;
```

### Tailwind radius scale derived from `--radius`
```
rounded-sm = calc(var(--radius) - 4px)  = 4px
rounded-md = calc(var(--radius) - 2px)  = 6px
rounded-lg = var(--radius)              = 8px
```

### Typography (Tailwind defaults)
- `font-sans`: Inter / Geist / `ui-sans-serif, system-ui, ...`
- Base size `0.875rem`–`1rem`, normal weight body, `font-medium`(500)/`font-semibold`(600) for emphasis. No condensed display face, no global monospace.

### Shadows (Tailwind)
```
shadow-sm = 0 1px 2px 0 rgb(0 0 0 / 0.05)
shadow    = 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)
shadow-md = 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)
```

---

## 3. Mapping Strategy (shadcn → Mantine)

DMC/Mantine can't take a JS `cssVariablesResolver`, so we bridge in two layers:

1. **Mantine theme object** (`flowtides_theme.py`) — set color arrays, radius, fonts,
   shadows, primary so DMC components pick up shadcn-ish values out of the box.
2. **CSS variable overrides** (`assets/styles.css`) — define the shadcn semantic vars
   on `:root` / `[data-mantine-color-scheme="dark"]`, and **remap Mantine's own CSS
   variables** (`--mantine-color-body`, `--mantine-color-default-border`, etc.) to the
   shadcn tokens so surfaces/borders/text follow shadcn exactly.

### Key Mantine variable remaps (in CSS)
| Mantine var | shadcn token |
|-------------|--------------|
| `--mantine-color-body` | `hsl(var(--background))` |
| `--mantine-color-text` | `hsl(var(--foreground))` |
| `--mantine-color-default` (surfaces) | `hsl(var(--card))` |
| `--mantine-color-default-border` | `hsl(var(--border))` |
| `--mantine-color-dimmed` | `hsl(var(--muted-foreground))` |
| `--mantine-primary-color-filled` | `hsl(var(--primary))` |
| `--mantine-primary-color-filled-hover` | `primary` @ ~92% L |
| focus ring color | `hsl(var(--ring))` |

### Color arrays
- Rebuild `blue` 10-shade array around hue **221** (light primary = index 6, dark primary = index 5) so `color="blue"` everywhere stays correct.
- Replace the pure-black `dark` array with shadcn **slate-dark** values
  (body `222 84% 4.9%`, card same, secondary/muted/border `217 33% 17.5%`).
- Rebuild `slate` array from shadcn slate (cool gray, not the current custom values).
- Keep `green`/`yellow`/`red` but retune `red` to shadcn `--destructive`.

---

## 4. Phased Implementation

### Phase 0 — Safety / baseline
- [x] Branch `feat/shadcn-theme` created.
- [ ] Screenshot current Home, Tools, Settings (light + dark) for before/after diffing.
- [ ] Add a memory note in `/memories/repo/` documenting the token mapping decisions.

### Phase 1 — Tokens in `flowtides_theme.py`
- [ ] Add shadcn HSL constants (light + dark token dicts).
- [ ] Rebuild `BLUE` scale around hue 221; update `primaryShade` to `{light:6, dark:5}`.
- [ ] Replace `dark` palette array with shadcn slate-dark values.
- [ ] Replace `SLATE` array with shadcn slate.
- [ ] Retune `RED` to `--destructive`.
- [ ] `defaultRadius` → `"md"`; redefine `radius` scale to `{xs:4, sm:6, md:8, lg:12, xl:16}` (8px = shadcn `lg`/`--radius`).
- [ ] Replace `shadows` with Tailwind-equivalent subtle set; **remove `glow`**.
- [ ] Typography: collapse `FONT_DISPLAY/BODY/MONO` to a single Inter/Geist/system sans stack; drop mono-everywhere (keep an optional mono only for true numeric tables if desired).
- [ ] Update `headings` sizes/weights to shadcn scale (semibold, normal line-height, no condensed).

### Phase 2 — Component defaults in `dmc_theme["components"]`
- [ ] `Button`: `radius="md"`, default `variant="filled"`; ensure filled = primary bg + `primary-foreground` text.
- [ ] `Card` / `Paper`: `radius="lg"` (8px), `withBorder=True`, shadow `xs`/none; remove hover glow.
- [ ] `Badge`: `radius="md"`, `variant="light"` secondary look.
- [ ] `Input`/`Select`/`Textarea`: `radius="md"`, drop mono font, border = `--input`, focus = `--ring`.
- [ ] `NavLink`: active = `secondary`/`accent` muted fill with `accent-foreground` (shadcn sidebar style) instead of blue glow.
- [ ] `Table`: keep border, neutral header (`muted`), `highlightOnHover` → `muted` row.
- [ ] `Tooltip`/`Popover`/`Menu`: `popover` bg, `border`, `md` radius, subtle shadow.

### Phase 3 — CSS variables & overrides in `assets/styles.css`
- [ ] Add shadcn `:root` (light) and `[data-mantine-color-scheme="dark"]` token blocks.
- [ ] Remap Mantine core CSS vars (table in §3) to shadcn tokens.
- [ ] Replace `.metric-card` glow hover with shadcn hover (muted bg / `border` shift, `shadow-sm`).
- [ ] Rewrite NavLink hover/active rules to use `--accent` / `--accent-foreground`.
- [ ] Update font `@import` (Inter/Geist) and set `font-feature-settings`.
- [ ] Add `--ring` focus-visible outline (`2px` + `2px` offset) globally.

### Phase 4 — Widget touch-ups
- [ ] [metric_card.py](../components/ui/metric_card.py): drop electric ThemeIcon `variant="light"` glow if needed; align radius.
- [ ] [dashboard.py](../components/layouts/dashboard.py): header title color → `foreground`/`primary` per shadcn; logo accent.
- [ ] [theme_toggle.py](../components/ui/theme_toggle.py): keep; restyle switch track to `--input`/`--primary`.
- [ ] Audit inline style helpers (`style_card_featured_*`, `style_kpi_value`, `style_section_header`) — replace glow/gradient with flat shadcn equivalents; keep API/signatures stable so pages don't break.

### Phase 5 — Plotly templates
- [ ] `PLOTLY_TEMPLATE_DARK/LIGHT`: `paper/plot_bgcolor` = `--card`, grid = `--border`, font = `--foreground`/`--muted-foreground`, colorway lead = shadcn blue.

### Phase 6 — Verify
- [ ] `python app.py`, click through Home / Tools / Settings in light + dark.
- [ ] Check: buttons, cards, nav active state, inputs, tables, badges, tooltips, charts.
- [ ] Confirm `prefers-reduced-motion` still disables transitions.
- [ ] Before/after screenshot comparison.

---

## 5. Design Decisions / Open Questions

1. **Accent**: keep **blue** primary (shadcn "blue" theme) vs. shadcn default monochrome
   (near-black primary). Recommendation: **keep blue** — minimal churn, all `color="blue"`
   usages stay valid, still authentically shadcn.
2. **Backwards-compat helpers**: preserve names/signatures of `style_*` helpers and `SPAN_*`
   exports so no `pages/**` edits are required; only their *values* change.
3. **Mono font**: shadcn uses sans everywhere. Decide whether numeric KPI/table cells keep a
   mono face (Geist Mono) for readability or go full sans. Recommendation: optional Geist Mono
   for data cells only.
4. **Radius intensity**: shadcn default `0.5rem`. Confirm we want the softer 8px corners vs.
   the current 4px "tactical" feel.

---

## 6. Rollback

All changes are isolated to `flowtides_theme.py`, `assets/styles.css`, and a handful of
`components/ui/*` widgets on branch `feat/shadcn-theme`. Revert = `git checkout main` or drop
the branch. No data, model, or route changes involved.
