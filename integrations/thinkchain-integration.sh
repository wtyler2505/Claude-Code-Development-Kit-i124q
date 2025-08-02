#!/usr/bin/env bash

# CCDK i124q - ThinkChain Integration Module
# Seamlessly integrates ThinkChain's advanced streaming capabilities
# Version 1.0.0

set -euo pipefail

# =============================================================================
# CONFIGURATION
# =============================================================================

THINKCHAIN_DIR="${THINKCHAIN_DIR:-/c/Users/wtyle/thinkchain}"
CCDK_DIR="${CCDK_DIR:-$HOME/.claude}"
INTEGRATION_VERSION="1.0.0"

# Colors
readonly COLOR_SUCCESS='\033[38;5;82m'
readonly COLOR_INFO='\033[38;5;87m'
readonly COLOR_WARNING='\033[38;5;214m'
readonly COLOR_ERROR='\033[38;5;196m'
readonly NC='\033[0m'
readonly BOLD='\033[1m'

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

print_header() {
    echo -e "\n${COLOR_INFO}${BOLD}═══════════════════════════════════════════════════${NC}"
    echo -e "${COLOR_INFO}${BOLD}  🔗 ThinkChain Integration for CCDK i124q${NC}"
    echo -e "${COLOR_INFO}${BOLD}═══════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${COLOR_SUCCESS}✓ $1${NC}"
}

print_info() {
    echo -e "${COLOR_INFO}ℹ $1${NC}"
}

print_warning() {
    echo -e "${COLOR_WARNING}⚠ $1${NC}"
}

print_error() {
    echo -e "${COLOR_ERROR}✗ $1${NC}"
}

# =============================================================================
# DETECTION FUNCTIONS
# =============================================================================

detect_thinkchain() {
    print_info "Detecting ThinkChain installation..."
    
    if [ -d "$THINKCHAIN_DIR" ]; then
        if [ -f "$THINKCHAIN_DIR/thinkchain.py" ]; then
            print_success "ThinkChain found at: $THINKCHAIN_DIR"
            return 0
        else
            print_error "ThinkChain directory exists but thinkchain.py not found"
            return 1
        fi
    else
        print_warning "ThinkChain not found at: $THINKCHAIN_DIR"
        print_info "You can install it with: git clone https://github.com/martinbowling/ThinkChain.git $THINKCHAIN_DIR"
        return 1
    fi
}

check_python_requirements() {
    print_info "Checking Python environment..."
    
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version | cut -d' ' -f2)
        print_success "Python $python_version detected"
    else
        print_error "Python 3 is required but not found"
        return 1
    fi
    
    # Check for uv (preferred) or pip
    if command -v uv &> /dev/null; then
        print_success "uv package manager detected (recommended)"
        PACKAGE_MANAGER="uv"
    elif command -v pip3 &> /dev/null; then
        print_success "pip package manager detected"
        PACKAGE_MANAGER="pip3"
    else
        print_error "No Python package manager found (uv or pip required)"
        return 1
    fi
}

# =============================================================================
# CONFIGURATION FUNCTIONS
# =============================================================================

configure_api_key() {
    print_info "Configuring Anthropic API key..."
    
    # Check if API key is already configured
    if [ -f "$THINKCHAIN_DIR/.env" ]; then
        if grep -q "ANTHROPIC_API_KEY=" "$THINKCHAIN_DIR/.env"; then
            print_success "API key already configured in .env"
            echo -n "Do you want to update it? (y/n): "
            read -r update_key
            if [ "$update_key" != "y" ]; then
                return 0
            fi
        fi
    fi
    
    # Prompt for API key
    echo -e "\n${COLOR_WARNING}${BOLD}Important: ThinkChain requires an Anthropic API key${NC}"
    echo -e "${COLOR_INFO}This is different from your Claude.ai account.${NC}"
    echo -e "${COLOR_INFO}You can get an API key from: https://console.anthropic.com/${NC}\n"
    
    echo -n "Enter your Anthropic API key (or press Enter to skip): "
    read -rs api_key
    echo
    
    if [ -n "$api_key" ]; then
        echo "ANTHROPIC_API_KEY=$api_key" > "$THINKCHAIN_DIR/.env"
        print_success "API key configured successfully"
    else
        print_warning "Skipping API key configuration - you'll need to set it later"
    fi
}

