from sudoku.main import solve
import time
import sys
import threading
from naoqi import ALBroker, ALProxy
from speech.speech import Speech, SudokuNao
from behaviour.posture import Posture
from behaviour.move import Move
from vision.image import Vision
from vision.perception import Human
from sensors.feet import Feet

from random import randint

# SET-UP
IP = '169.254.131.247'
PORT = 9559

# We need this broker to be able to construct
# NAOqi modules and subscribe to other modules
# The broker must stay alive until the program exists
carlos_broker = ALBroker("carlosBroker",
   "0.0.0.0",   # listen to anyone
   0,           # find a free port and use it
   IP,         # parent broker IP
   PORT)       # parent broker port

class Carlos:
    def __init__(self):

        # AL MODULES
        global human
        global feet
        human = Human()
        feet = Feet()

        # Normal classes
        self.speech = Speech()
        self.posture = Posture()
        self.move = Move()
        self.vision = Vision()


    def play_sudoku(self):
        if not self.human.current_name:
            return

        self.speech.current_name = human.current_name

        self.speech.introSpeech()

        if not self.feet.register_question():
            self.speech.bye()
            self.human.find_new()
            return
        
        self.speech.askForRules()

        if self.feet.registerQuestion():
            self.speech.getGameRules()

        self.speech.askForSudoku()
 
        scans = self.scan_sudoku(require_answer=True)

        init_sudoku = SudokuNao(scans)
        sudoku = SudokuNao(scans) 

        begin = True
        oldSudoku = []

        # Main solving loop
        while True:

            sudoku.print_arrays()

            if sudoku.check_if_end(sudoku.sudoku):
                aup = ALProxy('ALAudioPlayer')
                song = aup.post.playFile("/home/nao/songs/happy.wav")
                #self.move.randomDancing()
                self.feet.do_rasta()
                time.sleep(60)
                aup.stopAll()
                break

            self.speech.ask_for_square()

            oldSudoku = sudoku.sudoku
            if self.feet.register_question():
                self.speech.say_write()

                scans = self.scan_sudoku(prev = sudoku.sudoku)

                if oldSudoku != sudoku.sudoku:
                    speech.ask_for_square(begin, end)
                else:
                    speech.not_filled_anything_in()

                sudoku.update_sudoku(scans[0])

                if sudoku.is_correct():
                    self.speech.right_answer()
                else:
                    sudoku.print_arrays()
                    self.speech.wrong_answer_get_hint(sudoku.sudoku)

            else:
                sudoku.print_arrays()
                self.speech.wrong_answer_get_hint(sudoku.sudoku)
        else:
            self.speech.giveHint(sudoku.sudoku)

    def scan_sudoku(self,require_answer = False, prev = False):
        print("Started sudoku searcher")
        # Assume scanning position and stop normal head movements

        self.posture.stand()
        self.posture.basic_awareness.stopAwareness()
        self.posture.stopForScan()

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

        self.posture.resume()
        return solution
    
    def sleep(self):
        self.speech.bye()
        self.posture.sleep()

if __name__=='__main__':
    carlos = Carlos()
    try:
        carlos.play_sudoku()
        time.sleep(2)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        carlos.sleep()
        myBroker.shutdown()
        sys.exit(0)
