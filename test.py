from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "169.254.35.27", 9559)
for i in range(3):
    tts.say("hannah")
