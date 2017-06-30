# feet.py

# Merijn Testroote, 11173106
# Babette Mooij, 10740414
# Alexandra Spruit, 11262273
# Hannah Min, 11011580

# This code has been developed for the course ZSB 2017
# at the University of Amsterdam

# 30-06-2017 - We take no responsibility for the 
# effects of this software nor if Carlos is taking over the
# world or getting around in fancy cars and winning all poker games.
# The code is served as is.

import os
import time
from naoqi import ALProxy, ALModule

class Feet(ALModule ):

    feet_pressed = None

    def __init__(self):
        ALModule.__init__(self, "feet")
        self.led = ALProxy("ALLeds")
        self.normal_mode()
        self.touch = ALProxy("ALTouch")

        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("RightBumperPressed",
                                "feet",
                                "right_bumper")

        memory.subscribeToEvent("LeftBumperPressed",
                                "feet",
                                "left_bumper")

    def do_rasta(self):
        self.led.rasta(10)

    def question_mode(self):
        self.led.fadeRGB("LeftFootLeds",1,0,0,0.1)
        self.led.fadeRGB("RightFootLeds",0,1,0,0.1)
        self.led.on("FaceLeds")


    def normal_mode(self):
        self.led.fadeRGB("LeftFootLeds",0,0,1,0.1)
        self.led.fadeRGB("RightFootLeds",0,0,1,0.1)
        self.led.on("FaceLeds")

    def register_question(self):
        self.question_mode()
        self.feet_pressed = None
        while not self.feet_pressed:
            time.sleep(0.5)

        self.normal_mode()
        return True if self.feet_pressed == 'right' else False

    def right_bumper(self, *_args):
        self.feet_pressed = 'right'

    def left_bumper(self, *_args):
        self.feet_pressed = 'left'
