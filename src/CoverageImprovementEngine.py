#!/usr/bin/env python3
"""
Advanced Coverage Improvement Mechanisms
Analyzes coverage gaps and implements intelligent strategies to improve coverage
"""

import os
import re
import ast
import subprocess
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from ConfigReader import ConfigReader
from OllamaClient import OllamaClient
import json

class CoverageImprovementStrategy(ABC):
    """Abstract base class for coverage improvement strategies"""
    
    @abstractmethod
    def analyze_gaps(self, coverage_data: Dict, source_files: List[str]) -> Dict:
        """Analyze coverage gaps and identify improvement opportunities"""
        pass
    
    @abstractmethod
    def generate_improvements(self, gap_analysis: Dict) -> List[Dict]:
        """Generate specific improvements based on gap analysis"""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Return the name of this strategy"""
        pass

class BranchCoverageStrategy(CoverageImprovementStrategy):
    """Strategy focused on improving branch coverage"""
    
    def __init__(self):
        self.client = OllamaClient()
        self.configReader = ConfigReader()
    
    def get_strategy_name(self) -> str:
        return "Branch Coverage Enhancement"
    
    def analyze_gaps(self, coverage_data: Dict, source_files: List[str]) -> Dict:
        """Analyze branch coverage gaps"""
        
        gaps = {
            "uncovered_branches": [],
            "conditional_statements": [],
            "switch_statements": [],
            "exception_paths": [],
            "early_returns": []
        }
        
        for source_file in source_files:
            if os.path.exists(source_file):
                gaps.update(self._analyze_source_file_branches(source_file))
        
        return gaps
    
    def _analyze_source_file_branches(self, source_file: str) -> Dict:
        """Analyze individual source file for branch coverage opportunities"""
        
        with open(source_file, 'r') as f:
            content = f.read()
        
        analysis = {
            "file": source_file,
            "if_statements": self._find_if_statements(content),
            "switch_statements": self._find_switch_statements(content),
            "try_catch_blocks": self._find_exception_handlers(content),
            "ternary_operators": self._find_ternary_operators(content),
            "loops_with_conditions": self._find_conditional_loops(content)
        }
        
        return analysis
    
    def _find_if_statements(self, content: str) -> List[Dict]:
        """Find if statements that may need branch coverage"""
        if_pattern = r'if\s*\([^)]+\)\s*{[^}]*}'
        matches = re.finditer(if_pattern, content, re.MULTILINE | re.DOTALL)
        
        if_statements = []
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            condition = match.group().split('(', 1)[1].split(')', 1)[0]
            
            if_statements.append({
                "line": line_num,
                "condition": condition.strip(),
                "full_statement": match.group(),
                "has_else": "else" in match.group().split('}')[1][:50] if '}' in match.group() else False
            })
        
        return if_statements
    
    def _find_switch_statements(self, content: str) -> List[Dict]:
        """Find switch statements for comprehensive case coverage"""
        switch_pattern = r'switch\s*\([^)]+\)\s*{[^}]*}'
        matches = re.finditer(switch_pattern, content, re.MULTILINE | re.DOTALL)
        
        switches = []
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            case_pattern = r'case\s+[^:]+:'
            cases = re.findall(case_pattern, match.group())
            has_default = 'default:' in match.group()
            
            switches.append({
                "line": line_num,
                "cases": cases,
                "has_default": has_default,
                "case_count": len(cases)
            })
        
        return switches
    
    def _find_exception_handlers(self, content: str) -> List[Dict]:
        """Find try-catch blocks for exception path coverage"""
        try_pattern = r'try\s*{[^}]*}\s*catch\s*\([^)]+\)\s*{[^}]*}'
        matches = re.finditer(try_pattern, content, re.MULTILINE | re.DOTALL)
        
        exceptions = []
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            catch_pattern = r'catch\s*\(([^)]+)\)'
            catch_types = re.findall(catch_pattern, match.group())
            
            exceptions.append({
                "line": line_num,
                "catch_types": catch_types,
                "exception_count": len(catch_types)
            })
        
        return exceptions
    
    def _find_ternary_operators(self, content: str) -> List[Dict]:
        """Find ternary operators that need both paths tested"""
        ternary_pattern = r'[^?]*\?[^:]*:[^;,)]*'
        matches = re.finditer(ternary_pattern, content)
        
        ternaries = []
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            ternaries.append({
                "line": line_num,
                "expression": match.group().strip()
            })
        
        return ternaries
    
    def _find_conditional_loops(self, content: str) -> List[Dict]:
        """Find loops with conditions that may need edge case testing"""
        loop_patterns = [
            r'for\s*\([^)]+\)\s*{',
            r'while\s*\([^)]+\)\s*{',
            r'do\s*{[^}]*}\s*while\s*\([^)]+\)'
        ]
        
        loops = []
        for pattern in loop_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                loops.append({
                    "line": line_num,
                    "type": "for" if "for" in match.group() else "while" if "while" in match.group() else "do-while",
                    "condition": self._extract_loop_condition(match.group())
                })
        
        return loops
    
    def _extract_loop_condition(self, loop_text: str) -> str:
        """Extract condition from loop statement"""
        if '(' in loop_text and ')' in loop_text:
            start = loop_text.find('(') + 1
            end = loop_text.rfind(')')
            return loop_text[start:end].strip()
        return ""
    
    def generate_improvements(self, gap_analysis: Dict) -> List[Dict]:
        """Generate branch coverage improvements using LLM"""
        
        improvements = []
        
        # Generate tests for if statements
        if "if_statements" in gap_analysis:
            for if_stmt in gap_analysis["if_statements"]:
                improvement = self._generate_if_statement_tests(if_stmt, gap_analysis["file"])
                if improvement:
                    improvements.append(improvement)
        
        # Generate tests for switch statements
        if "switch_statements" in gap_analysis:
            for switch in gap_analysis["switch_statements"]:
                improvement = self._generate_switch_tests(switch, gap_analysis["file"])
                if improvement:
                    improvements.append(improvement)
        
        return improvements
    
    def _generate_if_statement_tests(self, if_stmt: Dict, source_file: str) -> Dict:
        """Generate test cases for if statement branches"""
        
        prompt = f"""Generate comprehensive unit test cases for this C++ if statement:

