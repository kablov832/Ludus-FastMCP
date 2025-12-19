"""Schema definitions for scenario customization and randomization."""

from typing import Any
from dataclasses import dataclass, field
from enum import Enum


class RandomizationScope(str, Enum):
    """What aspects of a scenario can be randomized."""
    USERS = "users"
    VULNERABILITIES = "vulnerabilities"
    NETWORK = "network"
    VMS = "vms"
    ALL = "all"


@dataclass
class ADUserCustomization:
    """Custom AD user account configuration."""
    username: str
    display_name: str
    password: str
    department: str | None = None
    title: str | None = None
    groups: list[str] = field(default_factory=list)
    password_never_expires: bool = False
    account_disabled: bool = False
    description: str | None = None
    path: str | None = None  # OU path


@dataclass
class VulnerabilityConfig:
    """Vulnerability configuration for scenarios - comprehensive APT attack techniques."""
    
    # ========== AD CS (Certificate Services) Vulnerabilities ==========
    esc1_enabled: bool | None = None  # Certificate template with SAN
    esc2_enabled: bool | None = None  # Any-purpose template
    esc3_enabled: bool | None = None  # Enrollment agent
    esc4_enabled: bool | None = None  # Vulnerable template ACLs
    esc6_enabled: bool | None = None  # EDITF_ATTRIBUTESUBJECTALTNAME2
    esc7_enabled: bool | None = None  # CA manager approval
    esc8_enabled: bool | None = None  # Web enrollment NTLM relay
    esc9_enabled: bool | None = None  # Exchange template abuse
    esc10_enabled: bool | None = None  # Weak certificate mapping
    
    # ========== Kerberos Attacks ==========
    asrep_roasting_enabled: bool | None = None  # Users without preauth (AS-REP Roasting)
    kerberoastable_accounts: bool | None = None  # Service accounts with weak passwords
    kerberos_encryption_downgrade: bool | None = None  # Weak encryption types allowed
    pkinit_downgrade: bool | None = None  # PKINIT downgrade attacks
    
    # ========== Delegation Attacks ==========
    unconstrained_delegation: bool | None = None  # Unconstrained delegation
    constrained_delegation: bool | None = None  # Constrained delegation (S4U2Proxy)
    resource_based_constrained_delegation: bool | None = None  # RBCD attacks
    delegation_to_domain_admin: bool | None = None  # Delegation to DA accounts
    
    # ========== Credential Theft & Dumping ==========
    lsass_dumpable: bool | None = None  # LSASS memory dumping opportunities
    sam_dumpable: bool | None = None  # SAM database accessible
    ntds_dit_accessible: bool | None = None  # NTDS.dit extraction possible
    volume_shadow_copy_abuse: bool | None = None  # VSS abuse for credential theft
    gpp_passwords: bool | None = None  # Group Policy Preferences with passwords
    laps_misconfigured: bool | None = None  # LAPS misconfiguration
    
    # ========== ACL & Permission Abuse ==========
    dcsync_abuse: bool | None = None  # DCSync rights on non-DA accounts
    acl_backdoors: bool | None = None  # ACL-based backdoors
    writable_domain_sysvol: bool | None = None  # Writable SYSVOL
    writable_domain_scripts: bool | None = None  # Writable logon scripts
    generic_write_on_dc: bool | None = None  # GenericWrite on DC objects
    
    # ========== Service & Account Misconfigurations ==========
    service_account_weak_passwords: bool | None = None  # Service accounts with weak passwords
    service_account_password_never_expires: bool | None = None  # Service accounts with non-expiring passwords
    local_admin_reuse: bool | None = None  # Same local admin password across machines
    domain_admin_in_domain_users: bool | None = None  # DA accounts in Domain Users
    admin_sd_holder_abuse: bool | None = None  # AdminSDHolder misconfiguration
    
    # ========== Group-Based Attacks ==========
    dns_admins_abuse: bool | None = None  # DNS Admins group abuse
    backup_operators_abuse: bool | None = None  # Backup Operators abuse
    account_operators_abuse: bool | None = None  # Account Operators abuse
    server_operators_abuse: bool | None = None  # Server Operators abuse
    print_operators_abuse: bool | None = None  # Print Operators abuse
    remote_desktop_users_abuse: bool | None = None  # RDP users with weak configs
    
    # ========== Network Protocol Vulnerabilities ==========
    smb_signing_disabled: bool | None = None  # SMB signing not required
    smb_relay_enabled: bool | None = None  # SMB relay opportunities
    llmnr_enabled: bool | None = None  # LLMNR enabled (name poisoning)
    nbns_enabled: bool | None = None  # NBT-NS enabled (name poisoning)
    wpad_misconfigured: bool | None = None  # WPAD attacks possible
    ldap_signing_disabled: bool | None = None  # LDAP signing not required
    ldap_channel_binding_disabled: bool | None = None  # LDAP channel binding disabled
    
    # ========== RPC & DCOM Attacks ==========
    ms_efsrpc_abuse: bool | None = None  # PetitPotam / MS-EFSRPC abuse
    print_spooler_enabled: bool | None = None  # PrintNightmare / Print Spooler
    dcom_lateral_movement: bool | None = None  # DCOM lateral movement
    wmi_abuse: bool | None = None  # WMI abuse for lateral movement
    winrm_abuse: bool | None = None  # WinRM abuse
    
    # ========== Scheduled Tasks & Services ==========
    scheduled_tasks_weak_permissions: bool | None = None  # Scheduled tasks with weak ACLs
    service_weak_permissions: bool | None = None  # Services with weak ACLs
    unquoted_service_paths: bool | None = None  # Unquoted service paths
    writable_service_binaries: bool | None = None  # Writable service executables
    
    # ========== Exchange & Email Attacks ==========
    exchange_privilege_escalation: bool | None = None  # Exchange privilege escalation
    exchange_ews_abuse: bool | None = None  # Exchange Web Services abuse
    exchange_proxyshell: bool | None = None  # ProxyShell vulnerabilities
    exchange_proxylogon: bool | None = None  # ProxyLogon vulnerabilities
    
    # ========== SQL Server Attacks ==========
    sql_server_weak_passwords: bool | None = None  # SQL Server with weak passwords
    sql_server_xp_cmdshell: bool | None = None  # xp_cmdshell enabled
    sql_server_impersonation: bool | None = None  # SQL Server impersonation abuse
    
    # ========== RDP & Remote Access ==========
    rdp_enabled: bool | None = None  # RDP enabled
    rdp_weak_credentials: bool | None = None  # RDP with weak credentials
    rdp_hijacking: bool | None = None  # RDP session hijacking opportunities
    credssp_abuse: bool | None = None  # CredSSP abuse
    
    # ========== File Share Attacks ==========
    open_shares: bool | None = None  # Open SMB shares
    writable_shares: bool | None = None  # Writable shares
    shares_with_credentials: bool | None = None  # Shares with stored credentials
    
    # ========== GPO & Policy Abuse ==========
    gpo_weak_permissions: bool | None = None  # GPOs with weak permissions
    gpo_scheduled_tasks: bool | None = None  # GPOs with scheduled tasks
    gpo_startup_scripts: bool | None = None  # GPOs with startup scripts
    gpo_logon_scripts: bool | None = None  # GPOs with logon scripts
    
    # ========== Trust & Forest Attacks ==========
    forest_trust_abuse: bool | None = None  # Forest trust abuse
    external_trust_abuse: bool | None = None  # External trust abuse
    sid_history_abuse: bool | None = None  # SID History abuse
    sid_filtering_disabled: bool | None = None  # SID filtering disabled
    
    # ========== Shadow Credentials ==========
    shadow_credentials_enabled: bool | None = None  # Shadow credentials attack
    key_credential_link_abuse: bool | None = None  # KeyCredentialLink abuse
    
    # ========== Token & Privilege Abuse ==========
    seimpersonate_privilege_abuse: bool | None = None  # SeImpersonatePrivilege abuse
    seassignprimarytoken_privilege_abuse: bool | None = None  # SeAssignPrimaryTokenPrivilege abuse
    sedebug_privilege_abuse: bool | None = None  # SeDebugPrivilege abuse
    sebackup_privilege_abuse: bool | None = None  # SeBackupPrivilege abuse
    serestore_privilege_abuse: bool | None = None  # SeRestorePrivilege abuse
    setakeownership_privilege_abuse: bool | None = None  # SeTakeOwnershipPrivilege abuse
    seloaddriver_privilege_abuse: bool | None = None  # SeLoadDriverPrivilege abuse
    
    # ========== Zero-Day & CVE-Based ==========
    zerologon_enabled: bool | None = None  # CVE-2020-1472 (Zerologon)
    nopac_enabled: bool | None = None  # CVE-2021-42287, CVE-2021-42278 (NoPac)
    ms14_068_enabled: bool | None = None  # MS14-068 (PAC validation bypass)
    
    # ========== Custom vulnerability config ==========
    custom_config: dict[str, Any] = field(default_factory=dict)


