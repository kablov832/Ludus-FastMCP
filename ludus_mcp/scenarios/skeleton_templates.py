"""Skeleton templates for building Ludus ranges and VMs.

This module provides ready-to-use skeleton configurations that users can
customize for their specific needs. These templates serve as starting points
for common security lab scenarios.
"""

from typing import Any


# =============================================================================
# VM SKELETON TEMPLATES
# =============================================================================

class VMSkeletons:
    """Pre-configured VM skeletons for common use cases."""

    # -------------------------------------------------------------------------
    # Windows Domain Controllers
    # -------------------------------------------------------------------------

    DOMAIN_CONTROLLER_2022 = {
        "hostname": "dc01",
        "template": "win2022-server-x64-template",
        "vlan": 10,
        "ip_last_octet": 10,
        "ram_gb": 4,
        "cpus": 2,
        "windows": {
            "sysprep": True,
        },
        "domain": {
            "fqdn": "yourcompany.local",
            "role": "primary_dc",
        },
        "testing": {
            "snapshot": True,
            "snapshot_mode": "dvd",
        },
    }

    DOMAIN_CONTROLLER_2019 = {
        "hostname": "dc01",
        "template": "win2019-server-x64-template",
        "vlan": 10,
        "ip_last_octet": 10,
        "ram_gb": 4,
        "cpus": 2,
        "windows": {
            "sysprep": True,
        },
        "domain": {
            "fqdn": "yourcompany.local",
            "role": "primary_dc",
        },
    }

    SECONDARY_DC = {
        "hostname": "dc02",
        "template": "win2022-server-x64-template",
        "vlan": 10,
        "ip_last_octet": 11,
        "ram_gb": 4,
        "cpus": 2,
        "windows": {
            "sysprep": True,
        },
        "domain": {
            "fqdn": "yourcompany.local",
            "role": "secondary_dc",
        },
    }

    # -------------------------------------------------------------------------
    # Windows Workstations
    # -------------------------------------------------------------------------

    WINDOWS_11_WORKSTATION = {
        "hostname": "ws01",
        "template": "win11-22h2-x64-enterprise-template",
        "vlan": 10,
        "ip_last_octet": 21,
        "ram_gb": 4,
        "cpus": 2,
        "windows": {
            "sysprep": True,
        },
        "domain": {
            "fqdn": "yourcompany.local",
            "role": "member",
        },
    }

    WINDOWS_10_WORKSTATION = {
        "hostname": "ws01",
        "template": "win10-21h2-x64-enterprise-template",
        "vlan": 10,
        "ip_last_octet": 21,
        "ram_gb": 4,
        "cpus": 2,
        "windows": {
            "sysprep": True,
        },
        "domain": {
            "fqdn": "yourcompany.local",
            "role": "member",
        },
    }

    # -------------------------------------------------------------------------
    # Windows Servers
    # -------------------------------------------------------------------------

    FILE_SERVER = {
        "hostname": "fs01",
        "template": "win2022-server-x64-template",
        "vlan": 10,
        "ip_last_octet": 30,
        "ram_gb": 4,
        "cpus": 2,
        "windows": {
            "sysprep": True,
        },
        "domain": {
            "fqdn": "yourcompany.local",
            "role": "member",
        },
        "roles_to_install": ["FileServer"],
    }

    SQL_SERVER = {
        "hostname": "sql01",
        "template": "win2022-server-x64-template",
        "vlan": 10,
        "ip_last_octet": 31,
        "ram_gb": 8,
        "cpus": 4,
        "windows": {
            "sysprep": True,
        },
        "domain": {
            "fqdn": "yourcompany.local",
            "role": "member",
        },
        "roles_to_install": ["SQLServer"],
    }

    EXCHANGE_SERVER = {
        "hostname": "ex01",
        "template": "win2022-server-x64-template",
        "vlan": 10,
        "ip_last_octet": 32,
        "ram_gb": 16,
        "cpus": 4,
        "windows": {
            "sysprep": True,
        },
        "domain": {
            "fqdn": "yourcompany.local",
            "role": "member",
        },
        "roles_to_install": ["Exchange"],
    }

    WEB_SERVER_IIS = {
        "hostname": "web01",
        "template": "win2022-server-x64-template",
        "vlan": 20,
        "ip_last_octet": 40,
        "ram_gb": 4,
        "cpus": 2,
        "windows": {
            "sysprep": True,
        },
        "roles_to_install": ["WebServer"],
    }

    CERTIFICATE_AUTHORITY = {
        "hostname": "ca01",
        "template": "win2022-server-x64-template",
        "vlan": 10,
        "ip_last_octet": 15,
        "ram_gb": 4,
        "cpus": 2,
        "windows": {
            "sysprep": True,
        },
        "domain": {
            "fqdn": "yourcompany.local",
            "role": "member",
        },
        "roles_to_install": ["CertificateAuthority"],
    }

    # -------------------------------------------------------------------------
    # Linux Servers
    # -------------------------------------------------------------------------

    UBUNTU_SERVER = {
        "hostname": "ubuntu01",
        "template": "ubuntu-22.04-x64-server-template",
        "vlan": 20,
        "ip_last_octet": 50,
        "ram_gb": 2,
        "cpus": 2,
    }

    DEBIAN_SERVER = {
        "hostname": "debian01",
        "template": "debian-12-x64-server-template",
        "vlan": 20,
        "ip_last_octet": 51,
        "ram_gb": 2,
        "cpus": 2,
    }

    ROCKY_LINUX_SERVER = {
        "hostname": "rocky01",
        "template": "rocky-9-x64-server-template",
        "vlan": 20,
        "ip_last_octet": 52,
        "ram_gb": 2,
        "cpus": 2,
    }

    DOCKER_HOST = {
        "hostname": "docker01",
        "template": "ubuntu-22.04-x64-server-template",
        "vlan": 20,
        "ip_last_octet": 60,
        "ram_gb": 8,
        "cpus": 4,
        "linux": {
            "packages": ["docker.io", "docker-compose"],
        },
    }

    # -------------------------------------------------------------------------
    # Attacker VMs
    # -------------------------------------------------------------------------

    KALI_ATTACKER = {
        "hostname": "kali",
        "template": "kali-2024.1-x64-template",
        "vlan": 99,
        "ip_last_octet": 100,
        "ram_gb": 8,
        "cpus": 4,
        "linux": {
            "packages": [
                "seclists",
                "wordlists",
                "impacket-scripts",
                "crackmapexec",
                "bloodhound",
                "neo4j",
            ],
        },
    }

    PARROT_ATTACKER = {
        "hostname": "parrot",
        "template": "parrot-security-x64-template",
        "vlan": 99,
        "ip_last_octet": 101,
        "ram_gb": 8,
        "cpus": 4,
    }

    COMMANDO_VM = {
        "hostname": "commando",
        "template": "win10-21h2-x64-enterprise-template",
        "vlan": 99,
        "ip_last_octet": 102,
        "ram_gb": 8,
        "cpus": 4,
        "notes": "Install Commando VM tools post-deployment",
    }

    # -------------------------------------------------------------------------
    # SIEM / Monitoring
    # -------------------------------------------------------------------------

    WAZUH_SERVER = {
        "hostname": "wazuh",
        "template": "ubuntu-22.04-x64-server-template",
        "vlan": 10,
        "ip_last_octet": 5,
        "ram_gb": 8,
        "cpus": 4,
        "linux": {
            "packages": ["curl", "wget", "gnupg2"],
        },
        "containers": [
            {
                "name": "wazuh",
                "image": "wazuh/wazuh-manager:4.7.2",
                "ports": ["1514:1514", "1515:1515", "514:514/udp", "55000:55000"],
            },
        ],
        "notes": "Wazuh Manager - agents should be installed on monitored hosts",
    }

    SPLUNK_SERVER = {
        "hostname": "splunk",
        "template": "ubuntu-22.04-x64-server-template",
        "vlan": 10,
        "ip_last_octet": 6,
        "ram_gb": 8,
        "cpus": 4,
        "containers": [
            {
                "name": "splunk",
                "image": "splunk/splunk:latest",
                "ports": ["8000:8000", "8089:8089", "9997:9997"],
                "environment": {
                    "SPLUNK_START_ARGS": "--accept-license",
                    "SPLUNK_PASSWORD": "changeme123!",
                },
            },
        ],
    }

    ELASTIC_SIEM = {
        "hostname": "elastic",
        "template": "ubuntu-22.04-x64-server-template",
        "vlan": 10,
        "ip_last_octet": 7,
        "ram_gb": 16,
        "cpus": 4,
        "containers": [
            {
                "name": "elasticsearch",
                "image": "docker.elastic.co/elasticsearch/elasticsearch:8.12.0",
                "ports": ["9200:9200"],
                "environment": {
                    "discovery.type": "single-node",
                    "xpack.security.enabled": "false",
                },
            },
            {
                "name": "kibana",
                "image": "docker.elastic.co/kibana/kibana:8.12.0",
                "ports": ["5601:5601"],
            },
        ],
    }

    SECURITY_ONION = {
        "hostname": "securityonion",
        "template": "ubuntu-22.04-x64-server-template",
        "vlan": 10,
        "ip_last_octet": 8,
        "ram_gb": 16,
        "cpus": 4,
        "notes": "Security Onion requires manual installation - download ISO from securityonionsolutions.com",
    }

    # -------------------------------------------------------------------------
    # Vulnerable Apps for Testing
    # -------------------------------------------------------------------------

    DVWA_SERVER = {
        "hostname": "dvwa",
        "template": "ubuntu-22.04-x64-server-template",
        "vlan": 30,
        "ip_last_octet": 70,
        "ram_gb": 2,
        "cpus": 2,
        "containers": [
            {
                "name": "dvwa",
                "image": "vulnerables/web-dvwa:latest",
                "ports": ["80:80"],
            },
        ],
        "notes": "Damn Vulnerable Web Application - default creds: admin/password",
    }

    JUICE_SHOP = {
        "hostname": "juiceshop",
        "template": "ubuntu-22.04-x64-server-template",
        "vlan": 30,
        "ip_last_octet": 71,
        "ram_gb": 2,
        "cpus": 2,
        "containers": [
            {
                "name": "juice-shop",
                "image": "bkimminich/juice-shop:latest",
                "ports": ["3000:3000"],
            },
        ],
        "notes": "OWASP Juice Shop - intentionally insecure web app",
    }

    METASPLOITABLE = {
        "hostname": "metasploitable",
        "template": "metasploitable-2-template",
        "vlan": 30,
        "ip_last_octet": 72,
        "ram_gb": 1,
        "cpus": 1,
        "notes": "Metasploitable 2 - intentionally vulnerable Linux",
    }

    VULNHUB_BASE = {
        "hostname": "vulnbox",
        "template": "custom-vulnhub-template",
        "vlan": 30,
        "ip_last_octet": 73,
        "ram_gb": 2,
        "cpus": 2,
        "notes": "Placeholder for VulnHub VM - import OVA manually",
    }

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    @classmethod
    def get_skeleton(cls, name: str) -> dict[str, Any]:
        """Get a VM skeleton by name."""
        skeletons = {
            # Domain Controllers
            "dc-2022": cls.DOMAIN_CONTROLLER_2022,
            "dc-2019": cls.DOMAIN_CONTROLLER_2019,
            "secondary-dc": cls.SECONDARY_DC,
            # Workstations
            "ws-win11": cls.WINDOWS_11_WORKSTATION,
            "ws-win10": cls.WINDOWS_10_WORKSTATION,
            # Windows Servers
            "file-server": cls.FILE_SERVER,
            "sql-server": cls.SQL_SERVER,
            "exchange": cls.EXCHANGE_SERVER,
            "web-iis": cls.WEB_SERVER_IIS,
            "ca": cls.CERTIFICATE_AUTHORITY,
            # Linux
            "ubuntu": cls.UBUNTU_SERVER,
            "debian": cls.DEBIAN_SERVER,
            "rocky": cls.ROCKY_LINUX_SERVER,
            "docker": cls.DOCKER_HOST,
            # Attackers
            "kali": cls.KALI_ATTACKER,
            "parrot": cls.PARROT_ATTACKER,
            "commando": cls.COMMANDO_VM,
            # SIEM
            "wazuh": cls.WAZUH_SERVER,
            "splunk": cls.SPLUNK_SERVER,
            "elastic": cls.ELASTIC_SIEM,
            "security-onion": cls.SECURITY_ONION,
            # Vulnerable
            "dvwa": cls.DVWA_SERVER,
            "juice-shop": cls.JUICE_SHOP,
            "metasploitable": cls.METASPLOITABLE,
            "vulnhub": cls.VULNHUB_BASE,
        }
        if name not in skeletons:
            raise ValueError(f"Unknown skeleton: {name}. Available: {', '.join(skeletons.keys())}")
        return skeletons[name].copy()

    @classmethod
    def list_skeletons(cls) -> dict[str, str]:
        """List all available VM skeletons."""
        return {
            # Domain Controllers
            "dc-2022": "Windows Server 2022 Domain Controller",
            "dc-2019": "Windows Server 2019 Domain Controller",
            "secondary-dc": "Secondary/Replica Domain Controller",
            # Workstations
            "ws-win11": "Windows 11 Enterprise Workstation",
            "ws-win10": "Windows 10 Enterprise Workstation",
            # Windows Servers
            "file-server": "Windows File Server with shares",
            "sql-server": "SQL Server (8GB RAM recommended)",
            "exchange": "Exchange Server (16GB RAM recommended)",
            "web-iis": "IIS Web Server",
            "ca": "Active Directory Certificate Services",
            # Linux
            "ubuntu": "Ubuntu 22.04 Server",
            "debian": "Debian 12 Server",
            "rocky": "Rocky Linux 9 Server",
            "docker": "Docker Host (Ubuntu with Docker installed)",
            # Attackers
            "kali": "Kali Linux with common tools",
            "parrot": "Parrot Security OS",
            "commando": "Windows base for Commando VM",
            # SIEM
            "wazuh": "Wazuh SIEM Manager",
            "splunk": "Splunk Enterprise",
            "elastic": "Elastic Stack (Elasticsearch + Kibana)",
            "security-onion": "Security Onion (manual install required)",
            # Vulnerable
            "dvwa": "Damn Vulnerable Web Application",
            "juice-shop": "OWASP Juice Shop",
            "metasploitable": "Metasploitable 2",
            "vulnhub": "VulnHub VM placeholder",
        }


