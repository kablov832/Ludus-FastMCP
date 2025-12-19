"""Active Directory red team scenarios."""

from .base import BaseScenarioBuilder


class ADScenarioBuilder(BaseScenarioBuilder):
    """Builder for Active Directory red team scenarios."""

    def build_basic_ad_lab(self) -> "ADScenarioBuilder":
        """Build a basic AD lab with DC and workstations."""
        range_id = self.range_id
        
        # Domain Controller
        self.add_vm(
            vm_name=f"{range_id}-ad-dc-win2022-server-x64",
            hostname=f"{range_id}-DC01",  # Shortened to avoid Windows 15-char limit
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=11,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "ludus.domain", "role": "primary-dc"},
        )
        
        # Windows 11 Workstations
        for i in range(1, 3):
            self.add_vm(
                vm_name=f"{range_id}-ad-win11-22h2-enterprise-x64-{i}",
                hostname=f"{range_id}-WS{i}",  # Shortened to avoid Windows 15-char limit
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=20 + i,
                ram_gb=8,
                cpus=4,
                windows={
                    "chocolatey_packages": ["vscodium", "googlechrome"],
                    "chocolatey_ignore_checksums": True,
                    "office_version": 2021,
                    "office_arch": "64bit",
                },
                domain={"fqdn": "ludus.domain", "role": "member"},
                # Note: sysprep will run automatically for domain members (ensures unique SIDs)
            )
        
        # Attacker (Kali)
        self.add_vm(
            vm_name=f"{range_id}-kali",
            hostname=f"{range_id}-kali",
            template="kali-x64-desktop-template",
            vlan=99,
            ip_last_octet=1,
            ram_gb=8,
            cpus=4,
            linux=True,
            testing={"snapshot": False, "block_internet": False},
        )
        
        # Network rules - Allow attacker to reach domain
        self.add_network_rule(
            "Allow kali to all windows",
            vlan_src=99,
            vlan_dst=10,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )
        
        # Allow domain to reach kali on specific ports
        for port in [80, 443, 8080]:
            self.add_network_rule(
                f"Allow windows to kali on {port}",
                vlan_src=10,
                vlan_dst=99,
                protocol="tcp",
                ports=port,
                action="ACCEPT",
            )
        
        # SIEM Server for detection tracking
        self.add_siem_server(vlan=10, ip_last_octet=100)
        
        # Add SIEM agents to all VMs (except SIEM server itself)
        self.add_siem_agents_to_all_vms()
        
        return self

    def build_ad_with_file_server(self) -> "ADScenarioBuilder":
        """Build AD lab with file server for lateral movement."""
        self.build_basic_ad_lab()
        range_id = self.range_id
        
        # File Server
        self.add_vm(
            vm_name=f"{range_id}-fileserver-win2019-server-x64",
            hostname=f"{range_id}-FILESERVER-2019",
            template="win2019-server-x64-template",
            vlan=10,
            ip_last_octet=15,
            ram_gb=8,
            cpus=4,
            domain={"fqdn": "ludus.domain", "role": "member"},
        )
        
        # Ensure SIEM agents are on all VMs
        self.add_siem_agents_to_all_vms()
        
        return self

    def build_ad_with_sql_server(self) -> "ADScenarioBuilder":
        """Build AD lab with SQL Server for credential theft."""
        self.build_basic_ad_lab()
        range_id = self.range_id
        
        # SQL Server
        self.add_vm(
            vm_name=f"{range_id}-sqlserver-win2022-server-x64",
            hostname=f"{range_id}-SQL01",  # Shortened to avoid Windows 15-char limit
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=12,
            ram_gb=16,
            cpus=4,
            domain={"fqdn": "ludus.domain", "role": "member"},
        )
        
        # Ensure SIEM agents are on all VMs
        self.add_siem_agents_to_all_vms()
        
        return self

    def build_ad_forest(self) -> "ADScenarioBuilder":
        """Build multi-domain AD forest for advanced attacks."""
        range_id = self.range_id
        
        # Root Domain Controller
        self.add_vm(
            vm_name=f"{range_id}-root-dc-win2022-server-x64",
            hostname=f"{range_id}-ROOTDC01",  # Shortened to avoid Windows 15-char limit
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=11,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "root.ludus.domain", "role": "primary-dc"},
        )
        
        # Child Domain Controller
        self.add_vm(
            vm_name=f"{range_id}-child-dc-win2022-server-x64",
            hostname=f"{range_id}-CHILDDC01",  # Shortened to avoid Windows 15-char limit
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=12,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "child.root.ludus.domain", "role": "primary-dc"},
        )
        
        # Workstations in root domain
        for i in range(1, 3):
            self.add_vm(
                vm_name=f"{range_id}-root-win11-{i}",
                hostname=f"{range_id}-ROOT-WS{i}",  # Shortened to avoid Windows 15-char limit
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=20 + i,
                ram_gb=8,
                cpus=4,
                domain={"fqdn": "root.ludus.domain", "role": "member"},
            )
        
        # Workstations in child domain
        for i in range(1, 3):
            self.add_vm(
                vm_name=f"{range_id}-child-win11-{i}",
                hostname=f"{range_id}-CHILD-WS{i}",  # Shortened to avoid Windows 15-char limit
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=30 + i,
                ram_gb=8,
                cpus=4,
                domain={"fqdn": "child.root.ludus.domain", "role": "member"},
            )
        
        # Attacker
        self.add_vm(
            vm_name=f"{range_id}-kali",
            hostname=f"{range_id}-kali",
            template="kali-x64-desktop-template",
            vlan=99,
            ip_last_octet=1,
            ram_gb=8,
            cpus=4,
            linux=True,
        )
        
        # Network rules
        self.add_network_rule(
            "Allow kali to all windows",
            vlan_src=99,
            vlan_dst=10,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )
        
        # SIEM Server for detection tracking
        self.add_siem_server(vlan=10, ip_last_octet=100)
        
        # Add SIEM agents to all VMs
        self.add_siem_agents_to_all_vms()
        
        return self

