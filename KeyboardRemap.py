#UI libraries
from PyQt6.QtWidgets import *
import tkinter as tk
from tkinter import * 
from tkinter import messagebox
#Keyboard manipulation libraries
import time#for various debugging purposes
import evdev#for reading input and preventing that input from getting to the device
import uinput#for sending our processed inputs to the device
from evdev import categorize
#file saving libraries
import pickle
#text editing libraryies for our UI
import re
#to run our practice and stop the program, we need the remapping to occur in another thread. 
import threading
#we need the ability to shut down the whole program afterwards, otherwise our remapping thread would continue
import sys

#default key layer
layer = -1
#to find what device we wanted, in this case the keyboard, we used the command "sudo evtest"
device = evdev.InputDevice('/dev/input/event4')
print(device.read_loop())
virtual = uinput.Device([uinput.KEY_A, uinput.KEY_B, uinput.KEY_C, uinput.KEY_D, uinput.KEY_E,
    uinput.KEY_F, uinput.KEY_G, uinput.KEY_H, uinput.KEY_I, uinput.KEY_J,
    uinput.KEY_K, uinput.KEY_L, uinput.KEY_M, uinput.KEY_N, uinput.KEY_O,
    uinput.KEY_P, uinput.KEY_Q, uinput.KEY_R, uinput.KEY_S, uinput.KEY_T,
    uinput.KEY_U, uinput.KEY_V, uinput.KEY_W, uinput.KEY_X, uinput.KEY_Y,
    uinput.KEY_Z,

    uinput.KEY_1, uinput.KEY_2, uinput.KEY_3, uinput.KEY_4, uinput.KEY_5,
    uinput.KEY_6, uinput.KEY_7, uinput.KEY_8, uinput.KEY_9, uinput.KEY_0,

    uinput.KEY_ENTER, uinput.KEY_ESC, uinput.KEY_BACKSPACE, uinput.KEY_TAB,
    uinput.KEY_SPACE, uinput.KEY_MINUS, uinput.KEY_EQUAL, uinput.KEY_LEFTBRACE,
    uinput.KEY_RIGHTBRACE, uinput.KEY_BACKSLASH, uinput.KEY_SEMICOLON,
    uinput.KEY_APOSTROPHE, uinput.KEY_GRAVE, uinput.KEY_COMMA, uinput.KEY_DOT,
    uinput.KEY_SLASH, uinput.KEY_CAPSLOCK,

    uinput.KEY_LEFTSHIFT, uinput.KEY_RIGHTSHIFT, uinput.KEY_LEFTCTRL,
    uinput.KEY_RIGHTCTRL, uinput.KEY_LEFTALT, uinput.KEY_RIGHTALT,
    uinput.KEY_LEFTMETA, uinput.KEY_FN,

    uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT,])
#prevent the keypress from going to the computer (yet)
nextKeyBeingUsed = False
def getNextKey():
    global nextKeyBeingUsed
    if (nextKeyBeingUsed == False):
        #clear the que first
        nextKeyBeingUsed = True
        while True:
            event = device.read_one()
            if event is None:
                break

        print("No")
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                keyEvent = evdev.categorize(event)
                if (keyEvent.keystate == keyEvent.key_down):
                    nextKeyBeingUsed = False
                    return keyEvent.keycode
            
    


root = Tk()
root.geometry("1300x600")#This represents the default window size, NOT the mandatory window size
root.title("Keyboard Remapper UI")
def onClose():
    print("At next keypress, the program will end")
    root.destroy()
    stopper(Event)
    quit()
    sys.exit()
root.protocol("WM_DELETE_WINDOW", onClose)

def setCursor(event):
    event.widget.config(cursor="hand2")
def resetCursor(event):
    event.widget.config(cursor="")


#Caption
firstCaption = Frame(root, bg="white", width=500, height=100, padx=10, pady=10, borderwidth=2, relief="solid")
firstCaption.pack(pady=10)

#Text goes in the caption
title = Label(firstCaption, text="Accessibility Keymap Editor", width=23, bd=10, bg="white", font=("Helvetica", 20))
title.pack()

