#!/usr/bin/env python3
"""
CCDK i124q - Unified Dashboard
Combines CCDK, SuperClaude, ThinkChain, and Templates dashboards into one interface
"""

from flask import Flask, render_template_string, jsonify, request
import sqlite3
import pathlib
import subprocess
import json
import os
from datetime import datetime
import requests

app = Flask(__name__)

class UnifiedDashboard:
    def __init__(self):
        self.app_dir = pathlib.Path('/app')
        self.claude_dir = pathlib.Path('/app/.claude')
        
    def get_ccdk_stats(self):
        """Get CCDK system statistics"""
        try:
            # Count CCDK commands
            ccdk_commands = list((self.claude_dir / 'commands').glob('*.md'))
            
            # Count hive sessions
            hive_sessions = 0
            session_rows = 0
            try:
                if (self.app_dir / '.ccd_hive/test-session/memory.db').exists():
                    conn = sqlite3.connect(str(self.app_dir / '.ccd_hive/test-session/memory.db'))
                    session_rows = conn.execute('select count(*) from notes').fetchone()[0]
                    hive_sessions = 1
                    conn.close()
            except:
                pass
                
            return {
                'commands': len(ccdk_commands),
                'hive_sessions': hive_sessions,
                'session_rows': session_rows,
                'status': 'active'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_superclaude_stats(self):
        """Get SuperClaude system statistics"""
        try:
            # Count SuperClaude commands
            sc_commands = list((self.claude_dir / 'superclaude/commands').glob('*.md'))
            
            # Check personas file
            personas_file = self.claude_dir / 'superclaude/core/PERSONAS.md'
            personas_count = 0
            if personas_file.exists():
                with open(personas_file, 'r') as f:
                    content = f.read()
                    personas_count = content.count('--persona-')
            
            return {
                'commands': len(sc_commands),
                'personas': personas_count,
                'version': '3.0.0.2',
                'status': 'integrated'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_thinkchain_stats(self):
        """Get ThinkChain system statistics"""
        try:
            # Count ThinkChain tools
            tc_tools = list((self.claude_dir / 'thinkchain/tools').glob('*.py'))
            tc_tools = [t for t in tc_tools if t.name not in ['__init__.py', 'base.py']]
            
            # Check MCP configuration
            mcp_config_file = self.claude_dir / 'thinkchain/mcp_config.json'
            mcp_servers = 0
            if mcp_config_file.exists():
                with open(mcp_config_file, 'r') as f:
                    config = json.load(f)
                    mcp_servers = len(config.get('mcpServers', {}))
            
            return {
                'tools': len(tc_tools),
                'mcp_servers': mcp_servers,
                'streaming': 'enabled',
                'status': 'integrated'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_templates_stats(self):
        """Get Templates system statistics"""
        try:
            # Check if templates CLI is available
            result = subprocess.run(['claude-code-templates', '--version'], 
                                    capture_output=True, text=True, timeout=5)
            version = result.stdout.strip().split('\n')[-1] if result.returncode == 0 else 'unknown'
            
            return {
                'version': version,
                'analytics_port': 3333,
                'cli_available': result.returncode == 0,
                'status': 'available'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_system_overview(self):
        """Get complete system overview"""
        ccdk = self.get_ccdk_stats()
        superclaude = self.get_superclaude_stats()
        thinkchain = self.get_thinkchain_stats()
        templates = self.get_templates_stats()
        
        total_capabilities = (
            ccdk.get('commands', 0) + 
            superclaude.get('commands', 0) + 
            thinkchain.get('tools', 0)
        )
        
        return {
            'ccdk': ccdk,
            'superclaude': superclaude,
            'thinkchain': thinkchain,
            'templates': templates,
            'total_capabilities': total_capabilities,
            'integration_status': 'phase_3_active',
            'timestamp': datetime.now().isoformat()
        }

dashboard = UnifiedDashboard()

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CCDK i124q - Unified Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { 
            text-align: center; 
            color: white; 
            margin-bottom: 30px;
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .stat-card { 
            background: rgba(255,255,255,0.95);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stat-card:hover { 
            transform: translateY(-5px);
            box-shadow: 0 12px 48px rgba(0,0,0,0.15);
        }
        .stat-card h3 { 
            color: #4a5568;
            margin-bottom: 15px;
            font-size: 1.3em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .stat-item { 
            display: flex; 
            justify-content: space-between; 
            margin: 10px 0;
            padding: 8px 0;
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }
        .stat-item:last-child { border-bottom: none; }
        .stat-label { font-weight: 600; }
        .stat-value { 
            color: #2d3748;
            font-weight: 700;
        }
        .status-active { color: #38a169; }
        .status-integrated { color: #3182ce; }
        .status-available { color: #805ad5; }
        .overview-card {
            background: rgba(255,255,255,0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            text-align: center;
            margin-bottom: 20px;
        }
        .total-capabilities { 
            font-size: 3em; 
            color: #4a5568;
            margin: 20px 0;
            font-weight: 700;
        }
        .dashboard-links { 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .dashboard-link {
            display: inline-block;
            padding: 12px 20px;
            background: #4299e1;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            text-align: center;
            transition: background 0.3s ease;
        }
        .dashboard-link:hover { background: #3182ce; }
        .dashboard-link.analytics { background: #38a169; }
        .dashboard-link.analytics:hover { background: #2f855a; }
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 12px 20px;
            background: #805ad5;
            color: white;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: background 0.3s ease;
        }
        .refresh-btn:hover { background: #6b46c1; }
        .emoji { font-size: 1.2em; }
        .integration-status {
            display: inline-block;
            padding: 6px 12px;
            background: linear-gradient(45deg, #4299e1, #38a169);
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            margin-left: 10px;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .pulse { animation: pulse 2s infinite; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 CCDK i124q Unified Dashboard</h1>
            <p>Claude Code Development Kit - Enhanced Community Integration</p>
            <span class="integration-status pulse">Phase 3: Templates Integration Active</span>
        </div>
        
        <div class="overview-card">
            <h2>🎯 System Overview</h2>
            <div class="total-capabilities">{{ stats.total_capabilities }}</div>
            <p><strong>Total Integrated Capabilities</strong></p>
            <p style="margin-top: 15px; color: #666;">
                The most comprehensive Claude Code enhancement toolkit, combining the best from 4 major frameworks
            </p>
        </div>

        <div class="stats-grid">
            <!-- CCDK Core -->
            <div class="stat-card">
                <h3><span class="emoji">🏗️</span> CCDK Foundation</h3>
                <div class="stat-item">
                    <span class="stat-label">Commands</span>
                    <span class="stat-value">{{ stats.ccdk.commands }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Hive Sessions</span>
                    <span class="stat-value">{{ stats.ccdk.hive_sessions }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Session Rows</span>
                    <span class="stat-value">{{ stats.ccdk.session_rows }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Status</span>
                    <span class="stat-value status-active">{{ stats.ccdk.status }}</span>
                </div>
            </div>

            <!-- SuperClaude -->
            <div class="stat-card">
                <h3><span class="emoji">🎭</span> SuperClaude Framework</h3>
                <div class="stat-item">
                    <span class="stat-label">Commands</span>
                    <span class="stat-value">{{ stats.superclaude.commands }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">AI Personas</span>
                    <span class="stat-value">{{ stats.superclaude.personas }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Version</span>
                    <span class="stat-value">{{ stats.superclaude.version }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Status</span>
                    <span class="stat-value status-integrated">{{ stats.superclaude.status }}</span>
                </div>
            </div>

            <!-- ThinkChain -->
            <div class="stat-card">
                <h3><span class="emoji">⚡</span> ThinkChain Engine</h3>
                <div class="stat-item">
                    <span class="stat-label">Advanced Tools</span>
                    <span class="stat-value">{{ stats.thinkchain.tools }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">MCP Servers</span>
                    <span class="stat-value">{{ stats.thinkchain.mcp_servers }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Streaming</span>
                    <span class="stat-value">{{ stats.thinkchain.streaming }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Status</span>
                    <span class="stat-value status-integrated">{{ stats.thinkchain.status }}</span>
                </div>
            </div>

            <!-- Templates -->
            <div class="stat-card">
                <h3><span class="emoji">📊</span> Templates Analytics</h3>
                <div class="stat-item">
                    <span class="stat-label">Version</span>
                    <span class="stat-value">{{ stats.templates.version }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Analytics Port</span>
                    <span class="stat-value">{{ stats.templates.analytics_port }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">CLI Available</span>
                    <span class="stat-value">{{ 'Yes' if stats.templates.cli_available else 'No' }}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Status</span>
                    <span class="stat-value status-available">{{ stats.templates.status }}</span>
                </div>
            </div>
        </div>

        <div class="dashboard-links">
            <a href="http://localhost:7000" class="dashboard-link" target="_blank">
                🌐 CCDK WebUI (Port 7000)
            </a>
            <a href="http://localhost:5005" class="dashboard-link" target="_blank">
                📈 CCDK Analytics (Port 5005)
            </a>
            <a href="http://localhost:3333" class="dashboard-link analytics" target="_blank">
                📊 Templates Analytics (Port 3333)
            </a>
            <a href="/api/status" class="dashboard-link" target="_blank">
                🔍 System Status API
            </a>
        </div>
    </div>

    <button class="refresh-btn" onclick="location.reload()">
        🔄 Refresh
    </button>

    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard page"""
    stats = dashboard.get_system_overview()
    return render_template_string(DASHBOARD_TEMPLATE, stats=stats)

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify(dashboard.get_system_overview())

@app.route('/api/refresh')
def api_refresh():
    """API endpoint to refresh data"""
    return jsonify({'status': 'refreshed', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("🚀 Starting CCDK i124q Unified Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:4000")
    print("🔗 Integrating: CCDK + SuperClaude + ThinkChain + Templates")
    app.run(host='0.0.0.0', port=4000, debug=True)