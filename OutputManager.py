import os
import shutil
import datetime
from ConfigReader import ConfigReader

class OutputManager:
    """Manages output directory operations including cleanup and organization"""
    
    def __init__(self):
        self.configReader = ConfigReader()
        self.output_base_dir = self.configReader.get_output_directory()
        self.coverage_dir = os.path.join(self.output_base_dir, "UnitTestCoverage")
    
    def prepare_output_directory(self):
        """Prepare output directory for a new run"""
        
        print("[OutputManager] Preparing output directory...")
        
        # Check if we should clean the output directory
        if self.configReader.get_clean_output_before_run():
            print("[OutputManager] Cleaning previous output (configured in settings)")
            self._clean_output_directory()
        else:
            print("[OutputManager] Preserving previous output (configured in settings)")
            self._backup_previous_output()
        
        # Create fresh directory structure
        self._create_directory_structure()
        
        print(f"[OutputManager] Output directory ready: {self.coverage_dir}")
    
    def _clean_output_directory(self):
        """Remove existing output directory"""
        
        if os.path.exists(self.coverage_dir):
            try:
                shutil.rmtree(self.coverage_dir)
                print(f"[OutputManager] Removed existing output: {self.coverage_dir}")
            except Exception as e:
                print(f"[OutputManager] Warning: Could not remove {self.coverage_dir}: {e}")
    
    def _backup_previous_output(self):
        """Backup existing output directory with timestamp"""
        
        if os.path.exists(self.coverage_dir):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"{self.coverage_dir}_backup_{timestamp}"
            
            try:
                shutil.move(self.coverage_dir, backup_dir)
                print(f"[OutputManager] Backed up previous output to: {backup_dir}")
            except Exception as e:
                print(f"[OutputManager] Warning: Could not backup output: {e}")
    
    def _create_directory_structure(self):
        """Create the standard output directory structure"""
        
        directories = [
            self.coverage_dir,
            os.path.join(self.coverage_dir, "unit_tests"),
            os.path.join(self.coverage_dir, "coverage_data"),
            os.path.join(self.coverage_dir, "mocks")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"[OutputManager] Created directory: {directory}")
    
    def get_unit_tests_dir(self):
        """Get the unit tests directory path"""
        return os.path.join(self.coverage_dir, "unit_tests")
    
    def get_coverage_data_dir(self):
        """Get the coverage data directory path"""
        return os.path.join(self.coverage_dir, "coverage_data")
    
    def get_mocks_dir(self):
        """Get the mocks directory path"""
        return os.path.join(self.coverage_dir, "mocks")
    
    def get_main_output_dir(self):
        """Get the main coverage output directory path"""
        return self.coverage_dir
    
    def cleanup_temporary_files(self):
        """Clean up temporary files after analysis"""
        
        temp_patterns = [
            "*.tmp",
            "*.temp",
            "*~",
            ".DS_Store"
        ]
        
        for root, dirs, files in os.walk(self.coverage_dir):
            for pattern in temp_patterns:
                import fnmatch
                for file in files:
                    if fnmatch.fnmatch(file, pattern):
                        temp_file = os.path.join(root, file)
                        try:
                            os.remove(temp_file)
                            print(f"[OutputManager] Removed temporary file: {temp_file}")
                        except:
                            pass
    
    def get_output_summary(self):
        """Get a summary of generated output files"""
        
        summary = {
            "unit_tests": [],
            "coverage_files": [],
            "mock_files": [],
            "report_files": []
        }
        
        if os.path.exists(self.coverage_dir):
            # Unit tests
            unit_tests_dir = self.get_unit_tests_dir()
            if os.path.exists(unit_tests_dir):
                summary["unit_tests"] = [f for f in os.listdir(unit_tests_dir) if f.endswith('.cpp')]
            
            # Coverage files
            coverage_dir = self.get_coverage_data_dir()
            if os.path.exists(coverage_dir):
                for root, dirs, files in os.walk(coverage_dir):
                    summary["coverage_files"].extend([
                        os.path.relpath(os.path.join(root, f), coverage_dir) 
                        for f in files if f.endswith(('.info', '.html', '.gcov'))
                    ])
            
            # Mock files
            for root, dirs, files in os.walk(self.coverage_dir):
                if "unit_tests" not in root and "coverage_data" not in root:
                    summary["mock_files"].extend([
                        os.path.relpath(os.path.join(root, f), self.coverage_dir)
                        for f in files if f.endswith('.h')
                    ])
            
            # Report files
            summary["report_files"] = [
                f for f in os.listdir(self.coverage_dir) 
                if f.endswith(('.txt', '.log', '.md'))
            ]
        
        return summary