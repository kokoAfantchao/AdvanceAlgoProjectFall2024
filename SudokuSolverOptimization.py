import requests
import sys

def checkValidity(number, row, col, sudoku):
    # Validity for Row and column
    for i in range(9):
        if sudoku[row][i] == number or sudoku[i][col] == number:
            return False
    
    # Validity for sub grids
    gridRow, gridCol = 3 * (row // 3), 3 * (col // 3)
    for i in range(gridRow, gridRow + 3):
        for j in range(gridCol, gridCol + 3):
            if sudoku[i][j] == number:
                return False
    
    return True

def nextEmptyCell(sudoku):
    #Finding the next empty cell in the board
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:  
                return (i, j)
    return None


def getPossibleValues(board):
    # Making possibleValues array for every cell
    possibleValues = {}
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:  
                possibleValues[(r, c)] = getPossibleValuesHelper(board, r, c)
    return possibleValues


def getPossibleValuesHelper(board, row, col):
    # Discard already existing numbers according to the sudoku rules from possibleValues array
    possibleValues = set(range(1, 10))
    for x in range(9):
        possibleValues.discard(board[row][x])  
        possibleValues.discard(board[x][col])  

    sRow, sCol = 3 * (row // 3), 3 * (col // 3)
    for i in range(sRow, sRow + 3):
        for j in range(sCol, sCol + 3):
            possibleValues.discard(board[i][j])  

    return possibleValues

def applySingleton(board,possibleValues):
    # Apply singleton Strategy Recursively - 
    # If any cell's possibleValue array has only 1 element, enter that element in that cell, 
    # then remove that number from other cells and delete that cell's possibleValue array
    singletons = {}
    for cell,elements in possibleValues.items():
        if len(elements)==1:
            r=cell[0]
            c=cell[1]
            number=list(elements)[0]
            board[r][c] = number
            singletons[cell] = number
            print("Cell ",cell,number)
    if singletons=={}:
        return
    
    for (r,c),number in singletons.items():
        for x in range(9):
            if (r,x) in possibleValues:
                if len(possibleValues[(r,x)])==1 and possibleValues[(r,x)]=={number}:
                    del possibleValues[(r,x)]
                else:
                    possibleValues[(r,x)].discard(number)  # Row
            if (x,c) in possibleValues:
                if len(possibleValues[(x,c)])==1 and possibleValues[(x,c)]=={number}:
                    del possibleValues[(x,c)]
                else:
                    possibleValues[(x,c)].discard(number)  # Row

        sRow, sCol = 3 * (r // 3), 3 * (c // 3)
        for i in range(sRow, sRow + 3):
            for j in range(sCol, sCol + 3):
                if (i,j) in possibleValues:
                    if len(possibleValues[(i,j)])==1 and possibleValues[(i,j)]=={number}:
                        del possibleValues[(i,j)]
                    else:
                        possibleValues[(i,j)].discard(number)  # 3x3 Box
    applySingleton(board,possibleValues)      

def applyHiddenPairs(board, possibleValues):
    # Applying HiddenPair strategy for rows,columns and grids
    for index in range(9):
        applyHiddenPairsFor(board, index, 'row', possibleValues)
        applyHiddenPairsFor(board, index, 'col', possibleValues)
        applyHiddenPairsFor(board, index, 'box', possibleValues)

def applyHiddenTriplets(board, possibleValues):
    # Applying HiddenTriplet strategy for rows,columns and grids
    for index in range(9):
        applyHiddenTripletsFor(board, index, 'row', possibleValues)
        applyHiddenTripletsFor(board, index, 'col', possibleValues)
        applyHiddenTripletsFor(board, index, 'box', possibleValues)

def applyHiddenPairsFor(board, index, group, possibleValues):
    # Applying HiddenPair Strategy -
    # If two numbers appear in only 2 cells of a row/column/grid, 
    # then the other elements in those cell's possibleValue array can be eliminated 
    options = {}

    if group == 'row':
        for col in range(9):
            if board[index][col] == 0:
                options[(index, col)] = possibleValues[(index, col)]

    elif group == 'col':
        for row in range(9):
            if board[row][index] == 0:
                options[(row, index)] = possibleValues[(row, index)]

    elif group == 'box':
        sRow, sCol = 3 * (index // 3), 3 * (index % 3)
        for r in range(sRow, sRow + 3):
            for c in range(sCol, sCol + 3):
                if board[r][c] == 0:
                    options[(r, c)] = possibleValues[(r, c)]
    
    counts = {}
    for cell, elements in options.items():
        for number in elements:
            counts.setdefault(number, set()).add(cell)

    # Find hidden pairs
    hiddenPairs = {}
    for num1, cell1 in counts.items():
        for num2, cell2 in counts.items():
            if num1 < num2 and cell1 == cell2 and len(cell1) == 2:
                hiddenPairs[(num1, num2)] = cell1

    print("HiddenPairs: ",hiddenPairs)

    # Remove other elements from the cell's possibleValues array
    for (num1, num2), cells in hiddenPairs.items():
        for cell in cells:
            possibleValues[cell] = {num1,num2}
            
        
    

def applyHiddenTripletsFor(board, index, group, possibleValues):
    # Applying HiddenTriplet Strategy -
    # If three numbers appear in only 3 cells of a row/column/grid, 
    # then the other elements in those cell's possibleValue array can be eliminated 
    options = {}

    if group == 'row':
        for col in range(9):
            if board[index][col] == 0:
                options[(index, col)] = possibleValues[(index, col)]

    elif group == 'col':
        for row in range(9):
            if board[row][index] == 0:
                options[(row, index)] = possibleValues[(row, index)]

    elif group == 'box':
        sRow, sCol = 3 * (index // 3), 3 * (index % 3)
        for r in range(sRow, sRow + 3):
            for c in range(sCol, sCol + 3):
                if board[r][c] == 0:
                    options[(r, c)] = possibleValues[(r, c)]
    
    
    counts = {}
    for cell, elements in options.items():
        for number in elements:
            if number not in counts:
                counts.setdefault(number, set()).add(cell)

    # Find hidden triplets
    hiddenTriplets = {}
    for num1, cell1 in counts.items():
        for num2, cell2 in counts.items():
            for num3, cell3 in counts.items():
                if num1 < num2 < num3 and cell1 == cell2 == cell3 and len(cell1) == 3:
                    hiddenTriplets[(num1, num2, num3)] = cell1

    print("HiddenTriplets: ",hiddenTriplets)

    #Remove other options from the cell's possibleValues array
    for (num1, num2, num3), cells in hiddenTriplets.items():
        for cell in cells:
            possibleValues[cell] = {num1,num2,num3}


def sudokuSolver(sudoku):
    
    possibleValues = getPossibleValues(sudoku)  # Get possibleValues array for all cells
    applySingleton(sudoku,possibleValues) #apply singleton
    applyHiddenPairs(sudoku, possibleValues)  # Apply hiddenPairs
    applyHiddenTriplets(sudoku, possibleValues)  # Apply hiddenTriplets
    print("possibleValues: ",possibleValues)
    with open("output.txt", "w") as file:
        return solverHelper(sudoku,possibleValues,file)

def solverHelper(sudoku,possibleValues,file):
    emptyCell = nextEmptyCell(sudoku)
    if not emptyCell:
        return True  # Sudoku has been solved

    row, col = emptyCell
    current_possibleValues = possibleValues.get((row, col), set())
    for number in current_possibleValues:  
        if checkValidity(number, row, col, sudoku):
            sudoku[row][col] = number  
            pretty_print_sudoku(sudoku,file)
            if solverHelper(sudoku,possibleValues,file): 
                return True

            sudoku[row][col] = 0  
    return False  



def getANewSudoku(diffLevel):
    apiURL = f"https://sugoku.onrender.com/board?difficulty={diffLevel}"
    response = requests.get(apiURL)
    sudoku_board = response.json()['board']
    return sudoku_board


def pretty_print_sudoku(board,file):
    # Prints all steps of value filling in output.txt 
    print("",file=file)
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21,file=file)
        for j, number in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ",file=file)
            if number == 0:
                print(".", end=" ",file=file)
            else:
                print(number, end=" ",file=file)

        print("",file=file)