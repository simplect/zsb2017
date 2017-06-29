import os
import time
from naoqi import ALProxy, ALModule

class HumanTrackedEventWatcher(ALModule):
    """ A module to react to HumanTracked and PeopleLeft events """

    current_name = None
    names_seen = []

    def __init__(self):
        ALModule.__init__(self, "humanEventWatcher")

        global memory
        memory = ALProxy("ALMemory")
        self.face_det = ALProxy("ALFaceDetection")
        self.face_det.setTrackingEnabled(False)
        self.face_char = ALProxy("ALFaceCharacteristics")

        self.tts = ALProxy("ALTextToSpeech")
#        self.face_det.forgetPerson("Merin")

        self.people = ALProxy("ALPeoplePerception")
        memory.subscribeToEvent("ALBasicAwareness/HumanTracked",
                                "humanEventWatcher",
                                "onHumanTracked")
        memory.subscribeToEvent("ALBasicAwareness/PeopleLeft",
                                "humanEventWatcher",
                                "onPeopleLeft")
        memory.subscribeToEvent("FaceDetected",
            "humanEventWatcher",
            "onFaceDetected")
        memory.subscribeToEvent("FaceCharacteristics/PersonSmiling",
            "humanEventWatcher",
            "onSmileDetected")

    def onHumanTracked(self, key, value, msg):
        """ callback for event HumanTracked """
        print "got HumanTracked: detected person with ID:", str(value)
        if value >= 0:  # found a new person
            position_human = self.get_people_perception_data(value)
            [x, y, z] = position_human
            print "The tracked person with ID", value, "is at the position:", \
                "x=", x, "/ y=",  y, "/ z=", z
        else:
            self.findNewHuman()

    def onPeopleLeft(self, key, value, msg):
        """ callback for event PeopleLeft """
        print "got PeopleLeft: lost person", str(value)

    def onFaceDetected(self, key, value, msg):
        """ callback for event PeopleLeft """
        try:
            name = value[1][0][1][2]
        except IndexError:
            return
        memory.unsubscribeToEvent("FaceDetected",
                                   "humanEventWatcher")

        if len(name) and name != self.current_name:
            print "Detected ", name
            self.tts.say("Hi there {}, good to see you again.".format(name))
            self.current_name = name
            self.seen_names.append(name)
            self.face_det.setTrackingEnabled(True)

        memory.subscribeToEvent("FaceDetected",
            "humanEventWatcher",
            "onFaceDetected")

    def get_people_perception_data(self, id_person_tracked):
        memory = ALProxy("ALMemory", self.ip, self.port)
        memory_key = "PeoplePerception/Person/" + str(id_person_tracked) + \
                     "/PositionInWorldFrame"
        return memory.getData(memory_key)


    def onSmileDetected(self, *_args):
        """ Smile event
        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("FaceCharacteristics/PersonSmiling",
            "humanEventWatcher")

        if self.current_name:
            self.tts.say("{}, you have such a cute smile.".format(self.current_name))
            print("Like event")
            time.sleep(30)

        # Subscribe again to the event
        memory.subscribeToEvent("FaceCharacteristics/PersonSmiling",
            "face_detection",
            "onSmileDetected")

    def sayGoodbye(self):
        if self.current_name:
            
            self.tts.say("Goodbye {}".format(self.current_name))
    
    def findNewHuman(self):
            self.current_name = None
            self.face_det.setTrackingEnabled(False)

    def learnNewHuman(self, name):
            self.face_det.learnFace(name)
            print("Learned new face")


