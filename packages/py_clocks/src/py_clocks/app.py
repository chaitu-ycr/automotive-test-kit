import logging
from datetime import datetime
from typing import List
from nicegui import ui

from py_clocks.ui_core.ui_theme import apply_theme
from py_clocks.ui_core.panel import panel_section
from py_clocks.ui_core.widgets.clock_widget import ClockWidget
from py_clocks.ui_core.widgets.stopwatch_widget import Stopwatch
from py_clocks.ui_core.widgets.timer_widget import Timer
from py_clocks.ui_core.widgets.alarm_widget import Alarm
from py_clocks.ui_core.utils import play_beep


class PyClocks:
    UPDATE_INTERVAL = 0.1

    def __init__(self, panel_width: int = 400, panel_height: int = 300, timezones: List[dict] | None = None):
        self.panel_width = panel_width
        self.panel_height = panel_height
        self.clocks: List[ClockWidget] = []
        self.stopwatch = Stopwatch()
        self.timer = Timer()
        self.alarm = Alarm()
        self.format_24h = False
        self.date_format = 'ISO'
        self.timezones = timezones or [
            {"timezone": "Asia/Kolkata", "label": "🇮🇳 INDIA", "bg_color": "#ffcc00", "text_color": "#000000"},
            {"timezone": "Europe/Berlin", "label": "🇩🇪 GERMANY", "bg_color": "#00aaff", "text_color": "#000000"},
            {"timezone": "Asia/Tokyo", "label": "🇯🇵 JAPAN", "bg_color": "#ff4444", "text_color": "#ffffff"},
        ]
        logging.info("PyClocks initialized")

    def setup_ui(self):
        apply_theme(self.panel_width, self.panel_height)

        with ui.header(elevated=True).classes('items-center').style('background: #00ffff; padding: 8px; border-bottom: 4px solid #00cccc;'):
            with ui.row().classes('items-center justify-between w-full'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('schedule', size='1.4rem').classes('text-black')
                    ui.label('PY_CLOCKS').classes('text-lg font-bold').style('color: #000000; font-family: "Courier New", monospace; letter-spacing: 2px;')
                with ui.row().classes('items-center gap-2'):
                    ui.label('24H').classes('text-black text-xs font-bold')
                    ui.switch(value=self.format_24h, on_change=lambda e: self.set_24h(e.value)).props('dense').classes('retro-toggle')
                    ui.label('Date').classes('text-black text-xs font-bold')
                    ui.switch(value=(self.date_format == 'Locale'), on_change=lambda e: self.set_date_format('Locale' if e.value else 'ISO')).props('dense').classes('retro-toggle')

        with ui.column().classes('w-full').style('height: calc(100vh - 55px); overflow: hidden; padding: 12px;'):
            with ui.element('div').classes('w-full app-grid'):
                with panel_section('🌍 WORLD CLOCK', accent='#ffff00', bg='#1a1a00'):
                    with ui.column().classes('gap-1').style('display: flex; flex: 1; min-height: 0; gap: 2px;'):
                        for cfg in self.timezones:
                            c = ClockWidget(cfg['timezone'], cfg['label'], cfg['bg_color'], cfg['text_color'])
                            c.set_format(self.format_24h)
                            c.set_date_format(self.date_format)
                            c.render()
                            self.clocks.append(c)

                with panel_section('⏱️ STOPWATCH', accent='#00ff00', bg='#001a00'):
                    self.stopwatch.render()

                with panel_section('⏲️ TIMER', accent='#00ffff', bg='#001a1a'):
                    self.timer.render()

                with panel_section('⏰ ALARMS', accent='#ff00ff', bg='#1a001a'):
                    self.alarm.render()

        ui.timer(self.UPDATE_INTERVAL, self.update_all_components)
        self.update_all_components()

    def update_all_components(self):
        for clock in self.clocks:
            clock.update()
        self.stopwatch.update_display()
        self.timer.update_display()
        self.check_alarms()

    def set_24h(self, value: bool):
        self.format_24h = bool(value)
        for c in self.clocks:
            c.set_format(self.format_24h)
            c.update()

    def set_date_format(self, fmt: str):
        if fmt not in ('ISO', 'Locale'):
            return
        self.date_format = fmt
        for c in self.clocks:
            c.set_date_format(self.date_format)
            c.update()

    def check_alarms(self):
        if not self.alarm or not self.alarm.alarms:
            return
        now = datetime.now()
        key = now.strftime('%Y%m%d%H%M')
        for a in self.alarm.alarms:
            try:
                if not a.get('enabled'):
                    continue
                hr = int(a.get('hour', -1)); mn = int(a.get('minute', -1))
                if hr == now.hour and mn == now.minute and a.get('last_trigger') != key:
                    a['last_trigger'] = key
                    ui.notify(f"🔔 Alarm: {a.get('label','Alarm')} {hr:02d}:{mn:02d}", type='warning', position='top', timeout=5000)
                    play_beep()
                    self.alarm.save_alarms()
            except Exception as e:
                logging.error(f'Alarm check error: {e}')

    def run(self, host: str = '0.0.0.0', port: int = 9400, title: str = 'PY_CLOCKS', reload: bool = False):
        self.setup_ui()
        ui.run(host=host, port=port, title=title, window_size=(980, 800), frameless=False, reload=reload)


if __name__ in {"__main__", "__mp_main__"}:
    app = PyClocks()
    app.run(reload=True)
