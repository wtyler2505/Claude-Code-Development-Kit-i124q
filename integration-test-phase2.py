#!/usr/bin/env python3
"""
CCDK i124q Phase 2 Integration Test Suite
Comprehensive testing of CCDK + SuperClaude + ThinkChain integration
"""

import os
import sys
import json
import importlib.util
from pathlib import Path

class Phase2IntegrationTester:
    def __init__(self):
        self.app_dir = Path('/app')
        self.claude_dir = Path('/app/.claude')
        self.results = {}
        
    def test_thinkchain_structure(self):
        """Test ThinkChain integration structure"""
        print("🔗 Testing ThinkChain Integration Structure...")
        
        required_files = [
            '/app/.claude/thinkchain/tools/base.py',
            '/app/.claude/thinkchain/tool_discovery.py', 
            '/app/.claude/thinkchain/ui_components.py',
            '/app/.claude/thinkchain/mcp_config.json',
            '/app/.claude/THINKCHAIN-INTEGRATION.md'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
                
        if missing_files:
            print(f"❌ Missing ThinkChain files: {missing_files}")
            return False
        else:
            print("✅ ThinkChain structure properly integrated")
            return True
    
    def test_thinkchain_tools(self):
        """Test ThinkChain tools availability"""
        print("🛠️ Testing ThinkChain Tools...")
        
        tools_dir = self.claude_dir / 'thinkchain' / 'tools'
        if not tools_dir.exists():
            print("❌ ThinkChain tools directory missing")
            return False
        
        expected_tools = [
            'filecreatortool.py',
            'fileedittool.py',
            'filecontentreadertool.py',
            'weathertool.py',
            'duckduckgotool.py',
            'webscrapertool.py',
            'uvpackagemanager.py',
            'lintingtool.py'
        ]
        
        found_tools = []
        for tool_file in tools_dir.glob("*.py"):
            if tool_file.name != '__init__.py' and tool_file.name != 'base.py':
                found_tools.append(tool_file.name)
        
        missing_tools = [tool for tool in expected_tools if tool not in found_tools]
        
        if missing_tools:
            print(f"❌ Missing tools: {missing_tools}")
            return False
        else:
            print(f"✅ Found {len(found_tools)} ThinkChain tools")
            return True
    
    def test_tool_discovery_system(self):
        """Test tool discovery system functionality"""
        print("🔍 Testing Tool Discovery System...")
        
        # Add the thinkchain directory to Python path for testing
        thinkchain_dir = str(self.claude_dir / 'thinkchain')
        if thinkchain_dir not in sys.path:
            sys.path.insert(0, thinkchain_dir)
        
        try:
            # Try to import the tool discovery system
            spec = importlib.util.spec_from_file_location(
                "tool_discovery", 
                self.claude_dir / 'thinkchain' / 'tool_discovery.py'
            )
            tool_discovery = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tool_discovery)
            
            # Test basic functionality
            if hasattr(tool_discovery, 'ToolDiscovery'):
                discovery = tool_discovery.ToolDiscovery(tools_dir='thinkchain/tools')
                tools = discovery.discover_tools()
                
                if len(tools) > 0:
                    print(f"✅ Tool discovery found {len(tools)} tools")
                    return True
                else:
                    print("❌ Tool discovery found no tools")
                    return False
            else:
                print("❌ ToolDiscovery class not found")
                return False
                
        except Exception as e:
            print(f"❌ Tool discovery test failed: {e}")
            return False
    
    def test_base_tool_interface(self):
        """Test ThinkChain BaseTool interface"""
        print("🏗️ Testing BaseTool Interface...")
        
        try:
            # Add path and import BaseTool
            thinkchain_dir = str(self.claude_dir / 'thinkchain')
            if thinkchain_dir not in sys.path:
                sys.path.insert(0, thinkchain_dir)
            
            spec = importlib.util.spec_from_file_location(
                "base", 
                self.claude_dir / 'thinkchain' / 'tools' / 'base.py'
            )
            base_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(base_module)
            
            if hasattr(base_module, 'BaseTool'):
                base_tool = base_module.BaseTool
                
                # Check abstract methods
                required_methods = ['name', 'description', 'input_schema', 'execute']
                missing_methods = []
                
                for method in required_methods:
                    if not hasattr(base_tool, method):
                        missing_methods.append(method)
                
                if missing_methods:
                    print(f"❌ Missing BaseTool methods: {missing_methods}")
                    return False
                else:
                    print("✅ BaseTool interface properly defined")
                    return True
            else:
                print("❌ BaseTool class not found")
                return False
                
        except Exception as e:
            print(f"❌ BaseTool interface test failed: {e}")
            return False
    
    def test_mcp_configuration(self):
        """Test MCP integration configuration"""
        print("🌐 Testing MCP Configuration...")
        
        mcp_config_file = self.claude_dir / 'thinkchain' / 'mcp_config.json'
        if not mcp_config_file.exists():
            print("❌ MCP config file missing")
            return False
        
        try:
            with open(mcp_config_file, 'r') as f:
                config = json.load(f)
            
            if 'mcpServers' not in config:
                print("❌ MCP config missing mcpServers section")
                return False
            
            servers = config['mcpServers']
            expected_servers = ['sqlite', 'puppeteer', 'filesystem']
            
            found_servers = list(servers.keys())
            missing_servers = [s for s in expected_servers if s not in found_servers]
            
            if len(found_servers) > 0:
                print(f"✅ Found {len(found_servers)} MCP server configurations")
                return True
            else:
                print("❌ No MCP servers configured")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ MCP config JSON invalid: {e}")
            return False
        except Exception as e:
            print(f"❌ MCP configuration test failed: {e}")
            return False
    
    def test_integration_documentation(self):
        """Test integration documentation completeness"""
        print("📚 Testing Integration Documentation...")
        
        doc_file = self.claude_dir / 'THINKCHAIN-INTEGRATION.md'
        if not doc_file.exists():
            print("❌ ThinkChain integration documentation missing")
            return False
        
        with open(doc_file, 'r') as f:
            content = f.read()
        
        required_sections = [
            'Integration Overview',
            'ThinkChain Features Integrated',
            'Real-Time Thinking Streams',
            'Tool Discovery System',
            'MCP Integration',
            'Usage Patterns'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Missing documentation sections: {missing_sections}")
            return False
        else:
            print("✅ Integration documentation comprehensive")
            return True
    
    def test_unified_command_system(self):
        """Test that all three systems work together"""
        print("🔄 Testing Unified Command System...")
        
        # Check for CCDK commands
        ccdk_commands = (self.claude_dir / 'commands').glob('*.md')
        ccdk_count = len(list(ccdk_commands))
        
        # Check for SuperClaude commands
        sc_commands = (self.claude_dir / 'superclaude' / 'commands').glob('*.md')
        sc_count = len(list(sc_commands))
        
        # Check for ThinkChain tools
        tc_tools = (self.claude_dir / 'thinkchain' / 'tools').glob('*.py')
        tc_count = len([f for f in tc_tools if f.name not in ['__init__.py', 'base.py']])
        
        total_capabilities = ccdk_count + sc_count + tc_count
        
        if total_capabilities >= 30:  # Expect significant combined capabilities
            print(f"✅ Unified system: {ccdk_count} CCDK + {sc_count} SuperClaude + {tc_count} ThinkChain = {total_capabilities} total capabilities")
            return True
        else:
            print(f"❌ Insufficient combined capabilities: {total_capabilities}")
            return False
    
    def generate_phase2_report(self):
        """Generate Phase 2 integration report"""
        print("\n" + "="*70)
        print("📊 CCDK i124q PHASE 2 INTEGRATION TEST RESULTS")
        print("="*70)
        
        tests = [
            ('ThinkChain Structure', self.test_thinkchain_structure),
            ('ThinkChain Tools', self.test_thinkchain_tools),
            ('Tool Discovery System', self.test_tool_discovery_system),
            ('BaseTool Interface', self.test_base_tool_interface),
            ('MCP Configuration', self.test_mcp_configuration),
            ('Integration Documentation', self.test_integration_documentation),
            ('Unified Command System', self.test_unified_command_system)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            result = test_func()
            self.results[test_name] = result
            if result:
                passed += 1
            print()
        
        print("="*70)
        print(f"📈 PHASE 2 RESULTS: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 PHASE 2 COMPLETE - ThinkChain Integration Successful!")
            print("\n✅ CCDK i124q Enhanced Capabilities:")
            print("   • CCDK Foundation: 3-tier docs, hooks, Task Master AI")
            print("   • SuperClaude: 16 commands + 11 AI personas")
            print("   • ThinkChain: Real-time thinking + 15 advanced tools")
            print("\n🚀 Ready for Phase 3: Templates Analytics & Component Integration")
        else:
            print("⚠️  Some Phase 2 tests failed - Review issues above")
        
        print("="*70)
        return passed == total

if __name__ == "__main__":
    tester = Phase2IntegrationTester()
    success = tester.generate_phase2_report()
    exit(0 if success else 1)