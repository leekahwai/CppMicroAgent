# flow_manager.py

import threading
from graphviz import Digraph

class FlowManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.transitions = []
        self.current_state = None

    def set_initial(self, state_name):
        with self.lock:
            self.current_state = state_name
            self.transitions.append(("Start", state_name))  # Start is implicit

    def transition(self, new_state):
        with self.lock:
            if self.current_state is not None:
                self.transitions.append((self.current_state, new_state))
            else:
                self.transitions.append(("Start", new_state))  # fallback if not initialized
            self.current_state = new_state

    def generate_dot(self):
        with self.lock:
            dot = Digraph(comment="Runtime Flow")
            for from_state, to_state in self.transitions:
                dot.edge(from_state, to_state)
            if self.current_state:
                dot.node(self.current_state, fillcolor="yellow", style="filled,bold", color="red", fontcolor="black")
            return dot.source

# Singleton instance
flow = FlowManager()
