from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator, model_validator


UsernameStr = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=50,
        pattern=r"^[a-z0-9_.-]+$",
        strip_whitespace=True,
    ),
]

ApiNumberStr = Annotated[
    str,
        StringConstraints(
            pattern=r"^\d{10}(\d{4})?$",
            strip_whitespace=True,
        ),
    ]

NameStr = Annotated[str, StringConstraints(min_length=1, max_length=100, strip_whitespace=True)]
ProjectNameStr = Annotated[str, StringConstraints(min_length=1, max_length=150, strip_whitespace=True)]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DrillingBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )


class UserRole(str, Enum):
    admin = "admin"
    engineer = "engineer"
    supervisor = "supervisor"
    geologist = "geologist"
    viewer = "viewer"


class ProjectStatus(str, Enum):
    planned = "planned"
    active = "active"
    on_hold = "on_hold"
    completed = "completed"
    archived = "archived"


class WellStatus(str, Enum):
    planned = "planned"
    drilling = "drilling"
    completed = "completed"
    suspended = "suspended"
    plugged_and_abandoned = "plugged_and_abandoned"


class WellType(str, Enum):
    oil = "oil"
    gas = "gas"
    injection = "injection"
    disposal = "disposal"
    exploration = "exploration"
    water_source = "water_source"


class User(DrillingBaseModel):
    user_id: UUID = Field(default_factory=uuid4, description="System-generated unique identifier for the user.")
    username: UsernameStr = Field(..., description="Unique application username; lowercase letters, numbers, dot, underscore, and hyphen only.")
    full_name: NameStr = Field(..., description="User's full display name.")
    email: EmailStr = Field(..., description="User's email address.")
    role: UserRole = Field(..., description="Application role used for authorization.")
    is_active: bool = Field(default=True, description="Indicates whether the user account is active.")
    created_at: datetime = Field(default_factory=utc_now, description="UTC timestamp when the user record was created.")
    updated_at: datetime = Field(default_factory=utc_now, description="UTC timestamp when the user record was last updated.")

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().lower()
        return value


