#from sudoku.main import solve
import time
import sys
from naoqi import ALBroker
from speech.speech import Speech
from behaviour.idle import IdleBehaviour, HumanGreeterModule, HumanTrackedEventWatcher

#solution = solve("sudoku.jpg")
solution = ('401290075200300800070080006000103062105000403730608000600020030007001004890065107', '481296375256317849379584216948153762165972483732648951614729538527831694893465127')
IP = '169.254.35.27'
PORT = 9559
sp = Speech(IP, PORT)
ib = IdleBehaviour(IP, PORT)
#ib.sitRelax()

sudoku = [[3,0,0,0,8,0,0,0,6],[0,1,0,0,0,6,0,2,0],[0,0,4,7,0,0,5,0,0],[0,4,0,0,1,0,9,0,0],[6,0,0,2,0,4,0,0,1],[0,0,3,0,6,0,0,5,0],[0,0,8,0,0,3,6,0,0],[0,2,0,4,0,0,0,1,0],[5,0,0,0,2,0,0,0,7]]
#sp.introSpeech()
#sp.instructionMenu()


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

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print
    print "Interrupted by user, shutting down"
    myBroker.shutdown()
    ib.sleep()
    sys.exit(0)

