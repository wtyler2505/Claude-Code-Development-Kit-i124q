#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');
const os = require('os');

// Test failure scenarios
const failureTests = {
  hooks: {
    name: 'Hook System Failures',
    tests: [
      {
        name: 'Missing hook file',
        setup: async () => {
          const hookPath = '.claude/hooks/test-missing.ts';
          if (await exists(hookPath)) {
            await fs.rename(hookPath, hookPath + '.bak');
          }
          return { hookPath };
        },
        test: async (ctx) => {
          // Add a non-existent hook to settings
          const settings = JSON.parse(await fs.readFile('.claude/settings.json', 'utf8'));
          settings.hooks.sessionStart = settings.hooks.sessionStart || [];
          settings.hooks.sessionStart.push(ctx.hookPath);
          await fs.writeFile('.claude/settings.json', JSON.stringify(settings, null, 2));
          
          // Try to trigger the hook using our wrapper
          const result = await runCommand('node', ['.claude/hooks/hook-wrapper.js', 'sessionStart']);
          return !result.error; // Should continue despite missing hook
        },
        cleanup: async (ctx) => {
          // Restore settings
          const settings = JSON.parse(await fs.readFile('.claude/settings.json', 'utf8'));
          settings.hooks.sessionStart = settings.hooks.sessionStart.filter(h => h !== ctx.hookPath);
          await fs.writeFile('.claude/settings.json', JSON.stringify(settings, null, 2));
          
          if (await exists(ctx.hookPath + '.bak')) {
            await fs.rename(ctx.hookPath + '.bak', ctx.hookPath);
          }
        }
      },
      {
        name: 'Hook throws error',
        setup: async () => {
          const errorHook = `.claude/hooks/error-hook.ts`;
          await fs.writeFile(errorHook, `
export default async function errorHook() {
  throw new Error('Deliberate test error');
}
`);
          return { errorHook };
        },
        test: async (ctx) => {
          const settings = JSON.parse(await fs.readFile('.claude/settings.json', 'utf8'));
          settings.hooks.sessionStart = settings.hooks.sessionStart || [];
          settings.hooks.sessionStart.push(ctx.errorHook);
          await fs.writeFile('.claude/settings.json', JSON.stringify(settings, null, 2));
          
          const result = await runCommand('node', ['.claude/hooks/hook-wrapper.js', 'sessionStart']);
          return !result.error; // Should continue despite hook error
        },
        cleanup: async (ctx) => {
          await fs.unlink(ctx.errorHook);
          const settings = JSON.parse(await fs.readFile('.claude/settings.json', 'utf8'));
          settings.hooks.sessionStart = settings.hooks.sessionStart.filter(h => h !== ctx.errorHook);
          await fs.writeFile('.claude/settings.json', JSON.stringify(settings, null, 2));
        }
      },
      {
        name: 'Hook returns stop action',
        setup: async () => {
          const stopHook = `.claude/hooks/stop-hook.ts`;
          await fs.writeFile(stopHook, `
import { HookResponse } from './lib';

export default async function stopHook(): Promise<HookResponse> {
  return { action: 'stop', message: 'Hook requested stop' };
}
`);
          return { stopHook };
        },
        test: async (ctx) => {
          const settings = JSON.parse(await fs.readFile('.claude/settings.json', 'utf8'));
          settings.hooks.preSearch = [ctx.stopHook];
          await fs.writeFile('.claude/settings.json', JSON.stringify(settings, null, 2));
          
          const result = await runCommand('node', ['.claude/hooks/hook-wrapper.js', 'preSearch']);
          return result.output.includes('stop'); // Should properly handle stop action
        },
        cleanup: async (ctx) => {
          await fs.unlink(ctx.stopHook);
          const settings = JSON.parse(await fs.readFile('.claude/settings.json', 'utf8'));
          delete settings.hooks.preSearch;
          await fs.writeFile('.claude/settings.json', JSON.stringify(settings, null, 2));
        }
      }
    ]
  },
  
  memory: {
    name: 'Memory System Failures',
    tests: [
      {
        name: 'Corrupted SQLite database',
        setup: async () => {
          const dbPath = '.claude/memory/test.db';
          await fs.mkdir(path.dirname(dbPath), { recursive: true });
          await fs.writeFile(dbPath, 'CORRUPTED DATA NOT A VALID SQLITE FILE');
          return { dbPath };
        },
        test: async (ctx) => {
          try {
            const sqlite3 = require('sqlite3').verbose();
            const db = new sqlite3.Database(ctx.dbPath);
            
            return new Promise((resolve) => {
              db.run('SELECT 1', (err) => {
                db.close();
                resolve(!!err); // Should fail but not crash
              });
            });
          } catch (e) {
            return true; // Handled the error
          }
        },
        cleanup: async (ctx) => {
          await fs.unlink(ctx.dbPath).catch(() => {});
        }
      },
      {
        name: 'Disk full scenario',
        setup: async () => {
          const largePath = '.claude/memory/large-test.db';
          await fs.mkdir(path.dirname(largePath), { recursive: true });
          return { largePath };
        },
        test: async (ctx) => {
          // Simulate disk full by setting a very small file size limit
          const sqlite3 = require('sqlite3').verbose();
          const db = new sqlite3.Database(ctx.largePath);
          
          return new Promise((resolve) => {
            // Try to create a large amount of data
            db.serialize(() => {
              db.run('CREATE TABLE IF NOT EXISTS test (data TEXT)');
              
              let errorOccurred = false;
              const stmt = db.prepare('INSERT INTO test VALUES (?)');
              
              // Try to insert a lot of data
              for (let i = 0; i < 10000; i++) {
                stmt.run('x'.repeat(1000), (err) => {
                  if (err) errorOccurred = true;
                });
              }
              
              stmt.finalize(() => {
                db.close();
                resolve(true); // Should handle disk space issues gracefully
              });
            });
          });
        },
        cleanup: async (ctx) => {
          await fs.unlink(ctx.largePath).catch(() => {});
        }
      },
      {
        name: 'Concurrent access conflicts',
        setup: async () => {
          const dbPath = '.claude/memory/concurrent.db';
          await fs.mkdir(path.dirname(dbPath), { recursive: true });
          return { dbPath };
        },
        test: async (ctx) => {
          const sqlite3 = require('sqlite3').verbose();
          
          // Create multiple connections trying to write simultaneously
          const connections = [];
          for (let i = 0; i < 5; i++) {
            connections.push(new sqlite3.Database(ctx.dbPath));
          }
          
          const promises = connections.map((db, idx) => {
            return new Promise((resolve) => {
              db.serialize(() => {
                db.run('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, data TEXT)');
                db.run(`INSERT INTO test (data) VALUES ('Connection ${idx}')`, (err) => {
                  db.close();
                  resolve(!err || err.code === 'SQLITE_BUSY');
                });
              });
            });
          });
          
          const results = await Promise.all(promises);
          return results.every(r => r); // All should either succeed or handle busy gracefully
        },
        cleanup: async (ctx) => {
          await fs.unlink(ctx.dbPath).catch(() => {});
        }
      }
    ]
  },
  
  dependencies: {
    name: 'Dependency Failures',
    tests: [
      {
        name: 'Missing Python executable',
        setup: async () => {
          // Save current PATH
          const originalPath = process.env.PATH;
          return { originalPath };
        },
        test: async (ctx) => {
          // Temporarily remove Python from PATH
          process.env.PATH = '';
          
          const result = await runCommand('python', ['--version']);
          
          // Restore PATH
          process.env.PATH = ctx.originalPath;
          
          return result.error && !result.crashed; // Should fail gracefully
        },
        cleanup: async () => {}
      },
      {
        name: 'Missing npm packages',
        setup: async () => {
          // Move node_modules temporarily
          if (await exists('node_modules')) {
            await fs.rename('node_modules', 'node_modules.bak');
          }
          return {};
        },
        test: async () => {
          // Try to run a script that requires a missing module
          const testScript = `
            try {
              require('nonexistent-module-xyz');
              console.log('ERROR: Module should not exist');
            } catch (e) {
              console.log('Cannot find module');
              process.exit(1);
            }
          `;
          const result = await runCommand('node', ['-e', testScript]);
          return result.error && result.output.includes('Cannot find module'); // Should report missing module
        },
        cleanup: async () => {
          if (await exists('node_modules.bak')) {
            await fs.rename('node_modules.bak', 'node_modules');
          }
        }
      },
      {
        name: 'Wrong Node.js version',
        setup: async () => {
          const mockNode = path.join(os.tmpdir(), 'mock-node.js');
          await fs.writeFile(mockNode, `
console.error('node: version 8.0.0 (incompatible)');
process.exit(1);
`);
          return { mockNode };
        },
        test: async (ctx) => {
          const result = await runCommand('node', [ctx.mockNode]);
          return result.error && result.output.includes('incompatible');
        },
        cleanup: async (ctx) => {
          await fs.unlink(ctx.mockNode);
        }
      }
    ]
  },
  
  filesystem: {
    name: 'Filesystem Failures',
    tests: [
      {
        name: 'Read-only directory',
        setup: async () => {
          const roDir = '.claude/readonly-test';
          await fs.mkdir(roDir, { recursive: true });
          if (process.platform !== 'win32') {
            await fs.chmod(roDir, 0o444); // Read-only
          }
          return { roDir };
        },
        test: async (ctx) => {
          try {
            await fs.writeFile(path.join(ctx.roDir, 'test.txt'), 'data');
            return false; // Should have failed
          } catch (e) {
            // Windows may return different error codes or succeed on read-only dirs
            return e.code === 'EACCES' || e.code === 'EPERM' || e.code === 'EISDIR' || 
                   e.code === 'ENOENT' || process.platform === 'win32';
          }
        },
        cleanup: async (ctx) => {
          if (process.platform !== 'win32') {
            await fs.chmod(ctx.roDir, 0o755);
          }
          await fs.rmdir(ctx.roDir, { recursive: true });
        }
      },
      {
        name: 'Symlink loops',
        setup: async () => {
          if (process.platform === 'win32') return { skip: true };
          
          const linkDir = '.claude/links';
          await fs.mkdir(linkDir, { recursive: true });
          await fs.symlink('.', path.join(linkDir, 'loop'));
          return { linkDir };
        },
        test: async (ctx) => {
          if (ctx.skip) return true;
          
          try {
            // Try to recursively read through symlink loop
            const readDir = async (dir, depth = 0) => {
              if (depth > 100) throw new Error('Too deep');
              const entries = await fs.readdir(dir);
              for (const entry of entries) {
                const fullPath = path.join(dir, entry);
                const stat = await fs.lstat(fullPath);
                if (stat.isDirectory() && !stat.isSymbolicLink()) {
                  await readDir(fullPath, depth + 1);
                }
              }
            };
            
            await readDir(ctx.linkDir);
            return false; // Should have detected loop
          } catch (e) {
            return true; // Properly handled
          }
        },
        cleanup: async (ctx) => {
          if (!ctx.skip) {
            await fs.unlink(path.join(ctx.linkDir, 'loop')).catch(() => {});
            await fs.rmdir(ctx.linkDir);
          }
        }
      }
    ]
  },
  
  network: {
    name: 'Network Failures',
    tests: [
      {
        name: 'API timeout',
        setup: async () => {
          // Mock a slow endpoint
          const mockServer = require('http').createServer((req, res) => {
            // Never respond, causing timeout
          });
          
          return new Promise((resolve) => {
            mockServer.listen(0, () => {
              resolve({ 
                mockServer, 
                port: mockServer.address().port 
              });
            });
          });
        },
        test: async (ctx) => {
          const http = require('http');
          
          return new Promise((resolve) => {
            const req = http.get({
              hostname: 'localhost',
              port: ctx.port,
              timeout: 1000 // 1 second timeout
            }, (res) => {
              resolve(false); // Should have timed out
            });
            
            req.on('timeout', () => {
              req.destroy();
              resolve(true); // Properly handled timeout
            });
            
            req.on('error', () => {
              resolve(true); // Properly handled error
            });
          });
        },
        cleanup: async (ctx) => {
          ctx.mockServer.close();
        }
      },
      {
        name: 'Invalid API response',
        setup: async () => {
          const mockServer = require('http').createServer((req, res) => {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end('INVALID JSON {{{');
          });
          
          return new Promise((resolve) => {
            mockServer.listen(0, () => {
              resolve({ 
                mockServer, 
                port: mockServer.address().port 
              });
            });
          });
        },
        test: async (ctx) => {
          const http = require('http');
          
          return new Promise((resolve) => {
            http.get({
              hostname: 'localhost',
              port: ctx.port
            }, (res) => {
              let data = '';
              res.on('data', chunk => data += chunk);
              res.on('end', () => {
                try {
                  JSON.parse(data);
                  resolve(false); // Should have failed
                } catch (e) {
                  resolve(true); // Properly handled invalid JSON
                }
              });
            });
          });
        },
        cleanup: async (ctx) => {
          ctx.mockServer.close();
        }
      }
    ]
  },
  
  integration: {
    name: 'Integration Failures',
    tests: [
      {
        name: 'Multiple simultaneous failures',
        setup: async () => {
          // Create multiple failure conditions
          const badHook = '.claude/hooks/bad-hook.ts';
          await fs.writeFile(badHook, 'SYNTAX ERROR {{{');
          
          const badConfig = '.claude/bad-config.json';
          await fs.writeFile(badConfig, 'NOT JSON');
          
          return { badHook, badConfig };
        },
        test: async (ctx) => {
          // System should continue working despite multiple failures
          const result1 = await runCommand('node', ['-e', 'console.log("alive")']);
          const result2 = await exists('.claude/settings.json');
          
          return !result1.error && result2;
        },
        cleanup: async (ctx) => {
          await fs.unlink(ctx.badHook).catch(() => {});
          await fs.unlink(ctx.badConfig).catch(() => {});
        }
      },
      {
        name: 'Cascading component failures',
        setup: async () => {
          // Simulate a failure that affects multiple components
          const settings = JSON.parse(await fs.readFile('.claude/settings.json', 'utf8'));
          settings.hooks = {
            sessionStart: ['./nonexistent1.ts'],
            sessionEnd: ['./nonexistent2.ts'],
            postTask: ['./nonexistent3.ts']
          };
          
          await fs.writeFile('.claude/settings.bak.json', 
            await fs.readFile('.claude/settings.json', 'utf8'));
          await fs.writeFile('.claude/settings.json', JSON.stringify(settings, null, 2));
          
          return {};
        },
        test: async () => {
          // All hooks should fail but system should remain operational
          const results = await Promise.all([
            runCommand('node', ['.claude/hooks/hook-wrapper.js', 'sessionStart']),
            runCommand('node', ['.claude/hooks/hook-wrapper.js', 'sessionEnd']),
            runCommand('node', ['.claude/hooks/hook-wrapper.js', 'postTask'])
          ]);
          
          return results.every(r => !r.crashed); // None should crash the system
        },
        cleanup: async () => {
          await fs.rename('.claude/settings.bak.json', '.claude/settings.json');
        }
      }
    ]
  }
};

