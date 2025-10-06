from states_coverage.StateInit import StateInit
from states_coverage.StateEnd import StateEnd
from states_coverage.StateParseCMake import StateParseCMake
from states_coverage.StateIterateSourceFiles import StateIterateSourceFiles
from states_coverage.StateCompileAndMeasureCoverage import StateCompileAndMeasureCoverage
from states_coverage.StateGenerateUnitTests import StateGenerateUnitTests
from states_coverage.StateAdvancedCoverageImprovement import StateAdvancedCoverageImprovement
from states_coverage.StateGenerateCoverageReport import StateGenerateCoverageReport
import ConfigReader
from flow_manager import flow
from OutputManager import OutputManager

class StateMachine:
    def __init__(self, input_data):
        # Set initial state
        
        self.states = {
            "init": StateInit(),
            "end": StateEnd(),
            "StateParseCMake":StateParseCMake(),
            "StateIterateSourceFiles":StateIterateSourceFiles(),
            "StateCompileAndMeasureCoverage":StateCompileAndMeasureCoverage(),
            "StateGenerateUnitTests":StateGenerateUnitTests(),
            "StateAdvancedCoverageImprovement":StateAdvancedCoverageImprovement(),
            "StateGenerateCoverageReport":StateGenerateCoverageReport()
        }
        self.current_state = "init"
        self.input_data = input_data
        self.configReader = ConfigReader.ConfigReader()
        self.outputManager = OutputManager()
    
    def run(self):
        flow.set_initial("init")
        
        # Prepare output directory before starting
        self.outputManager.prepare_output_directory()
        
        while self.current_state != "end":
            proceed, input_data = self.states[self.current_state].run(self.input_data)
            self.input_data = input_data
            
            if self.current_state == "init":
                self.current_state = "StateParseCMake" if proceed else "end"
            elif self.current_state == "StateParseCMake":
                self.current_state = "StateIterateSourceFiles" if proceed else "end"
            elif self.current_state == "StateIterateSourceFiles":
                self.current_state = "StateCompileAndMeasureCoverage" if proceed else "end"
            elif self.current_state == "StateCompileAndMeasureCoverage":
                self.current_state = "StateGenerateUnitTests" if proceed else "end"
            elif self.current_state == "StateGenerateUnitTests":
                self.current_state = "StateAdvancedCoverageImprovement" if proceed else "end"
            elif self.current_state == "StateAdvancedCoverageImprovement":
                self.current_state = "StateGenerateCoverageReport" if proceed else "end"
            elif self.current_state == "StateGenerateCoverageReport":
                self.current_state = "end" if proceed else "end"
            elif self.current_state == "end":
                proceed, input_data = self.states[self.current_state].run(self.input_data)
                break
        
        # Clean up temporary files after completion
        self.outputManager.cleanup_temporary_files()
        
        flow.set_initial("end")
