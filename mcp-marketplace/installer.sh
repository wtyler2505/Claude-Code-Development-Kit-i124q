#!/usr/bin/env bash

# MCP Server Marketplace Installer Module for CCDK i124q
# This module provides one-click and batch installation for MCP servers

set -euo pipefail

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Configuration
MARKETPLACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$MARKETPLACE_DIR/marketplace-config.json"
INSTALL_LOG="$MARKETPLACE_DIR/install.log"
MCP_CONFIG_FILE="$HOME/.claude/mcp_config.json"

# State tracking
declare -A INSTALLED_SERVERS
declare -A FAILED_SERVERS
declare -A SERVER_CONFIGS

# Load marketplace configuration
load_marketplace_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}❌ Marketplace configuration not found: $CONFIG_FILE${NC}"
        return 1
    fi
    
    # Parse JSON config using jq or python
    if command -v jq &> /dev/null; then
        MARKETPLACE_VERSION=$(jq -r '.marketplace.version' "$CONFIG_FILE")
        MARKETPLACE_UPDATED=$(jq -r '.marketplace.lastUpdated' "$CONFIG_FILE")
    elif command -v python3 &> /dev/null; then
        MARKETPLACE_VERSION=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['marketplace']['version'])")
        MARKETPLACE_UPDATED=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['marketplace']['lastUpdated'])")
    else
        echo -e "${YELLOW}⚠️  jq or python3 required for JSON parsing${NC}"
        return 1
    fi
    
    return 0
}

# Display marketplace header
show_marketplace_header() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                                              ║${NC}"
    echo -e "${CYAN}║  ${WHITE}🛍️  MCP Server Marketplace - CCDK i124q${CYAN}                                   ║${NC}"
    echo -e "${CYAN}║                                                                              ║${NC}"
    echo -e "${CYAN}║  ${GRAY}Version: $MARKETPLACE_VERSION | Updated: $MARKETPLACE_UPDATED${CYAN}                                  ║${NC}"
    echo -e "${CYAN}║                                                                              ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo
}

# Get server list by category
get_servers_by_category() {
    local category=$1
    
    if command -v jq &> /dev/null; then
        jq -r ".marketplace.servers | to_entries[] | select(.value.category == \"$category\") | .key" "$CONFIG_FILE" 2>/dev/null
    elif command -v python3 &> /dev/null; then
        python3 -c "
import json
data = json.load(open('$CONFIG_FILE'))
servers = data['marketplace']['servers']
for key, server in servers.items():
    if server.get('category') == '$category':
        print(key)
" 2>/dev/null
    fi
}

# Get all server names
get_all_servers() {
    if command -v jq &> /dev/null; then
        jq -r '.marketplace.servers | keys[]' "$CONFIG_FILE" 2>/dev/null
    elif command -v python3 &> /dev/null; then
        python3 -c "
import json
data = json.load(open('$CONFIG_FILE'))
for key in data['marketplace']['servers'].keys():
    print(key)
" 2>/dev/null
    fi
}

# Get server details
get_server_details() {
    local server_id=$1
    
    if command -v jq &> /dev/null; then
        jq -r ".marketplace.servers[\"$server_id\"]" "$CONFIG_FILE" 2>/dev/null
    elif command -v python3 &> /dev/null; then
        python3 -c "
import json
data = json.load(open('$CONFIG_FILE'))
server = data['marketplace']['servers'].get('$server_id', {})
print(json.dumps(server))
" 2>/dev/null
    fi
}

# Display server categories
show_categories_menu() {
    echo -e "${MAGENTA}📂 Server Categories:${NC}"
    echo
    echo -e "  ${CYAN}1)${NC} 🤖 AI & Language Model Assistants"
    echo -e "  ${CYAN}2)${NC} 💾 Data & Database Tools"
    echo -e "  ${CYAN}3)${NC} 🛠️  Development & Coding Tools"
    echo -e "  ${CYAN}4)${NC} 🔍 Search & Web Tools"
    echo -e "  ${CYAN}5)${NC} 🤖 Automation & Browser Control"
    echo -e "  ${CYAN}6)${NC} ☁️  Cloud Services & APIs"
    echo -e "  ${CYAN}7)${NC} 📊 Productivity & Workflow"
    echo -e "  ${CYAN}8)${NC} 📈 Monitoring & Analytics"
    echo -e "  ${CYAN}9)${NC} 🔒 Security & Authentication"
    echo -e "  ${CYAN}10)${NC} 💬 Communication & Collaboration"
    echo
    echo -e "  ${CYAN}11)${NC} 🌟 Show Recommended Servers"
    echo -e "  ${CYAN}12)${NC} 📦 Show All Servers"
    echo -e "  ${CYAN}13)${NC} 🚀 Quick Install Popular Bundle"
    echo -e "  ${CYAN}14)${NC} 📋 Batch Install from List"
    echo -e "  ${CYAN}15)${NC} 🔧 Configure Installed Servers"
    echo
    echo -e "  ${CYAN}0)${NC} ← Back to Main Menu"
    echo
}

