import os
import time
import motion
from naoqi import ALProxy, ALModule


class Move:

    # sets the volume to a default value
    def __init__(self):
        self.motion = ALProxy("ALMotion")

    def walkForward(self):
        self.motion.moveInit()
        self.motion.moveTo(0.5, 0, 0)

    def move_arms(self):
        chainName = "RArm"
        frame     = motion.FRAME_ROBOT
        useSensor = False

        effectorInit = self.motion.getPosition(chainName, frame, useSensor)

        # Active LArm tracking
        isEnabled = True
        self.motion.wbEnableEffectorControl(chainName, isEnabled)

        # Example showing how to set position target for LArm
        # The 3 coordinates are absolute LArm position in FRAME_ROBOT
        # Position in meter in x, y and z axis.

        # X Axis LArm Position feasible movement = [ +0.00, +0.12] meter
        # Y Axis LArm Position feasible movement = [ -0.05, +0.10] meter
        # Y Axis RArm Position feasible movement = [ -0.10, +0.05] meter
        # Z Axis LArm Position feasible movement = [ -0.10, +0.10] meter

        coef = 1.0
        if chainName == "LArm":
            coef = +1.0
        elif chainName == "RArm":
            coef = -1.0

        targetCoordinateList = [
        [ +0.12, +0.00*coef, +0.00], # target 0
        [ +0.12, +0.00*coef, -0.10], # target 1
        [ +0.12, +0.05*coef, -0.10], # target 1
        [ +0.12, +0.05*coef, +0.10], # target 2
        [ +0.12, -0.10*coef, +0.10], # target 3
        [ +0.12, -0.10*coef, -0.10], # target 4
        [ +0.12, +0.00*coef, -0.10], # target 5
        [ +0.12, +0.00*coef, +0.00], # target 6
        [ +0.00, +0.00*coef, +0.00], # target 7
        ]

        # wbSetEffectorControl is a non blocking function
        # time.sleep allow head go to his target
        # The recommended minimum period between two successives set commands is
        # 0.2 s.
        for targetCoordinate in targetCoordinateList:
            targetCoordinate = [targetCoordinate[i] + effectorInit[i] for i in range(3)]
            self.motion.wbSetEffectorControl(chainName, targetCoordinate)
            time.sleep(4.0)

        # Deactivate Head tracking
        isEnabled    = False
        self.motion.wbEnableEffectorControl(chainName, isEnabled)
