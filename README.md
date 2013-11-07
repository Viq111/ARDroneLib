Python ARDrone Libray for AR.Drone 2.0 to 2.3
==================

ARDroneLib is a library for AR.Drone 2 developped in Python
You can control your AR.Drone with our library
It's as easy as:

	> import ARDroneLib
	> drone = ARDroneLib.Drone()
	> drone.takeoff()
	> drone.land()

It doesn't require any third party library and can work as a stand-alone or an easy library to access your drone

Here is the description of each file:

######################
###  ARDroneConfig ###
######################
This is a sub-library to easily send configuration to your drone.
This library is now directly called by ARDroneLib.
You can see possible configuration with:

	> drone = ARDroneLib.Drone()
	> drone.list_config()

When you have in mind the configuration you want to send, just send it with:

	> drone.set_config(<your_config>=<your_value>)

Here is an example:

	> import ARDroneLib
	> drone = ARDroneLib.Drone()
	> drone.set_config(max_altitude=5)

It is also useful to activate the reception of some navdata with:

	> drone.set_config(activate_navdata=True)
	
Finally, there is two other functions related to ARDroneConfig: goto and animation.

Goto enables you to put your drone into a autonomous mode. It will go to a selected point depending on the method
You can call it with:

	> drone.goto(method, x, y, z, cap, speed)
	
For example to go to the eiffel tower at an altitude of 5 meters:

	> drone.goto("GPS", 48.858419, 2.294333, 5, 0)

animation
######################
###   ARDroneGUI   ###
######################
This file implements a simple GUI to control your drone and print data easily
Example:
<pre>
import ARDroneLib, ARDroneGUI
drone = ARDroneLib.Drone()
gui = ARDroneGUI.ControlWindow(default_action=drone.hover)
gui.add_action("<W>", drone.forward)
gui.change_text("Hello World !")
</pre>

######################
###   ARDroneLib   ###
######################
This is the main file which enable you to control your drone
All the easy function are implemented to control your drone without taking care of the information you have to send.
Example:
<pre>
import ARDroneLib
drone = ARDroneLib.Drone()
drone.takeoff()
drone.forward()
drone.hover()
drone.land()
</pre>

######################
### ARDroneNavdata ###
######################
This is the second most important file which enable you to receive data from the drone.
You don't actually need to call it into your program because ARDroneLib do it for you, you just have to create a callback function
which receive a navdata dictionary as the sole argument.
See inside the file to know what is sent back to your function
Example:
<pre>
import ARDroneLib
drone = ARDroneLib.Drone(data_callback=my_callback_function)
drone.start_navdata()
</pre>

######################
###   ARDroneTest  ###
######################
This file is a quick example of the library which enables you to command and receive info from your drone without even writing a single line of code.
Look at this file to quickly understand how the program is working.
