import os
import time
from naoqi import ALProxy, ALModule

class Feet(ALModule ):

    feet_pressed = None

    def __init__(self):
        ALModule.__init__(self, "feetWatcher")
        self.led = ALProxy("ALLeds")
        self.ledNormalMode()
        self.touch = ALProxy("ALTouch")

        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("RightBumperPressed",
                                "feetWatcher",
                                "rightBumper")

        memory.subscribeToEvent("LeftBumperPressed",
                                "feetWatcher",
                                "leftBumper")

    def doRasta(self):
        self.led.rasta(10)

    def ledQuestionMode(self):
        self.led.fadeRGB("LeftFootLeds",1,0,0,0.1)
        self.led.fadeRGB("RightFootLeds",0,1,0,0.1)

    def ledNormalMode(self):
        self.led.fadeRGB("LeftFootLeds",0,0,1,0.1)
        self.led.fadeRGB("RightFootLeds",0,0,1,0.1)
    
    def registerQuestion(self):
        self.ledQuestionMode()
        self.feet_pressed = None
        while not self.feet_pressed:
            time.sleep(0.5)

        self.ledNormalMode()
        return True if self.feet_pressed == 'right' else False

    def rightBumper(self, *_args):
        self.feet_pressed = 'right'
        pass

    def leftBumper(self, *_args):
        self.feet_pressed = 'left'
        pass

