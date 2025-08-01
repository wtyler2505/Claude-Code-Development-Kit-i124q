#!/usr/bin/env python3
"""
REAL Hook Testing - Not that surface level bullshit
Testing if hooks ACTUALLY FUCKING WORK
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

print("[HOOKS] REAL HOOK EXECUTION TEST")
print("=" * 60)

# Test 1: Do the hook files even fucking exist?
print("\n[TEST 1] Checking if hook files actually exist...")
hooks_dir = Path(".claude/hooks")
expected_hooks = [
    "session-start-persist.ts",
    "session-start-load-memory.ts", 
    "session-end-save-memory.ts",
    "post-task-summary.ts",
    "pre-search-logger.ts",
    "pre-compact-summary.ts",
    "subagent-stop-notify.ts",
    "post-tool-lint.ts",
    "postToolUse-streamInject.ts",
    "postEdit-ci.ts"
]

missing_hooks = []
for hook in expected_hooks:
    hook_path = hooks_dir / hook
    if not hook_path.exists():
        missing_hooks.append(hook)
        print(f"[FAIL] Missing hook: {hook}")
    else:
        print(f"[OK] Found: {hook}")

if missing_hooks:
    print(f"\n[CRITICAL] {len(missing_hooks)} hooks are MISSING!")
    print("This shit is broken before we even start!")
    sys.exit(1)

# Test 2: Can we actually execute these TypeScript hooks?
print("\n[TEST 2] Testing if hooks can execute...")
test_hook = hooks_dir / "session-start-persist.ts"

# Check if we have tsx in node_modules
tsx_check = subprocess.run("npx tsx --version", shell=True, capture_output=True)
if tsx_check.returncode != 0:
    print("[FAIL] tsx not found in node_modules")
    print("Hooks can't run without TypeScript support!")
    sys.exit(1)
else:
    print("[OK] TypeScript runner (tsx) is available")

# Test 3: Actually run a hook
print("\n[TEST 3] Actually executing a hook...")
try:
    # Create test context
    test_context = {
        "sessionId": "test_session_123",
        "timestamp": time.time(),
        "projectPath": os.getcwd()
    }
    
    # Try to run the hook
    cmd = f'npx tsx "{test_hook}" \'{json.dumps(test_context)}\''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("[OK] Hook executed successfully")
        if result.stdout:
            print(f"Output: {result.stdout[:100]}...")
    else:
        print("[FAIL] Hook execution failed!")
        print(f"Error: {result.stderr}")
        sys.exit(1)
        
except Exception as e:
    print(f"[FAIL] Hook test crashed: {e}")
    sys.exit(1)

# Test 4: Check if hooks are properly configured in settings.json
print("\n[TEST 4] Checking hook configuration...")
settings_path = Path(".claude/settings.json")
if not settings_path.exists():
    print("[FAIL] No settings.json - hooks won't be triggered!")
    sys.exit(1)

with open(settings_path) as f:
    settings = json.load(f)

if "hooks" not in settings:
    print("[FAIL] No hooks section in settings.json!")
    sys.exit(1)

# Check each hook type
hook_types = ["sessionStart", "sessionEnd", "postTask", "preSearch", 
              "preCompact", "subagentStop", "postToolUse", "postEdit"]

unconfigured = []
for hook_type in hook_types:
    if hook_type not in settings["hooks"] or not settings["hooks"][hook_type]:
        unconfigured.append(hook_type)
        print(f"[FAIL] {hook_type} has no hooks configured!")
    else:
        count = len(settings["hooks"][hook_type])
        print(f"[OK] {hook_type}: {count} hooks configured")

if unconfigured:
    print(f"\n[CRITICAL] {len(unconfigured)} hook types are NOT configured!")
    print("These hooks will NEVER fire!")
    sys.exit(1)

# Test 5: Test hook interaction - do they interfere with each other?
print("\n[TEST 5] Testing hook interference...")
# Run multiple hooks in sequence
for hook_type, hooks in settings["hooks"].items():
    if hook_type == "sessionStart":  # Test these specifically
        print(f"\nTesting {len(hooks)} sessionStart hooks in sequence...")
        for hook_file in hooks:
            hook_path = Path(hook_file.replace("./", ""))
            if hook_path.exists():
                cmd = f'npx tsx "{hook_path}" \'{json.dumps(test_context)}\''
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"[FAIL] {hook_path.name} failed in sequence!")
                    print(f"Error: {result.stderr}")
                    sys.exit(1)
                else:
                    print(f"[OK] {hook_path.name} executed")

print("\n" + "=" * 60)
print("[RESULT] ALL HOOK TESTS PASSED")
print("Hooks are ACTUALLY FUCKING WORKING!")