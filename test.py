from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "169.254.206.144", 9559)
for i in range(3):
    tts.say("piew")
