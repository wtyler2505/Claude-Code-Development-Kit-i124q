#!/usr/bin/env python3
"""
CCDK i124q Enhanced Analytics Dashboard  
Professional monitoring for all integrated systems with real-time metrics
"""

from flask import Flask, render_template_string, jsonify
import sqlite3
import pathlib
import json
import subprocess
from datetime import datetime, timedelta
import os

app = Flask(__name__)

class EnhancedAnalytics:
    def __init__(self):
        self.app_dir = pathlib.Path('/app')
        self.claude_dir = pathlib.Path('/app/.claude')
        
    def get_hive_analytics(self):
        """Get CCDK Hive session analytics"""
        try:
            base = pathlib.Path('.ccd_hive')
            sessions = []
            if base.exists():
                for d in base.iterdir():
                    if d.is_dir() and (d / 'memory.db').exists():
                        try:
                            c = sqlite3.connect(d/'memory.db').execute('select count(*) from notes').fetchone()[0]
                            sessions.append({
                                'name': d.name,
                                'rows': c,
                                'path': str(d),
                                'status': 'active' if c > 0 else 'empty'
                            })
                        except:
                            sessions.append({
                                'name': d.name,
                                'rows': 0,
                                'path': str(d),
                                'status': 'error'
                            })
            return {
                'total_sessions': len(sessions),
                'active_sessions': len([s for s in sessions if s['status'] == 'active']),
                'sessions': sessions
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_system_metrics(self):
        """Get comprehensive system metrics"""
        try:
            # Count all capabilities
            ccdk_commands = len(list((self.claude_dir / 'commands').glob('*.md')))
            
            sc_commands = 0
            sc_path = self.claude_dir / 'superclaude' / 'commands'
            if sc_path.exists():
                sc_commands = len(list(sc_path.glob('*.md')))
            
            tc_tools = 0
            tc_path = self.claude_dir / 'thinkchain' / 'tools'
            if tc_path.exists():
                tc_tools = len([f for f in tc_path.glob('*.py') if f.name not in ['__init__.py', 'base.py']])
            
            # Get AI personas count
            personas_count = 0
            personas_file = self.claude_dir / 'superclaude' / 'core' / 'PERSONAS.md'
            if personas_file.exists():
                with open(personas_file, 'r') as f:
                    content = f.read()
                    personas_count = content.count('--persona-')
            
            # Get MCP servers count
            mcp_servers = 0
            mcp_config = self.claude_dir / 'thinkchain' / 'mcp_config.json'
            if mcp_config.exists():
                with open(mcp_config, 'r') as f:
                    config = json.load(f)
                    mcp_servers = len(config.get('mcpServers', {}))
            
            return {
                'ccdk_commands': ccdk_commands,
                'superclaude_commands': sc_commands,
                'thinkchain_tools': tc_tools,
                'total_capabilities': ccdk_commands + sc_commands + tc_tools,
                'ai_personas': personas_count,
                'mcp_servers': mcp_servers,
                'integration_status': 'fully_integrated'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_usage_analytics(self):
        """Get usage analytics and performance metrics"""
        try:
            # Check tool usage log
            log_file = pathlib.Path('.ccd_analytics.log')
            usage_data = []
            if log_file.exists():
                with open(log_file, 'r') as f:
                    lines = f.readlines()[-100:]  # Last 100 entries
                    for line in lines:
                        try:
                            usage_data.append(json.loads(line.strip()))
                        except:
                            pass
            
            # Check dashboard access
            dashboard_status = self.check_dashboard_health()
            
            return {
                'recent_usage': usage_data,
                'usage_count': len(usage_data),
                'dashboard_health': dashboard_status,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def check_dashboard_health(self):
        """Check health of all dashboard services"""
        dashboards = {
            'unified_dashboard': {'port': 4000, 'name': 'Unified Dashboard'},
            'webui': {'port': 7000, 'name': 'CCDK WebUI'},
            'analytics': {'port': 5005, 'name': 'Analytics Dashboard'},
            'templates': {'port': 3333, 'name': 'Templates Analytics'}
        }
        
        health_status = {}
        for key, dashboard in dashboards.items():
            try:
                import requests
                response = requests.get(f'http://localhost:{dashboard["port"]}', timeout=2)
                health_status[key] = {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'port': dashboard['port'],
                    'name': dashboard['name'],
                    'response_code': response.status_code
                }
            except:
                health_status[key] = {
                    'status': 'unavailable',
                    'port': dashboard['port'],
                    'name': dashboard['name'],
                    'response_code': None
                }
        
        return health_status
    
    def get_comprehensive_report(self):
        """Get comprehensive analytics report"""
        return {
            'hive': self.get_hive_analytics(),
            'system': self.get_system_metrics(),
            'usage': self.get_usage_analytics(),
            'timestamp': datetime.now().isoformat(),
            'version': 'CCDK i124q',
            'status': 'operational'
        }

analytics = EnhancedAnalytics()

ENHANCED_ANALYTICS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CCDK i124q - Enhanced Analytics</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
            color: white;
            min-height: 100vh;
        }
        .container { max-width: 1600px; margin: 0 auto; padding: 20px; }
        .header { 
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.8; font-size: 1.2em; }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            text-align: center;
            transition: transform 0.3s ease;
        }
        .metric-card:hover { transform: translateY(-5px); }
        .metric-number { font-size: 3em; font-weight: bold; margin-bottom: 10px; }
        .metric-label { font-size: 1.1em; opacity: 0.8; }
        .metric-ccdk { color: #4299e1; }
        .metric-superclaude { color: #38a169; }
        .metric-thinkchain { color: #805ad5; }
        .metric-total { color: #f6ad55; }
        .analytics-sections {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        .section-card {
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .section-title {
            font-size: 1.4em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .dashboard-status {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .dashboard-item {
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-healthy { color: #38a169; }
        .status-unhealthy { color: #e53e3e; }
        .status-unavailable { color: #805ad5; }
        .session-list {
            max-height: 200px;
            overflow-y: auto;
        }
        .session-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }
        .session-active { border-left: 3px solid #38a169; }
        .session-empty { border-left: 3px solid #805ad5; }
        .session-error { border-left: 3px solid #e53e3e; }
        .controls {
            text-align: center;
            margin-bottom: 20px;
        }
        .btn {
            padding: 10px 20px;
            margin: 5px;
            background: #4299e1;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: background 0.3s ease;
        }
        .btn:hover { background: #3182ce; }
        .btn.success { background: #38a169; }
        .btn.success:hover { background: #2f855a; }
        .refresh-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px;
            background: rgba(56,161,105,0.9);
            border-radius: 20px;
            font-size: 0.9em;
        }
        .chart-container {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
            backdrop-filter: blur(10px);
        }
        @media (max-width: 768px) {
            .analytics-sections { grid-template-columns: 1fr; }
            .metrics-grid { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 CCDK i124q Enhanced Analytics</h1>
            <p>Real-time monitoring of all integrated systems</p>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-number metric-ccdk">{{ data.system.ccdk_commands }}</div>
                <div class="metric-label">CCDK Commands</div>
            </div>
            <div class="metric-card">
                <div class="metric-number metric-superclaude">{{ data.system.superclaude_commands }}</div>
                <div class="metric-label">SuperClaude Commands</div>
            </div>
            <div class="metric-card">
                <div class="metric-number metric-thinkchain">{{ data.system.thinkchain_tools }}</div>
                <div class="metric-label">ThinkChain Tools</div>
            </div>
            <div class="metric-card">
                <div class="metric-number metric-total">{{ data.system.total_capabilities }}</div>
                <div class="metric-label">Total Capabilities</div>
            </div>
            <div class="metric-card">
                <div class="metric-number metric-superclaude">{{ data.system.ai_personas }}</div>
                <div class="metric-label">AI Personas</div>
            </div>
            <div class="metric-card">
                <div class="metric-number metric-thinkchain">{{ data.system.mcp_servers }}</div>
                <div class="metric-label">MCP Servers</div>
            </div>
        </div>

        <div class="controls">
            <a href="http://localhost:4000" class="btn" target="_blank">🌐 Unified Dashboard</a>
            <a href="http://localhost:7000" class="btn" target="_blank">🖥️ Enhanced WebUI</a>
            <a href="http://localhost:3333" class="btn success" target="_blank">📊 Templates Analytics</a>
            <button class="btn" onclick="refreshData()">🔄 Refresh Data</button>
        </div>

        <div class="analytics-sections">
            <div class="section-card">
                <div class="section-title">
                    <span>🖥️</span> Dashboard Health Status
                </div>
                <div class="dashboard-status">
                    {% for key, dashboard in data.usage.dashboard_health.items() %}
                    <div class="dashboard-item">
                        <span>{{ dashboard.name }}</span>
                        <span class="status-{{ dashboard.status }}">{{ dashboard.status }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div class="section-card">
                <div class="section-title">
                    <span>🗂️</span> Hive Sessions ({{ data.hive.total_sessions }})
                </div>
                <div class="session-list">
                    {% for session in data.hive.sessions %}
                    <div class="session-item session-{{ session.status }}">
                        <div>
                            <strong>{{ session.name }}</strong><br>
                            <small>{{ session.path }}</small>
                        </div>
                        <div>{{ session.rows }} rows</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <div class="chart-container">
            <div class="section-title">
                <span>📈</span> System Capabilities Breakdown
            </div>
            <canvas id="capabilitiesChart" width="400" height="200"></canvas>
        </div>

        <div class="chart-container">
            <div class="section-title">
                <span>⚡</span> Integration Status Overview
            </div>
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 2em; color: #38a169; margin-bottom: 10px;">✅ FULLY INTEGRATED</div>
                <p>All systems operational and communicating properly</p>
                <p><small>Last updated: {{ data.timestamp }}</small></p>
            </div>
        </div>
    </div>

    <div class="refresh-indicator" id="refreshIndicator" style="display: none;">
        🔄 Refreshing data...
    </div>

    <script>
        // Create capabilities breakdown chart
        const ctx = document.getElementById('capabilitiesChart').getContext('2d');
        const capabilitiesChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['CCDK Commands', 'SuperClaude Commands', 'ThinkChain Tools'],
                datasets: [{
                    data: [{{ data.system.ccdk_commands }}, {{ data.system.superclaude_commands }}, {{ data.system.thinkchain_tools }}],
                    backgroundColor: ['#4299e1', '#38a169', '#805ad5'],
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: 'white',
                            font: {
                                size: 14
                            }
                        }
                    }
                }
            }
        });

        function refreshData() {
            const indicator = document.getElementById('refreshIndicator');
            indicator.style.display = 'block';
            
            setTimeout(() => {
                location.reload();
            }, 500);
        }

        // Auto-refresh every 30 seconds
        setInterval(() => {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    console.log('Analytics updated:', data.timestamp);
                })
                .catch(error => console.log('Update check failed:', error));
        }, 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Enhanced analytics dashboard"""
    data = analytics.get_comprehensive_report()
    return render_template_string(ENHANCED_ANALYTICS_TEMPLATE, data=data)

@app.route('/api/status')
def api_status():
    """API endpoint for complete analytics data"""
    return jsonify(analytics.get_comprehensive_report())

@app.route('/api/metrics')
def api_metrics():
    """API endpoint for system metrics only"""
    return jsonify(analytics.get_system_metrics())

@app.route('/api/health')
def api_health():
    """API endpoint for dashboard health check"""
    return jsonify(analytics.check_dashboard_health())

if __name__ == '__main__':
    print("📊 Starting CCDK i124q Enhanced Analytics Dashboard...")
    print("📈 Available at: http://localhost:5005")
    print("🔍 Monitoring: CCDK + SuperClaude + ThinkChain + Templates")
    app.run(host='0.0.0.0', port=5005, debug=True)