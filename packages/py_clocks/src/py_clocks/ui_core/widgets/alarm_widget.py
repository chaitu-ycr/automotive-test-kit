import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from nicegui import ui


class Alarm:
    def __init__(self):
        self.alarms: List[Dict] = []
        self.alarm_container: Optional[ui.column] = None
        self.store_path: Path = Path.home() / '.pyclocks_alarms.json'

    def render(self):
        self.load_alarms()
        with ui.card().classes('w-full').style('background: transparent; border: none; padding: 0; height: 100%; display: flex; flex-direction: column;'):
            ui.button('➕ ADD ALARM', on_click=self.show_add_alarm_dialog).props('flat').classes('w-full mb-2 py-1 text-sm font-bold').style('background: #ff00ff; color: #000000; border: 2px solid #cc00cc; border-radius: 0px; font-family: "Courier New", monospace; letter-spacing: 1px;')
            with ui.scroll_area().classes('w-full').style('flex: 1; min-height: 0; background: #0a000a; border: 2px solid #cc00cc; border-radius: 0px; padding: 4px;'):
                self.alarm_container = ui.column().classes('w-full gap-2')
                if not self.alarms:
                    with ui.card().classes('w-full').style('background: transparent; border-radius: 0px; padding: 8px;'):
                        ui.label('NO ALARMS SET').classes('text-center text-xs font-bold').style('color: #ff00ff; font-family: "Courier New", monospace; opacity: 0.6;')
                else:
                    for a in self.alarms:
                        self.render_alarm(a)

    def show_add_alarm_dialog(self):
        with ui.dialog() as dialog, ui.card().classes('p-6').style('min-width: 300px; border-radius: 12px;'):
            ui.label('⏰ Add New Alarm').classes('text-xl font-bold mb-4')
            with ui.row().classes('gap-4 mb-6 justify-center'):
                with ui.column().classes('items-center'):
                    ui.label('Hour').classes('text-sm mb-1')
                    hour_input = ui.number(value=8, min=0, max=23).props('outlined').classes('w-24')
                with ui.column().classes('items-center'):
                    ui.label('Minute').classes('text-sm mb-1')
                    minute_input = ui.number(value=0, min=0, max=59).props('outlined').classes('w-24')
            label_input = ui.input('Label', placeholder='Wake up, Morning workout, etc.').props('outlined').classes('w-full mb-6')
            with ui.row().classes('w-full justify-end gap-3'):
                ui.button('Cancel', on_click=dialog.close).props('flat size=md').classes('px-6')
                ui.button('Add Alarm', on_click=lambda: self.add_alarm(int(hour_input.value), int(minute_input.value), label_input.value, dialog)).props('rounded size=md').classes('px-8').style('background: #10B981; color: white;')
        dialog.open()

    def add_alarm(self, hour: int, minute: int, label: str, dialog):
        alarm = {'hour': hour, 'minute': minute, 'label': label or 'Alarm', 'enabled': True, 'id': len(self.alarms)}
        self.alarms.append(alarm)
        self.render_alarm(alarm)
        ui.notify(f'✅ Alarm set for {hour:02d}:{minute:02d}', type='positive', position='top')
        dialog.close()

    def render_alarm(self, alarm: Dict):
        with self.alarm_container:
            with ui.card().classes('w-full').style('background: #330033; border-radius: 0px; border: 2px solid #ff00ff; padding: 8px;'):
                with ui.row().classes('w-full justify-between items-center'):
                    with ui.column():
                        ui.label(f"{alarm['hour']:02d}:{alarm['minute']:02d}").classes('text-xl font-bold').style('color: #ff00ff; font-family: "Courier New", monospace; text-shadow: 0 0 6px rgba(255,0,255,0.6);')
                        ui.label(alarm['label']).classes('text-xs').style('color: #ff00ff; font-family: "Courier New", monospace; opacity: 0.8; margin-top: 2px;')
                    with ui.row().classes('gap-2 items-center'):
                        ui.switch(value=alarm['enabled'], on_change=lambda e, a=alarm: self.toggle_alarm_enabled(a, e.value)).props('color=purple')
                        ui.button(icon='delete', on_click=lambda a=alarm: self.delete_alarm(a)).props('flat round size=sm').style('color: #ff0000; background: rgba(255,0,0,0.1);')

    def delete_alarm(self, alarm: Dict):
        ui.notify('🗑️ Alarm deleted', type='info', position='top')
        self.alarms.remove(alarm)
        self.save_alarms()
        self.alarm_container.clear()
        for a in self.alarms:
            self.render_alarm(a)
        if not self.alarms:
            with self.alarm_container:
                with ui.card().classes('w-full').style('background: transparent; border-radius: 0px; padding: 8px;'):
                    ui.label('NO ALARMS SET').classes('text-center text-xs font-bold').style('color: #ff00ff; font-family: "Courier New", monospace; opacity: 0.6;')

    def toggle_alarm_enabled(self, alarm: Dict, enabled: bool):
        alarm['enabled'] = bool(enabled)
        self.save_alarms()

    def save_alarms(self):
        try:
            serializable = [{k: v for k, v in a.items() if k in {'hour', 'minute', 'label', 'enabled', 'id', 'last_trigger'}} for a in self.alarms]
            self.store_path.write_text(json.dumps(serializable, indent=2))
        except Exception as e:
            logging.error(f'Failed to save alarms: {e}')

    def load_alarms(self):
        try:
            if self.store_path.exists():
                data = json.loads(self.store_path.read_text())
                if isinstance(data, list):
                    self.alarms = data
        except Exception as e:
            logging.error(f'Failed to load alarms: {e}')
