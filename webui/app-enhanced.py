#!/usr/bin/env python3
"""
CCDK i124q Enhanced WebUI
Professional interface showing all integrated components with real-time updates
"""

from flask import Flask, render_template_string, jsonify, request
import pathlib
import json
import sqlite3
import subprocess
import os
from datetime import datetime

app = Flask(__name__)

class CCDKiEnhancedUI:
    def __init__(self):
        self.app_dir = pathlib.Path('/app')
        self.claude_dir = pathlib.Path('/app/.claude')
        
    def get_all_commands(self):
        """Get commands from all integrated systems"""
        commands = {}
        
        # CCDK Original Commands
        ccdk_commands = []
        ccdk_path = self.claude_dir / 'commands'
        if ccdk_path.exists():
            for cmd_file in ccdk_path.glob('*.md'):
                ccdk_commands.append({
                    'name': cmd_file.stem,
                    'file': cmd_file.name,
                    'system': 'CCDK',
                    'namespace': 'original'
                })
        
        # SuperClaude Commands
        sc_commands = []
        sc_path = self.claude_dir / 'superclaude' / 'commands'
        if sc_path.exists():
            for cmd_file in sc_path.glob('*.md'):
                sc_commands.append({
                    'name': f"sc:{cmd_file.stem}",
                    'file': cmd_file.name,
                    'system': 'SuperClaude',
                    'namespace': 'sc'
                })
        
        # ThinkChain Tools (as commands)
        tc_tools = []
        tc_path = self.claude_dir / 'thinkchain' / 'tools'
        if tc_path.exists():
            for tool_file in tc_path.glob('*.py'):
                if tool_file.name not in ['__init__.py', 'base.py']:
                    tc_tools.append({
                        'name': tool_file.stem,
                        'file': tool_file.name,
                        'system': 'ThinkChain',
                        'namespace': 'tool'
                    })
        
        commands = {
            'ccdk': ccdk_commands,
            'superclaude': sc_commands,
            'thinkchain': tc_tools
        }
        
        return commands
    
    def get_system_stats(self):
        """Get comprehensive system statistics"""
        try:
            commands = self.get_all_commands()
            
            # Get SuperClaude personas
            personas_count = 0
            personas_file = self.claude_dir / 'superclaude' / 'core' / 'PERSONAS.md'
            if personas_file.exists():
                with open(personas_file, 'r') as f:
                    content = f.read()
                    personas_count = content.count('--persona-')
            
            # Get ThinkChain MCP servers
            mcp_servers = 0
            mcp_config = self.claude_dir / 'thinkchain' / 'mcp_config.json'
            if mcp_config.exists():
                with open(mcp_config, 'r') as f:
                    config = json.load(f)
                    mcp_servers = len(config.get('mcpServers', {}))
            
            # Get hive session data
            hive_sessions = 0
            session_rows = 0
            try:
                hive_db = self.app_dir / '.ccd_hive/test-session/memory.db'
                if hive_db.exists():
                    conn = sqlite3.connect(str(hive_db))
                    session_rows = conn.execute('select count(*) from notes').fetchone()[0]
                    hive_sessions = 1
                    conn.close()
            except:
                pass
            
            return {
                'ccdk_commands': len(commands['ccdk']),
                'superclaude_commands': len(commands['superclaude']),
                'thinkchain_tools': len(commands['thinkchain']),
                'total_capabilities': len(commands['ccdk']) + len(commands['superclaude']) + len(commands['thinkchain']),
                'ai_personas': personas_count,
                'mcp_servers': mcp_servers,
                'hive_sessions': hive_sessions,
                'session_rows': session_rows,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_command_details(self, system, command_name):
        """Get detailed information about a specific command"""
        try:
            if system == 'ccdk':
                cmd_file = self.claude_dir / 'commands' / f'{command_name}.md'
            elif system == 'superclaude':
                cmd_file = self.claude_dir / 'superclaude' / 'commands' / f'{command_name}.md'
            elif system == 'thinkchain':
                cmd_file = self.claude_dir / 'thinkchain' / 'tools' / f'{command_name}.py'
            else:
                return {'error': 'Unknown system'}
            
            if cmd_file.exists():
                with open(cmd_file, 'r') as f:
                    content = f.read()
                return {
                    'name': command_name,
                    'system': system,
                    'content': content[:500] + '...' if len(content) > 500 else content,
                    'full_content': content
                }
            else:
                return {'error': 'Command not found'}
                
        except Exception as e:
            return {'error': str(e)}

ui_manager = CCDKiEnhancedUI()

ENHANCED_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CCDK i124q - Enhanced WebUI</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
            color: white;
            min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { 
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.8; font-size: 1.1em; }
        .stats-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-item {
            text-align: center;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            backdrop-filter: blur(5px);
        }
        .stat-number { font-size: 2em; font-weight: bold; color: #4299e1; }
        .stat-label { font-size: 0.9em; opacity: 0.8; margin-top: 5px; }
        .systems-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .system-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .system-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }
        .system-header h3 { font-size: 1.3em; }
        .system-icon { font-size: 1.5em; }
        .command-list {
            max-height: 300px;
            overflow-y: auto;
        }
        .command-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .command-item:hover {
            background: rgba(255,255,255,0.15);
        }
        .command-name { font-weight: 600; }
        .command-system { 
            font-size: 0.8em; 
            opacity: 0.7;
            background: rgba(255,255,255,0.1);
            padding: 2px 8px;
            border-radius: 12px;
        }
        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            justify-content: center;
        }
        .btn {
            padding: 10px 20px;
            background: #4299e1;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover { background: #3182ce; }
        .btn.success { background: #38a169; }
        .btn.success:hover { background: #2f855a; }
        .btn.purple { background: #805ad5; }
        .btn.purple:hover { background: #6b46c1; }
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 15px;
            background: #805ad5;
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.2em;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
        }
        .modal-content {
            background: #1a202c;
            margin: 5% auto;
            padding: 20px;
            border-radius: 15px;
            width: 80%;
            max-width: 800px;
            color: white;
        }
        .close { float: right; font-size: 28px; cursor: pointer; }
        .integration-badge {
            display: inline-block;
            background: linear-gradient(45deg, #4299e1, #38a169);
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 600;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 CCDK i124q Enhanced WebUI</h1>
            <p>Complete Command & Tool Browser with Multi-System Integration</p>
            <span class="integration-badge">{{ stats.total_capabilities }} Total Capabilities</span>
        </div>
        
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-number">{{ stats.ccdk_commands }}</div>
                <div class="stat-label">CCDK Commands</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ stats.superclaude_commands }}</div>
                <div class="stat-label">SuperClaude Commands</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ stats.thinkchain_tools }}</div>
                <div class="stat-label">ThinkChain Tools</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ stats.ai_personas }}</div>
                <div class="stat-label">AI Personas</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ stats.mcp_servers }}</div>
                <div class="stat-label">MCP Servers</div>
            </div>
        </div>

        <div class="controls">
            <a href="http://localhost:4000" class="btn" target="_blank">🌐 Unified Dashboard</a>
            <a href="http://localhost:5005" class="btn success" target="_blank">📈 Analytics</a>
            <a href="http://localhost:3333" class="btn purple" target="_blank">📊 Templates</a>
            <button class="btn" onclick="refreshData()">🔄 Refresh</button>
        </div>

        <div class="systems-grid">
            <div class="system-card">
                <div class="system-header">
                    <span class="system-icon">🏗️</span>
                    <h3>CCDK Foundation</h3>
                </div>
                <div class="command-list" id="ccdk-commands">
                    {% for cmd in commands.ccdk %}
                    <div class="command-item" onclick="showCommand('ccdk', '{{ cmd.name }}')">
                        <span class="command-name">/{{ cmd.name }}</span>
                        <span class="command-system">CCDK</span>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div class="system-card">
                <div class="system-header">
                    <span class="system-icon">🎭</span>
                    <h3>SuperClaude Framework</h3>
                </div>
                <div class="command-list" id="superclaude-commands">
                    {% for cmd in commands.superclaude %}
                    <div class="command-item" onclick="showCommand('superclaude', '{{ cmd.name.replace('sc:', '') }}')">
                        <span class="command-name">/{{ cmd.name }}</span>
                        <span class="command-system">SuperClaude</span>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div class="system-card">
                <div class="system-header">
                    <span class="system-icon">⚡</span>
                    <h3>ThinkChain Tools</h3>
                </div>
                <div class="command-list" id="thinkchain-tools">
                    {% for tool in commands.thinkchain %}
                    <div class="command-item" onclick="showCommand('thinkchain', '{{ tool.name }}')">
                        <span class="command-name">{{ tool.name }}</span>
                        <span class="command-system">ThinkChain</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <button class="refresh-btn" onclick="refreshData()" title="Refresh Data">🔄</button>

    <!-- Command Detail Modal -->
    <div id="commandModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2 id="modalTitle">Command Details</h2>
            <div id="modalContent">Loading...</div>
        </div>
    </div>

    <script>
        function refreshData() {
            location.reload();
        }

        function showCommand(system, command) {
            document.getElementById('commandModal').style.display = 'block';
            document.getElementById('modalTitle').textContent = `${system}: ${command}`;
            document.getElementById('modalContent').textContent = 'Loading...';
            
            fetch(`/command/${system}/${command}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('modalContent').innerHTML = `<p style="color: #e53e3e;">Error: ${data.error}</p>`;
                    } else {
                        document.getElementById('modalContent').innerHTML = `
                            <h3>System: ${data.system}</h3>
                            <p><strong>Name:</strong> ${data.name}</p>
                            <h4>Description:</h4>
                            <pre style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; overflow-x: auto;">${data.content}</pre>
                        `;
                    }
                })
                .catch(error => {
                    document.getElementById('modalContent').innerHTML = `<p style="color: #e53e3e;">Error loading command details</p>`;
                });
        }

        function closeModal() {
            document.getElementById('commandModal').style.display = 'none';
        }

        // Auto-refresh every 60 seconds
        setInterval(() => {
            // Silently refresh stats without full page reload
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    // Update stats without reloading
                    console.log('Stats refreshed:', data);
                });
        }, 60000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main enhanced dashboard page"""
    commands = ui_manager.get_all_commands()
    stats = ui_manager.get_system_stats()
    return render_template_string(ENHANCED_TEMPLATE, commands=commands, stats=stats)

@app.route('/api/stats')
def api_stats():
    """API endpoint for system statistics"""
    return jsonify(ui_manager.get_system_stats())

@app.route('/api/commands')
def api_commands():
    """API endpoint for all commands"""
    return jsonify(ui_manager.get_all_commands())

@app.route('/command/<system>/<command_name>')
def command_details(system, command_name):
    """Get detailed information about a command"""
    return jsonify(ui_manager.get_command_details(system, command_name))

if __name__ == '__main__':
    print("🚀 Starting CCDK i124q Enhanced WebUI...")
    print("🌐 Available at: http://localhost:7000")
    print("📊 Showing all integrated systems: CCDK + SuperClaude + ThinkChain")
    app.run(host='0.0.0.0', port=7000, debug=True)