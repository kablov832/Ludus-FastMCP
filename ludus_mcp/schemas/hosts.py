"""Host-related schemas."""

from pydantic import BaseModel, Field


class HostCreate(BaseModel):
    """Request schema for creating a host."""

    name: str = Field(..., description="Host name")
    range_id: str = Field(..., description="ID of the parent range")
    network_id: str | None = Field(None, description="ID of the network to attach to")
    template: str | None = Field(None, description="Template to use for the host")
    cpu: int | None = Field(None, description="Number of CPUs")
    memory: int | None = Field(None, description="Memory in MB")
    disk: int | None = Field(None, description="Disk size in GB")
    description: str | None = Field(None, description="Optional description")


class HostStatus(BaseModel):
    """Host status information."""

    status: str = Field(..., description="Host status (running, stopped, etc.)")
    ip_address: str | None = Field(None, description="IP address of the host")
    power_state: str | None = Field(None, description="Power state")


class Host(BaseModel):
    """Host response schema."""

    id: str | None = Field(None, description="Host ID")
    name: str = Field(..., description="Host name")
    range_id: str | None = Field(None, description="Parent range ID")
    network_id: str | None = Field(None, description="Attached network ID")
    template: str | None = Field(None, description="Template used")
    status: str | None = Field(None, description="Host status")
    ip_address: str | None = Field(None, description="IP address")
    cpu: int | None = Field(None, description="Number of CPUs")
    memory: int | None = Field(None, description="Memory in MB")
    disk: int | None = Field(None, description="Disk size in GB")
    description: str | None = Field(None, description="Host description")

