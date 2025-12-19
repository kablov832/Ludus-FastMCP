"""Live action attack simulations for blue team training.

This module provides realistic attack simulations that can be run automatically
in blue team scenarios to generate security events for detection training.
"""

from typing import Any
from .ad_config import get_ad_attack_paths, get_forest_pivot_attack_paths


def get_live_action_config(
    attack_paths: dict[str, Any] | None = None,
    forest_pivot_paths: dict[str, Any] | None = None,
    simulation_enabled: bool = True,
    simulation_interval: int = 1800,
    randomize_timing: bool = True,
    simulation_intensity: str = "medium",
) -> dict[str, Any]:
    """Get configuration for live action attack simulations.
    
    Args:
        attack_paths: Dictionary of attack paths to simulate
        forest_pivot_paths: Dictionary of forest pivot attack paths
        simulation_enabled: Whether to enable attack simulations
        simulation_interval: Interval between simulations (seconds)
        randomize_timing: Whether to randomize timing between attacks
        simulation_intensity: Intensity level (low, medium, high)
    
    Returns:
        Configuration dictionary for Ansible role
    """
    if attack_paths is None:
        attack_paths = get_ad_attack_paths()
    
    if forest_pivot_paths is None:
        forest_pivot_paths = get_forest_pivot_attack_paths()
    
    # Select attack paths based on intensity
    if simulation_intensity == "low":
        # Only basic attacks
        selected_paths = {
            k: v for k, v in attack_paths.items() 
            if k in ["path_1_kerberoasting", "path_3_pass_the_hash"]
        }
    elif simulation_intensity == "medium":
        # Most attacks except most advanced
        selected_paths = {
            k: v for k, v in attack_paths.items()
            if k != "path_4_dcsync"
        }
        # Add one forest pivot path
        selected_paths.update({
            k: v for k, v in list(forest_pivot_paths.items())[:1]
        })
    else:  # high
        # All attack paths
        selected_paths = {**attack_paths, **forest_pivot_paths}
    
    return {
        "simulation_enabled": simulation_enabled,
        "simulation_interval": simulation_interval,
        "randomize_timing": randomize_timing,
        "simulation_intensity": simulation_intensity,
        "attack_paths": selected_paths,
        "simulation_actions": [
            {
                "action": "kerberoasting",
                "description": "Simulate Kerberoasting attack",
                "frequency": "daily" if simulation_intensity == "low" else "twice_daily",
                "tools": ["Invoke-Kerberoast", "Rubeus"],
                "detection_rule": "redteam_001",
            },
            {
                "action": "ldap_enumeration",
                "description": "Simulate LDAP enumeration",
                "frequency": "hourly" if simulation_intensity == "high" else "daily",
                "tools": ["PowerView", "BloodHound"],
                "detection_rule": "redteam_011",
            },
            {
                "action": "lateral_movement_rdp",
                "description": "Simulate RDP lateral movement",
                "frequency": "daily",
                "tools": ["mstsc", "xfreerdp"],
                "detection_rule": "redteam_005",
            },
            {
                "action": "credential_dumping",
                "description": "Simulate credential dumping",
                "frequency": "twice_daily" if simulation_intensity == "high" else "daily",
                "tools": ["Mimikatz", "ProcDump"],
                "detection_rule": "redteam_012",
            },
            {
                "action": "pass_the_hash",
                "description": "Simulate Pass-the-Hash attack",
                "frequency": "daily",
                "tools": ["Mimikatz", "psexec"],
                "detection_rule": "redteam_004",
            },
            {
                "action": "ad_cs_certificate_abuse",
                "description": "Simulate AD CS certificate abuse",
                "frequency": "daily" if simulation_intensity in ["medium", "high"] else None,
                "tools": ["Certify", "Rubeus"],
                "detection_rule": "redteam_007",
            },
            {
                "action": "forest_trust_enumeration",
                "description": "Simulate forest trust enumeration",
                "frequency": "daily" if simulation_intensity == "high" else None,
                "tools": ["Get-DomainTrust", "PowerView"],
                "detection_rule": "redteam_009",
            },
            {
                "action": "cross_forest_kerberoasting",
                "description": "Simulate cross-forest Kerberoasting",
                "frequency": "daily" if simulation_intensity == "high" else None,
                "tools": ["Invoke-Kerberoast", "Rubeus"],
                "detection_rule": "redteam_001",
            },
        ],
    }


def get_live_action_schedule(intensity: str = "medium") -> dict[str, Any]:
    """Get schedule for live action simulations.
    
    Args:
        intensity: Simulation intensity (low, medium, high)
    
    Returns:
        Schedule configuration
    """
    if intensity == "low":
        return {
            "schedule": [
                {"time": "09:00", "action": "ldap_enumeration"},
                {"time": "14:00", "action": "kerberoasting"},
                {"time": "16:00", "action": "lateral_movement_rdp"},
            ],
            "randomize": True,
            "variance_minutes": 30,
        }
    elif intensity == "medium":
        return {
            "schedule": [
                {"time": "08:00", "action": "ldap_enumeration"},
                {"time": "10:00", "action": "kerberoasting"},
                {"time": "12:00", "action": "credential_dumping"},
                {"time": "14:00", "action": "pass_the_hash"},
                {"time": "16:00", "action": "lateral_movement_rdp"},
                {"time": "18:00", "action": "ad_cs_certificate_abuse"},
            ],
            "randomize": True,
            "variance_minutes": 45,
        }
    else:  # high
        return {
            "schedule": [
                {"time": "08:00", "action": "ldap_enumeration"},
                {"time": "09:00", "action": "kerberoasting"},
                {"time": "10:00", "action": "credential_dumping"},
                {"time": "11:00", "action": "pass_the_hash"},
                {"time": "12:00", "action": "lateral_movement_rdp"},
                {"time": "13:00", "action": "ad_cs_certificate_abuse"},
                {"time": "14:00", "action": "forest_trust_enumeration"},
                {"time": "15:00", "action": "cross_forest_kerberoasting"},
                {"time": "16:00", "action": "credential_dumping"},
                {"time": "17:00", "action": "lateral_movement_rdp"},
            ],
            "randomize": True,
            "variance_minutes": 30,
        }

