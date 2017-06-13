# chessgame.py
# In this file, chess is implemented using python.
# Babette Mooij, 10740414
# Merijn Terstroote, 11173106
# Groep D
# 09-06-2017
# You can enable PLAY_AGAINST !OR! AIVSAI.

from __future__ import print_function
from copy import deepcopy
import sys
import math

# GAME CONFIGURATION
DEBUG = False

PLAY_AGAINST = True 
PLAY_AGAINST_EASY = False

AIVSAI = False

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

def to_coordinates(move):
    move_list = list(move)
    old_place = move_list[0] + move_list[1]
    new_place = move_list[2] + move_list[3]
    return to_coordinate(old_place), to_coordinate(new_place)

## Defining board states

# These Static classes are used as enums for:
# - Material.Rook
# - Material.King
# - Material.Pawn
# - Material.Knight
# - Material.Queen
# - Material.Bishop
# - Side.White
# - Side.Black
class Material:
    Rook, King, Pawn, Knight, Queen, Bishop = ['r','k','p','h','q','b']
class Side:
    White, Black = range(0,2)
class Score:
    Rook, King, Pawn, Knight, Queen, Bishop = [5, 20, 1, 3, 9, 3]

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

    # Cache variables
    cstalemate = None
    clegal_moves = None
    copp_moves = None
    
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
            elif material == "h":
                score = 3
            elif material == "q":
                score = 9
            elif material == "b":
                score = 3

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
        # Check boundaries
        (x, y) = location
        legal_moves = []
        
        ny = y + (-1 if self.turn == Side.White else 1)
        if ny < 0 or ny > 7:
            return []

        for shift in range(-1,2):
            nx = x+shift
            
            if nx < 0 or nx > 7:
                continue
            # Is there already another piece on this place? 
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
  
    def check_knight(self, piece, location):
        legal_moves = []
        (x, y) = location

        for (i,j) in [(-1,2),(1,2),(-1,-2),(1,-2),(-2,-1),(2,-1),(-2,1),(2,1)]:

            if x + i < 0 or x + i > 7 or y + j < 0 or y + j > 7:
                continue
            check = self.get_boardpiece((x + i, y + j))

            if check is not None:
                if check.side != piece.side:
                    legal_moves.append(to_move((x,y), (x + i, y +j)))
            else:
                legal_moves.append(to_move((x,y), (x + i, y + j)))
        return legal_moves

    
    def check_queen(self, piece, location):
        legal_moves = []
        (x, y) = location

        for (a,b) in [(m,n) for m in range(-1,2) for n in range(-1,2)]:
            for i in range(1,8):
                 
                if x + a*i < 0 or x + a*i > 7 or y + b*i < 0 or y + b*i > 7:
                    continue
                check  = self.get_boardpiece((x + a*i, y + b*i))

                if check is not None:
                    if check.side != piece.side:
                        legal_moves.append(to_move((x,y), (x + a*i, y + b*i)))
                    break
                else:
                    legal_moves.append(to_move((x,y), (x + a*i, y + b*i)))
        return legal_moves
  

    def check_bishop(self, piece, location):
        legal_moves = []
        (x, y) = location

        for (a,b) in [(-1,-1),(-1,1),(1,1),(-1,1)]:
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

    def legal_moves(self, opponent = False):
        """
        This function returns all legal moves for a chessboard.
        Use opponent=True for legal_moves for the opponent player.
        """

        # Cache variables
        if self.clegal_moves and not opponent:
            return self.clegal_moves
        elif self.copp_moves and opponent:
            return self.copp_moves

        legal_moves = []

        # Temporarily switch sides
        if opponent:
            self.turn = Side.White if self.turn == Side.Black else Side.Black

        for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
            piece = self.get_boardpiece((x,y))
             
            if piece is None:
                continue

            if not piece.side == self.turn:
                continue

            if piece.material == Material.Pawn:
                legal_moves += self.check_pawn(piece, (x,y))
                        
            elif piece.material == Material.King:
                legal_moves += self.check_king(piece, (x,y))

            elif piece.material == Material.Rook:
                legal_moves += self.check_rook(piece, (x,y))
            
            elif piece.material == Material.Knight:
                legal_moves += self.check_knight(piece, (x,y))

            elif piece.material == Material.Queen:
                legal_moves += self.check_queen(piece, (x,y))

            elif piece.material == Material.Bishop:
                legal_moves += self.check_bishop(piece, (x,y))
        
        # Save in cache and possibly switch back sides
        if opponent:
            self.turn = Side.White if self.turn == Side.Black else Side.Black
            self.copp_moves = legal_moves
        else:
            self.clegal_moves = legal_moves

        return legal_moves
    
    def is_legal_move(self, move):
        """    
        Check if move is legal according to legal moves
        NOTE: Only works for player who's on the current turn.
        """
        if self.clegal_moves:
            legal_moves = self.clegal_moves
        else:
            legal_moves = self.legal_moves()

        if move not in legal_moves:
            return False
        return True

    def is_stalemate(self):
        """
         This function checks if the boards is in a few kind of stalemate
         Situations. Stalemate situations where the affecting player
         can still recover cannot be detected (yet).
         Returns -1 if it affects the current player, 1 if it affects the opponent player
         (in favor of the current player) and 0 if there is no stalemate detected).
        """
        # Cache
        if self.cstalemate:
            return self.cstalemate

        king = None
        king_loc = None

        for location in [(x,y) for x in range(8) for y in range(8)]:
            piece = self.get_boardpiece(location)
            if piece is not None and piece.material == 'k':
                king = piece
                king_loc = location

                legal_moves_king = self.check_king(king, king_loc)

                if not legal_moves_king:
                    return False


                if king.side == self.turn:
                    opponent = True
                else:
                    opponent = False

                opponent_moves = self.legal_moves(opponent=opponent)


                # Check if the king has free moves which do not 
                # put him in check
                free_moves = []
                for move in legal_moves_king:
                    free_move = True
                    for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
                        if to_notation((x,y)) + move[2:] in opponent_moves:
                            free_move = False
                            break
                    
                    if free_move:
                        free_moves.append(move)

                if king and king.side == self.turn and not free_moves:
                    self.cstalemate = -1
                    return -1
                elif king and not free_moves:
                    self.cstalemate = 1
                    return 1

        self.cstalemate = 0
        return 0

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
            return ChessComputer.alphabeta(chessboard, depth)
        else:
            return ChessComputer.minimax(chessboard, depth)

    

    # This function uses minimax to calculate the next move. Given the current
    # chessboard and max depth, this function should return a tuple of the
    # the score and the move that should be executed
    @staticmethod
    def minimax(chessboard, depth):
        legal_moves = chessboard.legal_moves()

        def mini(chessboard, depth_left):
                v = 9999
                for move in chessboard.legal_moves():
                    v = min(v, maxi(chessboard.make_move(move), depth_left-1))
                return v

        def maxi(chessboard, depth_left):
            if depth_left < 1 or ChessComputer.is_endgame(chessboard):
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
    @staticmethod
    def alphabeta(chessboard, depth, cutoff=None):

        def maxi(chessboard, depth, alpha, beta):
            if cutoff(depth, chessboard):
                return ChessComputer.evaluate_board(chessboard, depth)

            v = -math.inf
            for move in chessboard.legal_moves():
                v = max(v, mini(chessboard.make_move(move), depth+1, alpha, beta))
                
                if v >= beta:
                    break

                alpha = max(v, alpha)
            return v

        def mini(chessboard, depth, alpha, beta):

            v = math.inf
            for move in chessboard.legal_moves():
                v = min(v, maxi(chessboard.make_move(move), depth+1, alpha, beta))

                if v <= alpha:
                    break

                beta = min(v, beta)
            return v

        
        v = -math.inf
        maxmove = ''
        legal_moves = chessboard.legal_moves()
        # Enable the following when on a supercomputer
        # cutoff = lambda x, y: x > depth or ChessComputer.is_endgame(y)
        cutoff = lambda x, y: x >= depth

        for move in legal_moves:
            (v, maxmove) = max(
                    (v, maxmove),
                    (mini(chessboard.make_move(move), 0, -math.inf, math.inf), move))
        return (v, maxmove)



    # Calculates the score of a given board configuration based on the 
    # material left on the board. Returns a score number, in which positive
    # means white is better off, while negative means black is better of
    @staticmethod
    def evaluate_board(chessboard, depth):
        scores = 0
        pieces = {}

        legal_moves = chessboard.legal_moves()
        opp_legal_moves = chessboard.legal_moves(opponent=True)

        for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
            piece = chessboard.get_boardpiece((x,y))
            
            if piece is None:
                continue

            turn = 1 if piece.side == chessboard.turn else -1
            
            # Collect the piece scores and counts
            if piece.material in pieces:
                pieces[piece.material] = \
                    ((pieces[piece.material] / piece.score) + turn) * piece.score
            else:
                    pieces[piece.material] = turn * piece.score
            if piece.material in pieces:
                pieces[piece.material] = \
                    ((pieces[piece.material] / piece.score) + turn) * piece.score
            else:
                    pieces[piece.material] = turn * piece.score

            
            # Check if king is in danger
            if piece.material == 'k' and piece.side == chessboard.turn and turn == 1:
                for move in opp_legal_moves:
                    if (x,y) == to_coordinate(move[2:]):
                        scores -= 10
        
        # Take the sum of all values
        scores += sum(pieces.values()) 
        
        # Add a depth bias
        scores += -1 * depth
        
        # Add a bias based on the difference of moves
        scores += 0.1 * (len(legal_moves) - len(opp_legal_moves))

        # Add a bias for preventing stalemate
        # Enabled when on a super computer
        #scores += 100 * chessboard.is_stalemate()
        return scores
        
    @staticmethod
    def is_endgame(chessboard):
        # Exit the game if one of the kings is dead
        if chessboard.is_king_dead(Side.Black):
            return True
        elif chessboard.is_king_dead(Side.White):
            return True
        return False


