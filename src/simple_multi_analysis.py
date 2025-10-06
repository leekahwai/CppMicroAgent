#!/usr/bin/env python3
"""
Simple Multi-Project Coverage Analysis 
"""
import os
import sys
import datetime
import json

def run_project_analysis(project_name, project_path):
    """Run analysis on a single project"""
    
    print(f"🔄 Analyzing {project_name}...")
    
    # Update config file temporarily
    config_file = "CppMicroAgent.cfg"
    backup_file = f"{config_file}.backup"
    
    # Read current config
    with open(config_file, 'r') as f:
        content = f.read()
    
    # Backup current config
    with open(backup_file, 'w') as f:
        f.write(content)
    
    # Update config with new project path
    updated_content = content.replace(
        "default_project_path=TestProjects/SampleApplication/SampleApp",
        f"default_project_path={project_path}"
    )
    
    with open(config_file, 'w') as f:
        f.write(updated_content)
    
    try:
        # Run the coverage analysis
        import subprocess
        result = subprocess.run([
            "python3", "run_sample_coverage.py"
        ], capture_output=True, text=True, timeout=180)
        
        success = result.returncode == 0
        
        # Parse results from output
        coverage = 0.0
        iterations = 0
        target_achieved = False
        
        if success and result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if "Final Coverage:" in line:
                    try:
                        coverage = float(line.split(':')[1].strip().replace('%', ''))
                    except:
                        pass
                elif "Iterations:" in line:
                    try:
                        iterations = int(line.split(':')[1].strip())
                    except:
                        pass
                elif "Target Achieved:" in line:
                    target_achieved = "Yes" in line
        
        return {
            "project_name": project_name,
            "success": success,
            "coverage": coverage,
            "iterations": iterations,
            "target_achieved": target_achieved,
            "output": result.stdout if success else result.stderr
        }
        
    except Exception as e:
        return {
            "project_name": project_name,
            "success": False,
            "error": str(e)
        }
    finally:
        # Restore original config
        with open(backup_file, 'r') as f:
            original_content = f.read()
        with open(config_file, 'w') as f:
            f.write(original_content)
        os.remove(backup_file)

def main():
    print("🚀 C++ MICRO AGENT - SIMPLIFIED MULTI-PROJECT ANALYSIS")
    print("=" * 65)
    
    # Define projects to analyze
    projects = [
        {
            "name": "SampleApplication",
            "path": "TestProjects/SampleApplication/SampleApp"
        },
        {
            "name": "fmt-library",
            "path": "TestProjects/fmt-library"
        }
    ]
    
    results = []
    
    print(f"📋 Will analyze {len(projects)} projects:")
    for project in projects:
        full_path = os.path.join("/workspaces/CppMicroAgent", project["path"])
        if os.path.exists(os.path.join(full_path, "CMakeLists.txt")):
            print(f"   ✅ {project['name']}")
        else:
            print(f"   ❌ {project['name']} (CMakeLists.txt not found)")
    
    print()
    
    # Analyze each project
    for i, project in enumerate(projects, 1):
        print(f"\n[{i}/{len(projects)}] " + "="*40)
        
        result = run_project_analysis(project["name"], project["path"])
        results.append(result)
        
        if result["success"]:
            print(f"✅ {project['name']}: {result['coverage']:.1f}% coverage")
        else:
            print(f"❌ {project['name']}: Failed")
    
    # Generate consolidated report
    print(f"\n{'='*60}")
    print("📊 CONSOLIDATED RESULTS")
    print(f"{'='*60}")
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        avg_coverage = sum(r["coverage"] for r in successful) / len(successful)
        print(f"📈 Average Coverage: {avg_coverage:.1f}%")
        
        print(f"\n📋 PROJECT RANKINGS:")
        successful_sorted = sorted(successful, key=lambda x: x["coverage"], reverse=True)
        for i, result in enumerate(successful_sorted, 1):
            status = "🎯" if result["target_achieved"] else "📊"
            print(f"   {i}. {status} {result['project_name']:<20} {result['coverage']:6.1f}%")
    
    # Save consolidated report
    os.makedirs("output/ConsolidatedReports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON report
    json_file = f"output/ConsolidatedReports/multi_project_results_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "total_projects": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "average_coverage": sum(r["coverage"] for r in successful) / len(successful) if successful else 0,
            "results": results
        }, f, indent=2)
    
    # Text report
    text_file = f"output/ConsolidatedReports/multi_project_report_{timestamp}.txt"
    with open(text_file, 'w') as f:
        f.write(f"C++ MICRO AGENT - MULTI-PROJECT COVERAGE REPORT\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*60}\n\n")
        
        f.write(f"SUMMARY:\n")
        f.write(f"  Total Projects: {len(results)}\n")
        f.write(f"  Successful: {len(successful)}\n")
        f.write(f"  Failed: {len(failed)}\n")
        if successful:
            f.write(f"  Average Coverage: {avg_coverage:.1f}%\n")
        f.write(f"\n")
        
        f.write(f"DETAILED RESULTS:\n")
        f.write(f"{'-'*40}\n")
        for result in results:
            f.write(f"\nProject: {result['project_name']}\n")
            if result["success"]:
                f.write(f"  Coverage: {result['coverage']:.1f}%\n")
                f.write(f"  Iterations: {result['iterations']}\n")
                f.write(f"  Target Achieved: {'Yes' if result['target_achieved'] else 'No'}\n")
            else:
                f.write(f"  Status: Failed\n")
                f.write(f"  Error: {result.get('error', 'Unknown error')}\n")
    
    print(f"\n📄 Reports saved:")
    print(f"   📊 JSON: {json_file}")
    print(f"   📝 Text: {text_file}")
    
    return len(successful) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)