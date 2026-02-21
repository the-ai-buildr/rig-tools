# Rig Tools

Oilfield drilling calculators — standalone desktop app built with [stlite](https://github.com/whitphx/stlite) (Streamlit + WebAssembly + Electron).

No server, no internet required. Runs fully offline.

## Development

### Prerequisites
- Node.js 18+
- npm

### Setup

```bash
npm install
```

### Run locally

```bash
npm run dump    # build artifacts
npm run serve   # open Electron window
```

### Package for distribution

```bash
npm run app:dist
# → dist/Rig Tools-x.x.x.dmg  (macOS)
# → dist/Rig Tools Setup x.x.x.exe  (Windows)
```

## Project Structure

```
app.py              # Home screen
pages/              # Calculator pages (one file = one page)
calcs/              # Pure Python calculation modules
data/               # Reference data (pipe specs, etc.)
assets/             # App icons
```

## Adding a New Calculator

1. Copy `pages/01_template.py` → `pages/NN_my_calc.py`
2. Update the title, inputs, and calculation logic
3. Add any new Python deps to `requirements.txt` and `package.json → stlite.desktop.dependencies`
4. Run `npm run dump && npm run serve` to test
