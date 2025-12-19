"""Generate comprehensive walkthroughs for deployed scenarios."""

from typing import Any
from ..utils.logging import get_logger

logger = get_logger(__name__)


def generate_scenario_walkthrough(
    scenario_key: str,
    scenario_name: str,
    config: dict[str, Any],
    customized: bool = False,
    randomized: bool = False,
    customization_summary: str | None = None,
) -> dict[str, Any]:
    """Generate comprehensive walkthrough for a deployed scenario.
    
    Args:
        scenario_key: Scenario identifier
        scenario_name: Human-readable scenario name
        config: Final deployed configuration
        customized: Whether scenario was customized
        randomized: Whether scenario was randomized
        customization_summary: Summary of customizations applied
        
    Returns:
        Comprehensive walkthrough dictionary
    """
    vms = config.get("ludus", [])
    network = config.get("network", {})
    
    # Extract VM information
    vm_list = []
    credentials = {}
    
    for vm in vms:
        vm_info = {
            "name": vm.get("vm_name", "Unknown"),
            "hostname": vm.get("hostname", "Unknown"),
            "template": vm.get("template", "Unknown"),
            "vlan": vm.get("vlan", "Unknown"),
            "ip_last_octet": vm.get("ip_last_octet", "Unknown"),
            "ram_gb": vm.get("ram_gb", 0),
            "cpus": vm.get("cpus", 0),
        }
        
        # Extract domain info if present
        domain = vm.get("domain", {})
        if domain:
            vm_info["domain"] = domain.get("fqdn")
            vm_info["domain_role"] = domain.get("role")
        
        # Extract roles
        roles = vm.get("roles", [])
        if roles:
            vm_info["roles"] = roles
        
        vm_list.append(vm_info)
        
        # Extract credentials from AD users if present
        role_vars = vm.get("role_vars", {})
        ludus_ad = role_vars.get("ludus_ad", {})
        ad_users = ludus_ad.get("users", [])
        
        if ad_users:
            for user in ad_users:
                username = user.get("name", "")
                password = user.get("password", "")
                if username and password:
                    credentials[username] = {
                        "password": password,
                        "display_name": user.get("display_name", username),
                        "groups": user.get("groups", []),
                        "description": user.get("description", ""),
                    }
    
    # Extract network information
    network_info = {
        "inter_vlan_default": network.get("inter_vlan_default", "REJECT"),
        "rules": network.get("rules", []),
    }
    
    # Generate attack paths based on vulnerabilities
    attack_paths = _generate_attack_paths(config, scenario_key)
    
    # Generate testing guide
    testing_guide = _generate_testing_guide(scenario_key, vm_list, credentials, attack_paths)
    
    # Build walkthrough
    walkthrough = {
        "scenario_info": {
            "scenario_key": scenario_key,
            "name": scenario_name,
            "customized": customized,
            "randomized": randomized,
            "customization_summary": customization_summary or "Default configuration",
        },
        "basic_info": {
            "vm_count": len(vm_list),
            "vms": vm_list,
            "network": network_info,
            "credentials": credentials,
        },
        "attack_paths": attack_paths,
        "testing_guide": testing_guide,
    }
    
    return walkthrough


def _generate_attack_paths(config: dict[str, Any], scenario_key: str) -> list[dict[str, Any]]:
    """Generate attack paths based on scenario configuration."""
    attack_paths = []
    
    # Check for AD scenarios
    vms = config.get("ludus", [])
    has_dc = any("dc" in vm.get("vm_name", "").lower() for vm in vms)
    has_adcs = any("adcs" in vm.get("vm_name", "").lower() for vm in vms)
    
    if has_dc:
        # Basic AD attack path
        attack_paths.append({
            "name": "Initial Access and Enumeration",
            "description": "Gain initial access and enumerate the Active Directory environment",
            "steps": [
                "1. Initial access via compromised workstation or vulnerable service",
                "2. Enumerate domain using tools like PowerView, BloodHound, or ADExplorer",
                "3. Identify high-value targets (Domain Admins, service accounts)",
                "4. Map attack paths using BloodHound",
            ],
            "expected_outcome": "Complete AD environment map with attack paths identified",
        })
        
        # Check for Kerberoasting opportunities
        role_vars = {}
        for vm in vms:
            if vm.get("roles"):
                role_vars.update(vm.get("role_vars", {}))
        
        ludus_ad = role_vars.get("ludus_ad", {})
        ad_users = ludus_ad.get("users", [])
        
        has_service_accounts = any(
            "svc_" in user.get("name", "").lower() or "service" in user.get("description", "").lower()
            for user in ad_users
        )
        
        if has_service_accounts:
            attack_paths.append({
                "name": "Kerberoasting Attack",
                "description": "Extract and crack service account passwords",
                "steps": [
                    "1. Identify service accounts with SPNs using PowerView: Get-DomainUser -SPN",
                    "2. Request service tickets: Rubeus.exe kerberoast /outfile:hashes.txt",
                    "3. Crack hashes using Hashcat: hashcat -m 13100 hashes.txt wordlist.txt",
                    "4. Use cracked credentials for lateral movement",
                ],
                "expected_outcome": "Compromised service account credentials",
            })
        
        # Check for AD CS vulnerabilities
        if has_adcs:
            attack_paths.append({
                "name": "AD CS Certificate Attack (ESC1)",
                "description": "Exploit misconfigured certificate templates",
                "steps": [
                    "1. Enumerate certificate templates: Certify.exe find /vulnerable",
                    "2. Request certificate with SAN: Certify.exe request /ca:CORP-CA /template:VulnerableUser /alt:Administrator",
                    "3. Convert certificate to PFX: Rubeus.exe asktgt /user:Administrator /certificate:cert.pfx",
                    "4. Use ticket for domain admin access",
                ],
                "expected_outcome": "Domain administrator access via certificate",
            })
    
    # Check for file server
    has_fileserver = any("file" in vm.get("vm_name", "").lower() for vm in vms)
    if has_fileserver:
        attack_paths.append({
            "name": "SMB Enumeration and Lateral Movement",
            "description": "Enumerate SMB shares and move laterally",
            "steps": [
                "1. Enumerate SMB shares: smbclient -L //FILES01 -U '' -N",
                "2. Access open shares: smbclient //FILES01/share -U 'user'",
                "3. Search for credentials: find . -name '*password*' -o -name '*cred*'",
                "4. Use found credentials for lateral movement",
            ],
            "expected_outcome": "Lateral movement to file server with credential access",
        })
    
    # Default attack path if none found
    if not attack_paths:
        attack_paths.append({
            "name": "General Penetration Testing",
            "description": "Standard penetration testing methodology",
            "steps": [
                "1. Reconnaissance and enumeration",
                "2. Vulnerability identification",
                "3. Exploitation",
                "4. Post-exploitation and privilege escalation",
            ],
            "expected_outcome": "Successful compromise and privilege escalation",
        })
    
    return attack_paths


