#!/usr/bin/env python3
"""
Create a demo consolidated coverage report with sample data
"""
import os
import sys
import json
import datetime

def create_demo_consolidated_report():
    """Create a demonstration consolidated report with sample coverage data"""
    
    print("📊 CREATING DEMO CONSOLIDATED COVERAGE REPORT")
    print("=" * 55)
    
    # Create sample data for multiple projects
    sample_results = [
        {
            "project_name": "SampleApplication",
            "project_path": "TestProjects/SampleApplication/SampleApp",
            "description": "Original sample C++ application with interfaces",
            "source_files_count": 9,
            "analysis_time": datetime.datetime.now().isoformat(),
            "success": True,
            "final_coverage": 85.2,
            "iterations_completed": 2,
            "target_achieved": True,
            "target_coverage": 80.0,
            "coverage_data": {
                "lines_covered": 156,
                "lines_total": 183,
                "functions_covered": 12,
                "functions_total": 15,
                "coverage_percentage": 85.2
            }
        },
        {
            "project_name": "fmt-library",
            "project_path": "TestProjects/fmt-library",
            "description": "Modern C++ string formatting library",
            "source_files_count": 46,
            "analysis_time": datetime.datetime.now().isoformat(),
            "success": True,
            "final_coverage": 72.8,
            "iterations_completed": 3,
            "target_achieved": False,
            "target_coverage": 80.0,
            "coverage_data": {
                "lines_covered": 1247,
                "lines_total": 1713,
                "functions_covered": 89,
                "functions_total": 124,
                "coverage_percentage": 72.8
            }
        },
        {
            "project_name": "nlohmann-json",
            "project_path": "TestProjects/nlohmann-json",
            "description": "JSON for Modern C++ library",
            "source_files_count": 407,
            "analysis_time": datetime.datetime.now().isoformat(),
            "success": True,
            "final_coverage": 91.5,
            "iterations_completed": 2,
            "target_achieved": True,
            "target_coverage": 80.0,
            "coverage_data": {
                "lines_covered": 3847,
                "lines_total": 4203,
                "functions_covered": 287,
                "functions_total": 312,
                "coverage_percentage": 91.5
            }
        },
        {
            "project_name": "spdlog-library",
            "project_path": "TestProjects/spdlog-library",
            "description": "Fast C++ logging library",
            "source_files_count": 38,
            "analysis_time": datetime.datetime.now().isoformat(),
            "success": True,
            "final_coverage": 78.3,
            "iterations_completed": 3,
            "target_achieved": False,
            "target_coverage": 80.0,
            "coverage_data": {
                "lines_covered": 892,
                "lines_total": 1139,
                "functions_covered": 67,
                "functions_total": 89,
                "coverage_percentage": 78.3
            }
        },
        {
            "project_name": "catch2-library",
            "project_path": "TestProjects/catch2-library", 
            "description": "Modern C++ unit testing framework",
            "source_files_count": 220,
            "analysis_time": datetime.datetime.now().isoformat(),
            "success": False,
            "error": "Complex template metaprogramming - analysis incomplete"
        }
    ]
    
    # Create consolidated reports directory
    os.makedirs("output/ConsolidatedReports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate comprehensive JSON report
    json_report = {
        "analysis_metadata": {
            "timestamp": timestamp,
            "total_projects": len(sample_results),
            "successful_analyses": len([r for r in sample_results if r.get('success', False)]),
            "failed_analyses": len([r for r in sample_results if not r.get('success', False)]),
            "configuration": {
                "coverage_target": 80.0,
                "max_iterations": 3,
                "analysis_type": "iterative_unit_test_generation"
            }
        },
        "project_results": sample_results,
        "summary_statistics": {
            "total_source_files": sum(r.get('source_files_count', 0) for r in sample_results),
            "average_coverage": sum(r.get('final_coverage', 0) for r in sample_results if r.get('success', False)) / len([r for r in sample_results if r.get('success', False)]),
            "projects_achieving_target": len([r for r in sample_results if r.get('target_achieved', False)]),
            "total_iterations": sum(r.get('iterations_completed', 0) for r in sample_results if r.get('success', False))
        }
    }
    
    json_file = f"output/ConsolidatedReports/consolidated_coverage_analysis_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(json_report, f, indent=2)
    
    # Generate comprehensive text report
    text_report = generate_text_report(sample_results, timestamp)
    text_file = f"output/ConsolidatedReports/consolidated_coverage_report_{timestamp}.txt"
    with open(text_file, 'w') as f:
        f.write(text_report)
    
    # Generate executive summary
    summary_report = generate_executive_summary(sample_results)
    summary_file = f"output/ConsolidatedReports/executive_summary_{timestamp}.txt"
    with open(summary_file, 'w') as f:
        f.write(summary_report)
    
    print(f"📄 Generated consolidated reports:")
    print(f"   📊 JSON Data: {json_file}")
    print(f"   📝 Detailed Report: {text_file}")
    print(f"   📋 Executive Summary: {summary_file}")
    
    # Print console summary
    print_console_summary(sample_results)
    
    return json_file, text_file, summary_file

def generate_text_report(results, timestamp):
    """Generate detailed text report"""
    
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    report = f"""
{'='*80}
            C++ MICRO AGENT - CONSOLIDATED COVERAGE ANALYSIS REPORT
{'='*80}

Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Analysis ID: {timestamp}
Total Projects Analyzed: {len(results)}
Successful Analyses: {len(successful)}
Failed Analyses: {len(failed)}

CONFIGURATION:
  Coverage Target: 80.0%
  Maximum Iterations: 3
  Analysis Method: Iterative Unit Test Generation with LLM Feedback

{'='*80}

EXECUTIVE SUMMARY:
"""
    
    if successful:
        avg_coverage = sum(r['final_coverage'] for r in successful) / len(successful)
        high_coverage = [r for r in successful if r['target_achieved']]
        total_files = sum(r['source_files_count'] for r in results)
        
        report += f"""
  📊 Average Coverage Achieved: {avg_coverage:.1f}%
  🎯 Projects Meeting Target: {len(high_coverage)}/{len(successful)} ({len(high_coverage)/len(successful)*100:.1f}%)
  📁 Total Source Files Analyzed: {total_files:,}
  🔄 Average Iterations per Project: {sum(r['iterations_completed'] for r in successful) / len(successful):.1f}

PROJECT RANKINGS (by coverage):
"""
        
        successful_sorted = sorted(successful, key=lambda x: x['final_coverage'], reverse=True)
        for i, result in enumerate(successful_sorted, 1):
            status = "🏆" if result['target_achieved'] else "📊"
            report += f"  {i:2d}. {status} {result['project_name']:<25} {result['final_coverage']:6.1f}%\n"
    
    report += f"\n{'='*80}\n\nDETAILED PROJECT ANALYSIS:\n\n"
    
    for i, result in enumerate(results, 1):
        report += f"""
PROJECT {i}: {result['project_name']}
{'-'*60}
Path: {result['project_path']}
Description: {result['description']}
Source Files: {result['source_files_count']:,}
Analysis Time: {result['analysis_time']}
"""
        
        if result.get('success', False):
            coverage = result['final_coverage']
            iterations = result['iterations_completed']
            target_achieved = result['target_achieved']
            
            status = "SUCCESS ✅" if target_achieved else "PARTIAL 🔄"
            
            report += f"""
Status: {status}
Final Coverage: {coverage:.1f}%
Iterations Completed: {iterations}
Target Achieved: {'Yes' if target_achieved else 'No'}

Coverage Breakdown:
"""
            if 'coverage_data' in result:
                cd = result['coverage_data']
                report += f"  Lines: {cd['lines_covered']:,}/{cd['lines_total']:,} ({cd['coverage_percentage']:.1f}%)\n"
                report += f"  Functions: {cd['functions_covered']}/{cd['functions_total']} ({cd['functions_covered']/cd['functions_total']*100:.1f}%)\n"
            
            # Coverage assessment
            if coverage >= 90:
                assessment = "Excellent - Production ready"
            elif coverage >= 80:
                assessment = "Good - Meets target standards"
            elif coverage >= 60:
                assessment = "Fair - Needs improvement"
            else:
                assessment = "Poor - Significant gaps"
            
            report += f"  Assessment: {assessment}\n"
            
        else:
            report += f"""
Status: FAILED ❌
Error: {result.get('error', 'Unknown error')}
Recommendation: Manual analysis or project structure adjustment needed
"""
        
        report += "\n"
    
    if failed:
        report += f"""
FAILED ANALYSES SUMMARY:
{'-'*40}
"""
        for result in failed:
            report += f"• {result['project_name']}: {result.get('error', 'Unknown error')}\n"
    
    report += f"""

RECOMMENDATIONS:
{'-'*40}
"""
    
    if successful:
        low_coverage = [r for r in successful if r['final_coverage'] < 80]
        if low_coverage:
            report += f"• Focus on improving coverage for {len(low_coverage)} projects below target\n"
        
        high_iteration = [r for r in successful if r['iterations_completed'] >= 3]
        if high_iteration:
            report += f"• {len(high_iteration)} projects reached maximum iterations - consider manual test addition\n"
        
        if len(high_coverage) > 0:
            report += f"• {len(high_coverage)} projects achieved excellent coverage - use as templates\n"
    
    if failed:
        report += f"• Investigate {len(failed)} failed analyses for project structure or dependency issues\n"
    
    report += f"""

TOOLS USED:
• LCOV/GCOV for coverage measurement
• Google Test (gtest) for unit testing framework
• Ollama LLM for intelligent test generation
• CMake for build system integration

{'='*80}
Report generated by C++ Micro Agent - Multi-Project Coverage Analysis System
For technical support, review the detailed logs in each project's output directory.
{'='*80}
"""
    
    return report

def generate_executive_summary(results):
    """Generate executive summary"""
    
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    summary = f"""C++ MICRO AGENT - EXECUTIVE SUMMARY
{'='*50}
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW:
  📊 Total Projects Analyzed: {len(results)}
  ✅ Successful Analyses: {len(successful)}
  ❌ Failed Analyses: {len(failed)}
  📁 Total Source Files: {sum(r.get('source_files_count', 0) for r in results):,}

"""
    
    if successful:
        avg_coverage = sum(r['final_coverage'] for r in successful) / len(successful)
        high_coverage = [r for r in successful if r.get('target_achieved', False)]
        
        summary += f"""COVERAGE RESULTS:
  📈 Average Coverage: {avg_coverage:.1f}%
  🎯 Target Achievement: {len(high_coverage)}/{len(successful)} projects ({len(high_coverage)/len(successful)*100:.1f}%)
  🏆 Best Performance: {max(r['final_coverage'] for r in successful):.1f}%
  📉 Lowest Coverage: {min(r['final_coverage'] for r in successful):.1f}%

TOP PERFORMERS:
"""
        successful_sorted = sorted(successful, key=lambda x: x['final_coverage'], reverse=True)
        for i, result in enumerate(successful_sorted[:3], 1):
            status = "🎯" if result['target_achieved'] else "📊"
            summary += f"  {i}. {status} {result['project_name']} - {result['final_coverage']:.1f}%\n"
    
    summary += f"""
ANALYSIS METHOD:
  🤖 LLM-powered unit test generation
  🔄 Iterative coverage improvement
  📊 Real-time coverage measurement
  🎯 Target-driven optimization

DELIVERABLES:
  📄 Individual project coverage reports
  🧪 Generated unit test suites
  📊 Interactive HTML coverage reports
  📋 Consolidated analysis (this report)
"""
    
    return summary

def print_console_summary(results):
    """Print summary to console"""
    
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    print(f"\n🏆 CONSOLIDATED ANALYSIS COMPLETE!")
    print("=" * 45)
    print(f"📊 Total Projects: {len(results)}")
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        avg_coverage = sum(r['final_coverage'] for r in successful) / len(successful)
        high_coverage = [r for r in successful if r.get('target_achieved', False)]
        
        print(f"📈 Average Coverage: {avg_coverage:.1f}%")
        print(f"🎯 Target Achieved: {len(high_coverage)}/{len(successful)} projects")
        
        print(f"\n🏆 TOP PERFORMERS:")
        successful_sorted = sorted(successful, key=lambda x: x['final_coverage'], reverse=True)
        for i, result in enumerate(successful_sorted, 1):
            status = "🎯" if result['target_achieved'] else "📊"
            print(f"   {i}. {status} {result['project_name']:<20} {result['final_coverage']:6.1f}%")

def main():
    json_file, text_file, summary_file = create_demo_consolidated_report()
    
    print(f"\n💡 USE THESE REPORTS TO:")
    print("   • Compare coverage across multiple C++ projects")
    print("   • Identify best practices from high-coverage projects")
    print("   • Track coverage improvement over time")
    print("   • Generate stakeholder summaries")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())