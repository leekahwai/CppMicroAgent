from flow_manager import flow

class StateEnd():
    def __init__(self):
        print("Initializing [States_Coverage::StateEnd]")

    def run(self, input_data):
        flow.transition("States_Coverage::end")
        print("[States_Coverage::StateEnd] Reached end state.")
        return False, None # Stop state machine

