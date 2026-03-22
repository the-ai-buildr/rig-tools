# Well JSON File Manager — Implementation Plan

## Goal
Convert the existing Excel-based well data format to an optimized JSON schema,
then build an upload / download / create-new workflow so users can manage well
files locally — no database required for basic data exchange.

---

## 1. JSON Schema Design

The new schema covers everything in `Well Template.xlsx` (7 sheets) plus the
fields already in `src/data/models.py`, de-duplicated and flattened where safe.

```json
{
  "schema_version": "1.0",
  "well_id": "<uuid>",
  "created_at": "<ISO-8601>",
  "modified_at": "<ISO-8601>",

  "header": {
    "well_name": "BENEDUM 3G 7H",
    "operator": "",
    "rig_name": "HP 643",
    "afe_number": "",
    "job_id": "",
    "license_number": "",
    "api_number": "",
    "state": "Texas",
    "county": "Upton",
    "country": "USA",
    "field": "Spraberry Trend",
    "formation": "",
    "spud_date": "2024-01-01",
    "rig_release_date": null,
    "latitude": null,
    "longitude": null,
    "directions_to_well": ""
  },

  "wellbores": [
    {
      "wellbore_id": "<uuid>",
      "wellbore_name": "CONST",
      "hole_size_in": 17.5,
      "plan_start_md_ft": 100,
      "plan_end_md_ft": 1200
    }
  ],

  "casing": [
    {
      "casing_id": "<uuid>",
      "casing_name": "Conductor",
      "wellbore_name": "CONST",
      "od_in": 13.375,
      "id_in": null,
      "weight_lbft": 54.5,
      "grade": "J-55",
      "top_md_ft": 0,
      "bottom_md_ft": 1200
    }
  ],

  "mud": [
    {
      "mud_id": "<uuid>",
      "name": "Int 1",
      "mud_type": "Brine",
      "min_weight_ppg": 10.0,
      "max_weight_ppg": 10.5,
      "plan_start_md_ft": 1200,
      "plan_end_md_ft": 5310
    }
  ],

  "directional": [
    {
      "survey_type": "Plan",
      "md_ft": 0,
      "inclination_deg": 0.0,
      "azimuth_deg": 0.0,
      "tvd_ft": 0.0
    }
  ],

  "geology": [
    {
      "formation_name": "Spraberry Upper",
      "short_name": "Sprbry U",
      "top_md_ft": 8500,
      "top_tvd_ft": 8200
    }
  ],

  "drilling_string": [
    {
      "bha_id": "<uuid>",
      "bha_name": "INT 1 BHA",
      "provider": "HES",
      "bit_od_in": 12.25,
      "string_id_in": 8.835,
      "is_rss": false,
      "plan_start_md_ft": 1200,
      "plan_end_md_ft": 5310
    }
  ]
}
```

**Design decisions:**
- Units encoded in field names (`_ft`, `_in`, `_ppg`, `_deg`) — avoids silent
  unit mix-ups when files are exchanged between metric/US users.
- `schema_version` allows future migrations without breaking existing files.
- All lists are optional/empty-by-default so a minimal well file is valid.
- UUIDs generated on create, preserved on round-trip.

---

## 2. Files to Create / Modify

### New files

| File | Purpose |
|------|---------|
| `src/data/well_schema.py` | Pure dataclasses for new sub-entities (DirectionalPoint, GeologyFormation, DrillingString); `WellFile` root dataclass; `to_dict` / `from_dict` helpers |
| `src/data/well_io.py` | `well_to_json(well)→str`, `well_from_json(text)→WellFile`, `xlsx_to_well_file(bytes)→WellFile`, `validate_well_file(dict)→(bool, list[str])` |
| `src/api/routes/well_files.py` | FastAPI router: `POST /well-files/import` (upload JSON), `GET /well-files/{id}/export` (download JSON), `POST /well-files/validate` |
| `src/api/models/well_file_models.py` | Pydantic v2 schemas mirroring `WellFile` for API request/response |
| `src/components/wells/file_manager.py` | `@st.fragment` component: tabs for Upload / Download / Create New |

### Modified files

| File | Change |
|------|--------|
| `src/data/models.py` | Add `DirectionalPoint`, `GeologyFormation`, `DrillingString` dataclasses; add optional lists to `Well` |
| `src/api/models/project_models.py` | Add Pydantic schemas for the three new sub-entities; extend `WellRead` / `WellCreate` |
| `src/api/routes/__init__.py` | Register `well_files` router |
| `src/api/frontend/api_client.py` | Add `import_well_file()`, `export_well_file()`, `validate_well_file()` |
| `src/_pages/05_well.py` | Add `file_manager()` component call in a sidebar expander or new tab |

