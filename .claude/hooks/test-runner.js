#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');

// Hook test runner with proper error handling
async function runHook(hookType, payload = {}) {
  try {
    // Read settings
    const settingsPath = path.join(__dirname, '..', 'settings.json');
    const settings = JSON.parse(await fs.readFile(settingsPath, 'utf8'));
    
    // Get hooks for this type
    const hooks = settings.hooks?.[hookType] || [];
    
    console.log(`Running ${hookType} hooks: ${hooks.length} registered`);
    
    for (const hookPath of hooks) {
      console.log(`  Executing: ${hookPath}`);
      
      try {
        // Check if hook file exists
        const fullPath = path.join(__dirname, '..', '..', hookPath);
        try {
          await fs.access(fullPath);
        } catch (e) {
          console.error(`  ❌ Hook file not found: ${hookPath}`);
          continue; // Skip missing hooks
        }
        
        // Determine if it's TypeScript or JavaScript
        const ext = path.extname(hookPath);
        let result;
        
        if (ext === '.ts') {
          // Run TypeScript hook
          result = await runTypeScriptHook(fullPath, payload);
        } else {
          // Run JavaScript hook
          result = await runJavaScriptHook(fullPath, payload);
        }
        
        console.log(`  ✅ Result:`, result);
        
        // Handle hook response
        if (result && result.action === 'stop') {
          console.log(`  ⛔ Hook requested stop: ${result.message || 'No reason given'}`);
          return result;
        }
      } catch (error) {
        console.error(`  ❌ Hook error: ${error.message}`);
        // Continue with next hook despite error
      }
    }
    
    return { action: 'continue' };
  } catch (error) {
    console.error(`Fatal error in hook runner: ${error.message}`);
    return { action: 'continue', error: error.message };
  }
}

async function runTypeScriptHook(hookPath, payload) {
  return new Promise((resolve) => {
    // Create a temporary runner script
    const runnerScript = `
      const hook = require('${hookPath.replace(/\\/g, '/')}').default;
      const payload = ${JSON.stringify(payload)};
      
      hook(payload).then(result => {
        console.log(JSON.stringify(result));
      }).catch(err => {
        console.error(JSON.stringify({ error: err.message }));
      });
    `;
    
    const runner = spawn('node', ['-e', runnerScript], {
      cwd: path.dirname(hookPath),
      stdio: ['ignore', 'pipe', 'pipe']
    });
    
    let output = '';
    let error = '';
    
    runner.stdout.on('data', (data) => output += data.toString());
    runner.stderr.on('data', (data) => error += data.toString());
    
    runner.on('exit', (code) => {
      if (code !== 0) {
        resolve({ action: 'continue', error: error || 'Hook failed' });
      } else {
        try {
          const result = output ? JSON.parse(output) : { action: 'continue' };
          resolve(result);
        } catch (e) {
          resolve({ action: 'continue', error: 'Invalid hook response' });
        }
      }
    });
    
    runner.on('error', (err) => {
      resolve({ action: 'continue', error: err.message });
    });
  });
}

async function runJavaScriptHook(hookPath, payload) {
  try {
    delete require.cache[require.resolve(hookPath)];
    const hook = require(hookPath);
    const hookFn = hook.default || hook;
    
    const result = await hookFn(payload);
    return result || { action: 'continue' };
  } catch (error) {
    return { action: 'continue', error: error.message };
  }
}

// CLI interface
if (require.main === module) {
  const hookType = process.argv[2];
  const payloadStr = process.argv[3];
  
  if (!hookType) {
    console.error('Usage: node test-runner.js <hookType> [payload]');
    process.exit(1);
  }
  
  const payload = payloadStr ? JSON.parse(payloadStr) : {
    timestamp: Date.now(),
    workingDirectory: process.cwd()
  };
  
  runHook(hookType, payload).then(result => {
    console.log('Final result:', result);
    process.exit(result.action === 'stop' ? 1 : 0);
  }).catch(err => {
    console.error('Runner failed:', err);
    process.exit(1);
  });
}

module.exports = { runHook };