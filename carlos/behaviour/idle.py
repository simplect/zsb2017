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



class HumanGreeterModule(ALModule):
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")
        self.face = ALProxy("ALFaceCharacteristics")
        print(self.face.setSmilingThreshold(0.5))

        # Subscribe to the FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("FaceCharacteristics/PersonSmiling",
            "HumanGreeter",
            "onFaceDetected")

    def onFaceDetected(self, *_args):
        """ This will be called each time a face is
        detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("FaceCharacteristics/PersonSmiling",
            "HumanGreeter")

        self.tts.say("I like that you like it")
        print("like event")

        # Subscribe again to the event
        memory.subscribeToEvent("FaceCharacteristics/PersonSmiling",
            "HumanGreeter",
            "onFaceDetected")

class HumanTrackedEventWatcher(ALModule):
    """ A module to react to HumanTracked and PeopleLeft events """

    def __init__(self, IP, PORT):
        self.ip = IP
        self.port = PORT
        ALModule.__init__(self, "humanEventWatcher")
        global memory
        memory = ALProxy("ALMemory", IP, PORT)
        memory.subscribeToEvent("ALBasicAwareness/HumanTracked",
                                "humanEventWatcher",
                                "onHumanTracked")
        memory.subscribeToEvent("ALBasicAwareness/PeopleLeft",
                                "humanEventWatcher",
                                "onPeopleLeft")
        #self.speech_reco = ALProxy("ALSpeechRecognition", IP, PORT)
#        self.is_speech_reco_started = False

    def onHumanTracked(self, key, value, msg):
        """ callback for event HumanTracked """
        print "got HumanTracked: detected person with ID:", str(value)
        if value >= 0:  # found a new person
#            self.start_speech_reco()
            position_human = self.get_people_perception_data(value)
            [x, y, z] = position_human
            print "The tracked person with ID", value, "is at the position:", \
                "x=", x, "/ y=",  y, "/ z=", z

    def onPeopleLeft(self, key, value, msg):
        """ callback for event PeopleLeft """
        print "got PeopleLeft: lost person", str(value)
#        self.stop_speech_reco()

    def start_speech_reco(self):
        """ start asr when someone's detected in event handler class """
        if not self.is_speech_reco_started:
            try:
                self.speech_reco.setVocabulary(["yes", "no"], False)
            except RuntimeError:
                print "ASR already started"
            self.speech_reco.setVisualExpression(True)
            self.speech_reco.subscribe("BasicAwareness_Test")
            self.is_speech_reco_started = True
            print "start ASR"

    def stop_speech_reco(self):
        """ stop asr when someone's detected in event handler class """
        if self.is_speech_reco_started:
            self.speech_reco.unsubscribe("BasicAwareness_Test")
            self.is_speech_reco_started = False
            print "stop ASR"

    def get_people_perception_data(self, id_person_tracked):
        memory = ALProxy("ALMemory", self.ip, self.port)
        memory_key = "PeoplePerception/Person/" + str(id_person_tracked) + \
                     "/PositionInWorldFrame"
        return memory.getData(memory_key)
