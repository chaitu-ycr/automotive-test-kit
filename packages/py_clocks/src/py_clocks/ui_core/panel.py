from contextlib import contextmanager
from nicegui import ui


@contextmanager
def panel_section(title: str, accent: str, bg: str):
    with ui.column().classes('panel').style(f'--accent: {accent}; --panel-bg: {bg};'):
        ui.label(title).classes('panel-title')
        with ui.element('div').classes('panel-body'):
            yield
