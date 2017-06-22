from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "169.254.35.27", 9559)
print(tts.getVolume())
tts.setVolume(0.5)
tts.say("Lets go party.")
