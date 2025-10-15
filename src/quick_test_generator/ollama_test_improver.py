#!/usr/bin/env python3
"""
Ollama-powered Test Generation Improvement Tool
Uses Qwen AI via Ollama to analyze project structure and generate improved:
1. C++ parsers tailored to the project
2. Test generators with project-specific optimizations
3. Enhanced test templates for better coverage

This tool is designed to work with the Python state machines and generators
to create project-specific improvements for higher test coverage.
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config_reader import get_project_path, get_unittest_model


def call_ollama_qwen(prompt: str, model: str = None) -> str:
    """Call Ollama with Qwen model to get AI assistance
    
    Uses either:
    - Local Ollama CLI with qwen3-coder:480b
    - Cloud-based Ollama via OpenAI API format (when OPENAI_BASE_URL is set)
    """
    if model is None:
        model = os.environ.get('OPENAI_MODEL', 'qwen3-coder:480b')
    
    # Check if we should use OpenAI API format (for cloud-based Ollama)
    openai_base_url = os.environ.get('OPENAI_BASE_URL')
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    
    if openai_base_url and openai_api_key:
        print(f"  ☁️  Using cloud-based Ollama: {model}")
        return call_ollama_via_openai_api(prompt, model, openai_base_url, openai_api_key)
    else:
        print(f"  🖥️  Using local Ollama: {model}")
        return call_ollama_via_cli(prompt, model)


def call_ollama_via_cli(prompt: str, model: str) -> str:
    """Call local Ollama via CLI"""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            capture_output=True,
            timeout=120  # Longer timeout for complex analysis
        )
        return result.stdout.decode('utf-8', errors='ignore').strip()
    except subprocess.TimeoutExpired:
        print("  ⚠️  Ollama request timed out")
        return ""
    except Exception as e:
        print(f"  ❌ Error calling Ollama: {e}")
        return ""


def call_ollama_via_openai_api(prompt: str, model: str, base_url: str, api_key: str) -> str:
    """Call cloud-based Ollama via OpenAI API format"""
    try:
        import requests
        
        url = f"{base_url.rstrip('/')}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an expert C++ developer and testing specialist. Provide concise, high-quality code improvements."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,  # Lower temperature for more focused output
            "max_tokens": 4000
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
        
        print(f"  ⚠️  API returned status code: {response.status_code}")
        return ""
    except Exception as e:
        print(f"  ❌ Error calling Ollama API: {e}")
        return ""


def analyze_project_structure(project_path: str) -> Dict:
    """Analyze the project structure to understand patterns"""
    print(f"\n📂 Analyzing project structure: {project_path}")
    
    analysis = {
        "source_files": [],
        "header_files": [],
        "class_patterns": [],
        "common_includes": set(),
        "namespace_patterns": [],
        "template_usage": False,
        "inheritance_depth": 0,
        "project_name": Path(project_path).name
    }
    
    # Find all C++ files
    for ext in ['*.cpp', '*.cc', '*.cxx']:
        analysis["source_files"].extend(Path(project_path).rglob(ext))
    
    for ext in ['*.h', '*.hpp', '*.hxx']:
        analysis["header_files"].extend(Path(project_path).rglob(ext))
    
    print(f"  Found {len(analysis['source_files'])} source files")
    print(f"  Found {len(analysis['header_files'])} header files")
    
    # Analyze patterns in a sample of files
    sample_files = (list(analysis["source_files"])[:5] + 
                    list(analysis["header_files"])[:5])
    
    for file_path in sample_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Find includes
                includes = re.findall(r'#include\s+[<"]([^>"]+)[>"]', content)
                analysis["common_includes"].update(includes)
                
                # Find namespaces
                namespaces = re.findall(r'namespace\s+(\w+)', content)
                analysis["namespace_patterns"].extend(namespaces)
                
                # Check for templates
                if 'template<' in content or 'template <' in content:
                    analysis["template_usage"] = True
                
                # Find class declarations
                classes = re.findall(r'class\s+(\w+)', content)
                analysis["class_patterns"].extend(classes)
        except Exception as e:
            continue
    
    return analysis


def generate_improved_parser_prompt(analysis: Dict, current_parser_code: str) -> str:
    """Generate a prompt for Ollama to improve the C++ parser"""
    
    prompt = f"""You are tasked with improving a C++ parser for unit test generation. 

PROJECT CONTEXT:
- Project Name: {analysis['project_name']}
- Source Files: {len(analysis['source_files'])}
- Header Files: {len(analysis['header_files'])}
- Uses Templates: {analysis['template_usage']}
- Common Namespaces: {', '.join(set(analysis['namespace_patterns'][:5]))}
- Sample Classes: {', '.join(analysis['class_patterns'][:10])}

CURRENT PARSER CODE (excerpt):
```python
{current_parser_code[:2000]}
```

TASK:
Analyze the project structure and suggest 3-5 specific improvements to the parser that would:
1. Better handle this project's specific coding patterns
2. Improve method/function detection accuracy
3. Better parse constructor/destructor patterns
4. Handle template specializations if present
5. Improve parameter parsing for this project's style

Provide your response in this format:
IMPROVEMENT 1: [Title]
[Concise description]
CODE:
```python
[Code snippet showing the improvement]
```

IMPROVEMENT 2: [Title]
...

Focus on practical, implementable improvements. Be specific to this project's patterns.
"""
    return prompt


def generate_test_strategy_prompt(analysis: Dict, sample_code: str) -> str:
    """Generate a prompt for Ollama to suggest project-specific test strategies"""
    
    prompt = f"""You are a C++ testing expert. Analyze this project and suggest high-coverage testing strategies.

