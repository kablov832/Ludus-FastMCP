"""Orchestration schemas for smart deployment workflows."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class DeploymentStep(BaseModel):
    """A single step in the deployment process."""

    name: str = Field(..., description="Step name")
    status: str = Field(..., description="Status: pending, in_progress, completed, failed")
    started_at: datetime | None = Field(default=None, description="When step started")
    completed_at: datetime | None = Field(default=None, description="When step completed")
    message: str = Field(default="", description="Step message or error")


class SmartDeployResult(BaseModel):
    """Result of smart deployment orchestration."""

    status: str = Field(..., description="Deployment status: started, deploying, success, failed")
    deployment_id: str | None = Field(default=None, description="Deployment identifier")
    scenario_key: str = Field(..., description="Scenario that was deployed")
    siem_type: str = Field(..., description="SIEM type")
    snapshot_id: str | None = Field(default=None, description="Pre-deployment snapshot ID if created")

    # Preview info
    vm_count: int = Field(..., description="Number of VMs")
    estimated_time: str = Field(..., description="Estimated deployment time")

    # Monitoring info
    auto_monitor: bool = Field(default=True, description="Whether auto-monitoring is enabled")
    check_interval: int = Field(default=30, description="Monitoring interval in seconds")
    next_check_message: str = Field(default="", description="Message about next check")

    # Commands for user
    monitoring_commands: dict[str, str] = Field(
        default_factory=dict,
        description="Commands for manual monitoring"
    )

    # Additional context
    message: str = Field(default="", description="Human-readable status message")


class DeploymentTimeline(BaseModel):
    """Timeline of deployment progress."""

    started_at: datetime = Field(..., description="Deployment start time")
    steps: list[DeploymentStep] = Field(default_factory=list, description="Timeline steps")
    current_step: str = Field(default="", description="Current step name")
    progress_percentage: int = Field(default=0, description="Progress percentage (0-100)")
    estimated_completion: datetime | None = Field(default=None, description="Estimated completion time")
    elapsed_minutes: int = Field(default=0, description="Elapsed time in minutes")
    remaining_minutes: int = Field(default=0, description="Estimated remaining time in minutes")


class MonitoringUpdate(BaseModel):
    """Real-time monitoring update."""

    timestamp: datetime = Field(default_factory=datetime.now, description="Update timestamp")
    range_state: str = Field(..., description="Current range state")
    vm_count: int = Field(default=0, description="Total VMs")
    vms_ready: int = Field(default=0, description="VMs ready/running")
    current_task: str = Field(default="", description="Current task being executed")
    progress_percentage: int = Field(default=0, description="Progress percentage")

    # Recent activity
    recent_activity: list[str] = Field(default_factory=list, description="Recent log entries")

    # Status indicators
    is_healthy: bool = Field(default=True, description="Whether deployment is healthy")
    issues: list[str] = Field(default_factory=list, description="Any issues detected")

    # Timing
    elapsed_minutes: int = Field(default=0, description="Time elapsed")
    eta_minutes: int = Field(default=0, description="Estimated time remaining")

    # Next steps
    next_check_in: int = Field(default=30, description="Seconds until next check")
    should_continue_monitoring: bool = Field(default=True, description="Whether to continue monitoring")


class RecoveryRecommendation(BaseModel):
    """Recovery recommendation for failed deployment."""

    action: str = Field(..., description="Recommended action: wait, fix_config, retry, destroy")
    reason: str = Field(..., description="Why this action is recommended")
    severity: str = Field(..., description="Issue severity: info, warning, error, critical")
    steps: list[str] = Field(default_factory=list, description="Step-by-step recovery instructions")
    commands: dict[str, str] = Field(default_factory=dict, description="Useful commands")
    estimated_recovery_time: str = Field(default="", description="Estimated time to recover")
