import math
from fastapi import APIRouter
from api.models.calc_models import (
    HydrostaticPressureRequest, HydrostaticPressureResponse,
    EMWRequest, EMWResponse,
    KillSheetRequest, KillSheetResponse,
    AnnularVelocityRequest, AnnularVelocityResponse,
)

# Drilling unit conversion constants
US_PRESSURE_GRADIENT = 0.052    # psi per (ppg × ft)
METRIC_GRAVITY = 9.80665        # m/s² — exact SI value
US_AV_FACTOR = 24.51            # gpm·in⁻² → ft/min
METRIC_AV_FACTOR = 1_000_000    # L/min·mm⁻² → m/min scaling

router = APIRouter()


@router.post("/hydrostatic-pressure", response_model=HydrostaticPressureResponse)
async def hydrostatic_pressure(req: HydrostaticPressureRequest) -> HydrostaticPressureResponse:
    """Calculate hydrostatic pressure from mud weight and depth."""
    if req.unit_system == "us":
        # psi = mud_weight (ppg) × 0.052 × depth (ft)
        pressure = req.mud_weight * US_PRESSURE_GRADIENT * req.depth
    else:
        # kPa = mud_weight (kg/m³) × 9.80665 × depth (m) / 1000
        pressure = req.mud_weight * METRIC_GRAVITY * req.depth / 1000

    return HydrostaticPressureResponse(pressure=round(pressure, 2), unit_system=req.unit_system)


@router.post("/equivalent-mud-weight", response_model=EMWResponse)
async def equivalent_mud_weight(req: EMWRequest) -> EMWResponse:
    """Calculate equivalent mud weight from pressure and depth."""
    if req.unit_system == "us":
        # ppg = pressure (psi) / (0.052 × depth (ft))
        emw = req.pressure / (US_PRESSURE_GRADIENT * req.depth)
    else:
        # kg/m³ = pressure (kPa) × 1000 / (9.80665 × depth (m))
        emw = req.pressure * 1000 / (METRIC_GRAVITY * req.depth)

    return EMWResponse(emw=round(emw, 3), unit_system=req.unit_system)


@router.post("/kill-sheet", response_model=KillSheetResponse)
async def kill_sheet(req: KillSheetRequest) -> KillSheetResponse:
    """Calculate kill mud weight from SIDPP."""
    if req.unit_system == "us":
        # Kill MW (ppg) = current MW + SIDPP / (0.052 × depth)
        pressure_margin = req.shut_in_drillpipe_pressure / (US_PRESSURE_GRADIENT * req.depth)
    else:
        # Kill MW (kg/m³) = current MW + SIDPP×1000 / (9.80665 × depth)
        pressure_margin = req.shut_in_drillpipe_pressure * 1000 / (METRIC_GRAVITY * req.depth)

    kill_mw = req.current_mud_weight + pressure_margin
    kill_mw_rounded = math.ceil(kill_mw * 10) / 10

    return KillSheetResponse(
        kill_mud_weight=round(kill_mw, 3),
        kill_mud_weight_rounded=kill_mw_rounded,
        pressure_safety_margin=round(pressure_margin, 3),
        unit_system=req.unit_system,
    )


@router.post("/annular-velocity", response_model=AnnularVelocityResponse)
async def annular_velocity(req: AnnularVelocityRequest) -> AnnularVelocityResponse:
    """Calculate annular velocity from flow rate and annular geometry."""
    # Annular area is unit-agnostic (same formula for in² or mm²)
    area = math.pi / 4 * (req.hole_diameter**2 - req.pipe_od**2)

    if req.unit_system == "us":
        # ft/min = (gpm × 24.51) / annular_area (in²)
        velocity = (req.flow_rate * US_AV_FACTOR) / area
    else:
        # m/min = (L/min × 1_000_000) / area (mm²)
        velocity = (req.flow_rate * METRIC_AV_FACTOR) / area

    return AnnularVelocityResponse(
        annular_velocity=round(velocity, 2),
        annular_area=round(area, 4),
        unit_system=req.unit_system,
    )
