import os
import time
from naoqi import ALProxy, ALModule


class Move:

    # sets the volume to a default value
    def __init__(self, IP, PORT):
        self.motion = ALProxy("ALMotion", IP, PORT)

    def walkForward(self):
        self.motion.moveInit()
        self.motion.moveTo(0.5, 0, 0)

