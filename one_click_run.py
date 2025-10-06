#!/usr/bin/env python3
"""
Ultra-simple one-command execution
"""
import subprocess
import sys

def main():
    print("🚀 C++ MICRO AGENT - ONE-CLICK EXECUTION")
    print("=" * 50)
    print("Running: python3 CppMicroAgent.py with option 3 (Complete Coverage Analysis)")
    print("-" * 50)
    
    try:
        # Simulate choosing option 3 automatically
        process = subprocess.Popen(
            ["python3", "CppMicroAgent.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd="/workspaces/CppMicroAgent"
        )
        
        # Send option 3 to the process
        stdout, _ = process.communicate(input="3\n")
        
        # Print all output
        print(stdout)
        
        return process.returncode
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())