import keyboard

def quitTime():
    print("it's quittime!")

keyboard.add_hotkey("q", quitTime)


while True:
    x=1