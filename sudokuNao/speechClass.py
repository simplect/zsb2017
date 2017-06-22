from naoqi import ALProxy
import time

class Speech:
    tts = ALProxy("ALTextToSpeech", "169.254.28.133", 9559)

    # sets the volume to a default value
    def __init__(self):
        self.tts.setVolume(0.8)

    # outputs the intro monologue
    def introSpeech(self):
        self.tts.say("Hello!")
        self.tts.say("Let me see your sudoku puzzle before we start.")

    # outputs all the functions the nao can provide to the player
    def instructionMenu(self):
        self.tts.say("There are a few things I can do for you.")
        self.tts.say("I can give you general sudoku solving techniques or I can give you a general hint.")
        self.tts.say("Furthermore, you can ask me for a digit in a cell and I will give it to you.")
        self.tts.say("Lastly, I can give you the full answer of the sudoku")

    def seenSudoku(self):
        self.tts.say("Great! I have seen your sudoku.")
        self.tts.say("Now I can help you with hints or give you the full answer.")
        self.tts.say("Let's go play.")


    # gets a sudoku and a tuple with coordinates of a field
    # outputs the digit on that field
    def getHint(self, sudoku, coordinates):
        row,col = coordinates
        digit = sudoku[row][col]
        self.tts.say("The digit on that cell is "+str(digit))

    def readSudoku(self, sudoku):
        self.tts.say("Okay. I will now read all the digits from the top left corner down to the bottom right corner.")
        for row in range(9):
            for col in range(9):
                digit = sudoku[row][col]
                if digit == 0:
                    self.tts.say("empty")
                else:
                    self.tts.say(str(digit))

    # set the new volume (type double) in range [0-1]
    def setVolume(self, volume):
        if (volume >= 0 and volume <=1.0):
            self.tts.setVolume(volume);
        else:
            self.tts.say("My volume could not be changed correctly.");

    def checkThisDigit(self, digit):



class SudokuNao:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def checkDigit(self, sudoku):
        digit = 0
        return digit

def main():
    sp = Speech()
    sudoku = [[3,0,0,0,8,0,0,0,6],[0,1,0,0,0,6,0,2,0],[0,0,4,7,0,0,5,0,0],[0,4,0,0,1,0,9,0,0],[6,0,0,2,0,4,0,0,1],[0,0,3,0,6,0,0,5,0],[0,0,8,0,0,3,6,0,0],[0,2,0,4,0,0,0,1,0],[5,0,0,0,2,0,0,0,7]]
    #sp.introSpeech()
    #sp.instructionMenu()
    sp.getFullAnswer(sudoku)

if __name__=='__main__':
    main()
