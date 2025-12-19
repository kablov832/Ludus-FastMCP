"""Base scenario builder for Ludus range configurations."""

from typing import Any
import yaml
from .siem_config import (
    SIEMType,
    get_siem_server_config,
    add_siem_agent_to_vm,
    get_siem_network_rules,
)
from ..schemas.scenario_customization import ScenarioCustomization


class BaseScenarioBuilder:
    """Base class for building Ludus range scenarios."""

    def __init__(
        self,
        range_id: str = "{{ range_id }}",
        siem_type: SIEMType = "wazuh",
        resource_profile: str = "minimal",
        customization: ScenarioCustomization | None = None,
        randomize: bool = False,
    ):
        """Initialize the scenario builder.

        Args:
            range_id: Range identifier
            siem_type: SIEM type (wazuh, splunk, elastic, security-onion, none)
            resource_profile: Resource allocation profile - "minimal", "recommended", "maximum"
                - minimal: Lowest resource requirements (may be slow)
                - recommended: Balanced performance and resource usage (default)
                - maximum: High performance with maximum resources
            customization: Optional scenario customization (users, vulnerabilities, etc.)
            randomize: Whether to apply randomization (requires customization with randomization_config)
        """
        self.range_id = range_id
        self.siem_type = siem_type
        self.resource_profile = resource_profile
        self.customization = customization
        self.randomize = randomize
        self.config = {
            "name": None,  # Range name - will be set by scenario builders
            "ludus": [],
            "network": {
                "inter_vlan_default": "REJECT",
                "rules": [],
            },
        }

        # Resource profiles: (ram_gb, cpus)
        self.RESOURCE_PROFILES = {
            "minimal": {
                "dc": (2, 2),
                "workstation": (2, 2),
                "server": (2, 2),
                "sql_server": (4, 2),
                "exchange_server": (4, 2),
                "kali": (4, 2),
                "siem": (4, 2),
                "edr": (4, 2),
                "linux_server": (2, 2),
                "analysis_win": (4, 2),
                "analysis_linux": (4, 2),
            },
            "recommended": {
                "dc": (4, 2),
                "workstation": (4, 2),
                "server": (4, 2),
                "sql_server": (8, 4),
                "exchange_server": (8, 4),
                "kali": (8, 4),
                "siem": (8, 4),
                "edr": (6, 2),
                "linux_server": (4, 2),
                "analysis_win": (8, 4),
                "analysis_linux": (8, 4),
            },
            "maximum": {
                "dc": (8, 4),
                "workstation": (8, 4),
                "server": (8, 4),
                "sql_server": (16, 8),
                "exchange_server": (16, 8),
                "kali": (16, 8),
                "siem": (16, 8),
                "edr": (12, 4),
                "linux_server": (8, 4),
                "analysis_win": (16, 8),
                "analysis_linux": (16, 8),
            },
        }

    def get_resources(self, vm_type: str) -> tuple[int, int]:
        """Get RAM and CPU allocation for a VM type based on resource profile.

        Args:
            vm_type: Type of VM (dc, workstation, server, etc.)

        Returns:
            Tuple of (ram_gb, cpus)
        """
        profile = self.RESOURCE_PROFILES.get(self.resource_profile, self.RESOURCE_PROFILES["minimal"])
        return profile.get(vm_type, (2, 2))  # Default to 2GB/2CPU if type not found

    def add_vm(
        self,
        vm_name: str,
        hostname: str,
        template: str,
        vlan: int,
        ip_last_octet: int,
        ram_gb: int = 8,
        cpus: int = 4,
        **kwargs: Any,
    ) -> None:
        """Add a VM to the configuration."""
        vm_config: dict[str, Any] = {
            "vm_name": vm_name,
            "hostname": hostname,
            "template": template,
            "vlan": vlan,
            "ip_last_octet": ip_last_octet,
            "ram_gb": ram_gb,
            "cpus": cpus,
        }
        vm_config.update(kwargs)
        self.config["ludus"].append(vm_config)

    def add_network_rule(
        self,
        name: str,
        vlan_src: int,
        vlan_dst: int,
        protocol: str = "all",
        ports: str | int = "all",
        action: str = "ACCEPT",
    ) -> None:
        """Add a network rule."""
        rule = {
            "name": name,
            "vlan_src": vlan_src,
            "vlan_dst": vlan_dst,
            "protocol": protocol,
            "ports": ports,
            "action": action,
        }
        self.config["network"]["rules"].append(rule)

    def to_yaml(self) -> str:
        """Convert configuration to YAML string."""
        # Add YAML schema comment
        yaml_str = "# yaml-language-server: $schema=https://docs.ludus.cloud/schemas/range-config.json\n\n"
        yaml_str += yaml.dump(self.config, default_flow_style=False, sort_keys=False)
        return yaml_str

    def add_siem_server(
        self, vlan: int = 10, ip_last_octet: int = 100, siem_type: SIEMType | None = None
    ) -> dict[str, Any]:
        """Add SIEM server to the configuration."""
        if siem_type is None:
            siem_type = self.siem_type
        
        if siem_type == "none":
            return {}
        
        siem_config = get_siem_server_config(siem_type, self.range_id, vlan, ip_last_octet)
        self.add_vm(**siem_config)
        
        # Add SIEM network rules
        for rule in get_siem_network_rules(siem_type):
            # Convert 0 (all VLANs) to actual VLAN numbers for each rule
            if rule["vlan_src"] == 0:
                # Allow from all existing VLANs in the config
                existing_vlans = set()
                for vm in self.config["ludus"]:
                    if "vlan" in vm:
                        existing_vlans.add(vm["vlan"])
                # Add rules for each VLAN to SIEM server VLAN
                for src_vlan in existing_vlans:
                    self.add_network_rule(
                        name=rule["name"] + f" (from VLAN {src_vlan})",
                        vlan_src=src_vlan,
                        vlan_dst=vlan,
                        protocol=rule["protocol"],
                        ports=rule["ports"],
                        action=rule["action"],
                    )
            else:
                self.add_network_rule(**rule)
        
        return siem_config

    def add_siem_agents_to_all_vms(self, siem_server_ip: str | None = None, siem_type: SIEMType | None = None) -> None:
        """Add SIEM agent configuration to all VMs in the range."""
        if siem_type is None:
            siem_type = self.siem_type
        
        if siem_type == "none":
            return
        
        # If no IP provided, calculate from SIEM server config (default: VLAN 10, IP .100)
        if siem_server_ip is None:
            # Default SIEM server IP (will be set during deployment)
            siem_server_ip = "192.168.10.100"  # Default, will be replaced with actual IP
        
        siem_keywords = {
            "wazuh": "wazuh",
            "splunk": "splunk",
            "elastic": "elastic",
            "security-onion": "security-onion",
        }
        
        siem_keyword = siem_keywords.get(siem_type, "")
        
        for vm in self.config["ludus"]:
            # Skip SIEM server itself
            if siem_keyword in vm.get("vm_name", "").lower() and "server" in vm.get("vm_name", "").lower():
                continue
            
            # Add SIEM agent to all other VMs
            add_siem_agent_to_vm(vm, siem_type, siem_server_ip)
    
    # Backward compatibility methods
    def add_wazuh_server(self, vlan: int = 10, ip_last_octet: int = 100) -> dict[str, Any]:
        """Add Wazuh server (backward compatibility)."""
        return self.add_siem_server(vlan, ip_last_octet, "wazuh")
    
    def add_wazuh_agent_to_all_vms(self, wazuh_server_ip: str | None = None) -> None:
        """Add Wazuh agents (backward compatibility)."""
        self.add_siem_agents_to_all_vms(wazuh_server_ip, "wazuh")

    def set_range_name(self, name: str) -> "BaseScenarioBuilder":
        """Set the range name.
        
        Args:
            name: Range name to set
            
        Returns:
            Self for method chaining
        """
        self.config["name"] = name
        return self
    
    def apply_customizations(self) -> None:
        """Apply customizations to the configuration.
        
        This method should be called after the scenario is built but before finalizing.
        """
        if not self.customization:
            return
        
        # Apply network customizations
        if self.customization.network_customization:
            nc = self.customization.network_customization
            if nc.inter_vlan_default:
                self.config["network"]["inter_vlan_default"] = nc.inter_vlan_default
            
            # Apply VLAN changes
            if nc.vlan_changes:
                for vm in self.config.get("ludus", []):
                    vm_name = vm.get("vm_name", "")
                    for pattern, new_vlan in nc.vlan_changes.items():
                        if pattern in vm_name:
                            vm["vlan"] = new_vlan
            
            # Add additional rules
            if nc.additional_rules:
                self.config["network"]["rules"].extend(nc.additional_rules)
            
            # Remove rules
            if nc.remove_rules:
                self.config["network"]["rules"] = [
                    rule for rule in self.config["network"]["rules"]
                    if rule.get("name") not in nc.remove_rules
                ]
        
        # Apply VM customizations
        if self.customization.vm_customization:
            vc = self.customization.vm_customization
            
            # Apply resource overrides
            if vc.resource_overrides:
                for vm in self.config.get("ludus", []):
                    vm_name = vm.get("vm_name", "")
                    if vm_name in vc.resource_overrides:
                        overrides = vc.resource_overrides[vm_name]
                        if "ram_gb" in overrides:
                            vm["ram_gb"] = overrides["ram_gb"]
                        if "cpus" in overrides:
                            vm["cpus"] = overrides["cpus"]
            
            # Remove VMs
            if vc.remove_vms:
                self.config["ludus"] = [
                    vm for vm in self.config["ludus"]
                    if not any(pattern in vm.get("vm_name", "") for pattern in vc.remove_vms)
                ]
            
            # Add additional VMs
            if vc.additional_vms:
                self.config["ludus"].extend(vc.additional_vms)
    
    def to_dict(self) -> dict[str, Any]:
        """Get configuration as dictionary.
        
        Converts ansible_roles format to Ludus roles format:
        - ansible_roles: [{name: "...", vars: {...}}] -> roles: ["..."] and role_vars: {...}
        
        Also applies any customizations before returning.
        """
        # Apply customizations before converting
        self.apply_customizations()
        
        config = self.config.copy()
        
        # Ensure name is set (use default if None)
        if config.get("name") is None:
            config["name"] = "Ludus Range"
        
        # Convert ansible_roles to Ludus format (roles + role_vars)
        for vm in config.get("ludus", []):
            if "ansible_roles" in vm:
                ansible_roles = vm.pop("ansible_roles")
                
                # Extract role names for 'roles' array
                roles_list = []
                role_vars_dict = {}
                
                for role in ansible_roles:
                    if isinstance(role, dict):
                        role_name = role.get("name")
                        if role_name:
                            roles_list.append(role_name)
                            # Merge role-specific vars into role_vars
                            role_vars = role.get("vars", {})
                            if role_vars:
                                # Prefix role vars with role name to avoid conflicts
                                # Or merge directly if no conflicts
                                for key, value in role_vars.items():
                                    if key not in role_vars_dict:
                                        role_vars_dict[key] = value
                                    elif isinstance(role_vars_dict[key], dict) and isinstance(value, dict):
                                        role_vars_dict[key].update(value)
                    elif isinstance(role, str):
                        roles_list.append(role)
                
                if roles_list:
                    vm["roles"] = roles_list
                if role_vars_dict:
                    vm["role_vars"] = role_vars_dict
        
        return config