#Make a separate frame for our keyboard
keyFrame = Frame(root, bg="white", width=1100, height=500, padx=10, pady=10, borderwidth=2, relief="solid")
keyFrame.pack(pady=10)

#Caption
secondCaption = Frame(root, bg="white", width=500, height=100, padx=5, pady=5, borderwidth=2, relief="solid")
secondCaption.pack(pady=10)

#Text goes in the caption
infoText = Label(secondCaption, text="Select a Layer to Edit:", width=17, bd=5, bg="white", font=("Helvetica", 12))
infoText.pack()

#Make a separate frame for our editing features (layer select, start, etc...)
buttonsFrame = Frame(root, bg="white", width = 1100, height = 200, padx = 10, pady = 10, borderwidth=2, relief="solid")
buttonsFrame.pack(pady=10)

#Make a separate frame for our saving, loading, starting, and stopping
startFrame = Frame(root, bg='White', width=1100, height=200, padx= 10, pady=10, borderwidth=2, relief="solid")
startFrame.pack(pady=10)

#Make a separate frame for our example layouts
exampleFrame = Frame(root, bg='White', width=1100, height=200, padx= 10, pady=10, borderwidth=2, relief="solid")
exampleFrame.pack(pady=10)

"""
#Make a separate frame for the typing practice
practiceFrame = Frame(root, bg='White', width=1100, height=200, padx= 10, pady=10, borderwidth=2, relief="solid")
practiceFrame.pack(pady=10)"""

#create a class for each UI "Key"
class Key:
    display = "Default"
    code = "KEY_A"
    codes = []#Keycode by layer
    mode = 0#when mode is 0, the key just types the letter. + specifies a layer. - means it is unusable.
    label = Label(keyFrame)

    def __init__(self, code, display):
        self.code = code
        self.codes = [code, code, code]
        self.mode = 0
        self.display = display
        self.label = Label(keyFrame, text=display+"\n"+"", width=13, bd=10, bg='grey', fg='white', borderwidth=2, relief="solid", font=("Arial", 8))
    def updateText(self):
        if (self.code!=self.codes[layer]):
            self.label.config(text=self.display+"\n"+re.sub("KEY_", "", self.codes[layer]))
        else:
            self.label.config(text=self.display+"\n"+"")
    def updateColor(self):
        if (self.code!=self.codes[layer]):
            self.label.config(bg='green')
        else:
            if (self.mode == 0):
                self.label.config(bg='grey')
            if (self.mode == -1):
                self.label.config(bg='red4')
            if (self.mode == 1):
                self.label.config(bg='deep sky blue')
                self.label.config(text=self.display+"\n"+"Layer 1 Key")
            if (self.mode == 2):
                self.label.config(bg='DodgerBlue2')
                self.label.config(text=self.display+"\n"+"Layer 2 Key")
            if (self.mode == 3):
                self.label.config(bg='blue4')
                self.label.config(text=self.display+"\n"+"Layer 3 Key")
        
        
    def whenClicked(self, event):
        
        global layer
        global root
        global nextKeyBeingUsed
        print(layer)
        #when we are clicked, the action depends on which editing mode we are in.
        
        if (layer == -1):
            self.mode += 1
            if self.mode > 3:
                self.mode = 0
            self.updateColor()
        elif (nextKeyBeingUsed == False):
            self.codes[layer] = "Press A Key"
            updateKeyboardText()
            self.updateText()
            #root.mainloop()
            #messagebox.showinfo("Press A Key", "Press A Key")
            root.update()
            self.codes[layer] = getNextKey()
        updateKeyboardText()
        self.updateColor()
        
        
    """def whenEnter(self, event):
        event.widget.config(bg='black')
    def whenLeave(self, event):
        event.widget.config(bg='grey')"""

def updateKeyboardText():
    for i in range(len(keyboard)):
        for e in range(len(keyboard[i])):
            keyboard[i][e].updateText()
            keyboard[i][e].updateColor()

