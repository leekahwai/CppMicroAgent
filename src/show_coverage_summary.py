#!/usr/bin/env python3
"""
Quick coverage summary viewer
"""
import os
import sys

def main():
    coverage_file = "output/UnitTestCoverage/coverage_data/coverage.info"
    html_dir = "output/UnitTestCoverage/coverage_data/lcov_html"
    
    print("📊 QUICK COVERAGE SUMMARY")
    print("=" * 40)
    
    if os.path.exists(coverage_file):
        print(f"✅ Coverage data file: {coverage_file}")
        
        # Parse coverage.info for quick summary
        try:
            with open(coverage_file, 'r') as f:
                content = f.read()
            
            lines_hit = content.count("LH:")
            lines_found = content.count("LF:")
            funcs_hit = content.count("FNH:")
            funcs_found = content.count("FNF:")
            
            print(f"📁 Source files analyzed: {content.count('SF:')}")
            print(f"📊 Lines coverage data points: {lines_hit}")
            print(f"🔧 Function coverage data points: {funcs_hit}")
            
        except Exception as e:
            print(f"⚠️  Error reading coverage file: {e}")
    else:
        print(f"❌ Coverage data not found: {coverage_file}")
    
    if os.path.exists(html_dir):
        print(f"✅ HTML report directory: {html_dir}")
        print(f"🌐 Open: file://{os.path.abspath(html_dir)}/index.html")
        
        # Count HTML files
        html_files = []
        for root, dirs, files in os.walk(html_dir):
            html_files.extend([f for f in files if f.endswith('.html')])
        
        print(f"📄 HTML files generated: {len(html_files)}")
    else:
        print(f"❌ HTML report not found: {html_dir}")
    
    print("\n" + "=" * 40)
    print("💡 To view full report:")
    print("   python3 show_coverage_report.py")

if __name__ == "__main__":
    main()