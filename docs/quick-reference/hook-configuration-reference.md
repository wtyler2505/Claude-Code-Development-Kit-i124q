# Hook Configuration Reference

*Created by Tyler Walker (@wtyler2505) & Claude*

## Quick Setup

```bash
# Install all hooks
ccdk hook install

# Check status
ccdk hook status

# Uninstall if needed
ccdk hook uninstall
```

## Available Hooks

### Pre-commit Hooks
- ✅ **Code formatting** (Prettier, ESLint)
- ✅ **Linting** (Multiple languages)
- ✅ **Type checking** (TypeScript, Python)
- ✅ **Security scanning** (Basic vulnerability checks)

### Pre-push Hooks
- ✅ **Test execution** (Unit tests)
- ✅ **Build verification** (Compile check)
- ✅ **Coverage check** (Minimum thresholds)

### Post-merge Hooks
- ✅ **Dependency sync** (package.json changes)
- ✅ **Environment updates** (Config changes)

## Configuration Files

### `.ccdk/hooks.json`
```json
{
  "precommit": {
    "enabled": true,
    "formatters": ["prettier", "eslint"],
    "linters": ["eslint", "pylint"],
    "typecheck": true
  },
  "prepush": {
    "enabled": true,
    "runTests": true,
    "buildCheck": true,
    "coverageThreshold": 80
  }
}
```

### `.ccdk/hook-ignore`
```
# Patterns to ignore in hooks
*.min.js
dist/
build/
node_modules/
.env*
```

## Customization Options

### Hook Severity Levels
- **strict** - Fail on any issues
- **warning** - Show warnings, allow commit
- **disabled** - Skip specific checks

### Language-Specific Settings
```json
{
  "javascript": {
    "formatter": "prettier",
    "linter": "eslint",
    "config": ".eslintrc.js"
  },
  "python": {
    "formatter": "black",
    "linter": "pylint",
    "typecheck": "mypy"
  },
  "typescript": {
    "formatter": "prettier",
    "linter": "eslint",
    "typecheck": "tsc"
  }
}
```

## Troubleshooting

### Common Issues
| Problem | Solution |
|---------|----------|
| Hook not running | Check `ccdk hook status` |
| Formatting fails | Verify tool installation |
| Tests timeout | Increase timeout in config |
| Permission denied | Run `ccdk hook install` again |

### Performance Tuning
- Use `.ccdk/hook-ignore` for large files
- Set appropriate timeouts
- Enable parallel execution
- Cache dependencies when possible

### Quick Fixes
```bash
# Reinstall hooks
ccdk hook uninstall && ccdk hook install

# Skip hooks for emergency commit
git commit --no-verify -m "emergency fix"

# Test hooks manually
.git/hooks/pre-commit

# Reset hook config
ccdk config reset hooks
```