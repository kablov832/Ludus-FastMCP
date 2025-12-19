"""Range-related schemas."""

from typing import Any

from pydantic import BaseModel, Field


class RangeDefinition(BaseModel):
    """Complete range definition for LLM-generated ranges."""

    name: str = Field(..., description="Name of the range")
    description: str | None = Field(None, description="Description of the range")
    networks: list[dict[str, Any]] = Field(default_factory=list, description="Network definitions")
    hosts: list[dict[str, Any]] = Field(default_factory=list, description="Host definitions")
    links: list[dict[str, Any]] = Field(default_factory=list, description="Network links")


class RangeCreate(BaseModel):
    """Request schema for creating a range."""

    name: str = Field(..., description="Name of the range")
    description: str | None = Field(None, description="Optional description")


class Range(BaseModel):
    """Range response schema."""

    id: str | None = Field(None, description="Range ID")
    name: str = Field(..., description="Range name")
    description: str | None = Field(None, description="Range description")
    status: str | None = Field(None, description="Range status")
    created_at: str | None = Field(None, description="Creation timestamp")
    updated_at: str | None = Field(None, description="Last update timestamp")

