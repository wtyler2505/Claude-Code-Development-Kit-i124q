#!/usr/bin/env python3
"""
CCDK i124q - Professional Launch Script
Starts all enhanced dashboards and services with proper monitoring
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path
import json
import requests

class CCDKi124qLauncher:
    def __init__(self):
        self.app_dir = Path('/app')
        self.processes = {}
        self.running = True
        
    def print_banner(self):
        """Display launch banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🚀 CCDK i124q - Professional Dashboard Launcher            ║
║                                                              ║
║  Starting the Ultimate Claude Code Enhancement Toolkit      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🌟 Launching all integrated systems:
   • Unified Dashboard (Port 4000)
   • Enhanced WebUI (Port 7000)  
   • Enhanced Analytics (Port 5005)
   • Templates Analytics (Port 3333)
   
🎯 37+ Total capabilities across CCDK + SuperClaude + ThinkChain + Templates
"""
        print(banner)
    
    def start_service(self, name, script_path, port, description):
        """Start a dashboard service"""
        print(f"🔄 Starting {name}...")
        
        try:
            if not script_path.exists():
                print(f"❌ Script not found: {script_path}")
                return False
            
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.app_dir
            )
            
            self.processes[name] = {
                'process': process,
                'port': port,
                'description': description,
                'script': str(script_path)
            }
            
            # Wait a moment for startup
            time.sleep(2)
            
            # Check if service is responding
            if self.check_service_health(port):
                print(f"✅ {name} started successfully on port {port}")
                return True
            else:
                print(f"⚠️  {name} started but not yet responding on port {port}")
                return True  # Still consider it started
                
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return False
    
    def check_service_health(self, port, timeout=5):
        """Check if a service is responding"""
        try:
            response = requests.get(f'http://localhost:{port}', timeout=timeout)
            return response.status_code == 200
        except:
            return False
    
    def start_all_services(self):
        """Start all CCDK i124q services"""
        services = [
            {
                'name': 'Unified Dashboard',
                'script': self.app_dir / 'unified-dashboard.py',
                'port': 4000,
                'description': 'Main integration dashboard'
            },
            {
                'name': 'Enhanced WebUI',
                'script': self.app_dir / 'webui' / 'app-enhanced.py',
                'port': 7000,
                'description': 'Command browser with all systems'
            },
            {
                'name': 'Enhanced Analytics',
                'script': self.app_dir / 'dashboard' / 'app-enhanced.py',
                'port': 5005,
                'description': 'Advanced analytics monitoring'
            }
        ]
        
        started_services = []
        failed_services = []
        
        for service in services:
            if self.start_service(
                service['name'],
                service['script'],
                service['port'],
                service['description']
            ):
                started_services.append(service)
            else:
                failed_services.append(service)
        
        # Try to start Templates Analytics (external)
        print("\n🔄 Starting Templates Analytics...")
        try:
            templates_process = subprocess.Popen(
                ['claude-code-templates', '--analytics'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(3)
            if templates_process.poll() is None:  # Still running
                self.processes['Templates Analytics'] = {
                    'process': templates_process,
                    'port': 3333,
                    'description': 'Templates system analytics',
                    'script': 'claude-code-templates CLI'
                }
                print("✅ Templates Analytics started on port 3333")
                started_services.append({'name': 'Templates Analytics', 'port': 3333})
            else:
                print("⚠️  Templates Analytics may not be available")
        except Exception as e:
            print(f"⚠️  Templates Analytics unavailable: {e}")
        
        return started_services, failed_services
    
    def display_service_status(self, started_services):
        """Display the status of all services"""
        print("\n" + "="*70)
        print("🌐 CCDK i124q Dashboard Services Status")
        print("="*70)
        
        if not started_services:
            print("❌ No services are running")
            return
        
        for service in started_services:
            port = service['port']
            name = service['name']
            
            # Check if service is healthy
            health = "🟢 Healthy" if self.check_service_health(port) else "🟡 Starting"
            
            print(f"✅ {name:<25} http://localhost:{port:<4} {health}")
        
        print("="*70)
        print("🎯 Access your CCDK i124q system at any of the URLs above")
        print("🔄 Press Ctrl+C to stop all services")
        print("="*70)
    
    def monitor_services(self):
        """Monitor running services and restart if needed"""
        while self.running:
            time.sleep(30)  # Check every 30 seconds
            
            dead_services = []
            for name, service_info in self.processes.items():
                if service_info['process'].poll() is not None:
                    dead_services.append(name)
            
            for service_name in dead_services:
                print(f"\n⚠️  Service {service_name} has stopped. Attempting restart...")
                service_info = self.processes[service_name]
                
                # Try to restart
                try:
                    if service_name == 'Templates Analytics':
                        new_process = subprocess.Popen(
                            ['claude-code-templates', '--analytics'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                    else:
                        new_process = subprocess.Popen(
                            [sys.executable, service_info['script']],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=self.app_dir
                        )
                    
                    self.processes[service_name]['process'] = new_process
                    print(f"✅ {service_name} restarted successfully")
                    
                except Exception as e:
                    print(f"❌ Failed to restart {service_name}: {e}")
                    del self.processes[service_name]
    
    def setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print("\n\n🛑 Shutting down CCDK i124q services...")
            self.running = False
            self.cleanup_services()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def cleanup_services(self):
        """Clean up all running services"""
        for name, service_info in self.processes.items():
            try:
                process = service_info['process']
                if process.poll() is None:  # Still running
                    print(f"🔄 Stopping {name}...")
                    process.terminate()
                    time.sleep(2)
                    if process.poll() is None:  # Still running after terminate
                        process.kill()
                    print(f"✅ {name} stopped")
            except Exception as e:
                print(f"⚠️  Error stopping {name}: {e}")
    
    def run_health_check(self):
        """Run initial health check of the system"""
        print("\n🔍 Running system health check...")
        
        # Check if CCDK i124q is properly installed
        checks = []
        
        # Check directory structure
        claude_dir = Path.home() / '.claude'
        if claude_dir.exists():
            checks.append("✅ CCDK directory structure")
        else:
            checks.append("❌ CCDK directory structure missing")
        
        # Check dashboard files
        dashboard_files = [
            self.app_dir / 'unified-dashboard.py',
            self.app_dir / 'webui' / 'app-enhanced.py',
            self.app_dir / 'dashboard' / 'app-enhanced.py'
        ]
        
        all_files_exist = all(f.exists() for f in dashboard_files)
        if all_files_exist:
            checks.append("✅ Dashboard files present")
        else:
            checks.append("❌ Some dashboard files missing")
        
        # Check SuperClaude installation
        try:
            import SuperClaude
            checks.append("✅ SuperClaude Framework installed")
        except ImportError:
            checks.append("⚠️  SuperClaude Framework not installed")
        
        # Check Templates CLI
        import shutil
        if shutil.which('claude-code-templates'):
            checks.append("✅ Templates CLI available")
        else:
            checks.append("⚠️  Templates CLI not installed")
        
        for check in checks:
            print(f"   {check}")
        
        healthy_count = len([c for c in checks if c.startswith('✅')])
        total_checks = len(checks)
        
        print(f"\n📊 System Health: {healthy_count}/{total_checks} checks passed")
        
        if healthy_count < total_checks:
            print("⚠️  Some components may not be fully functional")
            print("💡 Consider running the CCDK i124q installer to fix issues")
        else:
            print("🎉 All systems are ready for launch!")
        
        return healthy_count >= (total_checks * 0.75)  # 75% success rate required
    
    def launch(self):
        """Main launch function"""
        self.print_banner()
        
        # Run health check
        if not self.run_health_check():
            print("\n⚠️  System health check failed. Proceeding anyway...")
        
        # Set up signal handlers
        self.setup_signal_handlers()
        
        # Start all services
        print("\n🚀 Starting CCDK i124q services...")
        started_services, failed_services = self.start_all_services()
        
        if failed_services:
            print(f"\n⚠️  {len(failed_services)} services failed to start:")
            for service in failed_services:
                print(f"   ❌ {service['name']}")
        
        if not started_services:
            print("\n❌ No services started successfully. Exiting.")
            return False
        
        # Display service status
        self.display_service_status(started_services)
        
        # Start monitoring in background
        monitor_thread = threading.Thread(target=self.monitor_services, daemon=True)
        monitor_thread.start()
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
        return True

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("""
CCDK i124q Professional Launcher

Usage: python launch-ccdk-i124q.py [options]

Options:
  --help, -h    Show this help message
  --check       Run health check only
  --force       Force start even if health check fails

This launcher starts all CCDK i124q dashboard services:
- Unified Dashboard (Port 4000) - Main integration interface
- Enhanced WebUI (Port 7000) - Command browser with all systems
- Enhanced Analytics (Port 5005) - Advanced monitoring dashboard
- Templates Analytics (Port 3333) - Templates system dashboard

Press Ctrl+C to stop all services gracefully.
""")
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        launcher = CCDKi124qLauncher()
        launcher.run_health_check()
        return
    
    launcher = CCDKi124qLauncher()
    try:
        success = launcher.launch()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Launch failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()