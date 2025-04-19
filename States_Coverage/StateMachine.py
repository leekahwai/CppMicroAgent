from States_Coverage.StateInit import StateInit
from States_Coverage.StateEnd import StateEnd
from States_Coverage.StateParseCMake import StateParseCMake
from States_Coverage.StateIterateSourceFiles import StateIterateSourceFiles
import ConfigReader
from flow_manager import flow

class StateMachine:
    def __init__(self, input_data):
        # Set initial state
        
        self.states = {
            "init": StateInit(),
            "end": StateEnd(),
            "StateParseCMake":StateParseCMake(),
            "StateIterateSourceFiles":StateIterateSourceFiles()
        }
        self.current_state = "init"
        self.input_data = input_data
        ConfigReader.ConfigReader()
    
    def run(self):
        flow.set_initial("init")
        while self.current_state != "end":
            proceed, input_data = self.states[self.current_state].run(self.input_data)
            self.input_data = input_data
            
            if self.current_state == "init":
                self.current_state = "StateParseCMake" if proceed else "end"
            elif self.current_state == "StateParseCMake":
                self.current_state = "StateIterateSourceFiles" if proceed else "end"
            elif self.current_state == "StateIterateSourceFiles" :
                self.current_state = "end" if proceed else "end"
            elif self.current_state == "end":
                proceed, input_data = self.states[self.current_state].run(self.input_data)
                break
        flow.set_initial("end")
