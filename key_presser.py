import time
from pynput import Controller, Listener, Key

keyboard = Controller()

def on_press(key):
    if key.char == 'k':
        return False
    
listener = Listener(on_press=on_press)
listener.start()

while listener.running:
    keyboard.press(Key.f2)
    keyboard.release(Key.f2)
    time.sleep(6)

listener.join()