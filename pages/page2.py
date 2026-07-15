'''
Script for visual elements of page 2 of TMA Extraction Tool for SCiLS (TMAET for SCiLS)
'''

from nicegui import ui
#from logic import 
import state

# User inputs for this page: feature_list, normalization

@ui.page('/page2')
def page2():
    # Button event handlers
    def handle_next_page2():
        state.normalization = normalization.value
        state.feature_list = feature_list.value
        ui.navigate.to('/page3')



    ### Rendering Logic ###
    ui.label('Select the feature list and normalization method')

    feature_list = ui.select(
        label='Select feature list:',
        options= state.feature_lists['name'].tolist(),
        value= state.feature_lists['name'].iloc[0]  # default value
    )

    normalization= ui.select(
        label='Select normalization method:',
        options=state.normalization_types['description'].tolist(),
        value='Total Ion Count'     # default value
    )

    ui.button('Back', on_click=lambda: ui.navigate.to('/page1'))
    ui.button('Next', on_click=handle_next_page2).bind_enabled_from(feature_list, 'value')