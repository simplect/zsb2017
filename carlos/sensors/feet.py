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

    def do_rasta(self):
        self.led.rasta(10)

    def led_question_mode(self):
        self.led.fadeRGB("LeftFootLeds",1,0,0,0.1)
        self.led.fadeRGB("RightFootLeds",0,1,0,0.1)

    def led_normal_mode(self):
        self.led.fadeRGB("LeftFootLeds",0,0,1,0.1)
        self.led.fadeRGB("RightFootLeds",0,0,1,0.1)

    def register_question(self):
        self.ledQuestionMode()
        self.feet_pressed = None
        while not self.feet_pressed:
            time.sleep(0.5)

        self.ledNormalMode()
        return True if self.feet_pressed == 'right' else False

    def right_bumper(self, *_args):
        self.feet_pressed = 'right'
        pass

    def left_bumper(self, *_args):
        self.feet_pressed = 'left'
        pass
