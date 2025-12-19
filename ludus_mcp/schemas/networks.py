"""Network-related schemas."""

from pydantic import BaseModel, Field


class NetworkCreate(BaseModel):
    """Request schema for creating a network."""

    name: str = Field(..., description="Network name")
    range_id: str = Field(..., description="ID of the parent range")
    cidr: str | None = Field(None, description="CIDR block for the network")
    description: str | None = Field(None, description="Optional description")


class Network(BaseModel):
    """Network response schema."""

    id: str | None = Field(None, description="Network ID")
    name: str = Field(..., description="Network name")
    range_id: str | None = Field(None, description="Parent range ID")
    cidr: str | None = Field(None, description="CIDR block")
    description: str | None = Field(None, description="Network description")
    status: str | None = Field(None, description="Network status")

