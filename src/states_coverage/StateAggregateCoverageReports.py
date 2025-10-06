"""
StateAggregateCoverageReports - Aggregate all function-level coverage into final report
"""

import os
import datetime
from flow_manager import flow

class StateAggregateCoverageReports():
    def __init__(self):
        print("Initializing [StateAggregateCoverageReports]")

    def run(self, input_data):
        flow.transition("StateAggregateCoverageReports")
        print("[StateAggregateCoverageReports] Aggregating all coverage reports...")
        
        cmake_dir = input_data.get_input_data()
        project_name = os.path.basename(cmake_dir)
        output_dir = "output/UnitTestCoverage"
        
        # Collect all function-level coverage data
        all_coverage_data = self._collect_all_coverage_data(output_dir)
        
        # Calculate overall statistics
        overall_stats = self._calculate_overall_stats(all_coverage_data)
        
        # Generate comprehensive report
        report_content = self._generate_comprehensive_report(
            project_name, 
            cmake_dir, 
            all_coverage_data, 
            overall_stats,
            input_data
        )
        
        # Save final report
        report_file = os.path.join(output_dir, "FINAL_COVERAGE_REPORT.txt")
        try:
            with open(report_file, 'w') as f:
                f.write(report_content)
            print(f"[StateAggregateCoverageReports] Final report saved: {report_file}")
            print(f"[StateAggregateCoverageReports] Overall Coverage: {overall_stats['overall_coverage']:.1f}%")
        except Exception as e:
            print(f"[StateAggregateCoverageReports] Error writing report: {e}")
            return False, input_data
        
        return True, input_data

    def _collect_all_coverage_data(self, output_dir):
        """Walk through all function directories and collect coverage data"""
        
        all_coverage = []
        
        if not os.path.exists(output_dir):
            return all_coverage
        
        # Walk through the directory structure
        for source_file_dir in os.listdir(output_dir):
            source_path = os.path.join(output_dir, source_file_dir)
            
            if not os.path.isdir(source_path):
                continue
            
            # This is a source file directory (e.g., Program.cpp)
            for function_dir in os.listdir(source_path):
                function_path = os.path.join(source_path, function_dir)
                
                if not os.path.isdir(function_path):
                    continue
                
                # This is a function directory
                # Look for coverage_summary.txt
                summary_file = os.path.join(function_path, "coverage_summary.txt")
                
                if os.path.exists(summary_file):
                    coverage_info = self._parse_coverage_summary(summary_file)
                    coverage_info["source_file"] = source_file_dir
                    coverage_info["function_name"] = function_dir
                    coverage_info["function_path"] = function_path
                    all_coverage.append(coverage_info)
        
        return all_coverage

    def _parse_coverage_summary(self, summary_file):
        """Parse a coverage summary file"""
        
        coverage_info = {
            "coverage_percentage": 0.0,
            "lines_covered": 0,
            "lines_total": 0,
            "functions_covered": 0,
            "functions_total": 0,
            "has_html_report": False
        }
        
        try:
            with open(summary_file, 'r') as f:
                content = f.read()
            
            # Parse key metrics
            for line in content.split('\n'):
                if "Coverage Percentage:" in line:
                    try:
                        coverage_info["coverage_percentage"] = float(line.split(':')[1].strip().rstrip('%'))
                    except:
                        pass
                elif "Lines Covered:" in line:
                    try:
                        coverage_info["lines_covered"] = int(line.split(':')[1].strip())
                    except:
                        pass
                elif "Total Lines:" in line:
                    try:
                        coverage_info["lines_total"] = int(line.split(':')[1].strip())
                    except:
                        pass
                elif "HTML Report:" in line:
                    coverage_info["has_html_report"] = True
        
        except Exception as e:
            print(f"[StateAggregateCoverageReports] Error parsing {summary_file}: {e}")
        
        return coverage_info

    def _calculate_overall_stats(self, all_coverage_data):
        """Calculate overall project statistics"""
        
        total_lines_covered = 0
        total_lines = 0
        total_functions = len(all_coverage_data)
        functions_with_coverage = 0
        
        for coverage in all_coverage_data:
            total_lines_covered += coverage.get("lines_covered", 0)
            total_lines += coverage.get("lines_total", 0)
            if coverage.get("coverage_percentage", 0) > 0:
                functions_with_coverage += 1
        
        overall_coverage = 0.0
        if total_lines > 0:
            overall_coverage = (total_lines_covered / total_lines) * 100
        
        return {
            "overall_coverage": overall_coverage,
            "total_lines_covered": total_lines_covered,
            "total_lines": total_lines,
            "total_functions_tested": total_functions,
            "functions_with_coverage": functions_with_coverage
        }

    def _generate_comprehensive_report(self, project_name, cmake_dir, all_coverage_data, overall_stats, input_data):
        """Generate comprehensive final report"""
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
{'='*80}
           C++ MICRO AGENT - FINAL COVERAGE REPORT
{'='*80}

Project Name: {project_name}
Project Path: {cmake_dir}
Generated:    {timestamp}
Report Type:  Per-Function Coverage Analysis with Aggregation

{'='*80}

OVERALL PROJECT COVERAGE SUMMARY
{'='*80}

Overall Coverage:           {overall_stats['overall_coverage']:.1f}%
Total Lines Covered:        {overall_stats['total_lines_covered']:,}
Total Lines:                {overall_stats['total_lines']:,}
Total Functions Tested:     {overall_stats['total_functions_tested']}
Functions with Coverage:    {overall_stats['functions_with_coverage']}

