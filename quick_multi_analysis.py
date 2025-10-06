#!/usr/bin/env python3
"""
Quick Multi-Project Coverage Analysis Runner (Smaller projects first)
"""
import os
import sys
import datetime
from States.Query import Query
from States_Coverage.StateMachine import StateMachine
from ConfigReader import ConfigReader

def analyze_small_projects():
    """Analyze a few smaller projects for demonstration"""
    
    print("🚀 C++ MICRO AGENT - QUICK MULTI-PROJECT ANALYSIS")
    print("=" * 60)
    
    # Select smaller projects for testing
    projects = [
        {
            "name": "SampleApplication",
            "path": "TestProjects/SampleApplication/SampleApp",
            "description": "Original sample application"
        },
        {
            "name": "fmt-library-subset",
            "path": "TestProjects/fmt-library", 
            "description": "Modern C++ formatting library"
        }
    ]
    
    configReader = ConfigReader()
    results = []
    
    print(f"📋 Analyzing {len(projects)} projects:")
    for project in projects:
        print(f"   • {project['name']}")
    
    # Analyze each project
    for i, project in enumerate(projects, 1):
        print(f"\n{'='*50}")
        print(f"[{i}/{len(projects)}] ANALYZING: {project['name']}")
        print(f"{'='*50}")
        
        try:
            # Get full path
            base_dir = "/workspaces/CppMicroAgent"
            full_path = os.path.join(base_dir, project["path"])
            
            # Create query and run analysis
            query = Query(full_path)
            sm = StateMachine(query)
            sm.run()
            
            # Collect results
            iteration_results = query.get_coverage_iteration_results()
            coverage_data = query.get_coverage_data()
            
            result = {
                "project_name": project['name'],
                "success": True,
                "final_coverage": iteration_results.get("final_coverage", 0.0) if iteration_results else 0.0,
                "iterations": iteration_results.get("iterations_completed", 0) if iteration_results else 0,
                "target_achieved": iteration_results.get("target_achieved", False) if iteration_results else False
            }
            
            results.append(result)
            
            print(f"✅ {project['name']} completed!")
            print(f"   📊 Coverage: {result['final_coverage']:.1f}%")
            print(f"   🔄 Iterations: {result['iterations']}")
            print(f"   🎯 Target: {'✅ Achieved' if result['target_achieved'] else '❌ Not achieved'}")
            
        except Exception as e:
            print(f"❌ Error analyzing {project['name']}: {e}")
            results.append({
                "project_name": project['name'],
                "success": False,
                "error": str(e)
            })
    
    # Generate quick report
    print(f"\n{'='*60}")
    print("📊 ANALYSIS SUMMARY")
    print(f"{'='*60}")
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        avg_coverage = sum(r['final_coverage'] for r in successful) / len(successful)
        print(f"📈 Average Coverage: {avg_coverage:.1f}%")
        
        print(f"\n📋 PROJECT RESULTS:")
        for result in successful:
            status = "🎯" if result['target_achieved'] else "📊"
            print(f"   {status} {result['project_name']:<20} {result['final_coverage']:6.1f}%")
    
    # Save quick report
    consolidated_dir = os.path.join(configReader.get_output_directory(), "ConsolidatedReports")
    os.makedirs(consolidated_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(consolidated_dir, f"quick_analysis_{timestamp}.txt")
    
    with open(report_file, 'w') as f:
        f.write(f"C++ MICRO AGENT - QUICK ANALYSIS REPORT\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*50}\n\n")
        
        for result in results:
            f.write(f"Project: {result['project_name']}\n")
            if result['success']:
                f.write(f"Coverage: {result['final_coverage']:.1f}%\n")
                f.write(f"Iterations: {result['iterations']}\n")
                f.write(f"Target Achieved: {'Yes' if result['target_achieved'] else 'No'}\n")
            else:
                f.write(f"Status: Failed - {result.get('error', 'Unknown error')}\n")
            f.write("\n")
    
    print(f"\n📄 Quick report saved to: {report_file}")
    return len(successful) > 0

if __name__ == "__main__":
    success = analyze_small_projects()
    sys.exit(0 if success else 1)