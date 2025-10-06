
from states_coverage.States_Function.StatesCreateMock import StatesCreateMock
from states_coverage.States_Function.StateEnd import StateEnd

import ConfigReader
from flow_manager import flow

class StateMachine:
    def __init__(self, input_data):
        # Set initial state
        
        self.states = {
            "StatesCreateMock":StatesCreateMock(),
            "end":StateEnd()
        }
        self.current_state = "StatesCreateMock"
        self.input_data = input_data
        ConfigReader.ConfigReader()
    
    def run(self):
        flow.set_initial("init")
        while self.current_state != "end":
            proceed, input_data = self.states[self.current_state].run(self.input_data)
            self.input_data = input_data
            
            if self.current_state == "StatesCreateMock":
                self.current_state = "end" if proceed else "end"
            elif self.current_state == "end":
                proceed, input_data = self.states[self.current_state].run(self.input_data)
                break
        flow.set_initial("end")