# Display servers in a category
show_servers_in_category() {
    local category=$1
    local servers=$(get_servers_by_category "$category")
    
    if [ -z "$servers" ]; then
        echo -e "${YELLOW}No servers found in this category${NC}"
        return
    fi
    
    echo -e "${MAGENTA}Available Servers:${NC}"
    echo
    
    local count=1
    for server_id in $servers; do
        local details=$(get_server_details "$server_id")
        local name=$(echo "$details" | jq -r '.name' 2>/dev/null || echo "$server_id")
        local description=$(echo "$details" | jq -r '.description' 2>/dev/null || echo "No description")
        local stars=$(echo "$details" | jq -r '.stars' 2>/dev/null || echo "0")
        local recommended=$(echo "$details" | jq -r '.recommended' 2>/dev/null || echo "false")
        
        # Check if already installed
        local status_icon="⬜"
        if is_server_installed "$server_id"; then
            status_icon="✅"
        fi
        
        # Show recommended badge
        local rec_badge=""
        if [ "$recommended" = "true" ]; then
            rec_badge="${GREEN}[RECOMMENDED]${NC} "
        fi
        
        echo -e "  ${CYAN}$count)${NC} $status_icon $name ${rec_badge}${GRAY}(⭐ $stars)${NC}"
        echo -e "      ${GRAY}$description${NC}"
        echo
        
        ((count++))
    done
}

# Check if server is already installed
is_server_installed() {
    local server_id=$1
    
    # Check MCP config file
    if [ -f "$MCP_CONFIG_FILE" ]; then
        if command -v jq &> /dev/null; then
            local exists=$(jq ".mcpServers[\"$server_id\"] // false" "$MCP_CONFIG_FILE")
            [ "$exists" != "false" ] && return 0
        fi
    fi
    
    # Check npm global packages for npm-based servers
    local package_name=$(get_server_package "$server_id")
    if [ -n "$package_name" ] && command -v npm &> /dev/null; then
        npm list -g "$package_name" &>/dev/null && return 0
    fi
    
    return 1
}

# Get server package name
get_server_package() {
    local server_id=$1
    
    if command -v jq &> /dev/null; then
        jq -r ".marketplace.servers[\"$server_id\"].installation.package // \"\"" "$CONFIG_FILE" 2>/dev/null
    elif command -v python3 &> /dev/null; then
        python3 -c "
import json
data = json.load(open('$CONFIG_FILE'))
server = data['marketplace']['servers'].get('$server_id', {})
package = server.get('installation', {}).get('package', '')
print(package)
" 2>/dev/null
    fi
}

