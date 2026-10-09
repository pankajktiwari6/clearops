from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TeamCreate(BaseModel):
    """Payload for creating a gold.ClearOps_Teams row (identity key and audit columns are generated)."""

    team_name: str
    team_mission: str | None = None
    team_lead: str | None = None
    team_members: str | None = None
    resource_id: int | None = None
    teammanager: str | None = None
    date_time: datetime | None = None


class TeamUpdate(BaseModel):
    """Partial update of a gold.ClearOps_Teams row -- every field optional."""

    team_name: str | None = None
    team_mission: str | None = None
    team_lead: str | None = None
    team_members: str | None = None
    resource_id: int | None = None
    teammanager: str | None = None
    date_time: datetime | None = None


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    team_id: int = Field(validation_alias="TeamId")
    team_name: str = Field(validation_alias="TeamName")
    team_mission: str | None = Field(default=None, validation_alias="TeamMission")
    team_lead: str | None = Field(default=None, validation_alias="TeamLead")
    team_members: str | None = Field(default=None, validation_alias="TeamMembers")
    resource_id: int | None = Field(default=None, validation_alias="ResourceId")
    teammanager: str | None = Field(default=None, validation_alias="Teammanager")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the Team grid may sort by (server-side).
TeamSortField = Literal[
    "team_id",
    "team_name",
    "team_mission",
    "team_lead",
    "team_members",
    "resource_id",
    "teammanager",
    "date_time",
]
