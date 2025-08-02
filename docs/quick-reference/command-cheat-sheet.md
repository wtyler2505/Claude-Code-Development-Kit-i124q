# Command Cheat Sheet

*Created by Tyler Walker (@wtyler2505) & Claude*

## Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ccdk help` | Show available commands | `ccdk help` |
| `ccdk version` | Show version info | `ccdk version` |
| `ccdk status` | Check system status | `ccdk status` |

## Agent Management

| Command | Description | Example |
|---------|-------------|---------|
| `ccdk agent list` | List available agents | `ccdk agent list` |
| `ccdk agent info <name>` | Show agent details | `ccdk agent info claude-coder` |
| `ccdk agent start <name>` | Start an agent | `ccdk agent start cursor-composer` |
| `ccdk agent stop <name>` | Stop running agent | `ccdk agent stop claude-coder` |
| `ccdk agent restart <name>` | Restart an agent | `ccdk agent restart cursor-composer` |

## Configuration

| Command | Description | Example |
|---------|-------------|---------|
| `ccdk config show` | Display current config | `ccdk config show` |
| `ccdk config set <key> <value>` | Set config value | `ccdk config set theme dark` |
| `ccdk config reset` | Reset to defaults | `ccdk config reset` |

## Development Tools

| Command | Description | Example |
|---------|-------------|---------|
| `ccdk dev start` | Start dev environment | `ccdk dev start` |
| `ccdk dev stop` | Stop dev environment | `ccdk dev stop` |
| `ccdk dev logs` | View development logs | `ccdk dev logs` |

## Hook Management

| Command | Description | Example |
|---------|-------------|---------|
| `ccdk hook install` | Install git hooks | `ccdk hook install` |
| `ccdk hook uninstall` | Remove git hooks | `ccdk hook uninstall` |
| `ccdk hook status` | Check hook status | `ccdk hook status` |

## Quick Tips

- Use `--help` with any command for detailed options
- Add `--verbose` for detailed output
- Use `--quiet` to suppress non-essential output
- Commands support both short and long forms where applicable