setup_mcp_integration() {
    print_info "Setting up MCP integration..."
    
    # Create enhanced MCP configuration
    cat > "$THINKCHAIN_DIR/mcp_config_enhanced.json" << 'EOF'
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./test.db"],
      "description": "SQLite database operations",
      "enabled": true
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/c/Users/wtyle"],
      "description": "File system operations",
      "enabled": true
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": ""
      },
      "description": "GitHub API integration",
      "enabled": false
    },
    "taskmaster": {
      "command": "node",
      "args": ["./mcp-servers/taskmaster/index.js"],
      "description": "Task Master AI integration",
      "enabled": false
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "description": "Knowledge graph memory",
      "enabled": true
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
      "description": "Web browser automation",
      "enabled": false
    },
    "brave-search": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": ""
      },
      "description": "Brave search API",
      "enabled": false
    }
  }
}
EOF
    
    print_success "Enhanced MCP configuration created"
}

# =============================================================================
# INTEGRATION FUNCTIONS
# =============================================================================

create_ccdk_bridge() {
    print_info "Creating CCDK-ThinkChain bridge..."
    
    # Create bridge directory
    mkdir -p "$CCDK_DIR/thinkchain"
    
    # Create bridge script
    cat > "$CCDK_DIR/thinkchain/bridge.py" << 'EOF'
#!/usr/bin/env python3
"""
CCDK-ThinkChain Bridge
Allows Claude Code to trigger ThinkChain operations
"""

import os
import sys
import json
import subprocess
from pathlib import Path

THINKCHAIN_DIR = Path("/c/Users/wtyle/thinkchain")
sys.path.insert(0, str(THINKCHAIN_DIR))

def run_thinkchain_command(command: str, mode: str = "cli"):
    """Execute a ThinkChain command"""
    try:
        # Set up environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(THINKCHAIN_DIR)
        
        # Choose the appropriate script
        script = "thinkchain_cli.py" if mode == "cli" else "thinkchain.py"
        
        # Run ThinkChain with the command
        result = subprocess.run(
            [sys.executable, str(THINKCHAIN_DIR / script)],
            input=command,
            text=True,
            capture_output=True,
            env=env
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

def list_available_tools():
    """List all available ThinkChain tools"""
    try:
        from tool_discovery import list_tools
        tools = list_tools()
        return {"success": True, "tools": tools}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CCDK-ThinkChain Bridge")
    parser.add_argument("action", choices=["run", "list", "test"])
    parser.add_argument("--command", help="Command to run")
    parser.add_argument("--mode", default="cli", choices=["cli", "ui"])
    
    args = parser.parse_args()
    
    if args.action == "run" and args.command:
        result = run_thinkchain_command(args.command, args.mode)
        print(json.dumps(result, indent=2))
    elif args.action == "list":
        result = list_available_tools()
        print(json.dumps(result, indent=2))
    elif args.action == "test":
        print("ThinkChain bridge is working!")
EOF
    
    chmod +x "$CCDK_DIR/thinkchain/bridge.py"
    print_success "CCDK-ThinkChain bridge created"
}

create_claude_commands() {
    print_info "Creating Claude Code commands for ThinkChain..."
    
    mkdir -p "$CCDK_DIR/commands"
    
    # Create /think command
    cat > "$CCDK_DIR/commands/think.md" << 'EOF'
# /think - Advanced Thinking with ThinkChain

Trigger ThinkChain's advanced streaming capabilities with interleaved thinking.

## Usage
```
/think [prompt]
```

## Features
- Interleaved thinking - Step-by-step problem solving
- Fine-grained tool streaming - Live progress updates
- Multiple tool calls per turn
- MCP server integration

## Examples
```
/think Create a Python web scraper that monitors price changes
/think Analyze this codebase and suggest improvements
/think Build a CLI tool with progress bars and rich formatting
```

## Configuration
ThinkChain settings can be adjusted in:
- `~/.claude/thinkchain/config.json`
- `~/thinkchain/.env` (for API key)
EOF
    
    # Create /tools command
    cat > "$CCDK_DIR/commands/tools.md" << 'EOF'
# /tools - ThinkChain Tool Management

Manage and discover ThinkChain tools.

## Usage
```
/tools list              - List all available tools
/tools refresh           - Refresh tool discovery
/tools enable [name]     - Enable a specific tool
/tools disable [name]    - Disable a specific tool
/tools create [spec]     - Create a new tool dynamically
```

## Available Tools
- File operations (create, edit, read)
- Web scraping and search
- Package management (uv)
- Weather information
- MCP server tools
- And more discovered dynamically!
EOF
    
    print_success "Claude Code commands created"
}

install_dependencies() {
    print_info "Installing ThinkChain dependencies..."
    
    cd "$THINKCHAIN_DIR"
    
    if [ "$PACKAGE_MANAGER" = "uv" ]; then
        print_info "Installing with uv..."
        uv pip install -r requirements.txt
    else
        print_info "Installing with pip..."
        pip3 install -r requirements.txt
    fi
    
    print_success "Dependencies installed"
}

# =============================================================================
# PROJECT INTEGRATION
# =============================================================================

integrate_with_project() {
    local project_dir="${1:-$(pwd)}"
    local project_name=$(basename "$project_dir")
    
    print_info "Integrating ThinkChain with project: $project_name"
    
    # Create project-specific ThinkChain config
    mkdir -p "$project_dir/.claude/thinkchain"
    
    cat > "$project_dir/.claude/thinkchain/config.json" << EOF
{
  "version": "$INTEGRATION_VERSION",
  "enabled": true,
  "thinkchain_path": "$THINKCHAIN_DIR",
  "features": {
    "interleaved_thinking": true,
    "tool_streaming": true,
    "mcp_integration": true,
    "dynamic_tool_discovery": true
  },
  "settings": {
    "model": "claude-sonnet-4-20250514",
    "thinking_budget": 1024,
    "max_tokens": 1024
  },
  "tools": {
    "local_tools_enabled": true,
    "mcp_servers_enabled": true,
    "custom_tools_dir": ".claude/thinkchain/tools"
  }
}
EOF
    
    # Create custom tools directory
    mkdir -p "$project_dir/.claude/thinkchain/tools"
    
    # Create project-specific launcher
    cat > "$project_dir/.claude/thinkchain/launch.sh" << 'EOF'
#!/bin/bash
# Launch ThinkChain for this project

THINKCHAIN_DIR="/c/Users/wtyle/thinkchain"
cd "$THINKCHAIN_DIR"

echo "🚀 Launching ThinkChain..."
echo "Choose mode:"
echo "  1) CLI mode (minimal)"
echo "  2) Enhanced UI (rich formatting)"
echo "  3) Smart launcher (auto-detect)"
read -r choice

case $choice in
    1) python3 thinkchain_cli.py ;;
    2) python3 thinkchain.py ;;
    3) python3 run.py ;;
    *) python3 run.py ;;
