import tkinter
import requests

def checkValidity(num, row, col, sudoku):
    # For row and column
    for i in range(9):
        if sudoku[row][i] == num or sudoku[i][col] == num:
            return False
    
    # For grid
    gridRow, gridCol = 3 * (row // 3), 3 * (col // 3)
    for i in range(gridRow, gridRow + 3):
        for j in range(gridCol, gridCol + 3):
            if sudoku[i][j] == num:
                return False
    
    return True

def nextEmptyCell(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:  
                return (i, j)
    return None

def printBoard(sudoku):
    for rows in sudoku:
        row = ""
        for num in rows:
            row += str(num) + " "
        print(row)

def sudokuSolver(sudoku):
    
    emptyCell = nextEmptyCell(sudoku)
    if not emptyCell:
        return True  # no empty cell left

    row, col = emptyCell

    for num in range(1, 10):  
        if checkValidity(num, row, col, sudoku):
            sudoku[row][col] = num  

            if sudokuSolver(sudoku): 
                return True

            sudoku[row][col] = 0  # change wrong placement to 0

    return False  # backtrack



def getANewSudoku(diffLevel):
    apiURL = f"https://sugoku.onrender.com/board?difficulty={diffLevel}"
    response = requests.get(apiURL)
    sudoku_board = response.json()['board']
    return sudoku_board

def start():
    sudoku = getANewSudoku()
    print("Given Sudoku:")
    printBoard(sudoku)
    print("")

    if sudokuSolver(sudoku):
        print("Solved Sudoku:")
        printBoard(sudoku)
    else:
        print("No solution exists.")

#start()