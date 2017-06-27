from sudoku.main import solve
import time
import sys
import threading
from naoqi import ALBroker, ALProxy
from speech.speech import Speech, SudokuNao
from behaviour.idle import IdleBehaviour, HumanGreeterModule, HumanTrackedEventWatcher
from behaviour.move import Move
from vision.image import Vision
from random import randint

# SET-UP
IP = '169.254.236.47'
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
"""
# Global variable to store the HumanGreeter module instance
HumanGreeter = None
memory = None

# Warning: HumanGreeter must be a global variable
# The name given to the constructor must be the name of the
# variable
global HumanGreeter
global humanEventWatcher

HumanGreeter = HumanGreeterModule("HumanGreeter")
humranEventWatcher = HumanTrackedEventWatcher(IP,PORT)
"""

# Thread functions
def sudoku_searcher(require_answer = False):
    print("Started sudoku searcher")
    solution = (False, False)
    while not solution[0]:
        vision.getImage("sudoku.jpg")
        solution = solve("sudoku.jpg")
        if solution[0] \
            and sudoku.countZeros(sudoku.makeSudokuArray(solution[0])) > 70:
            solution = (False, False)
            continue
        if not solution[1] and require_answer:
            solution = (False, False)
            continue

    return solution

# MAIN CARLOS
try:
    while True:
        begin = True
        end = False
        sp.introSpeech()
        saysYes = lambda : True
        if saysYes():
            speech.askForSudoku()
            scans = sudoku_searcher(require_answer=True)
            sudoku = SudokuNao(scans)
            while(True):
                end = sudoku.checkIfEnd(sudoku.sudoku)
                speech.askForSquare(begin, end)
                if saysYes():
                    speech.askForCheck()
                    scans = sudoku_searcher()
                    sudoku.updateSudoku(scans[0])
                    if sn.answerIsCorrect():
                        speech.rightAnswer()
                    else:
                        speech.wrongAnswerGetHint(sudoku.sudoku)
                else:
                    speech.giveHint(sudoku.sudoku)
            if end:
                #randomDancing()
                break
        else:
            print("game not entered")



except KeyboardInterrupt:
    print
    print "Interrupted by user, shutting down"
    myBroker.shutdown()
    idle.sleep()
    sys.exit(0)