def _generate_testing_guide(
    scenario_key: str,
    vm_list: list[dict[str, Any]],
    credentials: dict[str, Any],
    attack_paths: list[dict[str, Any]],
) -> dict[str, Any]:
    """Generate step-by-step testing guide."""
    
    # Find attacker VM (Kali)
    attacker_vm = None
    for vm in vm_list:
        if "kali" in vm.get("name", "").lower() or "attacker" in vm.get("name", "").lower():
            attacker_vm = vm
            break
    
    # Find domain controller
    dc_vm = None
    for vm in vm_list:
        if "dc" in vm.get("name", "").lower() and "domain" in vm.get("domain_role", "").lower():
            dc_vm = vm
            break
    
    prerequisites = [
        "Ludus range deployed and all VMs powered on",
        "Network connectivity verified",
        "SSH/RDP access configured",
    ]
    
    if attacker_vm:
        prerequisites.append(f"Access to attacker VM: {attacker_vm.get('hostname', 'Unknown')}")
    
    step_by_step = []
    
    # Step 1: Access and verify
    step_by_step.append({
        "step": 1,
        "title": "Access the Environment",
        "description": "Connect to the deployed range and verify all VMs are accessible",
        "commands": [
            "# Get SSH config",
            "ludus-fastmcp get_ssh_config",
            "",
            "# Get RDP configs",
            "ludus-fastmcp get_rdp_configs",
            "",
            "# Connect to attacker VM (example)",
            f"ssh {attacker_vm.get('hostname', 'kali') if attacker_vm else 'kali'}",
        ],
        "expected_result": "Successful connection to attacker VM and other VMs",
    })
    
    # Step 2: Initial enumeration
    if dc_vm:
        step_by_step.append({
            "step": 2,
            "title": "Enumerate Active Directory",
            "description": "Discover the AD environment structure and identify targets",
            "commands": [
                "# Install BloodHound (if not present)",
                "sudo apt-get update && sudo apt-get install -y bloodhound",
                "",
                "# Run SharpHound collector on domain-joined machine",
                "# Or use PowerView for enumeration:",
                "Get-DomainUser | Select-Object samaccountname, description",
                "Get-DomainGroup | Select-Object name, members",
                "Get-DomainComputer | Select-Object name, operatingsystem",
            ],
            "expected_result": "Complete AD environment enumeration with user, group, and computer lists",
        })
    
    # Step 3: Attack path execution
    if attack_paths:
        first_path = attack_paths[0]
        step_by_step.append({
            "step": 3,
            "title": f"Execute Attack Path: {first_path['name']}",
            "description": first_path["description"],
            "commands": [
                f"# {first_path['name']}",
            ] + [f"# {step}" for step in first_path["steps"]],
            "expected_result": first_path["expected_outcome"],
        })
    
    # Step 4: Credential usage
    if credentials:
        sample_user = list(credentials.keys())[0]
        sample_creds = credentials[sample_user]
        step_by_step.append({
            "step": 4,
            "title": "Use Discovered Credentials",
            "description": "Leverage discovered credentials for lateral movement",
            "commands": [
                f"# Example: Use credentials for RDP",
                f"xfreerdp /u:{sample_user} /p:{sample_creds['password']} /v:DC01",
                "",
                "# Or use with psexec for command execution",
                f"psexec.py corp.local/{sample_user}:{sample_creds['password']}@DC01 cmd",
            ],
            "expected_result": "Successful lateral movement using discovered credentials",
        })
    
    # Step 5: Privilege escalation
    step_by_step.append({
        "step": 5,
        "title": "Privilege Escalation",
        "description": "Escalate privileges to achieve domain administrator access",
        "commands": [
            "# Check for unquoted service paths",
            "Get-WmiObject win32_service | Where-Object {$_.PathName -notmatch '\"' -and $_.PathName -match ' '}",
            "",
            "# Check for writable service binaries",
            "Get-Acl 'C:\\Program Files\\*' | Format-List",
            "",
            "# Use BloodHound to find privilege escalation paths",
            "MATCH (u:User)-[:MemberOf*1..]->(g:Group) WHERE g.name = 'DOMAIN ADMINS' RETURN u.name",
        ],
        "expected_result": "Domain administrator access achieved",
    })
    
    return {
        "prerequisites": prerequisites,
        "step_by_step": step_by_step,
        "estimated_time": "2-4 hours for complete scenario",
        "difficulty": "Intermediate to Advanced",
    }

