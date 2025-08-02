# CCDK i124q Integration Guide

*Created by Tyler Walker (@wtyler2505) & Claude*

This guide covers the integration of external services, MCP servers, and IDE configurations for CCDK i124q.

## Table of Contents
- [Task Master AI Integration](#task-master-ai-integration)
- [MCP Server Configuration](#mcp-server-configuration)
- [IDE-Specific Setup](#ide-specific-setup)
- [API Key Management](#api-key-management)
- [Troubleshooting](#troubleshooting)

---

## Task Master AI Integration

Task Master AI provides comprehensive project and task management capabilities through MCP protocol.

### Installation

Task Master is integrated via MCP configuration. No separate installation required.

### Configuration

1. **Initialize Task Master in your project**:
   ```bash
   task-master init
   ```

2. **Configure AI models**:
   ```bash
   task-master models --setup
   ```

3. **Parse PRD document** (if available):
   ```bash
   task-master parse-prd .taskmaster/docs/prd.txt
   ```

### Key Features

- **Task Management**: Create, update, and track development tasks
- **AI-Powered Expansion**: Break down complex tasks into subtasks
- **Dependency Tracking**: Manage task dependencies and prerequisites
- **Complexity Analysis**: Analyze and score task complexity
- **Research Mode**: Enhanced task generation with web research

### MCP Tools Available

```javascript
// Project setup
initialize_project()      // Initialize Task Master
parse_prd()              // Generate tasks from PRD

// Daily workflow
get_tasks()              // List all tasks
next_task()              // Get next available task
set_task_status()        // Update task status

// Task management
add_task()               // Create new task
expand_task()            // Break into subtasks
update_task()            // Modify task details

// Analysis
analyze_project_complexity()  // Complexity scoring
complexity_report()          // View analysis
```

---

## MCP Server Configuration

### Overview

CCDK i124q supports multiple MCP servers for enhanced functionality:

1. **Task Master AI** - Project and task management
2. **Context7** - Real-time library documentation
3. **Gemini Assistant** - Architectural consultation
4. **Custom MCP Servers** - Additional integrations

### Claude Code Configuration

Add to `.claude/mcp.json`:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}",
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/mcp-server-context7"],
      "env": {
        "UPSTASH_VECTOR_REST_URL": "${UPSTASH_VECTOR_REST_URL}",
        "UPSTASH_VECTOR_REST_TOKEN": "${UPSTASH_VECTOR_REST_TOKEN}"
      }
    },
    "gemini-assistant": {
      "command": "npx",
      "args": ["-y", "mcp-gemini-assistant"],
      "env": {
        "GOOGLE_API_KEY": "${GOOGLE_API_KEY}"
      }
    }
  }
}
```

### Environment Variables

Set these in your shell profile or `.env` file:

```bash
# Core AI Providers
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"

# Research & Analysis
export PERPLEXITY_API_KEY="your-key-here"

# Context7 (if using)
export UPSTASH_VECTOR_REST_URL="your-url-here"
export UPSTASH_VECTOR_REST_TOKEN="your-token-here"

# Additional Providers (optional)
export XAI_API_KEY="your-key-here"
export MISTRAL_API_KEY="your-key-here"
export OPENROUTER_API_KEY="your-key-here"
```

---

## IDE-Specific Setup

CCDK i124q provides configurations for multiple IDE tools that support MCP.

### Cursor

Configuration location: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        // API keys configuration
      }
    }
  }
}
```

### Windsurf

Configuration location: `.windsurf/mcp.json`

Similar structure to Cursor configuration.

### Roo

Configuration location: `.roo/mcp.json`

Similar structure to Cursor configuration.

### VSCode (via extensions)

While VSCode doesn't natively support MCP, you can use:
- Claude Code CLI for terminal-based interaction
- Custom extensions that implement MCP protocol

---

## API Key Management

### Required Keys

At minimum, you need **one** of these for basic functionality:
- `ANTHROPIC_API_KEY` (Recommended for Claude models)
- `OPENAI_API_KEY` (For GPT models)
- `GOOGLE_API_KEY` (For Gemini models)

### Recommended Keys

For full functionality:
- `PERPLEXITY_API_KEY` - Enables research mode in Task Master
- `GOOGLE_API_KEY` - Enables Gemini consultations
- Context7 credentials - For real-time documentation

### Security Best Practices

1. **Never commit API keys**:
   ```bash
   # Add to .gitignore
   .env
   .env.local
   *.key
   ```

2. **Use environment variables**:
   ```bash
   # .env.example (commit this)
   ANTHROPIC_API_KEY=your-key-here
   
   # .env (don't commit this)
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Rotate keys regularly**:
   - Set up key rotation reminders
   - Use separate keys for development/production
   - Monitor usage for anomalies

4. **Use the security hook**:
   - The `mcp-security-scan` hook prevents accidental key exposure
   - Automatically scans before external AI calls

---

## Model Configuration

### Task Master Model Roles

Task Master uses three model roles:

1. **Main Model** - Primary task generation/updates
2. **Research Model** - Web-enhanced operations
3. **Fallback Model** - Backup when primary fails

### Configure Models

Interactive setup:
```bash
task-master models --setup
```

Manual configuration:
```bash
# Set specific models
task-master models --set-main claude-3-5-sonnet-20241022
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
task-master models --set-fallback gpt-4o-mini
```

### Model Router

The `model_router.json` file defines available models:

```json
{
  "providers": {
    "anthropic": {
      "models": [
        "claude-sonnet-4-20250514",
        "claude-opus-4-20250514"
      ]
    },
    "openai": {
      "models": ["gpt-4o-mini"]
    }
  },
  "default": "anthropic:claude-sonnet-4-20250514"
}
```

---

## Integration Workflows

### Initial Project Setup

1. **Install CCDK i124q**:
   ```bash
   git clone https://github.com/wtyler2505/Claude-Code-Development-Kit-i124q.git
   cd Claude-Code-Development-Kit-i124q
   ./setup.sh
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Initialize Task Master**:
   ```bash
   task-master init
   ```

4. **Configure MCP servers**:
   ```bash
   # Copy appropriate config for your IDE
   cp .cursor/mcp.json ~/.cursor/mcp.json
   ```

### Daily Development Flow

1. **Start Claude Code**:
   ```bash
   claude
   ```

2. **Check next task**:
   ```bash
   /full-context "show next task from Task Master"
   ```

3. **Work on implementation**:
   ```bash
   /swarm-run "implement task requirements"
   ```

4. **Update documentation**:
   ```bash
   /update-docs "document implementation"
   ```

### Advanced Integrations

#### Hive-Mind Sessions
```bash
# Start persistent session
/hive-start feature-auth

# Work across multiple terminals
# Terminal 1: Backend work
# Terminal 2: Frontend work
# Terminal 3: Testing

# Check status
/hive-status
```

#### Analytics Dashboard
```bash
# Start analytics server
python dashboard/app.py

# View at http://localhost:5000
```

#### Web UI
```bash
# Start web interface
/webui-start

# Access at http://localhost:7000
```

---

## Troubleshooting

### MCP Connection Issues

1. **Check MCP configuration**:
   ```bash
   cat ~/.claude/mcp.json
   ```

2. **Verify Node.js installation**:
   ```bash
   node --version  # Should be 18+
   npm --version
   ```

3. **Test MCP server**:
   ```bash
   npx -y --package=task-master-ai task-master-ai
   ```

4. **Enable debug mode**:
   ```bash
   claude --mcp-debug
   ```

### API Key Issues

1. **Verify environment variables**:
   ```bash
   echo $ANTHROPIC_API_KEY
   ```

2. **Check key permissions**:
   - Ensure keys have necessary scopes
   - Verify billing is active

3. **Test with CLI**:
   ```bash
   task-master models  # Should show configured models
   ```

### Task Master Issues

1. **Reinitialize if needed**:
   ```bash
   task-master init --force
   ```

2. **Fix dependencies**:
   ```bash
   task-master fix-dependencies
   ```

3. **Regenerate task files**:
   ```bash
   task-master generate
   ```

### Hook Failures

1. **Check hook logs**:
   ```bash
   ls -la logs/
   cat logs/hooks.log
   ```

2. **Disable problematic hooks**:
   Edit `.claude/settings.json` and remove hook entry

3. **Test hooks individually**:
   ```bash
   node .claude/hooks/test-runner.js
   ```

---

## Best Practices

1. **Start with core features** - Don't enable everything at once
2. **Monitor API usage** - Set up billing alerts
3. **Use research mode sparingly** - It consumes more tokens
4. **Keep documentation current** - Use `/update-docs` regularly
5. **Leverage hive sessions** - For complex multi-part features
6. **Review analytics** - Identify bottlenecks and optimize

---

*Integration guide maintained by Tyler Walker (@wtyler2505) & Claude*