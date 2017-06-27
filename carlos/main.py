#from sudoku.main import solve
import time
import sys
from naoqi import ALBroker, ALProxy
from speech.speech import Speech, SudokuNao
from behaviour.idle import IdleBehaviour, HumanGreeterModule, HumanTrackedEventWatcher
from behaviour.move import Move
#from vision.image import Vision
from random import randint

# SET-UP
IP = '169.254.35.27'
PORT = 9559

speech = Speech(IP, PORT)
idle = IdleBehaviour(IP, PORT)
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

# MAIN CARLOS
try:
    while True:
        time.sleep(1)

        idle.crouch()

        """
        speech.introSpeech()

        solution = False
        while solution == False:
            vision.getImage("sudoku.jpg")
            try:
                solution = solve("sudoku.jpg")
                print(solution)
                """
                print(solution[0][0])
                if solution[0][0] != '3':
                    solution = False
                    continue
                    """
            except:
                continue

        sudoku = SudokuNao(solution)
        sudoku.printArrays()

        speech.seenSudoku()
        """

except KeyboardInterrupt:
    print
    print "Interrupted by user, shutting down"
    myBroker.shutdown()
    ib.sleep()
    sys.exit(0)

'''
begin = True
end = False
sp.introSpeech()
if saysYes():
    sp.askForSudoku()
    waitForSudoku()
    while(true):
        end = checkIfEnd(sn.sudoku)
        sp.askForSquare(begin, end)
        if saysYes():
            sp.askForCheck()
            waitForSudoku()
            if rightAnswer:
                sp.rightAnswer()
                sn.sudoku = updateSudoku(answer)
            else:
                sp.wrongAnswerGetHint(sn.sudoku)
        else:
            sp.giveHint(sn.sudoku)
    if end:
        randomDancing()
        break
else:
    print("game not entered")
'''
