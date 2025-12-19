"""Wazuh OPSEC detection rules configuration for red team scenarios.

This module provides Wazuh custom rules for detecting red team attack patterns
and OPSEC violations in intermediate and advanced scenarios.
"""

from typing import Any
from .ad_config import get_opsec_detection_rules


def get_wazuh_opsec_rules_config() -> dict[str, Any]:
    """Get Wazuh custom rules configuration for OPSEC detection.
    
    Returns a configuration that can be applied to Wazuh server via Ansible.
    """
    opsec_rules = get_opsec_detection_rules()
    
    # Format rules for Wazuh XML format
    wazuh_rules = []
    for rule in opsec_rules:
        wazuh_rule = rule["wazuh_rule"]
        wazuh_rules.append({
            "id": rule["rule_id"],
            "level": wazuh_rule["level"],
            "rule": wazuh_rule["rule"],
            "name": rule["name"],
            "description": rule["description"],
            "attack_technique": rule.get("attack_technique", ""),
            "severity": rule.get("severity", "medium"),
            "opsec_violation": rule.get("opsec_violation", False),
        })
    
    return {
        "custom_rules": wazuh_rules,
        "rules_file": "/var/ossec/etc/rules/local_rules.xml",
        "decoders_file": "/var/ossec/etc/decoders/local_decoder.xml",
    }


def get_wazuh_opsec_dashboard_config() -> dict[str, Any]:
    """Get Wazuh dashboard configuration for OPSEC monitoring.
    
    Returns dashboard widgets and visualizations for OPSEC detection.
    """
    return {
        "dashboards": [
            {
                "name": "Red Team OPSEC Detection",
                "description": "Dashboard for monitoring red team attack patterns and OPSEC violations",
                "widgets": [
                    {
                        "type": "metric",
                        "title": "OPSEC Violations",
                        "query": "rule.id:redteam_011 OR rule.id:redteam_012 OR rule.id:redteam_013",
                        "time_range": "24h",
                    },
                    {
                        "type": "table",
                        "title": "Recent Attack Detections",
                        "query": "rule.id:redteam_*",
                        "columns": ["timestamp", "rule.name", "rule.level", "agent.name"],
                        "sort": "timestamp:desc",
                        "limit": 50,
                    },
                    {
                        "type": "pie",
                        "title": "Attack Techniques Distribution",
                        "query": "rule.id:redteam_*",
                        "group_by": "rule.attack_technique",
                    },
                    {
                        "type": "line",
                        "title": "Detection Timeline",
                        "query": "rule.id:redteam_*",
                        "time_range": "24h",
                        "interval": "1h",
                    },
                ],
            },
            {
                "name": "AD Attack Detection",
                "description": "Dashboard for Active Directory attack detection",
                "widgets": [
                    {
                        "type": "metric",
                        "title": "Kerberoasting Attempts",
                        "query": "rule.id:redteam_001",
                        "time_range": "24h",
                    },
                    {
                        "type": "metric",
                        "title": "DCSync Attempts",
                        "query": "rule.id:redteam_003",
                        "time_range": "24h",
                    },
                    {
                        "type": "table",
                        "title": "AD Attack Events",
                        "query": "rule.id:redteam_001 OR rule.id:redteam_002 OR rule.id:redteam_003 OR rule.id:redteam_004",
                        "columns": ["timestamp", "rule.name", "agent.name", "data.win.eventdata.targetUserName"],
                        "sort": "timestamp:desc",
                        "limit": 100,
                    },
                ],
            },
        ],
    }


def get_wazuh_opsec_ansible_vars() -> dict[str, Any]:
    """Get Ansible variables for configuring Wazuh with OPSEC detection rules.
    
    These variables can be used with an Ansible role to configure Wazuh.
    """
    opsec_config = get_wazuh_opsec_rules_config()
    dashboard_config = get_wazuh_opsec_dashboard_config()
    
    return {
        "wazuh_custom_rules": opsec_config["custom_rules"],
        "wazuh_custom_rules_file": opsec_config["rules_file"],
        "wazuh_opsec_dashboards": dashboard_config["dashboards"],
        "wazuh_opsec_enabled": True,
    }

