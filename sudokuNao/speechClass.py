from naoqi import ALProxy
import time

class Speech:
    tts = ALProxy("ALTextToSpeech", "169.254.35.27", 9559)

    def __init__(self):
        tts.setVolume(0.8)

    # outputs the intro monologue
    def introSpeech(self):
        tts.say("Hello! Welcome to Sudoku NAO 101!")
        tts.say("Let me read your sudoku before we start.")
        tts.say("Then I can give you the full answer or help you with hints")
        tts.say("Lets go party.")

    # outputs all the functions the nao can provide to the player
    def instructionMenu(self):
        tts.say("Lets go party.")

    # gets a sudoku and a tuple with coordinates of a field
    # outputs the digit on that field
    def getHint(self, sudoku, coordinates):
        x,y = coordinates
        digit = sudoku[x][y]
        tts.say("The digit on that cell is", digit)

    # outputs the whole sudoku
    def getFullAnswer(self, sudoku):
        tts.say("Okay. I will now say all the right digits from the top left corner down to the bottom right corner.")
        for x in range(9):
            for y in range(9):
                digit = sudoku[x][y]
                tts.say(digit)
                time.sleep(5)

        tts.say("Lets go party.")

    # set the new volume (type double) in range [0-1]
    def setVolume(self, volume):
        if (volume >= 0 and volume <=1.0):
            tts.setVolume(volume);
        else:
            tts.say("My volume could not be changed correctly.");


class SudokuNao:
    def __init__(self, sudoku):
        self.sudoku = sudoku