# =============================================================================
# RANGE SKELETON TEMPLATES
# =============================================================================

class RangeSkeletons:
    """Complete range configurations for common scenarios."""

    # -------------------------------------------------------------------------
    # Active Directory Labs
    # -------------------------------------------------------------------------

    @staticmethod
    def basic_ad_lab(
        domain: str = "yourcompany.local",
        workstations: int = 2,
        include_attacker: bool = True,
        include_siem: bool = True,
        siem_type: str = "wazuh",
    ) -> dict[str, Any]:
        """
        Basic Active Directory lab for learning AD attacks and defense.

        Components:
        - 1 Domain Controller (Windows Server 2022)
        - N Windows workstations (configurable)
        - Optional: Kali attacker
        - Optional: SIEM (Wazuh/Splunk/Elastic)
        """
        config = {
            "ludus": [
                {
                    "vm_name": "{{ range_id }}-dc01",
                    "hostname": "dc01",
                    "template": "win2022-server-x64-template",
                    "vlan": 10,
                    "ip_last_octet": 10,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "primary_dc"},
                },
            ],
            "network_rules": [],
        }

        # Add workstations
        for i in range(1, workstations + 1):
            config["ludus"].append({
                "vm_name": f"{{{{ range_id }}}}-ws{i:02d}",
                "hostname": f"ws{i:02d}",
                "template": "win11-22h2-x64-enterprise-template",
                "vlan": 10,
                "ip_last_octet": 20 + i,
                "ram_gb": 4,
                "cpus": 2,
                "windows": {"sysprep": True},
                "domain": {"fqdn": domain, "role": "member"},
            })

        # Add SIEM
        if include_siem:
            siem_configs = {
                "wazuh": VMSkeletons.WAZUH_SERVER,
                "splunk": VMSkeletons.SPLUNK_SERVER,
                "elastic": VMSkeletons.ELASTIC_SIEM,
            }
            if siem_type in siem_configs:
                siem = siem_configs[siem_type].copy()
                siem["vm_name"] = f"{{{{ range_id }}}}-{siem_type}"
                config["ludus"].append(siem)

        # Add attacker
        if include_attacker:
            attacker = VMSkeletons.KALI_ATTACKER.copy()
            attacker["vm_name"] = "{{ range_id }}-kali"
            config["ludus"].append(attacker)

            # Add network rule for attacker access
            config["network_rules"].append({
                "name": "attacker-to-domain",
                "vlan_src": 99,
                "vlan_dst": 10,
                "protocol": "all",
                "action": "accept",
            })

        return config

    @staticmethod
    def enterprise_ad_lab(
        domain: str = "yourcompany.local",
        child_domain: str | None = None,
    ) -> dict[str, Any]:
        """
        Enterprise Active Directory lab with multiple tiers.

        Components:
        - 2 Domain Controllers (primary + replica)
        - Certificate Authority (AD CS)
        - File Server
        - SQL Server
        - Exchange Server (optional)
        - 5 Workstations (mix of Win10/Win11)
        - Wazuh SIEM
        - Kali attacker

        Great for practicing:
        - Kerberoasting, AS-REP roasting
        - AD CS attacks (ESC1-ESC8)
        - Lateral movement
        - Privilege escalation
        """
        config = {
            "ludus": [
                # Primary DC
                {
                    "vm_name": "{{ range_id }}-dc01",
                    "hostname": "dc01",
                    "template": "win2022-server-x64-template",
                    "vlan": 10,
                    "ip_last_octet": 10,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "primary_dc"},
                },
                # Replica DC
                {
                    "vm_name": "{{ range_id }}-dc02",
                    "hostname": "dc02",
                    "template": "win2022-server-x64-template",
                    "vlan": 10,
                    "ip_last_octet": 11,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "secondary_dc"},
                },
                # Certificate Authority
                {
                    "vm_name": "{{ range_id }}-ca01",
                    "hostname": "ca01",
                    "template": "win2022-server-x64-template",
                    "vlan": 10,
                    "ip_last_octet": 15,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "member"},
                    "notes": "Enterprise CA - configure vulnerable templates for AD CS attacks",
                },
                # File Server
                {
                    "vm_name": "{{ range_id }}-fs01",
                    "hostname": "fs01",
                    "template": "win2022-server-x64-template",
                    "vlan": 10,
                    "ip_last_octet": 30,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "member"},
                },
                # SQL Server
                {
                    "vm_name": "{{ range_id }}-sql01",
                    "hostname": "sql01",
                    "template": "win2022-server-x64-template",
                    "vlan": 10,
                    "ip_last_octet": 31,
                    "ram_gb": 8,
                    "cpus": 4,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "member"},
                },
                # Workstations
                {
                    "vm_name": "{{ range_id }}-ws01",
                    "hostname": "ws01",
                    "template": "win11-22h2-x64-enterprise-template",
                    "vlan": 10,
                    "ip_last_octet": 21,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "member"},
                },
                {
                    "vm_name": "{{ range_id }}-ws02",
                    "hostname": "ws02",
                    "template": "win11-22h2-x64-enterprise-template",
                    "vlan": 10,
                    "ip_last_octet": 22,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "member"},
                },
                {
                    "vm_name": "{{ range_id }}-ws03",
                    "hostname": "ws03",
                    "template": "win10-21h2-x64-enterprise-template",
                    "vlan": 10,
                    "ip_last_octet": 23,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "member"},
                },
                {
                    "vm_name": "{{ range_id }}-ws04",
                    "hostname": "ws04",
                    "template": "win10-21h2-x64-enterprise-template",
                    "vlan": 10,
                    "ip_last_octet": 24,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "member"},
                },
                {
                    "vm_name": "{{ range_id }}-ws05",
                    "hostname": "ws05",
                    "template": "win11-22h2-x64-enterprise-template",
                    "vlan": 10,
                    "ip_last_octet": 25,
                    "ram_gb": 4,
                    "cpus": 2,
                    "windows": {"sysprep": True},
                    "domain": {"fqdn": domain, "role": "member"},
                },
                # SIEM
                {
                    "vm_name": "{{ range_id }}-wazuh",
                    "hostname": "wazuh",
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 10,
                    "ip_last_octet": 5,
                    "ram_gb": 8,
                    "cpus": 4,
                },
                # Attacker
                {
                    "vm_name": "{{ range_id }}-kali",
                    "hostname": "kali",
                    "template": "kali-2024.1-x64-template",
                    "vlan": 99,
                    "ip_last_octet": 100,
                    "ram_gb": 8,
                    "cpus": 4,
                },
            ],
            "network_rules": [
                {"name": "attacker-to-domain", "vlan_src": 99, "vlan_dst": 10, "protocol": "all", "action": "accept"},
            ],
        }

        return config

    # -------------------------------------------------------------------------
    # Red Team Labs
    # -------------------------------------------------------------------------

    @staticmethod
    def red_team_training_lab() -> dict[str, Any]:
        """
        Red team training environment.

        Components:
        - Full AD environment with DC, workstations, servers
        - Web application tier (DMZ)
        - Kali attacker with common tools
        - Network segmentation for realistic attack paths

        Scenarios:
        - External to internal pivot
        - Phishing simulation
        - Lateral movement
        - Privilege escalation
        - Data exfiltration
        """
        return {
            "ludus": [
                # DMZ - External facing
                {
                    "vm_name": "{{ range_id }}-web01",
                    "hostname": "web01",
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 20,
                    "ip_last_octet": 10,
                    "ram_gb": 2,
                    "cpus": 2,
                    "notes": "Web server in DMZ - entry point for attackers",
                },
                # Internal - AD
                {
                    "vm_name": "{{ range_id }}-dc01",
                    "hostname": "dc01",
                    "template": "win2022-server-x64-template",
                    "vlan": 10,
                    "ip_last_octet": 10,
                    "ram_gb": 4,
                    "cpus": 2,
                    "domain": {"fqdn": "corp.local", "role": "primary_dc"},
                },
                {
                    "vm_name": "{{ range_id }}-ws01",
                    "hostname": "ws01",
                    "template": "win11-22h2-x64-enterprise-template",
                    "vlan": 10,
                    "ip_last_octet": 21,
                    "ram_gb": 4,
                    "cpus": 2,
                    "domain": {"fqdn": "corp.local", "role": "member"},
                },
                {
                    "vm_name": "{{ range_id }}-ws02",
                    "hostname": "ws02",
                    "template": "win10-21h2-x64-enterprise-template",
                    "vlan": 10,
                    "ip_last_octet": 22,
                    "ram_gb": 4,
                    "cpus": 2,
                    "domain": {"fqdn": "corp.local", "role": "member"},
                },
                # Attacker
                {
                    "vm_name": "{{ range_id }}-kali",
                    "hostname": "kali",
                    "template": "kali-2024.1-x64-template",
                    "vlan": 99,
                    "ip_last_octet": 100,
                    "ram_gb": 8,
                    "cpus": 4,
                },
            ],
            "network_rules": [
                {"name": "attacker-to-dmz", "vlan_src": 99, "vlan_dst": 20, "protocol": "all", "action": "accept"},
                {"name": "dmz-to-internal", "vlan_src": 20, "vlan_dst": 10, "protocol": "tcp", "ports": "445,3389", "action": "accept"},
            ],
        }

    # -------------------------------------------------------------------------
    # Blue Team / SOC Labs
    # -------------------------------------------------------------------------

    @staticmethod
    def soc_training_lab(siem_type: str = "wazuh") -> dict[str, Any]:
        """
        SOC analyst training environment.

        Components:
        - Multiple endpoints to monitor
        - SIEM with agents installed
        - Attacker VM to generate alerts

        Training focus:
        - Alert triage
        - Log analysis
        - Incident response
        - Threat hunting
        """
        return {
            "ludus": [
                # Monitored endpoints
                {
                    "vm_name": "{{ range_id }}-win-srv",
                    "hostname": "win-srv",
                    "template": "win2022-server-x64-template",
                    "vlan": 10,
                    "ip_last_octet": 20,
                    "ram_gb": 4,
                    "cpus": 2,
                    "notes": "Windows Server - monitored endpoint",
                },
                {
                    "vm_name": "{{ range_id }}-win-ws",
                    "hostname": "win-ws",
                    "template": "win11-22h2-x64-enterprise-template",
                    "vlan": 10,
                    "ip_last_octet": 21,
                    "ram_gb": 4,
                    "cpus": 2,
                    "notes": "Windows Workstation - monitored endpoint",
                },
                {
                    "vm_name": "{{ range_id }}-linux-srv",
                    "hostname": "linux-srv",
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 10,
                    "ip_last_octet": 30,
                    "ram_gb": 2,
                    "cpus": 2,
                    "notes": "Linux Server - monitored endpoint",
                },
                # SIEM
                {
                    "vm_name": f"{{{{ range_id }}}}-{siem_type}",
                    "hostname": siem_type,
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 10,
                    "ip_last_octet": 5,
                    "ram_gb": 8,
                    "cpus": 4,
                    "notes": f"{siem_type.upper()} SIEM - collect and analyze logs",
                },
                # Attacker for generating alerts
                {
                    "vm_name": "{{ range_id }}-attacker",
                    "hostname": "attacker",
                    "template": "kali-2024.1-x64-template",
                    "vlan": 99,
                    "ip_last_octet": 100,
                    "ram_gb": 4,
                    "cpus": 2,
                    "notes": "Attacker VM - generate realistic attack traffic",
                },
            ],
            "network_rules": [
                {"name": "attacker-access", "vlan_src": 99, "vlan_dst": 10, "protocol": "all", "action": "accept"},
            ],
        }

    # -------------------------------------------------------------------------
    # Web Application Labs
    # -------------------------------------------------------------------------

    @staticmethod
    def web_pentest_lab() -> dict[str, Any]:
        """
        Web application penetration testing lab.

        Components:
        - Multiple vulnerable web apps (DVWA, Juice Shop, etc.)
        - Database server
        - Kali attacker

        Training focus:
        - OWASP Top 10
        - SQL injection
        - XSS
        - Authentication bypass
        """
        return {
            "ludus": [
                # Vulnerable web apps
                {
                    "vm_name": "{{ range_id }}-dvwa",
                    "hostname": "dvwa",
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 30,
                    "ip_last_octet": 70,
                    "ram_gb": 2,
                    "cpus": 2,
                    "notes": "DVWA - Damn Vulnerable Web Application",
                },
                {
                    "vm_name": "{{ range_id }}-juiceshop",
                    "hostname": "juiceshop",
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 30,
                    "ip_last_octet": 71,
                    "ram_gb": 2,
                    "cpus": 2,
                    "notes": "OWASP Juice Shop",
                },
                {
                    "vm_name": "{{ range_id }}-webgoat",
                    "hostname": "webgoat",
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 30,
                    "ip_last_octet": 72,
                    "ram_gb": 2,
                    "cpus": 2,
                    "notes": "OWASP WebGoat",
                },
                # Database
                {
                    "vm_name": "{{ range_id }}-db",
                    "hostname": "db",
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 30,
                    "ip_last_octet": 80,
                    "ram_gb": 2,
                    "cpus": 2,
                    "notes": "MySQL/PostgreSQL database",
                },
                # Attacker
                {
                    "vm_name": "{{ range_id }}-kali",
                    "hostname": "kali",
                    "template": "kali-2024.1-x64-template",
                    "vlan": 99,
                    "ip_last_octet": 100,
                    "ram_gb": 4,
                    "cpus": 2,
                },
            ],
            "network_rules": [
                {"name": "attacker-to-web", "vlan_src": 99, "vlan_dst": 30, "protocol": "all", "action": "accept"},
            ],
        }

    # -------------------------------------------------------------------------
    # Malware Analysis Labs
    # -------------------------------------------------------------------------

    @staticmethod
    def malware_analysis_lab() -> dict[str, Any]:
        """
        Malware analysis and reverse engineering lab.

        Components:
        - Windows analysis VM (isolated)
        - REMnux for Linux malware analysis
        - Network traffic analysis VM

        Training focus:
        - Static analysis
        - Dynamic analysis
        - Network traffic analysis
        - Behavioral analysis
        """
        return {
            "ludus": [
                # Windows analysis VM
                {
                    "vm_name": "{{ range_id }}-flare",
                    "hostname": "flare",
                    "template": "win10-21h2-x64-enterprise-template",
                    "vlan": 50,
                    "ip_last_octet": 10,
                    "ram_gb": 8,
                    "cpus": 4,
                    "notes": "FlareVM for Windows malware analysis - install FlareVM tools post-deploy",
                },
                # REMnux
                {
                    "vm_name": "{{ range_id }}-remnux",
                    "hostname": "remnux",
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 50,
                    "ip_last_octet": 20,
                    "ram_gb": 4,
                    "cpus": 2,
                    "notes": "REMnux for Linux malware analysis",
                },
                # Network monitor
                {
                    "vm_name": "{{ range_id }}-netmon",
                    "hostname": "netmon",
                    "template": "ubuntu-22.04-x64-server-template",
                    "vlan": 50,
                    "ip_last_octet": 5,
                    "ram_gb": 4,
                    "cpus": 2,
                    "notes": "Network traffic capture and analysis",
                },
            ],
            "network_rules": [
                # Isolated - no external access
                {"name": "block-external", "vlan_src": 50, "vlan_dst": 0, "protocol": "all", "action": "drop"},
            ],
        }

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    @classmethod
    def list_skeletons(cls) -> dict[str, str]:
        """List all available range skeletons."""
        return {
            "basic-ad": "Basic AD lab (1 DC, workstations, optional attacker/SIEM)",
            "enterprise-ad": "Enterprise AD with CA, servers, multiple workstations",
            "red-team": "Red team training with DMZ, AD, and segmentation",
            "soc-training": "SOC analyst training with SIEM and monitored endpoints",
            "web-pentest": "Web app pentest with DVWA, Juice Shop, WebGoat",
            "malware-analysis": "Isolated malware RE lab with FlareVM and REMnux",
        }

    @classmethod
    def get_skeleton(cls, name: str, **kwargs) -> dict[str, Any]:
        """Get a range skeleton by name with optional customizations."""
        skeletons = {
            "basic-ad": cls.basic_ad_lab,
            "enterprise-ad": cls.enterprise_ad_lab,
            "red-team": cls.red_team_training_lab,
            "soc-training": cls.soc_training_lab,
            "web-pentest": cls.web_pentest_lab,
            "malware-analysis": cls.malware_analysis_lab,
        }
        if name not in skeletons:
            raise ValueError(f"Unknown skeleton: {name}. Available: {', '.join(skeletons.keys())}")
        return skeletons[name](**kwargs)


