from ...flow_manager import flow

class StateEnd():
    def __init__(self):
        print("Initializing [states_coverage::StateEnd]")

    def run(self, input_data):
        flow.transition("states_coverage::end")
        print("[states_coverage::StateEnd] Reached end state.")
        return False, None # Stop state machine

