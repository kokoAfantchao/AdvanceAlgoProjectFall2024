from nicegui import ui


with ui.column():
     ui.label('Sodoku resolver  with GUI').classes(' justify-center text-2xl font-bold text-center mt-4 ')

with ui.row():

        with ui.dropdown_button('Game Leve', auto_close=True):
            ui.item('Level 1', on_click=lambda: ui.notify('You clicked item 1'))
            ui.item('Level 2', on_click=lambda: ui.notify('You clicked item 2'))
            ui.item('Level 3', on_click=lambda: ui.notify('You clicked item 3'))
        level = ui.label('Time: 00:00:00', ).classes('text-center')

with ui.grid(columns='40px 40px 40px 40px 40px 40px 40px 40px 40px').classes('w-full gap-0'):
    for _ in range(9):
        ui.label('6').classes('border p-1')
        ui.label('5').classes('border p-1')
        ui.label('1').classes('border p-1')
        ui.label('9').classes('border p-2')
        ui.label('0').classes('border p-1')
        ui.label('7').classes('border p-1')
        ui.label('8').classes('border p-1')
        ui.label('3').classes('border p-1')
        ui.label('2').classes('border p-1')

with ui.row():
    ui.button('Reset', on_click=lambda: ui.notify('You clicked me!'))
    ui.button('resolve', on_click=lambda:  ui.notify('You clicked me!'))


ui.run()