Source File: {source_file}
Line: {if_stmt['line']}
Condition: {if_stmt['condition']}
Has Else: {if_stmt['has_else']}

Generate test cases that cover:
1. Condition evaluates to true
2. Condition evaluates to false
3. Edge cases for the condition
4. Boundary conditions

Return ONLY valid C++ test code using Google Test framework.
Include both positive and negative test scenarios.
"""
        
        try:
            response = self.client.query(self.configReader.get_gtest_model(), prompt)
            test_code = self._extract_code_from_response(response)
            
            return {
                "type": "if_statement_branch_coverage",
                "source_file": source_file,
                "line": if_stmt['line'],
                "condition": if_stmt['condition'],
                "generated_tests": test_code,
                "improvement_focus": "Branch coverage for conditional statements"
            }
        except Exception as e:
            print(f"Error generating if statement tests: {e}")
            return None
    
    def _generate_switch_tests(self, switch: Dict, source_file: str) -> Dict:
        """Generate test cases for switch statement coverage"""
        
        prompt = f"""Generate comprehensive unit test cases for this C++ switch statement:

Source File: {source_file}
Line: {switch['line']}
Cases: {switch['cases']}
Has Default: {switch['has_default']}
Case Count: {switch['case_count']}

Generate test cases that cover:
1. Each individual case
2. Default case (if present)
3. Invalid/unexpected values
4. Boundary values

