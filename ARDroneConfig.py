# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone Config"
# version:
version = 3
# By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import time

###################
### DEFINITIONS ###
###################

# DATA-RELATED
def activate_navdata(activate=True):
    "Prepare the drone so he can send navdata back to us"
    if activate:    return [("general:navdata_demo","FALSE")] #Activate navdata
    else:   return [("general:navdata_demo","TRUE")]
def detect_tag(color=0):
    """ Send the config to the drone to activate drone detection
        0 is the blue-orange color
        1 is the yellow-orange color"""
    if color == 1:  tag_color = "2"
    else:           tag_color = "3"
    com = list()
    com.append(("detect:detect_type","13"))
    com.append(("detect:enemy_colors",tag_color))
    com.append(("detect:enemy_without_shell","0"))
    return com

def detect_carpet(activate = True):
    "Activate carpet detection"
    if activate:    return [("detect:detect_type","15"),("control:flying_camera_enable","TRUE")]
    else:           return [("control:flying_camera_enable","FALSE")]

# ONE-TIME CONFIG RELATED
def indoor(activate = True):
    "Set the drone config to act as if it is indoor"
    if activate:    return [("control:outdoor","FALSE"),("control:flight_without_shell","FALSE")]
    else:           return outdoor(activate=True)
def outdoor(activate = True):
    "Set the drone config to act as if it is outdoor"
    if activate:    return [("control:outdoor","TRUE"),("control:flight_without_shell","TRUE")]
    else:           return indoor(activate=True)

def nervosity_level(percentage=20):
    "Configure the nervosity of the drone,percentage=10:weak response to command; percentage=100:full trust"
    euler = int(0.52*percentage)/100.0 # 2 digits after coma
    vertical_speed = int(2000*percentage)
    yaw = int(6.11*percentage)/100.0
    com = list()
    com.append(("control:euler_angle_max",str(euler)))
    com.append(("control:control_vz_max",str(vertical_speed)))
    com.append(("control:control_yaw",str(yaw)))
    return com
def max_altitude(altitude=5):
    "Set the max altitude of the drone"
    return [("control:altitude_max",str(int(altitude*1000)))]
def set_ultrasound(freq=0):
    "Set the ultrasound frequence"
    if freq:    return [("pic:ultrasound_freq","7")]
    else:       return [("pic:ultrasound_freq","8")]
    
    
# Animations
def flip(side="LEFT"):
    """ Do a flip, side is the side of the flip
        Side is LEFT, RIGHT, FRONT, BACK"""
    s = 17
    if side.upper() == "FRONT": s = 16
    if side.upper() == "LEFT":  s = 18
    if side.upper() == "RIGHT": s = 19
    return [("control:flight_anim",str(s)+",15")]

# Autonomous Flight
def goto_gps_point(latitude, longitude, altitude=2, cap=0, speed=1):
    "Send the drone to the GPS point, cap is in degre"
    if (longitude == 0) or (latitude == 0):   return [] # Try not to send drone to somewhere weird
    # Compute each data
    longi = int(longitude*10000000)
    lati = int(latitude*10000000)
    alt = int(altitude*1000)
    cap = int(cap)
    # Create the right parameter according to doc
    param1 = "10,500,"+str(lati)+","+str(longi)+","+str(alt)+",0,0,0," + str(cap) + ",0"
    #param1 = "0,10,1500,0,0,0,0,0,0,0,0" # Forward traveling (1500 is x speed)
    # Let's go !
    com = list()
    com.append(("control:flying_mode","0"))
    com.append(("control:autonomous_flight","FALSE"))
    com.append(("control:travelling_mode",param1))
    com.append(("control:travelling_enable","TRUE"))
    return com

###############
### GLOBALS ###
###############

SUPPORTED_CONFIG = {
    "detect_tag":detect_tag, "detect_carpet":detect_carpet, "activate_navdata":activate_navdata,                                    # Data activation
    "indoor":indoor, "outdoor":outdoor, "nervosity_level":nervosity_level, "max_altitude":max_altitude, "set_ultrasound":set_ultrasound # One-time config
    }
AUTONOMOUS_FLIGHT = {"gps":goto_gps_point}
ANIMATIONS = {"flip":flip}
ANIMATIONS_INFOS = {"flip":"(side)"}
# Check if animations corelate
if ANIMATIONS.keys() != ANIMATIONS_INFOS.keys():    raise ImportError("Animations differs")

    
##################
###  __MAIN__  ###
##################

if __name__ == "__main__":
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde (under CC BY-SA 3.0 license)"
    print "> Loading program ..."
    print "> This is a library only, please use the test instead"

