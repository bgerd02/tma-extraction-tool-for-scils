'''
Script for visual elements of page 1 of TMA Extraction Tool for SCiLS (TMAET for SCiLS)
'''

from scilslab import LocalSession
from nicegui import ui, run
from logic import get_feature_lists
import state

exe_path = r'C:\Users\AngelLab\Desktop\SCiLS Lab\scilsMsServer.exe'         # Need to change for different computers

@ui.page('/')
def page1():
# Event handler(s)
    def _open_session_blocking(slx_path):
        "Runs in a worker thread, safe to block here"
        session = LocalSession(slx_path, executable=exe_path)
        session.__enter__()
        state.dataset = session.dataset_proxy
        feature_lists = get_feature_lists(slx_path)
        return session, feature_lists


    async def handle_next_page1(btn: ui.button):
        state.slx_path = slx_path.value

        # Turn on loading spinner
        btn.props('loading')

        # Close any existing session before opening a new one
        if state.session is not None:
            try:
                state.session.__exit__(None, None, None)
            except Exception as e:
                print(f'Error closing previous session: {e!r}')
            state.session = None

        try:
            state.session, state.feature_lists = await run.io_bound(
                _open_session_blocking, state.slx_path) 
        except Exception as e:
            ui.notify(f'Failed to open SCiLS session: {e}', type='negative')
            print(f'LocalSession error: {e!r}')
            state.session = None
            return
   
        btn.props(remove='loading')

        ui.navigate.to('/page2')


    #### Rendering logic ####
    ui.label('TMA Extraction Tool for SCiLS')

    slx_path = ui.input(label='Path to .slx file:', placeholder=r'ex. C:\Users\AngelLab\Desktop\slcc_heavy.slx')

    ui.button('Next', on_click=lambda e: handle_next_page1(e.sender)).bind_enabled_from(slx_path, 'value')


# TODO
# disable next button if nothing input
# figure out how to pass info between pages
# add loading/check for next so api has time to get feature list/check that there is a file at that location

# NOTE, for readme add: one common issue that can come up is the tool has a hard time locating the ____.exe file for SCiLS. 
# If you encounter any issues when running the tool, you may need to edit logic.py and change exe_path 