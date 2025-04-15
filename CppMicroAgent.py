import sys
import threading
import time
from States.StateMachine import StateMachine
from States.Query import Query
import flaskApp


def animate(stop_event):
    icon_frames = [ "🟢 LKW  ", "🟡 NWBNB", "🟠 LKW  ", "🔴 NWBNB", "🟠 LKW  ", "🟡 NWBNB"]  # A simple cycling icon
    index = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rListening: {icon_frames[index]} ")  # Overwrites the same line
        sys.stdout.flush()
        index = (index + 1) % len(icon_frames)
        time.sleep(0.2)

def listen_for_input(stop_event):
    try:
        print("\n")  # Ensure input appears on a new line
        stop_event.set()  # Temporarily stop animation while user types
            

        print ("Select the following choices:")
        print ("1. Generate code from input")
        print ("2. Generate unit tests from folder")
        my_input = input ("Enter your choice (1 or 2): ")
        if my_input == "1":
            user_input = input(" Key in your code generation query > ")  # User input prompt
            print(f"\nYou entered: {user_input}\n")  # Ensure input is visible
            query = Query(user_input)
            
            sm = StateMachine(query)
            sm.run()
        elif my_input == "2":
            print("You chose option 2")
        else:
            print("Invalid choice.")

        stop_event.clear()  # Resume animation
           
        
            
        

    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        stop_event.set()
        sys.exit(0)

if __name__ == "__main__":
    stop_event = threading.Event()
    
    # Start animation in a separate thread
    animation_thread = threading.Thread(target=animate, args=(stop_event,), daemon=True)
    animation_thread.start()
    
    # Give some time for animation to be visible before input appears
    flaskApp.start()
     
    time.sleep(1.0)
    # Start listening for input
    listen_for_input(stop_event)