@dataclass
class NetworkCustomization:
    """Network configuration customizations."""
    # VLAN changes (map of VM name pattern -> new VLAN)
    vlan_changes: dict[str, int] = field(default_factory=dict)
    
    # Firewall rule modifications
    additional_rules: list[dict[str, Any]] = field(default_factory=list)
    remove_rules: list[str] = field(default_factory=list)  # Rule names to remove
    
    # Network segment changes
    inter_vlan_default: str | None = None  # REJECT, ACCEPT, etc.


@dataclass
class VMCustomization:
    """VM configuration customizations."""
    # VM count overrides (e.g., {"workstation": 4} to have 4 workstations)
    vm_count_overrides: dict[str, int] = field(default_factory=dict)
    
    # VM type additions (e.g., add an extra server)
    additional_vms: list[dict[str, Any]] = field(default_factory=list)
    
    # VM removals (by name pattern)
    remove_vms: list[str] = field(default_factory=list)
    
    # Resource overrides (by VM name pattern)
    resource_overrides: dict[str, dict[str, int]] = field(default_factory=dict)  # {"vm_name": {"ram_gb": 8, "cpus": 4}}


@dataclass
class RandomizationConfig:
    """Configuration for randomization."""
    randomize_users: bool = True
    randomize_vulnerabilities: bool = True
    randomize_network: bool = False  # Network randomization can break scenarios
    randomize_vms: bool = False  # VM randomization can break scenarios
    
    # Randomization constraints
    min_users: int = 5
    max_users: int = 15
    min_workstations: int = 2
    max_workstations: int = 4
    
    # Randomization seed for reproducibility (optional)
    seed: int | None = None


