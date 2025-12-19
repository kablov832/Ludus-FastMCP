"""Validation schemas for Ludus ranges."""

from pydantic import BaseModel, Field


class ValidationError(BaseModel):
    """Validation error details."""

    field: str = Field(..., description="Field that failed validation")
    message: str = Field(..., description="Error message")
    severity: str = Field(default="error", description="Severity: error or warning")


class ValidationResult(BaseModel):
    """Result of configuration validation."""

    valid: bool = Field(..., description="Whether configuration is valid")
    errors: list[ValidationError] = Field(default_factory=list, description="Validation errors")
    warnings: list[ValidationError] = Field(default_factory=list, description="Validation warnings")
    recommendations: list[str] = Field(default_factory=list, description="Recommendations for improvement")

    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0


class PreviewResult(BaseModel):
    """Result of scenario preview."""

    scenario_key: str = Field(..., description="Scenario identifier")
    siem_type: str = Field(default="wazuh", description="SIEM type")
    config: dict = Field(..., description="Full configuration")
    visualization: str = Field(..., description="ASCII topology visualization")
    vm_count: int = Field(..., description="Number of VMs")
    estimated_time: str = Field(..., description="Estimated deployment time")
    estimated_memory_gb: int = Field(..., description="Estimated memory in GB")
    estimated_disk_gb: int = Field(..., description="Estimated disk space in GB")
    deploy_command: str = Field(..., description="Command to deploy this scenario")