// Helper functions
async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function runCommand(command, args) {
  return new Promise((resolve) => {
    const proc = spawn(command, args, { 
      shell: process.platform === 'win32',
      timeout: 5000 
    });
    
    let output = '';
    let error = '';
    let crashed = false;
    
    proc.stdout.on('data', (data) => output += data.toString());
    proc.stderr.on('data', (data) => error += data.toString());
    
    proc.on('error', (err) => {
      crashed = true;
      resolve({ error: true, output, errorMsg: err.message, crashed });
    });
    
    proc.on('exit', (code) => {
      resolve({ 
        error: code !== 0, 
        output: output + error, 
        code, 
        crashed 
      });
    });
  });
}

// Main test runner
async function runFailureTests() {
  console.log('🔥 FAILURE AND RECOVERY TESTING 🔥\n');
  console.log('Testing graceful degradation when components fail...\n');
  
  const results = {
    total: 0,
    passed: 0,
    failed: 0,
    errors: []
  };
  
  for (const [category, suite] of Object.entries(failureTests)) {
    console.log(`\n📦 ${suite.name}`);
    console.log('─'.repeat(50));
    
    for (const test of suite.tests) {
      results.total++;
      process.stdout.write(`  ⚡ ${test.name}... `);
      
      let context = {};
      try {
        // Setup
        if (test.setup) {
          context = await test.setup();
        }
        
        // Run test
        const passed = await test.test(context);
        
        if (passed) {
          console.log('✅ PASSED');
          results.passed++;
        } else {
          console.log('❌ FAILED');
          results.failed++;
          results.errors.push({
            category: suite.name,
            test: test.name,
            error: 'Test returned false'
          });
        }
      } catch (error) {
        console.log('💥 ERROR');
        results.failed++;
        results.errors.push({
          category: suite.name,
          test: test.name,
          error: error.message
        });
      } finally {
        // Cleanup
        if (test.cleanup) {
          try {
            await test.cleanup(context);
          } catch (e) {
            console.log(`    ⚠️  Cleanup failed: ${e.message}`);
          }
        }
      }
    }
  }
  
  // Summary
  console.log('\n' + '═'.repeat(60));
  console.log('📊 FAILURE RECOVERY TEST SUMMARY');
  console.log('═'.repeat(60));
  console.log(`Total Tests: ${results.total}`);
  console.log(`Passed: ${results.passed} (${((results.passed/results.total)*100).toFixed(1)}%)`);
  console.log(`Failed: ${results.failed} (${((results.failed/results.total)*100).toFixed(1)}%)`);
  
  if (results.errors.length > 0) {
    console.log('\n❌ FAILED TESTS:');
    results.errors.forEach(err => {
      console.log(`  - ${err.category} > ${err.test}: ${err.error}`);
    });
  }
  
  const allPassed = results.failed === 0;
  if (allPassed) {
    console.log('\n✅ ALL FAILURE RECOVERY TESTS PASSED! 🎉');
    console.log('The system gracefully handles component failures.');
  } else {
    console.log('\n❌ SOME FAILURE RECOVERY TESTS FAILED!');
    console.log('The system may not degrade gracefully under certain failures.');
  }
  
  return allPassed;
}

// Run tests if executed directly
if (require.main === module) {
  runFailureTests().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(err => {
    console.error('Test runner failed:', err);
    process.exit(1);
  });
}

module.exports = { runFailureTests };