class SurfaceLocation(DrillingBaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Surface latitude in decimal degrees.")
    longitude: float = Field(..., ge=-180, le=180, description="Surface longitude in decimal degrees.")
    county: Optional[str] = Field(default=None, max_length=100, description="County or local administrative area for the well surface location.")
    state: Optional[str] = Field(default=None, max_length=100, description="State or province for the well surface location.")
    country: Optional[str] = Field(default=None, max_length=100, description="Country for the well surface location.")


class Well(DrillingBaseModel):
    well_id: UUID = Field(default_factory=uuid4, description="System-generated unique identifier for the well record.")
    well_name: NameStr = Field(..., description="Common well name used in drilling and reporting systems.")
    api_number: Optional[ApiNumberStr] = Field(
        default=None,
        description="API well number as 10 or 14 digits with no separators.",
    )
    well_type: WellType = Field(..., description="Operational well type classification.")
    status: WellStatus = Field(default=WellStatus.planned, description="Current lifecycle status of the well.")
    operator_name: Optional[str] = Field(default=None, max_length=150, description="Operator responsible for the well.")
    field_name: Optional[str] = Field(default=None, max_length=150, description="Field or asset area where the well is located.")
    formation_name: Optional[str] = Field(default=None, max_length=150, description="Primary target formation name.")
    surface_location: Optional[SurfaceLocation] = Field(default=None, description="Surface location of the wellhead in decimal degrees.")
    kb_elevation_ft: Optional[float] = Field(
        default=None,
        gt=0,
        description="Kelly bushing elevation in feet above mean sea level (ft).",
    )
    planned_td_ft_md: Optional[float] = Field(
        default=None,
        gt=0,
        description="Planned total depth measured depth in feet (ft MD).",
    )
    current_md_ft: Optional[float] = Field(
        default=None,
        ge=0,
        description="Current measured depth in feet (ft MD).",
    )
    created_at: datetime = Field(default_factory=utc_now, description="UTC timestamp when the well record was created.")
    updated_at: datetime = Field(default_factory=utc_now, description="UTC timestamp when the well record was last updated.")

    @field_validator("api_number", mode="before")
    @classmethod
    def normalize_api_number(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if isinstance(value, str):
            digits_only = "".join(ch for ch in value if ch.isdigit())
            return digits_only or None
        return value

    @model_validator(mode="after")
    def validate_depths(self) -> "Well":
        if self.current_md_ft is not None and self.planned_td_ft_md is not None:
            if self.current_md_ft > self.planned_td_ft_md:
                raise ValueError("current_md_ft cannot exceed planned_td_ft_md.")
        return self


class ProjectWrapper(DrillingBaseModel):
    project_id: UUID = Field(default_factory=uuid4, description="System-generated unique identifier for the project.")
    project_name: ProjectNameStr = Field(..., description="Project name for the drilling program or asset grouping.")
    description: Optional[str] = Field(default=None, max_length=1000, description="Optional description of the project scope.")
    status: ProjectStatus = Field(default=ProjectStatus.planned, description="Current project lifecycle status.")
    owner: User = Field(..., description="Primary owner of the project.")
    wells: list[Well] = Field(
        ...,
        min_length=1,
        description="One-to-many collection of wells associated with the project.",
    )
    created_at: datetime = Field(default_factory=utc_now, description="UTC timestamp when the project record was created.")
    updated_at: datetime = Field(default_factory=utc_now, description="UTC timestamp when the project record was last updated.")

    @model_validator(mode="after")
    def validate_unique_wells(self) -> "ProjectWrapper":
        seen_well_ids: set[UUID] = set()
        seen_api_numbers: set[str] = set()

        for well in self.wells:
            if well.well_id in seen_well_ids:
                raise ValueError(f"Duplicate well_id detected in wells: {well.well_id}")
            seen_well_ids.add(well.well_id)

            if well.api_number:
                if well.api_number in seen_api_numbers:
                    raise ValueError(f"Duplicate api_number detected in wells: {well.api_number}")
                seen_api_numbers.add(well.api_number)

        return self
    


    # -----------------------------------------------------
    # Main 
    # -----------------------------------------------------
    

def main() -> None:
    owner = User(
        username="tyler.hunt",
        full_name="Tyler Hunt",
        email="tyler.hunt@example.com",
        role=UserRole.supervisor,
    )

    well_1 = Well(
        well_name="University 12H",
        api_number="42-329-45789",
        well_type=WellType.oil,
        status=WellStatus.drilling,
        operator_name="Permian Energy Operating",
        field_name="Midland Basin",
        formation_name="Wolfcamp A",
        surface_location=SurfaceLocation(
            latitude=31.9973,
            longitude=-102.0779,
            county="Midland",
            state="Texas",
            country="USA",
        ),
        kb_elevation_ft=2865.5,
        planned_td_ft_md=18500.0,
        current_md_ft=12450.0,
    )

    well_2 = Well(
        well_name="University 13H",
        api_number="42329457900000",
        well_type=WellType.oil,
        status=WellStatus.planned,
        operator_name="Permian Energy Operating",
        field_name="Midland Basin",
        formation_name="Wolfcamp A",
        surface_location=SurfaceLocation(
            latitude=31.9987,
            longitude=-102.0812,
            county="Midland",
            state="Texas",
            country="USA",
        ),
        kb_elevation_ft=2868.0,
        planned_td_ft_md=18750.0,
        current_md_ft=0.0,
    )

    project = ProjectWrapper(
        project_name="Midland Development Pad A",
        description="Multi-well horizontal drilling project for Wolfcamp development.",
        status=ProjectStatus.active,
        owner=owner,
        wells=[well_1, well_2],
    )

    print("USER INSTANCE:")
    print(owner.model_dump_json(indent=2))
    print("\nPROJECT INSTANCE:")
    print(project.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
