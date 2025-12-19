"""Wazuh configuration utilities for red team scenarios."""

from typing import Any


def get_wazuh_server_config(range_id: str, vlan: int = 10, ip_last_octet: int = 100) -> dict[str, Any]:
    """Get Wazuh server configuration for a scenario.
    
    Uses the correct Ludus-specific role: aleemladha.wazuh_server_install
    See: https://docs.ludus.cloud/docs/roles/
    """
    return {
        "vm_name": f"{range_id}-wazuh-server-ubuntu22",
        "hostname": f"{range_id}-WAZUH",
        "template": "ubuntu-22.04-x64-server-template",
        "vlan": vlan,
        "ip_last_octet": ip_last_octet,
        "ram_gb": 8,
        "cpus": 4,
        "linux": True,
        "ansible_roles": [
            {
                "name": "aleemladha.wazuh_server_install",
                "vars": {
                    # Role-specific variables as needed
                    # See role documentation for available vars
                },
            },
        ],
    }


def add_wazuh_agent_to_vm(vm_config: dict[str, Any], wazuh_server_ip: str) -> dict[str, Any]:
    """Add Wazuh agent configuration to a VM."""
    if "ansible_roles" not in vm_config:
        vm_config["ansible_roles"] = []
    
    # Check if Wazuh agent role already exists
    # Use correct Ludus-specific role: aleemladha.ludus_wazuh_agent
    wazuh_role_exists = any(
        role.get("name") in ["aleemladha.ludus_wazuh_agent", "ludus.wazuh", "wazuh.wazuh"]
        for role in vm_config.get("ansible_roles", [])
    )
    
    if not wazuh_role_exists:
        vm_config["ansible_roles"].append({
            "name": "aleemladha.ludus_wazuh_agent",
            "vars": {
                "wazuh_manager_ip": wazuh_server_ip,
                # See role documentation for additional available vars
            },
        })
    
    return vm_config


def get_wazuh_network_rules() -> list[dict[str, Any]]:
    """Get network rules for Wazuh communication."""
    return [
        {
            "name": "Allow Wazuh agents to manager (TCP 1514)",
            "vlan_src": "all",
            "vlan_dst": "all",
            "protocol": "tcp",
            "ports": 1514,
            "action": "ACCEPT",
        },
        {
            "name": "Allow Wazuh agents to manager (UDP 1514)",
            "vlan_src": "all",
            "vlan_dst": "all",
            "protocol": "udp",
            "ports": 1514,
            "action": "ACCEPT",
        },
        {
            "name": "Allow Wazuh API access (TCP 55000)",
            "vlan_src": "all",
            "vlan_dst": "all",
            "protocol": "tcp",
            "ports": 55000,
            "action": "ACCEPT",
        },
        {
            "name": "Allow Wazuh Dashboard access (TCP 5601)",
            "vlan_src": "all",
            "vlan_dst": "all",
            "protocol": "tcp",
            "ports": 5601,
            "action": "ACCEPT",
        },
    ]

