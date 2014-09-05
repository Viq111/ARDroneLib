# -*- coding:Utf-8 -*-
# ARDrone Lib Package
prog_name = "AR.Drone Test"
# version:
version = 4
# By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import time, sys, os
import ARDroneLib, ARDroneGUI
from ARDroneLog import Log

###############
### GLOBALS ###
###############

gui = None
last_coord=(None,None)
all_coords = dict()

###############
### CLASSES ###
###############

class GPS_Coord():
    "Very little class to store GPS Coord"
    def setPoint(self, longi=None, lati=None):
        self.lo = longi
        self.la = lati
        print "> Saved navpoint:",(self.lo,self.la)
    __init__ = setPoint
    def getPoint(self): return (self.lo, self.la)
###################
### DEFINITIONS ###
###################

######################
# CALLBACK FUNCTIONS #
######################

def print_navdata(navdata):
    "Print the navdata as RAW text" 
    print navdata
    pass

def save_gps_coord(navdata):
    "Save the last navdata coordinate in a global var"
    global last_coord, gui, a
    # Updata coord
    if navdata["gps_info"] == None:    return False
    last_coord = (navdata["gps_info"]["longitude"],navdata["gps_info"]["latitude"])
    a.add_data({"latitude":navdata["gps_info"]["latitude"],"longitude":navdata["gps_info"]["longitude"],"elevation":0})
    # And refresh GUI
    gui.callback(navdata)
    return True

##################
# TEST FUNCTIONS #
##################

# Choose your test
def choose_sequence(drone):
    "Choose a test program sequence"
    print "Please choose a test program you want to run:"
    print "1 - Take Off & Land"
    print "2 - Command line test"
    print "3 - GUI Command Test"
    print "4 - GPS Test"
    result = raw_input(">")
    if result == "1":
        takeoff_land(drone)
    elif result == "2":
        menu_list(drone)
    elif result == "3":
        print "-> Launching GUI ..."
        command_GUI(drone)
    elif result == "4":
        print "-> Starting GPS Test ..."
        GPS_Command(drone)      

# 1st Test: Just testing commands
def takeoff_land(drone):
    "Routine just to test takeoff_land"
    wait= raw_input("Press enter to take off...")
    drone.takeoff()
    wait= raw_input("Press enter to land..")
    drone.land()
    time.sleep(1)
    drone.stop()

# 2st Test: Command line
def menu_list(drone):
    "List of function you can perform"
    print "Choose your command:"
    print "0 - Emergency"
    print "1 - Hover"
    print "2 - Take Off"
    print "3 - Land"
    print "4 - Forward"
    print "5 - Backward"
    print "6 - Left"
    print "7 - Right"
    print "8 - Calibrate sensors"
    print "a - Reset"
    print "9 - Quit"
    result = ""
    while result != "9":
        result = raw_input(">")
        if result == "0": drone.emergency()
        if result == "1": drone.hover()
        if result == "2": drone.takeoff()
        if result == "3": drone.land()
        if result == "4": drone.forward()
        if result == "5": drone.backward()
        if result == "6": drone.left()
        if result == "7": drone.right()
        if result == "8": drone.calibrate()
        if result == "a": drone.reset()
        if result == "b": drone.set_config(activate_navdata=True)

