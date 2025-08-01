# CCDK Original Functionality Test Script
# Phase 1: Testing Original CCDK Commands

Write-Host "=== CCDK ORIGINAL FUNCTIONALITY TEST ===" -ForegroundColor Cyan
Write-Host "Testing all original CCDK commands to ensure nothing broke..." -ForegroundColor Yellow

# Test 1: Check if help command exists
Write-Host "`n[TEST 1] Testing /help command..." -ForegroundColor Green
if (Test-Path ".\.claude\commands\help.md") {
    Write-Host "✅ /help command found" -ForegroundColor Green
} else {
    Write-Host "❌ /help command missing!" -ForegroundColor Red
}

# Test 2: Check all original commands
Write-Host "`n[TEST 2] Checking all original Claude commands..." -ForegroundColor Green
$originalCommands = @(
    "help",
    "security-audit", 
    "run-tests",
    "git-create-pr",
    "context-frontend",
    "update-dependencies",
    "accessibility-review",
    "profile-performance",
    "hive-start",
    "swarm-run",
    "deploy-preview",
    "webui-start"
)

$commandsFound = 0
foreach ($cmd in $originalCommands) {
    if (Test-Path ".\.claude\commands\$cmd.md") {
        Write-Host "✅ /$cmd command present" -ForegroundColor Green
        $commandsFound++
    } else {
        Write-Host "❌ /$cmd command missing!" -ForegroundColor Red
    }
}

Write-Host "`nCommands found: $commandsFound/$($originalCommands.Count)" -ForegroundColor Cyan

# Test 3: Check MCP configurations
Write-Host "`n[TEST 3] Checking MCP configurations..." -ForegroundColor Green
if (Test-Path ".\.mcp.json") {
    $mcpConfig = Get-Content ".\.mcp.json" | ConvertFrom-Json
    Write-Host "✅ MCP config found with $($mcpConfig.mcpServers.PSObject.Properties.Count) servers" -ForegroundColor Green
} else {
    Write-Host "❌ MCP config missing!" -ForegroundColor Red
}

# Test 4: Check hooks configuration
Write-Host "`n[TEST 4] Checking hooks configuration..." -ForegroundColor Green
if (Test-Path ".\.claude\settings.json") {
    $settings = Get-Content ".\.claude\settings.json" | ConvertFrom-Json
    $hookCount = 0
    foreach ($hookType in $settings.hooks.PSObject.Properties) {
        $hookCount += $hookType.Value.Count
    }
    Write-Host "✅ Settings found with $hookCount hooks configured" -ForegroundColor Green
} else {
    Write-Host "❌ Settings.json missing!" -ForegroundColor Red
}

# Test 5: Check agents
Write-Host "`n[TEST 5] Checking agents..." -ForegroundColor Green
$agentCount = (Get-ChildItem ".\.claude\agents\*.md" -ErrorAction SilentlyContinue).Count
Write-Host "✅ Found $agentCount agents" -ForegroundColor Green

# Test 6: Check scripts directory
Write-Host "`n[TEST 6] Checking scripts..." -ForegroundColor Green
$scriptCount = (Get-ChildItem ".\scripts\*" -ErrorAction SilentlyContinue).Count
Write-Host "✅ Found $scriptCount scripts" -ForegroundColor Green

Write-Host "`n=== TEST COMPLETE ===" -ForegroundColor Cyan