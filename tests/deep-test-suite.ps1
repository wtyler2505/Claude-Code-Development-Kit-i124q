# CCDK Deep Obsessive Test Suite
# Testing EVERYTHING with extreme prejudice

Write-Host "`n🔥 CCDK DEEP OBSESSIVE TESTING BEGINS 🔥" -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor Cyan

# Initialize test results
$testResults = @{
    Passed = 0
    Failed = 0
    Warnings = 0
    Details = @()
}

function Test-Feature {
    param($Name, $TestBlock, $Critical = $false)
    
    Write-Host "`n[TESTING] $Name..." -ForegroundColor Yellow
    try {
        $result = & $TestBlock
        if ($result) {
            Write-Host "✅ PASSED: $Name" -ForegroundColor Green
            $script:testResults.Passed++
        } else {
            Write-Host "❌ FAILED: $Name" -ForegroundColor Red
            $script:testResults.Failed++
            if ($Critical) {
                Write-Host "⚠️  CRITICAL FAILURE - This is a core feature!" -ForegroundColor Red
            }
        }
    } catch {
        Write-Host "💥 ERROR in $Name : $_" -ForegroundColor Red
        $script:testResults.Failed++
    }
}

# Phase 1: Core File Structure
Write-Host "`n📁 PHASE 1: CORE FILE STRUCTURE" -ForegroundColor Cyan
Write-Host "-" * 40

Test-Feature "Claude settings.json exists" {
    Test-Path ".\.claude\settings.json"
} -Critical $true

Test-Feature "Commands directory populated" {
    (Get-ChildItem ".\.claude\commands\*.md" -ErrorAction SilentlyContinue).Count -gt 10
} -Critical $true

Test-Feature "Agents directory populated" {
    (Get-ChildItem ".\.claude\agents\*.md" -ErrorAction SilentlyContinue).Count -gt 8
} -Critical $true

Test-Feature "Hooks directory populated" {
    (Get-ChildItem ".\.claude\hooks\*.ts" -ErrorAction SilentlyContinue).Count -gt 5
} -Critical $true

Test-Feature "Scripts directory exists" {
    Test-Path ".\scripts" -and (Get-ChildItem ".\scripts\*" -ErrorAction SilentlyContinue).Count -gt 0
}

# Phase 2: Hook Configuration
Write-Host "`n🔗 PHASE 2: HOOK CONFIGURATION" -ForegroundColor Cyan
Write-Host "-" * 40

Test-Feature "Hooks properly configured in settings.json" {
    $settings = Get-Content ".\.claude\settings.json" | ConvertFrom-Json
    $hookTypes = @("sessionStart", "sessionEnd", "postTask", "preSearch", "postToolUse", "postEdit")
    $allHooksPresent = $true
    foreach ($hookType in $hookTypes) {
        if (-not $settings.hooks.$hookType) {
            Write-Host "  Missing hook type: $hookType" -ForegroundColor Yellow
            $allHooksPresent = $false
        }
    }
    $allHooksPresent
} -Critical $true

# Phase 3: Enhancement Kit Integration
Write-Host "`n🚀 PHASE 3: ENHANCEMENT KIT INTEGRATION" -ForegroundColor Cyan
Write-Host "-" * 40

Test-Feature "Kit 1 - Core Extensions" {
    $commands = @("security-audit", "run-tests", "git-create-pr", "context-frontend")
    $allPresent = $true
    foreach ($cmd in $commands) {
        if (-not (Test-Path ".\.claude\commands\$cmd.md")) {
            Write-Host "  Missing Kit 1 command: $cmd" -ForegroundColor Yellow
            $allPresent = $false
        }
    }
    $allPresent
}

Test-Feature "Kit 2 - Dependency & Performance" {
    $commands = @("update-dependencies", "accessibility-review", "profile-performance")
    $allPresent = $true
    foreach ($cmd in $commands) {
        if (-not (Test-Path ".\.claude\commands\$cmd.md")) {
            Write-Host "  Missing Kit 2 command: $cmd" -ForegroundColor Yellow
            $allPresent = $false
        }
    }
    $allPresent
}