# 3nd test
def command_GUI(drone):
    "Create a GUI to command the drone"
    global gui
    gui = ARDroneGUI.ControlWindow(default_action=drone.hover)
    # Add command
    gui.add_action("Up",drone.forward)
    gui.add_action("Down",drone.backward)
    gui.add_action("Left",drone.left)
    gui.add_action("Right",drone.right)
    gui.add_action("z",drone.up)
    gui.add_action("s",drone.down)
    gui.add_action("q",drone.rotate_left)
    gui.add_action("d",drone.rotate_right)
    gui.add_action("a",drone.takeoff)
    gui.add_action("space",drone.land)
    gui.add_action("Return",drone.emergency)
    gui.add_action("t",drone.reset)
    gui.add_action("y",drone.calibrate)
    gui.add_action("e",lambda arg=drone: drone.animation("flip",("LEFT",)))
    gui.add_action("j",lambda arg=drone: drone.set_config(record_video=True))
    gui.add_action("k",lambda arg=drone: drone.set_config(record_video=False))
    # Add info
    gui.add_printable_data("Battery",("navdata_demo","battery_percentage"))
    gui.add_printable_data("Number of tags",("vision_detect","nb_detected"))
    gui.add_printable_data("X position",("vision_detect","xc"))
    gui.add_printable_data("Y position",("vision_detect","yc"))
    gui.add_printable_data("Width",("vision_detect","width"))
    gui.add_printable_data("Height",("vision_detect","height"))
    gui.add_printable_data("Distance",("vision_detect","distance"))
    gui.add_printable_data("State (!=0)",("navdata_demo","ctrl_state"))
    drone.set_callback(gui.callback) # Enable the GUI to receive data from the drone
    drone.set_config(activate_navdata=True,detect_tag=1)
    gui.start()

# 4th test: GPS Test
def GPS_Command(drone):
    "Create a GUI to command the GPS"
    global gui, last_coord, a
    a = Log("Drone_GPS.kml","kml")
    pos1 = GPS_Coord()
    pos2 = GPS_Coord()
    pos3 = GPS_Coord(48.763947,2.288652) # Stade
    gui = ARDroneGUI.ControlWindow(default_action=drone.hover)
    drone.set_callback(save_gps_coord) # Change the callback so we can save the GPS data
    # Commands
    gui.add_action("Up",drone.forward)
    gui.add_action("Down",drone.backward)
    gui.add_action("Left",drone.left)
    gui.add_action("Right",drone.right)
    gui.add_action("z",drone.up)
    gui.add_action("s",drone.down)
    gui.add_action("a",drone.takeoff)
    gui.add_action("space",drone.land)
    gui.add_action("Return",drone.emergency)
    gui.add_action("t",drone.reset)
    gui.add_action("y",drone.calibrate)
    ## GPS
    gui.add_action("f",lambda arg=last_coord: pos1.setPoint(last_coord[1],last_coord[0]))
    gui.add_action("g",lambda arg=last_coord: pos2.setPoint(last_coord[1],last_coord[0]))
    gui.add_action("h",lambda arg=last_coord: pos3.setPoint(last_coord[1],last_coord[0]))
    gui.add_action("v",lambda arg=pos1: drone.goto("gps",arg.getPoint()[0],arg.getPoint()[1],2))
    gui.add_action("b",lambda arg=pos2: drone.goto("gps",arg.getPoint()[0],arg.getPoint()[1],2))
    gui.add_action("n",lambda arg=pos3: drone.goto("gps",arg.getPoint()[0],arg.getPoint()[1],2))

    # Infos
    gui.add_printable_data("Battery",("navdata_demo","battery_percentage"))
    gui.add_printable_data("Latitude",("gps_info","latitude"))
    gui.add_printable_data("Longitude",("gps_info","longitude"))
    gui.add_printable_data("Altitude",("gps_info","elevation"))
    gui.add_printable_data("HDOP",("gps_info","hdop"))
    gui.add_printable_data("State",("gps_info","data_available"))
    print "Press o to start reception...\nF,G,H - Save GPS point\nV,B,N (key must stay pressed) - GOTO GPS Point"
    # We don't start change the callback because we would lost gps info outside the gui
    drone.set_config(activate_navdata=True, activate_gps=True)
    gui.start()
    a.close()

##################
###  __MAIN__  ###
##################
if __name__ == "__main__":
    global drone
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    # Create the drone
    try:
        drone = ARDroneLib.Drone("192.168.1.1")
    except IOError:
        wait = raw_input("-> Cannot connect to drone !\n-> Press return to quit...")
        sys.exit()
    # Tests
    # And abord is something went wrong
    try:
        choose_sequence(drone)
    except KeyboardInterrupt:
        drone.stop()
    except:
        drone.stop()
        raise
    else:
        drone.stop()
    print "Test done." 