Return ONLY valid C++ test code using Google Test framework.
"""
        
        try:
            response = self.client.query(self.configReader.get_gtest_model(), prompt)
            test_code = self._extract_code_from_response(response)
            
            return {
                "type": "switch_statement_coverage",
                "source_file": source_file,
                "line": switch['line'],
                "cases": switch['cases'],
                "generated_tests": test_code,
                "improvement_focus": "Complete switch case coverage"
            }
        except Exception as e:
            print(f"Error generating switch tests: {e}")
            return None
    
    def _extract_code_from_response(self, response: str) -> str:
        """Extract C++ code from LLM response"""
        # Parse JSON responses
        lines = response.strip().split('\n')
        code_text = ""
        
        for line in lines:
            try:
                response_json = json.loads(line)
                if not response_json.get("done", False):
                    code_text += response_json.get("response", "")
            except:
                continue
        
        # Clean up code blocks
        if "```cpp" in code_text:
            start = code_text.find("```cpp") + 6
            end = code_text.find("```", start)
            if end != -1:
                code_text = code_text[start:end]
        elif "```" in code_text:
            start = code_text.find("```") + 3
            end = code_text.find("```", start)
            if end != -1:
                code_text = code_text[start:end]
        
        return code_text.strip()

class PathCoverageStrategy(CoverageImprovementStrategy):
    """Strategy focused on improving path coverage through execution paths"""
    
    def get_strategy_name(self) -> str:
        return "Execution Path Coverage"
    
    def analyze_gaps(self, coverage_data: Dict, source_files: List[str]) -> Dict:
        """Analyze execution path coverage gaps"""
        
        gaps = {
            "uncovered_paths": [],
            "complex_functions": [],
            "nested_conditions": [],
            "loop_paths": []
        }
        
        for source_file in source_files:
            if os.path.exists(source_file):
                analysis = self._analyze_function_complexity(source_file)
                gaps["complex_functions"].extend(analysis)
        
        return gaps
    
    def _analyze_function_complexity(self, source_file: str) -> List[Dict]:
        """Analyze functions for complexity and path coverage opportunities"""
        
        with open(source_file, 'r') as f:
            content = f.read()
        
        # Find function definitions
        function_pattern = r'(?:[\w:]+\s+)?(\w+)\s*\([^)]*\)\s*{[^}]*}'
        matches = re.finditer(function_pattern, content, re.MULTILINE | re.DOTALL)
        
        complex_functions = []
        for match in matches:
            func_body = match.group()
            line_num = content[:match.start()].count('\n') + 1
            
            # Calculate cyclomatic complexity indicators
            if_count = func_body.count('if')
            switch_count = func_body.count('switch')
            loop_count = func_body.count('for') + func_body.count('while')
            complexity_score = if_count + switch_count + loop_count
            
            if complexity_score > 3:  # Functions with complexity > 3
                complex_functions.append({
                    "function": match.group(1) if match.groups() else "unknown",
                    "line": line_num,
                    "complexity_score": complexity_score,
                    "if_statements": if_count,
                    "switches": switch_count,
                    "loops": loop_count,
                    "source_file": source_file
                })
        
        return complex_functions
    
    def generate_improvements(self, gap_analysis: Dict) -> List[Dict]:
        """Generate path coverage improvements"""
        
        improvements = []
        
        if "complex_functions" in gap_analysis:
            for func in gap_analysis["complex_functions"]:
                improvement = self._generate_path_coverage_tests(func)
                if improvement:
                    improvements.append(improvement)
        
        return improvements
    
    def _generate_path_coverage_tests(self, func_data: Dict) -> Dict:
        """Generate tests for different execution paths"""
        
        return {
            "type": "path_coverage",
            "function": func_data["function"],
            "complexity_score": func_data["complexity_score"],
            "recommended_tests": func_data["complexity_score"] * 2,  # 2 tests per complexity point
            "focus_areas": [
                "Happy path execution",
                "Error path execution", 
                "Edge case paths",
                "Boundary condition paths"
            ]
        }

class BoundaryValueStrategy(CoverageImprovementStrategy):
    """Strategy focused on boundary value testing"""
    
    def get_strategy_name(self) -> str:
        return "Boundary Value Coverage"
    
    def analyze_gaps(self, coverage_data: Dict, source_files: List[str]) -> Dict:
        """Analyze boundary value testing opportunities"""
        
        gaps = {
            "numeric_boundaries": [],
            "array_boundaries": [],
            "string_boundaries": [],
            "loop_boundaries": []
        }
        
        for source_file in source_files:
            if os.path.exists(source_file):
                boundaries = self._find_boundary_opportunities(source_file)
                gaps.update(boundaries)
        
        return gaps
    
    def _find_boundary_opportunities(self, source_file: str) -> Dict:
        """Find boundary value testing opportunities"""
        
        with open(source_file, 'r') as f:
            content = f.read()
        
        # Find array access patterns
        array_pattern = r'\w+\[([^]]+)\]'
        array_matches = re.finditer(array_pattern, content)
        
        # Find numeric comparisons
        comparison_pattern = r'(\w+)\s*([<>=!]+)\s*(\d+)'
        comparison_matches = re.finditer(comparison_pattern, content)
        
        # Find size/length checks
        size_pattern = r'\.size\(\)|\.length\(\)'
        size_matches = re.finditer(size_pattern, content)
        
        return {
            "array_accesses": [m.group() for m in array_matches],
            "numeric_comparisons": [m.group() for m in comparison_matches],
            "size_checks": [m.group() for m in size_matches]
        }
    
    def generate_improvements(self, gap_analysis: Dict) -> List[Dict]:
        """Generate boundary value test improvements"""
        
        improvements = []
        
        # Generate boundary tests for arrays
        if gap_analysis.get("array_accesses"):
            improvements.append({
                "type": "array_boundary_tests",
                "test_cases": [
                    "Test with index 0 (lower boundary)",
                    "Test with index size-1 (upper boundary)", 
                    "Test with index -1 (invalid lower)",
                    "Test with index size (invalid upper)",
                    "Test with empty array"
                ]
            })
        
        # Generate boundary tests for numeric comparisons
        if gap_analysis.get("numeric_comparisons"):
            improvements.append({
                "type": "numeric_boundary_tests",
                "test_cases": [
                    "Test with minimum valid value",
                    "Test with maximum valid value",
                    "Test with value just below minimum",
                    "Test with value just above maximum",
                    "Test with zero",
                    "Test with negative values"
                ]
            })
        
        return improvements

class CoverageImprovementEngine:
    """Main engine that orchestrates multiple coverage improvement strategies"""
    
    def __init__(self):
        self.strategies = [
            BranchCoverageStrategy(),
            PathCoverageStrategy(),
            BoundaryValueStrategy()
        ]
        self.configReader = ConfigReader()
    
    def analyze_and_improve_coverage(self, coverage_data: Dict, source_files: List[str], 
                                   project_path: str) -> Dict:
        """Run all improvement strategies and generate comprehensive improvements"""
        
        print("🧠 ADVANCED COVERAGE IMPROVEMENT ANALYSIS")
        print("=" * 55)
        
        all_improvements = {}
        
        for strategy in self.strategies:
            print(f"🔍 Running {strategy.get_strategy_name()}...")
            
            try:
                # Analyze gaps using this strategy
                gaps = strategy.analyze_gaps(coverage_data, source_files)
                
                # Generate improvements
                improvements = strategy.generate_improvements(gaps)
                
                all_improvements[strategy.get_strategy_name()] = {
                    "gaps_found": gaps,
                    "improvements": improvements,
                    "improvement_count": len(improvements)
                }
                
                print(f"   ✅ Found {len(improvements)} improvement opportunities")
                
            except Exception as e:
                print(f"   ❌ Error in {strategy.get_strategy_name()}: {e}")
                all_improvements[strategy.get_strategy_name()] = {
                    "error": str(e)
                }
        
        # Generate comprehensive improvement report
        improvement_report = self._generate_improvement_report(all_improvements, project_path)
        
        return {
            "strategy_results": all_improvements,
            "improvement_report": improvement_report,
            "total_improvements": sum(
                result.get("improvement_count", 0) 
                for result in all_improvements.values()
            )
        }
    
    def _generate_improvement_report(self, improvements: Dict, project_path: str) -> str:
        """Generate a comprehensive improvement report"""
        
        report = f"""
