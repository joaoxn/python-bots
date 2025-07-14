import os

import keyboard
import _thread
import threading
import time

from osu_reader import *

# Constants
KEYS = ["A", "S", 75, 76]

def play_tap_note(column):
    keyboard.send(KEYS[column])

def play_hold_note(column, duration):
    keyboard.press(KEYS[column])
    time.sleep(duration)
    keyboard.release(KEYS[column])

def main():
    path = input("Enter a .osu file's path: ")
    if not path.endswith(".osu"):
        path += ".osu"

    if not os.path.exists(path):
        print("File not found. Using default.osu instead.")
        path = "default.osu"

    print("Loading map...")
    osu_map = read(path)
    print("Map loaded")
    
    print("Press F6 to start playing!")
    keyboard.wait("F6")
    print("Playing...")
    
    # Record start time when F6 is pressed
    start_time = time.time() - osu_map[0].time
    
    # Create a list to keep track of all threads
    note_threads = []
    
    # Process each note
    for obj in osu_map:
        # Calculate when this note should be played
        time_to_wait = obj.time - (time.time() - start_time)
        
        # If we need to wait, do so
        if time_to_wait > 0:
            time.sleep(time_to_wait)
            
        # Create and start thread based on note type
        if obj.type == HitObjectType.TAP:
            # print(f"{obj.time:.2f}s - Tap {obj.column}")
            play_tap_note(obj.column)

        else:  # HOLD note
            # print(f"{obj.time:.2f}s - Hold {obj.column} for {obj.endTime - obj.time:.2f}s")
            duration = obj.endTime - obj.time
            thread = threading.Thread(
                target=play_hold_note,
                args=(obj.column, duration)
            )
            
            thread.start()
            note_threads.append(thread)
        
        # Optional: Clean up completed threads
        # note_threads = [t for t in note_threads if t.is_alive()]
    
    # Wait for all threads to complete
    for thread in note_threads:
        thread.join()

    print("Song finished!")

if __name__ == "__main__":
    # Set up stop hotkey
    def stop_program():
        print("Stopping...")
        _thread.interrupt_main()
    
    print("Press Ctrl + F8 to stop")
    keyboard.add_hotkey("Ctrl+F8", stop_program)
    
    main()
