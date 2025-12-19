"""Purple team collaborative security scenarios - red and blue teams working together."""

from .base import BaseScenarioBuilder


class PurpleTeamScenarioBuilder(BaseScenarioBuilder):
    """Builder for purple team collaborative security scenarios."""

    def build_purpleteam_lab_lite(self) -> "PurpleTeamScenarioBuilder":
        """Build lite purple team lab - Small collaborative exercise.

        Realistic scenario: Small purple team engagement
        - Blue team: Basic detection infrastructure
        - Red team: Offensive operations
        - Collaborative testing of detection capabilities

        Purple team activities:
        - Detection rule validation
        - Attack simulation and detection
        - SIEM alert testing
        - Gap analysis
        - Control effectiveness testing

        Resource requirements: 48GB RAM, 20 CPUs
        """
        range_id = self.range_id
        
        # Blue Team - Domain Controller with monitoring
        self.add_vm(
            vm_name=f"{range_id}-blue-dc-win2022-server-x64",
            hostname=f"{range_id}-BLUE-DC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=11,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "ludus.domain", "role": "primary-dc"},
        )
        
        # Blue Team - SIEM/Security Monitoring
        self.add_vm(
            vm_name=f"{range_id}-blue-siem-ubuntu22",
            hostname=f"{range_id}-BLUE-SIEM",
            template="ubuntu-22.04-x64-server-template",
            vlan=10,
            ip_last_octet=20,
            ram_gb=8,
            cpus=4,
            linux=True,
        )
        
        # Blue Team - Workstations
        for i in range(1, 3):
            self.add_vm(
                vm_name=f"{range_id}-blue-workstation-{i}-win11",
                hostname=f"{range_id}-BLUE-WS{i:02d}",
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=30 + i,
                ram_gb=8,
                cpus=4,
                domain={"fqdn": "ludus.domain", "role": "member"},
            )
        
        # Red Team - Attacker
        self.add_vm(
            vm_name=f"{range_id}-red-kali",
            hostname=f"{range_id}-RED-KALI",
            template="kali-x64-desktop-template",
            vlan=99,
            ip_last_octet=1,
            ram_gb=8,
            cpus=4,
            linux=True,
            testing={"snapshot": False, "block_internet": False},
        )
        
        # Red Team - C2 Server
        self.add_vm(
            vm_name=f"{range_id}-red-c2-ubuntu22",
            hostname=f"{range_id}-RED-C2",
            template="ubuntu-22.04-x64-server-template",
            vlan=99,
            ip_last_octet=2,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Network rules - Red can attack blue
        self.add_network_rule(
            "Allow red team to blue team",
            vlan_src=99,
            vlan_dst=10,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )
        
        # Blue team can monitor but not attack back
        self.add_network_rule(
            "Allow blue team monitoring to red",
            vlan_src=10,
            vlan_dst=99,
            protocol="tcp",
            ports="all",  # Monitoring ports (all for multiple)
            action="ACCEPT",
        )
        
        return self

    def build_purpleteam_lab_intermediate(self) -> "PurpleTeamScenarioBuilder":
        """Build intermediate purple team lab - Medium collaborative exercise with EDR.

        Realistic scenario: Medium-scale purple team engagement
        - Blue team: SIEM + EDR + multiple endpoints
        - Red team: Multi-stage attack capabilities
        - Advanced detection testing

        Purple team activities:
        - EDR rule development and testing
        - Advanced threat simulation
        - Detection engineering validation
        - Incident response testing
        - Control gap identification
        - Purple team playbook development
        - Attack path validation

        Resource requirements: 72GB RAM, 32 CPUs
        """
        range_id = self.range_id
        
        # Blue Team - Domain Controller
        self.add_vm(
            vm_name=f"{range_id}-blue-dc-win2022-server-x64",
            hostname=f"{range_id}-BLUE-DC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=11,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "ludus.domain", "role": "primary-dc"},
        )
        
        # Blue Team - SIEM/Log Aggregation
        self.add_vm(
            vm_name=f"{range_id}-blue-siem-ubuntu22",
            hostname=f"{range_id}-BLUE-SIEM",
            template="ubuntu-22.04-x64-server-template",
            vlan=10,
            ip_last_octet=20,
            ram_gb=16,
            cpus=4,
            linux=True,
        )
        
        # Blue Team - EDR Server
        self.add_vm(
            vm_name=f"{range_id}-blue-edr-ubuntu22",
            hostname=f"{range_id}-BLUE-EDR",
            template="ubuntu-22.04-x64-server-template",
            vlan=10,
            ip_last_octet=21,
            ram_gb=8,
            cpus=4,
            linux=True,
        )
        
        # Blue Team - File Server (high-value target)
        self.add_vm(
            vm_name=f"{range_id}-blue-fileserver-win2022-server-x64",
            hostname=f"{range_id}-BLUE-FILESERVER",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=30,
            ram_gb=8,
            cpus=4,
            domain={"fqdn": "ludus.domain", "role": "member"},
        )
        
        # Blue Team - Workstations (with EDR agents)
        for i in range(1, 4):
            self.add_vm(
                vm_name=f"{range_id}-blue-workstation-{i}-win11",
                hostname=f"{range_id}-BLUE-WS{i:02d}",
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=40 + i,
                ram_gb=8,
                cpus=4,
                domain={"fqdn": "ludus.domain", "role": "member"},
            )
        
        # Red Team - Primary Attacker
        self.add_vm(
            vm_name=f"{range_id}-red-kali",
            hostname=f"{range_id}-RED-KALI",
            template="kali-x64-desktop-template",
            vlan=99,
            ip_last_octet=1,
            ram_gb=8,
            cpus=4,
            linux=True,
        )
        
        # Red Team - C2 Server
        self.add_vm(
            vm_name=f"{range_id}-red-c2-ubuntu22",
            hostname=f"{range_id}-RED-C2",
            template="ubuntu-22.04-x64-server-template",
            vlan=99,
            ip_last_octet=2,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Red Team - Pivot Host (compromised)
        self.add_vm(
            vm_name=f"{range_id}-red-pivot-ubuntu22",
            hostname=f"{range_id}-RED-PIVOT",
            template="ubuntu-22.04-x64-server-template",
            vlan=99,
            ip_last_octet=3,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Network rules
        self.add_network_rule(
            "Allow red team to blue team",
            vlan_src=99,
            vlan_dst=10,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )
        
        # Blue team monitoring
        self.add_network_rule(
            "Allow blue team monitoring",
            vlan_src=10,
            vlan_dst=99,
            protocol="tcp",
            ports="all",  # HTTP, HTTPS, monitoring, syslog (all for multiple)
            action="ACCEPT",
        )
        
        return self

    def build_purpleteam_lab_advanced(self) -> "PurpleTeamScenarioBuilder":
        """Build advanced purple team lab - Enterprise-scale collaborative exercise.

        Realistic scenario: Large-scale purple team engagement
        - Blue team: Full SOC stack (SIEM, EDR, IDS/IPS, Forensics)
        - Red team: Complete adversary emulation
        - Multi-layer network with DMZ and internal zones
        - Comprehensive attack and defense testing

        Purple team activities:
        - Enterprise detection engineering
        - Adversary emulation based on real threats
        - Full kill chain validation
        - Detection maturity assessment
        - Control effectiveness measurement
        - Purple team framework implementation
        - Automated detection testing
        - Threat modeling validation
        - Security control optimization

        Resource requirements: 120GB RAM, 52 CPUs
        """
        range_id = self.range_id
        
        # Blue Team Infrastructure
        # DC
        self.add_vm(
            vm_name=f"{range_id}-blue-dc-win2022-server-x64",
            hostname=f"{range_id}-BLUE-DC01",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=11,
            ram_gb=8,
            cpus=4,
            windows={"sysprep": False},
            domain={"fqdn": "ludus.domain", "role": "primary-dc"},
        )
        
        # SIEM
        self.add_vm(
            vm_name=f"{range_id}-blue-siem-ubuntu22",
            hostname=f"{range_id}-BLUE-SIEM",
            template="ubuntu-22.04-x64-server-template",
            vlan=10,
            ip_last_octet=20,
            ram_gb=16,
            cpus=4,
            linux=True,
        )
        
        # EDR Management
        self.add_vm(
            vm_name=f"{range_id}-blue-edr-win2022-server-x64",
            hostname=f"{range_id}-BLUE-EDR-MGMT",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=21,
            ram_gb=8,
            cpus=4,
            domain={"fqdn": "ludus.domain", "role": "member"},
        )
        
        # Web Server (DMZ)
        self.add_vm(
            vm_name=f"{range_id}-blue-web-ubuntu22",
            hostname=f"{range_id}-BLUE-WEB",
            template="ubuntu-22.04-x64-server-template",
            vlan=20,
            ip_last_octet=10,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Database Server
        self.add_vm(
            vm_name=f"{range_id}-blue-db-ubuntu22",
            hostname=f"{range_id}-BLUE-DB",
            template="ubuntu-22.04-x64-server-template",
            vlan=10,
            ip_last_octet=30,
            ram_gb=8,
            cpus=2,
            linux=True,
        )
        
        # File Server
        self.add_vm(
            vm_name=f"{range_id}-blue-fileserver-win2022-server-x64",
            hostname=f"{range_id}-BLUE-FILESERVER",
            template="win2022-server-x64-template",
            vlan=10,
            ip_last_octet=31,
            ram_gb=8,
            cpus=4,
            domain={"fqdn": "ludus.domain", "role": "member"},
        )
        
        # Blue Team Workstations
        for i in range(1, 5):
            self.add_vm(
                vm_name=f"{range_id}-blue-workstation-{i}-win11",
                hostname=f"{range_id}-BLUE-WS{i:02d}",
                template="win11-22h2-x64-enterprise-template",
                vlan=10,
                ip_last_octet=40 + i,
                ram_gb=8,
                cpus=4,
                domain={"fqdn": "ludus.domain", "role": "member"},
            )
        
        # Red Team Infrastructure
        # Primary Attacker
        self.add_vm(
            vm_name=f"{range_id}-red-kali",
            hostname=f"{range_id}-RED-KALI",
            template="kali-x64-desktop-template",
            vlan=99,
            ip_last_octet=1,
            ram_gb=8,
            cpus=4,
            linux=True,
        )
        
        # C2 Server
        self.add_vm(
            vm_name=f"{range_id}-red-c2-ubuntu22",
            hostname=f"{range_id}-RED-C2",
            template="ubuntu-22.04-x64-server-template",
            vlan=99,
            ip_last_octet=2,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Red Team Pivot Host
        self.add_vm(
            vm_name=f"{range_id}-red-pivot-ubuntu22",
            hostname=f"{range_id}-RED-PIVOT",
            template="ubuntu-22.04-x64-server-template",
            vlan=99,
            ip_last_octet=3,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Network rules - Red can attack
        self.add_network_rule(
            "Allow red to DMZ",
            vlan_src=99,
            vlan_dst=20,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )
        
        self.add_network_rule(
            "Allow red to internal",
            vlan_src=99,
            vlan_dst=10,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )
        
        # Blue team monitoring
        self.add_network_rule(
            "Allow blue monitoring to red",
            vlan_src=10,
            vlan_dst=99,
            protocol="tcp",
            ports="all",  # HTTP, HTTPS, monitoring, syslog, C2 (all for multiple)
            action="ACCEPT",
        )
        
        self.add_network_rule(
            "Allow DMZ to internal DB",
            vlan_src=20,
            vlan_dst=10,
            protocol="tcp",
            ports=3306,  # MySQL
            action="ACCEPT",
        )
        
        return self

