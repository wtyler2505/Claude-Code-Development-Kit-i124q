#!/usr/bin/env python3
"""
CCDK i124q Backend Testing Suite
Comprehensive testing of all Flask services and integrations
"""

import requests
import json
import sqlite3
import pathlib
import time
import sys
from datetime import datetime

class CCDKBackendTester:
    def __init__(self):
        self.services = {
            'unified_dashboard': {
                'url': 'http://localhost:4000',
                'name': 'Unified Dashboard',
                'endpoints': ['/', '/api/status', '/api/refresh']
            },
            'enhanced_webui': {
                'url': 'http://localhost:7000', 
                'name': 'Enhanced WebUI',
                'endpoints': ['/', '/api/stats', '/api/commands']
            },
            'enhanced_analytics': {
                'url': 'http://localhost:5005',
                'name': 'Enhanced Analytics', 
                'endpoints': ['/', '/api/status', '/api/metrics', '/api/health']
            }
        }
        self.test_results = {}
        self.app_dir = pathlib.Path('/app')
        self.claude_dir = pathlib.Path('/app/.claude')
        
    def log_test(self, service, test_name, status, details=""):
        """Log test results"""
        if service not in self.test_results:
            self.test_results[service] = {}
        self.test_results[service][test_name] = {
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
    def test_service_health(self, service_key):
        """Test basic service health and connectivity"""
        service = self.services[service_key]
        print(f"\n🔍 Testing {service['name']} ({service['url']})...")
        
        try:
            response = requests.get(service['url'], timeout=10)
            if response.status_code == 200:
                self.log_test(service_key, 'health_check', 'PASS', f"Service responding with status {response.status_code}")
                print(f"  ✅ Health check: PASS (Status: {response.status_code})")
                return True
            else:
                self.log_test(service_key, 'health_check', 'FAIL', f"Unexpected status code: {response.status_code}")
                print(f"  ❌ Health check: FAIL (Status: {response.status_code})")
                return False
        except Exception as e:
            self.log_test(service_key, 'health_check', 'FAIL', f"Connection error: {str(e)}")
            print(f"  ❌ Health check: FAIL ({str(e)})")
            return False
    
    def test_api_endpoints(self, service_key):
        """Test all API endpoints for a service"""
        service = self.services[service_key]
        print(f"\n🔗 Testing API endpoints for {service['name']}...")
        
        passed = 0
        total = len(service['endpoints'])
        
        for endpoint in service['endpoints']:
            url = service['url'] + endpoint
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # Try to parse JSON for API endpoints
                    if endpoint.startswith('/api/'):
                        try:
                            data = response.json()
                            self.log_test(service_key, f'endpoint_{endpoint}', 'PASS', f"Valid JSON response with {len(data)} keys")
                            print(f"  ✅ {endpoint}: PASS (JSON with {len(data)} keys)")
                        except:
                            self.log_test(service_key, f'endpoint_{endpoint}', 'PASS', "Valid response but not JSON")
                            print(f"  ✅ {endpoint}: PASS (Non-JSON response)")
                    else:
                        self.log_test(service_key, f'endpoint_{endpoint}', 'PASS', f"HTML response length: {len(response.text)}")
                        print(f"  ✅ {endpoint}: PASS (HTML, {len(response.text)} chars)")
                    passed += 1
                else:
                    self.log_test(service_key, f'endpoint_{endpoint}', 'FAIL', f"Status: {response.status_code}")
                    print(f"  ❌ {endpoint}: FAIL (Status: {response.status_code})")
            except Exception as e:
                self.log_test(service_key, f'endpoint_{endpoint}', 'FAIL', str(e))
                print(f"  ❌ {endpoint}: FAIL ({str(e)})")
        
        print(f"  📊 API Endpoints: {passed}/{total} passed")
        return passed == total
    
    def test_unified_dashboard_data(self):
        """Test Unified Dashboard specific functionality"""
        print(f"\n📊 Testing Unified Dashboard data aggregation...")
        
        try:
            response = requests.get('http://localhost:4000/api/status', timeout=10)
            if response.status_code != 200:
                self.log_test('unified_dashboard', 'data_aggregation', 'FAIL', f"API not accessible: {response.status_code}")
                print(f"  ❌ Data aggregation: FAIL (API not accessible)")
                return False
                
            data = response.json()
            
            # Check required data structure
            required_keys = ['ccdk', 'superclaude', 'thinkchain', 'templates', 'total_capabilities']
            missing_keys = [key for key in required_keys if key not in data]
            
            if missing_keys:
                self.log_test('unified_dashboard', 'data_aggregation', 'FAIL', f"Missing keys: {missing_keys}")
                print(f"  ❌ Data aggregation: FAIL (Missing keys: {missing_keys})")
                return False
            
            # Validate total capabilities calculation
            expected_total = (
                data['ccdk'].get('commands', 0) + 
                data['superclaude'].get('commands', 0) + 
                data['thinkchain'].get('tools', 0)
            )
            
            if data['total_capabilities'] != expected_total:
                self.log_test('unified_dashboard', 'data_aggregation', 'FAIL', 
                             f"Total capabilities mismatch: {data['total_capabilities']} != {expected_total}")
                print(f"  ❌ Data aggregation: FAIL (Total mismatch: {data['total_capabilities']} != {expected_total})")
                return False
            
            self.log_test('unified_dashboard', 'data_aggregation', 'PASS', 
                         f"All systems integrated, total capabilities: {data['total_capabilities']}")
            print(f"  ✅ Data aggregation: PASS (Total capabilities: {data['total_capabilities']})")
            
            # Test individual system stats
            systems_tested = 0
            for system in ['ccdk', 'superclaude', 'thinkchain', 'templates']:
                if system in data and isinstance(data[system], dict):
                    systems_tested += 1
                    print(f"    ✅ {system.title()}: {data[system]}")
            
            print(f"  📊 Systems integrated: {systems_tested}/4")
            return True
            
        except Exception as e:
            self.log_test('unified_dashboard', 'data_aggregation', 'FAIL', str(e))
            print(f"  ❌ Data aggregation: FAIL ({str(e)})")
            return False
    
    def test_webui_commands(self):
        """Test Enhanced WebUI command browsing functionality"""
        print(f"\n🖥️ Testing Enhanced WebUI command browsing...")
        
        try:
            # Test commands API
            response = requests.get('http://localhost:7000/api/commands', timeout=10)
            if response.status_code != 200:
                self.log_test('enhanced_webui', 'command_browsing', 'FAIL', f"Commands API not accessible: {response.status_code}")
                print(f"  ❌ Command browsing: FAIL (API not accessible)")
                return False
                
            commands = response.json()
            
            # Check command structure
            expected_systems = ['ccdk', 'superclaude', 'thinkchain']
            missing_systems = [sys for sys in expected_systems if sys not in commands]
            
            if missing_systems:
                self.log_test('enhanced_webui', 'command_browsing', 'FAIL', f"Missing systems: {missing_systems}")
                print(f"  ❌ Command browsing: FAIL (Missing systems: {missing_systems})")
                return False
            
            # Count total commands
            total_commands = sum(len(commands[sys]) for sys in expected_systems)
            
            # Test stats API
            stats_response = requests.get('http://localhost:7000/api/stats', timeout=10)
            if stats_response.status_code == 200:
                stats = stats_response.json()
                expected_total = stats.get('total_capabilities', 0)
                
                if total_commands != expected_total:
                    self.log_test('enhanced_webui', 'command_browsing', 'FAIL', 
                                 f"Command count mismatch: {total_commands} != {expected_total}")
                    print(f"  ❌ Command browsing: FAIL (Count mismatch: {total_commands} != {expected_total})")
                    return False
            
            self.log_test('enhanced_webui', 'command_browsing', 'PASS', 
                         f"All command systems accessible, total commands: {total_commands}")
            print(f"  ✅ Command browsing: PASS (Total commands: {total_commands})")
            
            # Test individual systems
            for system in expected_systems:
                count = len(commands[system])
                print(f"    ✅ {system.title()}: {count} commands/tools")
            
            return True
            
        except Exception as e:
            self.log_test('enhanced_webui', 'command_browsing', 'FAIL', str(e))
            print(f"  ❌ Command browsing: FAIL ({str(e)})")
            return False
    
    def test_analytics_monitoring(self):
        """Test Enhanced Analytics monitoring functionality"""
        print(f"\n📈 Testing Enhanced Analytics monitoring...")
        
        try:
            # Test main analytics API
            response = requests.get('http://localhost:5005/api/status', timeout=10)
            if response.status_code != 200:
                self.log_test('enhanced_analytics', 'monitoring', 'FAIL', f"Analytics API not accessible: {response.status_code}")
                print(f"  ❌ Monitoring: FAIL (API not accessible)")
                return False
                
            data = response.json()
            
            # Check analytics data structure
            required_sections = ['hive', 'system', 'usage']
            missing_sections = [sec for sec in required_sections if sec not in data]
            
            if missing_sections:
                self.log_test('enhanced_analytics', 'monitoring', 'FAIL', f"Missing sections: {missing_sections}")
                print(f"  ❌ Monitoring: FAIL (Missing sections: {missing_sections})")
                return False
            
            # Test health monitoring
            health_response = requests.get('http://localhost:5005/api/health', timeout=10)
            if health_response.status_code == 200:
                health_data = health_response.json()
                healthy_services = sum(1 for service in health_data.values() if service.get('status') == 'healthy')
                total_services = len(health_data)
                
                print(f"    📊 Service Health: {healthy_services}/{total_services} services healthy")
                
                # Check if our main services are healthy
                main_services = ['unified_dashboard', 'webui', 'analytics']
                for service in main_services:
                    if service in health_data:
                        status = health_data[service].get('status', 'unknown')
                        print(f"      {service}: {status}")
            
            # Test metrics API
            metrics_response = requests.get('http://localhost:5005/api/metrics', timeout=10)
            if metrics_response.status_code == 200:
                metrics = metrics_response.json()
                total_capabilities = metrics.get('total_capabilities', 0)
                print(f"    📊 Total Capabilities Monitored: {total_capabilities}")
            
            self.log_test('enhanced_analytics', 'monitoring', 'PASS', 
                         f"Analytics monitoring operational with {len(required_sections)} sections")
            print(f"  ✅ Monitoring: PASS (All analytics sections operational)")
            return True
            
        except Exception as e:
            self.log_test('enhanced_analytics', 'monitoring', 'FAIL', str(e))
            print(f"  ❌ Monitoring: FAIL ({str(e)})")
            return False
    
    def test_database_operations(self):
        """Test SQLite database operations for hive sessions"""
        print(f"\n🗄️ Testing database operations...")
        
        try:
            # Check if hive database exists
            hive_db_path = self.app_dir / '.ccd_hive/test-session/memory.db'
            
            if not hive_db_path.exists():
                self.log_test('database', 'hive_operations', 'PASS', "No hive database found - this is acceptable for a fresh system")
                print(f"  ✅ Database operations: PASS (No hive database - fresh system)")
                return True
            
            # Test database connectivity
            conn = sqlite3.connect(str(hive_db_path))
            cursor = conn.cursor()
            
            # Test basic query
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if not tables:
                self.log_test('database', 'hive_operations', 'FAIL', "Database exists but no tables found")
                print(f"  ❌ Database operations: FAIL (No tables found)")
                conn.close()
                return False
            
            # Test notes table if it exists
            table_names = [table[0] for table in tables]
            if 'notes' in table_names:
                cursor.execute("SELECT COUNT(*) FROM notes")
                note_count = cursor.fetchone()[0]
                print(f"    📊 Notes in database: {note_count}")
                
                # Test a simple insert/delete to verify write operations
                test_note = f"Test note - {datetime.now().isoformat()}"
                cursor.execute("INSERT INTO notes (content) VALUES (?)", (test_note,))
                cursor.execute("DELETE FROM notes WHERE content = ?", (test_note,))
                conn.commit()
                
                self.log_test('database', 'hive_operations', 'PASS', 
                             f"Database operational with {note_count} notes, CRUD operations working")
                print(f"  ✅ Database operations: PASS (CRUD operations verified)")
            else:
                self.log_test('database', 'hive_operations', 'PASS', 
                             f"Database exists with tables: {table_names}")
                print(f"  ✅ Database operations: PASS (Tables: {table_names})")
            
            conn.close()
            return True
            
        except Exception as e:
            self.log_test('database', 'hive_operations', 'FAIL', str(e))
            print(f"  ❌ Database operations: FAIL ({str(e)})")
            return False
    
    def test_system_integration(self):
        """Test integration between all systems"""
        print(f"\n🔗 Testing system integration...")
        
        try:
            # Get data from all services
            dashboard_data = requests.get('http://localhost:4000/api/status', timeout=10).json()
            webui_data = requests.get('http://localhost:7000/api/stats', timeout=10).json()
            analytics_data = requests.get('http://localhost:5005/api/metrics', timeout=10).json()
            
            # Compare total capabilities across services
            dashboard_total = dashboard_data.get('total_capabilities', 0)
            webui_total = webui_data.get('total_capabilities', 0)
            analytics_total = analytics_data.get('total_capabilities', 0)
            
            if dashboard_total == webui_total == analytics_total:
                self.log_test('integration', 'data_consistency', 'PASS', 
                             f"All services report consistent total capabilities: {dashboard_total}")
                print(f"  ✅ Data consistency: PASS (All services report {dashboard_total} capabilities)")
            else:
                self.log_test('integration', 'data_consistency', 'FAIL', 
                             f"Inconsistent totals: Dashboard={dashboard_total}, WebUI={webui_total}, Analytics={analytics_total}")
                print(f"  ❌ Data consistency: FAIL (Inconsistent totals)")
                return False
            
            # Test cross-service navigation links
            navigation_tests = [
                ('http://localhost:4000', 'Unified Dashboard'),
                ('http://localhost:7000', 'Enhanced WebUI'),
                ('http://localhost:5005', 'Enhanced Analytics')
            ]
            
            accessible_services = 0
            for url, name in navigation_tests:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        accessible_services += 1
                        print(f"    ✅ {name}: Accessible")
                    else:
                        print(f"    ❌ {name}: Not accessible (Status: {response.status_code})")
                except:
                    print(f"    ❌ {name}: Connection failed")
            
            if accessible_services == len(navigation_tests):
                self.log_test('integration', 'cross_service_navigation', 'PASS', 
                             f"All {accessible_services} services accessible for navigation")
                print(f"  ✅ Cross-service navigation: PASS ({accessible_services}/{len(navigation_tests)} services)")
                return True
            else:
                self.log_test('integration', 'cross_service_navigation', 'FAIL', 
                             f"Only {accessible_services}/{len(navigation_tests)} services accessible")
                print(f"  ❌ Cross-service navigation: FAIL ({accessible_services}/{len(navigation_tests)} services)")
                return False
            
        except Exception as e:
            self.log_test('integration', 'system_integration', 'FAIL', str(e))
            print(f"  ❌ System integration: FAIL ({str(e)})")
            return False
    
    def run_comprehensive_tests(self):
        """Run all backend tests"""
        print("🚀 Starting CCDK i124q Backend Testing Suite")
        print("=" * 60)
        
        start_time = time.time()
        total_tests = 0
        passed_tests = 0
        
        # Test each service
        for service_key in self.services.keys():
            print(f"\n{'='*20} {self.services[service_key]['name']} {'='*20}")
            
            # Health check
            if self.test_service_health(service_key):
                passed_tests += 1
            total_tests += 1
            
            # API endpoints
            if self.test_api_endpoints(service_key):
                passed_tests += 1
            total_tests += 1
        
        # Specific functionality tests
        print(f"\n{'='*20} Functionality Tests {'='*20}")
        
        # Unified Dashboard data aggregation
        if self.test_unified_dashboard_data():
            passed_tests += 1
        total_tests += 1
        
        # WebUI command browsing
        if self.test_webui_commands():
            passed_tests += 1
        total_tests += 1
        
        # Analytics monitoring
        if self.test_analytics_monitoring():
            passed_tests += 1
        total_tests += 1
        
        # Database operations
        if self.test_database_operations():
            passed_tests += 1
        total_tests += 1
        
        # System integration
        if self.test_system_integration():
            passed_tests += 1
        total_tests += 1
        
        # Final results
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n{'='*60}")
        print(f"🏁 CCDK i124q Backend Testing Complete")
        print(f"📊 Results: {passed_tests}/{total_tests} tests passed ({(passed_tests/total_tests)*100:.1f}%)")
        print(f"⏱️ Duration: {duration:.2f} seconds")
        
        if passed_tests == total_tests:
            print(f"✅ ALL TESTS PASSED - System is fully operational!")
        else:
            print(f"❌ {total_tests - passed_tests} tests failed - See details above")
        
        return passed_tests == total_tests
    
    def generate_test_report(self):
        """Generate detailed test report"""
        print(f"\n{'='*60}")
        print("📋 DETAILED TEST REPORT")
        print(f"{'='*60}")
        
        for service, tests in self.test_results.items():
            print(f"\n🔧 {service.upper().replace('_', ' ')}")
            print("-" * 40)
            for test_name, result in tests.items():
                status_icon = "✅" if result['status'] == 'PASS' else "❌"
                print(f"  {status_icon} {test_name}: {result['status']}")
                if result['details']:
                    print(f"     Details: {result['details']}")
        
        return self.test_results

if __name__ == '__main__':
    tester = CCDKBackendTester()
    
    # Run comprehensive tests
    success = tester.run_comprehensive_tests()
    
    # Generate detailed report
    report = tester.generate_test_report()
    
    # Save results to file
    with open('/app/backend_test_results.json', 'w') as f:
        json.dump({
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'results': report
        }, f, indent=2)
    
    print(f"\n📄 Test results saved to: /app/backend_test_results.json")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)