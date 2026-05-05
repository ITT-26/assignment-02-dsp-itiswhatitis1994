import pyglet
from pyglet import window, shapes
import audio_sample
import threading
import time
from scipy.stats import linregress
import numpy
from pynput.keyboard import Key, Controller

WINDOW_HEIGHT= 800
WINDOW_WIDTH = 600
PADDING = 10
WIDTH = 300
HEIGHT = WINDOW_HEIGHT/5 - PADDING
SMALL_PADDING = PADDING/2
X_POS = (WINDOW_WIDTH - WIDTH)/2
Y_FACTOR = PADDING + HEIGHT
COLOR = (181, 47, 208)
ITEM_AMOUNT = 5
TRANSPARENT = 128
OPAQUE = 255
FREQ_MIN = 3
LIMIT = 20

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
selection = 2
frequencies = []
keyboard = Controller()

#creates class for a menu_item
class Menu_Item:
    def __init__(self, number):
        if (number == 0):
            self.y = SMALL_PADDING
        else:
            self.y = SMALL_PADDING + Y_FACTOR*number
        self.rect = shapes.Rectangle(X_POS, self.y, WIDTH, HEIGHT, COLOR)
        self.rect.opacity = TRANSPARENT
    
    #changes opacity dependant on if selected is true or false
    def isSelected(self, selected):
        if (selected):
            self.rect.opacity = OPAQUE
        else:
            self.rect.opacity = TRANSPARENT

menu_items = []

#creates the menu_items and sets item that is selected to opaque
def initApp():
    global ITEM_AMOUNT
    for i in range(int(ITEM_AMOUNT)):
        menu_items.append(Menu_Item(i))
        if (i == selection):
            menu_items[i].isSelected(True)

#calculates if frequencies get higher or lower
def calculateMovement():
    global frequencies
    x = numpy.arange(len(frequencies))
    slope, intercept, rvalue, pvalue, stderr = linregress(x, frequencies)
    #print(slope)
    return slope
        
#receives frequency from audio_sample 
# null_counter is used to check if break has been too long to detect changes from previous inputs and then clears the array if it reaches limit
# if frequencies-array is at least FREQ_MIN long, moveSelection gets started with information from calculateMovement
# longer whistle inputs lead to more than one jump. this is intended.
def checkFrequency():
    null_counter = 0
    while True:
        currentFrequency = audio_sample.getFrequency()
        if (currentFrequency != 0):
            frequencies.append(float(currentFrequency))
        else:
            null_counter += 1
            if (null_counter == LIMIT):
                null_counter = 0
                frequencies.clear()
        print(currentFrequency)
        print(frequencies)
        print("---")
        if (len(frequencies) >= FREQ_MIN):
            moveSelection(calculateMovement())
            null_counter = 0
        time.sleep(0.05) 

def moveSelection(change):
    global selection, frequencies
    if (change > 0):
        if (selection < ITEM_AMOUNT-1):
            new_selection = selection + 1
            menu_items[selection].isSelected(False)
            menu_items[new_selection].isSelected(True)
            selection = new_selection
            print(selection)
            print('up')
        keyboard.press(Key.up)
    elif (change < 0):
        if (selection > 0):
            new_selection = selection -1
            menu_items[selection].isSelected(False)
            menu_items[new_selection].isSelected(True)
            selection = new_selection
            print(selection)
            print('down')
        keyboard.press(Key.down)
    else:
        print(selection)
        print('Nothing was detected.')
    #print(frequencies)
    frequencies.clear()

def startThread():
    threading.Thread(target=checkFrequency, daemon=True).start()

@win.event
def on_draw():
    win.clear()
    for item in menu_items:
        item.rect.draw()

if __name__ == "__main__":
    startThread()
    initApp()
    pyglet.app.run()