---

## 3. Implementation Steps

### Step 1 — Data layer: `src/data/well_schema.py`

Define dataclasses:
- `DirectionalPoint(md_ft, inclination_deg, azimuth_deg, tvd_ft, survey_type)`
- `GeologyFormation(formation_name, short_name, top_md_ft, top_tvd_ft)`
- `DrillingString(bha_id, bha_name, provider, bit_od_in, string_id_in, is_rss, plan_start_md_ft, plan_end_md_ft)`
- `WellFile` — root object with `schema_version`, `well_id`, timestamps, `header`, and all seven lists

Implement:
- `WellFile.to_dict()` → plain dict (JSON-serializable)
- `WellFile.from_dict(d)` → `WellFile` (with validation / defaults)
- `WellFile.new(well_name)` → blank scaffold with generated UUID

### Step 2 — `src/data/models.py` extension

Add the three new dataclasses (or import from `well_schema.py`) and append
optional fields to `Well`:
```python
directional: list[DirectionalPoint] = field(default_factory=list)
geology: list[GeologyFormation] = field(default_factory=list)
drilling_string: list[DrillingString] = field(default_factory=list)
```
Update `project_to_dict` / `project_from_dict` serializers accordingly.

### Step 3 — IO helpers: `src/data/well_io.py`

- `well_to_json(wf: WellFile, indent=2) → str`
- `well_from_json(text: str) → tuple[WellFile | None, str | None]`  — returns `(obj, error)`
- `validate_well_file(d: dict) → tuple[bool, list[str]]` — checks required fields, types, depth ordering
- `xlsx_to_well_file(file_bytes: bytes) → tuple[WellFile | None, str | None]` — openpyxl-based parser for the Excel template (best-effort; skips empty sheets)

### Step 4 — API models: `src/api/models/well_file_models.py`

Pydantic v2 models:
- `DirectionalPointSchema`, `GeologyFormationSchema`, `DrillingStringSchema`
- `WellFileSchema` (full read model)
- `WellFileImportRequest` (accepts raw JSON body or multipart file)
- `WellFileValidateResponse(valid: bool, errors: list[str])`
- `WellFileExportResponse(filename: str, content: str)`  — base64 or raw JSON string

### Step 5 — API routes: `src/api/routes/well_files.py`

```
POST /well-files/validate   — validate a JSON body, return errors list
POST /well-files/import     — parse uploaded JSON, upsert into project store
GET  /well-files/{id}/export — serialize stored well to JSON, return as download
POST /well-files/from-xlsx  — parse uploaded Excel file → WellFile JSON
```

All routes use `Depends(get_file_db)` (file-based, no Supabase required).

### Step 6 — Frontend component: `src/components/wells/file_manager.py`

`@st.fragment`-decorated function `well_file_manager(well_id: str | None)` with three tabs:

**Tab 1 — Upload**
- `st.file_uploader` accepting `.json`
- On upload: call `api_client.validate_well_file()`, show errors or success
- "Import" button: call `api_client.import_well_file()`, refresh state

**Tab 2 — Download**
- Shows current well name and metadata summary
- "Download JSON" button: calls `api_client.export_well_file(well_id)`, uses
  `st.download_button` to push the file to browser

**Tab 3 — Create New**
- Minimal form: well name, operator, rig name, state, county, field
- Optional: spud date, API number
- "Create" button: builds a blank `WellFile`, calls import endpoint, redirects
  to well page

### Step 7 — Wire into well page `src/_pages/05_well.py`

Add a "Well File" expander or sidebar section that calls `well_file_manager()`.
Keep it unobtrusive — a collapsed expander works well.

### Step 8 — Register router and API client helpers

- `src/api/routes/__init__.py`: `app.include_router(well_files_router)`
- `src/api/frontend/api_client.py`: add three wrapper functions

---

## 4. Dependency Check

`openpyxl` is needed for Excel parsing. Check `requirements.txt` — add if missing.
No other new dependencies.

---

## 5. Out of Scope (this ticket)

- Metric / US unit conversion on import (values stored as-is with unit suffix in key)
- Supabase persistence (current file-based DB layer is sufficient)
- Directional survey visualization
- Multi-well batch import