keyboard = [
    [Key('KEY_GRAVE', '` ~'), Key('KEY_1', '1 !'), Key('KEY_2', '2 @'), Key('KEY_3', '3 #'), Key('KEY_4', '4 $'), Key('KEY_5', '5 %'), Key('KEY_6', '6 ^'),
     Key('KEY_7', '7 &'), Key('KEY_8', '8 *'), Key('KEY_9', '9 ('), Key('KEY_0', '0 )'), Key('KEY_MINUS', '- _'), Key('KEY_EQUAL', '= +'), Key('KEY_BACKSPACE', 'Backspace')],
    
    [Key('KEY_TAB', 'Tab'), Key('KEY_Q', 'Q'), Key('KEY_W', 'W'), Key('KEY_E', 'E'), Key('KEY_R', 'R'), Key('KEY_T', 'T'), Key('KEY_Y', 'Y'),
     Key('KEY_U', 'U'), Key('KEY_I', 'I'), Key('KEY_O', 'O'), Key('KEY_P', 'P'), Key('KEY_LEFTBRACE', '[ {'), Key('KEY_RIGHTBRACE', '] }'), Key('KEY_BACKSLASH', '\\ |')],
    
    [Key('KEY_CAPSLOCK', 'Caps'), Key('KEY_A', 'A'), Key('KEY_S', 'S'), Key('KEY_D', 'D'), Key('KEY_F', 'F'), Key('KEY_G', 'G'), Key('KEY_H', 'H'),
     Key('KEY_J', 'J'), Key('KEY_K', 'K'), Key('KEY_L', 'L'), Key('KEY_SEMICOLON', '; :'), Key('KEY_APOSTROPHE', "' \""), Key('KEY_ENTER', 'Enter')],
    
    [Key('KEY_LEFTSHIFT', 'Shift'), Key('KEY_Z', 'Z'), Key('KEY_X', 'X'), Key('KEY_C', 'C'), Key('KEY_V', 'V'), Key('KEY_B', 'B'), Key('KEY_N', 'N'),
     Key('KEY_M', 'M'), Key('KEY_COMMA', ', <'), Key('KEY_DOT', '. >'), Key('KEY_SLASH', '/ ?'), Key('KEY_RIGHTSHIFT', 'Shift')],
    
    [Key('KEY_LEFTCTRL', 'Ctrl'), Key('KEY_FN', 'Fn'), Key('KEY_LEFTMETA', 'Win'), Key('KEY_LEFTALT', 'Alt'), Key('KEY_SPACE', 'Space'),
     Key('KEY_RIGHTALT', 'Alt'), Key('KEY_RIGHTCTRL', 'Ctrl'), Key('KEY_LEFT', '←'), Key('KEY_UP', '↑'), Key('KEY_DOWN', '↓'), Key('KEY_RIGHT', '→')],
]



#Create our on screen keyboard

for i in range(len(keyboard)):
    for e in range(len(keyboard[i])):
        key = keyboard[i][e]
        key.label.grid(row=i,column=e, padx=2, pady=2)
        key.label.bind("<Button-1>", key.whenClicked)
        """key.label.bind("<Enter>", key.whenEnter)
        key.label.bind("<Leave>", key.whenLeave)"""
        key.label.bind("<Enter>", setCursor)
        key.label.bind("<Leave>", resetCursor)
        key.updateColor()
#Create the three layer buttons
def layerSet(event):
    name = event.widget.cget("text")
    realLayerSet(name)

def realLayerSet(name):
    global layer
    if (name == "Layer 1"):
        layer = 0
        layer1.config(bg="black")
        layer2.config(bg="grey")
        layer3.config(bg="grey")
        modeButton.config(bg="grey")
        updateKeyboardText()
    if (name == "Layer 2"):
        layer = 1
        layer2.config(bg="black")
        layer1.config(bg="grey")
        layer3.config(bg="grey")
        modeButton.config(bg="grey")
        updateKeyboardText()
    if (name == "Layer 3"):
        layer = 2
        layer3.config(bg="black")
        layer2.config(bg="grey")
        layer1.config(bg="grey")
        modeButton.config(bg="grey")
        updateKeyboardText()
    if (name == "Layer Keys"):
        layer = -1
        modeButton.config(bg="black")
        layer2.config(bg="grey")
        layer1.config(bg="grey")
        layer3.config(bg="grey")
        updateKeyboardText()

    print (layer)
