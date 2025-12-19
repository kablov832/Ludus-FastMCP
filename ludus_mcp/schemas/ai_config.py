"""Schemas for AI-powered configuration generation."""

from typing import Any
from pydantic import BaseModel, Field
from enum import Enum


class ScenarioType(str, Enum):
    """Type of security scenario."""
    CUSTOM = "custom"
    RED_TEAM = "red_team"
    BLUE_TEAM = "blue_team"
    PURPLE_TEAM = "purple_team"
    PENTEST = "pentest"
    SOC = "soc"
    MALWARE_ANALYSIS = "malware_analysis"
    FORENSICS = "forensics"


class ComplexityLevel(str, Enum):
    """Complexity level of the range."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ResourceProfile(str, Enum):
    """Resource allocation profile."""
    MINIMAL = "minimal"
    RECOMMENDED = "recommended"
    MAXIMUM = "maximum"


class SIEMType(str, Enum):
    """Supported SIEM types."""
    WAZUH = "wazuh"
    SPLUNK = "splunk"
    ELASTIC = "elastic"
    SECURITY_ONION = "security-onion"
    NONE = "none"


class ClarificationQuestion(BaseModel):
    """A clarification question to ask the user."""
    question: str = Field(..., description="The question to ask")
    field: str = Field(..., description="The configuration field this clarifies")
    question_type: str = Field(default="text", description="Type of input: text, number, choice")
    options: list[str] | None = Field(default=None, description="Options for choice questions")
    default: Any | None = Field(default=None, description="Default value if not answered")


class ParsedRequirements(BaseModel):
    """Structured requirements parsed from natural language."""
    needs_domain_controller: bool = False
    domain_name: str = "corp.local"
    dc_hostname: str | None = None
    workstation_count: int = 0
    server_types: list[str] = Field(default_factory=list)
    needs_attacker: bool = False
    include_monitoring: bool = True
    siem_type: SIEMType = SIEMType.WAZUH
    scenario_type: ScenarioType = ScenarioType.CUSTOM
    tags: list[str] = Field(default_factory=list)


class ConfigMetadata(BaseModel):
    """Metadata about generated configuration."""
    vm_count: int
    network_rules_count: int
    siem_type: str
    resource_profile: str
    complexity: str
    scenario_type: str | None = None
    estimated_resource_usage: dict[str, Any] | None = None


class Suggestion(BaseModel):
    """A suggestion for improving or enhancing the configuration."""
    suggestion_type: str = Field(..., description="Type: enhancement, scaling, security, learning")
    title: str = Field(..., description="Short title of the suggestion")
    description: str = Field(..., description="Detailed description")
    benefit: str = Field(..., description="What benefit this provides")
    implementation_complexity: str = Field(default="medium", description="low, medium, high")
    resource_impact: str | None = Field(default=None, description="Impact on resources")


class ConfigGenerationResult(BaseModel):
    """Result of AI config generation."""
    status: str = Field(..., description="success or needs_clarification")
    prompt: str = Field(..., description="Original user prompt")
    configuration: dict[str, Any] | None = Field(default=None, description="Generated Ludus config")
    metadata: ConfigMetadata | None = Field(default=None, description="Config metadata")
    parsed_requirements: ParsedRequirements | None = Field(default=None)
    clarifications: list[ClarificationQuestion] | None = Field(default=None)
    suggestions: list[Suggestion] | None = Field(default=None)
    educational_notes: list[str] | None = Field(default=None)
    next_steps: list[str] | None = Field(default=None)
    partial_understanding: dict[str, Any] | None = Field(default=None, description="Partial parse if clarification needed")
    message: str | None = Field(default=None, description="Message to user")


class ConfigValidationResult(BaseModel):
    """Result of validating a generated configuration."""
    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    schema_compliance: bool = True
    ludus_api_compatible: bool = True


class EnhancementResult(BaseModel):
    """Result of suggesting enhancements to a configuration."""
    status: str
    original_description: str
    enhancement_focus: str
    current_config_summary: dict[str, Any]
    suggested_additions: list[Suggestion]
    focus_specific_enhancements: list[str]
    implementation_notes: list[str]
    next_steps: list[str]
