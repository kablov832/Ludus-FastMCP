"""Custom user-defined scenarios - build and save your own lab configurations."""

import json
import os
from pathlib import Path
from typing import Any, Optional
from .base import BaseScenarioBuilder


class CustomScenarioBuilder(BaseScenarioBuilder):
    """Builder for custom user-defined scenarios."""

    def __init__(
        self,
        range_id: str = "{{ range_id }}",
        siem_type: str = "wazuh",
        resource_profile: str = "minimal",
    ):
        """Initialize custom scenario builder."""
        super().__init__(range_id, siem_type, resource_profile)
        self.metadata = {
            "name": "Custom Scenario",
            "description": "User-defined custom scenario",
            "author": "user",
            "created_at": None,
            "updated_at": None,
            "tags": [],
        }

    def set_metadata(
        self,
        name: str,
        description: str,
        author: str = "user",
        tags: Optional[list[str]] = None,
    ) -> "CustomScenarioBuilder":
        """Set scenario metadata.

        Args:
            name: Scenario name
            description: Scenario description
            author: Author name
            tags: Optional tags for categorization

        Returns:
            Self for method chaining
        """
        import datetime

        self.metadata["name"] = name
        self.metadata["description"] = description
        self.metadata["author"] = author
        self.metadata["tags"] = tags or []
        self.metadata["updated_at"] = datetime.datetime.now().isoformat()

        if self.metadata["created_at"] is None:
            self.metadata["created_at"] = self.metadata["updated_at"]

        return self

    def add_domain_controller(
        self,
        hostname: str,
        domain: str,
        vlan: int = 10,
        ip_last_octet: int = 10,
        ram_gb: Optional[int] = None,
        cpus: Optional[int] = None,
    ) -> "CustomScenarioBuilder":
        """Add a domain controller to the scenario.

        Args:
            hostname: Hostname for the DC
            domain: Domain FQDN (e.g., 'corp.local')
            vlan: VLAN number
            ip_last_octet: Last octet of IP address
            ram_gb: Optional RAM override (uses profile default if not set)
            cpus: Optional CPU override (uses profile default if not set)

        Returns:
            Self for method chaining
        """
        dc_ram, dc_cpus = self.get_resources("dc")
        self.add_vm(
            vm_name=f"{self.range_id}-dc-{hostname.lower()}",
            hostname=hostname,
            template="win2022-server-x64-template",
            vlan=vlan,
            ip_last_octet=ip_last_octet,
            ram_gb=ram_gb or dc_ram,
            cpus=cpus or dc_cpus,
            windows={"sysprep": False},
            domain={"fqdn": domain, "role": "primary-dc"},
        )
        return self

    def add_workstation(
        self,
        hostname: str,
        domain: Optional[str] = None,
        vlan: int = 10,
        ip_last_octet: int = 20,
        ram_gb: Optional[int] = None,
        cpus: Optional[int] = None,
        packages: Optional[list[str]] = None,
    ) -> "CustomScenarioBuilder":
        """Add a Windows 11 workstation to the scenario.

        Args:
            hostname: Hostname for the workstation
            domain: Optional domain to join
            vlan: VLAN number
            ip_last_octet: Last octet of IP address
            ram_gb: Optional RAM override
            cpus: Optional CPU override
            packages: Optional Chocolatey packages to install

        Returns:
            Self for method chaining
        """
        ws_ram, ws_cpus = self.get_resources("workstation")
        vm_config = {
            "vm_name": f"{self.range_id}-{hostname.lower()}",
            "hostname": hostname,
            "template": "win11-22h2-x64-enterprise-template",
            "vlan": vlan,
            "ip_last_octet": ip_last_octet,
            "ram_gb": ram_gb or ws_ram,
            "cpus": cpus or ws_cpus,
        }

        if packages:
            vm_config["windows"] = {
                "chocolatey_packages": packages,
                "chocolatey_ignore_checksums": True,
            }

        if domain:
            vm_config["domain"] = {"fqdn": domain, "role": "member"}

        self.add_vm(**vm_config)
        return self

    def add_server(
        self,
        hostname: str,
        server_type: str = "fileserver",
        domain: Optional[str] = None,
        vlan: int = 10,
        ip_last_octet: int = 15,
        ram_gb: Optional[int] = None,
        cpus: Optional[int] = None,
    ) -> "CustomScenarioBuilder":
        """Add a Windows Server to the scenario.

        Args:
            hostname: Hostname for the server
            server_type: Type of server (fileserver, sql, exchange, web)
            domain: Optional domain to join
            vlan: VLAN number
            ip_last_octet: Last octet of IP address
            ram_gb: Optional RAM override
            cpus: Optional CPU override

        Returns:
            Self for method chaining
        """
        # Choose appropriate resource profile based on server type
        if server_type == "sql":
            default_ram, default_cpus = self.get_resources("sql_server")
        elif server_type == "exchange":
            default_ram, default_cpus = self.get_resources("exchange_server")
        else:
            default_ram, default_cpus = self.get_resources("server")

        vm_config = {
            "vm_name": f"{self.range_id}-{server_type}-{hostname.lower()}",
            "hostname": hostname,
            "template": "win2022-server-x64-template",
            "vlan": vlan,
            "ip_last_octet": ip_last_octet,
            "ram_gb": ram_gb or default_ram,
            "cpus": cpus or default_cpus,
            "windows": {"sysprep": False},
        }

        if domain:
            vm_config["domain"] = {"fqdn": domain, "role": "member"}

        self.add_vm(**vm_config)
        return self

    def add_linux_server(
        self,
        hostname: str,
        vlan: int = 10,
        ip_last_octet: int = 50,
        ram_gb: Optional[int] = None,
        cpus: Optional[int] = None,
        template: str = "ubuntu-22.04-x64-server-template",
    ) -> "CustomScenarioBuilder":
        """Add a Linux server to the scenario.

        Args:
            hostname: Hostname for the server
            vlan: VLAN number
            ip_last_octet: Last octet of IP address
            ram_gb: Optional RAM override
            cpus: Optional CPU override
            template: Linux template to use

        Returns:
            Self for method chaining
        """
        srv_ram, srv_cpus = self.get_resources("linux_server")
        self.add_vm(
            vm_name=f"{self.range_id}-{hostname.lower()}",
            hostname=hostname,
            template=template,
            vlan=vlan,
            ip_last_octet=ip_last_octet,
            ram_gb=ram_gb or srv_ram,
            cpus=cpus or srv_cpus,
            linux=True,
        )
        return self

    def add_kali_attacker(
        self,
        hostname: str = "KALI",
        vlan: int = 99,
        ip_last_octet: int = 10,
        ram_gb: Optional[int] = None,
        cpus: Optional[int] = None,
    ) -> "CustomScenarioBuilder":
        """Add a Kali Linux attacker to the scenario.

        Args:
            hostname: Hostname for the attacker
            vlan: VLAN number (default: 99 for attacker network)
            ip_last_octet: Last octet of IP address
            ram_gb: Optional RAM override
            cpus: Optional CPU override

        Returns:
            Self for method chaining
        """
        kali_ram, kali_cpus = self.get_resources("kali")
        self.add_vm(
            vm_name=f"{self.range_id}-kali-{hostname.lower()}",
            hostname=hostname,
            template="kali-x64-desktop-template",
            vlan=vlan,
            ip_last_octet=ip_last_octet,
            ram_gb=ram_gb or kali_ram,
            cpus=cpus or kali_cpus,
            linux=True,
            testing={"snapshot": False, "block_internet": False},
        )
        return self

    def allow_communication(
        self,
        name: str,
        from_vlan: int,
        to_vlan: int,
        protocol: str = "all",
        ports: Any = "all",
    ) -> "CustomScenarioBuilder":
        """Add a network rule to allow communication between VLANs.

        Args:
            name: Rule name
            from_vlan: Source VLAN
            to_vlan: Destination VLAN
            protocol: Protocol (tcp, udp, all)
            ports: Port(s) to allow (single int, list of ints, or "all")

        Returns:
            Self for method chaining
        """
        self.add_network_rule(
            name=name,
            vlan_src=from_vlan,
            vlan_dst=to_vlan,
            protocol=protocol,
            ports=ports,
            action="ACCEPT",
        )
        return self

    def add_monitoring(
        self,
        vlan: int = 10,
        ip_last_octet: int = 100,
        include_agents: bool = True,
    ) -> "CustomScenarioBuilder":
        """Add SIEM monitoring to the scenario.

        Args:
            vlan: VLAN for SIEM server
            ip_last_octet: Last octet of IP address
            include_agents: Whether to add SIEM agents to all VMs

        Returns:
            Self for method chaining
        """
        if self.siem_type != "none":
            self.add_siem_server(vlan=vlan, ip_last_octet=ip_last_octet)
            if include_agents:
                self.add_siem_agents_to_all_vms()
        return self

    def to_dict_with_metadata(self) -> dict[str, Any]:
        """Get configuration with metadata as dictionary.

        Returns:
            Dictionary containing both config and metadata
        """
        return {
            "metadata": self.metadata,
            "config": self.config.copy(),
        }


