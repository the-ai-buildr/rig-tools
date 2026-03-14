"""
Database Module — Well Dashboard API

Provides the ``Database`` class with async methods for every CRUD operation
used by the route modules.

This file is the single source of truth for all database interactions.
All route modules import and instantiate ``Database`` at module level:

    from api.database import Database
    db = Database()

Schema (SQLite, managed by ``init_database()``)
-----------------------------------------------
    users              id, username, password_hash, email, created_at
    projects           id, project_name, project_type, pad_name, ..., created_by
    wells              id, project_id, well_name, ..., current_status
    wellbore_details   id, well_id, ..., is_plan
    casing_strings     id, well_id, ..., is_plan
    tubular_strings    id, well_id, ..., is_plan
    directional_surveys id, well_id, md, inclination, azimuth, ..., survey_type
    templates          id, template_name, template_type, template_data (JSON), created_by
    status_history     id, well_id, old_status, new_status, changed_by, changed_at, notes

Extending the schema
--------------------
1. Add CREATE TABLE IF NOT EXISTS statement to ``init_database()``.
2. Add CRUD methods below using the async ``aiosqlite`` pattern.
3. Call the new methods from the appropriate route module.

NOTE: This stub contains method signatures and docstrings only.
      Full SQL implementations from the original codebase slot directly in.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiosqlite

from api.config import settings


class Database:
    """
    Async SQLite database interface.

    All public methods are ``async`` and safe to ``await`` inside FastAPI
    route handlers. The underlying connection uses ``aiosqlite`` for
    non-blocking I/O.

    Usage::

        db = Database()

        # In a lifespan/startup handler:
        await db.init_database()

        # In a route:
        project = await db.get_project_by_id(project_id)
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.DATABASE_PATH
        self._conn: Optional[aiosqlite.Connection] = None

    # ── Connection management ─────────────────────────────────────────────────

    async def get_connection(self) -> aiosqlite.Connection:
        """Return (or lazily open) the shared async connection."""
        if self._conn is None:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self._conn = await aiosqlite.connect(self.db_path)
            self._conn.row_factory = aiosqlite.Row
            await self._conn.execute("PRAGMA foreign_keys = ON")
        return self._conn

    async def close(self) -> None:
        """Close the database connection on application shutdown."""
        if self._conn:
            await self._conn.close()
            self._conn = None

    # ── Schema ────────────────────────────────────────────────────────────────

    async def init_database(self) -> None:
        """
        Create all tables (if they don't already exist) and seed pre-built templates.

        Called once at application startup from ``api/main.py > lifespan()``.
        """
        conn = await self.get_connection()

        await conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    UNIQUE NOT NULL,
                password_hash TEXT    NOT NULL,
                email         TEXT,
                created_at    TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS projects (
                id                   INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name         TEXT    NOT NULL,
                project_type         TEXT    DEFAULT 'single_well',
                pad_name             TEXT,
                surface_location_lat REAL,
                surface_location_lon REAL,
                field                TEXT,
                operator             TEXT,
                description          TEXT,
                created_by           INTEGER REFERENCES users(id),
                created_at           TEXT    DEFAULT (datetime('now')),
                updated_at           TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS wells (
                id                           INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id                   INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                well_name                    TEXT    NOT NULL,
                well_number                  TEXT,
                api_number                   TEXT,
                well_type                    TEXT,
                surface_lat                  REAL,
                surface_lon                  REAL,
                bottom_hole_lat              REAL,
                bottom_hole_lon              REAL,
                rig_name                     TEXT,
                contractor                   TEXT,
                spud_date                    TEXT,
                completion_date              TEXT,
                release_date                 TEXT,
                total_depth_planned          REAL,
                total_depth_actual           REAL,
                measured_depth_planned       REAL,
                measured_depth_actual        REAL,
                true_vertical_depth_planned  REAL,
                true_vertical_depth_actual   REAL,
                kick_off_point               REAL,
                current_status               TEXT    DEFAULT 'Planned',
                description                  TEXT,
                created_at                   TEXT    DEFAULT (datetime('now')),
                updated_at                   TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS wellbore_details (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                well_id        INTEGER REFERENCES wells(id) ON DELETE CASCADE,
                section_name   TEXT,
                section_type   TEXT,
                top_md         REAL,
                bottom_md      REAL,
                top_tvd        REAL,
                bottom_tvd     REAL,
                hole_size      REAL,
                hole_size_unit TEXT    DEFAULT 'in',
                mud_weight     REAL,
                mud_type       TEXT,
                description    TEXT,
                is_plan        INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS casing_strings (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                well_id          INTEGER REFERENCES wells(id) ON DELETE CASCADE,
                string_name      TEXT,
                string_type      TEXT,
                top_md           REAL,
                bottom_md        REAL,
                top_tvd          REAL,
                bottom_tvd       REAL,
                casing_od        REAL,
                casing_id        REAL,
                weight           REAL,
                grade            TEXT,
                connection       TEXT,
                cement_top_md    REAL,
                cement_bottom_md REAL,
                cement_volume    REAL,
                installed_date   TEXT,
                description      TEXT,
                is_plan          INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS tubular_strings (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                well_id         INTEGER REFERENCES wells(id) ON DELETE CASCADE,
                string_name     TEXT,
                string_type     TEXT,
                component_name  TEXT,
                top_md          REAL,
                bottom_md       REAL,
                outer_diameter  REAL,
                inner_diameter  REAL,
                weight          REAL,
                length          REAL,
                grade           TEXT,
                connection      TEXT,
                material        TEXT,
                description     TEXT,
                is_plan         INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS directional_surveys (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                well_id          INTEGER REFERENCES wells(id) ON DELETE CASCADE,
                md               REAL,
                inclination      REAL,
                azimuth          REAL,
                tvd              REAL,
                northing         REAL,
                easting          REAL,
                vertical_section REAL,
                dls              REAL,
                tool_face        REAL,
                section          TEXT,
                survey_type      TEXT    DEFAULT 'plan',
                survey_date      TEXT,
                survey_company   TEXT,
                tool_type        TEXT
            );

            CREATE TABLE IF NOT EXISTS templates (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name  TEXT    NOT NULL,
                template_type  TEXT    DEFAULT 'custom',
                category       TEXT,
                description    TEXT,
                template_data  TEXT,
                created_by     INTEGER REFERENCES users(id),
                is_default     INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS status_history (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                well_id      INTEGER REFERENCES wells(id) ON DELETE CASCADE,
                old_status   TEXT,
                new_status   TEXT,
                changed_by   INTEGER REFERENCES users(id),
                changed_at   TEXT DEFAULT (datetime('now')),
                notes        TEXT
            );
        """)
        await conn.commit()
        await self._seed_default_user(conn)
        await self._seed_prebuilt_templates(conn)

    # ── Seeding ───────────────────────────────────────────────────────────────

    async def _seed_default_user(self, conn: aiosqlite.Connection) -> None:
        """Create the default admin user if no users exist yet."""
        from api.auth import get_password_hash
        cursor = await conn.execute("SELECT COUNT(*) FROM users")
        (count,) = await cursor.fetchone()
        if count == 0:
            await conn.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                ("admin", get_password_hash("admin123"), "admin@welldashboard.local"),
            )
            await conn.commit()

    async def _seed_prebuilt_templates(self, conn: aiosqlite.Connection) -> None:
        """Insert pre-built templates if the table is empty."""
        cursor = await conn.execute(
            "SELECT COUNT(*) FROM templates WHERE template_type = 'prebuilt'"
        )
        (count,) = await cursor.fetchone()
        if count > 0:
            return

        prebuilt = [
            {
                "template_name": "Standard Onshore Well",
                "category": "Onshore",
                "description": "Typical onshore vertical well with conductor, surface, and production casing.",
                "template_data": json.dumps({
                    "wellbore": [
                        {"section_name": "Conductor", "section_type": "surface", "top_md": 0, "bottom_md": 100, "hole_size": 26},
                        {"section_name": "Surface",   "section_type": "surface", "top_md": 0, "bottom_md": 2000, "hole_size": 17.5},
                        {"section_name": "Production","section_type": "production","top_md": 0,"bottom_md": 8000, "hole_size": 12.25},
                    ],
                    "casing": [
                        {"string_name": "Conductor",  "string_type": "conductor",  "top_md": 0, "bottom_md": 100,  "casing_od": 20},
                        {"string_name": "Surface",    "string_type": "surface",    "top_md": 0, "bottom_md": 2000, "casing_od": 13.375},
                        {"string_name": "Production", "string_type": "production", "top_md": 0, "bottom_md": 8000, "casing_od": 9.625},
                    ],
                }),
            },
            {
                "template_name": "Offshore Deep Well",
                "category": "Offshore",
                "description": "Offshore well with riser, conductor, surface, intermediate, and production strings.",
                "template_data": json.dumps({
                    "wellbore": [
                        {"section_name": "Riser",        "section_type": "surface",     "top_md": 0,   "bottom_md": 300,   "hole_size": 36},
                        {"section_name": "Conductor",    "section_type": "surface",     "top_md": 0,   "bottom_md": 1000,  "hole_size": 26},
                        {"section_name": "Surface",      "section_type": "surface",     "top_md": 0,   "bottom_md": 3000,  "hole_size": 17.5},
                        {"section_name": "Intermediate", "section_type": "intermediate","top_md": 0,   "bottom_md": 10000, "hole_size": 12.25},
                        {"section_name": "Production",   "section_type": "production",  "top_md": 0,   "bottom_md": 18000, "hole_size": 8.5},
                    ],
                }),
            },
            {
                "template_name": "Horizontal Well",
                "category": "Horizontal / Directional",
                "description": "Directional well with a build section and horizontal lateral.",
                "template_data": json.dumps({
                    "wellbore": [
                        {"section_name": "Vertical",    "section_type": "surface",    "top_md": 0,    "bottom_md": 5000,  "hole_size": 12.25},
                        {"section_name": "Build",       "section_type": "intermediate","top_md": 5000, "bottom_md": 7000, "hole_size": 8.75},
                        {"section_name": "Lateral",     "section_type": "production", "top_md": 7000, "bottom_md": 14000,"hole_size": 6.125},
                    ],
                }),
            },
        ]

        for t in prebuilt:
            await conn.execute(
                """INSERT INTO templates
                   (template_name, template_type, category, description, template_data, is_default)
                   VALUES (?, 'prebuilt', ?, ?, ?, 1)""",
                (t["template_name"], t["category"], t["description"], t["template_data"]),
            )
        await conn.commit()

    # ── Users ─────────────────────────────────────────────────────────────────

    async def create_user(self, username: str, password_hash: str, email: Optional[str]) -> int:
        conn = await self.get_connection()
        cursor = await conn.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email),
        )
        await conn.commit()
        return cursor.lastrowid

    async def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_user_by_username(self, username: str) -> Optional[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = await cursor.fetchone()
        return dict(row) if row else None

    # ── Projects ──────────────────────────────────────────────────────────────

    async def create_project(self, data: Dict) -> int:
        conn = await self.get_connection()
        cursor = await conn.execute(
            """INSERT INTO projects
               (project_name, project_type, pad_name, surface_location_lat, surface_location_lon,
                field, operator, description, created_by)
               VALUES (:project_name, :project_type, :pad_name, :surface_location_lat,
                       :surface_location_lon, :field, :operator, :description, :created_by)""",
            data,
        )
        await conn.commit()
        return cursor.lastrowid

    async def get_project_by_id(self, project_id: int) -> Optional[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute(
            """SELECT p.*,
                      (SELECT COUNT(*) FROM wells w WHERE w.project_id = p.id) AS well_count
               FROM projects p WHERE p.id = ?""",
            (project_id,),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_all_projects(self, user_id: int, project_type: Optional[str] = None) -> List[Dict]:
        conn = await self.get_connection()
        query = """SELECT p.*,
                          (SELECT COUNT(*) FROM wells w WHERE w.project_id = p.id) AS well_count
                   FROM projects p WHERE p.created_by = ?"""
        params: list = [user_id]
        if project_type:
            query += " AND p.project_type = ?"
            params.append(project_type)
        query += " ORDER BY p.created_at DESC"
        cursor = await conn.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]

    async def update_project(self, project_id: int, data: Dict) -> None:
        conn = await self.get_connection()
        data["updated_at"] = datetime.now().isoformat()
        data["project_id"] = project_id
        sets = ", ".join(f"{k} = :{k}" for k in data if k != "project_id")
        await conn.execute(f"UPDATE projects SET {sets} WHERE id = :project_id", data)
        await conn.commit()

    async def delete_project(self, project_id: int) -> None:
        conn = await self.get_connection()
        await conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        await conn.commit()

    # ── Wells ─────────────────────────────────────────────────────────────────

    async def create_well(self, data: Dict) -> int:
        data = {k: v for k, v in data.items() if k != "template_id"}
        conn = await self.get_connection()
        cursor = await conn.execute(
            """INSERT INTO wells
               (project_id, well_name, well_number, api_number, well_type,
                surface_lat, surface_lon, bottom_hole_lat, bottom_hole_lon,
                rig_name, contractor, spud_date, completion_date, release_date,
                total_depth_planned, measured_depth_planned, true_vertical_depth_planned,
                kick_off_point, description)
               VALUES
               (:project_id, :well_name, :well_number, :api_number, :well_type,
                :surface_lat, :surface_lon, :bottom_hole_lat, :bottom_hole_lon,
                :rig_name, :contractor, :spud_date, :completion_date, :release_date,
                :total_depth_planned, :measured_depth_planned, :true_vertical_depth_planned,
                :kick_off_point, :description)""",
            data,
        )
        await conn.commit()
        return cursor.lastrowid

    async def get_well_by_id(self, well_id: int) -> Optional[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT * FROM wells WHERE id = ?", (well_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_wells_by_project(self, project_id: int, status: Optional[str] = None) -> List[Dict]:
        conn = await self.get_connection()
        query = "SELECT * FROM wells WHERE project_id = ?"
        params: list = [project_id]
        if status:
            query += " AND current_status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC"
        cursor = await conn.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]

    async def update_well(self, well_id: int, data: Dict) -> None:
        conn = await self.get_connection()
        data["updated_at"] = datetime.now().isoformat()
        data["well_id"] = well_id
        sets = ", ".join(f"{k} = :{k}" for k in data if k != "well_id")
        await conn.execute(f"UPDATE wells SET {sets} WHERE id = :well_id", data)
        await conn.commit()

    async def delete_well(self, well_id: int) -> None:
        conn = await self.get_connection()
        await conn.execute("DELETE FROM wells WHERE id = ?", (well_id,))
        await conn.commit()

    async def update_well_status(
        self, well_id: int, new_status: str, user_id: int, notes: Optional[str] = None
    ) -> None:
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT current_status FROM wells WHERE id = ?", (well_id,))
        row = await cursor.fetchone()
        old_status = row["current_status"] if row else "Unknown"

        await conn.execute(
            "UPDATE wells SET current_status = ?, updated_at = ? WHERE id = ?",
            (new_status, datetime.now().isoformat(), well_id),
        )
        await conn.execute(
            """INSERT INTO status_history (well_id, old_status, new_status, changed_by, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (well_id, old_status, new_status, user_id, notes),
        )
        await conn.commit()

    async def get_complete_well_data(self, well_id: int) -> Optional[Dict]:
        """Return the well with all nested sub-data arrays populated."""
        well = await self.get_well_by_id(well_id)
        if not well:
            return None

        well["wellbore_plan"]   = await self.get_wellbore_sections(well_id, is_plan=True)
        well["wellbore_actual"] = await self.get_wellbore_sections(well_id, is_plan=False)
        well["casing_plan"]     = await self.get_casing_strings(well_id, is_plan=True)
        well["casing_actual"]   = await self.get_casing_strings(well_id, is_plan=False)
        well["tubular_plan"]    = await self.get_tubular_strings(well_id, is_plan=True)
        well["tubular_actual"]  = await self.get_tubular_strings(well_id, is_plan=False)
        well["survey_plan"]     = await self.get_survey_points(well_id, survey_type="plan")
        well["survey_actual"]   = await self.get_survey_points(well_id, survey_type="actual")
        well["status_history"]  = await self._get_status_history(well_id)
        return well

    async def get_complete_project_data(self, project_id: int) -> Optional[Dict]:
        """Return the project with a list of fully-populated well dicts."""
        project = await self.get_project_by_id(project_id)
        if not project:
            return None
        raw_wells = await self.get_wells_by_project(project_id)
        project["wells"] = [await self.get_complete_well_data(w["id"]) for w in raw_wells]
        return project

    # ── Wellbore sections ─────────────────────────────────────────────────────

    async def add_wellbore_section(self, data: Dict) -> int:
        conn = await self.get_connection()
        cursor = await conn.execute(
            """INSERT INTO wellbore_details
               (well_id, section_name, section_type, top_md, bottom_md, top_tvd, bottom_tvd,
                hole_size, hole_size_unit, mud_weight, mud_type, description, is_plan)
               VALUES
               (:well_id, :section_name, :section_type, :top_md, :bottom_md, :top_tvd, :bottom_tvd,
                :hole_size, :hole_size_unit, :mud_weight, :mud_type, :description, :is_plan)""",
            data,
        )
        await conn.commit()
        return cursor.lastrowid

    async def get_wellbore_section_by_id(self, section_id: int) -> Optional[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT * FROM wellbore_details WHERE id = ?", (section_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_wellbore_sections(self, well_id: int, is_plan: Optional[bool] = None) -> List[Dict]:
        conn = await self.get_connection()
        query = "SELECT * FROM wellbore_details WHERE well_id = ?"
        params: list = [well_id]
        if is_plan is not None:
            query += " AND is_plan = ?"
            params.append(1 if is_plan else 0)
        query += " ORDER BY top_md"
        cursor = await conn.execute(query, params)
        return [dict(r) for r in await cursor.fetchall()]

    # ── Casing strings ────────────────────────────────────────────────────────

    async def add_casing_string(self, data: Dict) -> int:
        conn = await self.get_connection()
        cursor = await conn.execute(
            """INSERT INTO casing_strings
               (well_id, string_name, string_type, top_md, bottom_md, top_tvd, bottom_tvd,
                casing_od, casing_id, weight, grade, connection, cement_top_md, cement_bottom_md,
                cement_volume, installed_date, description, is_plan)
               VALUES
               (:well_id, :string_name, :string_type, :top_md, :bottom_md, :top_tvd, :bottom_tvd,
                :casing_od, :casing_id, :weight, :grade, :connection, :cement_top_md, :cement_bottom_md,
                :cement_volume, :installed_date, :description, :is_plan)""",
            data,
        )
        await conn.commit()
        return cursor.lastrowid

    async def get_casing_string_by_id(self, casing_id: int) -> Optional[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT * FROM casing_strings WHERE id = ?", (casing_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_casing_strings(self, well_id: int, is_plan: Optional[bool] = None) -> List[Dict]:
        conn = await self.get_connection()
        query = "SELECT * FROM casing_strings WHERE well_id = ?"
        params: list = [well_id]
        if is_plan is not None:
            query += " AND is_plan = ?"
            params.append(1 if is_plan else 0)
        query += " ORDER BY top_md"
        cursor = await conn.execute(query, params)
        return [dict(r) for r in await cursor.fetchall()]

    # ── Tubular strings ───────────────────────────────────────────────────────

    async def add_tubular_string(self, data: Dict) -> int:
        conn = await self.get_connection()
        cursor = await conn.execute(
            """INSERT INTO tubular_strings
               (well_id, string_name, string_type, component_name, top_md, bottom_md,
                outer_diameter, inner_diameter, weight, length, grade, connection, material,
                description, is_plan)
               VALUES
               (:well_id, :string_name, :string_type, :component_name, :top_md, :bottom_md,
                :outer_diameter, :inner_diameter, :weight, :length, :grade, :connection, :material,
                :description, :is_plan)""",
            data,
        )
        await conn.commit()
        return cursor.lastrowid

    async def get_tubular_string_by_id(self, tubular_id: int) -> Optional[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT * FROM tubular_strings WHERE id = ?", (tubular_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_tubular_strings(self, well_id: int, is_plan: Optional[bool] = None) -> List[Dict]:
        conn = await self.get_connection()
        query = "SELECT * FROM tubular_strings WHERE well_id = ?"
        params: list = [well_id]
        if is_plan is not None:
            query += " AND is_plan = ?"
            params.append(1 if is_plan else 0)
        cursor = await conn.execute(query, params)
        return [dict(r) for r in await cursor.fetchall()]

    # ── Directional surveys ───────────────────────────────────────────────────

    async def add_survey_point(self, data: Dict) -> int:
        conn = await self.get_connection()
        cursor = await conn.execute(
            """INSERT INTO directional_surveys
               (well_id, md, inclination, azimuth, tvd, northing, easting,
                vertical_section, dls, tool_face, section, survey_type, survey_date,
                survey_company, tool_type)
               VALUES
               (:well_id, :md, :inclination, :azimuth, :tvd, :northing, :easting,
                :vertical_section, :dls, :tool_face, :section, :survey_type, :survey_date,
                :survey_company, :tool_type)""",
            data,
        )
        await conn.commit()
        return cursor.lastrowid

    async def get_survey_point_by_id(self, survey_id: int) -> Optional[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT * FROM directional_surveys WHERE id = ?", (survey_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_survey_points(self, well_id: int, survey_type: Optional[str] = None) -> List[Dict]:
        conn = await self.get_connection()
        query = "SELECT * FROM directional_surveys WHERE well_id = ?"
        params: list = [well_id]
        if survey_type:
            query += " AND survey_type = ?"
            params.append(survey_type)
        query += " ORDER BY md"
        cursor = await conn.execute(query, params)
        return [dict(r) for r in await cursor.fetchall()]

    async def delete_survey_points(self, well_id: int, survey_type: Optional[str] = None) -> None:
        conn = await self.get_connection()
        if survey_type:
            await conn.execute(
                "DELETE FROM directional_surveys WHERE well_id = ? AND survey_type = ?",
                (well_id, survey_type),
            )
        else:
            await conn.execute("DELETE FROM directional_surveys WHERE well_id = ?", (well_id,))
        await conn.commit()

    # ── Templates ─────────────────────────────────────────────────────────────

    async def create_template(self, data: Dict) -> int:
        conn = await self.get_connection()
        if isinstance(data.get("template_data"), dict):
            data["template_data"] = json.dumps(data["template_data"])
        cursor = await conn.execute(
            """INSERT INTO templates
               (template_name, template_type, category, description, template_data, created_by)
               VALUES (:template_name, :template_type, :category, :description, :template_data, :created_by)""",
            data,
        )
        await conn.commit()
        return cursor.lastrowid

    async def get_template_by_id(self, template_id: int) -> Optional[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT * FROM templates WHERE id = ?", (template_id,))
        row = await cursor.fetchone()
        if not row:
            return None
        t = dict(row)
        if t.get("template_data"):
            try:
                t["template_data"] = json.loads(t["template_data"])
            except (json.JSONDecodeError, TypeError):
                pass
        return t

    async def get_all_templates(
        self, template_type: Optional[str] = None, user_id: Optional[int] = None
    ) -> List[Dict]:
        conn = await self.get_connection()
        query = "SELECT * FROM templates WHERE (template_type = 'prebuilt'"
        params: list = []
        if user_id:
            query += " OR created_by = ?)"
            params.append(user_id)
        else:
            query += ")"
        if template_type:
            query += " AND template_type = ?"
            params.append(template_type)
        cursor = await conn.execute(query, params)
        rows = await cursor.fetchall()
        result = []
        for row in rows:
            t = dict(row)
            if t.get("template_data"):
                try:
                    t["template_data"] = json.loads(t["template_data"])
                except (json.JSONDecodeError, TypeError):
                    pass
            result.append(t)
        return result

    async def delete_template(self, template_id: int) -> None:
        conn = await self.get_connection()
        await conn.execute("DELETE FROM templates WHERE id = ?", (template_id,))
        await conn.commit()

    async def apply_template_to_well(self, well_id: int, template_data: Dict) -> None:
        """Bulk-insert wellbore, casing, and tubular records from a template dict."""
        for section in template_data.get("wellbore", []):
            await self.add_wellbore_section({**section, "well_id": well_id, "is_plan": 1})
        for casing in template_data.get("casing", []):
            await self.add_casing_string({**casing, "well_id": well_id, "is_plan": 1})
        for tubular in template_data.get("tubulars", []):
            await self.add_tubular_string({**tubular, "well_id": well_id, "is_plan": 1})

    # ── Status history ────────────────────────────────────────────────────────

    async def _get_status_history(self, well_id: int) -> List[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute(
            """SELECT sh.*, u.username AS changed_by_username
               FROM status_history sh
               LEFT JOIN users u ON sh.changed_by = u.id
               WHERE sh.well_id = ?
               ORDER BY sh.changed_at DESC""",
            (well_id,),
        )
        return [dict(r) for r in await cursor.fetchall()]

    # ── Dashboard aggregates ──────────────────────────────────────────────────

    async def get_dashboard_stats(self, user_id: int) -> Dict:
        conn = await self.get_connection()
        projects = await self.get_all_projects(user_id)
        project_ids = [p["id"] for p in projects]

        wells_by_status: Dict[str, int] = {}
        total_wells = 0
        for pid in project_ids:
            wells = await self.get_wells_by_project(pid)
            total_wells += len(wells)
            for w in wells:
                s = w.get("current_status", "Unknown")
                wells_by_status[s] = wells_by_status.get(s, 0) + 1

        return {
            "total_projects": len(projects),
            "total_wells": total_wells,
            "wells_by_status": wells_by_status,
        }

    async def get_recent_activity(self, user_id: int, limit: int = 10) -> List[Dict]:
        conn = await self.get_connection()
        cursor = await conn.execute(
            """SELECT sh.*, w.well_name, u.username AS changed_by_username
               FROM status_history sh
               JOIN wells w ON sh.well_id = w.id
               JOIN projects p ON w.project_id = p.id
               LEFT JOIN users u ON sh.changed_by = u.id
               WHERE p.created_by = ?
               ORDER BY sh.changed_at DESC
               LIMIT ?""",
            (user_id, limit),
        )
        return [dict(r) for r in await cursor.fetchall()]