# Install a single MCP server
install_mcp_server() {
    local server_id=$1
    local silent=${2:-false}
    
    echo -e "${CYAN}📦 Installing $server_id...${NC}"
    
    # Get server details
    local details=$(get_server_details "$server_id")
    if [ -z "$details" ] || [ "$details" = "null" ]; then
        echo -e "${RED}❌ Server not found: $server_id${NC}"
        FAILED_SERVERS["$server_id"]="Not found in marketplace"
        return 1
    fi
    
    local name=$(echo "$details" | jq -r '.name')
    local method=$(echo "$details" | jq -r '.installation.method')
    local package=$(echo "$details" | jq -r '.installation.package')
    
    # Check if already installed
    if is_server_installed "$server_id"; then
        echo -e "${YELLOW}⚠️  $name is already installed${NC}"
        INSTALLED_SERVERS["$server_id"]="Already installed"
        return 0
    fi
    
    # Install based on method
    case "$method" in
        "npm")
            if ! command -v npm &> /dev/null; then
                echo -e "${RED}❌ npm is required but not installed${NC}"
                FAILED_SERVERS["$server_id"]="npm not available"
                return 1
            fi
            
            echo -e "${CYAN}  Installing npm package: $package${NC}"
            if npm install -g "$package" >> "$INSTALL_LOG" 2>&1; then
                echo -e "${GREEN}  ✅ Package installed successfully${NC}"
                
                # Run post-install commands if any
                local post_install=$(echo "$details" | jq -r '.installation.postInstall // ""')
                if [ -n "$post_install" ] && [ "$post_install" != "null" ]; then
                    echo -e "${CYAN}  Running post-install: $post_install${NC}"
                    eval "$post_install" >> "$INSTALL_LOG" 2>&1 || true
                fi
                
                # Configure the server in MCP config
                configure_mcp_server "$server_id" "$details"
                
                INSTALLED_SERVERS["$server_id"]="Successfully installed"
                return 0
            else
                echo -e "${RED}  ❌ Failed to install package${NC}"
                FAILED_SERVERS["$server_id"]="npm install failed"
                return 1
            fi
            ;;
            
        "git")
            echo -e "${CYAN}  Cloning from repository...${NC}"
            # Implementation for git-based installation
            ;;
            
        "binary")
            echo -e "${CYAN}  Downloading binary...${NC}"
            # Implementation for binary installation
            ;;
            
        *)
            echo -e "${RED}❌ Unknown installation method: $method${NC}"
            FAILED_SERVERS["$server_id"]="Unknown installation method"
            return 1
            ;;
    esac
}

# Configure MCP server in config file
configure_mcp_server() {
    local server_id=$1
    local details=$2
    
    echo -e "${CYAN}  Configuring MCP server...${NC}"
    
    # Ensure MCP config directory exists
    mkdir -p "$(dirname "$MCP_CONFIG_FILE")"
    
    # Initialize config file if it doesn't exist
    if [ ! -f "$MCP_CONFIG_FILE" ]; then
        echo '{"mcpServers": {}}' > "$MCP_CONFIG_FILE"
    fi
    
    # Extract configuration details
    local name=$(echo "$details" | jq -r '.name')
    local package=$(echo "$details" | jq -r '.installation.package')
    local command="npx"
    local args="[\"$package\"]"
    
    # Check for environment variables
    local env_vars=$(echo "$details" | jq -r '.installation.env // {}')
    local has_required_env=true
    
    if [ "$env_vars" != "{}" ] && [ "$env_vars" != "null" ]; then
        echo -e "${YELLOW}  ⚠️  This server requires environment variables:${NC}"
        
        # Check each required env var
        echo "$env_vars" | jq -r 'to_entries[] | select(.value.required == true) | .key' | while read -r env_key; do
            local env_desc=$(echo "$env_vars" | jq -r ".[\"$env_key\"].description")
            local env_url=$(echo "$env_vars" | jq -r ".[\"$env_key\"].url // \"\"")
            
            echo -e "${CYAN}    • $env_key: $env_desc${NC}"
            if [ -n "$env_url" ] && [ "$env_url" != "null" ]; then
                echo -e "${GRAY}      Get it from: $env_url${NC}"
            fi
            
            # Check if env var is already set
            if [ -z "${!env_key:-}" ]; then
                has_required_env=false
                echo -e "${YELLOW}      ⚠️  Not set - server may not function properly${NC}"
            else
                echo -e "${GREEN}      ✅ Already set${NC}"
            fi
        done
    fi
    
    # Add server to MCP config using jq or python
    if command -v jq &> /dev/null; then
        # Create server config object
        local server_config=$(cat <<EOF
{
  "command": "$command",
  "args": $args,
  "enabled": true
}
EOF
)
        
        # Add environment variables if present
        if [ "$env_vars" != "{}" ] && [ "$env_vars" != "null" ]; then
            # Only add env vars that are actually set
            local env_config="{}"
            echo "$env_vars" | jq -r 'to_entries[] | .key' | while read -r env_key; do
                if [ -n "${!env_key:-}" ]; then
                    env_config=$(echo "$env_config" | jq ". + {\"$env_key\": \"${!env_key}\"}")
                fi
            done
            
            if [ "$env_config" != "{}" ]; then
                server_config=$(echo "$server_config" | jq ". + {\"env\": $env_config}")
            fi
        fi
        
        # Update MCP config file
        jq ".mcpServers[\"$server_id\"] = $server_config" "$MCP_CONFIG_FILE" > "$MCP_CONFIG_FILE.tmp" && \
        mv "$MCP_CONFIG_FILE.tmp" "$MCP_CONFIG_FILE"
        
        echo -e "${GREEN}  ✅ Server configured in MCP${NC}"
    else
        echo -e "${YELLOW}  ⚠️  Manual configuration required in $MCP_CONFIG_FILE${NC}"
    fi
}

