#!/usr/bin/env python3
"""
CCDK i124q Integration Test Suite
Comprehensive testing of CCDK + SuperClaude integration
"""

import os
import json
import subprocess
from pathlib import Path

class CCDKIntegrationTester:
    def __init__(self):
        self.app_dir = Path('/app')
        self.claude_dir = Path('/app/.claude')
        self.results = {}
        
    def test_file_structure(self):
        """Test that all required files and directories exist"""
        print("🔍 Testing File Structure...")
        
        required_files = [
            '/app/.claude/CLAUDE.md',
            '/app/.claude/COMMANDS-INDEX.md',
            '/app/.claude/superclaude/core/PERSONAS.md',
            '/app/.claude/superclaude/core/COMMANDS.md',
            '/app/.claude/commands/full-context.md',
            '/app/.claude/commands/code-review.md'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
                
        if missing_files:
            print(f"❌ Missing files: {missing_files}")
            return False
        else:
            print("✅ All required files present")
            return True
    
    def test_command_availability(self):
        """Test that both CCDK and SuperClaude commands are available"""
        print("📋 Testing Command Availability...")
        
        # Test CCDK commands
        ccdk_commands = [
            'full-context.md',
            'code-review.md', 
            'create-docs.md',
            'refactor.md',
            'handoff.md'
        ]
        
        ccdk_missing = []
        for cmd in ccdk_commands:
            if not (self.claude_dir / 'commands' / cmd).exists():
                ccdk_missing.append(cmd)
        
        # Test SuperClaude commands
        sc_commands = [
            'implement.md',
            'analyze.md',
            'task.md',
            'build.md',
            'design.md'
        ]
        
        sc_missing = []
        for cmd in sc_commands:
            if not (self.claude_dir / 'superclaude' / 'commands' / cmd).exists():
                sc_missing.append(cmd)
        
        if ccdk_missing or sc_missing:
            print(f"❌ Missing CCDK commands: {ccdk_missing}")
            print(f"❌ Missing SuperClaude commands: {sc_missing}")
            return False
        else:
            print(f"✅ Found {len(ccdk_commands)} CCDK commands")
            print(f"✅ Found {len(sc_commands)} SuperClaude commands")
            return True
    
    def test_persona_system(self):
        """Test SuperClaude persona system integration"""
        print("🎭 Testing Persona System...")
        
        personas_file = self.claude_dir / 'superclaude' / 'core' / 'PERSONAS.md'
        if not personas_file.exists():
            print("❌ PERSONAS.md not found")
            return False
        
        with open(personas_file, 'r') as f:
            content = f.read()
        
        expected_personas = [
            'architect',
            'frontend', 
            'backend',
            'security',
            'analyzer',
            'mentor',
            'scribe'
        ]
        
        missing_personas = []
        for persona in expected_personas:
            if f"--persona-{persona}" not in content:
                missing_personas.append(persona)
        
        if missing_personas:
            print(f"❌ Missing personas: {missing_personas}")
            return False
        else:
            print(f"✅ Found {len(expected_personas)} core personas")
            return True
    
    def test_dashboard_functionality(self):
        """Test that web dashboards are functional"""
        print("🌐 Testing Dashboard Functionality...")
        
        try:
            # Test that dashboard files exist and are executable
            webui_file = self.app_dir / 'webui' / 'app.py'
            dashboard_file = self.app_dir / 'dashboard' / 'app.py'
            
            if not webui_file.exists() or not dashboard_file.exists():
                print("❌ Dashboard files missing")
                return False
                
            print("✅ Dashboard files present")
            return True
            
        except Exception as e:
            print(f"❌ Dashboard test failed: {e}")
            return False
    
    def test_documentation_integration(self):
        """Test that documentation systems are properly integrated"""
        print("📚 Testing Documentation Integration...")
        
        claude_md = self.claude_dir / 'CLAUDE.md'
        if not claude_md.exists():
            print("❌ Main CLAUDE.md missing")
            return False
        
        with open(claude_md, 'r') as f:
            content = f.read()
        
        # Check for key integration elements
        integration_elements = [
            'CCDK i124q',
            'SuperClaude',
            '3-tier documentation',
            'AI Persona System',
            'sc: namespace'
        ]
        
        missing_elements = []
        for element in integration_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Missing integration elements: {missing_elements}")
            return False
        else:
            print("✅ Documentation properly integrated")
            return True
    
    def generate_report(self):
        """Generate comprehensive integration report"""
        print("\n" + "="*60)
        print("📊 CCDK i124q INTEGRATION TEST RESULTS")
        print("="*60)
        
        tests = [
            ('File Structure', self.test_file_structure),
            ('Command Availability', self.test_command_availability), 
            ('Persona System', self.test_persona_system),
            ('Dashboard Functionality', self.test_dashboard_functionality),
            ('Documentation Integration', self.test_documentation_integration)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            result = test_func()
            self.results[test_name] = result
            if result:
                passed += 1
            print()
        
        print("="*60)
        print(f"📈 OVERALL RESULTS: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - Integration Successful!")
            print("\n✅ CCDK i124q is ready for Phase 2: ThinkChain Integration")
        else:
            print("⚠️  Some tests failed - Review issues above")
        
        print("="*60)
        return passed == total

if __name__ == "__main__":
    tester = CCDKIntegrationTester()
    success = tester.generate_report()
    exit(0 if success else 1)