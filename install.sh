#!/usr/bin/env bash

# CCDK i124q - Enhanced Claude Code Development Kit Remote Installer
#
# This script downloads and installs the enhanced CCDK i124q with:
# - SuperClaude Framework integration
# - ThinkChain streaming capabilities
# - Claude Code Templates analytics
# - Task Master AI integration
# - Professional dashboards and monitoring
#
# Usage: curl -fsSL https://raw.githubusercontent.com/wtyler2505/Claude-Code-Development-Kit-i124q/main/install.sh | bash

set -euo pipefail

# Configuration
REPO_OWNER="wtyler2505"
REPO_NAME="Claude-Code-Development-Kit-i124q"
BRANCH="main"
VERSION="3.0.0"

# Parse command line arguments
FORCE_INSTALL=false
SKIP_CHECKS=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE_INSTALL=true
            shift
            ;;
        --skip-checks)
            SKIP_CHECKS=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "CCDK i124q Enhanced Installer"
            echo ""
            echo "Usage: curl -fsSL https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${BRANCH}/install.sh | bash [-s -- options]"
            echo ""
            echo "Options:"
            echo "  --force        Force installation without prompts"
            echo "  --skip-checks  Skip prerequisite checks (not recommended)"
            echo "  --verbose, -v  Enable verbose output"
            echo "  --help, -h     Show this help message"
            echo ""
            echo "Examples:"
            echo "  # Standard installation"
            echo "  curl -fsSL ... | bash"
            echo ""
            echo "  # Force install without prompts"
            echo "  curl -fsSL ... | bash -s -- --force"
            echo ""
            echo "  # Verbose installation"
            echo "  curl -fsSL ... | bash -s -- --verbose"
            exit 0
            ;;
        *)
            print_color "$RED" "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Print colored output
print_color() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Check for existing CCDK installation
check_existing_installation() {
    local claude_dir="$HOME/.claude"
    
    if [ -d "$claude_dir" ]; then
        print_color "$YELLOW" "⚠️  Existing Claude configuration detected at ~/.claude"
        
        # Check for CCDK signature files
        if [ -f "$claude_dir/CLAUDE.md" ] || [ -f "$claude_dir/.ccdk_version" ]; then
            print_color "$YELLOW" "📦 Found existing CCDK installation"
            
            # Try to read version
            local existing_version="unknown"
            if [ -f "$claude_dir/.ccdk_version" ]; then
                existing_version=$(cat "$claude_dir/.ccdk_version" 2>/dev/null || echo "unknown")
            fi
            
            print_color "$YELLOW" "   Current version: $existing_version"
            print_color "$YELLOW" "   New version: $VERSION"
            echo
            
            # If force install, proceed without prompting
            if [ "$FORCE_INSTALL" = true ]; then
                print_color "$YELLOW" "⚡ Force install enabled - proceeding with upgrade"
                return 0
            fi
            
            print_color "$CYAN" "Would you like to:"
            echo "  1) Upgrade to CCDK i124q (recommended)"
            echo "  2) Backup existing and fresh install"
            echo "  3) Cancel installation"
            echo
            
            read -p "Enter your choice (1-3): " choice
            
            case $choice in
                1)
                    print_color "$GREEN" "✅ Proceeding with upgrade..."
                    return 0
                    ;;
                2)
                    local backup_dir="$claude_dir.backup.$(date +%Y%m%d_%H%M%S)"
                    print_color "$CYAN" "📦 Creating backup at $backup_dir..."
                    mv "$claude_dir" "$backup_dir"
                    print_color "$GREEN" "✅ Backup complete"
                    return 0
                    ;;
                3)
                    print_color "$YELLOW" "❌ Installation cancelled"
                    exit 0
                    ;;
                *)
                    print_color "$RED" "❌ Invalid choice. Installation cancelled"
                    exit 1
                    ;;
            esac
        fi
    fi
    
    return 0
}

