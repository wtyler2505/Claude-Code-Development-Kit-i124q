// Comprehensive test of ALL hooks - no bullshit
import * as fs from 'fs';
import * as path from 'path';
import { 
    SessionStartPayload, 
    SessionEndPayload, 
    TaskPayload,
    SearchPayload,
    ToolUsePayload,
    EditPayload,
    CompactPayload,
    SubagentPayload 
} from '../.claude/hooks/lib';

interface TestResult {
    hook: string;
    status: 'PASS' | 'FAIL';
    error?: string;
}

const results: TestResult[] = [];

async function testHook(hookPath: string, payload: any): Promise<TestResult> {
    const hookName = path.basename(hookPath);
    console.log(`\n[TESTING] ${hookName}`);
    
    try {
        const hook = await import(hookPath);
        const result = await hook.default(payload);
        
        if (result && result.action) {
            console.log(`  [OK] Hook executed - Action: ${result.action}`);
            return { hook: hookName, status: 'PASS' };
        } else {
            console.log(`  [FAIL] Invalid response:`, result);
            return { hook: hookName, status: 'FAIL', error: 'Invalid response format' };
        }
    } catch (error: any) {
        console.log(`  [FAIL] Error: ${error.message}`);
        return { hook: hookName, status: 'FAIL', error: error.message };
    }
}

async function runAllTests() {
    console.log("COMPREHENSIVE HOOK TESTING - EVERY SINGLE FUCKING HOOK");
    console.log("=" * 60);
    
    const sessionId = `test_${Date.now()}`;
    const timestamp = Date.now();
    
    // Test 1: Session Start hooks
    console.log("\n=== SESSION START HOOKS ===");
    const sessionStartPayload: SessionStartPayload = {
        session_id: sessionId,
        timestamp: timestamp,
        project_path: process.cwd()
    };
    
    results.push(await testHook('../.claude/hooks/session-start-persist', sessionStartPayload));
    results.push(await testHook('../.claude/hooks/session-start-load-memory', sessionStartPayload));
    
    // Test 2: Task hooks
    console.log("\n=== TASK HOOKS ===");
    const taskPayload: TaskPayload = {
        session_id: sessionId,
        task: "Test task execution",
        result: { success: true },
        timestamp: timestamp
    };
    
    results.push(await testHook('../.claude/hooks/post-task-summary', taskPayload));
    
    // Test 3: Search hooks
    console.log("\n=== SEARCH HOOKS ===");
    const searchPayload: SearchPayload = {
        session_id: sessionId,
        query: "test search",
        files: ["file1.ts", "file2.ts"],
        timestamp: timestamp
    };
    
    results.push(await testHook('../.claude/hooks/pre-search-logger', searchPayload));
    
    // Test 4: Tool Use hooks
    console.log("\n=== TOOL USE HOOKS ===");
    const toolPayload: ToolUsePayload = {
        session_id: sessionId,
        tool: "Edit",
        params: { file: "test.ts", content: "test" },
        result: { success: true },
        timestamp: timestamp
    };
    
    results.push(await testHook('../.claude/hooks/post-tool-lint', toolPayload));
    results.push(await testHook('../.claude/hooks/postToolUse-streamInject', toolPayload));
    
    // Test 5: Edit hooks
    console.log("\n=== EDIT HOOKS ===");
    const editPayload: EditPayload = {
        session_id: sessionId,
        file: "test.ts",
        changes: { lines: 10 },
        timestamp: timestamp
    };
    
    results.push(await testHook('../.claude/hooks/postEdit-ci', editPayload));
    
    // Test 6: Compact hooks
    console.log("\n=== COMPACT HOOKS ===");
    const compactPayload: CompactPayload = {
        session_id: sessionId,
        summary: "Test session summary",
        timestamp: timestamp
    };
    
    results.push(await testHook('../.claude/hooks/pre-compact-summary', compactPayload));
    
    // Test 7: Subagent hooks
    console.log("\n=== SUBAGENT HOOKS ===");
    const subagentPayload: SubagentPayload = {
        session_id: sessionId,
        agent_id: "test-agent",
        reason: "Test stop",
        timestamp: timestamp
    };
    
    results.push(await testHook('../.claude/hooks/subagent-stop-notify', subagentPayload));
    
    // Test 8: Session End hooks
    console.log("\n=== SESSION END HOOKS ===");
    const sessionEndPayload: SessionEndPayload = {
        session_id: sessionId,
        timestamp: timestamp,
        duration: 60000
    };
    
    results.push(await testHook('../.claude/hooks/session-end-save-memory', sessionEndPayload));
    
    // FINAL REPORT
    console.log("\n" + "=" * 60);
    console.log("FINAL HOOK TEST REPORT");
    console.log("=" * 60);
    
    const passed = results.filter(r => r.status === 'PASS').length;
    const failed = results.filter(r => r.status === 'FAIL').length;
    
    console.log(`\nPASSED: ${passed}`);
    console.log(`FAILED: ${failed}`);
    console.log(`TOTAL: ${results.length}`);
    console.log(`SUCCESS RATE: ${((passed / results.length) * 100).toFixed(1)}%`);
    
    if (failed > 0) {
        console.log("\nFAILED HOOKS:");
        results.filter(r => r.status === 'FAIL').forEach(r => {
            console.log(`  - ${r.hook}: ${r.error}`);
        });
    }
    
    // Check for artifacts
    console.log("\n=== CHECKING ARTIFACTS ===");
    if (fs.existsSync('.ccd_memory.db')) {
        console.log("[OK] Memory database exists");
    }
    if (fs.existsSync('.ccd_analytics.log')) {
        console.log("[OK] Analytics log exists");
    }
    
    // Return exit code
    process.exit(failed > 0 ? 1 : 0);
}

// Run the tests
runAllTests().catch(error => {
    console.error("CATASTROPHIC TEST FAILURE:", error);
    process.exit(1);
});