# Batch install servers
batch_install_servers() {
    local servers=("$@")
    local total=${#servers[@]}
    local success=0
    local failed=0
    
    echo -e "${MAGENTA}🚀 Batch Installing $total Servers${NC}"
    echo -e "${GRAY}════════════════════════════════════════${NC}"
    echo
    
    for server_id in "${servers[@]}"; do
        if install_mcp_server "$server_id" true; then
            ((success++))
        else
            ((failed++))
        fi
        echo
    done
    
    # Show summary
    echo -e "${GRAY}════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}📊 Installation Summary:${NC}"
    echo -e "  ${GREEN}✅ Successful: $success${NC}"
    echo -e "  ${RED}❌ Failed: $failed${NC}"
    echo
    
    # Show details of failures
    if [ $failed -gt 0 ]; then
        echo -e "${RED}Failed Servers:${NC}"
        for server_id in "${!FAILED_SERVERS[@]}"; do
            echo -e "  • $server_id: ${FAILED_SERVERS[$server_id]}"
        done
        echo
    fi
}

# Install popular bundle
install_popular_bundle() {
    echo -e "${MAGENTA}🌟 Installing Popular MCP Server Bundle${NC}"
    echo
    echo -e "${CYAN}This bundle includes:${NC}"
    echo -e "  • ${WHITE}mcp-gemini-assistant${NC} - Google Gemini AI integration"
    echo -e "  • ${WHITE}mcp-context7${NC} - Up-to-date library documentation"
    echo -e "  • ${WHITE}mcp-github${NC} - GitHub repository management"
    echo -e "  • ${WHITE}mcp-memory${NC} - Knowledge graph storage"
    echo -e "  • ${WHITE}mcp-time${NC} - Time and timezone utilities"
    echo -e "  • ${WHITE}mcp-desktop-commander${NC} - Desktop automation"
    echo -e "  • ${WHITE}mcp-taskmaster-ai${NC} - AI-powered task management"
    echo -e "  • ${WHITE}mcp-clear-thought${NC} - Advanced reasoning tools"
    echo
    
    read -p "$(echo -e ${CYAN}"Install popular bundle? (y/n): "${NC})" -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local bundle_servers=(
            "mcp-gemini-assistant"
            "mcp-context7"
            "mcp-github"
            "mcp-memory"
            "mcp-time"
            "mcp-desktop-commander"
            "mcp-taskmaster-ai"
            "mcp-clear-thought"
        )
        
        batch_install_servers "${bundle_servers[@]}"
    fi
}

# Show installed servers
show_installed_servers() {
    echo -e "${MAGENTA}📦 Installed MCP Servers:${NC}"
    echo
    
    if [ ! -f "$MCP_CONFIG_FILE" ]; then
        echo -e "${YELLOW}No MCP configuration found${NC}"
        return
    fi
    
    if command -v jq &> /dev/null; then
        local servers=$(jq -r '.mcpServers | keys[]' "$MCP_CONFIG_FILE" 2>/dev/null)
        
        if [ -z "$servers" ]; then
            echo -e "${YELLOW}No servers installed yet${NC}"
            return
        fi
        
        for server_id in $servers; do
            local enabled=$(jq -r ".mcpServers[\"$server_id\"].enabled // true" "$MCP_CONFIG_FILE")
            local status="🟢 Enabled"
            if [ "$enabled" = "false" ]; then
                status="🔴 Disabled"
            fi
            
            # Get server name from marketplace config
            local name=$(jq -r ".marketplace.servers[\"$server_id\"].name // \"$server_id\"" "$CONFIG_FILE" 2>/dev/null)
            
            echo -e "  • ${WHITE}$name${NC} $status"
        done
    else
        echo -e "${YELLOW}jq required to list installed servers${NC}"
    fi
    echo
}

# Configure installed server
configure_installed_server() {
    show_installed_servers
    
    echo -e "${CYAN}Enter server ID to configure (or 0 to cancel): ${NC}"
    read -r server_id
    
    if [ "$server_id" = "0" ]; then
        return
    fi
    
    if ! is_server_installed "$server_id"; then
        echo -e "${RED}Server not installed: $server_id${NC}"
        return
    fi
    
    echo -e "${MAGENTA}Configuration Options:${NC}"
    echo -e "  1) Enable/Disable server"
    echo -e "  2) Update environment variables"
    echo -e "  3) Remove server"
    echo
    
    read -p "$(echo -e ${CYAN}"Select option (1-3): "${NC})" -r option
    
    case $option in
        1)
            toggle_server_status "$server_id"
            ;;
        2)
            update_server_env "$server_id"
            ;;
        3)
            remove_mcp_server "$server_id"
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            ;;
    esac
}

