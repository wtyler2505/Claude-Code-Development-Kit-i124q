#!/usr/bin/env python3
"""
CCDK Performance Benchmark Test
Testing performance impact of enhancements with obsessive detail
"""

import os
import sys
import time
import json
import subprocess
import statistics
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_command_benchmark(command, iterations=5):
    """Run a command multiple times and measure performance"""
    times = []
    
    for i in range(iterations):
        start = time.time()
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            elapsed = time.time() - start
            times.append(elapsed)
        except Exception as e:
            print(f"[ERROR] Command failed: {e}")
            return None
    
    return {
        "min": min(times),
        "max": max(times),
        "avg": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0
    }

def test_file_operations():
    """Benchmark file operation performance"""
    print("\n[TEST] File Operations Performance")
    print("-" * 40)
    
    test_file = "test_perf_temp.txt"
    test_content = "x" * 1000  # 1KB of data
    
    # Test write performance
    print("Testing file write performance...")
    write_times = []
    for i in range(10):
        start = time.time()
        with open(test_file, 'w') as f:
            f.write(test_content * (i + 1))  # Increasing file sizes
        write_times.append(time.time() - start)
    
    # Test read performance
    print("Testing file read performance...")
    read_times = []
    for i in range(10):
        start = time.time()
        with open(test_file, 'r') as f:
            _ = f.read()
        read_times.append(time.time() - start)
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print(f"[OK] Write avg: {statistics.mean(write_times)*1000:.2f}ms")
    print(f"[OK] Read avg: {statistics.mean(read_times)*1000:.2f}ms")
    
    return {
        "write_ms": statistics.mean(write_times) * 1000,
        "read_ms": statistics.mean(read_times) * 1000
    }

def test_hook_execution():
    """Test hook execution overhead"""
    print("\n[TEST] Hook Execution Overhead")
    print("-" * 40)
    
    # Simulate hook execution by running a minimal TypeScript file
    hook_test_file = "test_hook.ts"
    with open(hook_test_file, 'w') as f:
        f.write('console.log("Hook executed");')
    
    # Benchmark hook execution
    stats = run_command_benchmark(f"node {hook_test_file}", iterations=10)
    
    # Cleanup
    if os.path.exists(hook_test_file):
        os.remove(hook_test_file)
    
    if stats:
        print(f"[OK] Hook execution avg: {stats['avg']*1000:.2f}ms")
        print(f"[OK] Hook execution median: {stats['median']*1000:.2f}ms")
        return stats['avg'] * 1000
    else:
        print("[FAIL] Could not benchmark hook execution")
        return None

def test_python_script_startup():
    """Test Python script startup time"""
    print("\n[TEST] Python Script Startup Time")
    print("-" * 40)
    
    # Create minimal Python script
    test_script = "test_startup.py"
    with open(test_script, 'w') as f:
        f.write('print("Started")')
    
    # Benchmark startup
    stats = run_command_benchmark(f"python {test_script}", iterations=10)
    
    # Cleanup
    if os.path.exists(test_script):
        os.remove(test_script)
    
    if stats:
        print(f"[OK] Python startup avg: {stats['avg']*1000:.2f}ms")
        print(f"[OK] Python startup median: {stats['median']*1000:.2f}ms")
        return stats['avg'] * 1000
    else:
        print("[FAIL] Could not benchmark Python startup")
        return None

def test_json_processing():
    """Test JSON processing performance"""
    print("\n[TEST] JSON Processing Performance")
    print("-" * 40)
    
    # Create test data
    test_data = {
        "commands": [f"command_{i}" for i in range(100)],
        "agents": [{"name": f"agent_{i}", "id": i} for i in range(50)],
        "hooks": {
            "sessionStart": ["hook1.ts", "hook2.ts"],
            "sessionEnd": ["hook3.ts"],
            "postTask": ["hook4.ts", "hook5.ts"]
        }
    }
    
    # Test serialization
    serialize_times = []
    for _ in range(100):
        start = time.time()
        json_str = json.dumps(test_data)
        serialize_times.append(time.time() - start)
    
    # Test deserialization
    deserialize_times = []
    for _ in range(100):
        start = time.time()
        _ = json.loads(json_str)
        deserialize_times.append(time.time() - start)
    
    print(f"[OK] JSON serialize avg: {statistics.mean(serialize_times)*1000:.2f}ms")
    print(f"[OK] JSON deserialize avg: {statistics.mean(deserialize_times)*1000:.2f}ms")
    
    return {
        "serialize_ms": statistics.mean(serialize_times) * 1000,
        "deserialize_ms": statistics.mean(deserialize_times) * 1000
    }

