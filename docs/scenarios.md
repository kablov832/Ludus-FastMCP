# Scenarios

Pre-built deployment scenarios available in Ludus FastMCP for security training and testing environments.

## Overview

Scenarios are pre-configured range templates that deploy complete lab environments. Each scenario includes VM definitions, network configurations, and post-deployment automation.

## Available Scenarios

### Active Directory

Basic to advanced Active Directory environments for penetration testing and security training.

#### ad-basic

Minimal Active Directory environment.

| Component | Description |
|-----------|-------------|
| Domain Controller | Windows Server with AD DS |
| Workstation | Domain-joined Windows client |
| Network | Single internal network |

**Use Cases:**
- AD enumeration practice
- Kerberos attack training
- Domain privilege escalation

**Deployment Time:** 20-30 minutes

```
Deploy the ad-basic scenario
```

#### ad-basic-fileserver

Active Directory with file server for share enumeration training.

| Component | Description |
|-----------|-------------|
| Domain Controller | Windows Server with AD DS |
| File Server | Windows Server with SMB shares |
| Workstation | Domain-joined Windows client |

**Use Cases:**
- SMB enumeration
- File share permissions testing
- Credential harvesting from shares

**Deployment Time:** 25-35 minutes

#### ad-basic-sql

Active Directory with SQL Server for database attack training.

| Component | Description |
|-----------|-------------|
| Domain Controller | Windows Server with AD DS |
| SQL Server | Windows Server with SQL Server |
| Workstation | Domain-joined Windows client |

**Use Cases:**
- SQL injection training
- Database enumeration
- Linked server attacks
- Kerberoasting (SQL service accounts)

**Deployment Time:** 30-40 minutes

#### ad-forest

Multi-domain forest environment.

| Component | Description |
|-----------|-------------|
| Forest Root DC | Parent domain controller |
| Child DC | Child domain controller |
| Workstations | Domain-joined clients |

**Use Cases:**
- Cross-domain attacks
- Trust relationship exploitation
- Forest-level privilege escalation

**Deployment Time:** 45-60 minutes

### GOAD-Style Environments

Environments inspired by the Game of Active Directory (GOAD) project.

#### goad-light

Lightweight GOAD-style environment.

| Component | Description |
|-----------|-------------|
| Domain Controllers | 2 DCs with trust |
| Workstations | Multiple domain-joined clients |
| Misconfigurations | Pre-configured vulnerabilities |

**Use Cases:**
- Realistic AD attack paths
- Multi-domain enumeration
- Credential relay attacks

**Deployment Time:** 45-60 minutes

#### goad-mini

Minimal GOAD configuration.

| Component | Description |
|-----------|-------------|
| Domain Controller | Single DC with vulnerabilities |
| Workstation | Client with local admin |

**Deployment Time:** 25-35 minutes

#### goad-full

Complete GOAD environment.

| Component | Description |
|-----------|-------------|
| Multiple Domains | 5 domain controllers |
| Trusts | Forest and external trusts |
| Workstations | 5+ client machines |
| Vulnerabilities | Full vulnerability suite |

**Use Cases:**
- Advanced AD penetration testing
- Red team training
- Attack chain practice

**Deployment Time:** 90-120 minutes

### Purple Team

Environments with both offensive and defensive capabilities.

#### purple-team-basic

Basic purple team lab with SIEM integration.

| Component | Description |
|-----------|-------------|
| Domain Controller | Windows Server with AD DS |
| Workstation | Domain-joined client |
| SIEM | Wazuh or Splunk |
| Attack Box | Kali Linux |

**Use Cases:**
- Detection engineering
- Alert tuning
- Attack simulation with monitoring

**Deployment Time:** 40-50 minutes

#### purple-team-advanced

Advanced purple team environment.

| Component | Description |
|-----------|-------------|
| AD Environment | Multi-VM AD setup |
| SIEM Platform | Full SIEM deployment |
| EDR | Endpoint detection |
| Attack Infrastructure | Multiple attack boxes |