COVERAGE IMPROVEMENT ANALYSIS REPORT
{'='*50}
Project: {project_path}
Analysis Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

IMPROVEMENT STRATEGIES APPLIED:
"""
        
        total_improvements = 0
        
        for strategy_name, result in improvements.items():
            if "error" in result:
                report += f"\n❌ {strategy_name}: Failed - {result['error']}\n"
                continue
                
            improvement_count = result.get("improvement_count", 0)
            total_improvements += improvement_count
            
            report += f"\n✅ {strategy_name}: {improvement_count} improvements identified\n"
            
            # Add specific improvements
            for improvement in result.get("improvements", []):
                if isinstance(improvement, dict):
                    imp_type = improvement.get("type", "general")
                    report += f"   • {imp_type.replace('_', ' ').title()}\n"
        
        report += f"""
SUMMARY:
  Total Improvement Opportunities: {total_improvements}
  
RECOMMENDED ACTIONS:
  1. Implement generated test cases for branch coverage
  2. Add boundary value tests for edge cases  
  3. Create path coverage tests for complex functions
  4. Review and execute generated test code
  5. Re-run coverage analysis to measure improvement

NEXT STEPS:
  • Review generated test cases in improvement report
  • Integrate recommended tests into test suite
  • Run iterative coverage improvement again
  • Target specific uncovered code paths identified