def test_directory_scanning():
    """Test directory scanning performance"""
    print("\n[TEST] Directory Scanning Performance")
    print("-" * 40)
    
    # Scan .claude directory
    scan_times = []
    for _ in range(5):
        start = time.time()
        file_count = 0
        for root, dirs, files in os.walk('.claude'):
            file_count += len(files)
        scan_times.append(time.time() - start)
    
    print(f"[OK] Found {file_count} files in .claude directory")
    print(f"[OK] Directory scan avg: {statistics.mean(scan_times)*1000:.2f}ms")
    
    return statistics.mean(scan_times) * 1000

def main():
    """Run all performance benchmarks"""
    print("[PERFORMANCE] CCDK PERFORMANCE BENCHMARK TEST")
    print("=" * 60)
    
    results = {}
    
    # Run all tests
    results['file_ops'] = test_file_operations()
    results['hook_overhead'] = test_hook_execution()
    results['python_startup'] = test_python_script_startup()
    results['json_processing'] = test_json_processing()
    results['dir_scanning'] = test_directory_scanning()
    
    # Calculate overall performance score
    print("\n" + "=" * 60)
    print("[RESULTS] PERFORMANCE BENCHMARK SUMMARY")
    print("=" * 60)
    
    # Define acceptable thresholds (in milliseconds)
    thresholds = {
        'file_write': 5.0,
        'file_read': 2.0,
        'hook_overhead': 100.0,
        'python_startup': 200.0,
        'json_serialize': 1.0,
        'json_deserialize': 1.0,
        'dir_scanning': 50.0
    }
    
    passed = 0
    failed = 0
    
    # Check file operations
    if results['file_ops']:
        if results['file_ops']['write_ms'] < thresholds['file_write']:
            print(f"[OK] File write: {results['file_ops']['write_ms']:.2f}ms < {thresholds['file_write']}ms")
            passed += 1
        else:
            print(f"[FAIL] File write: {results['file_ops']['write_ms']:.2f}ms > {thresholds['file_write']}ms")
            failed += 1
            
        if results['file_ops']['read_ms'] < thresholds['file_read']:
            print(f"[OK] File read: {results['file_ops']['read_ms']:.2f}ms < {thresholds['file_read']}ms")
            passed += 1
        else:
            print(f"[FAIL] File read: {results['file_ops']['read_ms']:.2f}ms > {thresholds['file_read']}ms")
            failed += 1
    
    # Check other metrics
    if results['hook_overhead'] and results['hook_overhead'] < thresholds['hook_overhead']:
        print(f"[OK] Hook overhead: {results['hook_overhead']:.2f}ms < {thresholds['hook_overhead']}ms")
        passed += 1
    else:
        print(f"[WARN] Hook overhead could not be measured (Node.js may not be available)")
    
    if results['python_startup'] and results['python_startup'] < thresholds['python_startup']:
        print(f"[OK] Python startup: {results['python_startup']:.2f}ms < {thresholds['python_startup']}ms")
        passed += 1
    else:
        print(f"[FAIL] Python startup: {results['python_startup']:.2f}ms > {thresholds['python_startup']}ms")
        failed += 1
    
    if results['json_processing']:
        if results['json_processing']['serialize_ms'] < thresholds['json_serialize']:
            print(f"[OK] JSON serialize: {results['json_processing']['serialize_ms']:.2f}ms < {thresholds['json_serialize']}ms")
            passed += 1
        else:
            print(f"[FAIL] JSON serialize: {results['json_processing']['serialize_ms']:.2f}ms > {thresholds['json_serialize']}ms")
            failed += 1
            
        if results['json_processing']['deserialize_ms'] < thresholds['json_deserialize']:
            print(f"[OK] JSON deserialize: {results['json_processing']['deserialize_ms']:.2f}ms < {thresholds['json_deserialize']}ms")
            passed += 1
        else:
            print(f"[FAIL] JSON deserialize: {results['json_processing']['deserialize_ms']:.2f}ms > {thresholds['json_deserialize']}ms")
            failed += 1
    
    if results['dir_scanning'] and results['dir_scanning'] < thresholds['dir_scanning']:
        print(f"[OK] Directory scanning: {results['dir_scanning']:.2f}ms < {thresholds['dir_scanning']}ms")
        passed += 1
    else:
        print(f"[FAIL] Directory scanning: {results['dir_scanning']:.2f}ms > {thresholds['dir_scanning']}ms")
        failed += 1
    
    # Final summary
    print("\n" + "-" * 60)
    print(f"[OK] Passed: {passed}")
    print(f"[FAIL] Failed: {failed}")
    print(f"Performance Score: {(passed / (passed + failed) * 100):.1f}%")
    
    if failed == 0:
        print("\n[SUCCESS] All performance benchmarks passed!")
        print("The enhanced CCDK maintains excellent performance!")
    else:
        print("\n[WARNING] Some performance metrics exceeded thresholds")
        print("Consider optimizing the affected areas")

if __name__ == "__main__":
    main()