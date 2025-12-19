# Safety

Safety features and best practices for Ludus FastMCP to prevent accidental data loss and ensure secure operations.

## Built-in Safety Features

### User-Scoped Operations

All destructive operations are scoped to specific users. Operations cannot affect:
- Other users' ranges
- System-wide settings
- Other users' API keys or data

### Explicit User ID Requirement

Destructive operations require explicit user identification:

```python
# Safe: Explicit user ID
delete_range(user_id="testuser", confirm=True)

# Rejected: No user ID
delete_range()  # Raises safety error
```

### Wildcard Protection

Mass deletion patterns are rejected:

```
# These patterns are rejected:
delete_range(user_id="*")
delete_range(user_id="all")
delete_range(user_id="%")
```

### Confirmation Requirements

Destructive operations require explicit confirmation:

```
Delete my range with confirmation
```

Without confirmation, destructive operations will not proceed.

### Audit Logging

All destructive operations are logged:

```
[DESTRUCTIVE OPERATION] Deleting range for user: testuser
[SAFETY] Using explicit userID parameter: testuser
```

Log levels:
- `WARNING` - Potentially dangerous operations
- `CRITICAL` - Irreversible operations (user deletion)

## Destructive Operations

### Range Deletion

**What it deletes:**
- All VMs in the range
- All snapshots
- All network configurations
- Range metadata

**Safety checks:**
1. Requires explicit user ID
2. Verifies current API key user
3. Confirms target range belongs to specified user
4. Logs operation details

**Example:**
```
Delete the range for user testuser with confirmation
```

### User Removal

**What it deletes:**
- User account
- All user's ranges
- All user's API keys
- All user's data

**Safety checks:**
1. Rejects empty user ID
2. Rejects wildcard patterns
3. Logs at CRITICAL level
4. Requires admin privileges

### Snapshot Removal

**What it deletes:**
- Specified snapshot
- Cannot be recovered

**Safety checks:**
1. Requires exact VM name
2. Requires exact snapshot name
3. Logs operation

## Best Practices

### Before Destructive Operations

1. **Verify target:**
   ```
   Show my range status
   ```

2. **Create backup snapshot:**
   ```
   Create snapshot of all VMs named pre-delete-backup
   ```

3. **Confirm correct user:**
   ```
   Show my user information
   ```

### During Operations

1. **Use explicit parameters:**
   ```
   Delete range for user testuser (not "delete all ranges")
   ```

2. **Monitor operations:**
   ```
   Show deployment status
   ```

3. **Check logs for warnings:**
   ```bash
   tail -f ~/.ludus-fastmcp/ludus-fastmcp.log
   ```

### Multi-User Environments

1. **Always specify user IDs** for operations that support them

2. **Use admin privileges carefully** - they can affect other users

3. **Review before confirming** destructive operations

4. **Maintain whitelist** for cleanup operations:
   ```
   Cleanup old ranges except admin and production
   ```

## Recovery Options

### After Accidental Deletion

1. **Check Ludus backups:**
   - Ludus may have automatic backups
   - Contact Ludus administrator

2. **Check Proxmox:**
   - VMs may still exist in Proxmox
   - Can be recovered from Proxmox interface

3. **Re-deploy scenario:**
   - All scenarios can be redeployed
   - Customizations will be lost

### Preventing Data Loss

1. **Regular snapshots:**
   ```
   Create snapshot of DC01 named daily-backup
   ```

2. **Export configurations:**
   ```
   Export my range configuration to YAML
   ```

3. **Document customizations** outside the system

## API Key Security

### Protection Measures

1. **Never commit keys to version control**
   - Add `.env` to `.gitignore`

2. **Use MCP client configuration**
   - Keys in client config are not exposed in shell history

3. **Rotate keys periodically:**
   ```bash
   ludus user apikey  # Generates new key
   ```

4. **Use separate keys** for development and production

### Key Storage

Recommended:
- MCP client configuration file
- Environment variables in secure locations

Not recommended:
- Shell history
- Version control
- Shared documents

## Operation Logging

### What Gets Logged

| Operation | Log Level | Details |
|-----------|-----------|---------|
| Range deletion | WARNING | User ID, timestamp |
| User removal | CRITICAL | User ID, timestamp |
| Snapshot removal | INFO | VM, snapshot name |
| Configuration changes | INFO | Changed fields |
| Authentication failures | WARNING | Attempted operation |

### Accessing Logs

```bash
# View all logs
cat ~/.ludus-fastmcp/ludus-fastmcp.log

# Filter destructive operations
grep "DESTRUCTIVE" ~/.ludus-fastmcp/ludus-fastmcp.log

# Monitor in real-time
tail -f ~/.ludus-fastmcp/ludus-fastmcp.log
```

## Limitations

### What Safety Features Do NOT Prevent

1. **Intentional deletion** - If you explicitly confirm, it proceeds

2. **Correct user, wrong range** - Verify before confirming

3. **Ludus API issues** - Cannot protect against upstream bugs

4. **Admin misuse** - Admins have elevated privileges

### User Responsibility

- Verify targets before destructive operations
- Maintain backups of important configurations
- Use confirmation prompts appropriately
- Monitor logs for unexpected operations

## Emergency Procedures

### Stop Active Deployment

```
Abort the current deployment
```

### Power Off All VMs

```
Power off all VMs in my range
```

### Check System State

```
Show my range status
Run health check
```

### Contact Support

For critical issues:
1. Collect logs: `~/.ludus-fastmcp/ludus-fastmcp.log`
2. Document the issue
3. Report via GitHub Issues

## Related Documentation

- [Getting Started](getting-started.md) - Installation and setup
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
- [Configuration](configuration.md) - Environment and client configuration
