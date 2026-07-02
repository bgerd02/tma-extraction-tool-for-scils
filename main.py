'''
Entry point for the single-cell/TMA extraction tool
'''


from nicegui import ui
from pages import page1, page2, page3

ui.run(
    title='TMA Extraction Tool for SCiLS',      # Browser tab title
    port=8080,           # Default, but explicit is fine
    native=True,         # Opens as a desktop window instead of browser
    reload=False         # Disable auto-reload in production
)

ui.run()