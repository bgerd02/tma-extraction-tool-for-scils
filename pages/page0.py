'''
Entry page for first loading of .exe file--prompts user to paste the path to the scilsMsServer.exe
'''
import sys
from nicegui import ui
import os
import json
import state

base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
JSON_PATH = os.path.join(base, 'tmaet.json')

@ui.page('/')
def page0():
    def check_exe_existance():
        # If no json file exists, create an empty one
        if not os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'w') as f:
                json.dump({}, f)
            return None
        # Catch case where json file is corrupted/improperly formatted
        try: 
            with open(JSON_PATH, 'r') as f:      
                data = json.load(f)
        except json.JSONDecodeError:
            return None
        
        return data.get('EXE_PATH')

    EXE_PATH = check_exe_existance()

    if EXE_PATH is not None and os.path.exists(EXE_PATH):
        state.EXE_PATH = EXE_PATH
        ui.navigate.to('/page1')
        return
    
    with ui.dialog().props('persistent') as dialog, ui.card():
        exe_path_input = ui.input('Enter the path to scilsMsServer.exe. It will be located in your SCiLS Lab folder, which is likely in Program Files or Desktop depending on your computer.'
                                  , placeholder='ex. C:/Program Files/SCiLS Lab/scilsMsServer.exe')
        def save():
            if not os.path.exists(exe_path_input.value):
                ui.notify('That path does not exist -- please check it and try again.', type='negative')
                return
            with open(JSON_PATH, 'w') as f:
                json.dump({'EXE_PATH': exe_path_input.value}, f)
            state.EXE_PATH = exe_path_input.value
            dialog.close()
            ui.navigate.to('/page1')
        ui.button('Save', on_click=save)

    dialog.open()