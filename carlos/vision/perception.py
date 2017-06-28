import os
import time
from naoqi import ALProxy, ALModule

class HumanTrackedEventWatcher(ALModule):
    """ A module to react to HumanTracked and PeopleLeft events """

    current_name = None

    def __init__(self, IP, PORT):
        self.ip = IP
        self.port = PORT
        ALModule.__init__(self, "humanEventWatcher")

        global memory
        memory = ALProxy("ALMemory", IP, PORT)
        self.face_det = ALProxy("ALFaceDetection")
        self.face_char = ALProxy("ALFaceCharacteristics")

        self.tts = ALProxy("ALTextToSpeech")
        #self.face_det.forgetPerson("Merijn")

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
            #self.face_det.learnFace("Hannah")
            #print("Learned new face")
        else:
            self.current_name = None

    def onPeopleLeft(self, key, value, msg):
        """ callback for event PeopleLeft """
        print "got PeopleLeft: lost person", str(value)

    def onFaceDetected(self, key, value, msg):
        """ callback for event PeopleLeft """
        name = value[1][0][1][2]
        memory.unsubscribeToEvent("FaceDetected",
                                   "humanEventWatcher")

        if len(name) and name != self.current_name:
            print "Detected ", name
            self.tts.say("Hi there {}, good to see you again.".format(name))
            self.current_name = name

        memory.subscribeToEvent("FaceDetected",
            "humanEventWatcher",
            "onFaceDetected")

    def get_people_perception_data(self, id_person_tracked):
        memory = ALProxy("ALMemory", self.ip, self.port)
        memory_key = "PeoplePerception/Person/" + str(id_person_tracked) + \
                     "/PositionInWorldFrame"
        return memory.getData(memory_key)

    def onSmileDetected(self, *_args):
        """ This will be called each time a face is
        detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("FaceCharacteristics/PersonSmiling",
            "humanEventWatcher")
        if self.current_name:
            self.tts.say("{}, you have such a cute smile.".format(self.current_name))
            print("like event")
            time.sleep(30)
            # Subscribe again to the event
        memory.subscribeToEvent("FaceCharacteristics/PersonSmiling",
            "face_detection",
            "onSmileDetected")

    def sayGoodbye(self):
        if self.current_name:
            self.tts.say("Goodbye {}".format(self.current_name))
