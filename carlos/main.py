from sudoku.main import solve
import time
import sys
import threading
from naoqi import ALBroker, ALProxy
from speech.speech import Speech, SudokuNao
from behaviour.idle import IdleBehaviour
from behaviour.move import Move
from vision.image import Vision
from vision.perception import HumanTrackedEventWatcher

from random import randint

# SET-UP
IP = '169.254.65.64'
PORT = 9559

speech = Speech(IP, PORT)
idle = IdleBehaviour(IP, PORT)
move = Move(IP, PORT)
vision = Vision(IP, PORT)

# We need this broker to be able to construct
# NAOqi modules and subscribe to other modules
# The broker must stay alive until the program exists
myBroker = ALBroker("myBroker",
   "0.0.0.0",   # listen to anyone
   0,           # find a free port and use it
   IP,         # parent broker IP
   PORT)       # parent broker port

# Global variable to store the FaceDetection module instance
memory = None

# Warning: FaceDetection must be a global variable
# The name given to the constructor must be the name of the
# variable
global humanEventWatcher

humanEventWatcher = HumanTrackedEventWatcher(IP,PORT)

# Thread functions
def sudoku_searcher(require_answer = False, prev = False):
    print("Started sudoku searcher")
    solution = (False, False)
    sudoku = SudokuNao(([],[]))
    while not solution[0]:
        vision.getImage("sudoku.jpg")
        solution = solve("sudoku.jpg")
        if not solution[0] \
                or sudoku.countZeros(sudoku.makeSudokuArray(solution[0])) > 70:
            solution = (False, False)
            continue
        if not solution[1] and require_answer:
            solution = (False, False)
            continue
        if prev:
            new_sudoku = sudoku.makeSudokuArray(solution[0])
            for x in range(9):
                for y in range(9):
                    if prev[x][y] != 0 and\
                        prev[x][y] != new_sudoku[x][y]:
                            solution = (False, False)

    return solution

# MAIN CARLOS
try:
    while False:
        begin = True
        end = False
        speech.introSpeech()
        saysYes = lambda : True
        if saysYes():
            speech.askForSudoku()
            scans = sudoku_searcher(require_answer=True)
            sudoku = SudokuNao(scans)

            while True:
                sudoku.printArrays()
                end = sudoku.checkIfEnd(sudoku.sudoku)
                speech.askForSquare(begin, end)
                if saysYes():
                    speech.askForCheck()
                    scans = sudoku_searcher(prev = sudoku.sudoku)

                    sudoku.updateSudoku(scans[0])
                    if sudoku.answerIsCorrect():
                        speech.rightAnswer()
                    else:
                        sudoku.printArrays()
                        speech.wrongAnswerGetHint(sudoku.sudoku)
                else:
                    speech.giveHint(sudoku.sudoku)
            if end:
                #randomDancing()
                break
        else:
            print("game not entered")
    while True:
        time.sleep(5)

except KeyboardInterrupt:
    print
    print "Interrupted by user, shutting down"
    humanEventWatcher.sayGoodbye()
    myBroker.shutdown()
    idle.sleep()
    sys.exit(0)
