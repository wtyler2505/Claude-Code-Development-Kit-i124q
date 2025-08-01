// Direct TypeScript test for hook execution
import { SessionStartPayload } from '../.claude/hooks/lib';

// Test the session-start-persist hook directly
async function testHook() {
    console.log("[HOOK TEST] Testing session-start-persist hook directly");
    
    const testPayload: SessionStartPayload = {
        session_id: "test_" + Date.now(),
        timestamp: Date.now(),
        project_path: process.cwd()
    };
    
    try {
        // Import and run the hook
        const hook = await import('../.claude/hooks/session-start-persist');
        const result = await hook.default(testPayload);
        
        console.log("[OK] Hook executed successfully");
        console.log("Result:", result);
        
        // Check if database was created
        const fs = await import('fs');
        if (fs.existsSync('.ccd_memory.db')) {
            console.log("[OK] Memory database created");
        } else {
            console.log("[FAIL] Memory database NOT created");
            process.exit(1);
        }
        
    } catch (error) {
        console.error("[FAIL] Hook execution failed:", error);
        process.exit(1);
    }
}

testHook();