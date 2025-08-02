# Troubleshooting Guide

*Created by Tyler Walker (@wtyler2505) & Claude*

## Quick Diagnostics

```bash
# Check overall system status
ccdk status

# View detailed logs
ccdk dev logs

# Verify configuration
ccdk config show

# Test agent connectivity
ccdk agent list
```

## Common Issues & Fixes

### Agent Problems

| Issue | Quick Fix |
|-------|-----------|
| Agent won't start | `ccdk agent restart <name>` |
| Agent crashes | Check logs: `ccdk dev logs` |
| Agent unresponsive | `ccdk agent stop <name>` then start |
| Multiple agents conflict | Stop all: `ccdk agent stop --all` |

### Configuration Issues

| Issue | Quick Fix |
|-------|-----------|
| Config corrupted | `ccdk config reset` |
| Settings not saving | Check file permissions |
| Wrong paths | `ccdk config set <key> <new-path>` |
| Missing dependencies | Reinstall: `npm install -g ccdk` |

### Hook Problems

| Issue | Quick Fix |
|-------|-----------|
| Hooks not running | `ccdk hook install` |
| Hook failures | Check `.ccdk/hook-ignore` |
| Permission errors | Run as admin/sudo |
| Git hook conflicts | `ccdk hook uninstall` then reinstall |

### Development Environment

| Issue | Quick Fix |
|-------|-----------|
| Dev server won't start | `ccdk dev stop && ccdk dev start` |
| Port conflicts | Change port in config |
| Build failures | Clear cache: `npm run clean` |
| Module not found | `npm install` or `pip install` |

## Emergency Commands

### System Reset
```bash
# Nuclear option - reset everything
ccdk config reset
ccdk hook uninstall
ccdk agent stop --all
ccdk dev stop

# Then reconfigure
ccdk hook install
ccdk config set <required-settings>
```

### Debugging Steps
1. **Check status:** `ccdk status`
2. **View logs:** `ccdk dev logs --verbose`
3. **Verify config:** `ccdk config show`
4. **Test agents:** `ccdk agent info <name>`
5. **Check hooks:** `ccdk hook status`

### Log Locations
- **Main logs:** `~/.ccdk/logs/`
- **Agent logs:** `~/.ccdk/agents/<name>/logs/`
- **Hook logs:** `.git/hooks/logs/`
- **Dev logs:** `./dev-server.log`

## Performance Issues

### Slow Performance
- Check system resources
- Reduce agent count
- Clear log files
- Restart development server

### Memory Issues
```bash
# Check memory usage
ccdk status --memory

# Stop resource-heavy agents
ccdk agent stop claude-coder
ccdk agent stop cursor-composer

# Restart with lighter config
ccdk dev start --light-mode
```

### Network Issues
- Check internet connectivity
- Verify API endpoints
- Test with: `ccdk agent info --test-connection`
- Configure proxy if needed

## Getting Help

### Self-Diagnosis
```bash
# Generate diagnostic report
ccdk status --full-report > diagnosis.txt

# Test all systems
ccdk dev start --test-mode

# Validate installation
ccdk version --check-integrity
```

### Support Information
- 📧 **Issues:** GitHub issues page
- 📚 **Docs:** `/docs/` directory
- 🔧 **Config:** `ccdk config show`
- 📊 **Logs:** `ccdk dev logs --export`

### Before Reporting Issues
1. Run `ccdk status --full-report`
2. Check recent logs
3. Try system reset
4. Document reproduction steps
5. Include system information