#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');

/**
 * Robust hook wrapper that ensures graceful degradation
 * This wrapper catches ALL errors and ensures the system continues
 */
class HookWrapper {
  constructor() {
    this.settingsPath = path.join(__dirname, '..', 'settings.json');
    this.logPath = path.join(__dirname, '..', 'logs', 'hook-errors.log');
  }

  async loadSettings() {
    try {
      const content = await fs.readFile(this.settingsPath, 'utf8');
      return JSON.parse(content);
    } catch (error) {
      await this.logError('Failed to load settings.json', error);
      return { hooks: {} };
    }
  }

  async logError(message, error) {
    try {
      await fs.mkdir(path.dirname(this.logPath), { recursive: true });
      const timestamp = new Date().toISOString();
      const logEntry = `[${timestamp}] ${message}: ${error.message}\n${error.stack}\n\n`;
      await fs.appendFile(this.logPath, logEntry);
    } catch (e) {
      // Even logging failed - just continue
      console.error('Failed to log error:', e.message);
    }
  }

  async executeHook(hookPath, payload) {
    const fullPath = path.resolve(path.dirname(this.settingsPath), '..', hookPath);
    
    try {
      // Check if file exists
      await fs.access(fullPath);
    } catch (e) {
      await this.logError(`Hook file not found: ${hookPath}`, e);
      return { action: 'continue', error: 'File not found' };
    }

    const ext = path.extname(hookPath);
    
    try {
      if (ext === '.ts') {
        return await this.executeTypeScriptHook(fullPath, payload);
      } else if (ext === '.js') {
        return await this.executeJavaScriptHook(fullPath, payload);
      } else {
        return { action: 'continue', error: 'Unsupported file type' };
      }
    } catch (error) {
      await this.logError(`Hook execution failed: ${hookPath}`, error);
      return { action: 'continue', error: error.message };
    }
  }

  async executeTypeScriptHook(hookPath, payload) {
    return new Promise((resolve) => {
      const timeout = setTimeout(() => {
        runner.kill();
        resolve({ action: 'continue', error: 'Hook timeout' });
      }, 5000); // 5 second timeout

      // Try tsx first, then ts-node
      const runners = ['tsx', 'ts-node'];
      let runnerIndex = 0;

      const tryNextRunner = () => {
        if (runnerIndex >= runners.length) {
          resolve({ action: 'continue', error: 'No TypeScript runner available' });
          return;
        }

        const runnerCmd = runners[runnerIndex++];
        const runner = spawn(runnerCmd, [hookPath], {
          env: { 
            ...process.env,
            HOOK_PAYLOAD: JSON.stringify(payload)
          },
          stdio: ['ignore', 'pipe', 'pipe']
        });

        let output = '';
        let error = '';

        runner.stdout.on('data', (data) => output += data.toString());
        runner.stderr.on('data', (data) => error += data.toString());

        runner.on('exit', (code) => {
          clearTimeout(timeout);
          
          if (code === 0) {
            try {
              // Try to parse output as JSON
              const lines = output.trim().split('\n');
              const lastLine = lines[lines.length - 1];
              const result = JSON.parse(lastLine);
              resolve(result);
            } catch (e) {
              resolve({ action: 'continue' });
            }
          } else {
            resolve({ action: 'continue', error: error || 'Hook failed' });
          }
        });

        runner.on('error', (err) => {
          if (err.code === 'ENOENT' && runnerIndex < runners.length) {
            tryNextRunner();
          } else {
            clearTimeout(timeout);
            resolve({ action: 'continue', error: err.message });
          }
        });
      };

      tryNextRunner();
    });
  }

  async executeJavaScriptHook(hookPath, payload) {
    try {
      // Clear require cache
      delete require.cache[require.resolve(hookPath)];
      
      const hook = require(hookPath);
      const hookFn = hook.default || hook;
      
      if (typeof hookFn !== 'function') {
        return { action: 'continue', error: 'Hook is not a function' };
      }

      // Execute with timeout
      const timeoutPromise = new Promise((resolve) => {
        setTimeout(() => resolve({ action: 'continue', error: 'Hook timeout' }), 5000);
      });

      const hookPromise = Promise.resolve(hookFn(payload))
        .then(result => result || { action: 'continue' })
        .catch(error => ({ action: 'continue', error: error.message }));

      return await Promise.race([hookPromise, timeoutPromise]);
    } catch (error) {
      await this.logError(`JavaScript hook error: ${hookPath}`, error);
      return { action: 'continue', error: error.message };
    }
  }

  async runHooks(hookType, payload = {}) {
    const settings = await this.loadSettings();
    const hooks = settings.hooks?.[hookType] || [];
    
    console.log(`[HookWrapper] Running ${hookType} hooks: ${hooks.length} registered`);
    
    const results = [];
    
    for (const hookPath of hooks) {
      console.log(`[HookWrapper] Executing: ${hookPath}`);
      
      const result = await this.executeHook(hookPath, payload);
      results.push({ hookPath, result });
      
      if (result.error) {
        console.error(`[HookWrapper] ⚠️  Hook error but continuing: ${result.error}`);
      } else if (result.action === 'stop') {
        console.log(`[HookWrapper] ⛔ Hook requested stop: ${result.message || 'No reason'}`);
        return result;
      } else {
        console.log(`[HookWrapper] ✅ Hook completed successfully`);
      }
    }
    
    return { action: 'continue', results };
  }
}

// Export for use in other modules
module.exports = HookWrapper;

// CLI interface
if (require.main === module) {
  const hookType = process.argv[2];
  const payloadStr = process.argv[3];
  
  if (!hookType) {
    console.error('Usage: node hook-wrapper.js <hookType> [payload]');
    process.exit(1);
  }
  
  const payload = payloadStr ? JSON.parse(payloadStr) : {
    timestamp: Date.now(),
    workingDirectory: process.cwd()
  };
  
  const wrapper = new HookWrapper();
  wrapper.runHooks(hookType, payload).then(result => {
    console.log('[HookWrapper] Final result:', JSON.stringify(result, null, 2));
    process.exit(0); // Always exit successfully
  }).catch(err => {
    console.error('[HookWrapper] Fatal error:', err);
    process.exit(0); // Still exit successfully to ensure graceful degradation
  });
}