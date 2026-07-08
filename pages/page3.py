'''
Script for visual elements of page 3 of TMA Extraction Tool for SCiLS (TMAET for SCiLS)
'''
from nicegui import ui
from logic import check_for_attribute
import state


@ui.page('/page3')
def page3():
    def handle_attribute_check():
        state.attribute = attribute.value
        num_regions = check_for_attribute()
        result_label.text = f'Found {num_regions} region(s) with this attribute.'

    def next_enabler():
        next_button.enabled = bool(attribute.value) or all_checkbox.value

    def handle_next_page3():
        state.attribute = attribute.value
        ui.navigate.to('/page4')



    ### Rendering logic ###
    ui.label('Enter the attribute of the region(s) you would like to extract')

    attribute = ui.input(label='Region attribute', placeholder='ex. stage 1', on_change=next_enabler)
    ui.button('Check existance/abundance of attribute', on_click= handle_attribute_check)
    result_label = ui.label('')        # Empty label that will hold result of handle_attribute_check

    all_checkbox = ui.checkbox('Extract all', on_change=next_enabler)
    

    ui.button('Back', on_click=lambda: ui.navigate.to('/page2'))
    next_button = ui.button('Next', on_click=handle_next_page3)
    next_button.enabled=False   # initial state


### TODO
# have loading thing associated with check existance button
# allow attribute to be comma separated list