# Toggle server enabled status
toggle_server_status() {
    local server_id=$1
    
    if command -v jq &> /dev/null; then
        local current=$(jq -r ".mcpServers[\"$server_id\"].enabled // true" "$MCP_CONFIG_FILE")
        local new_status="true"
        
        if [ "$current" = "true" ]; then
            new_status="false"
            echo -e "${YELLOW}Disabling $server_id...${NC}"
        else
            echo -e "${GREEN}Enabling $server_id...${NC}"
        fi
        
        jq ".mcpServers[\"$server_id\"].enabled = $new_status" "$MCP_CONFIG_FILE" > "$MCP_CONFIG_FILE.tmp" && \
        mv "$MCP_CONFIG_FILE.tmp" "$MCP_CONFIG_FILE"
        
        echo -e "${GREEN}✅ Server status updated${NC}"
    fi
}

# Update server environment variables
update_server_env() {
    local server_id=$1
    
    # Get server details from marketplace
    local details=$(get_server_details "$server_id")
    local env_vars=$(echo "$details" | jq -r '.installation.env // {}')
    
    if [ "$env_vars" = "{}" ] || [ "$env_vars" = "null" ]; then
        echo -e "${YELLOW}This server doesn't require environment variables${NC}"
        return
    fi
    
    echo -e "${MAGENTA}Environment Variables:${NC}"
    echo
    
    # Show each env var and allow updates
    echo "$env_vars" | jq -r 'to_entries[] | .key' | while read -r env_key; do
        local env_desc=$(echo "$env_vars" | jq -r ".[\"$env_key\"].description")
        local current_value=$(jq -r ".mcpServers[\"$server_id\"].env[\"$env_key\"] // \"\"" "$MCP_CONFIG_FILE" 2>/dev/null)
        
        echo -e "${CYAN}$env_key: $env_desc${NC}"
        if [ -n "$current_value" ] && [ "$current_value" != "null" ]; then
            echo -e "${GRAY}Current value: [SET]${NC}"
        else
            echo -e "${YELLOW}Current value: [NOT SET]${NC}"
        fi
        
        read -p "Enter new value (or press Enter to skip): " -r new_value
        
        if [ -n "$new_value" ]; then
            # Update the env var in config
            jq ".mcpServers[\"$server_id\"].env[\"$env_key\"] = \"$new_value\"" "$MCP_CONFIG_FILE" > "$MCP_CONFIG_FILE.tmp" && \
            mv "$MCP_CONFIG_FILE.tmp" "$MCP_CONFIG_FILE"
            echo -e "${GREEN}✅ Updated${NC}"
        fi
        echo
    done
}

# Remove MCP server
remove_mcp_server() {
    local server_id=$1
    
    echo -e "${YELLOW}⚠️  Remove $server_id? This will:${NC}"
    echo -e "  • Remove from MCP configuration"
    echo -e "  • Uninstall npm package (if applicable)"
    echo
    
    read -p "$(echo -e ${RED}"Confirm removal (y/n): "${NC})" -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GRAY}Cancelled${NC}"
        return
    fi
    
    # Remove from MCP config
    if command -v jq &> /dev/null; then
        jq "del(.mcpServers[\"$server_id\"])" "$MCP_CONFIG_FILE" > "$MCP_CONFIG_FILE.tmp" && \
        mv "$MCP_CONFIG_FILE.tmp" "$MCP_CONFIG_FILE"
        echo -e "${GREEN}✅ Removed from MCP configuration${NC}"
    fi
    
    # Uninstall npm package if applicable
    local package=$(get_server_package "$server_id")
    if [ -n "$package" ] && command -v npm &> /dev/null; then
        echo -e "${CYAN}Uninstalling npm package: $package${NC}"
        npm uninstall -g "$package" 2>/dev/null || true
    fi
    
    echo -e "${GREEN}✅ Server removed successfully${NC}"
}