Test-Feature "Kit 3 - Hive Mind & Memory" {
    Test-Path ".\.claude\commands\hive-start.md" -and 
    Test-Path ".\scripts\ccdk-hive.py"
}

Test-Feature "Kit 4 - Analytics & Swarm" {
    Test-Path ".\.claude\commands\swarm-run.md" -and
    Test-Path ".\dashboard\app.py"
}

Test-Feature "Kit 5 - CI/CD Integration" {
    Test-Path ".\.claude\commands\deploy-preview.md" -and
    Test-Path ".\.github\workflows\ci.yml"
}

Test-Feature "Kit 6 - WebUI" {
    Test-Path ".\.claude\commands\webui-start.md" -and
    Test-Path ".\webui\app.py"
}

# Phase 4: Python Scripts
Write-Host "`n🐍 PHASE 4: PYTHON SCRIPT VALIDATION" -ForegroundColor Cyan
Write-Host "-" * 40

Test-Feature "Python scripts are syntactically valid" {
    $pythonFiles = Get-ChildItem -Path . -Filter "*.py" -Recurse -ErrorAction SilentlyContinue
    $allValid = $true
    foreach ($file in $pythonFiles) {
        $result = python -m py_compile $file.FullName 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  Syntax error in: $($file.Name)" -ForegroundColor Red
            $allValid = $false
        }
    }
    $allValid
}

# Phase 5: Node.js Dependencies
Write-Host "`n📦 PHASE 5: NODE.JS DEPENDENCIES" -ForegroundColor Cyan
Write-Host "-" * 40

Test-Feature "Package.json exists" {
    Test-Path ".\package.json"
}

Test-Feature "Node modules installed" {
    Test-Path ".\node_modules"
}

Test-Feature "No security vulnerabilities" {
    $audit = npm audit 2>&1
    $audit -notmatch "found [1-9]\d* vulnerabilities"
}

# Phase 6: Git Integration
Write-Host "`n🔀 PHASE 6: GIT INTEGRATION" -ForegroundColor Cyan
Write-Host "-" * 40

Test-Feature "Git repository initialized" {
    Test-Path ".\.git"
}

Test-Feature "On correct branch" {
    $branch = git branch --show-current
    Write-Host "  Current branch: $branch" -ForegroundColor Gray
    $branch -eq "integrate-kits"
}

# Phase 7: Documentation
Write-Host "`n📚 PHASE 7: DOCUMENTATION" -ForegroundColor Cyan
Write-Host "-" * 40

Test-Feature "Test plans exist" {
    Test-Path ".\.claude\docs\MASTER_TEST_PLAN.md" -and
    Test-Path ".\.claude\docs\COMPLETE_INTEGRATION_TEST_PLAN.md"
}

Test-Feature "Integration test log exists" {
    Test-Path ".\.claude\docs\integration-test-log.md"
}

Test-Feature "Session summary exists" {
    Test-Path ".\.claude\docs\session-summary.md"
}

# Phase 8: Task Master Integration
Write-Host "`n✅ PHASE 8: TASK MASTER" -ForegroundColor Cyan
Write-Host "-" * 40

Test-Feature "Task Master initialized" {
    Test-Path ".\.taskmaster"
}

Test-Feature "Tasks file exists" {
    Test-Path ".\.taskmaster\tasks\tasks.json"
}

# FINAL REPORT
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "🏁 FINAL TEST REPORT" -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ Passed: $($testResults.Passed)" -ForegroundColor Green
Write-Host "❌ Failed: $($testResults.Failed)" -ForegroundColor Red
Write-Host "⚠️  Warnings: $($testResults.Warnings)" -ForegroundColor Yellow

$successRate = [math]::Round(($testResults.Passed / ($testResults.Passed + $testResults.Failed)) * 100, 2)
Write-Host "`n📊 Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })

if ($testResults.Failed -gt 0) {
    Write-Host "`n⚠️  ATTENTION: There are failures that need to be addressed!" -ForegroundColor Red
} else {
    Write-Host "`n🎉 ALL TESTS PASSED! The integration is solid! 🎉" -ForegroundColor Green
}

Write-Host "`n🔥 DEEP OBSESSIVE TESTING COMPLETE 🔥" -ForegroundColor Magenta