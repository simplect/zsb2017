from __future__ import print_function
from copy import deepcopy
import sys

# GAME CONFIGURATION
DEBUG = False
PLAY_AGAINST = False 
PLAY_AGAINST_EASY = False

## Helper functions

# Translate a position in chess notation to x,y-coordinates
# Example: c3 corresponds to (2,5)
def to_coordinate(notation):
    x = ord(notation[0]) - ord('a')
    y = 8 - int(notation[1])
    return (x, y)

# Translate a position in x,y-coordinates to chess notation
# Example: (2,5) corresponds to c3
def to_notation(coordinates):
    (x,y) = coordinates
    letter = chr(ord('a') + x)
    number = 8 - y
    return letter + str(number)

# Translates two x,y-coordinates into a chess move notation
# Example: (1,4) and (2,3) will become b4c5
def to_move(from_coord, to_coord):
    return to_notation(from_coord) + to_notation(to_coord)

## Defining board states

# These Static classes are used as enums for:
# - Material.Rook
# - Material.King
# - Material.Pawn
# - Side.White
# - Side.Black
class Material:
    Rook, King, Pawn = ['r','k','p']
class Side:
    White, Black = range(0,2)
class Score:
    Rook, King, Pawn = [5, 10, 1]

# A chesspiece on the board is specified by the side it belongs to and the type
# of the chesspiece
class Piece:
    def __init__(self, side, material, score):
        self.side = side
        self.material = material
        self.score = score

# A chess configuration is specified by whose turn it is and a 2d array
# with all the pieces on the board
class ChessBoard:
    
    def __init__(self, turn):
        # This variable is either equal to Side.White or Side.Black
        self.turn = turn
        self.board_matrix = None


    ## Getter and setter methods 
    def set_board_matrix(self,board_matrix):
        self.board_matrix = board_matrix

    # Note: assumes the position is valid
    def get_boardpiece(self,position):
        (x,y) = position
        return self.board_matrix[y][x]

    # Note: assumes the position is valid
    def set_boardpiece(self,position,piece):
        (x,y) = position
        self.board_matrix[y][x] = piece
    
    # Read in the board_matrix using an input string
    def load_from_input(self,input_str):
        self.board_matrix = [[None for _ in range(8)] for _ in range(8)]
        x = 0
        y = 0
        for char in input_str:
            if y == 8:
                if char == 'W':
                    self.turn = Side.White
                elif char == 'B':
                    self.turn = Side.Black
                return
            if char == '\r':
                continue
            if char == '.':
                x += 1
                continue
            if char == '\n':
                x = 0
                y += 1
                continue 
            
            if char.isupper():
                side = Side.White
            else:
                side = Side.Black
            material = char.lower()
            
            if material == "p":
                score = 1
            elif material == "k":
                score = 10
            elif material == "r":
                score = 5

            piece = Piece(side, material, score)
            self.set_boardpiece((x,y),piece)
            x += 1

    # Print the current board state
    def __str__(self):
        return_str = ""

        return_str += "   abcdefgh\n\n"
        y = 8
        for board_row in self.board_matrix:
            return_str += str(y) + "  " 
            for piece in board_row:
                if piece == None:
                    return_str += "."
                else:
                    char = piece.material
                    if piece.side == Side.White:
                        char = char.upper()
                    return_str += char
            return_str += '\n'
            y -= 1
        
        turn_name = ("White" if self.turn == Side.White else "Black") 
        return_str += "It is " + turn_name + "'s turn\n"

        return return_str

    # Given a move string in chess notation, return a new ChessBoard object
    # with the new board situation
    # Note: this method assumes the move suggested is a valid, legal move
    def make_move(self, move_str):
        
        start_pos = to_coordinate(move_str[0:2])
        end_pos = to_coordinate(move_str[2:4])

        if self.turn == Side.White:
            turn = Side.Black
        else:
            turn = Side.White
            
        # Duplicate the current board_matrix
        new_matrix = [row[:] for row in self.board_matrix]
        
        # Create a new chessboard object
        new_board = ChessBoard(turn)
        new_board.set_board_matrix(new_matrix)

        # Carry out the move in the new chessboard object
        piece = new_board.get_boardpiece(start_pos)
        new_board.set_boardpiece(end_pos, piece)
        new_board.set_boardpiece(start_pos, None)

        return new_board

    def is_king_dead(self, side):
        seen_king = False
        for x in range(8):
            for y in range(8):
                piece = self.get_boardpiece((x,y))
                if piece != None and piece.side == side and \
                        piece.material == Material.King:
                    seen_king = True
        return not seen_king

    def check_pawn(self, piece, location):
        # Check boundary and side
        (x, y) = location
        legal_moves = []

        ny = y + (-1 if self.turn == Side.White else 1)
        if ny < 0 or ny > 7:
            return []

        for shift in range(-1,2):
            nx = x+shift
            
            if nx < 0 or nx > 7:
                continue
            
            check  = self.get_boardpiece((nx,ny))

            if check is not None:
                if shift == 0 or check.side == piece.side:
                    continue
            elif shift != 0:
                continue

            legal_moves.append(to_move((x,y), (nx, ny)))
        return legal_moves
    
    def check_king(self, piece, location):
        legal_moves = []
        (x, y) = location
        for (i,j) in [(a,b) for a in range(-1,2) for b in range(-1,2)]:
            if x + i < 0 or x + i > 7 or y + j < 0 or y + j > 7:
                continue
            
            check  = self.get_boardpiece((x + i, y + j))

            if check is not None:
                if check.side == piece.side:
                    continue


            legal_moves.append(to_move((x,y), (x + i, y + j)))
        return legal_moves

    def check_rook(self, piece, location):
        legal_moves = []
        (x, y) = location

        for (a,b) in [(1,0),(-1,0),(0,1),(0,-1)]:
            for i in range(1,8):
                 
                if x + a*i < 0 or x + a*i > 7 or y + b*i < 0 or y + b*i > 7:
                    continue
                check  = self.get_boardpiece((x+a*i, y+b*i))

                if check is not None:
                    if check.side != piece.side:
                        legal_moves.append(to_move((x,y), (x+a*i, y+b*i)))
                    break
                else:
                    legal_moves.append(to_move((x,y), (x+a*i, y+b*i)))
        return legal_moves
  
    # This function should return, given the current board configuation and
    # which players turn it is, all the moves possible for that player
    # It should return these moves as a list of move strings, e.g.
    # [c2c3, d4e5, f4f8]
    # TODO: write an implementation for this function
    def legal_moves(self):
        legal_moves = []
        for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
            piece = self.get_boardpiece((x,y))

            if piece is None or not piece.side == self.turn:
                continue

            if piece.material == 'p':
                legal_moves += self.check_pawn(piece, (x,y))
                        
            elif piece.material == 'k':
                legal_moves += self.check_king(piece, (x,y))

            elif piece.material == 'r':
                legal_moves += self.check_rook(piece, (x,y))

        return legal_moves
    

    # This function should return, given the move specified (in the format
    # 'd2d3') whether this move is legal
    # TODO: write an implementation for this function, implement it in terms
    # of legal_moves()
    def is_legal_move(self, move):
        legal_moves = self.legal_moves()

        if move not in legal_moves:
            return False
        return True