class CustomScenarioManager:
    """Manager for custom user-defined scenarios."""

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize custom scenario manager.

        Args:
            storage_dir: Directory to store custom scenarios (default: ~/.ludus/custom-scenarios)
        """
        if storage_dir is None:
            storage_dir = Path.home() / ".ludus" / "custom-scenarios"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_scenario(
        self, scenario_id: str, builder: CustomScenarioBuilder
    ) -> dict[str, Any]:
        """Save a custom scenario to disk.

        Args:
            scenario_id: Unique identifier for the scenario
            builder: CustomScenarioBuilder instance

        Returns:
            Dictionary with save status and file path
        """
        import datetime

        # Update timestamp
        builder.metadata["updated_at"] = datetime.datetime.now().isoformat()

        # Save to JSON file
        file_path = self.storage_dir / f"{scenario_id}.json"
        data = builder.to_dict_with_metadata()

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        return {
            "status": "saved",
            "scenario_id": scenario_id,
            "file_path": str(file_path),
            "name": builder.metadata["name"],
        }

    def load_scenario(
        self, scenario_id: str, resource_profile: str = "minimal"
    ) -> CustomScenarioBuilder:
        """Load a custom scenario from disk.

        Args:
            scenario_id: Unique identifier for the scenario
            resource_profile: Resource profile to use

        Returns:
            CustomScenarioBuilder instance

        Raises:
            FileNotFoundError: If scenario doesn't exist
        """
        file_path = self.storage_dir / f"{scenario_id}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Custom scenario '{scenario_id}' not found")

        with open(file_path, "r") as f:
            data = json.load(f)

        # Create builder and restore configuration
        builder = CustomScenarioBuilder(resource_profile=resource_profile)
        builder.metadata = data.get("metadata", {})
        builder.config = data.get("config", {"ludus": [], "network": {"inter_vlan_default": "REJECT", "rules": []}})

        return builder

    def list_scenarios(self) -> dict[str, dict[str, Any]]:
        """List all saved custom scenarios.

        Returns:
            Dictionary mapping scenario IDs to their metadata
        """
        scenarios = {}

        for file_path in self.storage_dir.glob("*.json"):
            scenario_id = file_path.stem

            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    scenarios[scenario_id] = data.get("metadata", {})
            except Exception as e:
                # Skip corrupted files
                continue

        return scenarios

    def delete_scenario(self, scenario_id: str) -> dict[str, str]:
        """Delete a custom scenario.

        Args:
            scenario_id: Unique identifier for the scenario

        Returns:
            Dictionary with deletion status

        Raises:
            FileNotFoundError: If scenario doesn't exist
        """
        file_path = self.storage_dir / f"{scenario_id}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Custom scenario '{scenario_id}' not found")

        file_path.unlink()

        return {
            "status": "deleted",
            "scenario_id": scenario_id,
        }

    def export_scenario(self, scenario_id: str, export_path: Path) -> dict[str, str]:
        """Export a custom scenario to a specific location.

        Args:
            scenario_id: Unique identifier for the scenario
            export_path: Path to export the scenario to

        Returns:
            Dictionary with export status
        """
        import shutil

        source_path = self.storage_dir / f"{scenario_id}.json"

        if not source_path.exists():
            raise FileNotFoundError(f"Custom scenario '{scenario_id}' not found")

        shutil.copy(source_path, export_path)

        return {
            "status": "exported",
            "scenario_id": scenario_id,
            "export_path": str(export_path),
        }

    def import_scenario(
        self, scenario_id: str, import_path: Path
    ) -> dict[str, str]:
        """Import a custom scenario from a file.

        Args:
            scenario_id: Unique identifier for the scenario
            import_path: Path to import the scenario from

        Returns:
            Dictionary with import status
        """
        import shutil

        if not Path(import_path).exists():
            raise FileNotFoundError(f"Import file not found: {import_path}")

        # Validate JSON structure
        with open(import_path, "r") as f:
            data = json.load(f)
            if "metadata" not in data or "config" not in data:
                raise ValueError("Invalid scenario file format")

        # Copy to storage directory
        dest_path = self.storage_dir / f"{scenario_id}.json"
        shutil.copy(import_path, dest_path)

        return {
            "status": "imported",
            "scenario_id": scenario_id,
            "name": data.get("metadata", {}).get("name", "Unknown"),
        }