"""
        
        return report
    
    def save_improvement_analysis(self, analysis_results: Dict, output_dir: str) -> str:
        """Save detailed improvement analysis to file"""
        
        import json
        import datetime
        
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON analysis
        json_file = os.path.join(output_dir, f"coverage_improvement_analysis_{timestamp}.json")
        with open(json_file, 'w') as f:
            json.dump(analysis_results, f, indent=2, default=str)
        
        # Save text report
        text_file = os.path.join(output_dir, f"coverage_improvement_report_{timestamp}.txt")
        with open(text_file, 'w') as f:
            f.write(analysis_results["improvement_report"])
        
        print(f"📄 Improvement analysis saved:")
        print(f"   📊 JSON: {json_file}")
        print(f"   📝 Report: {text_file}")
        
        return text_file

def main():
    """Demo the coverage improvement engine"""
    
    # Sample coverage data
    sample_coverage = {
        "coverage_percentage": 65.0,
        "lines_covered": 130,
        "lines_total": 200,
        "uncovered_lines": [15, 23, 45, 67, 89]
    }
    
    # Sample source files
    sample_sources = [
        "/workspaces/CppMicroAgent/TestProjects/SampleApplication/SampleApp/SampleApp.cpp",
        "/workspaces/CppMicroAgent/TestProjects/SampleApplication/SampleApp/src/Program/Program.cpp"
    ]
    
    # Run improvement analysis
    engine = CoverageImprovementEngine()
    results = engine.analyze_and_improve_coverage(
        sample_coverage, 
        sample_sources, 
        "TestProjects/SampleApplication/SampleApp"
    )
    
    # Save results
    engine.save_improvement_analysis(results, "output/CoverageImprovements")
    
    print(f"\n🎯 IMPROVEMENT ANALYSIS COMPLETE!")
    print(f"Total improvement opportunities: {results['total_improvements']}")

if __name__ == "__main__":
    main()