'''
Script for visual elements of page 4
'''

from nicegui import ui, run, timer
from logic import extract_spots
import state
import os

@ui.page('/page4')
def page4():
    status = {'message': ''}

    def on_progress(message):  
        status['message'] = message
    
    def refresh_status():
        result_label.text = status['message']

    async def handle_extract(btn: ui.button):
        btn.loading = True
        status['message'] = 'Starting extraction...'
        timer.active = True
        state.output_path = output_directory.value
        state.export_type = export_type.value
        try:
            if not os.path.isdir(state.output_path) : raise FileNotFoundError('Directory not found at specified path')
            await run.io_bound(extract_spots, on_progress)
            result_label.text = 'Extraction complete!'
        except Exception as e: 
            result_label.text = f'Error :{e}'
        finally: 
            timer.active = False
            btn.loading = False


    def extract_enabler():
        extract_button.enabled = bool(export_type.value) and bool(output_directory.value)


    

    ### Rendering logic ###
    ui.label('Select export type and directory')

    export_type = ui.select(
        label='Export type',
        options=['.csv', '.txt'],
        on_change=extract_enabler
    )

    output_directory = ui.input(label='Output directory', on_change=extract_enabler)
    
    result_label = ui.label('')
    timer = ui.timer(0.5, refresh_status, active=False)

    with ui.row().classes('w-full justify-between'):
        ui.button('Back', on_click=lambda: ui.navigate.to('/page3'))
        extract_button = ui.button('Extract', on_click=lambda e: handle_extract(e.sender))
        extract_button.enabled = False
