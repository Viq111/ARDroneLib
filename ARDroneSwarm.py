# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone Swarm"
# version:
version = 2
# By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import os, time
import ARDroneLib, ARDroneConfig

###############
### GLOBALS ###
###############

###################
### DEFINITIONS ###
###################
    
##################
###  __MAIN__  ###
##################

if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    print "> This is a library only, please use the test instead"

    # Connect back

    # Creation drone
    drone1 = ARDroneLib.Drone("192.168.100.50")
    drone2 = ARDroneLib.Drone("192.168.100.51")
    drone1.calibrate()
    drone2.calibrate()
    
    wait =raw_input("Press enter to take off ...")
    drone1.takeoff()
    drone2.takeoff()
    wait =raw_input("Press enter to take altitude ...")
    drone1.set_config(activate_navdata=True,detect_carpet=True)
    drone2.set_config(activate_navdata=True,detect_carpet=True)
    drone1.up()
    drone2.up()
    
    wait =raw_input("Press enter to stop taking altitude...")
    drone1.hover()
    drone2.hover()
    wait =raw_input("Press enter to start  program...")
    # Set middle
    print "Middle..."
    drone1.goto("carpet",2.5,3.5,2.5)
    drone2.goto("carpet",2.5,1.5,2.5)
    time.sleep(1)
    # Go in position
    print "Go in position..."
    drone1.goto("carpet",1.5,3.5,2.5)
    drone2.goto("carpet",3.5,1.5,2.5)
    time.sleep(1)
    print "Doing figure..."
    drone1.goto("carpet",3.5,3.5,2.5)
    drone2.goto("carpet",1.5,1.5,2.5)
    time.sleep(1)
    drone1.goto("carpet",1.5,3.5,2.5)
    drone2.goto("carpet",3.5,1.5,2.5)
    time.sleep(2)
    print "Flipping !"
    drone1.animation("flip",("RIGHT",))
    drone2.animation("flip",("LEFT",))
    time.sleep(0.75)
    drone1.goto("carpet",1.5,1.5,2.5)
    drone2.goto("carpet",3.5,3.5,2.5)
                     
    time.sleep(1)
    print "Doing figure..."
    drone1.goto("carpet",3.5,1.5,2.5)
    drone2.goto("carpet",1.5,3.5,2.5)
    time.sleep(0.5)
    drone1.goto("carpet",1.5,1.5,2.5)
    drone2.goto("carpet",3.5,3.5,2.5)
    time.sleep(1)
    print "Final position..."
    drone1.goto("carpet",2,2.5,2.5)
    drone2.goto("carpet",3,2.5,2.5)
    time.sleep(1)
    print "Going in position for circle..."
    drone1.goto("carpet",2.5,2.5,2.5)
    drone2.goto("carpet",4,2.5,2.5)
    time.sleep(2)
    print "Circling!"
    drone2.animation("carpet_circle",(1.5,8,2.5,0))
    time.sleep(3)
    drone1.animation("carpet_circle",(1.5,8,2.5,0))
    time.sleep(25)
    print "Landing..."
    drone1.hover()
    drone2.hover()
    drone1.land()
    drone2.land()
    drone1.stop()
    drone2.stop()
    print "Done !"
