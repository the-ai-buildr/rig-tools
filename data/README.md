# Data Directory

Reference data (pipe specs, formation tops, etc.) and examples for loading/saving data in Rig Tools.

## Bundled vs. Persistent Data

| Type | Path | Persists? |
|------|------|-----------|
| **Bundled** | `/home/pyodide/app/data/` | No (read-only, shipped with app) |
| **IDBFS** | `/mnt/` | Yes (add `idbfsMountpoints: ["/mnt"]` to package.json) |
| **NODEFS** | `/mnt/` or custom | Yes (add `nodefsMountpoints` to package.json) |

---

## Bundled reference data

Files in this `data/` folder are bundled at build time and appear at:

```
/home/pyodide/app/data/<filename>
```

### Example: load bundled CSV

```python
import pandas as pd

def load_reference_pipe_specs():
    path = "/home/pyodide/app/data/pipe_specs.csv"
    return pd.read_csv(path)

df = load_reference_pipe_specs()
```

### Example: load bundled JSON

```python
import json

def load_reference_data():
    path = "/home/pyodide/app/data/config.json"
    with open(path) as f:
        return json.load(f)

config = load_reference_data()
```

---

## Persistent user data (IDBFS)

To persist tables/files across app restarts, add to `package.json`:

```json
"stlite": {
  "desktop": {
    "idbfsMountpoints": ["/mnt"]
  }
}
```

Then run `npm run dump` again.

### Example: save/load table to IndexedDB

```python
import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = "/mnt/saved_table.csv"

if Path(DATA_PATH).exists():
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame({"col1": [], "col2": []})

df = st.data_editor(df, num_rows="dynamic")
if st.button("Save"):
    df.to_csv(DATA_PATH, index=False)
    st.success("Saved.")
```

**Note:** With IDBFS you must call `pyodide.FS.syncfs(false)` after writes to persist to IndexedDB. See the main project README for sync details.

---

## Host filesystem access (NODEFS)

To read/write real files on disk, add to `package.json`:

```json
"stlite": {
  "desktop": {
    "nodeJsWorker": true,
    "nodefsMountpoints": {
      "/mnt": "{{userData}}"
    }
  }
}
```

Placeholders: `{{userData}}`, `{{home}}`, `{{temp}}` — resolved via Electron `app.getPath()`.

### Example: save to app data folder

```python
import pandas as pd
from pathlib import Path

# {{userData}} → e.g. ~/Library/Application Support/Rig Tools (macOS)
df.to_csv("/mnt/results.csv", index=False)
df = pd.read_csv("/mnt/results.csv")
```

---

## Session-only data

For temporary data (lost on restart):

```python
if "scratch_df" not in st.session_state:
    st.session_state.scratch_df = pd.DataFrame()

st.session_state.scratch_df = st.data_editor(st.session_state.scratch_df)
```
