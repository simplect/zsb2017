import os
import time
from naoqi import ALProxy, ALModule


class Posture:

    # sets the volume to a default value
    def __init__(self):
        self.posture = ALProxy("ALRobotPosture")
        self.motion = ALProxy("ALMotion")
        self.basic_awareness = ALProxy("ALBasicAwareness")

        self.motion.wakeUp()

        self.posture.goToPosture("StandInit", 0.7)

        self.resume()

    def stop_for_scan(self):
        self.basic_awareness.stopAwareness()
        self.stand()

        # Example showing multiple trajectories
        # Interpolate the head yaw to 1.0 radian and back to zero in 2.0 seconds
        # while interpolating HeadPitch up and down over a longer period.
        names  = ["RHipPitch","LHipPitch", "HeadPitch", "RAnklePitch", "RAnkleRoll"]
        # Each joint can have lists of different lengths, but the number of
        # angles and the number of times must be the same for each joint.
        # Here, the second joint ("HeadPitch") has three angles, and
        # three corresponding times.
        angleLists  = [[-1.0], [-1.0], [-0.4], [0.154], [0.192]]
        timeLists   = [[3.0], [3.0], [3.0], [3.0], [3.0]]
        isAbsolute  = True
        self.motion.angleInterpolation(names, angleLists, timeLists, isAbsolute)

    def resume(self):
        self.basic_awareness.startAwareness()
        self.basic_awareness.setEngagementMode("FullyEngaged")
        self.stand()

    def sit(self):
        self.posture.goToPosture("Sit", 0.7)

    def sit_relax(self):
        self.posture.goToPosture("SitRelax", 0.7)

    def stand(self):
        self.posture.goToPosture("Stand", 0.6)

    def crouch(self):
        self.posture.goToPosture("Crouch", 0.7)

    def sleep(self):
        print("Sleeping")
        self.basic_awareness.stopAwareness()
        self.motion.rest()

    def start_idling(self, idling):
        while idling:
            print("tudele")
            # TODO: Write some funny things here
            time.sleep(20)