# Spinner function for progress indication
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Print banner
clear
print_color "$BLUE" "╔══════════════════════════════════════════════════════════════╗"
print_color "$BLUE" "║                                                              ║"
print_color "$BLUE" "║  🚀 CCDK i124q - Enhanced Claude Code Development Kit       ║"
print_color "$BLUE" "║                                                              ║"
print_color "$BLUE" "║  Version $VERSION - The Ultimate Claude Code Enhancement       ║"
print_color "$BLUE" "║                                                              ║"
print_color "$BLUE" "╚══════════════════════════════════════════════════════════════╝"
echo
print_color "$MAGENTA" "🎯 What you'll get:"
print_color "$CYAN" "   • 37+ Integrated capabilities across 4 frameworks"
print_color "$CYAN" "   • 11 AI personas with intelligent auto-activation"
print_color "$CYAN" "   • Real-time thinking streams and tool discovery"
print_color "$CYAN" "   • Professional analytics dashboards"
print_color "$CYAN" "   • Task Master AI integration"
print_color "$CYAN" "   • Complete development toolkit for Claude Code"
echo

# Check for existing installation
check_existing_installation

# Check for required commands
if [ "$SKIP_CHECKS" = true ]; then
    print_color "$YELLOW" "⚡ Skipping prerequisite checks (--skip-checks enabled)"
    PYTHON_CMD="python3"  # Assume python3
else
    print_color "$YELLOW" "📋 Checking system requirements..."
    MISSING_DEPS=""

    # Check basic tools
    for cmd in curl tar mktemp git; do
        if ! command -v "$cmd" &> /dev/null; then
            MISSING_DEPS="$MISSING_DEPS $cmd"
        fi
    done

    # Check Python
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        MISSING_DEPS="$MISSING_DEPS python3"
    fi

    # Check npm (for templates)
    if ! command -v npm &> /dev/null; then
        print_color "$YELLOW" "⚠️  npm not found - Some features may be limited"
    fi

    if [ -n "$MISSING_DEPS" ]; then
        print_color "$RED" "❌ Missing required commands:$MISSING_DEPS"
        print_color "$RED" "Please install these before running the installer."
        exit 1
    fi

    print_color "$GREEN" "✅ System requirements satisfied"

    # Check Python version
    PYTHON_CMD=""
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    fi

    if [ -n "$PYTHON_CMD" ]; then
        PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_color "$GREEN" "✅ Python $PYTHON_VERSION detected"
    fi
fi

echo

# Create temp directory with cleanup
TEMP_DIR=$(mktemp -d)
cleanup() {
    if [ -n "${TEMP_DIR:-}" ] && [ -d "$TEMP_DIR" ]; then
        print_color "$YELLOW" "🧹 Cleaning up temporary files..."
        rm -rf "$TEMP_DIR"
        print_color "$GREEN" "✅ Cleanup complete"
    fi
}
trap cleanup EXIT INT TERM

# Download framework
print_color "$CYAN" "📥 Downloading CCDK i124q Enhanced Framework..."
print_color "$CYAN" "   Repository: ${REPO_OWNER}/${REPO_NAME}"
print_color "$CYAN" "   Branch: ${BRANCH}"
DOWNLOAD_URL="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/tarball/${BRANCH}"

# Download with progress indication
(
    if [ "$VERBOSE" = true ]; then
        # Verbose download with progress bar
        if ! curl -fSL "$DOWNLOAD_URL" \
            -H "Accept: application/vnd.github.v3+json" \
            -o "$TEMP_DIR/framework.tar.gz" \
            --progress-bar 2>"$TEMP_DIR/download.log"; then
            echo "DOWNLOAD_FAILED" > "$TEMP_DIR/status"
        else
            echo "DOWNLOAD_SUCCESS" > "$TEMP_DIR/status"
        fi
    else
        # Silent download with spinner
        if ! curl -fsSL "$DOWNLOAD_URL" \
            -H "Accept: application/vnd.github.v3+json" \
            -o "$TEMP_DIR/framework.tar.gz" 2>"$TEMP_DIR/download.log"; then
            echo "DOWNLOAD_FAILED" > "$TEMP_DIR/status"
        else
            echo "DOWNLOAD_SUCCESS" > "$TEMP_DIR/status"
        fi
    fi
) &

