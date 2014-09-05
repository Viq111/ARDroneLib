# -*- coding:Utf-8 -*-
# ARDrone Lib Package
prog_name = "AR.Drone GUI"
# version:
version = 4
# By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import os, time, threading
from Tkinter import *


###############
### GLOBALS ###
###############

FPS = 50

###################
### DEFINITIONS ###
###################
def nop_func(arg1=None):
    "Do nothing"
    pass
def kill_fen(root):
    "Kill the window that called"
    root.fen.destroy()
    root.fen.quit()
    # Return a function
    return nop_func

###############
### CLASSES ###
###############

class ControlWindow():
    "Create a simple window to control the drone"
    def __init__(self,default_action=nop_func):
        "Create a window to control the drone"
        self.actions = dict()   # Actions associated to keys
        self.to_print = list()  # Data we have to print each time
        self.default_action = default_action
        self.text = None # Text that will be changed
        self.text_label = None
        self.last_key = None
        self.running = False
    def add_action(self,button_bind,function_call):
        "Add an action when a key is pressed"
        self.actions[button_bind] = function_call
        return True
    def add_printable_data(self, description, tree):
        "Add something in navdata to print, tree is a tulpe"
        # Check if the arguments are good
        if type(tree) != type((0,0)):   raise TypeError("Tree must be a tulpe")
        self.to_print.append((str(description),tree))
        return True
    def change_text(self, new_text):
        "Change the text inside the box"
        try:    new_text=str(new_text) # Check if we have no error changing text
        except: return False
        if self.text is None:   return False # Window not yet initiated
        self.text.set(new_text)
        return True
    def callback(self, navdata):
        "Callback function that can be given to Navdata filter"
        new_text = ""
        if len(navdata.keys()) < 1: return False # We don't have any navdata
        for p in self.to_print:
            # Get data
            data = navdata
            # Get the tree
            for key in p[1]:
                if data != None:
                    if str(key) in data.keys():
                        data = data[str(key)]
                    else:
                        data = "Error in given tree (" + str(p[1]) + "): " + str(key)
                else:
                    data = "No data"
                    break
            # Format
            new_text = new_text + str(p[0]) + ": " + str(data) + "\n"
        # And done
        self.change_text(new_text)        
    
    def start(self):
        "Activate the window (and keep the thread)"
        self.fen = Tk()
        cadre = Frame(self.fen, width=500, height = 200, bg="grey")
        self.text = StringVar() # Text that will be changed
        self.text_label = Label(self.fen,textvariable=self.text, fg = "black")
        self.text_label.pack()
        self.fen.bind("<KeyPress>",self._key_pressed)
        self.fen.bind("<KeyRelease>",self._key_released)        
        cadre.pack()
        self.fen.protocol("WM_DELETE_WINDOW", self.stop) # Called when the window is closed
        #self.fen.mainloop()
        self.running = True
        while self.running:
            self.fen.update()
            time.sleep(1.0/FPS) # Adjust FPS

    def stop(self):
        "Stop the window"
        try:    self.fen.destroy()
        except: pass
        try:    self.fen.quit()
        except: pass
        self.running = False
        return True

    # Keys handler
    def _key_pressed(self, action):
        "Function which is called when a key is pressed"
        if self.last_key != action.keysym : # Check if it's new key
            self.last_key = action.keysym
            if action.keysym in self.actions.keys(): # Check if we need to perform action
                self.actions[action.keysym]()
    def _key_released(self,action):
        "Function called when the key is released"
        if self.last_key != None:
            self.last_key = None
            self.default_action()
##################
###  __MAIN__  ###
##################
if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    gui = None
    gui = ControlWindow(lambda arg=1:gui.change_text("No button pressed"))
    gui.add_action("Up",lambda arg=gui:gui.change_text("Up Arrow pressed"))
    gui.add_action("a",lambda arg=gui:arg.change_text("A button pressed"))
    print "Press A or Up Arrow for an example"
    gui.start()