# =============================================================================
# YAML EXAMPLE TEMPLATES
# =============================================================================

YAML_EXAMPLES = {
    "basic_ad": """# Basic Active Directory Lab
# Deploy: ludus range config set -f config.yml && ludus range deploy

ludus:
  - vm_name: "{{ range_id }}-dc01"
    hostname: "dc01"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 10
    ram_gb: 4
    cpus: 2
    windows:
      sysprep: true
    domain:
      fqdn: yourcompany.local
      role: primary_dc

  - vm_name: "{{ range_id }}-ws01"
    hostname: "ws01"
    template: win11-22h2-x64-enterprise-template
    vlan: 10
    ip_last_octet: 21
    ram_gb: 4
    cpus: 2
    windows:
      sysprep: true
    domain:
      fqdn: yourcompany.local
      role: member

  - vm_name: "{{ range_id }}-ws02"
    hostname: "ws02"
    template: win11-22h2-x64-enterprise-template
    vlan: 10
    ip_last_octet: 22
    ram_gb: 4
    cpus: 2
    windows:
      sysprep: true
    domain:
      fqdn: yourcompany.local
      role: member

  - vm_name: "{{ range_id }}-kali"
    hostname: "kali"
    template: kali-2024.1-x64-template
    vlan: 99
    ip_last_octet: 100
    ram_gb: 8
    cpus: 4
""",

    "with_siem": """# AD Lab with Wazuh SIEM
# Great for blue team training

ludus:
  - vm_name: "{{ range_id }}-dc01"
    hostname: "dc01"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 10
    ram_gb: 4
    cpus: 2
    windows:
      sysprep: true
    domain:
      fqdn: yourcompany.local
      role: primary_dc

  - vm_name: "{{ range_id }}-ws01"
    hostname: "ws01"
    template: win11-22h2-x64-enterprise-template
    vlan: 10
    ip_last_octet: 21
    ram_gb: 4
    cpus: 2
    windows:
      sysprep: true
    domain:
      fqdn: yourcompany.local
      role: member

  - vm_name: "{{ range_id }}-wazuh"
    hostname: "wazuh"
    template: ubuntu-22.04-x64-server-template
    vlan: 10
    ip_last_octet: 5
    ram_gb: 8
    cpus: 4
    linux:
      packages:
        - docker.io
        - docker-compose

  - vm_name: "{{ range_id }}-kali"
    hostname: "kali"
    template: kali-2024.1-x64-template
    vlan: 99
    ip_last_octet: 100
    ram_gb: 8
    cpus: 4

network_rules:
  - name: attacker-to-domain
    vlan_src: 99
    vlan_dst: 10
    protocol: all
    action: accept
""",

    "web_app_lab": """# Web Application Security Lab
# OWASP Top 10 training environment

ludus:
  - vm_name: "{{ range_id }}-webserver"
    hostname: "webserver"
    template: ubuntu-22.04-x64-server-template
    vlan: 20
    ip_last_octet: 10
    ram_gb: 4
    cpus: 2
    linux:
      packages:
        - docker.io
        - docker-compose
        - nginx
        - mysql-server

  - vm_name: "{{ range_id }}-dvwa"
    hostname: "dvwa"
    template: ubuntu-22.04-x64-server-template
    vlan: 20
    ip_last_octet: 70
    ram_gb: 2
    cpus: 2

  - vm_name: "{{ range_id }}-kali"
    hostname: "kali"
    template: kali-2024.1-x64-template
    vlan: 99
    ip_last_octet: 100
    ram_gb: 4
    cpus: 2
    linux:
      packages:
        - burpsuite
        - sqlmap
        - nikto
        - gobuster

network_rules:
  - name: attacker-to-web
    vlan_src: 99
    vlan_dst: 20
    protocol: all
    action: accept
""",
}


