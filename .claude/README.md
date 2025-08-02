# .claude Directory

This directory contains all Claude-specific configurations, commands, agents, and hooks for the CCDK Enhancement Kits integration.

## Directory Structure

- **commands/** - Custom slash commands for Claude
- **agents/** - Specialized AI agents for various development tasks
- **hooks/** - Event-driven hooks for session management and automation
- **config/** - Configuration files and settings
- **memory/** - Persistent memory storage for context retention
- **analytics/** - Usage analytics and performance metrics
- **templates/** - Reusable templates for commands and agents
- **docs/** - Documentation and guides
- **web/** - Web UI components and dashboard

## Usage

This directory is automatically recognized by Claude when working within this project. All commands, agents, and hooks are loaded and available for use.

## Contributing

When adding new functionality:
1. Place files in the appropriate subdirectory
2. Update the relevant settings.json if adding hooks
3. Document your additions in the subdirectory's README
4. Test cross-platform compatibility

## Security

Sensitive files are excluded via .gitignore. Never commit:
- API keys or secrets
- Database files
- Personal configuration
- Log files with sensitive data