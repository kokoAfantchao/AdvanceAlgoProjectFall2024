from nicegui import ui
import SudokuSolverOptimization

with ui.column():
     ui.label('Sudoku solver with GUI').classes(' justify-center text-2xl font-bold text-center mt-4 ')

diffs = ["Easy", "Medium", "Hard"]
difficulty = 0

def setDiff(newDiff):
     difficulty = newDiff
     difficultySelector.set_text(diffs[difficulty])

difficultySelector = ui.dropdown_button(diffs[difficulty], auto_close=True)

with ui.row():
    with difficultySelector:
        ui.item(diffs[0], on_click=lambda: setDiff(0))
        ui.item(diffs[1], on_click=lambda: setDiff(1))
        ui.item(diffs[2], on_click=lambda: setDiff(2))
    ui.button("Generate", on_click=lambda: generate())

board = [([0]*9) for i in range(9)]
boardReset = True
boardSolved = False

def resetBoard():
    global board
    global boardReset
    board = [([0]*9) for i in range(9)]
    boardReset = True
    boardGrid.refresh()
    statusMsg.set_text("Click Generate to begin.")

@ui.refreshable
def boardGrid():
    with ui.grid(columns=9*'40px ').classes('w-full gap-0'):
        for row in board:
            for col in row:
                ui.label(col).classes('border p-1')

def generate():
    global board
    global boardReset
    global boardSolved
    statusMsg.set_text(f"Generating {diffs[difficulty].lower()} board...")
    board = SudokuSolverOptimization.getANewSudoku(diffs[difficulty].lower())
    boardReset = False
    boardSolved = False
    print(board)
    boardGrid.refresh()
    statusMsg.set_text("Click Solve")

boardGrid()

def solveSudoku():
    global board
    global boardReset
    global boardSolved
    if boardReset == False and boardSolved == False:

        if SudokuSolverOptimization.sudokuSolver(board):
            statusMsg.set_text("Sudoku Solved")
            boardGrid.refresh()
            boardSolved = True
        else:
            statusMsg.set_text("No solution exists.")
    else:
        statusMsg.set_text("Reset the board first")
        

with ui.row():
    ui.button('Reset', on_click=lambda: resetBoard())
    ui.button('Solve', on_click=lambda: solveSudoku())

statusMsg = ui.label("Ready")


ui.run()