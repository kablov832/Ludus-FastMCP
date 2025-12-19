"""Active Directory configuration for realistic red team scenarios.

This module provides realistic AD configurations including:
- Real user accounts with proper group memberships
- Service accounts with appropriate permissions
- Local admin accounts
- AD CS (Certificate Services) configuration
- OPSEC detection rules for SIEM integration
"""

from typing import Any
from ..schemas.scenario_customization import ADUserCustomization
from .randomizer import generate_random_users


def convert_custom_users_to_dict(users: list[ADUserCustomization]) -> list[dict[str, Any]]:
    """Convert ADUserCustomization objects to dictionary format.
    
    Args:
        users: List of ADUserCustomization objects
        
    Returns:
        List of user dictionaries in the format expected by get_realistic_ad_users()
    """
    result = []
    for user in users:
        user_dict = {
            "username": user.username,
            "display_name": user.display_name,
            "password": user.password,
            "groups": user.groups,
            "password_never_expires": user.password_never_expires,
            "account_disabled": user.account_disabled,
        }
        if user.department:
            user_dict["department"] = user.department
        if user.title:
            user_dict["title"] = user.title
        if user.description:
            user_dict["description"] = user.description
        if user.path:
            user_dict["path"] = user.path
        result.append(user_dict)
    return result


