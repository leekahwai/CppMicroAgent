from flow_manager import flow

class StateEnd():
    def __init__(self):
        print("Initializing [StateEnd]")

    def run(self, input_data):
        flow.transition("end")
        print("[StateEnd] Reached end state.")
        return False, None # Stop state machine
