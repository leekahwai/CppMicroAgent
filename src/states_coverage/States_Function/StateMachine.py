
from .StatesCreateMock import StatesCreateMock
from .StateGenerateFunctionTest import StateGenerateFunctionTest
from .StateCompileFunctionTest import StateCompileFunctionTest
from .StateMeasureFunctionCoverage import StateMeasureFunctionCoverage
from .StateEnd import StateEnd

from ...ConfigReader import ConfigReader
from ...flow_manager import flow

class StateMachine:
    def __init__(self, input_data):
        # Set initial state
        
        self.states = {
            "StatesCreateMock": StatesCreateMock(),
            "StateGenerateFunctionTest": StateGenerateFunctionTest(),
            "StateCompileFunctionTest": StateCompileFunctionTest(),
            "StateMeasureFunctionCoverage": StateMeasureFunctionCoverage(),
            "end": StateEnd()
        }
        self.current_state = "StatesCreateMock"
        self.input_data = input_data
        self.configReader = ConfigReader()
    
    def run(self):
        flow.set_initial("init")
        while self.current_state != "end":
            proceed, input_data = self.states[self.current_state].run(self.input_data)
            self.input_data = input_data
            
            if self.current_state == "StatesCreateMock":
                # After creating mocks, generate the unit test
                self.current_state = "StateGenerateFunctionTest" if proceed else "end"
            elif self.current_state == "StateGenerateFunctionTest":
                # After generating test, try to compile it
                self.current_state = "StateCompileFunctionTest" if proceed else "end"
            elif self.current_state == "StateCompileFunctionTest":
                # After successful compilation, measure coverage
                self.current_state = "StateMeasureFunctionCoverage" if proceed else "end"
            elif self.current_state == "StateMeasureFunctionCoverage":
                # After coverage measurement, we're done
                self.current_state = "end" if proceed else "end"
            elif self.current_state == "end":
                proceed, input_data = self.states[self.current_state].run(self.input_data)
                break
        flow.set_initial("end")