PROJECT CONTEXT:
- Project Name: {analysis['project_name']}
- Total Source Files: {len(analysis['source_files'])}
- Total Header Files: {len(analysis['header_files'])}
- Uses Templates: {analysis['template_usage']}
- Common Includes: {', '.join(list(analysis['common_includes'])[:10])}

SAMPLE CODE FROM PROJECT:
```cpp
{sample_code[:1500]}
```

TASK:
Suggest 5 specific test generation strategies optimized for THIS project:

1. Boundary value strategies (based on actual patterns seen)
2. Mock object strategies (based on dependencies)
3. Constructor testing approaches (based on patterns)
4. Template testing strategies (if applicable)
5. Integration test opportunities

For each strategy, provide:
- Strategy name
- Why it's relevant to THIS project
- Sample test pattern (pseudo-code)

Be specific and actionable. Focus on achieving 70%+ coverage.
"""
    return prompt


def improve_parser_for_project(project_path: str) -> bool:
    """Use Ollama to analyze project and generate improved parser"""
    
    print("\n" + "="*70)
    print("🤖 OLLAMA AI: Improving C++ Parser for Project")
    print("="*70)
    
    # Analyze project
    analysis = analyze_project_structure(project_path)
    
    # Read current parser code
    parser_file = Path(__file__).parent.parent / "improved_cpp_parser.py"
    if not parser_file.exists():
        print(f"  ❌ Parser file not found: {parser_file}")
        return False
    
    with open(parser_file, 'r') as f:
        current_parser = f.read()
    
    print("\n📝 Generating improvement suggestions...")
    prompt = generate_improved_parser_prompt(analysis, current_parser)
    
    improvements = call_ollama_qwen(prompt)
    
    if not improvements:
        print("  ❌ Failed to get improvements from Ollama")
        return False
    
    # Save improvements to a file
    output_dir = Path("output/OllamaImprovements")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    improvements_file = output_dir / "parser_improvements.md"
    with open(improvements_file, 'w') as f:
        f.write(f"# Parser Improvements for {analysis['project_name']}\n\n")
        f.write(f"Generated using Qwen AI via Ollama\n\n")
        f.write(improvements)
    
    print(f"\n✅ Improvements saved to: {improvements_file}")
    print("\n" + "-"*70)
    print("SUGGESTED IMPROVEMENTS:")
    print("-"*70)
    print(improvements[:1000])
    if len(improvements) > 1000:
        print(f"\n... (see full output in {improvements_file})")
    
    return True


def generate_project_specific_tests(project_path: str) -> bool:
    """Use Ollama to generate project-specific test strategies"""
    
    print("\n" + "="*70)
    print("🤖 OLLAMA AI: Generating Project-Specific Test Strategies")
    print("="*70)
    
    # Analyze project
    analysis = analyze_project_structure(project_path)
    
    # Get sample code from the project
    sample_code = ""
    if analysis['source_files']:
        try:
            sample_file = analysis['source_files'][0]
            with open(sample_file, 'r', encoding='utf-8', errors='ignore') as f:
                sample_code = f.read()
        except:
            pass
    
    print("\n📝 Analyzing project patterns and generating test strategies...")
    prompt = generate_test_strategy_prompt(analysis, sample_code)
    
    strategies = call_ollama_qwen(prompt)
    
    if not strategies:
        print("  ❌ Failed to get strategies from Ollama")
        return False
    
    # Save strategies
    output_dir = Path("output/OllamaImprovements")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    strategies_file = output_dir / "test_strategies.md"
    with open(strategies_file, 'w') as f:
        f.write(f"# Test Strategies for {analysis['project_name']}\n\n")
        f.write(f"Generated using Qwen AI via Ollama\n\n")
        f.write(strategies)
    
    print(f"\n✅ Strategies saved to: {strategies_file}")
    print("\n" + "-"*70)
    print("SUGGESTED TEST STRATEGIES:")
    print("-"*70)
    print(strategies[:1000])
    if len(strategies) > 1000:
        print(f"\n... (see full output in {strategies_file})")
    
    return True


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🚀 Ollama AI Test Generation Improver")
    print("   Using Qwen 3-Coder 480B for project-specific analysis")
    print("="*70)
    
    # Get project path
    project_path = get_project_path()
    
    if not project_path or not Path(project_path).exists():
        print(f"\n❌ Project path not found or invalid: {project_path}")
        return False
    
    print(f"\n📍 Working with project: {project_path}")
    
    # Check if Ollama is available
    try:
        result = subprocess.run(
            ["which", "ollama"],
            capture_output=True,
            timeout=2
        )
        if result.returncode != 0:
            print("\n❌ Ollama not found. Please install it first.")
            return False
    except:
        print("\n❌ Ollama not available")
        return False
    
    print("\n" + "="*70)
    print("ANALYSIS PLAN:")
    print("="*70)
    print("1. Analyze project structure and patterns")
    print("2. Generate improved C++ parser recommendations")
    print("3. Generate project-specific test strategies")
    print("4. Save all recommendations for review and implementation")
    print("="*70)
    
    input("\nPress Enter to start analysis...")
    
    # Step 1: Improve parser
    success1 = improve_parser_for_project(project_path)
    
    # Step 2: Generate test strategies
    success2 = generate_project_specific_tests(project_path)
    
    if success1 and success2:
        print("\n" + "="*70)
        print("✅ ANALYSIS COMPLETE!")
        print("="*70)
        print("\n📁 Results saved in: output/OllamaImprovements/")
        print("\nNext steps:")
        print("1. Review parser_improvements.md")
        print("2. Review test_strategies.md")
        print("3. Apply relevant improvements to the codebase")
        print("4. Run Option 1 to generate tests with improvements")
        print("="*70)
        return True
    else:
        print("\n❌ Analysis incomplete - check errors above")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