#the starter function allows our remapping to run in the background, even while we use the UI and run our typing practice.
thread = threading.Thread()
def starter(event):
    global thread
    thread = threading.Thread(target=start, args=())
    thread.start()
stopEvent = threading.Event()
def stopper(event):
    global thread
    global device
    if (thread):
        stopEvent.set()
        thread.join()
        device.ungrab()
        print("exited the thread")
        #reset our stop event for later
        stopEvent.clear()
def start():
    global device
    global virtual
    global layer
    device.grab()
    layer = 0
    for event in device.read_loop():
        if stopEvent.is_set():
            break
        if event.type == evdev.ecodes.EV_KEY:
            keyEvent = evdev.categorize(event)
            
            #virtual.emit_click(getattr(uinput, ))
            #loop through every key and "translate" their keycodes.
            for i in range(len(keyboard)):
                for e in range(len(keyboard[i])):
                    if (keyEvent.keycode == keyboard[i][e].code):
                        if (keyboard[i][e].mode < 1):
                            if (keyEvent.keystate == keyEvent.key_down):
                                virtual.emit(getattr(uinput, keyboard[i][e].codes[layer]), 1)
                            if (keyEvent.keystate == keyEvent.key_up):
                                virtual.emit(getattr(uinput, keyboard[i][e].codes[layer]), 0)
                        elif (keyboard[i][e].mode == 1):
                            layer = 0
                        elif (keyboard[i][e].mode == 2):
                            layer = 1
                        elif (keyboard[i][e].mode == 3):
                            layer = 2

layer1 = Label(buttonsFrame, text="Layer 1", width=7, bd=10, bg='grey', fg='white')
layer1.grid(row=0,column=0, padx=5)
layer1.bind("<Button-1>", layerSet)
layer1.bind("<Enter>", setCursor)
layer1.bind("<Leave>", resetCursor)
layer2 = Label(buttonsFrame, text="Layer 2", width=7, bd=10, bg='grey', fg='white')
layer2.grid(row=0,column=1, padx=5)
layer2.bind("<Button-1>", layerSet)
layer2.bind("<Enter>", setCursor)
layer2.bind("<Leave>", resetCursor)
layer3 = Label(buttonsFrame, text="Layer 3", width=7, bd=10, bg='grey', fg='white')
layer3.grid(row=0,column=2, padx=5)
layer3.bind("<Button-1>", layerSet)
layer3.bind("<Enter>", setCursor)
layer3.bind("<Leave>", resetCursor)
#button for setting key modes
modeButton = Label(buttonsFrame, text="Layer Keys", width=7, bd=10, bg='black', fg='white')
modeButton.grid(row=0,column=3, padx=5)
modeButton.bind("<Button-1>", layerSet)
modeButton.bind("<Enter>", setCursor)
modeButton.bind("<Leave>", resetCursor)

#button for starting the modified keyboard
startButton = Label(startFrame, text="Start Keyboard", width=12, bd=10, bg='green', fg='white')
startButton.grid(row=0, column=4, padx=5)
startButton.bind("<Button-1>", starter)
startButton.bind("<Enter>", setCursor)
startButton.bind("<Leave>", resetCursor)
#button for stopping the keyboard
"""
stopButton = Label(startFrame, text="Stop Keyboard", width=12, bd=10, bg='red', fg='white')
stopButton.grid(row=0, column=5, padx=5)
stopButton.bind("<Button-1>", stopper)
stopButton.bind("<Enter>", setCursor)
stopButton.bind("<Leave>", resetCursor)
"""
#type file name box
fileBox = Entry(startFrame, width=15)
fileBox.insert(0, "default.txt")
fileBox.grid(row=0, column=6, padx=5)
#save file
#make a saveable version of the keyboard object with only crucial information (display, code, code1, code2, code3, mode)
class saveKey:
    display = ""
    code = "KEY_A"
    codes = ["KEY_A", "KEY_B", "KEY_C"]
    mode = 0
    def __init__(self, display, code, codes, mode):
        self.display = display
        self.code = code
        self.codes = codes
        self.mode = mode
