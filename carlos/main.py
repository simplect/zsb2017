#from sudoku.main import solve
from speech.speech import Speech, SudokuNao

#solution = solve("sudoku.jpg")
solution = ('401290075200300800070080006000103062105000403730608000600020030007001004890065107', '481296375256317849379584216948153762165972483732648951614729538527831694893465127')
suNao = SudokuNao(solution)
suNao.printArrays()
sp = Speech("169.254.28.133", 9559)

sudoku = [[3,0,0,0,8,0,0,0,6],[0,1,0,0,0,6,0,2,0],[0,0,4,7,0,0,5,0,0],[0,4,0,0,1,0,9,0,0],[6,0,0,2,0,4,0,0,1],[0,0,3,0,6,0,0,5,0],[0,0,8,0,0,3,6,0,0],[0,2,0,4,0,0,0,1,0],[5,0,0,0,2,0,0,0,7]]
#sp.introSpeech()
#sp.instructionMenu()
