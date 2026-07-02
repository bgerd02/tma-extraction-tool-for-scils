'''
Script for visual elements of page 2 of TMA Extraction Tool for SCiLS (TMAET for SCiLS)
'''

from nicegui import ui
#from logic import 
import state

# User inputs for this page: feature_list, normalization

@ui.page('/page2')
# Button event handlers
def handle_next_page2():
    state.normalization = normalization.value
    state.feature_list = feature_list.value
    ui.navigate.to('/page3')



### Rendering Logic ###
ui.label('Select the feature list and normalization method')

feature_list = ui.select(
    label='Select feature list:',
    options= [list for list in state.feature_lists],
    value= state.feature_lists[0]
)

normalization= ui.select(
    label='Select normalization method:',
    options=['Total Ion Count', 'Root Mean Square', 'None'],
    value='Total Ion Count'     # default value
)


ui.button('Next', on_click=handle_next_page2())
ui.button('Back', on_click=lambda: ui.navigate.to('/'))