Coverage Assessment: {self._get_coverage_assessment(overall_stats['overall_coverage'])}

{'='*80}

PER-FUNCTION COVERAGE BREAKDOWN
{'='*80}

"""
        
        # Group by source file
        by_source = {}
        for coverage in all_coverage_data:
            source = coverage["source_file"]
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(coverage)
        
        # Report each source file
        for source_file, functions in sorted(by_source.items()):
            report += f"\n📁 {source_file}\n"
            report += f"{'-'*60}\n"
            
            for func in sorted(functions, key=lambda x: x.get("coverage_percentage", 0), reverse=True):
                func_name = func["function_name"]
                coverage_pct = func.get("coverage_percentage", 0)
                lines_covered = func.get("lines_covered", 0)
                lines_total = func.get("lines_total", 0)
                
                # Visual indicator
                if coverage_pct >= 80:
                    indicator = "✅"
                elif coverage_pct >= 60:
                    indicator = "🟡"
                elif coverage_pct >= 40:
                    indicator = "🟠"
                else:
                    indicator = "❌"
                
                report += f"  {indicator} {func_name:<40} {coverage_pct:>5.1f}%  ({lines_covered}/{lines_total} lines)\n"
                
                if func.get("has_html_report"):
                    report += f"     HTML: {func['function_path']}/build/coverage_html/index.html\n"
            
            # Calculate source file average
            source_avg = sum(f.get("coverage_percentage", 0) for f in functions) / len(functions) if functions else 0
            report += f"\n  Source File Average: {source_avg:.1f}%\n"
        
        # Coverage distribution
        report += f"""

{'='*80}

COVERAGE DISTRIBUTION
{'='*80}

"""
        
        # Categorize functions by coverage
        excellent = [c for c in all_coverage_data if c.get("coverage_percentage", 0) >= 80]
        good = [c for c in all_coverage_data if 60 <= c.get("coverage_percentage", 0) < 80]
        fair = [c for c in all_coverage_data if 40 <= c.get("coverage_percentage", 0) < 60]
        poor = [c for c in all_coverage_data if c.get("coverage_percentage", 0) < 40]
        
        report += f"✅ Excellent (>=80%):  {len(excellent):3d} functions\n"
        report += f"🟡 Good (60-79%):      {len(good):3d} functions\n"
        report += f"🟠 Fair (40-59%):      {len(fair):3d} functions\n"
        report += f"❌ Poor (<40%):        {len(poor):3d} functions\n"
        
        # Recommendations
        report += f"""

{'='*80}

RECOMMENDATIONS
{'='*80}

"""
        
        if overall_stats['overall_coverage'] >= 80:
            report += "🎉 Excellent! Your project has high test coverage.\n"
            report += "   - Maintain this coverage level\n"
            report += "   - Focus on edge cases and error conditions\n"
        elif overall_stats['overall_coverage'] >= 60:
            report += "👍 Good coverage, but there's room for improvement.\n"
            report += "   - Focus on functions with <60% coverage\n"
            report += "   - Add more test cases for edge conditions\n"
        else:
            report += "⚠️  Coverage needs improvement.\n"
            report += "   - Prioritize functions with low coverage\n"
            report += "   - Review and enhance existing tests\n"
        
        if poor:
            report += f"\n📋 Functions needing immediate attention ({len(poor)} functions):\n"
            for func in sorted(poor, key=lambda x: x.get("coverage_percentage", 0))[:10]:
                report += f"   - {func['source_file']}/{func['function_name']}: {func.get('coverage_percentage', 0):.1f}%\n"
        
        # Directory structure
        report += f"""

{'='*80}

OUTPUT DIRECTORY STRUCTURE
{'='*80}

output/UnitTestCoverage/
"""
        
        for source_file, functions in sorted(by_source.items()):
            report += f"├── {source_file}/\n"
            for i, func in enumerate(sorted(functions, key=lambda x: x["function_name"])):
                is_last = (i == len(functions) - 1)
                connector = "└──" if is_last else "├──"
                report += f"│   {connector} {func['function_name']}/\n"
                indent = "    " if is_last else "│   "
                report += f"│   {indent}├── test_{func['function_name']}.cpp (unit test)\n"
                report += f"│   {indent}├── coverage_summary.txt\n"
                report += f"│   {indent}└── build/\n"
                report += f"│   {indent}    ├── test_executable\n"
                report += f"│   {indent}    ├── coverage_html/ (HTML report)\n"
                report += f"│   {indent}    └── *.gcov files\n"
        
        report += f"""
└── FINAL_COVERAGE_REPORT.txt (this file)

{'='*80}

For detailed per-function coverage, open the HTML reports in each function's
build/coverage_html/index.html directory.

Report generated by C++ Micro Agent - Per-Function Coverage Analysis
{'='*80}
"""
        
        return report

    def _get_coverage_assessment(self, coverage_pct):
        """Get textual assessment of coverage level"""
        
        if coverage_pct >= 90:
            return "🟢 Excellent - Outstanding test coverage!"
        elif coverage_pct >= 80:
            return "🟢 Very Good - High quality testing"
        elif coverage_pct >= 70:
            return "🟡 Good - Solid test coverage"
        elif coverage_pct >= 60:
            return "🟡 Fair - Adequate but could improve"
        elif coverage_pct >= 40:
            return "🟠 Needs Improvement - Critical gaps exist"
        else:
            return "🔴 Poor - Significant testing required"
