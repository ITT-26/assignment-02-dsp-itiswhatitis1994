import audio_sample
import pyglet
from pyglet import window, shapes
import threading

WINDOW_HEIGHT= 800
WINDOW_WIDTH = 1200
PADDING = 20
COLOR = (181, 47, 208)
LOWEST_FREQ = 50
HIGHEST_FREQ = 800
RANGE = HIGHEST_FREQ-LOWEST_FREQ
MOVEMENTHEIGHT = WINDOW_HEIGHT - 2*PADDING
PIXEL_PER_FREQ = MOVEMENTHEIGHT/RANGE

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
player = shapes.Circle(PADDING, WINDOW_HEIGHT/2, 5, color=COLOR)

def checkFrequency():
    while True:
        current_frequency = audio_sample.getFrequency()
        print(current_frequency)
        if (current_frequency != 0):
            player.y = calculatePos(current_frequency)

def calculatePos (freq):
    new_frequency = freq-LOWEST_FREQ
    position = new_frequency*PIXEL_PER_FREQ
    return position

def startThread():
    threading.Thread(target=checkFrequency, daemon=True).start()

@win.event
def on_draw():
    win.clear()
    player.draw()

if __name__ == "__main__":
    startThread()
    pyglet.app.run()