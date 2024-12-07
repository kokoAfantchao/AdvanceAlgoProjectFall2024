from operator import is_not

from jinja2.optimizer import optimize
from nicegui import ui
from typing_extensions import get_origin
from uvicorn.protocols.utils import get_local_addr

import SudokuSolverOptimization
import asyncio
import  copy
with ui.column():
     ui.label('Sudoku solver with GUI').classes(' justify-center text-2xl font-bold text-center mt-4 ')

diffs = ["Easy", "Medium", "Hard"]
difficulty = 0
elapsed = 0
# basicTask = None
# optimizeTask = None
timerTask = None
timeEvent = asyncio.Event()

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
    global timer_label
    global timeEvent
    global timerTask
    board = [([0]*9) for i in range(9)]
    boardOptimized = [([0]*9) for i in range(9)]
    elapsed = 0
    timeEvent.set()
    timeEvent.clear()

    timer_label.set_text(f"Time: {elapsed} seconds")
    uptiFinaltime.set_text(f"Optimized Algo Time: {elapsed} seconds")
    finaltime.set_text(f"Basic Algo Time: {elapsed} seconds")

    if  basicTask and not basicTask.done():
        basicTask.cancel()
    if  optimizeTask and not optimizeTask.done() :
        optimizeTask.cancel()
    boardReset = True
    boardGrid.refresh()
    statusMsg.set_text("Click Generate to begin.")

async def counting_up_timer(timeEvent):
    global elapsed
    while not timeEvent.is_set():
       # / timer_label.set_text(f"Time: {elapsed} seconds")
        await asyncio.sleep(0.01)
        elapsed = round(elapsed + 1/100.00, 2)

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
    uptiFinaltime = ui.label('Optimized Algo Time:  ').classes('justify-center text-2xl font-bold text-center mt-4')

def generate():
    global board
    global boardOptimized
    global boardReset
    global boardSolved
    global  elapsed
    statusMsg.set_text(f"Generating {diffs[difficulty].lower()} board...")
    board = SudokuSolverOptimization.getANewSudoku(diffs[difficulty].lower())
    if board is None:
        statusMsg.set_text("Failed to generate board ")
        ui.notify("Failed to generate board, Please retry again",position="top", duration=1, type="negative",multi_line=True)
        return
    boardOptimized = copy.deepcopy(board)
    boardReset = False
    boardSolved = False
    elapsed = 0
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
    global basicTask
    global optimizeTask
    global timeEvent
    global timerTaks
    if boardReset == False and boardSolved == False:
        event = asyncio.Event()
        event_2 = asyncio.Event()
        timerTaks = asyncio.create_task(counting_up_timer(timeEvent))
        optimizeTask  = asyncio.create_task(SudokuSolverOptimization.sudokuSolver(boardOptimized, updateFastCell, event, finaltimeUpdate))
        basicTask = asyncio.create_task(SudokuSolverOptimization.resolverUnoptimized(board, updateCell, event_2, finaltimeUpdate))
        if ( await event.wait() and await event_2.wait()):
             timeEvent.set()
             timerTaks.cancel()
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