"""Blue team defensive security scenarios - realistic SOC and detection engineering labs."""

from .base import BaseScenarioBuilder
from .ad_config import (
    get_realistic_ad_users,
    get_local_admin_accounts,
    get_ad_cs_config,
    get_ad_attack_paths,
    get_forest_pivot_attack_paths,
    convert_custom_users_to_dict,
)
from .wazuh_opsec import get_wazuh_opsec_ansible_vars
from .live_actions import get_live_action_config


class BlueTeamScenarioBuilder(BaseScenarioBuilder):
    """Builder for blue team defensive security scenarios."""

    def build_blueteam_lab_lite(self) -> "BlueTeamScenarioBuilder":
        """Build lite blue team lab - Small SOC environment.

        Realistic scenario: Small business SOC setup
        - SIEM for log aggregation and analysis
        - Domain controller with logging enabled
        - 2 Windows workstations generating user activity
        - File server with audit logging
        - Basic threat hunting and detection

        Blue team activities:
        - SIEM configuration and log analysis
        - Alert tuning and rule creation
        - Threat hunting basics
        - Incident detection and response
        - Log correlation
        - User behavior analysis

        Resource requirements: 32GB RAM, 14 CPUs
        """
        range_id = self.range_id

        # Prepare AD role variables for ludus-ad-content - use custom users if provided
        custom_users_dict = None
        if self.customization and self.customization.custom_users:
            custom_users_dict = convert_custom_users_to_dict(self.customization.custom_users)
        
        ad_users = get_realistic_ad_users(custom_users=custom_users_dict)
        
        # Base OUs that are always created
        ad_ous = [
            {"name": "Workstations", "path": "DC=corp,DC=local", "description": "Organizational unit for all workstations"},
            {"name": "Servers", "path": "DC=corp,DC=local", "description": "Organizational unit for all servers"},
        ]
        
        # Base groups that are always created
        ad_groups = [
            {"name": "Domain Users", "scope": "global", "path": "DC=corp,DC=local", "description": "All domain users"},
            {"name": "Domain Admins", "scope": "global", "path": "DC=corp,DC=local", "description": "Domain administrators"},
        ]
        
        # Built-in groups that might be assigned to users
        # These groups already exist in AD (CN=Builtin,DC=corp,DC=local) and should NOT be created
        builtin_group_names = {"Power Users", "Backup Operators", "Remote Desktop Users"}
        
        # Dynamically create OUs and groups based on departments in the user list
        departments_found = set()
        groups_needed = set()
        
        for user in ad_users:
            dept = user.get("department")
            if dept:
                departments_found.add(dept)
            # Collect all groups that users need
            user_groups = user.get("groups", [])
            for group in user_groups:
                # Skip base groups and built-in groups
                if group not in ["Domain Users", "Domain Admins"] and group not in builtin_group_names:
                    groups_needed.add(group)
        
        # Note: Built-in groups are NOT added to ad_groups because they already exist in AD
        # Users can still be assigned to them even if they're not in the ad_groups list
        
        # Add OUs for all departments found in users
        for dept in sorted(departments_found):
            ad_ous.append({
                "name": dept,
                "path": "DC=corp,DC=local",
                "description": f"{dept} Department"
            })
            # Add corresponding group for each department
            dept_group_name = f"{dept} Department"
            if not any(g["name"] == dept_group_name for g in ad_groups):
                ad_groups.append({
                    "name": dept_group_name,
                    "scope": "global",
                    "path": f"OU={dept},DC=corp,DC=local",
                    "description": f"{dept} Department members"
                })
        
        # Add ALL other groups that users are assigned to (manager groups, executive, etc.)
        for group_name in groups_needed:
            # Skip if already added (department groups or base groups)
            if not any(g["name"] == group_name for g in ad_groups):
                # Determine OU path based on group name
                group_path = "DC=corp,DC=local"  # Default
                if "Managers" in group_name:
                    # Extract department from group name (e.g., "HR Managers" -> "HR")
                    dept = group_name.replace(" Managers", "").replace("Managers", "").strip()
                    if dept in departments_found:
                        group_path = f"OU={dept},DC=corp,DC=local"
                elif group_name == "Executive":
                    # Executive group goes to Executive OU if it exists
                    if "Executive" in departments_found:
                        group_path = "OU=Executive,DC=corp,DC=local"
                
                ad_groups.append({
                    "name": group_name,
                    "scope": "global",
                    "path": group_path,
                    "description": f"{group_name} group"
                })
        
        # If no custom users, ensure default departments are included
        if not custom_users_dict:
            default_departments = ["IT", "HR", "Finance"]
            for dept in default_departments:
                if dept not in departments_found:
                    ad_ous.append({
                        "name": dept,
                        "path": "DC=corp,DC=local",
                        "description": f"{dept} Department"
                    })
                    dept_group_name = f"{dept} Department"
                    if not any(g["name"] == dept_group_name for g in ad_groups):
                        ad_groups.append({
                            "name": dept_group_name,
                            "scope": "global",
                            "path": f"OU={dept},DC=corp,DC=local",
                            "description": f"{dept} Department members"
                        })
        
        # Convert ad_users to format expected by ludus-ad-content role
        ludus_ad_users = []
        for user in ad_users:
            ludus_ad_users.append({
                "name": user["username"],
                "firstname": user.get("display_name", "").split()[0] if user.get("display_name") else "",
                "surname": user.get("display_name", "").split()[-1] if user.get("display_name") else "",
                "display_name": user.get("display_name", user["username"]),
                "password": user["password"],
                "path": f"OU={user['department']},DC=corp,DC=local" if user.get("department") else "DC=corp,DC=local",
                "description": user.get("description", ""),
                "groups": user.get("groups", []),
            })

        # Domain Controller with enhanced logging and realistic AD configuration
        dc_ram, dc_cpus = self.get_resources("dc")
        self.add_vm(
            vm_name=f"{range_id}-dc-win2022-server-x64",
            hostname=f"{range_id}-DC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=10,
            ram_gb=dc_ram,
            cpus=dc_cpus,
            windows={"sysprep": False},
            domain={"fqdn": "corp.local", "role": "primary-dc"},
            ansible_roles=[
                {
                    "name": "ludus-ad-content",
                    "vars": {
                        "ludus_ad": {
                            "ous": ad_ous,
                            "groups": ad_groups,
                            "users": ludus_ad_users,
                        }
                    }
                },
                # Note: ludus.enhanced_logging role is optional - remove if not installed
                # {
                #     "name": "ludus.enhanced_logging",
                #     "vars": {
                #         "audit_policy": "comprehensive",
                #         "log_retention_days": 90,
                #     },
                # },
            ],
        )

        # Workstations (monitored endpoints) - check for VM customization
        workstation_count = 2  # Default
        if self.customization and self.customization.vm_customization:
            vm_custom = self.customization.vm_customization
            if "workstation" in vm_custom.vm_count_overrides:
                workstation_count = vm_custom.vm_count_overrides["workstation"]
        
        for i in range(1, workstation_count + 1):
            self.add_vm(
                vm_name=f"{range_id}-workstation-{i}-win11",
                hostname=f"{range_id}-WS{i}",
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=20 + i,
                ram_gb=4,
                cpus=2,
                windows={
                    "chocolatey_packages": ["googlechrome", "notepadplusplus"],
                    "chocolatey_ignore_checksums": True,
                },
                domain={"fqdn": "corp.local", "role": "member"},
            )

        # File Server with auditing
        self.add_vm(
            vm_name=f"{range_id}-fileserver-win2022-server-x64",
            hostname=f"{range_id}-FILES01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=15,
            ram_gb=4,
            cpus=2,
            windows={},
            domain={"fqdn": "corp.local", "role": "member"},
        )

        # SIEM Server with OPSEC detection rules
        if self.siem_type == "wazuh":
            self.add_siem_server(vlan=10, ip_last_octet=100)
            # Enhance Wazuh with OPSEC detection rules
            # Note: ludus.wazuh_opsec role is optional - uncomment if installed
            # for vm in self.config["ludus"]:
            #     if "wazuh" in vm.get("vm_name", "").lower() and "server" in vm.get("vm_name", "").lower():
            #         if "ansible_roles" not in vm:
            #             vm["ansible_roles"] = []
            #         vm["ansible_roles"].append({
            #             "name": "ludus.wazuh_opsec",
            #             "vars": get_wazuh_opsec_ansible_vars(),
            #         })
            #         break

        # Add SIEM agents to all VMs for log collection
        self.add_siem_agents_to_all_vms()
        
        # Add live action simulation role for blue team training
        # Note: ludus.live_actions role is optional - uncomment if installed
        # for vm in self.config["ludus"]:
        #     if "dc" in vm.get("vm_name", "").lower():
        #         if "ansible_roles" not in vm:
        #             vm["ansible_roles"] = []
        #         vm["ansible_roles"].append({
        #             "name": "ludus.live_actions",
        #             "vars": get_live_action_config(
        #                 simulation_enabled=True,
        #                 simulation_interval=3600,  # Run every hour
        #                 simulation_intensity="low",
        #             ),
        #         })
        #         break

        return self

    def build_blueteam_lab_intermediate(self) -> "BlueTeamScenarioBuilder":
        """Build intermediate blue team lab - Medium SOC with EDR and network monitoring.

        Realistic scenario: Medium enterprise SOC
        - Advanced SIEM with correlation rules
        - EDR deployment across endpoints
        - Network monitoring and traffic analysis
        - Multiple departments to monitor
        - IDS/IPS capabilities
        - Threat intelligence integration

        Blue team activities:
        - Advanced SIEM rule creation
        - EDR alert investigation
        - Network traffic analysis
        - Threat hunting with multiple data sources
        - Incident response workflows
        - Detection engineering
        - PCAP analysis
        - Indicator of Compromise (IOC) tracking
        - Malware analysis preparation

        Resource requirements: 64GB RAM, 26 CPUs
        """
        range_id = self.range_id

        # Prepare AD role variables for ludus-ad-content - use custom users if provided
        custom_users_dict = None
        if self.customization and self.customization.custom_users:
            custom_users_dict = convert_custom_users_to_dict(self.customization.custom_users)
        
        ad_users = get_realistic_ad_users(custom_users=custom_users_dict)
        
        # Base OUs that are always created
        ad_ous = [
            {"name": "Workstations", "path": "DC=corp,DC=local", "description": "Organizational unit for all workstations"},
            {"name": "Servers", "path": "DC=corp,DC=local", "description": "Organizational unit for all servers"},
        ]
        
        # Base groups that are always created
        ad_groups = [
            {"name": "Domain Users", "scope": "global", "path": "DC=corp,DC=local", "description": "All domain users"},
            {"name": "Domain Admins", "scope": "global", "path": "DC=corp,DC=local", "description": "Domain administrators"},
        ]
        
        # Built-in groups that might be assigned to users
        # These groups already exist in AD (CN=Builtin,DC=corp,DC=local) and should NOT be created
        builtin_group_names = {"Power Users", "Backup Operators", "Remote Desktop Users"}
        
        # Dynamically create OUs and groups based on departments in the user list
        departments_found = set()
        groups_needed = set()
        
        for user in ad_users:
            dept = user.get("department")
            if dept:
                departments_found.add(dept)
            # Collect all groups that users need
            user_groups = user.get("groups", [])
            for group in user_groups:
                # Skip base groups and built-in groups
                if group not in ["Domain Users", "Domain Admins"] and group not in builtin_group_names:
                    groups_needed.add(group)
        
        # Note: Built-in groups are NOT added to ad_groups because they already exist in AD
        # Users can still be assigned to them even if they're not in the ad_groups list
        
        # Add OUs for all departments found in users
        for dept in sorted(departments_found):
            ad_ous.append({
                "name": dept,
                "path": "DC=corp,DC=local",
                "description": f"{dept} Department"
            })
            # Add corresponding group for each department
            dept_group_name = f"{dept} Department"
            if not any(g["name"] == dept_group_name for g in ad_groups):
                ad_groups.append({
                    "name": dept_group_name,
                    "scope": "global",
                    "path": f"OU={dept},DC=corp,DC=local",
                    "description": f"{dept} Department members"
                })
        
        # Add ALL other groups that users are assigned to (manager groups, executive, etc.)
        for group_name in groups_needed:
            # Skip if already added (department groups or base groups)
            if not any(g["name"] == group_name for g in ad_groups):
                # Determine OU path based on group name
                group_path = "DC=corp,DC=local"  # Default
                if "Managers" in group_name:
                    # Extract department from group name (e.g., "HR Managers" -> "HR")
                    dept = group_name.replace(" Managers", "").replace("Managers", "").strip()
                    if dept in departments_found:
                        group_path = f"OU={dept},DC=corp,DC=local"
                elif group_name == "Executive":
                    # Executive group goes to Executive OU if it exists
                    if "Executive" in departments_found:
                        group_path = "OU=Executive,DC=corp,DC=local"
                
                ad_groups.append({
                    "name": group_name,
                    "scope": "global",
                    "path": group_path,
                    "description": f"{group_name} group"
                })
        
        # Ensure default departments are included (IT, HR, FINANCE, SALES for intermediate)
        default_departments = ["IT", "HR", "Finance", "Sales"]
        for dept in default_departments:
            if dept not in departments_found:
                ad_ous.append({
                    "name": dept,
                    "path": "DC=corp,DC=local",
                    "description": f"{dept} Department"
                })
                dept_group_name = f"{dept} Department"
                if not any(g["name"] == dept_group_name for g in ad_groups):
                    ad_groups.append({
                        "name": dept_group_name,
                        "scope": "global",
                        "path": f"OU={dept},DC=corp,DC=local",
                        "description": f"{dept} Department members"
                    })
        
        # Convert ad_users to format expected by ludus-ad-content role
        ludus_ad_users = []
        for user in ad_users:
            ludus_ad_users.append({
                "name": user["username"],
                "firstname": user.get("display_name", "").split()[0] if user.get("display_name") else "",
                "surname": user.get("display_name", "").split()[-1] if user.get("display_name") else "",
                "display_name": user.get("display_name", user["username"]),
                "password": user["password"],
                "path": f"OU={user['department']},DC=corp,DC=local" if user.get("department") else "DC=corp,DC=local",
                "description": user.get("description", ""),
                "groups": user.get("groups", []),
            })

        # Domain Controller with realistic AD configuration
        dc_ram, dc_cpus = self.get_resources("dc")
        self.add_vm(
            vm_name=f"{range_id}-dc-win2022-server-x64",
            hostname=f"{range_id}-DC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=10,
            ram_gb=dc_ram,
            cpus=dc_cpus,
            windows={"sysprep": False},
            domain={"fqdn": "corp.local", "role": "primary-dc"},
            ansible_roles=[
                {
                    "name": "ludus-ad-content",
                    "vars": {
                        "ludus_ad": {
                            "ous": ad_ous,
                            "groups": ad_groups,
                            "users": ludus_ad_users,
                        }
                    }
                },
                # Note: ludus.enhanced_logging role is optional - remove if not installed
                # {
                #     "name": "ludus.enhanced_logging",
                #     "vars": {
                #         "audit_policy": "comprehensive",
                #         "log_retention_days": 90,
                #     },
                # },
            ],
        )
        
        # AD CS Server for certificate-based attack detection
        self.add_vm(
            vm_name=f"{range_id}-adcs-win2022-server-x64",
            hostname=f"{range_id}-ADCS01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=12,
            ram_gb=4,
            cpus=2,
            windows={},
            domain={"fqdn": "corp.local", "role": "member"},
            ansible_roles=[
                {
                    "name": "badsectorlabs.ludus_adcs",  # Correct Ludus role from docs
                    "vars": {
                        "ad_cs_config": get_ad_cs_config(
                            vulnerability_config=(
                                {
                                    "esc1_enabled": self.customization.vulnerability_config.esc1_enabled,
                                    "esc2_enabled": self.customization.vulnerability_config.esc2_enabled,
                                    "esc3_enabled": self.customization.vulnerability_config.esc3_enabled,
                                    "esc4_enabled": self.customization.vulnerability_config.esc4_enabled,
                                    "esc6_enabled": self.customization.vulnerability_config.esc6_enabled,
                                    "esc7_enabled": self.customization.vulnerability_config.esc7_enabled,
                                    "esc8_enabled": self.customization.vulnerability_config.esc8_enabled,
                                }
                                if self.customization and self.customization.vulnerability_config
                                else None
                            )
                        ),
                        "ca_name": "CORP-CA",
                        "ca_type": "Enterprise Root CA",
                    },
                },
            ],
        )

        # SIEM Server (enhanced resources)
        self.add_siem_server(vlan=10, ip_last_octet=100)

        # EDR Server (Endpoint Detection & Response)
        self.add_vm(
            vm_name=f"{range_id}-edr-ubuntu22",
            hostname=f"{range_id}-EDR01",
            template="ubuntu-22.04-x64-server-template",
            vlan=10,
            ip_last_octet=101,
            ram_gb=8,
            cpus=4,
            linux=True,
        )

        # Network IDS/IPS (Suricata/Zeek)
        self.add_vm(
            vm_name=f"{range_id}-ids-ubuntu22",
            hostname=f"{range_id}-IDS01",
            template="ubuntu-22.04-x64-server-template",
            vlan=10,
            ip_last_octet=102,
            ram_gb=8,
            cpus=4,
            linux=True,
        )

        # File Server
        self.add_vm(
            vm_name=f"{range_id}-fileserver-win2022-server-x64",
            hostname=f"{range_id}-FILES01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=20,
            ram_gb=6,
            cpus=2,
            windows={},
            domain={"fqdn": "corp.local", "role": "member"},
        )

        # SQL Server with service account (database logging target)
        sql_ram, sql_cpus = self.get_resources("sql_server")
        self.add_vm(
            vm_name=f"{range_id}-sql-win2022-server-x64",
            hostname=f"{range_id}-SQL01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=25,
            ram_gb=sql_ram,
            cpus=sql_cpus,
            windows={},
            domain={"fqdn": "corp.local", "role": "member"},
            ansible_roles=[
                {
                    "name": "badsectorlabs.ludus_mssql",  # Correct Ludus role from docs
                    "vars": {
                        "sql_service_account": "svc_sql",
                        "sql_install": True,
                    },
                },
            ],
        )

        # Workstations (different departments for varied logging)
        departments = ["IT", "HR", "FINANCE", "SALES"]
        for i, dept in enumerate(departments, start=1):
            self.add_vm(
                vm_name=f"{range_id}-{dept.lower()}-ws-win11",
                hostname=f"{range_id}-{dept}-WS01",
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=30 + i,
                ram_gb=4,
                cpus=2,
                windows={
                    "chocolatey_packages": ["googlechrome", "notepadplusplus", "7zip"],
                    "chocolatey_ignore_checksums": True,
                },
                domain={"fqdn": "corp.local", "role": "member"},
            )

        # Add SIEM agents to all VMs
        self.add_siem_agents_to_all_vms()
        
        # Enhance Wazuh with OPSEC detection rules
        if self.siem_type == "wazuh":
            for vm in self.config["ludus"]:
                if "wazuh" in vm.get("vm_name", "").lower() and "server" in vm.get("vm_name", "").lower():
                    if "ansible_roles" not in vm:
                        vm["ansible_roles"] = []
                    vm["ansible_roles"].append({
                        "name": "ludus.wazuh_opsec",
                        "vars": get_wazuh_opsec_ansible_vars(),
                    })
                    break
        
        # Add live action simulation for blue team training
        # Note: ludus.live_actions role is optional - uncomment if installed
        # for vm in self.config["ludus"]:
        #     if "dc" in vm.get("vm_name", "").lower():
        #         if "ansible_roles" not in vm:
        #             vm["ansible_roles"] = []
        #         vm["ansible_roles"].append({
        #             "name": "ludus.live_actions",
        #             "vars": get_live_action_config(
        #                 simulation_enabled=True,
        #                 simulation_interval=1800,  # Run every 30 minutes
        #                 simulation_intensity="medium",
        #                 randomize_timing=True,
        #             ),
        #         })
        #         break

        return self

    def build_blueteam_lab_advanced(self) -> "BlueTeamScenarioBuilder":
        """Build advanced blue team lab - Enterprise SOC with full detection stack.

        Realistic scenario: Large enterprise SOC operations
        - Multi-tier SIEM architecture
        - EDR with advanced threat hunting
        - Network monitoring with full packet capture
        - Threat intelligence platform
        - Security orchestration and automation (SOAR)
        - Multiple domains and network segments
        - Honeypots and deception technology
        - Forensics workstation

        Blue team activities:
        - Enterprise SIEM management
        - Advanced threat hunting
        - Behavioral analytics
        - Automated incident response
        - Threat intelligence correlation
        - Digital forensics and incident response (DFIR)
        - Malware analysis
        - Network forensics
        - Memory forensics
        - Detection rule development
        - Purple team exercises
        - Honeypot monitoring
        - Deception techniques

        Resource requirements: 104GB RAM, 44 CPUs
        """
        range_id = self.range_id

        # Security Operations Network (VLAN 5) - SOC Infrastructure
        # Primary SIEM
        self.add_siem_server(vlan=5, ip_last_octet=100)

        # Secondary SIEM / Log Collector (for redundancy/scaling)
        self.add_vm(
            vm_name=f"{range_id}-siem-secondary-ubuntu22",
            hostname=f"{range_id}-SIEM02",
            template="ubuntu-22.04-x64-server-template",
            vlan=5,
            ip_last_octet=101,
            ram_gb=12,
            cpus=4,
            linux=True,
        )

        # EDR Server
        self.add_vm(
            vm_name=f"{range_id}-edr-ubuntu22",
            hostname=f"{range_id}-EDR01",
            template="ubuntu-22.04-x64-server-template",
            vlan=5,
            ip_last_octet=102,
            ram_gb=8,
            cpus=4,
            linux=True,
        )

        # Network Security Monitoring (Zeek/Suricata)
        self.add_vm(
            vm_name=f"{range_id}-nsm-ubuntu22",
            hostname=f"{range_id}-NSM01",
            template="ubuntu-22.04-x64-server-template",
            vlan=5,
            ip_last_octet=103,
            ram_gb=12,
            cpus=4,
            linux=True,
        )

        # Threat Intelligence Platform
        self.add_vm(
            vm_name=f"{range_id}-tip-ubuntu22",
            hostname=f"{range_id}-TIP01",
            template="ubuntu-22.04-x64-server-template",
            vlan=5,
            ip_last_octet=104,
            ram_gb=8,
            cpus=4,
            linux=True,
        )

        # SOAR Platform (Security Orchestration, Automation and Response)
        self.add_vm(
            vm_name=f"{range_id}-soar-ubuntu22",
            hostname=f"{range_id}-SOAR01",
            template="ubuntu-22.04-x64-server-template",
            vlan=5,
            ip_last_octet=105,
            ram_gb=6,
            cpus=2,
            linux=True,
        )

        # Forensics Workstation
        self.add_vm(
            vm_name=f"{range_id}-forensics-win11",
            hostname=f"{range_id}-FORENSICS01",
            template="win11-22h2-x64-enterprise-template",
            vlan=5,
            ip_last_octet=110,
            ram_gb=8,
            cpus=4,
            windows={
                "chocolatey_packages": ["autopsy", "wireshark", "7zip"],
                "chocolatey_ignore_checksums": True,
            },
        )

        # Corporate Network (VLAN 10) - Monitored Environment
        # Prepare AD role variables for ludus-ad-content (corp.local forest)
        custom_users_dict = None
        if self.customization and self.customization.custom_users:
            custom_users_dict = convert_custom_users_to_dict(self.customization.custom_users)
        
        ad_users_corp = get_realistic_ad_users(custom_users=custom_users_dict)
        
        # Base OUs for corp.local
        ad_ous_corp = [
            {"name": "Workstations", "path": "DC=corp,DC=local", "description": "Organizational unit for all workstations"},
            {"name": "Servers", "path": "DC=corp,DC=local", "description": "Organizational unit for all servers"},
        ]
        
        # Base groups for corp.local
        ad_groups_corp = [
            {"name": "Domain Users", "scope": "global", "path": "DC=corp,DC=local", "description": "All domain users"},
            {"name": "Domain Admins", "scope": "global", "path": "DC=corp,DC=local", "description": "Domain administrators"},
        ]
        
        # Built-in groups
        # These groups already exist in AD (CN=Builtin,DC=corp,DC=local) and should NOT be created
        builtin_group_names = {"Power Users", "Backup Operators", "Remote Desktop Users"}
        
        # Dynamically create OUs and groups based on departments
        departments_found_corp = set()
        groups_needed_corp = set()
        
        for user in ad_users_corp:
            dept = user.get("department")
            if dept:
                departments_found_corp.add(dept)
            user_groups = user.get("groups", [])
            for group in user_groups:
                # Skip base groups and built-in groups
                if group not in ["Domain Users", "Domain Admins"] and group not in builtin_group_names:
                    groups_needed_corp.add(group)
        
        # Note: Built-in groups are NOT added to ad_groups_corp because they already exist in AD
        # Users can still be assigned to them even if they're not in the ad_groups_corp list
        
        # Add OUs and groups for departments
        for dept in sorted(departments_found_corp):
            ad_ous_corp.append({
                "name": dept,
                "path": "DC=corp,DC=local",
                "description": f"{dept} Department"
            })
            dept_group_name = f"{dept} Department"
            if not any(g["name"] == dept_group_name for g in ad_groups_corp):
                ad_groups_corp.append({
                    "name": dept_group_name,
                    "scope": "global",
                    "path": f"OU={dept},DC=corp,DC=local",
                    "description": f"{dept} Department members"
                })
        
        # Add ALL other groups that users are assigned to (manager groups, executive, etc.)
        for group_name in groups_needed_corp:
            # Skip if already added (department groups or base groups)
            if not any(g["name"] == group_name for g in ad_groups_corp):
                # Determine OU path based on group name
                group_path = "DC=corp,DC=local"  # Default
                if "Managers" in group_name:
                    # Extract department from group name (e.g., "HR Managers" -> "HR")
                    dept = group_name.replace(" Managers", "").replace("Managers", "").strip()
                    if dept in departments_found_corp:
                        group_path = f"OU={dept},DC=corp,DC=local"
                elif group_name == "Executive":
                    # Executive group goes to Executive OU if it exists
                    if "Executive" in departments_found_corp:
                        group_path = "OU=Executive,DC=corp,DC=local"
                
                ad_groups_corp.append({
                    "name": group_name,
                    "scope": "global",
                    "path": group_path,
                    "description": f"{group_name} group"
                })
        
        # Ensure default departments for advanced (IT, HR, FINANCE, LEGAL, SALES)
        default_departments = ["IT", "HR", "Finance", "Legal", "Sales"]
        for dept in default_departments:
            if dept not in departments_found_corp:
                ad_ous_corp.append({
                    "name": dept,
                    "path": "DC=corp,DC=local",
                    "description": f"{dept} Department"
                })
                dept_group_name = f"{dept} Department"
                if not any(g["name"] == dept_group_name for g in ad_groups_corp):
                    ad_groups_corp.append({
                        "name": dept_group_name,
                        "scope": "global",
                        "path": f"OU={dept},DC=corp,DC=local",
                        "description": f"{dept} Department members"
                    })
        
        # Convert users to ludus-ad-content format
        ludus_ad_users_corp = []
        for user in ad_users_corp:
            ludus_ad_users_corp.append({
                "name": user["username"],
                "firstname": user.get("display_name", "").split()[0] if user.get("display_name") else "",
                "surname": user.get("display_name", "").split()[-1] if user.get("display_name") else "",
                "display_name": user.get("display_name", user["username"]),
                "password": user["password"],
                "path": f"OU={user['department']},DC=corp,DC=local" if user.get("department") else "DC=corp,DC=local",
                "description": user.get("description", ""),
                "groups": user.get("groups", []),
            })

        # Primary Domain Controller with realistic AD configuration
        dc_ram, dc_cpus = self.get_resources("dc")
        self.add_vm(
            vm_name=f"{range_id}-parent-dc-win2022-server-x64",
            hostname=f"{range_id}-DC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=10,
            ram_gb=dc_ram,
            cpus=dc_cpus,
            windows={"sysprep": False},
            domain={"fqdn": "corp.local", "role": "primary-dc"},
            ansible_roles=[
                {
                    "name": "ludus-ad-content",
                    "vars": {
                        "ludus_ad": {
                            "ous": ad_ous_corp,
                            "groups": ad_groups_corp,
                            "users": ludus_ad_users_corp,
                        }
                    }
                },
                # Note: ludus.enhanced_logging role is optional - remove if not installed
                # {
                #     "name": "ludus.enhanced_logging",
                #     "vars": {
                #         "audit_policy": "comprehensive",
                #         "log_retention_days": 180,
                #     },
                # },
            ],
        )
        
        # AD CS Server for certificate-based attack detection
        self.add_vm(
            vm_name=f"{range_id}-adcs-win2022-server-x64",
            hostname=f"{range_id}-ADCS01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=12,
            ram_gb=6,
            cpus=2,
            windows={},
            domain={"fqdn": "corp.local", "role": "member"},
            ansible_roles=[
                {
                    "name": "badsectorlabs.ludus_adcs",  # Correct Ludus role from docs
                    "vars": {
                        "ad_cs_config": get_ad_cs_config(
                            vulnerability_config=(
                                {
                                    "esc1_enabled": self.customization.vulnerability_config.esc1_enabled,
                                    "esc2_enabled": self.customization.vulnerability_config.esc2_enabled,
                                    "esc3_enabled": self.customization.vulnerability_config.esc3_enabled,
                                    "esc4_enabled": self.customization.vulnerability_config.esc4_enabled,
                                    "esc6_enabled": self.customization.vulnerability_config.esc6_enabled,
                                    "esc7_enabled": self.customization.vulnerability_config.esc7_enabled,
                                    "esc8_enabled": self.customization.vulnerability_config.esc8_enabled,
                                }
                                if self.customization and self.customization.vulnerability_config
                                else None
                            )
                        ),
                        "ca_name": "CORP-CA",
                        "ca_type": "Enterprise Root CA",
                    },
                },
            ],
        )

        # File Server
        self.add_vm(
            vm_name=f"{range_id}-fileserver-win2022-server-x64",
            hostname=f"{range_id}-FILES01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=20,
            ram_gb=6,
            cpus=2,
            windows={},
            domain={"fqdn": "corp.local", "role": "member"},
        )

        # SQL Server with service account
        sql_ram, sql_cpus = self.get_resources("sql_server")
        self.add_vm(
            vm_name=f"{range_id}-sql-win2022-server-x64",
            hostname=f"{range_id}-SQL01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=25,
            ram_gb=sql_ram,
            cpus=sql_cpus,
            windows={},
            domain={"fqdn": "corp.local", "role": "member"},
            ansible_roles=[
                {
                    "name": "badsectorlabs.ludus_mssql",  # Correct Ludus role from docs
                    "vars": {
                        "sql_service_account": "svc_sql",
                        "sql_install": True,
                    },
                },
            ],
        )

        # Exchange Server with service account
        exch_ram, exch_cpus = self.get_resources("exchange_server")
        self.add_vm(
            vm_name=f"{range_id}-exchange-win2022-server-x64",
            hostname=f"{range_id}-EXCH01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=30,
            ram_gb=exch_ram,
            cpus=exch_cpus,
            windows={},
            domain={"fqdn": "corp.local", "role": "member"},
            ansible_roles=[
                {
                    "name": "aleemladha.ludus_exchange",  # Correct Ludus role from docs
                    "vars": {
                        "exchange_service_account": "svc_exchange",
                        "exchange_install": True,
                    },
                },
            ],
        )

        # Workstations (various departments)
        departments = ["IT", "HR", "FINANCE", "LEGAL", "SALES"]
        for i, dept in enumerate(departments, start=1):
            self.add_vm(
                vm_name=f"{range_id}-{dept.lower()}-ws-win11",
                hostname=f"{range_id}-{dept}-WS01",
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=40 + i,
                ram_gb=4,
                cpus=2,
                windows={
                    "chocolatey_packages": ["googlechrome", "notepadplusplus"],
                    "chocolatey_ignore_checksums": True,
                },
                domain={"fqdn": "corp.local", "role": "member"},
            )

        # Branch Network (VLAN 20) - Remote office monitoring
        # Prepare AD role variables for ludus-ad-content (branch.corp.local forest)
        # Use a subset of users for branch domain
        ad_users_branch = get_realistic_ad_users(custom_users=None)  # Use default users for branch
        
        # Base OUs for branch.corp.local
        ad_ous_branch = [
            {"name": "Workstations", "path": "DC=branch,DC=corp,DC=local", "description": "Organizational unit for all workstations"},
            {"name": "Servers", "path": "DC=branch,DC=corp,DC=local", "description": "Organizational unit for all servers"},
        ]
        
        # Base groups for branch.corp.local
        ad_groups_branch = [
            {"name": "Domain Users", "scope": "global", "path": "DC=branch,DC=corp,DC=local", "description": "All domain users"},
            {"name": "Domain Admins", "scope": "global", "path": "DC=branch,DC=corp,DC=local", "description": "Domain administrators"},
        ]
        
        # Built-in groups for branch
        # These groups already exist in AD (CN=Builtin,DC=branch,DC=corp,DC=local) and should NOT be created
        builtin_group_names_branch = {"Power Users", "Backup Operators", "Remote Desktop Users"}
        
        # Collect departments and groups for branch
        departments_found_branch = set()
        groups_needed_branch = set()
        
        for user in ad_users_branch:
            dept = user.get("department")
            if dept:
                departments_found_branch.add(dept)
            user_groups = user.get("groups", [])
            for group in user_groups:
                # Skip base groups and built-in groups
                if group not in ["Domain Users", "Domain Admins"] and group not in builtin_group_names_branch:
                    groups_needed_branch.add(group)
        
        # Note: Built-in groups are NOT added to ad_groups_branch because they already exist in AD
        # Users can still be assigned to them even if they're not in the ad_groups_branch list
        
        # Add OUs and groups for branch departments
        for dept in sorted(departments_found_branch):
            ad_ous_branch.append({
                "name": dept,
                "path": "DC=branch,DC=corp,DC=local",
                "description": f"{dept} Department"
            })
            dept_group_name = f"{dept} Department"
            if not any(g["name"] == dept_group_name for g in ad_groups_branch):
                ad_groups_branch.append({
                    "name": dept_group_name,
                    "scope": "global",
                    "path": f"OU={dept},DC=branch,DC=corp,DC=local",
                    "description": f"{dept} Department members"
                })
        
        # Add ALL other groups that users are assigned to (manager groups, executive, etc.)
        for group_name in groups_needed_branch:
            # Skip if already added (department groups or base groups)
            if not any(g["name"] == group_name for g in ad_groups_branch):
                # Determine OU path based on group name
                group_path = "DC=branch,DC=corp,DC=local"  # Default
                if "Managers" in group_name:
                    # Extract department from group name (e.g., "HR Managers" -> "HR")
                    dept = group_name.replace(" Managers", "").replace("Managers", "").strip()
                    if dept in departments_found_branch:
                        group_path = f"OU={dept},DC=branch,DC=corp,DC=local"
                elif group_name == "Executive":
                    # Executive group goes to Executive OU if it exists
                    if "Executive" in departments_found_branch:
                        group_path = "OU=Executive,DC=branch,DC=corp,DC=local"
                
                ad_groups_branch.append({
                    "name": group_name,
                    "scope": "global",
                    "path": group_path,
                    "description": f"{group_name} group"
                })
        
        # Convert users to ludus-ad-content format for branch
        ludus_ad_users_branch = []
        for user in ad_users_branch:
            ludus_ad_users_branch.append({
                "name": user["username"],
                "firstname": user.get("display_name", "").split()[0] if user.get("display_name") else "",
                "surname": user.get("display_name", "").split()[-1] if user.get("display_name") else "",
                "display_name": user.get("display_name", user["username"]),
                "password": user["password"],
                "path": f"OU={user['department']},DC=branch,DC=corp,DC=local" if user.get("department") else "DC=branch,DC=corp,DC=local",
                "description": user.get("description", ""),
                "groups": user.get("groups", []),
            })

        # Branch Domain Controller with realistic AD configuration
        self.add_vm(
            vm_name=f"{range_id}-branch-dc-win2022-server-x64",
            hostname=f"{range_id}-BRANCH-DC01",
            template="win2022-server-x64-template",
            vlan=20,
            ip_last_octet=10,
            ram_gb=dc_ram,
            cpus=dc_cpus,
            windows={"sysprep": False},
            domain={"fqdn": "branch.corp.local", "role": "primary-dc"},
            ansible_roles=[
                {
                    "name": "ludus-ad-content",
                    "vars": {
                        "ludus_ad": {
                            "ous": ad_ous_branch,
                            "groups": ad_groups_branch,
                            "users": ludus_ad_users_branch,
                        }
                    }
                },
                # Note: ludus.enhanced_logging role is optional - remove if not installed
                # {
                #     "name": "ludus.enhanced_logging",
                #     "vars": {
                #         "audit_policy": "comprehensive",
                #         "log_retention_days": 180,
                #     },
                # },
            ],
        )

        # Branch workstations
        # Workstations - check for VM customization
        workstation_count = 2  # Default
        if self.customization and self.customization.vm_customization:
            vm_custom = self.customization.vm_customization
            if "workstation" in vm_custom.vm_count_overrides:
                workstation_count = vm_custom.vm_count_overrides["workstation"]
        
        for i in range(1, workstation_count + 1):
            self.add_vm(
                vm_name=f"{range_id}-branch-ws{i}-win11",
                hostname=f"{range_id}-BRANCH-WS{i:02d}",
                template="win11-22h2-x64-enterprise-template",
                vlan=20,
                ip_last_octet=20 + i,
                ram_gb=4,
                cpus=2,
                windows={
                    "chocolatey_packages": ["googlechrome"],
                    "chocolatey_ignore_checksums": True,
                },
                domain={"fqdn": "branch.corp.local", "role": "member"},
            )

        # Honeypot Network (VLAN 99) - Deception technology
        # Honeypot server (mimics high-value target)
        self.add_vm(
            vm_name=f"{range_id}-honeypot-win2022-server-x64",
            hostname=f"{range_id}-HONEYPOT01",
            template="win2022-server-x64-template",
            vlan=99,
            ip_last_octet=10,
            ram_gb=4,
            cpus=2,
            windows={"sysprep": False},
        )

        # Network Rules - Security monitoring can see all traffic
        # SOC can reach all networks (monitoring)
        for vlan in [10, 20, 99]:
            self.add_network_rule(
                f"Allow SOC to monitor VLAN {vlan}",
                vlan_src=5,
                vlan_dst=vlan,
                protocol="all",
                ports="all",
                action="ACCEPT",
            )
            self.add_network_rule(
                f"Allow VLAN {vlan} to SOC (log shipping)",
                vlan_src=vlan,
                vlan_dst=5,
                protocol="all",
                ports="all",
                action="ACCEPT",
            )

        # Corporate can reach branch
        self.add_network_rule(
            "Allow corporate to branch",
            vlan_src=10,
            vlan_dst=20,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )

        self.add_network_rule(
            "Allow branch to corporate",
            vlan_src=20,
            vlan_dst=10,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )

        # Honeypot isolation (can only be accessed, not initiate connections)
        self.add_network_rule(
            "Allow corporate to honeypot",
            vlan_src=10,
            vlan_dst=99,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )

        # Add SIEM agents to all VMs
        self.add_siem_agents_to_all_vms()
        
        # Enhance Wazuh with OPSEC detection rules
        if self.siem_type == "wazuh":
            for vm in self.config["ludus"]:
                if "wazuh" in vm.get("vm_name", "").lower() and "server" in vm.get("vm_name", "").lower():
                    if "ansible_roles" not in vm:
                        vm["ansible_roles"] = []
                    vm["ansible_roles"].append({
                        "name": "ludus.wazuh_opsec",
                        "vars": get_wazuh_opsec_ansible_vars(),
                    })
                    break
        
        # Add live action simulation for advanced blue team training
        # Simulates realistic attack patterns for detection training
        # Note: ludus.live_actions role is optional - uncomment if installed
        # for vm in self.config["ludus"]:
        #     if "dc" in vm.get("vm_name", "").lower() and "parent" in vm.get("vm_name", "").lower():
        #         if "ansible_roles" not in vm:
        #             vm["ansible_roles"] = []
        #         vm["ansible_roles"].append({
        #             "name": "ludus.live_actions",
        #             "vars": get_live_action_config(
        #                 simulation_enabled=True,
        #                 simulation_interval=900,  # Run every 15 minutes
        #                 simulation_intensity="high",
        #                 randomize_timing=True,
        #             ),
        #         })
        #         break

        return self
