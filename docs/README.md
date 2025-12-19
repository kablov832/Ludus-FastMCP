# Ludus FastMCP Documentation

Documentation for Ludus FastMCP - MCP server for Ludus cyber range automation with 157 tools across 15 modules.

## Contents

### Getting Started

| Document | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | Installation, setup, and first deployment |
| [Configuration](configuration.md) | Environment variables and MCP client setup |

### Reference

| Document | Description |
|----------|-------------|
| [Tools Reference](tools-reference.md) | Complete documentation for all 157 tools |
| [Scenarios](scenarios.md) | Pre-built deployment scenarios |

### Operations

| Document | Description |
|----------|-------------|
| [Troubleshooting](troubleshooting.md) | Common issues and solutions |
| [Safety](safety.md) | Safety features and best practices |

## Quick Reference

### Installation

```bash
# Using pipx (recommended)
pipx install git+https://github.com/tjnull/ludus-mcp-python.git

# From source
git clone https://github.com/tjnull/ludus-mcp-python.git
cd ludus-mcp-python
pip install -e .
```

### Interactive Setup

Run the setup wizard to configure credentials and generate MCP client configurations:

```bash
ludus-fastmcp --setup
```

### Manual Configuration

```bash
export LUDUS_API_URL="https://your-ludus-instance:8080"
export LUDUS_API_KEY="username.your-api-key"
```

### Verify Installation

```bash
ludus-fastmcp --version
ludus-fastmcp --list-tools
```

### MCP Client Configuration

Configuration file locations:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ludus": {
      "command": "ludus-fastmcp",
      "env": {
        "LUDUS_API_URL": "https://your-ludus-instance:8080",
        "LUDUS_API_KEY": "username.your-api-key"
      }
    }
  }
}
```

### ludus-ai Client

```bash
ludus-ai setup-llm              # Configure local LLM (Ollama)
ludus-ai install anythingllm    # Install AnythingLLM interface
ludus-ai tool list-tools        # List available tools
ludus-ai tool call-tool <name>  # Execute tools directly
```

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| Core Operations | 16 | Range, snapshot, power, network, template management |
| Deployment | 12 | Scenario deployment, orchestration, monitoring |
| User Management | 5 | User accounts, API keys, access control |
| Security Integration | 16 | SIEM configuration, compliance, vulnerability |
| Templates Advanced | 13 | Template discovery, creation, building |
| Metrics and Monitoring | 17 | Performance, health checks, inventory |
| Automation | 11 | Pipelines, scheduling, bulk operations |
| Integrations | 4 | Webhooks, Slack, Jira, Git |
| Documentation | 4 | Lab guides, attack paths, playbooks |
| Collaboration | 11 | Sharing, resources, community |
| Custom Builder | 18 | Skeleton templates, custom OS/containers |
| Range Management | 6 | List, search, delete, cleanup |
| AI Config Generation | 8 | Natural language to YAML |
| Profile Transformation | 5 | Adversary/defender profiles |
| Role Management | 11 | Ansible Galaxy, custom roles |

## External Resources

| Resource | Link |
|----------|------|
| Ludus Documentation | [docs.ludus.cloud](https://docs.ludus.cloud) |
| Ludus GitHub | [github.com/badsectorlabs/ludus](https://github.com/badsectorlabs/ludus) |
| FastMCP Framework | [gofastmcp.com](https://gofastmcp.com) |
| MCP Protocol | [modelcontextprotocol.io](https://modelcontextprotocol.io) |

## Support

| Resource | Link |
|----------|------|
| GitHub Issues | [github.com/tjnull/ludus-mcp-python/issues](https://github.com/tjnull/ludus-mcp-python/issues) |
| GitHub Discussions | [github.com/tjnull/ludus-mcp-python/discussions](https://github.com/tjnull/ludus-mcp-python/discussions) |