**Use Cases:**
- SOC analyst training
- Detection rule development
- Incident response practice

**Deployment Time:** 60-90 minutes

### Web Applications

Vulnerable web application environments.

#### dvwa

Damn Vulnerable Web Application.

| Component | Description |
|-----------|-------------|
| Web Server | DVWA application |
| Database | MySQL backend |

**Use Cases:**
- SQL injection
- XSS practice
- CSRF exploitation
- File inclusion

**Deployment Time:** 15-20 minutes

#### owasp-top10

OWASP Top 10 vulnerabilities lab.

| Component | Description |
|-----------|-------------|
| Multiple Apps | Various vulnerable applications |
| Documentation | Attack guides |

**Use Cases:**
- Web application security training
- OWASP methodology practice

**Deployment Time:** 20-30 minutes

### Red Team

Offensive security focused environments.

#### redteam-lab-lite

Lightweight red team environment.

| Component | Description |
|-----------|-------------|
| Target Network | AD with vulnerabilities |
| Attack Box | Pre-configured Kali |

**Deployment Time:** 35-45 minutes

#### redteam-lab-full

Complete red team infrastructure.

| Component | Description |
|-----------|-------------|
| Target Environment | Full AD forest |
| C2 Infrastructure | Command and control setup |
| Pivot Points | Multiple network segments |

**Deployment Time:** 90-120 minutes

## SIEM Integration

Most scenarios support SIEM integration. Add monitoring during deployment:

```
Deploy ad-basic with Wazuh SIEM integration
```

### Supported SIEM Platforms

| Platform | Description |
|----------|-------------|
| Wazuh | Open source security platform |
| Splunk | Enterprise SIEM |
| Elastic | ELK stack |
| Security Onion | Network security monitoring |

## Scenario Operations

### List Available Scenarios

```
List available scenarios
```

### Preview Before Deployment

```
Preview the ad-basic scenario
```

Preview displays:
- VM specifications
- Network configuration
- Resource requirements
- Estimated deployment time

### Deploy a Scenario

```
Deploy the ad-basic scenario
```

### Deploy with Options

```
Deploy ad-basic with Wazuh and minimal resources
```

### Monitor Deployment Progress

```
Show deployment status
```

## Resource Profiles

Scenarios support resource profiles for different hardware capabilities.

| Profile | RAM per VM | CPU per VM | Use Case |
|---------|------------|------------|----------|
| minimal | 2-4 GB | 1-2 cores | Limited resources |
| recommended | 4-8 GB | 2-4 cores | Standard deployment |
| maximum | 8-16 GB | 4-8 cores | Performance testing |

```
Deploy ad-forest with minimal resource profile
```

## Custom Scenarios

Build custom scenarios from existing templates.

### Clone and Modify

```
Clone ad-basic and add a Kali Linux attack box
```

### Build from Scratch

```
Create a custom range with:
- 2 Windows Server 2022 DCs
- 3 Windows 11 workstations
- 1 Kali Linux
- Wazuh SIEM
```

### Export Configuration

```
Export my range configuration to YAML
```

## Post-Deployment Operations

After deployment completes:

### Create Snapshots

```
Create snapshots of all VMs named clean-state
```

### Enable Testing Mode

```
Start testing mode for my range
```

### Retrieve Access Information

```
Show SSH config for my range
Show RDP configurations
```

## Troubleshooting Deployments

### Check Status

```
Show deployment status
```

### View Logs

```
Show deployment logs
```

### Common Issues

**Deployment stuck:**
```
Abort the current deployment
```

**Partial failure:**
```
Resume deployment with tags user,domain
```

For additional solutions, see [Troubleshooting](troubleshooting.md).

## Related Documentation

- [Tools Reference](tools-reference.md) - Complete tool documentation
- [Getting Started](getting-started.md) - Installation and setup
- [Configuration](configuration.md) - Environment and client configuration
