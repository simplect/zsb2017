import os
import time
from naoqi import ALProxy, ALModule

global human

class Human(ALModule):
    """ A module to react to HumanTracked and PeopleLeft events """

    current_name = None
    names_seen = []

    def __init__(self):
        ALModule.__init__(self, "human")

        global memory

        memory = ALProxy("ALMemory")
        self.face_det = ALProxy("ALFaceDetection")
        self.face_det.setTrackingEnabled(False)

        self.face_char = ALProxy("ALFaceCharacteristics")

        self.tts = ALProxy("ALTextToSpeech")

        self.people = ALProxy("ALPeoplePerception")

        memory.subscribeToEvent("ALBasicAwareness/HumanTracked",
                                "human",
                                "on_human_tracked")

        memory.subscribeToEvent("ALBasicAwareness/PeopleLeft",
                                "human",
                                "on_people_left")

        memory.subscribeToEvent("FaceDetected",
            "human",
            "on_face_detected")

        memory.subscribeToEvent("FaceCharacteristics/PersonSmiling",
            "human",
            "on_smile_detected")

    def on_human_tracked(self, key, value, msg):
        """ callback for event HumanTracked """
        if value >= 0:  # found a new person
            print "Tracked person with ID: {}".format(value)
        else:
            self.find_new()

    def on_people_left(self, key, value, msg):
        """ callback for event PeopleLeft """
        print "got PeopleLeft: lost person ID: {}".format(value)

    def on_face_detected(self, eventName, value):
        """ callback for event PeopleLeft """
        
        try:
            name = value[1][0][1][2]
        except IndexError:
            return

        if len(name) \
                and name != self.current_name \
                and name not in self.names_seen:
            self.current_name = name
            self.names_seen.append(name)
            self.face_det.setTrackingEnabled(True)

    def on_smile_detected(self, *_args):
        """ Smile event
        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("FaceCharacteristics/PersonSmiling",
            "human")

        if self.current_name:
            self.tts.say("{}, you have such a cute smile.".format(self.current_name))
            print("Like event")
            time.sleep(30)

        # Subscribe again to the event
        memory.subscribeToEvent("FaceCharacteristics/PersonSmiling",
            "human",
            "on_smile_detected")

    def find_new(self):
            self.current_name = None
            self.face_det.setTrackingEnabled(False)

    def learn_new_human(self, name):
            self.face_det.learnFace(name)
            print("Learned new face")
