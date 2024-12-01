from operator import is_not

from nicegui import ui
import SudokuSolverOptimization
import asyncio
import  copy
with ui.column():
     ui.label('Sudoku solver with GUI').classes(' justify-center text-2xl font-bold text-center mt-4 ')

diffs = ["Easy", "Medium", "Hard"]
difficulty = 0
elapsed = 0
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
boardOptimized = [([0]*9) for i in range(9)]
boardReset = True
boardSolved = False
def updateCell(row: int, col: int, value: int):
    global board
    board[row][col] = value
    boardGrid.refresh()

def updateFastCell(row: int, col: int, value: int):
    global boardOptimized
    boardOptimized[row][col] = value
    boardGrid.refresh()


def resetBoard():
    global board
    global  boardOptimized
    global boardReset
    global elapsed
    board = [([0]*9) for i in range(9)]
    boardOptimized = [([0]*9) for i in range(9)]
    elapsed = 0
    boardReset = True
    boardGrid.refresh()
    statusMsg.set_text("Click Generate to begin.")

async def counting_up_timer(timeEvent):
    global elapsed
    while not timeEvent.is_set():
       # / timer_label.set_text(f"Time: {elapsed} seconds")
        await asyncio.sleep(1)
        elapsed += 1

@ui.refreshable
def boardGrid():
    global timer_label

    global uptiFinaltime
    timer_label = ui.label(f"Time: {elapsed} seconds").classes('justify-center text-2xl font-bold text-center mt-4')
    with ui.row():
        with ui.column():
            ui.label('Sudoku basic algorithm').classes('text-center font-bold text-xl mt-4')
            with ui.grid(columns=9*'40px ').classes('gap-0'):
                for row in board:
                    for col in row:
                        ui.label(col).classes('border p-1')

        with ui.column():
            ui.label('Sudoku  optimized algorithm').classes('text-center font-bold text-xl mt-4')
            with ui.grid(columns=9*'40px ').classes('gap-0'):
                    for row in boardOptimized:
                        for col in row:
                            ui.label(col).classes('border p-1')


with ui.column():
    finaltime = ui.label('Basic Algo Time: ').classes('justify-center text-2xl font-bold text-center mt-4')
with ui.column():
    uptiFinaltime = ui.label('Optimized Time:  ').classes('justify-center text-2xl font-bold text-center mt-4')

def generate():
    global board
    global boardOptimized
    global boardReset
    global boardSolved
    statusMsg.set_text(f"Generating {diffs[difficulty].lower()} board...")
    board = SudokuSolverOptimization.getANewSudoku(diffs[difficulty].lower())
    boardOptimized = copy.deepcopy(board)
    boardReset = False
    boardSolved = False
    print(board)
    boardGrid.refresh()
    statusMsg.set_text("Click Solve")

boardGrid()
def finaltimeUpdate(typeresolved = "basic"):
    if typeresolved == "basic":
        finaltime.set_text(f"Basic Algo Time: {elapsed} seconds")
    else :
        uptiFinaltime.set_text(f"Optimized Time: {elapsed} seconds")


async def  solveSudoku():
    global board
    global boardOptimized
    global boardReset
    global boardSolved
    if boardReset == False and boardSolved == False:
        event = asyncio.Event()
        event_2 = asyncio.Event()
        timeEvent = asyncio.Event()
        asyncio.create_task(counting_up_timer(timeEvent))
        asyncio.create_task(SudokuSolverOptimization.sudokuSolver(boardOptimized, updateFastCell, event, finaltimeUpdate))
        asyncio.create_task(SudokuSolverOptimization.resolverUnoptimized(board, updateCell, event_2, finaltimeUpdate))
        if ( await event.wait() and await event_2.wait()):
             timeEvent.set()
             statusMsg.set_text("Sudoku Solved")
             boardGrid.refresh()
             boardSolved = True
        else:
            statusMsg.set_text("No solution exists.")
    else:
        statusMsg.set_text("Reset the board first")

async def asyncSolver():
    await solveSudoku()

with ui.row():
    ui.button('Reset', on_click=lambda: resetBoard())
    ui.button('Solve', on_click=lambda: asyncio.create_task(asyncSolver()))

statusMsg = ui.label("Ready")

ui.run()