#!/usr/bin/env python3
"""
Build and test script to verify the application before deployment
"""

import sys
import subprocess
from pathlib import Path

def run_test(name, command):
    """Run a test command"""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"{'='*70}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"✓ {name} PASSED")
            if result.stdout:
                print(result.stdout[:500])  # Print first 500 chars
            return True
        else:
            print(f"✗ {name} FAILED")
            print(f"Error: {result.stderr[:500]}")
            return False
    except Exception as e:
        print(f"✗ {name} FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("="*70)
    print("Gold Price Prediction - Build & Test")
    print("="*70)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Import test
    tests_total += 1
    if run_test("Import Test", "python test_imports.py"):
        tests_passed += 1
    
    # Test 2: Config test
    tests_total += 1
    if run_test("Config Test", 'python -c "from app.config import Config; print(\'Config OK\')"'):
        tests_passed += 1
    
    # Test 3: App initialization
    tests_total += 1
    if run_test("App Initialization", 'python -c "from app.core import GoldPriceApp; app = GoldPriceApp(); print(\'App OK\')"'):
        tests_passed += 1
    
    # Summary
    print(f"\n{'='*70}")
    print(f"Test Results: {tests_passed}/{tests_total} passed")
    print(f"{'='*70}")
    
    if tests_passed == tests_total:
        print("\n✓ All tests passed! Application is ready for deployment.")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix errors before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

