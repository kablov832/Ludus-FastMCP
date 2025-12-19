# Troubleshooting

Common issues and solutions for Ludus FastMCP.

## Connection Issues

### Cannot Connect to Ludus Server

**Symptoms:**
- "Connection refused" error
- "Cannot connect to Ludus server" message
- Timeout errors

**Solutions:**

1. Verify the Ludus server URL is correct:
   ```bash
   echo $LUDUS_API_URL
   ```

2. Test connectivity directly:
   ```bash
   curl -k $LUDUS_API_URL
   ```

3. Check if VPN connection is required and active

4. Verify firewall allows connection to Ludus port (typically 8080)

5. Confirm Ludus server is running:
   ```bash
   # On Ludus server
   systemctl status ludus
   ```

### Authentication Failed

**Symptoms:**
- "Authentication failed" error
- 401 Unauthorized response
- "Invalid API key" message

**Solutions:**

1. Regenerate API key on Ludus server:
   ```bash
   ludus user apikey
   ```

2. Verify key format is `username.key-value`:
   ```bash
   echo $LUDUS_API_KEY
   # Should output: username.abc123def456...
   ```

3. Check for whitespace in configuration:
   - Remove leading/trailing spaces from API key
   - Ensure no line breaks in environment variables

4. Verify key in MCP client config matches exactly

### SSL Certificate Errors

**Symptoms:**
- SSL verification failed
- Certificate errors
- HTTPS connection issues

**Solutions:**

1. For self-signed certificates (default for most Ludus installations):
   ```bash
   export LUDUS_SSL_VERIFY=false
   ```

2. Add to MCP client configuration:
   ```json
   {
     "env": {
       "LUDUS_SSL_VERIFY": "false"
     }
   }
   ```

3. For production with valid certificates:
   ```bash
   export LUDUS_SSL_VERIFY=true
   ```

## MCP Client Issues

### Tools Not Appearing in AI Client

**Symptoms:**
- AI assistant does not recognize Ludus commands
- No tools available message
- MCP server not connected

**Solutions:**

1. Verify server works independently:
   ```bash
   ludus-fastmcp --list-tools
   # Should show 157 tools
   ```

2. Check MCP client configuration:
   - Verify JSON syntax is valid
   - Ensure command path is correct
   - Confirm environment variables are set

3. Use full path to executable if needed:
   ```json
   {
     "command": "/home/user/.local/bin/ludus-fastmcp"
   }
   ```

4. Restart AI client completely:
   - Claude Desktop: Quit application and reopen (not just close window)
   - VS Code: Developer > Reload Window

5. Reinstall if necessary:
   ```bash
   pipx reinstall ludus-fastmcp
   ```

### Wrong Python Version

**Symptoms:**
- Import errors
- Syntax errors
- Module not found

**Solutions:**

1. Verify Python version:
   ```bash
   python --version
   # Must be 3.11 or higher
   ```

2. Use specific Python version with pipx:
   ```bash
   pipx install --python python3.11 git+https://github.com/tjnull/ludus-mcp-python.git
   ```

## Deployment Issues

### Deployment Stuck or Failing

**Symptoms:**
- Deployment not progressing
- Repeated failures in logs
- Timeout waiting for VMs

**Solutions:**

1. Check deployment status:
   ```
   Show deployment status
   ```

2. View deployment logs:
   ```
   Show deployment logs
   ```

3. Abort and retry:
   ```
   Abort the current deployment
   ```

4. Resume with specific tags:
   ```
   Resume deployment with tags user,domain
   ```

### Active Directory Services Not Ready

**Symptoms:**
- "Active Directory Web Services not running" error
- Domain join failures
- DNS resolution issues

**Solutions:**

1. This is typically a transient error during DC initialization

2. Wait 5-10 minutes for AD services to start

3. Check VM power state:
   ```
   Show my range status
   ```

4. Ludus automatically retries failed tasks

### Template Not Found

**Symptoms:**
- "Template not found" error
- VM creation fails
- Invalid template name

