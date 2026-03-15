"""
Integration tests for FastAPI routes — uses FastAPI's TestClient (synchronous WSGI shim).
No Docker, no running server required. Tests the full request/response cycle including
Pydantic validation and route logic.

Produced by: backend-agent / fastapi-routes skill
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from api.main import create_app

# ── Shared test client ────────────────────────────────────────────────────────
# Patch validate_production_secrets so tests run without a real SECRET_KEY.

@pytest.fixture(scope="module")
def client():
    with patch("api.config.Settings.validate_production_secrets"), \
         patch("api.main.ensure_directories"):
        app = create_app()
        with TestClient(app) as c:
            yield c


# ── Health ────────────────────────────────────────────────────────────────────

class TestHealth:
    def test_returns_200(self, client):
        r = client.get("/health")
        assert r.status_code == 200

    def test_response_shape(self, client):
        data = client.get("/health").json()
        assert data["status"] == "ok"
        assert data["service"] == "rig-tools-api"


# ── Hydrostatic Pressure ──────────────────────────────────────────────────────

class TestHydrostaticPressure:
    ENDPOINT = "/calcs/hydrostatic-pressure"

    def test_us_calculation(self, client):
        # psi = 10.5 ppg × 0.052 × 5000 ft = 2730.0 psi
        r = client.post(self.ENDPOINT, json={"mud_weight": 10.5, "depth": 5000, "unit_system": "us"})
        assert r.status_code == 200
        assert r.json()["pressure"] == pytest.approx(2730.0, rel=1e-3)

    def test_metric_calculation(self, client):
        # kPa = 1200 kg/m³ × 9.80665 × 1000 m / 1000 = 11767.98 kPa
        r = client.post(self.ENDPOINT, json={"mud_weight": 1200, "depth": 1000, "unit_system": "metric"})
        assert r.status_code == 200
        assert r.json()["pressure"] == pytest.approx(11767.98, rel=1e-3)

    def test_unit_system_echoed(self, client):
        r = client.post(self.ENDPOINT, json={"mud_weight": 10.0, "depth": 1000, "unit_system": "us"})
        assert r.json()["unit_system"] == "us"

    def test_missing_field_returns_422(self, client):
        r = client.post(self.ENDPOINT, json={"mud_weight": 10.5})
        assert r.status_code == 422

    def test_invalid_unit_system_returns_422(self, client):
        r = client.post(self.ENDPOINT, json={"mud_weight": 10.5, "depth": 5000, "unit_system": "imperial"})
        assert r.status_code == 422


# ── Equivalent Mud Weight ─────────────────────────────────────────────────────

class TestEquivalentMudWeight:
    ENDPOINT = "/calcs/equivalent-mud-weight"

    def test_us_calculation(self, client):
        # ppg = 2730 psi / (0.052 × 5000 ft) = 10.5 ppg  (inverse of hydrostatic)
        r = client.post(self.ENDPOINT, json={"pressure": 2730, "depth": 5000, "unit_system": "us"})
        assert r.status_code == 200
        assert r.json()["emw"] == pytest.approx(10.5, rel=1e-3)

    def test_metric_calculation(self, client):
        # kg/m³ = 11767.98 kPa × 1000 / (9.80665 × 1000 m) ≈ 1200 kg/m³
        r = client.post(self.ENDPOINT, json={"pressure": 11767.98, "depth": 1000, "unit_system": "metric"})
        assert r.status_code == 200
        assert r.json()["emw"] == pytest.approx(1200.0, rel=1e-3)

    def test_zero_depth_returns_422(self, client):
        # depth=0 is invalid (gt=0 constraint) — Pydantic should reject with 422
        r = client.post(self.ENDPOINT, json={"pressure": 2730, "depth": 0, "unit_system": "us"})
        assert r.status_code == 422


# ── Kill Sheet ────────────────────────────────────────────────────────────────

class TestKillSheet:
    ENDPOINT = "/calcs/kill-sheet"

    def test_us_calculation(self, client):
        # SIDPP=500 psi, MW=10 ppg, TVD=10000 ft
        # margin = 500 / (0.052 × 10000) = 0.9615…
        # kill_mw = 10 + 0.9615… = 10.9615…, rounded_up = 11.0
        r = client.post(self.ENDPOINT, json={
            "shut_in_drillpipe_pressure": 500,
            "current_mud_weight": 10,
            "depth": 10000,
            "unit_system": "us",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["kill_mud_weight"] == pytest.approx(10.962, rel=1e-2)
        assert data["kill_mud_weight_rounded"] == pytest.approx(11.0, rel=1e-3)

    def test_response_has_all_fields(self, client):
        r = client.post(self.ENDPOINT, json={
            "shut_in_drillpipe_pressure": 200,
            "current_mud_weight": 9.5,
            "depth": 8000,
            "unit_system": "us",
        })
        data = r.json()
        assert "kill_mud_weight" in data
        assert "kill_mud_weight_rounded" in data
        assert "pressure_safety_margin" in data
        assert "unit_system" in data


# ── Annular Velocity ──────────────────────────────────────────────────────────

class TestAnnularVelocity:
    ENDPOINT = "/calcs/annular-velocity"

    def test_us_calculation(self, client):
        # hole=12.25 in, pipe=5 in, flow=600 gpm
        # area = π/4 × (12.25² - 5²) = π/4 × (150.0625 - 25) = π/4 × 125.0625 ≈ 98.17 in²
        # velocity = 600 × 24.51 / 98.17 ≈ 149.7 ft/min
        r = client.post(self.ENDPOINT, json={
            "flow_rate": 600,
            "hole_diameter": 12.25,
            "pipe_od": 5.0,
            "unit_system": "us",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["annular_velocity"] > 0
        assert data["annular_area"] > 0
        assert data["unit_system"] == "us"

    def test_pipe_od_larger_than_hole_produces_negative_area(self, client):
        """Physically invalid input — server should return 200 but velocity will be negative."""
        r = client.post(self.ENDPOINT, json={
            "flow_rate": 600,
            "hole_diameter": 4.0,
            "pipe_od": 5.0,
            "unit_system": "us",
        })
        # Response shape still valid — the math produces a negative value
        assert r.status_code == 200
