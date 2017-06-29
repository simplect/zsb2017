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
from sensors.feet import Feet

from random import randint

# SET-UP
IP = '169.254.131.247'
PORT = 9559


# We need this broker to be able to construct
# NAOqi modules and subscribe to other modules
# The broker must stay alive until the program exists
myBroker = ALBroker("carlosBroker",
   "0.0.0.0",   # listen to anyone
   0,           # find a free port and use it
   IP,         # parent broker IP
   PORT)       # parent broker port

# AL MODULES
global humanEventWatcher
global feetWatcher

humanEventWatcher = HumanTrackedEventWatcher()
feetWatcher = Feet()
# Normal classes
speech = Speech()
idle = IdleBehaviour()
move = Move()
vision = Vision()


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
    while True:
        time.sleep(2)
        while humanEventWatcher.current_name:
            speech.current_name = humanEventWatcher.current_name
            speech.current_name = "Merin"

            begin = True
            end = False
            oldSudoku = []

            speech.introSpeech()

            if feetWatcher.registerQuestion():
                speech.askForSudoku()
                idle.stand()
                idle.basic_awareness.stopAwareness()
                idle.stopForScan()
                scans = sudoku_searcher(require_answer=True)
                idle.resume()
                sudoku = SudokuNao(scans)

                while True:
                    sudoku.printArrays()
                    end = sudoku.checkIfEnd(sudoku.sudoku)
                    speech.askForSquare(begin, end)

                    """
                    if oldSudoku != sudoku.sudoku:
                        speech.askForSquare(begin, end)
                    else:
                        speech.notFilledAnythingIn()
                        """
                    oldSudoku = sudoku.sudoku
                    if feetWatcher.registerQuestion():
                        speech.askForCheck()
                        idle.stopForScan()
                        scans = sudoku_searcher(prev = sudoku.sudoku)
                        idle.resume()
                        sudoku.updateSudoku(scans[0])
                        if sudoku.answerIsCorrect():
                            speech.rightAnswer()
                        else:
                            sudoku.printArrays()
                            speech.wrongAnswerGetHint(sudoku.sudoku)
                    else:
                        speech.giveHint(sudoku.sudoku)
                if end:
                    aup = ALProxy('ALAudioPlayer')
                    song = aup.post.playFile("/home/nao/songs/happy.wav")
                    #move.randomDancing()
                    feet.doRasta()

                    time.sleep(60)
                    aup.stopAll()
                    break
            else:
                print("game not entered")
                humanEventWatcher.findNewHuman()
    while True:
        time.sleep(5)

except KeyboardInterrupt:
    print
    print "Interrupted by user, shutting down"
    humanEventWatcher.sayGoodbye()
    idle.sleep()
    myBroker.shutdown()
    sys.exit(0)