**Solutions:**

1. List available templates:
   ```
   List available templates
   ```

2. Verify template name spelling (case-sensitive)

3. Check if template is built:
   ```
   Show template status
   ```

### Insufficient Resources

**Symptoms:**
- "Out of memory" errors
- VM creation fails
- Storage full messages

**Solutions:**

1. Use minimal resource profile:
   ```
   Deploy ad-basic with minimal resources
   ```

2. Power off unused ranges:
   ```
   Power off all VMs in my range
   ```

3. Delete unused ranges:
   ```
   Delete old test ranges
   ```

4. Check Proxmox dashboard for resource usage

## Server Issues

### Daemon Not Starting

**Symptoms:**
- Daemon command returns error
- PID file issues
- Port already in use

**Solutions:**

1. Check if already running:
   ```bash
   ludus-fastmcp --status
   ```

2. Stop existing daemon:
   ```bash
   ludus-fastmcp --stop-daemon
   ```

3. Remove stale PID file if necessary:
   ```bash
   rm ~/.ludus-fastmcp/ludus-fastmcp.pid
   ```

4. Check logs for errors:
   ```bash
   cat ~/.ludus-fastmcp/ludus-fastmcp.log
   ```

### Rate Limit Exceeded

**Symptoms:**
- "Rate limit exceeded" error
- 429 response code
- Requests being blocked

**Solutions:**

1. Wait 30-60 seconds before retrying

2. Reduce request frequency

3. Check for duplicate requests in automation

## Permission Issues

### Permission Denied

**Symptoms:**
- 403 Forbidden response
- "Permission denied" error
- Admin-only operation failed

**Solutions:**

1. Verify your user has required permissions:
   ```
   Show my user information
   ```

2. Some operations require admin privileges:
   - User management
   - System-wide template operations
   - Viewing other users' ranges

3. Contact Ludus administrator for elevated access

## Diagnostic Commands

### Check Server Health

```bash
# Verify installation
ludus-fastmcp --version

# List tools
ludus-fastmcp --list-tools

# Verbose startup
ludus-fastmcp --verbose
```

### Check Environment

```bash
# Verify environment variables
env | grep LUDUS

# Test API directly
curl -k -H "X-API-KEY: $LUDUS_API_KEY" $LUDUS_API_URL/
```

### Check Logs

```bash
# Daemon logs
tail -f ~/.ludus-fastmcp/ludus-fastmcp.log

# Filter for errors
grep ERROR ~/.ludus-fastmcp/ludus-fastmcp.log
```

### Health Check Tool

Use the built-in health check:

```
Run a health check on Ludus connection
```

Returns:
- Server status
- API connectivity
- Response latency
- Rate limiter status

## ludus-ai Client Issues

### LLM Connection Failed

**Symptoms:**
- Cannot connect to local LLM
- Ollama not responding
- Model not found

**Solutions:**

1. Verify Ollama is running:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. Check model is installed:
   ```bash
   ollama list
   ```

3. Reconfigure LLM settings:
   ```bash
   ludus-ai setup-llm
   ```

### Tool Execution Timeout

**Symptoms:**
- Tool calls timing out
- Long-running operations failing

**Solutions:**

1. Increase timeout for complex operations
2. Check network connectivity to Ludus server
3. Verify server is not overloaded

## Getting Help

If issues persist:

1. Enable debug logging:
   ```bash
   export LOG_LEVEL=DEBUG
   ludus-fastmcp --verbose
   ```

2. Collect diagnostic information:
   - Python version
   - Ludus FastMCP version
   - Error messages
   - Relevant log output

3. Report issues:
   - [GitHub Issues](https://github.com/tjnull/ludus-mcp-python/issues)
   - Include steps to reproduce
   - Include diagnostic output

## Related Documentation

- [Getting Started](getting-started.md) - Installation and setup
- [Configuration](configuration.md) - Environment and client configuration
- [Safety](safety.md) - Safety features and best practices