# This class is responsible for starting the chess game, playing and user 
# feedback
class ChessGame:
    def __init__(self, turn):
     
        # NOTE: you can make this depth higher once you have implemented
        # alpha-beta, which is more efficient
        self.depth = 3
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

    def check_game(self):
        # Exit the game if one of the kings is dead
        stale = self.chessboard.is_stalemate()
        if self.chessboard.is_king_dead(Side.Black):
            print(self.chessboard)
            print("White wins!")
            sys.exit(0)
        elif self.chessboard.is_king_dead(Side.White):
            print(self.chessboard)
            print("Black wins!")
            sys.exit(0)
        elif stale != 0:
            print(self.chessboard)
            print("(almost) Stalemate!")
            if stale == -1:
                print("{} wins!"
                        .format("White" if self.chessboard.turn == Side.Black else "Black"))
            elif stale == 1:
                print("{} wins!"
                        .format("White" if self.chessboard.turn == Side.White else "Black"))

            sys.exit(0)

    def resign(self):
        print("{} Resigns!"
                .format("White" if self.chessboard.turn == Side.White else "Black"))
        sys.exit(0)

    def main(self):
        if PLAY_AGAINST:
            print("Play against mode enabled, alphabeta will be playing white.")

        elif AIVSAI:
            print("AI VS. AI mode enabled, enjoy watching alphabeta wrecking itself.")

            while True:
                print(self.chessboard)

                self.check_game()

                move = self.make_computer_move()

        while True:
            print(self.chessboard)
            self.check_game()

            if DEBUG:
                # Print the legal moves ~ Merijn
                print("Legal moves: {}".format(self.chessboard.legal_moves()))

            # Print the current score
            score = ChessComputer.evaluate_board(self.chessboard,self.depth)

            print("Current score: " + str(score))

            if PLAY_AGAINST and self.chessboard.turn == Side.White:
                move = self.make_computer_move()
                print(self.chessboard)

                self.check_game()

            if not PLAY_AGAINST or PLAY_AGAINST_EASY:
                # Calculate the best possible move
                print("Calculating best move...")
                new_score, best_move = ChessComputer.computer_move(self.chessboard,
                self.depth, alphabeta=True)
                print("Best move: " + best_move)
                print("Score to achieve: " + str(new_score))
                print("")
            
            self.make_human_move()
            self.check_game()

    def make_computer_move(self):
        score, best_move = ChessComputer.computer_move(self.chessboard,
            self.depth, alphabeta=True)

        if not best_move:
            self.resign()

        player = "White" if self.chessboard.turn == Side.White else "Black"
        print("{} is playing {} with score {}".format(player, best_move, score))

        self.chessboard = self.chessboard.make_move(best_move)

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


chess_game = ChessGame(Side.White)
chess_game.main()