@dataclass
class ScenarioCustomization:
    """Container for all scenario customizations."""
    # Custom AD users (replaces default users if provided)
    custom_users: list[ADUserCustomization] | None = None
    
    # Custom OUs (additional or replacement)
    custom_ous: list[dict[str, Any]] | None = None
    
    # Custom groups (additional or replacement)
    custom_groups: list[dict[str, Any]] | None = None
    
    # Vulnerability configuration
    vulnerability_config: VulnerabilityConfig | None = None
    
    # Network customizations
    network_customization: NetworkCustomization | None = None
    
    # VM customizations
    vm_customization: VMCustomization | None = None
    
    # Randomization config (if randomize=True)
    randomization_config: RandomizationConfig | None = None
    
    def has_customizations(self) -> bool:
        """Check if any customizations are provided."""
        return (
            self.custom_users is not None or
            self.custom_ous is not None or
            self.custom_groups is not None or
            self.vulnerability_config is not None or
            self.network_customization is not None or
            self.vm_customization is not None
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        result: dict[str, Any] = {}
        
        if self.custom_users:
            result["custom_users"] = [
                {
                    "username": u.username,
                    "display_name": u.display_name,
                    "password": u.password,
                    "department": u.department,
                    "title": u.title,
                    "groups": u.groups,
                    "password_never_expires": u.password_never_expires,
                    "account_disabled": u.account_disabled,
                    "description": u.description,
                    "path": u.path,
                }
                for u in self.custom_users
            ]
        
        if self.custom_ous:
            result["custom_ous"] = self.custom_ous
        
        if self.custom_groups:
            result["custom_groups"] = self.custom_groups
        
        if self.vulnerability_config:
            vuln_dict: dict[str, Any] = {}
            # Use getattr to dynamically include all vulnerability fields
            vulnerability_fields = [
                # AD CS
                "esc1_enabled", "esc2_enabled", "esc3_enabled", "esc4_enabled",
                "esc6_enabled", "esc7_enabled", "esc8_enabled", "esc9_enabled", "esc10_enabled",
                # Kerberos
                "asrep_roasting_enabled", "kerberoastable_accounts",
                "kerberos_encryption_downgrade", "pkinit_downgrade",
                # Delegation
                "unconstrained_delegation", "constrained_delegation",
                "resource_based_constrained_delegation", "delegation_to_domain_admin",
                # Credential theft
                "lsass_dumpable", "sam_dumpable", "ntds_dit_accessible",
                "volume_shadow_copy_abuse", "gpp_passwords", "laps_misconfigured",
                # ACL abuse
                "dcsync_abuse", "acl_backdoors", "writable_domain_sysvol",
                "writable_domain_scripts", "generic_write_on_dc",
                # Service misconfigurations
                "service_account_weak_passwords", "service_account_password_never_expires",
                "local_admin_reuse", "domain_admin_in_domain_users", "admin_sd_holder_abuse",
                # Group-based attacks
                "dns_admins_abuse", "backup_operators_abuse", "account_operators_abuse",
                "server_operators_abuse", "print_operators_abuse", "remote_desktop_users_abuse",
                # Network protocols
                "smb_signing_disabled", "smb_relay_enabled", "llmnr_enabled", "nbns_enabled",
                "wpad_misconfigured", "ldap_signing_disabled", "ldap_channel_binding_disabled",
                # RPC/DCOM
                "ms_efsrpc_abuse", "print_spooler_enabled", "dcom_lateral_movement",
                "wmi_abuse", "winrm_abuse",
                # Scheduled tasks/services
                "scheduled_tasks_weak_permissions", "service_weak_permissions",
                "unquoted_service_paths", "writable_service_binaries",
                # Exchange
                "exchange_privilege_escalation", "exchange_ews_abuse",
                "exchange_proxyshell", "exchange_proxylogon",
                # SQL Server
                "sql_server_weak_passwords", "sql_server_xp_cmdshell", "sql_server_impersonation",
                # RDP
                "rdp_enabled", "rdp_weak_credentials", "rdp_hijacking", "credssp_abuse",
                # File shares
                "open_shares", "writable_shares", "shares_with_credentials",
                # GPO
                "gpo_weak_permissions", "gpo_scheduled_tasks", "gpo_startup_scripts", "gpo_logon_scripts",
                # Trust
                "forest_trust_abuse", "external_trust_abuse", "sid_history_abuse", "sid_filtering_disabled",
                # Shadow credentials
                "shadow_credentials_enabled", "key_credential_link_abuse",
                # Privileges
                "seimpersonate_privilege_abuse", "seassignprimarytoken_privilege_abuse",
                "sedebug_privilege_abuse", "sebackup_privilege_abuse", "serestore_privilege_abuse",
                "setakeownership_privilege_abuse", "seloaddriver_privilege_abuse",
                # Zero-day/CVE
                "zerologon_enabled", "nopac_enabled", "ms14_068_enabled",
            ]
            
            for field in vulnerability_fields:
                value = getattr(self.vulnerability_config, field, None)
                if value is not None:
                    vuln_dict[field] = value
            
            if self.vulnerability_config.custom_config:
                vuln_dict["custom_config"] = self.vulnerability_config.custom_config
            
            result["vulnerability_config"] = vuln_dict
        
        if self.network_customization:
            result["network_customization"] = {
                "vlan_changes": self.network_customization.vlan_changes,
                "additional_rules": self.network_customization.additional_rules,
                "remove_rules": self.network_customization.remove_rules,
                "inter_vlan_default": self.network_customization.inter_vlan_default,
            }
        
        if self.vm_customization:
            result["vm_customization"] = {
                "vm_count_overrides": self.vm_customization.vm_count_overrides,
                "additional_vms": self.vm_customization.additional_vms,
                "remove_vms": self.vm_customization.remove_vms,
                "resource_overrides": self.vm_customization.resource_overrides,
            }
        
        if self.randomization_config:
            result["randomization_config"] = {
                "randomize_users": self.randomization_config.randomize_users,
                "randomize_vulnerabilities": self.randomization_config.randomize_vulnerabilities,
                "randomize_network": self.randomization_config.randomize_network,
                "randomize_vms": self.randomization_config.randomize_vms,
                "min_users": self.randomization_config.min_users,
                "max_users": self.randomization_config.max_users,
                "min_workstations": self.randomization_config.min_workstations,
                "max_workstations": self.randomization_config.max_workstations,
                "seed": self.randomization_config.seed,
            }
        
        return result

