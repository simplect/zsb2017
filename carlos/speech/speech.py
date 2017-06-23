from naoqi import ALProxy
import time
from random import randint

class Speech:

    # sets the volume to a default value
    def __init__(self, IP, PORT):
        self.tts = ALProxy("ALTextToSpeech", IP, PORT)
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

    def getRandomHint(self):
        randNum = randint(0,4)
        if (randNum == 0):
            self.tts.say("Have you already looked at the most filled in row, column or square?")

        elif (randNum == 1):
            self.tts.say("Maybe you have to think one step ahead. Look which numbers' locations in a row, column or square are blocked by the numbers in the already filled in fields.")

        elif (randNum == 2):
            self.tts.say("Which specific numbers are missing in the row, column or square you are looking at?")

        elif (randNum == 3):
            self.tts.say("Look at three squares and see if there are two identical numbers in two of the squares. Maybe you can fill in this number in the third square?")


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
        self.tts.say("Here's a tip: maybe you can fill out number"+ str(digit));

class Dialoge:
    def __init__(self):
        self.tts.say("Let's go play.")

    def chooseRightAnswer(self):
        self.tts.say("Let's go play.")

class SudokuNao:
    def __init__(self, strings):
        self.startSudoku = self.makeSudokuArray(strings[0])
        self.endSudoku = self.makeSudokuArray(strings[1])

    def printArrays(self):
        print("The start sudoku is: ")
        for x in self.startSudoku:
            print(x)
        print("The solved sudoku is: ")
        for x in self.endSudoku:
            print(x)

    def checkDigit(self, sudoku):
        best_count = 0
        for i in range(1,10):
            count = counter(i, sudoku)
            if count > best_count and count < 9:
                best_count = count
        return best_count

    def counter(self, number, sudoku):
        count = 0
        for i in range(9):
            for j in range(9):
                value = sudoku[i][j]
                if value == number:
                    count += 1
        return count

    def makeSudokuArray(self, sudokuStr):
        sudokuArray = []
        for n in range(9):
            substr = sudokuStr[(n*9):((n+1)*9)]
            rowArray = []
            for x in substr:
                rowArray.append(int(x))
            sudokuArray.append(rowArray)
        return sudokuArray