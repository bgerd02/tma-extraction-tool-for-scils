'''
Script for visual elements of page 4
'''

from nicegui import ui, run
from logic import extract_spots
import state

@ui.page('/page4')
def page4():
    async def handle_extract(btn: ui.button):

        btn.props('loading')

        state.output_path = output_directory.value
        state.export_type = export_type.value
        await run.io_bound(extract_spots)

        btn.props(remove='loading')
        result_label.text = 'Extraction complete!'


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
    ui.button('Back', on_click=lambda: ui.navigate.to('/page3'))
    extract_button = ui.button('Extract', on_click=lambda e: handle_extract(e.sender))
    extract_button.enabled = False
