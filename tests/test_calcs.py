"""
Unit tests for src/calcs/wellbore.py — pure Python math, no framework required.

Produced by: backend-agent / calcs layer
"""
import math
import numpy as np
import pandas as pd
import pytest

from calcs.wellbore import (
    calc_capacity,
    calc_segment_capacity,
    calc_displacement,
    calc_segment_displacement,
    calc_volume,
    calc_segment_volume,
)


def _series(*values):
    return pd.Series(list(values), dtype=float)


class TestCalcCapacity:
    def test_basic(self):
        depth = _series(100.0)
        diam = _series(10.0)
        result = calc_capacity(depth, diam)
        expected = math.pi * 5.0**2 * 100.0
        assert abs(result.iloc[0] - expected) < 1e-6

    def test_multiple_rows(self):
        depth = _series(100.0, 200.0)
        diam = _series(10.0, 10.0)
        result = calc_capacity(depth, diam)
        assert len(result) == 2
        assert result.iloc[1] == pytest.approx(result.iloc[0] * 2, rel=1e-6)

    def test_zero_diameter_returns_zero(self):
        result = calc_capacity(_series(100.0), _series(0.0))
        assert result.iloc[0] == pytest.approx(0.0)


class TestCalcSegmentCapacity:
    def test_basic(self):
        result = calc_segment_capacity(_series(0.0), _series(100.0), _series(10.0))
        expected = math.pi * 5.0**2 * 100.0
        assert abs(result.iloc[0] - expected) < 1e-6

    def test_same_depth_returns_zero(self):
        result = calc_segment_capacity(_series(100.0), _series(100.0), _series(10.0))
        assert result.iloc[0] == pytest.approx(0.0)


class TestCalcDisplacement:
    def test_equals_capacity_same_inputs(self):
        """Displacement uses the same formula as capacity."""
        depth = _series(50.0)
        diam = _series(8.0)
        assert calc_displacement(depth, diam).iloc[0] == pytest.approx(
            calc_capacity(depth, diam).iloc[0]
        )


class TestCalcVolume:
    def test_equals_capacity_same_inputs(self):
        depth = _series(200.0)
        diam = _series(12.0)
        assert calc_volume(depth, diam).iloc[0] == pytest.approx(
            calc_capacity(depth, diam).iloc[0]
        )


class TestCalcSegmentVolume:
    def test_basic(self):
        result = calc_segment_volume(_series(500.0), _series(600.0), _series(6.0))
        expected = math.pi * 3.0**2 * 100.0
        assert abs(result.iloc[0] - expected) < 1e-6

    def test_nan_on_invalid_input(self):
        """Non-numeric hole diameter should produce NaN."""
        result = calc_segment_volume(
            pd.Series([0.0]), pd.Series([100.0]), pd.Series([float("nan")])
        )
        assert np.isnan(result.iloc[0])
