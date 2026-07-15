'''
Entry point for the single-cell/TMA extraction tool
'''

from nicegui import ui, app
from pages import page0, page1, page2, page3, page4
import state

ui.add_head_html('''
<style>
.q-btn.disabled, .q-btn--disable {
    opacity: 0.7; 
    background: #333; 
    color: #999; 
}
.q-page, .nicegui-content {
    width: 100%;
    padding: 5px; 
}
.q-field { 
    width:100%; 
}
.q-card {
    width:100%
}
.q-input {
    white-space: pre-wrap;                 
}
</style>                                  
''', shared=True)

@app.on_shutdown
def close_session():
    if state.session is not None:
        try: state.session.__exit__(None, None, None)
        except Exception as e:
            print(f'Error closing session: {e!r}')

ui.run(
    title='TMA Extraction Tool for SCiLS',      # Browser tab title
    port=8080,           # Default, but explicit is fine
    native=True,         # Opens as a desktop window instead of browser
    reload=False         # Disable auto-reload in production
)