DOWNLOAD_PID=$!
if [ "$VERBOSE" = false ]; then
    spinner $DOWNLOAD_PID
fi
wait $DOWNLOAD_PID

# Check download status
if [ -f "$TEMP_DIR/status" ] && [ "$(cat "$TEMP_DIR/status")" = "DOWNLOAD_FAILED" ]; then
    print_color "$RED" "❌ Failed to download framework"
    if [ -f "$TEMP_DIR/download.log" ] && [ -s "$TEMP_DIR/download.log" ]; then
        print_color "$RED" "Error details:"
        cat "$TEMP_DIR/download.log"
    fi
    echo
    print_color "$YELLOW" "Possible solutions:"
    echo "  1. Check your internet connection"
    echo "  2. Verify the repository exists: https://github.com/${REPO_OWNER}/${REPO_NAME}"
    echo "  3. Ensure Claude Code is installed: https://github.com/anthropics/claude-code"
    echo "  4. Try manual installation (git clone)"
    exit 1
fi

# Show download size
if [ -f "$TEMP_DIR/framework.tar.gz" ]; then
    SIZE=$(ls -lh "$TEMP_DIR/framework.tar.gz" | awk '{print $5}')
    print_color "$GREEN" "✅ Download complete (${SIZE}B)"
else
    print_color "$RED" "❌ Download file not found"
    exit 1
fi

# Extract files
echo
print_color "$CYAN" "📦 Extracting CCDK i124q framework files..."
print_color "$CYAN" "   This includes all integrated components:"
print_color "$CYAN" "   • CCDK foundation with 3-tier documentation"
print_color "$CYAN" "   • SuperClaude Framework commands and personas"
print_color "$CYAN" "   • ThinkChain streaming tools"
print_color "$CYAN" "   • Templates analytics system"
print_color "$CYAN" "   • Task Master AI integration"

# Extract with progress indication
(
    if ! tar -xzf "$TEMP_DIR/framework.tar.gz" -C "$TEMP_DIR" 2>"$TEMP_DIR/extract.log"; then
        echo "EXTRACT_FAILED" > "$TEMP_DIR/extract_status"
    else
        echo "EXTRACT_SUCCESS" > "$TEMP_DIR/extract_status"
    fi
) &

EXTRACT_PID=$!
if [ "$VERBOSE" = false ]; then
    spinner $EXTRACT_PID
fi
wait $EXTRACT_PID

# Check extraction status
if [ -f "$TEMP_DIR/extract_status" ] && [ "$(cat "$TEMP_DIR/extract_status")" = "EXTRACT_FAILED" ]; then
    print_color "$RED" "❌ Failed to extract framework"
    if [ -f "$TEMP_DIR/extract.log" ] && [ -s "$TEMP_DIR/extract.log" ]; then
        print_color "$RED" "Error details:"
        cat "$TEMP_DIR/extract.log"
    fi
    exit 1
fi

# Find extracted directory (GitHub creates a directory with commit hash)
EXTRACT_DIR=$(find "$TEMP_DIR" -mindepth 1 -maxdepth 1 -type d -name "${REPO_OWNER}-${REPO_NAME}-*" | head -n1)

if [ ! -d "$EXTRACT_DIR" ]; then
    print_color "$RED" "❌ Could not find extracted framework directory"
    print_color "$YELLOW" "Looking in: $TEMP_DIR"
    ls -la "$TEMP_DIR" 2>/dev/null || true
    exit 1
fi

print_color "$GREEN" "✅ Extraction complete"
echo

# Verify setup.sh exists and is executable
if [ ! -f "$EXTRACT_DIR/setup.sh" ]; then
    print_color "$RED" "❌ setup.sh not found in extracted files"
    exit 1
fi

# Make setup.sh executable
chmod +x "$EXTRACT_DIR/setup.sh"

# Save the original directory before changing
ORIGINAL_PWD="$(pwd)"

# Change to extract directory and run setup
cd "$EXTRACT_DIR"

