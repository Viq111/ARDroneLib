# -*- coding:Utf-8 -*-
# ARDrone Package
prog_name = "AR.Drone Log"
# version:
version = 1
# By Vianney Tran, Romain Fihue, Giulia Guidi, Julien Lagarde
# License: Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) 
# (http://creativecommons.org/licenses/by-sa/3.0/)

##############
### IMPORT ###
##############
import os, time

###############
### GLOBALS ###
###############

###############
### CLASSES ###
###############

class Log():
    "Create log of some data"
    def __init__(self, filename, format="kml"):
        "Initialise the file, format is the output format, currently: currently: kml"
        supported_ext = ["kml"]
        if not format in supported_ext: raise TypeError("Format Error")
        self.format = format
        self.filename = filename
        self.f = open(filename,"w")
        self.open = True
        # Write Header
        if format == "kml": self.f.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n<name>' + str(filename) + '</name>\n')
            
    def add_data(self,data_dict):
        "Add some data to the file, format have to be good"
        if not self.open:   return False
        if self.format == "kml":
            longi = data_dict["longitude"]
            lati = data_dict["latitude"]
            elev = data_dict["elevation"]
            to_write = '<Placemark>\n<name>' + time.strftime("%H:%M:%S") + '</name>\n<Point>\n<coordinates>' + str(longi) + ',' + str(lati) + ',' + str(elev) + '</coordinates>\n</Point>\n</Placemark>\n'
            self.f.write(to_write)
        return True
    def close(self):
        "Close the file"
        # Write footer
        if self.format == "kml":    self.f.write("</Document>\n</kml>")
        self.open = False
        self.f.close()

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
    a = Log("text.kml","kml")
    a.add_data({"latitude":48.766854,"longitude":2.290127,"elevation":0})
    a.add_data({"latitude":48.763884,"longitude":2.289913,"elevation":0})
    a.close()

