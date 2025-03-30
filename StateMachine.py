from States.StateInit import StateInit
from States.StateVerifyGenerateCodeQuery import StateVerifyGenerateCodeQuery
from States.StateGenerateCodeFromInput import StateGenerateCodeFromInput
from States.StateGenerateGTestCodeFromInput import StateGenerateGTestCodeFromInput
from States.StateEnd import StateEnd
from States.StateAttempCompile import StateAttempCompile
from States.StateVerifyFailedCompiledGTest import StateVerifyFailedCompiledGTest
import ConfigReader

class StateMachine:
    def __init__(self, input_data):
        self.states = {
            "init": StateInit(),
            "StateVerifyGenerateCodeQuery": StateVerifyGenerateCodeQuery(),
            "StateGenerateCodeFromInput": StateGenerateCodeFromInput(),
            "StateGenerateGTestCodeFromInput":StateGenerateGTestCodeFromInput(),
            "StateAttempCompile":StateAttempCompile(),
            "StateVerifyFailedCompiledGTest": StateVerifyFailedCompiledGTest(),
            "end": StateEnd()
        }
        self.current_state = "init"
        self.input_data = input_data
        ConfigReader.ConfigReader()
    
    def run(self):
        while self.current_state:
            proceed, input_data = self.states[self.current_state].run(self.input_data)
            self.input_data = input_data
            
            if self.current_state == "init":
                self.current_state = "StateVerifyGenerateCodeQuery" if proceed else "end"
            elif self.current_state == "StateVerifyGenerateCodeQuery":
                self.current_state = "StateGenerateCodeFromInput" if proceed else "end"
            elif self.current_state == "StateGenerateCodeFromInput":
                self.current_state = "StateGenerateGTestCodeFromInput" if proceed else "end"
            elif self.current_state == "StateGenerateGTestCodeFromInput":
                self.current_state = "StateAttempCompile" if proceed else "end"
            elif self.current_state == "StateAttempCompile" :
                self.current_state = "end" if proceed else "StateVerifyFailedCompiledGTest"
            elif self.current_state == "StateVerifyFailedCompiledGTest" :
                self.current_state = "StateGenerateCodeFromInput" if proceed else "StateGenerateGTestCodeFromInput"
            elif self.current_state == "end":
                break