print_color "$CYAN" "🔧 Starting CCDK i124q framework setup..."
print_color "$CYAN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# Check if Python installer exists for enhanced installation
if [ -f "install-ccdk-i124q.py" ] && [ -n "$PYTHON_CMD" ]; then
    print_color "$MAGENTA" "🎯 Enhanced installer detected - using Python installation"
    print_color "$CYAN" "   This will set up all integrated components automatically"
    echo
    
    # Build arguments for Python installer
    PYTHON_ARGS=""
    if [ "$FORCE_INSTALL" = true ]; then
        PYTHON_ARGS="$PYTHON_ARGS --force"
    fi
    if [ "$VERBOSE" = true ]; then
        PYTHON_ARGS="$PYTHON_ARGS --verbose"
    fi
    
    # Run Python installer for enhanced setup
    INSTALLER_ORIGINAL_PWD="$ORIGINAL_PWD" $PYTHON_CMD install-ccdk-i124q.py $PYTHON_ARGS
    INSTALL_RESULT=$?
else
    # Fall back to shell script setup
    print_color "$YELLOW" "⚠️  Using standard shell setup (Python installer not found)"
    
    # Check if running on Windows (Git Bash/MSYS)
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ -n "$WINDIR" ]]; then
        # Windows detected - pass flag to setup script
        INSTALLER_ORIGINAL_PWD="$ORIGINAL_PWD" WINDOWS_INSTALL=1 ./setup.sh "$@"
        INSTALL_RESULT=$?
    else
        # Non-Windows system
        INSTALLER_ORIGINAL_PWD="$ORIGINAL_PWD" ./setup.sh "$@"
        INSTALL_RESULT=$?
    fi
fi

# Check if setup succeeded
if [ $INSTALL_RESULT -ne 0 ]; then
    echo
    print_color "$RED" "❌ Setup failed"
    print_color "$YELLOW" "You can try manual installation:"
    echo "  git clone https://github.com/${REPO_OWNER}/${REPO_NAME}.git"
    echo "  cd ${REPO_NAME}"
    echo "  python3 install-ccdk-i124q.py  # For enhanced installation"
    echo "  # OR"
    echo "  ./setup.sh  # For standard installation"
    exit 1
fi

# Success! Cleanup will happen automatically via trap
echo
print_color "$GREEN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_color "$GREEN" "🎉 CCDK i124q Enhanced Installation Complete!"
print_color "$GREEN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
print_color "$MAGENTA" "✨ What's been installed:"
print_color "$CYAN" "   ✅ CCDK Foundation (3-tier docs, hooks, Task Master AI)"
print_color "$CYAN" "   ✅ SuperClaude Framework (16 commands, 11 AI personas)"
print_color "$CYAN" "   ✅ ThinkChain Engine (real-time streaming, tool discovery)"
print_color "$CYAN" "   ✅ Templates Analytics (professional dashboards)"
print_color "$CYAN" "   ✅ Unified Configuration (~/.claude/CLAUDE.md)"
echo
print_color "$MAGENTA" "🌐 Dashboard Access (once running):"
print_color "$CYAN" "   • Port 4000: 🌟 Unified Dashboard (main interface)"
print_color "$CYAN" "   • Port 5005: 📈 Enhanced Analytics Dashboard"
print_color "$CYAN" "   • Port 7000: 🌐 Enhanced WebUI with all systems"
echo
print_color "$MAGENTA" "🚀 Next Steps:"
print_color "$CYAN" "   1. Restart Claude Code to load new configuration"
print_color "$CYAN" "   2. Try CCDK commands: /full-context, /code-review, /refactor"
print_color "$CYAN" "   3. Try SuperClaude commands: /sc:implement, /sc:analyze"
print_color "$CYAN" "   4. Explore AI personas and ThinkChain tools"
print_color "$CYAN" "   5. Launch dashboards for monitoring and analytics"
echo
print_color "$GREEN" "Welcome to the ultimate Claude Code enhancement experience! 🚀"
print_color "$GREEN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"