'''
Script for visual elements of page 1 of TMA Extraction Tool for SCiLS (TMAET for SCiLS)
'''

from scilslab import LocalSession
from nicegui import ui
from logic import get_feature_lists
import state

exe_path = r'C:\Users\AngelLab\Desktop\SCiLS Lab\scilsMsServer.exe'         # Need to change for different computers

@ui.page('/')
def page1():
# Button event handler(s)
    def handle_next_page1():
        state.slx_path = slx_path

        with LocalSession(slx_path, executable=exe_path) as session:
            state.dataset = session.dataset_proxy

        state.feature_lists = get_feature_lists(slx_path)
        ui.navigate.to('/page2')


    #### Rendering logic ####
    ui.label('TMA Extraction Tool for SCiLS')

    slx_path = ui.input(label='Path to .slx file:', placeholder=r'ex. C:\Users\AngelLab\Desktop\slcc_heavy.slx')

    ui.button('Next', on_click=handle_next_page1).bind_enabled_from(slx_path, 'value')


# TODO
# disable next button if nothing input
# figure out how to pass info between pages
# add loading/check for next so api has time to get feature list/check that there is a file at that location

# NOTE, for readme add: one common issue that can come up is the tool has a hard time locating the ____.exe file for SCiLS. 
# If you encounter any issues when running the tool, you may need to edit logic.py and change exe_path 