def get_realistic_ad_users(
    custom_users: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Get realistic AD user accounts for red team scenarios.
    
    Args:
        custom_users: Optional list of custom user dictionaries to use instead of defaults.
                      If provided, these users will be returned instead of the default set.
    
    Returns:
        List of user configurations with:
        - Realistic names and usernames
        - Department assignments
        - Group memberships
        - Password policies
        - Account status
    """
    if custom_users is not None:
        return custom_users
    
    return [
        # IT Department
        {
            "username": "john.smith",
            "display_name": "John Smith",
            "department": "IT",
            "title": "IT Administrator",
            "groups": ["Domain Users", "IT Department", "Remote Desktop Users"],
            "password": "Welcome123!",  # Weak password for red team exercises
            "password_never_expires": False,
            "account_disabled": False,
            "description": "IT Administrator - Local admin on IT workstations",
        },
        {
            "username": "sarah.johnson",
            "display_name": "Sarah Johnson",
            "department": "IT",
            "title": "Help Desk Technician",
            "groups": ["Domain Users", "IT Department"],
            "password": "Password123!",
            "password_never_expires": False,
            "account_disabled": False,
            "description": "Help desk staff - Limited privileges",
        },
        # HR Department
        {
            "username": "michael.brown",
            "display_name": "Michael Brown",
            "department": "HR",
            "title": "HR Manager",
            "groups": ["Domain Users", "HR Department", "HR Managers"],
            "password": "HR2024!",
            "password_never_expires": False,
            "account_disabled": False,
            "description": "HR Manager - Access to sensitive employee data",
        },
        {
            "username": "emily.davis",
            "display_name": "Emily Davis",
            "department": "HR",
            "title": "HR Assistant",
            "groups": ["Domain Users", "HR Department"],
            "password": "Welcome2024!",
            "password_never_expires": False,
            "account_disabled": False,
            "description": "HR Assistant - Standard user privileges",
        },
        # Finance Department
        {
            "username": "david.wilson",
            "display_name": "David Wilson",
            "department": "Finance",
            "title": "Finance Director",
            "groups": ["Domain Users", "Finance Department", "Finance Managers"],
            "password": "Finance2024!",
            "password_never_expires": False,
            "account_disabled": False,
            "description": "Finance Director - High-value target",
        },
        {
            "username": "lisa.anderson",
            "display_name": "Lisa Anderson",
            "department": "Finance",
            "title": "Accountant",
            "groups": ["Domain Users", "Finance Department"],
            "password": "Account2024!",
            "password_never_expires": False,
            "account_disabled": False,
            "description": "Accountant - Access to financial systems",
        },
        # Sales Department
        {
            "username": "robert.taylor",
            "display_name": "Robert Taylor",
            "department": "Sales",
            "title": "Sales Manager",
            "groups": ["Domain Users", "Sales Department"],
            "password": "Sales2024!",
            "password_never_expires": False,
            "account_disabled": False,
            "description": "Sales Manager - Standard user",
        },
        {
            "username": "jennifer.martinez",
            "display_name": "Jennifer Martinez",
            "department": "Sales",
            "title": "Sales Representative",
            "groups": ["Domain Users", "Sales Department"],
            "password": "Welcome2024!",
            "password_never_expires": False,
            "account_disabled": False,
            "description": "Sales Rep - Standard user",
        },
        # Executive
        {
            "username": "william.thomas",
            "display_name": "William Thomas",
            "department": "Executive",
            "title": "CEO",
            "groups": ["Domain Users", "Executive", "Domain Admins"],  # High privilege
            "password": "CEO2024!",
            "password_never_expires": False,
            "account_disabled": False,
            "description": "CEO - Domain Admin (misconfiguration for red team)",
        },
        # Service Accounts (high-value targets)
        {
            "username": "svc_sql",
            "display_name": "SQL Service Account",
            "department": "IT",
            "title": "Service Account",
            "groups": ["Domain Users"],
            "password": "SvcSQL2024!",
            "password_never_expires": True,  # Common misconfiguration
            "account_disabled": False,
            "description": "SQL Server service account - Kerberoastable",
            "service_principal_names": ["MSSQLSvc/SQL01.corp.local:1433"],
        },
        {
            "username": "svc_exchange",
            "display_name": "Exchange Service Account",
            "department": "IT",
            "title": "Service Account",
            "groups": ["Domain Users"],
            "password": "SvcExchange2024!",
            "password_never_expires": True,
            "account_disabled": False,
            "description": "Exchange service account - Kerberoastable",
            "service_principal_names": ["exchange/exch01.corp.local"],
        },
        {
            "username": "svc_backup",
            "display_name": "Backup Service Account",
            "department": "IT",
            "title": "Service Account",
            "groups": ["Domain Users", "Backup Operators"],  # High privilege
            "password": "SvcBackup2024!",
            "password_never_expires": True,
            "account_disabled": False,
            "description": "Backup service account - Backup Operators group",
        },
        {
            "username": "svc_web",
            "display_name": "Web Service Account",
            "department": "IT",
            "title": "Service Account",
            "groups": ["Domain Users", "IIS_IUSRS"],
            "password": "SvcWeb2024!",
            "password_never_expires": True,
            "account_disabled": False,
            "description": "Web application service account",
            "service_principal_names": ["HTTP/web01.corp.local"],
        },
    ]


def get_local_admin_accounts() -> list[dict[str, Any]]:
    """Get local administrator accounts for workstations.
    
    Returns accounts that should be local admins on specific machines.
    This simulates real-world scenarios where some users have local admin rights.
    """
    return [
        {
            "username": "admin.local",
            "display_name": "Local Administrator",
            "password": "LocalAdmin2024!",
            "description": "Local admin account on workstations",
            "local_admin_on": ["workstations"],  # All workstations
        },
        {
            "username": "it.admin",
            "display_name": "IT Local Admin",
            "password": "ITAdmin2024!",
            "description": "IT department local admin",
            "local_admin_on": ["IT-WS01"],  # IT workstations only
        },
    ]


def get_ad_cs_config(
    vulnerability_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Get Active Directory Certificate Services (AD CS) configuration.
    
    Args:
        vulnerability_config: Optional vulnerability configuration to override defaults.
                             Keys can include: esc1_enabled, esc2_enabled, esc3_enabled,
                             esc4_enabled, esc6_enabled, esc7_enabled, esc8_enabled, etc.
    
    AD CS is commonly misconfigured and provides multiple attack vectors:
    - ESC1: Misconfigured Certificate Templates
    - ESC2: Vulnerable Certificate Template
    - ESC3: Enrollment Agent Templates
    - ESC4: Vulnerable Certificate Template ACLs
    - ESC6: EDITF_ATTRIBUTESUBJECTALTNAME2 enabled
    - ESC7: Vulnerable CA Certificate Manager Approval
    - ESC8: Web Enrollment vulnerable to NTLM relay
    """
    config = {
        "ca_name": "CORP-CA",
        "ca_type": "Enterprise Root CA",
        "vulnerable_configurations": {
            "esc1": {
                "enabled": True,
                "description": "Certificate template allows enrollment by Domain Users with Subject Alternative Name",
                "template_name": "VulnerableUser",
                "permissions": {
                    "enroll": ["Domain Users"],
                    "autoenroll": ["Domain Users"],
                },
            },
            "esc2": {
                "enabled": True,
                "description": "Certificate template allows any purpose",
                "template_name": "AnyPurposeTemplate",
            },
            "esc6": {
                "enabled": True,
                "description": "EDITF_ATTRIBUTESUBJECTALTNAME2 flag enabled on CA",
                "registry_key": "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\CertSvc\\Configuration\\CORP-CA",
                "registry_value": "EDITF_ATTRIBUTESUBJECTALTNAME2",
                "registry_data": 1,
            },
            "esc8": {
                "enabled": True,
                "description": "Web Enrollment enabled and vulnerable to NTLM relay",
                "web_enrollment_path": "/certsrv/",
                "ntlm_authentication": True,
            },
        },
        "certificate_templates": [
            {
                "name": "User",
                "purpose": "User authentication",
                "enrollment_restrictions": ["Domain Users"],
            },
            {
                "name": "VulnerableUser",
                "purpose": "Vulnerable template for ESC1",
                "enrollment_restrictions": ["Domain Users"],
                "subject_alternative_name": True,
                "vulnerable": True,
            },
            {
                "name": "DomainController",
                "purpose": "Domain controller authentication",
                "enrollment_restrictions": ["Domain Controllers"],
            },
            {
                "name": "WebServer",
                "purpose": "Web server SSL certificates",
                "enrollment_restrictions": ["Web Servers"],
            },
        ],
    }
    
    # Apply vulnerability customizations if provided
    if vulnerability_config:
            vuln_configs = config.get("vulnerable_configurations", {})
            
            # Update AD CS ESC configurations
            for esc_num in [1, 2, 3, 4, 6, 7, 8, 9, 10]:
                esc_key = f"esc{esc_num}_enabled"
                if esc_key in vulnerability_config:
                    esc_name = f"esc{esc_num}"
                    if esc_name not in vuln_configs:
                        # Create default config for new ESC vulnerabilities
                        vuln_configs[esc_name] = {
                            "enabled": vulnerability_config[esc_key],
                            "description": f"AD CS ESC{esc_num} vulnerability",
                        }
                    else:
                        vuln_configs[esc_name]["enabled"] = vulnerability_config[esc_key]
            
            # Store all other vulnerability flags in the config for use by Ansible roles
            # These will be passed to ludus-ad-vulns or similar roles
            config["vulnerability_flags"] = {
                # Kerberos
                "asrep_roasting_enabled": vulnerability_config.get("asrep_roasting_enabled"),
                "kerberoastable_accounts": vulnerability_config.get("kerberoastable_accounts"),
                "kerberos_encryption_downgrade": vulnerability_config.get("kerberos_encryption_downgrade"),
                "pkinit_downgrade": vulnerability_config.get("pkinit_downgrade"),
                # Delegation
                "unconstrained_delegation": vulnerability_config.get("unconstrained_delegation"),
                "constrained_delegation": vulnerability_config.get("constrained_delegation"),
                "resource_based_constrained_delegation": vulnerability_config.get("resource_based_constrained_delegation"),
                "delegation_to_domain_admin": vulnerability_config.get("delegation_to_domain_admin"),
                # Credential theft
                "lsass_dumpable": vulnerability_config.get("lsass_dumpable"),
                "sam_dumpable": vulnerability_config.get("sam_dumpable"),
                "ntds_dit_accessible": vulnerability_config.get("ntds_dit_accessible"),
                "volume_shadow_copy_abuse": vulnerability_config.get("volume_shadow_copy_abuse"),
                "gpp_passwords": vulnerability_config.get("gpp_passwords"),
                "laps_misconfigured": vulnerability_config.get("laps_misconfigured"),
                # ACL abuse
                "dcsync_abuse": vulnerability_config.get("dcsync_abuse"),
                "acl_backdoors": vulnerability_config.get("acl_backdoors"),
                "writable_domain_sysvol": vulnerability_config.get("writable_domain_sysvol"),
                "writable_domain_scripts": vulnerability_config.get("writable_domain_scripts"),
                "generic_write_on_dc": vulnerability_config.get("generic_write_on_dc"),
                # Service misconfigurations
                "service_account_weak_passwords": vulnerability_config.get("service_account_weak_passwords"),
                "service_account_password_never_expires": vulnerability_config.get("service_account_password_never_expires"),
                "local_admin_reuse": vulnerability_config.get("local_admin_reuse"),
                "domain_admin_in_domain_users": vulnerability_config.get("domain_admin_in_domain_users"),
                "admin_sd_holder_abuse": vulnerability_config.get("admin_sd_holder_abuse"),
                # Group-based attacks
                "dns_admins_abuse": vulnerability_config.get("dns_admins_abuse"),
                "backup_operators_abuse": vulnerability_config.get("backup_operators_abuse"),
                "account_operators_abuse": vulnerability_config.get("account_operators_abuse"),
                "server_operators_abuse": vulnerability_config.get("server_operators_abuse"),
                "print_operators_abuse": vulnerability_config.get("print_operators_abuse"),
                "remote_desktop_users_abuse": vulnerability_config.get("remote_desktop_users_abuse"),
                # Network protocols
                "smb_signing_disabled": vulnerability_config.get("smb_signing_disabled"),
                "smb_relay_enabled": vulnerability_config.get("smb_relay_enabled"),
                "llmnr_enabled": vulnerability_config.get("llmnr_enabled"),
                "nbns_enabled": vulnerability_config.get("nbns_enabled"),
                "wpad_misconfigured": vulnerability_config.get("wpad_misconfigured"),
                "ldap_signing_disabled": vulnerability_config.get("ldap_signing_disabled"),
                "ldap_channel_binding_disabled": vulnerability_config.get("ldap_channel_binding_disabled"),
                # RPC/DCOM
                "ms_efsrpc_abuse": vulnerability_config.get("ms_efsrpc_abuse"),
                "print_spooler_enabled": vulnerability_config.get("print_spooler_enabled"),
                "dcom_lateral_movement": vulnerability_config.get("dcom_lateral_movement"),
                "wmi_abuse": vulnerability_config.get("wmi_abuse"),
                "winrm_abuse": vulnerability_config.get("winrm_abuse"),
                # Scheduled tasks/services
                "scheduled_tasks_weak_permissions": vulnerability_config.get("scheduled_tasks_weak_permissions"),
                "service_weak_permissions": vulnerability_config.get("service_weak_permissions"),
                "unquoted_service_paths": vulnerability_config.get("unquoted_service_paths"),
                "writable_service_binaries": vulnerability_config.get("writable_service_binaries"),
                # Exchange
                "exchange_privilege_escalation": vulnerability_config.get("exchange_privilege_escalation"),
                "exchange_ews_abuse": vulnerability_config.get("exchange_ews_abuse"),
                "exchange_proxyshell": vulnerability_config.get("exchange_proxyshell"),
                "exchange_proxylogon": vulnerability_config.get("exchange_proxylogon"),
                # SQL Server
                "sql_server_weak_passwords": vulnerability_config.get("sql_server_weak_passwords"),
                "sql_server_xp_cmdshell": vulnerability_config.get("sql_server_xp_cmdshell"),
                "sql_server_impersonation": vulnerability_config.get("sql_server_impersonation"),
                # RDP
                "rdp_enabled": vulnerability_config.get("rdp_enabled"),
                "rdp_weak_credentials": vulnerability_config.get("rdp_weak_credentials"),
                "rdp_hijacking": vulnerability_config.get("rdp_hijacking"),
                "credssp_abuse": vulnerability_config.get("credssp_abuse"),
                # File shares
                "open_shares": vulnerability_config.get("open_shares"),
                "writable_shares": vulnerability_config.get("writable_shares"),
                "shares_with_credentials": vulnerability_config.get("shares_with_credentials"),
                # GPO
                "gpo_weak_permissions": vulnerability_config.get("gpo_weak_permissions"),
                "gpo_scheduled_tasks": vulnerability_config.get("gpo_scheduled_tasks"),
                "gpo_startup_scripts": vulnerability_config.get("gpo_startup_scripts"),
                "gpo_logon_scripts": vulnerability_config.get("gpo_logon_scripts"),
                # Trust
                "forest_trust_abuse": vulnerability_config.get("forest_trust_abuse"),
                "external_trust_abuse": vulnerability_config.get("external_trust_abuse"),
                "sid_history_abuse": vulnerability_config.get("sid_history_abuse"),
                "sid_filtering_disabled": vulnerability_config.get("sid_filtering_disabled"),
                # Shadow credentials
                "shadow_credentials_enabled": vulnerability_config.get("shadow_credentials_enabled"),
                "key_credential_link_abuse": vulnerability_config.get("key_credential_link_abuse"),
                # Privileges
                "seimpersonate_privilege_abuse": vulnerability_config.get("seimpersonate_privilege_abuse"),
                "seassignprimarytoken_privilege_abuse": vulnerability_config.get("seassignprimarytoken_privilege_abuse"),
                "sedebug_privilege_abuse": vulnerability_config.get("sedebug_privilege_abuse"),
                "sebackup_privilege_abuse": vulnerability_config.get("sebackup_privilege_abuse"),
                "serestore_privilege_abuse": vulnerability_config.get("serestore_privilege_abuse"),
                "setakeownership_privilege_abuse": vulnerability_config.get("setakeownership_privilege_abuse"),
                "seloaddriver_privilege_abuse": vulnerability_config.get("seloaddriver_privilege_abuse"),
                # Zero-day/CVE
                "zerologon_enabled": vulnerability_config.get("zerologon_enabled"),
                "nopac_enabled": vulnerability_config.get("nopac_enabled"),
                "ms14_068_enabled": vulnerability_config.get("ms14_068_enabled"),
            }
            
            config["vulnerable_configurations"] = vuln_configs
    
    return config


def get_opsec_detection_rules() -> list[dict[str, Any]]:
    """Get OPSEC detection rules for Wazuh SIEM.
    
    These rules detect common red team attack patterns and OPSEC violations.
    """
    return [
        {
            "rule_id": "redteam_001",
            "name": "Kerberoasting Attack Detection",
            "description": "Detects multiple Kerberos TGS-REQ requests for service accounts",
            "wazuh_rule": {
                "level": 12,
                "rule": {
                    "if_sid": ["5710"],  # Windows authentication events
                    "frequency": 5,
                    "timeframe": 300,
                    "description": "Multiple Kerberos service ticket requests detected (possible Kerberoasting)",
                },
            },
            "attack_technique": "T1558.003",
            "severity": "high",
        },
        {
            "rule_id": "redteam_002",
            "name": "AS-REP Roasting Detection",
            "description": "Detects AS-REQ requests without pre-authentication",
            "wazuh_rule": {
                "level": 12,
                "rule": {
                    "if_sid": ["5710"],
                    "description": "Kerberos AS-REQ without pre-authentication (possible AS-REP roasting)",
                },
            },
            "attack_technique": "T1558.004",
            "severity": "high",
        },
        {
            "rule_id": "redteam_003",
            "name": "DCSync Attack Detection",
            "description": "Detects DCSync attempts (replication requests)",
            "wazuh_rule": {
                "level": 15,
                "rule": {
                    "if_sid": ["4719"],  # System audit policy change
                    "description": "DCSync replication request detected (possible credential theft)",
                },
            },
            "attack_technique": "T1003.006",
            "severity": "critical",
        },
        {
            "rule_id": "redteam_004",
            "name": "Pass-the-Hash Detection",
            "description": "Detects NTLM authentication with hash",
            "wazuh_rule": {
                "level": 12,
                "rule": {
                    "if_sid": ["4624"],  # Successful logon
                    "description": "NTLM authentication detected (possible Pass-the-Hash)",
                },
            },
            "attack_technique": "T1550.002",
            "severity": "high",
        },
        {
            "rule_id": "redteam_005",
            "name": "Lateral Movement via RDP",
            "description": "Detects multiple RDP connections from same source",
            "wazuh_rule": {
                "level": 10,
                "rule": {
                    "if_sid": ["4624"],
                    "logon_type": 10,  # RemoteInteractive (RDP)
                    "frequency": 3,
                    "timeframe": 600,
                    "description": "Multiple RDP connections from same source (possible lateral movement)",
                },
            },
            "attack_technique": "T1021.001",
            "severity": "medium",
        },
        {
            "rule_id": "redteam_006",
            "name": "Lateral Movement via SMB",
            "description": "Detects SMB connections to multiple hosts",
            "wazuh_rule": {
                "level": 10,
                "rule": {
                    "if_sid": ["5140"],  # Network share accessed
                    "frequency": 5,
                    "timeframe": 300,
                    "description": "SMB connections to multiple hosts (possible lateral movement)",
                },
            },
            "attack_technique": "T1021.002",
            "severity": "medium",
        },
        {
            "rule_id": "redteam_007",
            "name": "AD CS Certificate Abuse",
            "description": "Detects certificate enrollment abuse",
            "wazuh_rule": {
                "level": 12,
                "rule": {
                    "if_sid": ["4897"],  # Certificate services
                    "description": "Certificate enrollment from non-standard account (possible AD CS abuse)",
                },
            },
            "attack_technique": "T1649",
            "severity": "high",
        },
        {
            "rule_id": "redteam_008",
            "name": "Golden Ticket Usage",
            "description": "Detects use of golden tickets (TGT with long lifetime)",
            "wazuh_rule": {
                "level": 15,
                "rule": {
                    "if_sid": ["4768"],  # Kerberos TGT
                    "ticket_lifetime": "> 10 hours",
                    "description": "Kerberos TGT with extended lifetime (possible Golden Ticket)",
                },
            },
            "attack_technique": "T1558.001",
            "severity": "critical",
        },
        {
            "rule_id": "redteam_009",
            "name": "Service Account Enumeration",
            "description": "Detects enumeration of service accounts",
            "wazuh_rule": {
                "level": 8,
                "rule": {
                    "if_sid": ["4798"],  # User account enumeration
                    "frequency": 10,
                    "timeframe": 60,
                    "description": "Multiple service account queries (possible enumeration)",
                },
            },
            "attack_technique": "T1087.002",
            "severity": "low",
        },
        {
            "rule_id": "redteam_010",
            "name": "Unconstrained Delegation Abuse",
            "description": "Detects abuse of unconstrained delegation",
            "wazuh_rule": {
                "level": 12,
                "rule": {
                    "if_sid": ["4769"],  # Kerberos service ticket
                    "delegation": "unconstrained",
                    "description": "Unconstrained delegation usage detected",
                },
            },
            "attack_technique": "T1558.002",
            "severity": "high",
        },
        {
            "rule_id": "redteam_011",
            "name": "OPSEC Violation - High Volume LDAP Queries",
            "description": "Detects high volume LDAP queries (poor OPSEC)",
            "wazuh_rule": {
                "level": 10,
                "rule": {
                    "if_sid": ["5136"],  # Directory service access
                    "frequency": 100,
                    "timeframe": 60,
                    "description": "High volume LDAP queries detected (poor OPSEC)",
                },
            },
            "attack_technique": "T1087.002",
            "severity": "medium",
            "opsec_violation": True,
        },
        {
            "rule_id": "redteam_012",
            "name": "OPSEC Violation - Rapid Credential Dumping",
            "description": "Detects rapid credential dumping attempts",
            "wazuh_rule": {
                "level": 12,
                "rule": {
                    "if_sid": ["4656"],  # Handle to object requested
                    "frequency": 50,
                    "timeframe": 30,
                    "description": "Rapid credential access attempts (poor OPSEC)",
                },
            },
            "attack_technique": "T1003",
            "severity": "high",
            "opsec_violation": True,
        },
        {
            "rule_id": "redteam_013",
            "name": "OPSEC Violation - Suspicious Process Execution",
            "description": "Detects execution of known red team tools",
            "wazuh_rule": {
                "level": 10,
                "rule": {
                    "if_sid": ["4688"],  # Process creation
                    "process_name": [
                        "mimikatz.exe",
                        "sekurlsa.exe",
                        "lsadump.exe",
                        "procdump.exe",
                        "bloodhound.exe",
                        "sharphound.exe",
                    ],
                    "description": "Known red team tool execution detected",
                },
            },
            "attack_technique": "T1055",
            "severity": "high",
            "opsec_violation": True,
        },
    ]


def get_forest_pivot_attack_paths() -> dict[str, Any]:
    """Get attack paths requiring forest pivoting between two forests.
    
    These paths require compromising one forest and pivoting to another via trust.
    """
    return {
        "path_forest_pivot_1": {
            "name": "Forest Trust Pivot via Kerberoasting",
            "steps": [
                "1. Initial access in Forest 1 (CORP.LOCAL) via compromised workstation",
                "2. Enumerate forest trust relationships: Get-DomainTrust",
                "3. Identify Forest 2 (PARTNER.LOCAL) trust relationship",
                "4. Enumerate users in Forest 2 via trust: Get-DomainUser -Domain PARTNER.LOCAL",
                "5. Identify service accounts in Forest 2 with SPNs",
                "6. Cross-forest Kerberoasting: Invoke-Kerberoast -Domain PARTNER.LOCAL",
                "7. Crack service account passwords from Forest 2",
                "8. Use Forest 2 service account to access SQL Server in Forest 2",
                "9. Escalate to Forest 2 Domain Admin",
                "10. Use Forest 2 DA to perform cross-forest DCSync on Forest 1",
                "11. Compromise Forest 1 via cross-forest attack",
            ],
            "detection_points": ["redteam_001", "redteam_003", "redteam_009"],
            "opsec_considerations": [
                "Cross-forest enumeration is highly detectable",
                "Use low-volume queries across trust",
                "Time delays between forest operations",
            ],
        },
        "path_forest_pivot_2": {
            "name": "Forest Trust Golden Ticket Pivot",
            "steps": [
                "1. Compromise Forest 1 (CORP.LOCAL) Domain Admin",
                "2. Extract KRBTGT hash from Forest 1",
                "3. Create Golden Ticket for Forest 1",
                "4. Enumerate forest trust: Get-DomainTrust",
                "5. Use Forest 1 Golden Ticket to authenticate to Forest 2",
                "6. Enumerate Forest 2 structure via trust",
                "7. Perform DCSync on Forest 2 DC via trust relationship",
                "8. Extract Forest 2 KRBTGT hash",
                "9. Create Golden Ticket for Forest 2",
                "10. Full compromise of both forests",
            ],
            "detection_points": ["redteam_003", "redteam_008"],
            "opsec_considerations": [
                "Cross-forest DCSync is very detectable",
                "Golden tickets with long lifetime are easily spotted",
                "Use shorter ticket lifetimes",
            ],
        },
        "path_forest_pivot_3": {
            "name": "Forest Trust via SID History",
            "steps": [
                "1. Compromise Forest 1 (CORP.LOCAL) Domain Admin",
                "2. Enumerate forest trust relationship",
                "3. Create user in Forest 1 with SID History from Forest 2",
                "4. Use SID History to gain privileges in Forest 2",
                "5. Escalate in Forest 2 using SID History",
                "6. Compromise Forest 2 Domain Admin",
            ],
            "detection_points": ["redteam_003", "redteam_004"],
            "opsec_considerations": [
                "SID History manipulation is detectable",
                "Monitor for unusual SID History values",
            ],
        },
    }


def get_ad_attack_paths() -> dict[str, Any]:
    """Get realistic AD attack paths for red team scenarios.
    
    These attack paths represent common real-world scenarios.
    """
    return {
        "path_1_kerberoasting": {
            "name": "Kerberoasting to Domain Admin",
            "steps": [
                "1. Initial access via compromised workstation (WS01)",
                "2. Domain enumeration using PowerView/BloodHound",
                "3. Identify service accounts with SPNs",
                "4. Kerberoast service accounts (svc_sql, svc_exchange)",
                "5. Crack service account passwords",
                "6. Use service account to access SQL Server",
                "7. Escalate to Domain Admin via SQL Server privileges",
            ],
            "detection_points": ["redteam_001", "redteam_009"],
            "opsec_considerations": [
                "Use low-volume LDAP queries",
                "Avoid rapid-fire Kerberoasting",
                "Use legitimate tools when possible",
            ],
        },
        "path_2_ad_cs_esc1": {
            "name": "AD CS ESC1 Certificate Abuse",
            "steps": [
                "1. Initial access via compromised workstation",
                "2. Enumerate AD CS certificate templates",
                "3. Identify vulnerable template (VulnerableUser)",
                "4. Request certificate with Subject Alternative Name",
                "5. Use certificate for authentication",
                "6. Escalate to Domain Admin",
            ],
            "detection_points": ["redteam_007"],
            "opsec_considerations": [
                "Minimize certificate enrollment requests",
                "Use legitimate enrollment methods",
            ],
        },
        "path_3_pass_the_hash": {
            "name": "Pass-the-Hash Lateral Movement",
            "steps": [
                "1. Initial access via phishing/vulnerable service",
                "2. Dump credentials from memory (LSASS)",
                "3. Extract NTLM hashes",
                "4. Pass-the-hash to multiple workstations",
                "5. Identify local admin accounts",
                "6. Escalate to Domain Admin",
            ],
            "detection_points": ["redteam_004", "redteam_005", "redteam_012"],
            "opsec_considerations": [
                "Avoid rapid credential dumping",
                "Use legitimate authentication methods when possible",
                "Limit lateral movement speed",
            ],
        },
        "path_4_dcsync": {
            "name": "DCSync to Golden Ticket",
            "steps": [
                "1. Compromise account with DCSync rights",
                "2. Perform DCSync to extract KRBTGT hash",
                "3. Create Golden Ticket with extended lifetime",
                "4. Use Golden Ticket for domain-wide access",
                "5. Establish persistence",
            ],
            "detection_points": ["redteam_003", "redteam_008"],
            "opsec_considerations": [
                "DCSync is highly detectable",
                "Golden tickets with long lifetime are easily detected",
                "Use shorter ticket lifetimes",
            ],
        },
    }