# This static class is responsible for providing functions that can calculate
# the optimal move using minimax
class ChessComputer:

    # This method uses either alphabeta or minimax to calculate the best move
    # possible. The input needed is a chessboard configuration and the max
    # depth of the search algorithm. It returns a tuple of (score, chessboard)
    # with score the maximum score attainable and chessboardmove that is needed
    #to achieve this score.
    @staticmethod
    def computer_move(chessboard, depth, alphabeta=False):
        if alphabeta:
            inf = 99999999
            min_inf = -inf
            return ChessComputer.alphabeta(chessboard, depth, min_inf, inf)
        else:
            return ChessComputer.minimax(chessboard, depth)

    

    # This function uses minimax to calculate the next move. Given the current
    # chessboard and max depth, this function should return a tuple of the
    # the score and the move that should be executed
    # NOTE: use ChessComputer.evaluate_board() to calculate the score
    # of a specific board configuration after the max depth is reached
    @staticmethod
    def minimax(chessboard, depth):
        legal_moves = chessboard.legal_moves()

        def mini(chessboard, depth_left):
                v = 9999
                for move in chessboard.legal_moves():
                    v = min(v, maxi(chessboard.make_move(move), depth_left-1))
                return v

        def maxi(chessboard, depth_left):
            if depth_left < 1:
                return ChessComputer.evaluate_board(chessboard, depth_left)
            else:
                v = -9999
                for move in chessboard.legal_moves():
                    v = max(v, mini(chessboard.make_move(move), depth_left-1))
                return v

        v = -9999
        maxmove = ''
        for move in legal_moves:
            (v, maxmove) = max((v, maxmove), (mini(chessboard.make_move(move), 3), move))
        
        return (v, maxmove)

    # This function uses lphabeta to calculate the next move. Given the
    # chessboard and max depth, this function should return a tuple of the
    # the score and the move that should be executed.
    # It has alpha and beta as extra pruning parameters
    # NOTE: use ChessComputer.evaluate_board() to calculate the score
    # of a specific board configuration after the max depth is reached
    @staticmethod
    def alphabeta(chessboard, depth, alpha, beta):
        legal_moves = chessboard.legal_moves()

        def mini(chessboard, depth_left, alpha, beta):
                v = 9999
                for move in chessboard.legal_moves():
                    v = min(v, maxi(chessboard.make_move(move), depth_left-1, alpha, beta))

                    beta = min(v, beta)
                    if beta <= alpha:
                        break

                return v

        def maxi(chessboard, depth_left, alpha, beta):
            if depth_left < 1:
                return ChessComputer.evaluate_board(chessboard, depth_left)
            else:
                v = -9999
                for move in chessboard.legal_moves():
                    v = max(v, mini(chessboard.make_move(move), depth_left-1, alpha, beta))

                    alpha = max(v, alpha)
                    if beta <= alpha:
                        break

                return v

        v = -9999
        maxmove = ''
        for move in legal_moves:
            (v, maxmove) = max((v, maxmove), (mini(chessboard.make_move(move), depth, alpha, beta), move))

        return (v, maxmove)



    # Calculates the score of a given board configuration based on the 
    # material left on the board. Returns a score number, in which positive
    # means white is better off, while negative means black is better of
    # NOTE: Most comments in here are ideas which are disabled :) ~ Merijn
    # TODO: Optimize this with depth_left
    @staticmethod
    def evaluate_board(chessboard, depth_left):
        """
        score_white = 0
        score_black = 0
        for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
            piece = chessboard.get_boardpiece((x,y))

            if piece is None:
                continue
            elif piece.side == Side.White:
                score_white += piece.score 
            elif piece.side == Side.Black:
                score_black += piece.score

        if score_black < score_white:
            return 1
        else:
            return -1
        """
        score = 0
        for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
            piece = chessboard.get_boardpiece((x,y))

            if piece is None:
                continue
            elif piece.side == chessboard.turn:
                score += piece.score
            else:
                score -= piece.score

        #return score * (1 if chessboard.turn == Side.White else -1)
        return score 