esac
EOF
    
    chmod +x "$project_dir/.claude/thinkchain/launch.sh"
    
    print_success "ThinkChain integrated with $project_name"
}

# =============================================================================
# MAIN INSTALLATION FLOW
# =============================================================================

main() {
    print_header
    
    # Step 1: Detection
    if ! detect_thinkchain; then
        echo -e "\n${COLOR_WARNING}Would you like to install ThinkChain now? (y/n): ${NC}"
        read -r install_now
        if [ "$install_now" = "y" ]; then
            print_info "Installing ThinkChain..."
            git clone https://github.com/martinbowling/ThinkChain.git "$THINKCHAIN_DIR"
            print_success "ThinkChain installed"
        else
            print_error "ThinkChain installation required for integration"
            exit 1
        fi
    fi
    
    # Step 2: Check requirements
    if ! check_python_requirements; then
        exit 1
    fi
    
    # Step 3: Configure API
    configure_api_key
    
    # Step 4: Install dependencies
    echo -n "Install ThinkChain dependencies? (y/n): "
    read -r install_deps
    if [ "$install_deps" = "y" ]; then
        install_dependencies
    fi
    
    # Step 5: Set up integrations
    setup_mcp_integration
    create_ccdk_bridge
    create_claude_commands
    
    # Step 6: Project integration
    echo -n "Integrate with current project? (y/n): "
    read -r integrate_project
    if [ "$integrate_project" = "y" ]; then
        integrate_with_project
    fi
    
    # Success!
    echo -e "\n${COLOR_SUCCESS}${BOLD}✨ ThinkChain Integration Complete!${NC}\n"
    
    print_info "Next steps:"
    echo "  1. Set your Anthropic API key in $THINKCHAIN_DIR/.env"
    echo "  2. Test ThinkChain: cd $THINKCHAIN_DIR && python3 run.py"
    echo "  3. Use in Claude Code: /think [your prompt]"
    echo "  4. Manage tools: /tools list"
    
    echo -e "\n${COLOR_INFO}Documentation:${NC}"
    echo "  - ThinkChain: https://github.com/martinbowling/ThinkChain"
    echo "  - CCDK i124q: ~/.claude/docs/"
}

# Run main if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi