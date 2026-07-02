'''
Script for visual elements of page 4
'''

from nicegui import ui
from logic import extract_spots
import state

@ui.page('/page4')

def handle_extract():
    state.extract_spots(
        normalization=state.normalization, 
        feature_list=state.feature_list, 
        attribute=state.attribute, 
        export_type=export_type,
        output_directory=output_directory
    )


### Rendering logic ###
ui.label('Select export type and directory')

export_type = ui.select(
    label='Export type',
    options=['.csv', '.txt'],
)

output_directory = ui.input(label='Output directory')

ui.button('Extract', on_click=handle_extract())