# This class is responsible for starting the chess game, playing and user 
# feedback
class ChessGame:
    def __init__(self, turn):
     
        # NOTE: you can make this depth higher once you have implemented
        # alpha-beta, which is more efficient
        self.depth = 4000
        self.chessboard = ChessBoard(turn)

        # If a file was specified as commandline argument, use that filename
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        else:
            filename = "board.chb"

        print("Reading from " + filename + "...")
        self.load_from_file(filename)

    def load_from_file(self, filename):
        with open(filename) as f:
            content = f.read()

        self.chessboard.load_from_input(content)

    def main(self):
        if PLAY_AGAINST:
            print("Play against mode enabled, alphabeta will be playing white.")
        while True:
            print(self.chessboard)
            if DEBUG:
                # Print the legal moves ~ Merijn
                print("Legal moves: {}".format(self.chessboard.legal_moves()))

            # Print the current score
            score = ChessComputer.evaluate_board(self.chessboard,self.depth)
            print("Current score: " + str(score))
            
            if PLAY_AGAINST and self.chessboard.turn == 0:
                move = self.make_computer_move()

            if not PLAY_AGAINST or PLAY_AGAINST_EASY:
                # Calculate the best possible move
                print("Calculating best move...")
                new_score, best_move = ChessComputer.computer_move(self.chessboard,
                self.depth, alphabeta=True)
                print("Best move: " + best_move)
                print("Score to achieve: " + str(new_score))
                print("")

            self.make_human_move()


    def make_computer_move(self):
        new_score, best_move = ChessComputer.computer_move(self.chessboard,
            self.depth, alphabeta=True)

        print("White is playing {}".format(best_move))

        self.chessboard = self.chessboard.make_move(best_move)
        print(self.chessboard)

        # Exit the game if one of the kings is dead
        if self.chessboard.is_king_dead(Side.Black):
            print(self.chessboard)
            print("White wins!")
            sys.exit(0)
        elif self.chessboard.is_king_dead(Side.White):
            print(self.chessboard)
            print("Black wins!")
            sys.exit(0)

    def make_human_move(self):
        # Endlessly request input until the right input is specified
        while True:
            if sys.version_info[:2] <= (2, 7):
                move = raw_input("Indicate your move (or q to stop): ")
            else:
                move = input("Indicate your move (or q to stop): ")
            if move == "q":
                print("Exiting program...")
                sys.exit(0)
            elif self.chessboard.is_legal_move(move):
                break
            print("Incorrect move!")

        self.chessboard = self.chessboard.make_move(move)

        # Exit the game if one of the kings is dead
        if self.chessboard.is_king_dead(Side.Black):
            print(self.chessboard)
            print("White wins!")
            sys.exit(0)
        elif self.chessboard.is_king_dead(Side.White):
            print(self.chessboard)
            print("Black wins!")
            sys.exit(0)

chess_game = ChessGame(Side.White)
chess_game.main()

