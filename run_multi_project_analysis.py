#!/usr/bin/env python3
"""
Multi-Project Coverage Analysis Runner
Analyzes multiple C++ projects and creates consolidated reports
"""
import os
import sys
import json
import datetime
import shutil
from States.Query import Query
from States_Coverage.StateMachine import StateMachine
from ConfigReader import ConfigReader
from OutputManager import OutputManager

class MultiProjectCoverageRunner:
    def __init__(self):
        self.configReader = ConfigReader()
        self.results = []
        self.base_dir = "/workspaces/CppMicroAgent"
        
    def find_cmake_projects(self):
        """Find viable CMake projects in TestProjects directory"""
        projects = []
        test_projects_dir = os.path.join(self.base_dir, "TestProjects")
        
        print("🔍 Scanning for CMake projects...")
        
        # Define project configurations
        project_configs = [
            {
                "name": "SampleApplication",
                "path": "TestProjects/SampleApplication/SampleApp",
                "description": "Original sample application with interfaces"
            },
            {
                "name": "fmt-library", 
                "path": "TestProjects/fmt-library",
                "description": "Modern C++ string formatting library"
            },
            {
                "name": "nlohmann-json",
                "path": "TestProjects/nlohmann-json", 
                "description": "JSON for Modern C++ library"
            },
            {
                "name": "spdlog-library",
                "path": "TestProjects/spdlog-library",
                "description": "Fast C++ logging library"
            },
            {
                "name": "catch2-library",
                "path": "TestProjects/catch2-library",
                "description": "Modern C++ unit testing framework"
            }
        ]
        
        for config in project_configs:
            full_path = os.path.join(self.base_dir, config["path"])
            cmake_file = os.path.join(full_path, "CMakeLists.txt")
            
            if os.path.exists(cmake_file):
                # Count source files
                src_count = 0
                for root, dirs, files in os.walk(full_path):
                    src_count += len([f for f in files if f.endswith(('.cpp', '.cc', '.cxx'))])
                
                if src_count > 0:  # Only include projects with source files
                    config["source_files"] = src_count
                    config["full_path"] = full_path
                    projects.append(config)
                    print(f"   ✅ {config['name']}: {src_count} source files")
                else:
                    print(f"   ⚠️  {config['name']}: No source files found")
            else:
                print(f"   ❌ {config['name']}: No CMakeLists.txt")
        
        return projects
    
    def analyze_project(self, project_config):
        """Analyze a single project and return results"""
        
        print(f"\n{'='*60}")
        print(f"🔄 ANALYZING: {project_config['name']}")
        print(f"📁 Path: {project_config['path']}")
        print(f"📝 Description: {project_config['description']}")
        print(f"📄 Source Files: {project_config['source_files']}")
        print(f"{'='*60}")
        
        # Update configuration to point to this project
        original_path = self.configReader.get_default_project_path()
        
        # Temporarily update the config in memory (don't modify file)
        self.configReader.default_project_path = project_config['path']
        
        try:
            # Create query and run analysis
            query = Query(project_config['full_path'])
            sm = StateMachine(query)
            sm.run()
            
            # Collect results
            iteration_results = query.get_coverage_iteration_results()
            coverage_data = query.get_coverage_data()
            
            result = {
                "project_name": project_config['name'],
                "project_path": project_config['path'],
                "description": project_config['description'], 
                "source_files_count": project_config['source_files'],
                "analysis_time": datetime.datetime.now().isoformat(),
                "success": True,
                "coverage_data": coverage_data,
                "iteration_results": iteration_results
            }
            
            if iteration_results:
                result.update({
                    "final_coverage": iteration_results.get("final_coverage", 0.0),
                    "iterations_completed": iteration_results.get("iterations_completed", 0),
                    "target_achieved": iteration_results.get("target_achieved", False),
                    "target_coverage": iteration_results.get("target_coverage", 80.0)
                })
            
            print(f"✅ Analysis completed for {project_config['name']}")
            if iteration_results:
                print(f"📊 Coverage: {result.get('final_coverage', 0):.1f}%")
                print(f"🔄 Iterations: {result.get('iterations_completed', 0)}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error analyzing {project_config['name']}: {e}")
            return {
                "project_name": project_config['name'],
                "project_path": project_config['path'],
                "description": project_config['description'],
                "source_files_count": project_config['source_files'],
                "analysis_time": datetime.datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }
        finally:
            # Restore original configuration
            self.configReader.default_project_path = original_path
    
    def run_multi_project_analysis(self):
        """Run analysis on multiple projects"""
        
        print("🚀 C++ MICRO AGENT - MULTI-PROJECT COVERAGE ANALYSIS")
        print("=" * 65)
        
        # Find projects
        projects = self.find_cmake_projects()
        
        if not projects:
            print("❌ No viable CMake projects found!")
            return False
        
        print(f"\n📋 Found {len(projects)} projects to analyze:")
        for project in projects:
            print(f"   • {project['name']} ({project['source_files']} source files)")
        
        print(f"\n🔄 Starting analysis of {len(projects)} projects...")
        print(f"🎯 Target Coverage: {self.configReader.get_coverage_target()}%")
        print(f"🔄 Max Iterations: {self.configReader.get_max_iterations()}")
        
        # Analyze each project
        for i, project in enumerate(projects, 1):
            print(f"\n[{i}/{len(projects)}] Processing {project['name']}...")
            
            result = self.analyze_project(project)
            self.results.append(result)
            
            # Brief status
            if result['success']:
                coverage = result.get('final_coverage', 0)
                status = "✅ SUCCESS" if result.get('target_achieved', False) else f"🔄 PARTIAL ({coverage:.1f}%)"
                print(f"   {status}")
            else:
                print(f"   ❌ FAILED")
        
        # Generate consolidated report
        self.generate_consolidated_report()
        
        return True
    
    def generate_consolidated_report(self):
        """Generate a consolidated report of all project analyses"""
        
        print(f"\n📊 GENERATING CONSOLIDATED REPORT...")
        
        # Create output directory for consolidated reports
        consolidated_dir = os.path.join(self.configReader.get_output_directory(), "ConsolidatedReports")
        os.makedirs(consolidated_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate JSON report
        json_report_file = os.path.join(consolidated_dir, f"multi_project_analysis_{timestamp}.json")
        with open(json_report_file, 'w') as f:
            json.dump({
                "analysis_metadata": {
                    "timestamp": timestamp,
                    "total_projects": len(self.results),
                    "successful_analyses": len([r for r in self.results if r['success']]),
                    "configuration": {
                        "coverage_target": self.configReader.get_coverage_target(),
                        "max_iterations": self.configReader.get_max_iterations()
                    }
                },
                "project_results": self.results
            }, f, indent=2)
        
        # Generate text report
        text_report_file = os.path.join(consolidated_dir, f"multi_project_coverage_report_{timestamp}.txt")
        with open(text_report_file, 'w') as f:
            f.write(self._generate_text_report())
        
        # Generate summary report
        summary_file = os.path.join(consolidated_dir, f"coverage_summary_{timestamp}.txt")
        with open(summary_file, 'w') as f:
            f.write(self._generate_summary_report())
        
        print(f"📄 Reports generated:")
        print(f"   📊 JSON Data: {json_report_file}")
        print(f"   📝 Text Report: {text_report_file}")
        print(f"   📋 Summary: {summary_file}")
        
        # Print summary to console
        print(f"\n🏆 MULTI-PROJECT ANALYSIS COMPLETE!")
        print("=" * 50)
        self._print_console_summary()
    
    def _generate_text_report(self):
        """Generate detailed text report"""
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
{'='*80}
               C++ MICRO AGENT - MULTI-PROJECT COVERAGE REPORT
{'='*80}

Generated: {timestamp}
Total Projects Analyzed: {len(self.results)}
Successful Analyses: {len([r for r in self.results if r['success']])}
Configuration:
  - Coverage Target: {self.configReader.get_coverage_target()}%
  - Max Iterations: {self.configReader.get_max_iterations()}

{'='*80}

"""
        
        for i, result in enumerate(self.results, 1):
            report += f"""
PROJECT {i}: {result['project_name']}
{'-'*60}
Path: {result['project_path']}
Description: {result['description']}
Source Files: {result['source_files_count']}
Analysis Time: {result['analysis_time']}
"""
            
            if result['success']:
                final_coverage = result.get('final_coverage', 0)
                iterations = result.get('iterations_completed', 0)
                target_achieved = result.get('target_achieved', False)
                
                status = "SUCCESS ✅" if target_achieved else "PARTIAL 🔄"
                
                report += f"""
Status: {status}
Final Coverage: {final_coverage:.1f}%
Iterations Completed: {iterations}
Target Achieved: {'Yes' if target_achieved else 'No'}

Coverage Breakdown:
"""
                coverage_data = result.get('coverage_data', {})
                if coverage_data:
                    lines_covered = coverage_data.get('lines_covered', 0)
                    lines_total = coverage_data.get('lines_total', 0)
                    functions_covered = coverage_data.get('functions_covered', 0)
                    functions_total = coverage_data.get('functions_total', 0)
                    
                    report += f"  - Lines: {lines_covered}/{lines_total}\n"
                    report += f"  - Functions: {functions_covered}/{functions_total}\n"
            else:
                report += f"""
Status: FAILED ❌
Error: {result.get('error', 'Unknown error')}
"""
            
            report += "\n"
        
        return report
    
    def _generate_summary_report(self):
        """Generate concise summary report"""
        
        successful = [r for r in self.results if r['success']]
        failed = [r for r in self.results if not r['success']]
        
        if successful:
            avg_coverage = sum(r.get('final_coverage', 0) for r in successful) / len(successful)
            high_coverage = [r for r in successful if r.get('target_achieved', False)]
        else:
            avg_coverage = 0
            high_coverage = []
        
        summary = f"""C++ MICRO AGENT - COVERAGE ANALYSIS SUMMARY
{'='*50}

OVERVIEW:
  📊 Total Projects: {len(self.results)}
  ✅ Successful: {len(successful)}
  ❌ Failed: {len(failed)}
  🎯 Target Achieved: {len(high_coverage)}

COVERAGE STATISTICS:
  📈 Average Coverage: {avg_coverage:.1f}%
  🎯 Target Coverage: {self.configReader.get_coverage_target()}%

PROJECT RANKINGS (by coverage):
"""
        
        # Sort successful projects by coverage
        successful_sorted = sorted(successful, key=lambda x: x.get('final_coverage', 0), reverse=True)
        
        for i, result in enumerate(successful_sorted, 1):
            coverage = result.get('final_coverage', 0)
            status = "🏆" if result.get('target_achieved', False) else "📊"
            summary += f"  {i:2d}. {status} {result['project_name']:<20} {coverage:6.1f}%\n"
        
        if failed:
            summary += f"\nFAILED ANALYSES:\n"
            for result in failed:
                summary += f"  ❌ {result['project_name']:<20} {result.get('error', 'Unknown error')}\n"
        
        return summary
    
    def _print_console_summary(self):
        """Print summary to console"""
        
        successful = [r for r in self.results if r['success']]
        failed = [r for r in self.results if not r['success']]
        high_coverage = [r for r in successful if r.get('target_achieved', False)]
        
        print(f"📊 Total Projects: {len(self.results)}")
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"🎯 Target Achieved: {len(high_coverage)}")
        
        if successful:
            avg_coverage = sum(r.get('final_coverage', 0) for r in successful) / len(successful)
            print(f"📈 Average Coverage: {avg_coverage:.1f}%")

def main():
    runner = MultiProjectCoverageRunner()
    success = runner.run_multi_project_analysis()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())