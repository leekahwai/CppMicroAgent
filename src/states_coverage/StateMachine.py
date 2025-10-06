from states_coverage.StateInit import StateInit
from states_coverage.StateEnd import StateEnd
from states_coverage.StateParseCMake import StateParseCMake
from states_coverage.StateIterateSourceFiles import StateIterateSourceFiles
from states_coverage.StateAggregateCoverageReports import StateAggregateCoverageReports
import ConfigReader
from flow_manager import flow
from OutputManager import OutputManager

class StateMachine:
    def __init__(self, input_data):
        # Set initial state
        
        self.states = {
            "init": StateInit(),
            "end": StateEnd(),
            "StateParseCMake": StateParseCMake(),
            "StateIterateSourceFiles": StateIterateSourceFiles(),
            "StateAggregateCoverageReports": StateAggregateCoverageReports()
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
                # After iterating all source files and functions (which now includes 
                # per-function test generation, compilation, and coverage measurement),
                # aggregate all the coverage reports
                self.current_state = "StateAggregateCoverageReports" if proceed else "end"
            elif self.current_state == "StateAggregateCoverageReports":
                self.current_state = "end" if proceed else "end"
            elif self.current_state == "end":
                proceed, input_data = self.states[self.current_state].run(self.input_data)
                break
        
        # Clean up temporary files after completion
        self.outputManager.cleanup_temporary_files()
        
        flow.set_initial("end")
