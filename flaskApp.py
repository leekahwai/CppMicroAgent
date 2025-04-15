# app.py

from flask import Flask, render_template
from flow_manager import flow
import threading

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/graph")
def graph():
    return flow.generate_dot(), 200, {'Content-Type': 'text/plain'}

def start():
    thread = threading.Thread(target=lambda: app.run(debug=False, use_reloader=False), daemon=True)
    thread.start()
