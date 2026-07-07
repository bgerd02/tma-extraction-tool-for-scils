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

    def handle_next_page3():
        state.attribute = attribute.value
        ui.navigate.to('/page4')


    ### Rendering logic ###
    ui.label('Enter the attribute of the region(s) you would like to extract')

    attribute = ui.input(label='Region attribute', placeholder='ex. stage 1')
    ui.button('Check existance/abundance of attribute', on_click= handle_attribute_check)
    result_label = ui.label('')        # Empty label that will hold result of handle_attribute_check

    all_checkbox = ui.checkbox('Extract all')
    

    ui.button('Back', on_click=lambda: ui.navigate.to('/page2'))
    ui.button('Next', on_click=handle_next_page3).bind_enabled_from(
        attribute, 'value', backward=lambda v: bool(v) or all_checkbox.value
    )


### TODO
# have loading thing associated with check existance button
# allow attribute to be comma separated list