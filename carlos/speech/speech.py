from naoqi import ALProxy
import time
from random import randint

class Speech:

    current_name = None

    # sets the volume to a default value
    def __init__(self):
        self.animated_speech = ALProxy("ALAnimatedSpeech")

    # outputs the intro monologuew
    def intro_speech(self):
        randNum = randint(0,2)
        if randNum == 0:
            self.animated_speech.say("^start(animations/Stand/Gestures/You_1) Hey {}! Do you want to make a sudoku with me? You can touch my feet to answer my questions.".format(self.current_name))
        if randNum == 1:
            self.animated_speech.say("^start(animations/Stand/Gestures/You_1) Hello {}! Do you want to make a sudoku with me? Press on my feet to answer my questions.".format(self.current_name))
        if randNum == 2:
            self.animated_speech.say("^start(animations/Stand/Gestures/You_1) Hi {}! Would you like to make a sudoku with me? You can press on my feet to answer my questions.".format(self.current_name))

    def ask_for_rules(self):
        randNum = randint(0,1)
        if randNum == 0:
            self.animated_speech.say("^start(animations/Stand/Gestures/Explain_2) Would you like to hear the rules of a sudoku?")
        if randNum == 1:
            self.animated_speech.say("^start(animations/Stand/Gestures/Explain_2) Do you want to start with the rules of a sudoku?")

    def ask_for_sudoku(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_1) Let me see your sudoku puzzle before we start. ^stop(animations/Stand/Gestures/Explain_1)")

    def say_write_down(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_1) Write it down and show it to me.")

    def bye(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/You_2) Bye {}! See you soon!.".format(self.current_name))

    def hi(self):
        randNum = randint(0,1)
        if randNum == 0:
            self.animated_speech.say("^start(animations/Stand/Gestures/Explain_2) Hi there {}, good to see you again.".format(self.current_name))
        if randNum == 1:
            self.animated_speech.say("^start(animations/Stand/Gestures/Explain_2) Hello {}, I missed you.".format(self.current_name))

    def wrong_answer_get_hint(self, sudoku):
        self.animated_speech.say("^start(animations/Stand/Emotions/Neutral/Embarrassed_1) Oops! I think you made a mistake.")
        self.give_hint(sudoku)

    def right_answer(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Yes_1) Well done!")

    def ask_for_square(self):
        if self.count_zeros(sudoku) == 1:
            self.animated_speech.say("^start(animations/Stand/Gestures/Enthusiastic_3) Only one square to go, do you know the answer?")
        else:
            self.animated_speech.say("^start(animations/Stand/Gestures/Enthusiastic_5) Can you fill in another square?")

    def say_no_answer(self):
        self.animated_speech.say("^start(animations/Stand/Emotions/Neutral/Embarrassed_1) You didn't fill in anything. Please, do so now.")

    def give_hint(self, sudoku):
        self.animated_speech.say("^start(animations/Stand/Gestures/ShowSky_1) Let me give you a hint.")
        randNum = randint(1,2)
        if randNum == 1:
            self.get_random_hint()
        elif randNum == 2:
            sudokuNao = SudokuNao(([],[]))
            number = sudokuNao.best_number(sudoku)
            self.look_for_number(number)

    # nao confirms it has seen the sudoku
    def seen_sudoku(self):
        randNum = randint(0,3)
        if randNum == 0:
            self.animated_speech.say("^start(animations/Stand/Gestures/Hey_1) Nice one! Can you fill in a square?")
        if randNum == 1:
            self.animated_speech.say("^start(animations/Stand/Gestures/Hey_1) Thank you! Can you fill in a square?")
        if randNum == 2:
            self.animated_speech.say("^start(animations/Stand/Gestures/Hey_1) That's great! Can you fill in a square?")
        if randNum == 3:
            self.animated_speech.say("^start(animations/Stand/Gestures/Hey_1) Very nice! Can you fill in a square?")

    # outputs the general rules of the sudoku game
    def get_game_rules(self):
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_7) To complete your sudoku correctly, you must fill in al the empty squares.")
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_8) When you are finished, the numbers 1 to 9 must appear exactly once in each row, column and box.")

    # gives one of the four random hints
    def get_random_hint(self):
        randNum = randint(0,3)
        if randNum == 0:
            self.animated_speech.say("^start(animations/Stand/Gestures/YouKnowWhat_1) Have you already looked at the most filled in row, column or box?")
        elif randNum == 1:
            self.animated_speech.say("^start(animations/Stand/Gestures/YouKnowWhat_5) Maybe you have to think one step ahead. Look which numbers' locations in a row, column or box are blocked by the numbers in the already filled in squares.")
        elif randNum == 2:
            self.animated_speech.say("^start(animations/Stand/Gestures/YouKnowWhat_1) Which specific numbers are missing in the row, column or box you are looking at?")
        elif randNum == 3:
            self.animated_speech.say("^start(animations/Stand/Gestures/YouKnowWhat_5) Look at three boxes and see if there are two identical numbers in two of the boxes. Maybe you can fill in this number in the third box?")

    # tells the player to look at a given number
    def look_for_number(self, digit):
        self.animated_speech.say("^start(animations/Stand/Gestures/Explain_1) Here's a tip: maybe you can fill out number"+ str(digit))

class SudokuNao:
    def __init__(self, strings):
        self.sudoku = self.make_sudoku_array(strings[0])
        self.sudokuAnswer = self.make_sudoku_array(strings[1])

    def update_sudoku(self, string):
        self.sudoku = self.make_sudoku_array(string)

    def is_correct(self):
        for x in range(9):
            for y in range(9):
                if self.sudoku[x][y] == 0:
                    continue
                if self.sudoku[x][y] != self.sudokuAnswer[x][y]:
                    return False
        return True

    def print_arrays(self):
        print("The start sudoku is: ")
        for x in self.sudoku:
            print(x)
        print("The solved sudoku is: ")
        for x in self.sudokuAnswer:
            print(x)

    def best_number(self, sudoku):
        best_count = 0
        number = 0
        for i in range(1,10):
            count = self.counter(i, sudoku)
            if count > best_count and count < 9:
                best_count = count
                number = i
        return number

    def counter(self, number, sudoku):
        count = 0
        for i in range(9):
            for j in range(9):
                value = sudoku[i][j]
                if value == number:
                    count += 1
        return count

    def make_sudoku_array(self, sudokuStr):
        sudokuArray = []
        for n in range(9):
            substr = sudokuStr[(n*9):((n+1)*9)]
            rowArray = []
            for x in substr:
                rowArray.append(int(x))
            sudokuArray.append(rowArray)
        return sudokuArray

    def count_zeros(self, sudoku):
        # Works with a string for now
        numZeros = 0
        for x in range(9):
            for y in range(9):
                if sudoku[x][y] == 0:
                    numZeros += 1
        return numZeros

    def check_if_end(self, sudoku):
        if self.count_zeros(sudoku) == 0:
            return True
        return False