def get_yaml_example(name: str) -> str:
    """Get a YAML example by name."""
    if name not in YAML_EXAMPLES:
        raise ValueError(f"Unknown example: {name}. Available: {', '.join(YAML_EXAMPLES.keys())}")
    return YAML_EXAMPLES[name]


def list_yaml_examples() -> dict[str, str]:
    """List all available YAML examples."""
    return {
        "basic_ad": "Basic AD lab with DC, workstations, and attacker",
        "with_siem": "AD lab with Wazuh SIEM for blue team training",
        "web_app_lab": "Web application security testing lab",
    }


# =============================================================================
# ANSIBLE ROLE CONFIGURATIONS
# =============================================================================

class RoleConfigurations:
    """Pre-configured Ansible role sets for common scenarios."""

    # Galaxy roles (namespace.role_name format)
    GALAXY_ROLES = {
        # Ludus Official Roles
        "adcs": "badsectorlabs.ludus_adcs",
        "mssql": "badsectorlabs.ludus_mssql",
        "commandovm": "badsectorlabs.ludus_commandovm",
        "flarevm": "badsectorlabs.ludus_flarevm",
        "remnux": "badsectorlabs.ludus_remnux",
        "elastic_container": "badsectorlabs.ludus_elastic_container",
        "elastic_agent": "badsectorlabs.ludus_elastic_agent",
        # SIEM Roles
        "wazuh_server": "aleemladha.wazuh_server_install",
        "wazuh_agent": "aleemladha.ludus_wazuh_agent",
        # Infrastructure Roles
        "docker": "geerlingguy.docker",
        "nginx": "geerlingguy.nginx",
        "postgresql": "geerlingguy.postgresql",
        "redis": "geerlingguy.redis",
        "java": "geerlingguy.java",
        "nodejs": "geerlingguy.nodejs",
        # Security Hardening
        "os_hardening": "dev-sec.os-hardening",
        "ssh_hardening": "dev-sec.ssh-hardening",
    }

    # Directory-based roles (require cloning from GitHub)
    DIRECTORY_ROLES = {
        "ad_content": {
            "name": "ludus-ad-content",
            "url": "https://github.com/Cyblex-Consulting/ludus-ad-content",
            "description": "Creates AD structure (OUs, groups, users)",
        },
        "ad_vulns": {
            "name": "ludus-ad-vulns",
            "url": "https://github.com/Primusinterp/ludus-ad-vulns",
            "description": "Adds vulnerabilities to AD environment",
        },
        "child_domain": {
            "name": "ludus_child_domain",
            "url": "https://github.com/ChoiSG/ludus_ansible_roles",
            "description": "Child domain creation",
        },
        "badblood": {
            "name": "ludus_badblood",
            "url": "https://github.com/curi0usJack/ludus_badblood",
            "description": "BadBlood AD population",
        },
        "local_users": {
            "name": "ludus-local-users",
            "url": "https://github.com/Cyblex-Consulting/ludus-local-users",
            "description": "Local user creation",
        },
        "juiceshop": {
            "name": "ludus_juiceshop",
            "url": "https://github.com/xurger/ludus_juiceshop",
            "description": "OWASP Juice Shop deployment",
        },
        "graylog": {
            "name": "ludus_graylog_server",
            "url": "https://github.com/frack113/my-ludus-roles",
            "description": "Graylog SIEM server",
        },
        "opencti": {
            "name": "ludus_filigran_opencti",
            "url": "https://github.com/frack113/ludus_filigran_opencti",
            "description": "OpenCTI threat intelligence platform",
        },
        "guacamole": {
            "name": "ludus_guacamole",
            "url": "https://github.com/brmkit/ludus_guacamole",
            "description": "Apache Guacamole remote desktop gateway",
        },
    }

    # Role sets for common scenarios
    SCENARIO_ROLE_SETS = {
        "basic_ad": [
            GALAXY_ROLES["adcs"],  # Optional but common
        ],
        "enterprise_ad": [
            GALAXY_ROLES["adcs"],
            GALAXY_ROLES["mssql"],
        ],
        "red_team": [
            GALAXY_ROLES["adcs"],
        ],
        "soc_training": [
            GALAXY_ROLES["wazuh_server"],
            GALAXY_ROLES["wazuh_agent"],
        ],
        "web_pentest": [
            GALAXY_ROLES["docker"],
            GALAXY_ROLES["nginx"],
        ],
        "malware_analysis": [
            GALAXY_ROLES["flarevm"],
            GALAXY_ROLES["remnux"],
        ],
    }

    @classmethod
    def get_galaxy_role(cls, key: str) -> str:
        """Get a Galaxy role by short key."""
        if key not in cls.GALAXY_ROLES:
            raise ValueError(f"Unknown Galaxy role: {key}. Available: {', '.join(cls.GALAXY_ROLES.keys())}")
        return cls.GALAXY_ROLES[key]

    @classmethod
    def get_directory_role(cls, key: str) -> dict[str, str]:
        """Get a directory-based role by short key."""
        if key not in cls.DIRECTORY_ROLES:
            raise ValueError(f"Unknown directory role: {key}. Available: {', '.join(cls.DIRECTORY_ROLES.keys())}")
        return cls.DIRECTORY_ROLES[key]

    @classmethod
    def get_roles_for_scenario(cls, scenario: str) -> list[str]:
        """Get recommended roles for a scenario."""
        if scenario not in cls.SCENARIO_ROLE_SETS:
            return []
        return cls.SCENARIO_ROLE_SETS[scenario]

    @classmethod
    def list_all_roles(cls) -> dict[str, Any]:
        """List all available roles."""
        return {
            "galaxy_roles": cls.GALAXY_ROLES,
            "directory_roles": cls.DIRECTORY_ROLES,
            "scenario_sets": {k: v for k, v in cls.SCENARIO_ROLE_SETS.items()},
        }


