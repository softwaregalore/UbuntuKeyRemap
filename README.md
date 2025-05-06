# UbuntuKeyRemap
This simple python program allows you to remap your keyboard to accommodate for various disabilities like paralysis and finger amputations. Essentially, it allows you to remap your keyboard into a select number of keys, using "layer keys" to switch between layers.
# Installation
*note, this program can currently only run on linux systems, and has only been tested on Ubuntu.

Before running, you must open permissions on your devices keyboard object, typically stored in /dev/input/event#. Running the command "sudo evtest" can help to find which object this is.

After opening permissions on your keyboard, please ensure that the following libraries are installed: 
- PyQt6
- tkinter
- time
- evdev
- uinput
- pickle
- re
- threading
- sys

After installing these libraries (or checking that they are already installed), you should be able to run the python script. 
