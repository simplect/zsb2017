import os
import time
from naoqi import ALProxy, ALModule


class IdleBehaviour:

    # sets the volume to a default value
    def __init__(self, IP, PORT):
        self.posture = ALProxy("ALRobotPosture", IP, PORT)
        self.motion = ALProxy("ALMotion", IP, PORT)
        self.basic_awareness = ALProxy("ALBasicAwareness", IP, PORT)

        print("Waking up")
        self.motion.wakeUp()
        self.basic_awareness.startAwareness()
        self.basic_awareness.setEngagementMode("FullyEngaged")

    def test(self):
         # Send robot to Pose Init
         self.posture.goToPosture("StandInit", 0.5)
         self.motion.wbEnable(True)
         # Example showing how to com go to LLeg.
         supportLeg = "LLeg"
         duration   = 2.0
         self.motion.wbGoToBalance(supportLeg, duration)
         supportLeg = "RLeg"
         duration   = 2.0
         self.motion.wbGoToBalance(supportLeg, duration)
         self.motion.wbEnable(False)

    def doFunny(self):
        pass

    def sit(self):
        self.posture.goToPosture("Sit", 1.0)

    def sitRelax(self):
        self.posture.goToPosture("SitRelax", 1.0)

    def stand(self):
        self.posture.goToPosture("Stand", 1.0)

    def crouch(self):
        self.posture.goToPosture("Crouch", 1.0)

    def sleep(self):
        print("Sleeping")
        self.basic_awareness.stopAwareness()
        self.motion.rest()

    def startIdling(self, idling):
        while idling:
            print("tudele")
            # TODO: Write some funny things here
            time.sleep(20)