# Search servers
search_servers() {
    echo -e "${CYAN}Enter search term: ${NC}"
    read -r search_term
    
    if [ -z "$search_term" ]; then
        return
    fi
    
    echo -e "${MAGENTA}Search Results for '$search_term':${NC}"
    echo
    
    local found=false
    local all_servers=$(get_all_servers)
    
    for server_id in $all_servers; do
        local details=$(get_server_details "$server_id")
        local name=$(echo "$details" | jq -r '.name')
        local description=$(echo "$details" | jq -r '.description')
        
        # Case-insensitive search in name and description
        if echo "$name $description" | grep -i "$search_term" &>/dev/null; then
            found=true
            local stars=$(echo "$details" | jq -r '.stars')
            
            echo -e "  • ${WHITE}$name${NC} ${GRAY}($server_id)${NC}"
            echo -e "    ${GRAY}$description${NC}"
            echo -e "    ${GRAY}⭐ $stars stars${NC}"
            echo
        fi
    done
    
    if [ "$found" = "false" ]; then
        echo -e "${YELLOW}No servers found matching '$search_term'${NC}"
    fi
}

# Main marketplace interface
marketplace_main() {
    # Load configuration
    if ! load_marketplace_config; then
        return 1
    fi
    
    while true; do
        show_marketplace_header
        show_categories_menu
        
        read -p "$(echo -e ${CYAN}"Select option: "${NC})" -r choice
        
        case $choice in
            1) show_servers_in_category "ai_assistants" ;;
            2) show_servers_in_category "data_tools" ;;
            3) show_servers_in_category "dev_tools" ;;
            4) show_servers_in_category "search_web" ;;
            5) show_servers_in_category "automation" ;;
            6) show_servers_in_category "cloud_services" ;;
            7) show_servers_in_category "productivity" ;;
            8) show_servers_in_category "monitoring" ;;
            9) show_servers_in_category "security" ;;
            10) show_servers_in_category "communication" ;;
            11) 
                # Show recommended servers
                echo -e "${MAGENTA}🌟 Recommended Servers:${NC}"
                echo
                local recommended=$(jq -r '.marketplace.servers | to_entries[] | select(.value.recommended == true) | .key' "$CONFIG_FILE")
                for server_id in $recommended; do
                    local name=$(jq -r ".marketplace.servers[\"$server_id\"].name" "$CONFIG_FILE")
                    local desc=$(jq -r ".marketplace.servers[\"$server_id\"].description" "$CONFIG_FILE")
                    echo -e "  • ${WHITE}$name${NC}"
                    echo -e "    ${GRAY}$desc${NC}"
                    echo
                done
                ;;
            12) 
                # Show all servers
                local all_servers=$(get_all_servers)
                for server_id in $all_servers; do
                    local name=$(jq -r ".marketplace.servers[\"$server_id\"].name" "$CONFIG_FILE")
                    echo -e "  • $name ${GRAY}($server_id)${NC}"
                done
                echo
                ;;
            13) install_popular_bundle ;;
            14) 
                # Batch install from list
                echo -e "${CYAN}Enter server IDs separated by spaces:${NC}"
                read -ra server_list
                if [ ${#server_list[@]} -gt 0 ]; then
                    batch_install_servers "${server_list[@]}"
                fi
                ;;
            15) configure_installed_server ;;
            0) return ;;
            *)
                echo -e "${RED}Invalid option${NC}"
                ;;
        esac
        
        echo
        read -p "$(echo -e ${GRAY}"Press Enter to continue..."${NC})" -r
    done
}

# Export functions for use in main installer
export -f marketplace_main
export -f install_mcp_server
export -f batch_install_servers
export -f show_installed_servers

# Run standalone if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    marketplace_main
fi