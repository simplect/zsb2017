form naoqi import ALProxy

class Speech:
    tts = ALProxy("ALTextToSpeech", "169.254.35.27", 9559)

    def __init__(self):
        tts.setVolume(0.8)

    def introSpeech(self):
        tts.say("Hello! Welcome to Sudoku NAO 101!")
        tts.say("Let me read your sudoku before you start.")
        tts.say("Then I can give you the full answer or help you with hints")
        tts.say("Lets go party.")

    def instructionMenu(self):
        tts.say("Lets go party.")

    def getHint(self, sudoku):
        tts.say("Lets go party.")

    def getFullAnswer(self, sudoku):
        tts.say("Lets go party.")

    # set the new volume (type double) in range [0-1]
    def setVolume(self, volume):
        if (volume >= 0 and volume <=1.0) {
            tts.setVolume(volume);
        } else {
            tts.say("My volhume could not be changed correctly.");
        }

class SudokuNao:
    def __init__(self, sudoku):
        self.sudoku = sudoku
