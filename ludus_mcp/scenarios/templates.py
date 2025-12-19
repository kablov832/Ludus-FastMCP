"""Range templates library for quick customization."""

from typing import Any


class RangeTemplates:
    """Pre-built customizable range templates."""

    @staticmethod
    def list_templates() -> dict[str, str]:
        """
        List all available templates.

        Returns:
            Dictionary of template_key -> description
        """
        return {
            "basic-ad": "Basic AD lab (1 DC, configurable workstations)",
            "multi-dc-ad": "Multi-DC AD lab with replication",
            "ad-with-servers": "AD lab with file/SQL servers",
            "purple-team": "Purple team exercise (targets + attacker + SIEM)",
            "web-app": "Web application lab with database",
            "network-segmentation": "Multi-VLAN network lab",
            "minimal": "Minimal lab (2 VMs for quick testing)",
        }

    @staticmethod
    def get_template(template_key: str, **customizations: Any) -> dict[str, Any]:
        """
        Get template configuration with optional customizations.

        Args:
            template_key: Template identifier
            **customizations: Custom parameters (workstation_count, os_type, etc.)

        Returns:
            Ludus range configuration dictionary
        """
        templates = {
            "basic-ad": RangeTemplates._basic_ad,
            "multi-dc-ad": RangeTemplates._multi_dc_ad,
            "ad-with-servers": RangeTemplates._ad_with_servers,
            "purple-team": RangeTemplates._purple_team,
            "web-app": RangeTemplates._web_app,
            "network-segmentation": RangeTemplates._network_segmentation,
            "minimal": RangeTemplates._minimal,
        }

        if template_key not in templates:
            raise ValueError(f"Unknown template: {template_key}. Available: {', '.join(templates.keys())}")

        return templates[template_key](**customizations)

    @staticmethod
    def _basic_ad(
        workstation_count: int = 2,
        os_type: str = "windows-11",
        include_attacker: bool = True,
        siem_type: str = "wazuh",
        **kwargs: Any
    ) -> dict[str, Any]:
        """Basic AD lab template."""
        config = {
            "ludus": {
                "domain": {"fqdn": "lab.local", "netbios_name": "LAB"},
                "networks": [
                    {"name": "domain", "cidr": "192.168.1.0/24", "description": "Domain network"},
                ],
                "vms": [
                    {
                        "hostname": "dc01",
                        "network": "domain",
                        "template": "windows-server-2022",
                        "ram_mb": 4096,
                        "disk_size_gb": 60,
                        "role": "Domain Controller",
                    },
                ],
            }
        }

        # Add workstations
        for i in range(1, workstation_count + 1):
            config["ludus"]["vms"].append({
                "hostname": f"ws{i:02d}",
                "network": "domain",
                "template": os_type,
                "ram_mb": 4096,
                "disk_size_gb": 60,
                "role": "Domain Workstation",
            })

        # Add SIEM
        if siem_type and siem_type != "none":
            config["ludus"]["vms"].append({
                "hostname": f"{siem_type}-server",
                "network": "domain",
                "template": "ubuntu-22",
                "ram_mb": 4096,
                "disk_size_gb": 80,
                "role": "SIEM Server",
            })

        # Add attacker
        if include_attacker:
            config["ludus"]["networks"].append({
                "name": "attacker",
                "cidr": "192.168.2.0/24",
                "description": "Attacker network",
            })
            config["ludus"]["vms"].append({
                "hostname": "kali-attacker",
                "network": "attacker",
                "template": "kali-linux",
                "ram_mb": 4096,
                "disk_size_gb": 60,
                "role": "Red Team Attacker",
            })

        return config

    @staticmethod
    def _multi_dc_ad(
        dc_count: int = 2,
        workstation_count: int = 3,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Multi-DC AD lab with replication."""
        config = {
            "ludus": {
                "domain": {"fqdn": "lab.local", "netbios_name": "LAB"},
                "networks": [
                    {"name": "domain", "cidr": "192.168.1.0/24", "description": "Domain network"},
                ],
                "vms": [],
            }
        }

        # Add DCs
        for i in range(1, dc_count + 1):
            config["ludus"]["vms"].append({
                "hostname": f"dc{i:02d}",
                "network": "domain",
                "template": "windows-server-2022",
                "ram_mb": 4096,
                "disk_size_gb": 60,
                "role": f"Domain Controller {i}",
            })

        # Add workstations
        for i in range(1, workstation_count + 1):
            config["ludus"]["vms"].append({
                "hostname": f"ws{i:02d}",
                "network": "domain",
                "template": "windows-11",
                "ram_mb": 4096,
                "disk_size_gb": 60,
                "role": "Domain Workstation",
            })

        return config

    @staticmethod
    def _ad_with_servers(
        include_fileserver: bool = True,
        include_sqlserver: bool = True,
        workstation_count: int = 2,
        **kwargs: Any
    ) -> dict[str, Any]:
        """AD lab with file and SQL servers."""
        config = RangeTemplates._basic_ad(workstation_count=workstation_count, include_attacker=True)

        if include_fileserver:
            config["ludus"]["vms"].append({
                "hostname": "file-server",
                "network": "domain",
                "template": "windows-server-2022",
                "ram_mb": 4096,
                "disk_size_gb": 100,
                "role": "File Server",
            })

        if include_sqlserver:
            config["ludus"]["vms"].append({
                "hostname": "sql-server",
                "network": "domain",
                "template": "windows-server-2022",
                "ram_mb": 8192,
                "disk_size_gb": 100,
                "role": "SQL Server",
            })

        return config

    @staticmethod
    def _purple_team(
        target_count: int = 3,
        siem_type: str = "wazuh",
        **kwargs: Any
    ) -> dict[str, Any]:
        """Purple team exercise template."""
        config = {
            "ludus": {
                "networks": [
                    {"name": "targets", "cidr": "192.168.1.0/24", "description": "Target network"},
                    {"name": "attacker", "cidr": "192.168.2.0/24", "description": "Attacker network"},
                ],
                "vms": [],
            }
        }

        # Add targets
        for i in range(1, target_count + 1):
            config["ludus"]["vms"].append({
                "hostname": f"target{i:02d}",
                "network": "targets",
                "template": "windows-11" if i % 2 == 1 else "ubuntu-22",
                "ram_mb": 4096,
                "disk_size_gb": 60,
                "role": f"Target System {i}",
            })

        # Add SIEM
        config["ludus"]["vms"].append({
            "hostname": f"{siem_type}-server",
            "network": "targets",
            "template": "ubuntu-22",
            "ram_mb": 4096,
            "disk_size_gb": 80,
            "role": "SIEM / Blue Team",
        })

        # Add attacker
        config["ludus"]["vms"].append({
            "hostname": "kali-attacker",
            "network": "attacker",
            "template": "kali-linux",
            "ram_mb": 4096,
            "disk_size_gb": 60,
            "role": "Red Team Attacker",
        })

        return config

    @staticmethod
    def _web_app(
        database_type: str = "mysql",
        include_attacker: bool = True,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Web application lab template."""
        config = {
            "ludus": {
                "networks": [
                    {"name": "web", "cidr": "192.168.1.0/24", "description": "Web application network"},
                ],
                "vms": [
                    {
                        "hostname": "web-server",
                        "network": "web",
                        "template": "ubuntu-22",
                        "ram_mb": 2048,
                        "disk_size_gb": 40,
                        "role": "Web Server",
                    },
                ],
            }
        }

        # Add database
        if database_type and database_type != "none":
            config["ludus"]["vms"].append({
                "hostname": "db-server",
                "network": "web",
                "template": "ubuntu-22",
                "ram_mb": 2048,
                "disk_size_gb": 40,
                "role": f"{database_type.upper()} Database",
            })

        # Add attacker
        if include_attacker:
            config["ludus"]["vms"].append({
                "hostname": "kali-attacker",
                "network": "web",
                "template": "kali-linux",
                "ram_mb": 4096,
                "disk_size_gb": 60,
                "role": "Security Testing",
            })

        return config

    @staticmethod
    def _network_segmentation(
        vlans: int = 3,
        vms_per_vlan: int = 2,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Network segmentation lab template."""
        config = {
            "ludus": {
                "networks": [],
                "vms": [],
            }
        }

        vlan_names = ["dmz", "internal", "management", "servers", "clients"]

        for i in range(vlans):
            vlan_name = vlan_names[i] if i < len(vlan_names) else f"vlan{i+1}"
            base_ip = 10 + i

            config["ludus"]["networks"].append({
                "name": vlan_name,
                "cidr": f"192.168.{base_ip}.0/24",
                "description": f"{vlan_name.upper()} VLAN",
            })

            # Add VMs to this VLAN
            for j in range(1, vms_per_vlan + 1):
                config["ludus"]["vms"].append({
                    "hostname": f"{vlan_name}-vm{j}",
                    "network": vlan_name,
                    "template": "ubuntu-22",
                    "ram_mb": 2048,
                    "disk_size_gb": 40,
                    "role": f"{vlan_name.upper()} System",
                })

        return config

    @staticmethod
    def _minimal(
        template1: str = "ubuntu-22",
        template2: str = "ubuntu-22",
        **kwargs: Any
    ) -> dict[str, Any]:
        """Minimal 2-VM lab for quick testing."""
        return {
            "ludus": {
                "networks": [
                    {"name": "main", "cidr": "192.168.1.0/24", "description": "Main network"},
                ],
                "vms": [
                    {
                        "hostname": "vm01",
                        "network": "main",
                        "template": template1,
                        "ram_mb": 2048,
                        "disk_size_gb": 40,
                        "role": "System 1",
                    },
                    {
                        "hostname": "vm02",
                        "network": "main",
                        "template": template2,
                        "ram_mb": 2048,
                        "disk_size_gb": 40,
                        "role": "System 2",
                    },
                ],
            }
        }