saveKeyboard = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
#save the crucial information
def save(event):
    global keyboard
    global saveKeyboard
    for i in range(len(keyboard)):
        for e in range(len(keyboard[i])):
            key = keyboard[i][e]
            saveKeyboard[i][e] = saveKey(key.display, key.code, key.codes, key.mode)
    with open(fileBox.get(), "wb") as file:
        pickle.dump(saveKeyboard, file)
saveButton = Label(startFrame, text="Save Configuration", width=16, bd=10, bg='green', fg='white')
saveButton.grid(row=0, column=7, padx=5)
saveButton.bind("<Button-1>", save)

#load file
#open the file and load it into our saveKeyboard list

def loadFile(event):
    realLayerSet("Layer 1")
    global keyboard
    global saveKeyboard
    global keyFrame
    global layer
    print (layer)
    with open(fileBox.get(), "rb") as file:
        saveKeyboard = pickle.load(file)
        #convert the saveKeyboard into a 'proper' keyboard lists
        for i in range(len(keyboard)):
            for e in range(len(keyboard[i])):
                key = keyboard[i][e]
                saveKey = saveKeyboard[i][e]

                key.display = saveKey.display
                key.code = saveKey.code
                key.codes = saveKey.codes
                key.mode = saveKey.mode
                key.label.config(text=key.display+"\n"+re.sub("KEY_", "", key.codes[layer]), width=13, bd=10, bg='grey', fg='white', borderwidth=2, relief="solid", font=("Arial", 8))
                layer = 0
                key.updateText()
                key.updateColor()
def example1(event):
    fileBox.delete(0, 100)
    fileBox.insert(0, "LeftHand.txt")
    loadFile(event)
def example2(event):
    fileBox.delete(0, 100)
    fileBox.insert(0, "RightHand.txt")
    loadFile(event)
def example3(event):
    fileBox.delete(0, 100)
    fileBox.insert(0, "WASD.txt")
    loadFile(event)
def example4(event):
    fileBox.delete(0, 100)
    fileBox.insert(0, "clear.txt")
    loadFile(event)

loadButton = Label(startFrame, text="Load Configuration", width=16, bd=10, bg='green', fg='white')
loadButton.grid(row=0, column=8, padx=5)
loadButton.bind("<Button-1>", loadFile)
loadButton.bind("<Enter>", setCursor)
loadButton.bind("<Leave>", resetCursor)

example1Button = Label(exampleFrame, text="Left Hand Layout", width=16, bd=10, bg='green', fg='white')
example1Button.grid(row=0, column=0, padx=5)
example1Button.bind("<Button-1>", example1)
example1Button.bind("<Enter>", setCursor)
example1Button.bind("<Leave>", resetCursor)

example2Button = Label(exampleFrame, text="Right Hand Layout", width=16, bd=10, bg='green', fg='white')
example2Button.grid(row=0, column=1, padx=5)
example2Button.bind("<Button-1>", example2)
example2Button.bind("<Enter>", setCursor)
example2Button.bind("<Leave>", resetCursor)

example3Button = Label(exampleFrame, text="WASD Layout", width=16, bd=10, bg='green', fg='white')
example3Button.grid(row=0, column=2, padx=5)
example3Button.bind("<Button-1>", example3)
example3Button.bind("<Enter>", setCursor)
example3Button.bind("<Leave>", resetCursor)

example4Button = Label(exampleFrame, text="Blank Layout", width=16, bd=10, bg='green', fg='white')
example4Button.grid(row=0, column=3, padx=5)
example4Button.bind("<Button-1>", example4)
example4Button.bind("<Enter>", setCursor)
example4Button.bind("<Leave>", resetCursor)

"""
#label in practice
textLabel = Label(practiceFrame, width=800, height=100)
textLabel.pack()

#text box in practice
textBox = Text(practiceFrame, width=800, height =100)
textBox.pack()
"""

root.mainloop()

#Below is our original test code that we have here as a reference for later use

"""
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        keyEvent = evdev.categorize(event)
        print(keyEvent)
        print(keyEvent.keycode)
        if keyEvent.keycode == 'KEY_A':
            print("emitting the letter A")
            break
        if (keyEvent.keycode == 'KEY_B'):
            print("key b has been pressed")
            time.sleep(1)
            virtual.emit_click(uinput.KEY_B)
"""
