from naoqi import ALProxy
import time
from random import randint

class Speech:

    # sets the volume to a default value
    def __init__(self, IP, PORT):
        self.tts = ALProxy("ALTextToSpeech", IP, PORT)
        self.animated_speech = ALProxy("ALAnimatedSpeech", IP, PORT)
        self.tts.setVolume(0.8)

    # outputs the intro monologuew
    def introSpeech(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/You_1) Hey! Do you want to make a sudoku with me?")

    def askForSudoku(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_1) Let me see your sudoku puzzle before we start. ^stop(animations/Stand/Gestures/Explain_1)")

    def askForCheck(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_1) Write it down and show it to me, please! I can check it for you!")

    def wrongAnswerGetHint(self, sudoku):
        self.animated_speech.say("^start(animations/Stand/Emotions/Neutral/Embarrassed_1) Oops! I think you made a mistake. Do you want a hint?")
        while(True):
            self.giveHint()
            randNum = randint()
            if randNum == 1:
                self.getRandomHint()
            elif randNum == 2:
                digit = SudokuNao.checkDigit(sudoku)
                self.checkThisDigit(digit)
            self.askForSquare(False, False)
            if saysYes():
                pass
                # if correctAnswer():
                    # self.rightAnswer()
                    #break
                # else:
                    #continue
            else:
                continue

    def rightAnswer(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Yes_1) Well done!")

    def askForSquare(self, begin, end):
        if begin == True:
            self.seenSudoku()
            begin == False
        elif end == True:
            self.lastSquare()
        else:
            self.animated_speech.say("^start(animations/Stand/Gestures/Enthusiastic_5) Can you fill in another square?")

    def giveHint(self, sudoku):
        self.animated_speech.say("^start(animations/Stand/Gestures/ShowSky_1) Let me give you a hint.")
        randNum = randint()
        if randNum == 1:
            sp.getRandomHint()
        elif randNum == 2:
            digit = SudokuNao.checkDigit(sudoku)
            sp.checkThisDigit(digit)

    def lastSquare(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Enthusiastic_3) Only one box to go!")

    # outputs all the functions the nao can provide to the player
    def instructionMenu(self):
        self.tts.say("There are a few things I can do for you.")
        self.tts.say("I can give you general sudoku solving techniques or I can give you a general hint.")
        self.tts.say("Furthermore, you can ask me for a digit in a cell and I will give it to you.")
        self.tts.say("Lastly, I can give you the full answer of the sudoku")

    # nao confirms it has seen the sudoku
    def seenSudoku(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Hey_1) Nice one! Can you fill in a square already?")

    # outputs the general rules of the sudoku game
    def getGameRules(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_7) To complete your sudoku correctly, you must fill in al the empty squares.")
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_8) When you are finished, the numbers 1 to 9 must appear exactly once in each row, column and box.")
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_5) During the game, you must keep this in mind and use this knowledge to your advantage, while filling in squares.")

    # gives one of the four random hints
    def getRandomHint(self):
        randNum = randint(0,4)
        if randNum == 0:
            self.tts.say("^start(animations/Stand/Gestures/YouKnowWhat_1) Have you already looked at the most filled in row, column or box?")

        elif randNum == 1:
            self.tts.say("^start(animations/Stand/Gestures/YouKnowWhat_5) Maybe you have to think one step ahead. Look which numbers' locations in a row, column or box are blocked by the numbers in the already filled in squares.")

        elif randNum == 2:
            self.tts.say("^start(animations/Stand/Gestures/YouKnowWhat_1) Which specific numbers are missing in the row, column or box you are looking at?")

        elif randNum == 3:
            self.tts.say("^start(animations/Stand/Gestures/YouKnowWhat_5) Look at three boxes and see if there are two identical numbers in two of the boxes. Maybe you can fill in this number in the third box?")


    # gets a sudoku and a tuple with coordinates of a square
    # outputs the digit on that square
    def getHint(self, sudoku, coordinates):
        row,col = coordinates
        digit = sudoku[row][col]
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_3) The digit on that cell is "+str(digit))

    # reads aloud the given sudoku
    def readSudoku(self, sudoku):
        self.tts.say("^start(animations/Stand/Gestures/Me_1) Okay. I will now read all the digits from the top left corner down to the bottom right corner.")
        for row in range(9):
            for col in range(9):
                digit = sudoku[row][col]
                if digit == 0:
                    self.tts.say("empty")
                else:
                    self.tts.say(str(digit))

    # set the new volume (type double) in range [0-1]
    def setVolume(self, volume):
        if volume >= 0 and volume <=1.0:
            self.tts.setVolume(volume);
        else:
            self.tts.say("My volume could not be changed correctly.");

    # tells the player to look at a given number
    def checkThisDigit(self, digit):
        self.tts.say("Here's a tip: maybe you can fill out number"+ str(digit));

    # asks if the player is sure of his question
    def checkIfSure(self):
        self.tts.say("Are you sure you want me to tell you?");

    # tells player the nao didn't understand the message
    def didNotUnderstand(self):
        self.tts.say("Sorry, I didn't understand");

    # says okay
    def okay(self):
        self.tts.say("Okay.");


class Dialoge:
    def __init__(self, IP, PORT):
        self.speech = Speech(IP, PORT)

    # chooses the right response according to the audio input
    def chooseRightAnswer(self, sudoku, sentence, row, col, volume):
        if sentence == "give random hint":
            self.speech.getRandomHint()
        elif sentence == "give instructions" or sentence == "what can you help me with":
            self.speech.instructionMenu()
        elif sentence == "rules":
            self.speech.getGameRules()
        elif sentence == "give hint":
            digit = SudokuNao.checkDigit(sudoku)
            self.speech.checkThisDigit(digit)
        elif sentence == "full answer":
            self.speech.checkIfSure()
            # if speechRecognition.checkIfSure() == True:
            self.speech.readSudoku(sudoku)
            # else:
            # self.speech.okay()
        elif row != None and col != None:
            self.speech.getHint(sudoku, (row, col))
        elif volume != None:
            self.speech.setVolume(volume)
        else:
            self.speech.didNotUnderstand()


class SudokuNao:
    def __init__(self, strings):
        self.sudoku = self.makeSudokuArray(strings[0])
        self.sudokuAnswer = self.makeSudokuArray(strings[1])

    def updateSudoku(self, string):
        self.sudoku = self.makeSudokuArray(string)

    def answerIsCorrect(self):
        for x in range(9):
            for y in range(9):
                if self.sudoku[x][y] == 0:
                    continue
                if self.sudoku[x][y] != self.sudokuAnswer[x][y]:
                    return False
        return True

    def printArrays(self):
        print("The start sudoku is: ")
        for x in self.sudoku:
            print(x)
        print("The solved sudoku is: ")
        for x in self.sudokuAnswer:
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

    def countZeros(self, sudoku):
        # Works with a string for now
        numZeros = 0
        for x in range(9):
            for y in range(9):
                if sudoku[x][y] == 0:
                    numZeros += 1
        return numZeros

    def checkIfEnd(self, sudoku):
        if self.countZeros(sudoku) == 1:
            return True
        return False
