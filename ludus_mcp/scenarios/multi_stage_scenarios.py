"""Multi-stage attack path scenarios for red team exercises."""

from .base import BaseScenarioBuilder


class MultiStageScenarioBuilder(BaseScenarioBuilder):
    """Builder for multi-stage attack path scenarios."""

    def build_kerberoasting_scenario(self) -> "MultiStageScenarioBuilder":
        """Build scenario for Kerberoasting attack path."""
        range_id = self.range_id
        
        # Domain Controller
        self.add_vm(
            vm_name=f"{range_id}-dc-win2022-server-x64",
            hostname=f"{range_id}-DC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=11,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "ludus.domain", "role": "primary-dc"},
        )
        
        # SQL Server with SPN (Kerberoastable)
        self.add_vm(
            vm_name=f"{range_id}-sql-win2022-server-x64",
            hostname=f"{range_id}-SQL01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=12,
            ram_gb=16,
            cpus=4,
            domain={"fqdn": "ludus.domain", "role": "member"},
        )
        
        # Workstation (initial foothold)
        self.add_vm(
            vm_name=f"{range_id}-workstation-win11",
            hostname=f"{range_id}-WORKSTATION01",
            template="win11-22h2-x64-enterprise-template",
            vlan=10,
            ip_last_octet=21,
            ram_gb=8,
            cpus=4,
            domain={"fqdn": "ludus.domain", "role": "member"},
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
            "Allow kali to domain",
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

    def build_golden_ticket_scenario(self) -> "MultiStageScenarioBuilder":
        """Build scenario for Golden Ticket attack path."""
        range_id = self.range_id
        
        # Primary DC
        self.add_vm(
            vm_name=f"{range_id}-pdc-win2022-server-x64",
            hostname=f"{range_id}-PDC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=11,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "ludus.domain", "role": "primary-dc"},
        )
        
        # Backup DC
        self.add_vm(
            vm_name=f"{range_id}-bdc-win2022-server-x64",
            hostname=f"{range_id}-BDC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=12,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "ludus.domain", "role": "primary-dc"},
        )
        
        # High-value targets
        for i, target in enumerate(["fileserver", "sqlserver", "exchange"], start=1):
            self.add_vm(
                vm_name=f"{range_id}-{target}-win2022-server-x64",
                hostname=f"{range_id}-{target.upper()}01",
                template="win2022-server-x64-template",
                vlan=10,
                ip_last_octet=20 + i,
                ram_gb=8,
                cpus=4,
                windows={"sysprep": False},
                domain={"fqdn": "ludus.domain", "role": "member"},
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
            "Allow kali to domain",
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

    def build_lateral_movement_scenario(self) -> "MultiStageScenarioBuilder":
        """Build scenario for lateral movement techniques."""
        range_id = self.range_id
        
        # Domain Controller
        self.add_vm(
            vm_name=f"{range_id}-dc-win2022-server-x64",
            hostname=f"{range_id}-DC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=11,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "ludus.domain", "role": "primary-dc"},
        )
        
        # Initial foothold (compromised workstation)
        self.add_vm(
            vm_name=f"{range_id}-compromised-win11",
            hostname=f"{range_id}-COMPROMISED01",
            template="win11-22h2-x64-enterprise-template",
            vlan=10,
            ip_last_octet=21,
            ram_gb=8,
            cpus=4,
            domain={"fqdn": "ludus.domain", "role": "member"},
        )
        
        # Lateral movement targets
        targets = [
            ("fileserver", 22),
            ("sqlserver", 23),
            ("webserver", 24),
            ("admin-workstation", 25),
        ]
        
        for target, octet in targets:
            self.add_vm(
                vm_name=f"{range_id}-{target}-win11",
                hostname=f"{range_id}-{target.upper().replace('-', '')}01",
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=octet,
                ram_gb=8,
                cpus=4,
                domain={"fqdn": "ludus.domain", "role": "member"},
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
            "Allow kali to domain",
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

    def build_red_team_exercise(self) -> "MultiStageScenarioBuilder":
        """Build comprehensive red team exercise scenario."""
        range_id = self.range_id
        
        # DMZ
        self.add_vm(
            vm_name=f"{range_id}-dmz-web-ubuntu22",
            hostname=f"{range_id}-DMZ-WEB",
            template="ubuntu-22.04-x64-server-template",
            vlan=10,
            ip_last_octet=10,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Internal Network - AD
        self.add_vm(
            vm_name=f"{range_id}-dc-win2022-server-x64",
            hostname=f"{range_id}-DC01",
            template="win2022-server-x64-template",
            vlan=20,
            ip_last_octet=11,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "ludus.domain", "role": "primary-dc"},
        )
        
        # Internal workstations
        for i in range(1, 4):
            self.add_vm(
                vm_name=f"{range_id}-workstation-{i}-win11",
                hostname=f"{range_id}-WORKSTATION{i:02d}",
                template="win11-22h2-x64-enterprise-template",
                vlan=20,
                ip_last_octet=20 + i,
                ram_gb=8,
                cpus=4,
                domain={"fqdn": "ludus.domain", "role": "member"},
            )
        
        # Internal servers
        self.add_vm(
            vm_name=f"{range_id}-fileserver-win2022-server-x64",
            hostname=f"{range_id}-FILESERVER01",
            template="win2022-server-x64-template",
            vlan=20,
            ip_last_octet=30,
            ram_gb=8,
            cpus=4,
            domain={"fqdn": "ludus.domain", "role": "member"},
        )
        
        # Management network
        self.add_vm(
            vm_name=f"{range_id}-mgmt-admin-ubuntu22",
            hostname=f"{range_id}-MGMT-ADMIN",
            template="ubuntu-22.04-x64-server-template",
            vlan=30,
            ip_last_octet=10,
            ram_gb=4,
            cpus=2,
            linux=True,
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
        
        # Network rules - Simulate real network segmentation
        self.add_network_rule(
            "Allow kali to DMZ",
            vlan_src=99,
            vlan_dst=10,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )
        
        self.add_network_rule(
            "Allow DMZ to internal web",
            vlan_src=10,
            vlan_dst=20,
            protocol="tcp",
            ports=80,
            action="ACCEPT",
        )
        
        self.add_network_rule(
            "Allow internal to management",
            vlan_src=20,
            vlan_dst=30,
            protocol="tcp",
            ports=22,
            action="ACCEPT",
        )
        
        # SIEM Server for detection tracking
        self.add_siem_server(vlan=10, ip_last_octet=100)
        
        # Add SIEM agents to all VMs
        self.add_siem_agents_to_all_vms()
        
        return self

