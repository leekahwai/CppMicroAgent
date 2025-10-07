#!/usr/bin/env python3
"""
Ollama-powered test fixer
Uses Ollama to analyze and fix test logic issues
"""

import json
import subprocess
import sys
from pathlib import Path


def call_ollama(prompt: str, model: str = "qwen2.5:0.5b") -> str:
    """Call Ollama API to get AI assistance"""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            capture_output=True,
            timeout=60
        )
        return result.stdout.decode('utf-8', errors='ignore').strip()
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return ""


def analyze_test_failure(test_name: str, test_code: str, class_name: str, method_name: str) -> str:
    """Use Ollama to analyze why a test might be failing"""
    
    prompt = f"""Analyze this C++ unit test that is crashing at runtime.

Test Name: {test_name}
Class: {class_name}
Method: {method_name}

Test Code:
{test_code}

The test compiles successfully but crashes at runtime with stack smashing or futex errors.
This suggests threading or initialization issues.

Provide a brief analysis (2-3 sentences) of what might be wrong and what should be checked.
Focus on: initialization order, thread safety, resource management, and object lifecycle.
"""
    
    return call_ollama(prompt)


def generate_improved_test(test_code: str, class_name: str, method_name: str, 
                          analysis: str, return_type: str) -> str:
    """Use Ollama to generate improved test code"""
    
    prompt = f"""You are improving a C++ unit test that crashes at runtime.

Class: {class_name}
Method: {method_name}
Return Type: {return_type}

Current Test Code:
{test_code}

Analysis: {analysis}

Generate an improved test that:
1. Properly initializes the object (call init() if available)
2. Checks initialization success before testing
3. Properly cleans up (call close() if available)
4. Uses EXPECT instead of ASSERT for non-critical checks
5. Handles potential threading issues

Provide ONLY the improved test code, no explanations. Start with TEST_F and end with the closing brace.
"""
    
    return call_ollama(prompt)


def main():
    """Main function to fix failing tests"""
    
    # Load test metadata
    metadata_path = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests/test_metadata.json")
    with open(metadata_path) as f:
        tests = json.load(f)
    
    # Get list of failing tests
    failing_tests = [
        "InterfaceB_init", "InterfaceB_close", "InterfaceB_addToTx", "InterfaceB_addToRx",
        "InterfaceB_getTxStats", "InterfaceB_getRxStats",
        "InterfaceA_init", "InterfaceA_close", "InterfaceA_addToTx", "InterfaceA_addToRx",
        "InterfaceA_getTxStats", "InterfaceA_getRxStats",
        "ProgramApp_ProgramApp", "ProgramApp_run", "Program_run"
    ]
    
    print("Analyzing failing tests with Ollama...")
    print("=" * 70)
    
    for test_meta in tests:
        test_name = test_meta['test_name']
        
        if test_name not in failing_tests:
            continue
        
        test_file = Path(test_meta['test_file'])
        if not test_file.exists():
            continue
        
        print(f"\nAnalyzing: {test_name}")
        
        # Read test code
        with open(test_file, 'r') as f:
            test_code = f.read()
        
        # Analyze with Ollama
        analysis = analyze_test_failure(
            test_name,
            test_code,
            test_meta['class_name'],
            test_meta['method_name']
        )
        
        print(f"Analysis: {analysis[:200]}...")
        
        # For now, just show analysis
        # In the next step, we'll integrate improvements back into the generator
    
    print("\n" + "=" * 70)
    print("Analysis complete!")


if __name__ == "__main__":
    main()