def get_roles_for_vm(vm_type: str) -> list[str]:
    """Get recommended Ansible roles for a VM type.

    Args:
        vm_type: VM skeleton type (e.g., "dc-2022", "kali", "wazuh")

    Returns:
        List of recommended Ansible role names
    """
    role_mappings = {
        # Domain Controllers - AD roles
        "dc-2022": [],  # Base DC doesn't need extra roles
        "dc-2019": [],
        "secondary-dc": [],
        # Windows with AD CS
        "ca": [RoleConfigurations.GALAXY_ROLES["adcs"]],
        # SQL Server
        "sql-server": [RoleConfigurations.GALAXY_ROLES["mssql"]],
        # Attacker VMs
        "commando": [RoleConfigurations.GALAXY_ROLES["commandovm"]],
        # Malware Analysis
        "flare": [RoleConfigurations.GALAXY_ROLES["flarevm"]],
        "remnux": [RoleConfigurations.GALAXY_ROLES["remnux"]],
        # SIEM
        "wazuh": [RoleConfigurations.GALAXY_ROLES["wazuh_server"]],
        "elastic": [
            RoleConfigurations.GALAXY_ROLES["elastic_container"],
        ],
        # Docker host
        "docker": [RoleConfigurations.GALAXY_ROLES["docker"]],
    }
    return role_mappings.get(vm_type, [])
