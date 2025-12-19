"""Wireless security testing scenarios - WiFi pentesting and security assessment."""

from .base import BaseScenarioBuilder


class WirelessScenarioBuilder(BaseScenarioBuilder):
    """Builder for wireless security testing scenarios."""

    def build_wireless_lab(self) -> "WirelessScenarioBuilder":
        """Build wireless security testing lab with WiFiChallengeLab.

        Realistic scenario: Comprehensive WiFi security testing environment
        - Kali Linux attack platform with wireless tools
        - WiFiChallengeLab Docker environment (https://github.com/r4ulcl/WiFiChallengeLab-docker)
        - Multiple WiFi security challenges and scenarios

        WiFiChallengeLab features:
        - WEP cracking challenges
        - WPA/WPA2 cracking (PSK)
        - WPA3 testing scenarios
        - WPS attacks
        - Evil Twin attacks
        - Captive portal testing
        - Rogue AP detection
        - Client isolation testing
        - PMKID attacks
        - Deauth attacks

        Wireless testing activities:
        - WiFi reconnaissance and mapping
        - Encryption cracking (WEP/WPA/WPA2)
        - WPS attacks and exploitation
        - Evil Twin and rogue AP creation
        - Client attack scenarios
        - Wireless packet capture analysis
        - WiFi password auditing
        - Enterprise WiFi testing (WPA2-Enterprise)
        - Wireless intrusion detection
        - WiFi security assessment

        Resource requirements: 16GB RAM, 8 CPUs

        Note: This lab requires USB WiFi adapter passthrough for real wireless testing.
        The WiFiChallengeLab Docker container provides simulated WiFi environments
        for training without requiring physical wireless hardware.
        """
        range_id = self.range_id

        # Kali Linux - Wireless Attack Platform
        self.add_vm(
            vm_name=f"{range_id}-wireless-kali",
            hostname=f"{range_id}-WIFI-KALI",
            template="kali-x64-desktop-template",
            vlan=80,
            ip_last_octet=10,
            ram_gb=8,
            cpus=4,
            linux=True,
            testing={"snapshot": False, "block_internet": False},
        )

        # Debian 12/13 - WiFiChallengeLab Docker Host
        self.add_vm(
            vm_name=f"{range_id}-wifichallenge-debian",
            hostname=f"{range_id}-WIFI-LAB",
            template="debian-12-x64-server-template",
            vlan=80,
            ip_last_octet=20,
            ram_gb=8,
            cpus=4,
            linux=True,
            ansible_roles=[
                {
                    "name": "ludus.docker",
                    "vars": {
                        "docker_install": True,
                        "docker_compose_install": True,
                    },
                },
                {
                    "name": "ludus.wifichallenge",
                    "vars": {
                        "wifichallenge_docker_repo": "https://github.com/r4ulcl/WiFiChallengeLab-docker.git",
                        "wifichallenge_docker_dir": "/opt/wifichallenge",
                        "wifichallenge_auto_start": True,
                        # WiFiChallengeLab configuration
                        "wifichallenge_scenarios": [
                            "wep_cracking",
                            "wpa2_psk",
                            "wps_attacks",
                            "evil_twin",
                            "pmkid",
                        ],
                    },
                },
            ],
        )

        # Network rules - allow wireless testing traffic
        self.add_network_rule(
            "Allow Kali to WiFiChallenge Lab",
            vlan_src=80,
            vlan_dst=80,
            protocol="all",
            ports="all",
            action="ACCEPT",
        )

        return self
