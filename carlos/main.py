#from sudoku.main import solve
import time
import sys
import threading
from naoqi import ALBroker, ALProxy
from speech.speech import Speech, SudokuNao
from behaviour.idle import IdleBehaviour, HumanGreeterModule, HumanTrackedEventWatcher
from behaviour.move import Move
#from vision.image import Vision
from random import randint

# SET-UP
IP = '169.254.236.47'
PORT = 9559

speech = Speech(IP, PORT)
idle = IdleBehaviour(IP, PORT)
move = Move(IP, PORT)
#vision = Vision(IP, PORT)


# We need this broker to be able to construct
# NAOqi modules and subscribe to other modules
# The broker must stay alive until the program exists
myBroker = ALBroker("myBroker",
   "0.0.0.0",   # listen to anyone
   0,           # find a free port and use it
   IP,         # parent broker IP
   PORT)       # parent broker port

# Global variable to store the HumanGreeter module instance
HumanGreeter = None
memory = None

# Warning: HumanGreeter must be a global variable
# The name given to the constructor must be the name of the
# variable
global HumanGreeter
global humanEventWatcher

HumanGreeter = HumanGreeterModule("HumanGreeter")
humanEventWatcher = HumanTrackedEventWatcher(IP,PORT)

# Thread functions
def sudoku_searcher(sudoku, require_answer):
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

    sudoku.updateSudoku(solution)

# MAIN CARLOS
try:
    while True:
        time.sleep(1)

        idle.crouch()

        speech.introSpeech()
        askForSudoku()
        speech.askForCheck()
        speech.rightAnswer()


        """

        speech.introSpeech()

        sudoku = SudokuNao(([],[]))
        idling = True
        thread_sudoku = threading.Thread(target=sudoku_searcher, args=(sudoku,True,))
        thread_idling =\
            threading.Thread(target=IdleBehaviour.startIdling, args=(idle,idling,))

#        thread_idling.start()
        thread_sudoku.start()
        thread_sudoku.join()

        speech.seenSudoku()
        idling = False

#        thread_idling.join()
        break

        """

except KeyboardInterrupt:
    print
    print "Interrupted by user, shutting down"
    myBroker.shutdown()
    idle.sleep()
    sys.exit(0)

'''
begin = True
end = False
sp.introSpeech()
if saysYes():
    speech.askForSudoku()
    scans = waitForSudoku()
    sudoku = SudokuNao(scans)
    while(true):
        end = checkIfEnd(sudoku.sudoku)
        speech.askForSquare(begin, end)
        if saysYes():
            speech.askForCheck()
            scans = waitForSudoku()
            sudoku.updateSudoku(scans[0])
            if sn.answerIsCorrect():
                speech.rightAnswer()
            else:
                speech.wrongAnswerGetHint(sudoku.sudoku)
        else:
            speech.giveHint(sudoku.sudoku)
    if end:
        randomDancing()
        break
else:
    print("game not entered")
'''
