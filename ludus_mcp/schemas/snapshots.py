"""Snapshot-related schemas."""

from pydantic import BaseModel, Field


class SnapshotCreate(BaseModel):
    """Request schema for creating a snapshot."""

    name: str = Field(..., description="Snapshot name")
    host_id: str = Field(..., description="ID of the host to snapshot")
    description: str | None = Field(None, description="Optional description")


class Snapshot(BaseModel):
    """Snapshot response schema."""

    id: str | None = Field(None, description="Snapshot ID")
    name: str = Field(..., description="Snapshot name")
    host_id: str | None = Field(None, description="Host ID")
    description: str | None = Field(None, description="Snapshot description")
    created_at: str | None = Field(None, description="Creation timestamp")
    size: int | None = Field(None, description="Snapshot size in bytes")

