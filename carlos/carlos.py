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
IP = '169.254.35.27'
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

         
        # Normal classes
        self.speech = Speech()
        self.posture = Posture()
        self.move = Move()
        self.vision = Vision()


    def play_sudoku(self):

        if not human.current_name:
            return


        self.speech.current_name = human.current_name

        self.speech.hi()
    
        time.sleep(1)

        self.speech.intro_speech()

        if not feet.register_question():
            self.speech.bye()
            human.find_new()
            return
        
        self.speech.ask_for_rules()

        if feet.register_question():
            self.speech.get_game_rules()

        self.speech.ask_for_sudoku()
 
        scans = self.scan_sudoku(require_answer=True)

        init_sudoku = SudokuNao(scans)
        sudoku = SudokuNao(scans) 

        self.speech.seen_sudoku()

        begin = True
        oldSudoku = []

        # Main solving loop
        while True:

            sudoku.print_arrays()

            if sudoku.check_if_end(sudoku.sudoku):
                aup = ALProxy('ALAudioPlayer')
                song = aup.post.playFile("/home/nao/songs/happy.wav")
                #self.move.randomDancing()
                feet.do_rasta()
                time.sleep(60)
                aup.stopAll()
                break

            if oldSudoku != []:
                self.speech.ask_for_square()

            oldSudoku = sudoku.sudoku
            if feet.register_question():
                self.speech.say_write_down()

                scans = self.scan_sudoku(prev = sudoku.sudoku)

                if oldSudoku != sudoku.make_sudoku_array(scans[0]):
                    self.speech.ask_for_square()
                else:
                    self.speech.say_no_answer()
                    continue

                sudoku.update_sudoku(scans[0])

                if sudoku.is_correct():
                    self.speech.right_answer()
                else:
                    sudoku.print_arrays()
                    self.speech.wrong_answer_get_hint(sudoku.sudoku)

            else:
                self.speech.give_hint(sudoku.sudoku)

    def scan_sudoku(self,require_answer = False, prev = False):
        print("Started sudoku searcher")
        # Assume scanning position and stop normal head movements

        self.posture.stand()
        self.posture.basic_awareness.stopAwareness()
        self.posture.stop_for_scan()

        solution = (False, False)
        sudoku = SudokuNao(([],[]))
        while not solution[0]:
            self.vision.getImage("sudoku.jpg")
            solution = solve("sudoku.jpg")
            if not solution[0] \
                    or sudoku.count_zeros(sudoku.make_sudoku_array(solution[0])) > 70:
                solution = (False, False)
                continue
            if not solution[1] and require_answer:
                solution = (False, False)
                continue
            if prev:
                new_sudoku = sudoku.make_sudoku_array(solution[0])
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
    try:
        global human
        human = Human()
        global feet
        feet = Feet()

        carlos = Carlos()
        while True:
            carlos.play_sudoku()
            time.sleep(2)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        carlos.sleep()
        carlos_broker.shutdown()
        sys.exit(0)
