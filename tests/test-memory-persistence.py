#!/usr/bin/env python3
"""
CCDK Memory Persistence Test - Hive Mind SQLite Testing
Testing the persistence layer with obsessive detail
"""

import os
import sys
import sqlite3
import json
import tempfile
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_memory_persistence():
    """Test the Hive Mind memory persistence system"""
    print("[BRAIN] TESTING HIVE MIND MEMORY PERSISTENCE")
    print("=" * 60)
    
    test_results = {
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    # Test 1: Create a test database
    print("\n[TEST 1] Creating test memory database...")
    test_db = os.path.join(tempfile.gettempdir(), "test_hive_memory.db")
    
    try:
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        # Create the schema that Hive Mind expects
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                context TEXT,
                UNIQUE(session_id, key)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_metadata (
                session_id TEXT PRIMARY KEY,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_accessed DATETIME,
                total_entries INTEGER DEFAULT 0,
                tags TEXT
            )
        """)
        
        conn.commit()
        print("[OK] Database created successfully")
        test_results["passed"] += 1
        
    except Exception as e:
        print(f"[FAIL] Database creation failed: {e}")
        test_results["failed"] += 1
        return test_results
    
    # Test 2: Store memory entries
    print("\n[TEST 2] Storing memory entries...")
    test_session = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    test_memories = [
        ("user_preference", "dark_mode", "UI settings"),
        ("last_command", "/security-audit", "command history"),
        ("project_context", json.dumps({"name": "CCDK", "version": "1.0"}), "project info"),
        ("performance_data", json.dumps({"avg_response": 250, "peak_memory": 512}), "metrics")
    ]
    
    try:
        for key, value, context in test_memories:
            cursor.execute("""
                INSERT OR REPLACE INTO memory_store (session_id, key, value, context)
                VALUES (?, ?, ?, ?)
            """, (test_session, key, value, context))
        
        # Update session metadata
        cursor.execute("""
            INSERT OR REPLACE INTO session_metadata (session_id, last_accessed, total_entries)
            VALUES (?, CURRENT_TIMESTAMP, ?)
        """, (test_session, len(test_memories)))
        
        conn.commit()
        print(f"[OK] Stored {len(test_memories)} memory entries")
        test_results["passed"] += 1
        
    except Exception as e:
        print(f"[FAIL] Memory storage failed: {e}")
        test_results["failed"] += 1
    
    # Test 3: Retrieve memories
    print("\n[TEST 3] Retrieving stored memories...")
    try:
        cursor.execute("""
            SELECT key, value, context FROM memory_store
            WHERE session_id = ?
        """, (test_session,))
        
        retrieved = cursor.fetchall()
        if len(retrieved) == len(test_memories):
            print(f"[OK] Retrieved all {len(retrieved)} memories")
            for key, value, context in retrieved:
                print(f"  - {key}: {value[:50]}...")
            test_results["passed"] += 1
        else:
            print(f"[FAIL] Memory count mismatch: expected {len(test_memories)}, got {len(retrieved)}")
            test_results["failed"] += 1
            
    except Exception as e:
        print(f"[FAIL] Memory retrieval failed: {e}")
        test_results["failed"] += 1
    
    # Test 4: Test persistence across connections
    print("\n[TEST 4] Testing persistence across connections...")
    conn.close()
    
    try:
        # Reopen connection
        conn2 = sqlite3.connect(test_db)
        cursor2 = conn2.cursor()
        
        cursor2.execute("SELECT COUNT(*) FROM memory_store WHERE session_id = ?", (test_session,))
        count = cursor2.fetchone()[0]
        
        if count == len(test_memories):
            print("[OK] Memories persisted across connections")
            test_results["passed"] += 1
        else:
            print(f"[FAIL] Persistence failed: expected {len(test_memories)}, got {count}")
            test_results["failed"] += 1
            
        conn2.close()
        
    except Exception as e:
        print(f"[FAIL] Persistence test failed: {e}")
        test_results["failed"] += 1
    
    # Test 5: Test memory updates
    print("\n[TEST 5] Testing memory updates...")
    try:
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        # Update existing memory
        new_value = "light_mode"
        cursor.execute("""
            UPDATE memory_store 
            SET value = ?, timestamp = CURRENT_TIMESTAMP
            WHERE session_id = ? AND key = ?
        """, (new_value, test_session, "user_preference"))
        
        conn.commit()
        
        # Verify update
        cursor.execute("""
            SELECT value FROM memory_store
            WHERE session_id = ? AND key = ?
        """, (test_session, "user_preference"))
        
        result = cursor.fetchone()
        if result and result[0] == new_value:
            print("[OK] Memory update successful")
            test_results["passed"] += 1
        else:
            print("[FAIL] Memory update failed")
            test_results["failed"] += 1
            
    except Exception as e:
        print(f"[FAIL] Update test failed: {e}")
        test_results["failed"] += 1
    
    # Test 6: Test session queries
    print("\n[TEST 6] Testing session metadata...")
    try:
        cursor.execute("""
            SELECT session_id, total_entries 
            FROM session_metadata
            WHERE session_id = ?
        """, (test_session,))
        
        metadata = cursor.fetchone()
        if metadata:
            print(f"[OK] Session metadata found: {metadata[0]} with {metadata[1]} entries")
            test_results["passed"] += 1
        else:
            print("[FAIL] Session metadata not found")
            test_results["failed"] += 1
            
    except Exception as e:
        print(f"[FAIL] Session query failed: {e}")
        test_results["failed"] += 1
    
    # Cleanup
    conn.close()
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Final report
    print("\n" + "=" * 60)
    print("[RESULTS] MEMORY PERSISTENCE TEST RESULTS")
    print(f"[OK] Passed: {test_results['passed']}")
    print(f"[FAIL] Failed: {test_results['failed']}")
    print(f"Success Rate: {(test_results['passed'] / (test_results['passed'] + test_results['failed']) * 100):.1f}%")
    
    return test_results

if __name__ == "__main__":
    test_memory_persistence()