"""Network penetration testing scenarios."""

from .base import BaseScenarioBuilder


class NetworkScenarioBuilder(BaseScenarioBuilder):
    """Builder for network penetration testing scenarios."""

    def build_network_segmentation_lab(self) -> "NetworkScenarioBuilder":
        """Build multi-segment network for testing segmentation bypass."""
        range_id = self.range_id
        
        # DMZ Network (VLAN 10)
        self.add_vm(
            vm_name=f"{range_id}-dmz-web-ubuntu22",
            hostname=f"{range_id}-dmz-web",
            template="ubuntu-22.04-x64-server-template",
            vlan=10,
            ip_last_octet=10,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Internal Network (VLAN 20)
        self.add_vm(
            vm_name=f"{range_id}-internal-db-ubuntu22",
            hostname=f"{range_id}-internal-db",
            template="ubuntu-22.04-x64-server-template",
            vlan=20,
            ip_last_octet=10,
            ram_gb=8,
            cpus=2,
            linux=True,
        )
        
        self.add_vm(
            vm_name=f"{range_id}-internal-file-ubuntu22",
            hostname=f"{range_id}-internal-file",
            template="ubuntu-22.04-x64-server-template",
            vlan=20,
            ip_last_octet=11,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Management Network (VLAN 30)
        self.add_vm(
            vm_name=f"{range_id}-mgmt-admin-ubuntu22",
            hostname=f"{range_id}-mgmt-admin",
            template="ubuntu-22.04-x64-server-template",
            vlan=30,
            ip_last_octet=10,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Attacker (VLAN 99)
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
        
        # Network rules - Test segmentation bypass
        self.add_network_rule(
            "Allow kali to DMZ",
            vlan_src=99,
            vlan_dst=10,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )
        
        # DMZ can reach internal on specific ports
        self.add_network_rule(
            "Allow DMZ to internal DB",
            vlan_src=10,
            vlan_dst=20,
            protocol="tcp",
            ports=3306,  # MySQL
            action="ACCEPT",
        )
        
        # Internal can reach management
        self.add_network_rule(
            "Allow internal to management",
            vlan_src=20,
            vlan_dst=30,
            protocol="tcp",
            ports=22,  # SSH
            action="ACCEPT",
        )
        
        # SIEM Server for detection tracking
        self.add_siem_server(vlan=10, ip_last_octet=100)
        
        # Add SIEM agents to all VMs
        self.add_siem_agents_to_all_vms()
        
        return self

    def build_wireless_lab(self) -> "NetworkScenarioBuilder":
        """Build wireless security testing lab."""
        range_id = self.range_id
        
        # Access Point (simulated)
        self.add_vm(
            vm_name=f"{range_id}-ap-ubuntu22",
            hostname=f"{range_id}-ap",
            template="ubuntu-22.04-x64-server-template",
            vlan=50,
            ip_last_octet=1,
            ram_gb=4,
            cpus=2,
            linux=True,
        )
        
        # Client devices
        for i in range(1, 4):
            self.add_vm(
                vm_name=f"{range_id}-client-{i}-ubuntu22",
                hostname=f"{range_id}-client-{i}",
                template="ubuntu-22.04-x64-server-template",
                vlan=50,
                ip_last_octet=10 + i,
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
        
        # Network rules
        self.add_network_rule(
            "Allow kali to wireless network",
            vlan_src=99,
            vlan_dst=50,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )
        
        # SIEM Server for detection tracking
        self.add_siem_server(vlan=50, ip_last_octet=100)

        # Add SIEM agents to all VMs
        self.add_siem_agents_to_all_vms()

        return self

