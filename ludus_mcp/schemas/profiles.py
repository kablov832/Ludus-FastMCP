"""Schemas for Adversary/Defender profile transformations."""

from typing import Any
from pydantic import BaseModel, Field
from enum import Enum


class ThreatLevel(str, Enum):
    """Adversary profile threat levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"  # APT-level threats with advanced persistence


class APTProfile(str, Enum):
    """APT-style adversary profiles modeled after real threat actors."""
    APT28 = "apt28"  # Fancy Bear - credential theft, lateral movement
    APT29 = "apt29"  # Cozy Bear - stealthy persistence, cloud exploitation
    APT41 = "apt41"  # Dual espionage/financial, supply chain
    FIN7 = "fin7"    # Financial cybercrime, POS malware
    LAZARUS = "lazarus"  # Destructive attacks, cryptocurrency theft
    CARBANAK = "carbanak"  # Banking trojans, ATM attacks
    WIZARD_SPIDER = "wizard_spider"  # Ransomware operations


class AttackChainFocus(str, Enum):
    """Focus areas for attack chain profiles."""
    INITIAL_ACCESS = "initial_access"
    PERSISTENCE = "persistence"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    CREDENTIAL_ACCESS = "credential_access"
    LATERAL_MOVEMENT = "lateral_movement"
    EXFILTRATION = "exfiltration"
    COMMAND_AND_CONTROL = "command_and_control"
    IMPACT = "impact"


class RansomwareProfile(str, Enum):
    """Ransomware simulation profiles."""
    RANSOMWARE_LITE = "ransomware_lite"  # Simulation only, no actual encryption
    RANSOMWARE_ADVANCED = "ransomware_advanced"  # Full attack chain simulation


class MonitoringLevel(str, Enum):
    """Defender profile monitoring levels."""
    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    ADVANCED = "advanced"
    ELITE = "elite"  # Advanced threat hunting and automation


class ThreatHuntingProfile(str, Enum):
    """Threat hunting capability profiles."""
    HUNTER_LITE = "hunter_lite"  # Basic hunting queries, scheduled searches
    HUNTER_ADVANCED = "hunter_advanced"  # Behavioral analytics, anomaly detection
    HUNTER_ELITE = "hunter_elite"  # Threat intel integration, automated hunting


class IncidentResponseProfile(str, Enum):
    """Incident response readiness profiles."""
    IR_PREPARATION = "ir_preparation"  # Logging, baseline, IR tools
    IR_DETECTION = "ir_detection"  # Real-time alerting, correlation, playbooks
    IR_CONTAINMENT = "ir_containment"  # Segmentation, automated response, forensics
    IR_ACTIVE_BREACH = "ir_active_breach"  # Full IR setup for active investigation


class SOCMaturityLevel(str, Enum):
    """SOC maturity levels."""
    SOC_LEVEL1 = "soc_level1"  # 8x5 monitoring, signature-based
    SOC_LEVEL2 = "soc_level2"  # 24x7 monitoring, behavioral detection
    SOC_LEVEL3 = "soc_level3"  # Proactive hunting, automation, threat intel


class MalwareAnalysisProfile(str, Enum):
    """Malware analysis and reverse engineering profiles."""
    MALWARE_BASIC = "malware_basic"  # Basic static analysis tools
    MALWARE_INTERMEDIATE = "malware_intermediate"  # Static + dynamic analysis
    MALWARE_ADVANCED = "malware_advanced"  # Full RE suite with debugging
    MALWARE_EXPERT = "malware_expert"  # Complete malware lab with detonation


class SIEMType(str, Enum):
    """Supported SIEM types."""
    WAZUH = "wazuh"
    SPLUNK = "splunk"
    ELASTIC = "elastic"
    SECURITY_ONION = "security-onion"


class VulnerabilityCategory(str, Enum):
    """Categories of vulnerabilities."""
    ACTIVE_DIRECTORY = "Active Directory"
    WINDOWS_SECURITY = "Windows Security"
    NETWORK_SECURITY = "Network Security"
    LINUX_SECURITY = "Linux Security"
    APPLICATION = "Application"


class VulnerabilitySeverity(str, Enum):
    """Severity levels for vulnerabilities."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class VulnerabilityInjection(BaseModel):
    """Details of an injected vulnerability."""
    vm_name: str = Field(..., description="Name of the affected VM")
    vulnerability_type: str = Field(..., description="Type of vulnerability")
    category: str = Field(..., description="Category (AD, Windows, Network, etc.)")
    severity: str = Field(..., description="Severity level")
    ansible_role: str = Field(..., description="Ansible role that implements this")
    description: str = Field(..., description="What this vulnerability is")
    exploitation: str = Field(..., description="How to exploit this vulnerability")
    cve: str | None = Field(default=None, description="Associated CVE if applicable")
    remediation: str | None = Field(default=None, description="How to fix this vulnerability")


class MonitoringEnhancement(BaseModel):
    """Details of a monitoring enhancement."""
    vm_name: str = Field(..., description="Name of the affected VM")
    enhancement_type: str = Field(..., description="Type of enhancement")
    category: str = Field(..., description="Category (Logging, Advanced Logging, etc.)")
    ansible_role: str = Field(..., description="Ansible role that implements this")
    description: str = Field(..., description="What this enhancement provides")
    capabilities: list[str] = Field(..., description="List of capabilities enabled")


class DetectionRule(BaseModel):
    """A detection rule configuration."""
    rule_name: str = Field(..., description="Name of the detection rule")
    category: str = Field(..., description="Attack category this detects")
    description: str = Field(..., description="What this rule detects")
    severity: str = Field(..., description="Severity of alerts from this rule")
    indicators: list[str] = Field(..., description="Indicators of compromise this looks for")


class AdversaryProfileResult(BaseModel):
    """Result of applying an adversary profile."""
    status: str = "success"
    profile_type: str = "adversary"
    threat_level: str
    modified_config: dict[str, Any]
    vulnerability_injections: list[VulnerabilityInjection]
    vulnerabilities_count: int
    affected_vms: list[str]
    documentation: str
    warnings: list[str]
    next_steps: list[str]


class DefenderProfileResult(BaseModel):
    """Result of applying a defender profile."""
    status: str = "success"
    profile_type: str = "defender"
    monitoring_level: str
    siem_type: str
    modified_config: dict[str, Any]
    monitoring_enhancements: list[MonitoringEnhancement]
    enhancements_count: int
    siem_added: bool
    detection_rules: list[DetectionRule]
    affected_vms: list[str]
    documentation: str
    next_steps: list[str]


class ProfilePreview(BaseModel):
    """Preview of profile changes without applying them."""
    status: str = "success"
    profile_type: str
    profile_level: str
    affected_vms: list[str]
    vm_count: int
    changes_summary: list[str]
    ansible_roles_added: list[str]
    estimated_impact: dict[str, Any]
    recommendations: list[str]
