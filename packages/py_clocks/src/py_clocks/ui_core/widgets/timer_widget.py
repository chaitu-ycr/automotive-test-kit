from datetime import datetime
from typing import Optional
from nicegui import ui
from ..utils import play_beep


class Timer:
    def __init__(self):
        self.running = False
        self.remaining_time = 0.0
        self.total_time = 0.0
        self.start_time: Optional[datetime] = None
        self.time_label: Optional[ui.label] = None
        self.progress: Optional[ui.circular_progress] = None
        self.start_btn: Optional[ui.button] = None
        self.reset_btn: Optional[ui.button] = None
        self.hours_input: Optional[ui.number] = None
        self.minutes_input: Optional[ui.number] = None
        self.seconds_input: Optional[ui.number] = None

    def render(self):
        with ui.card().classes('w-full').style('background: transparent; border: none; padding: 0; height: 100%; display: flex; flex-direction: column;'):
            with ui.row().classes('w-full gap-2 mb-1 items-center'):
                with ui.column().classes('items-stretch').style('flex: 1; min-width: 0;'):
                    ui.label('HOUR').classes('text-xs font-bold').style('color: #00ffff; font-family: "Courier New", monospace; margin-bottom: 0;')
                    self.hours_input = ui.number(value=0, min=0, max=23).props('outlined dense dark').classes('w-full').style('color: #00ffff;')
                with ui.column().classes('items-stretch').style('flex: 1; min-width: 0;'):
                    ui.label('MIN').classes('text-xs font-bold').style('color: #00ffff; font-family: "Courier New", monospace; margin-bottom: 0;')
                    self.minutes_input = ui.number(value=0, min=0, max=59).props('outlined dense dark').classes('w-full').style('color: #00ffff;')
                with ui.column().classes('items-stretch').style('flex: 1; min-width: 0;'):
                    ui.label('SEC').classes('text-xs font-bold').style('color: #00ffff; font-family: "Courier New", monospace; margin-bottom: 0;')
                    self.seconds_input = ui.number(value=0, min=0, max=59).props('outlined dense dark').classes('w-full').style('color: #00ffff;')

            self.progress = ui.circular_progress(value=0, size='40px', color='cyan', show_value=False).classes('mx-auto').style('margin-top: 2px; margin-bottom: 2px;')
            self.time_label = ui.label('00:00:00').classes('font-bold text-center').style('color: #00ffff; font-family: "Courier New", monospace; font-size: 0.85rem; text-shadow: 0 0 8px rgba(0,255,255,0.6); margin-bottom: 1px;')

            with ui.row().classes('w-full gap-2 items-center'):
                self.start_btn = ui.button('START', on_click=self.toggle_start).props('flat id=timer-start').classes('w-full px-4 py-1 text-sm font-bold').style('background: #00ffff; color: #000000; border: 2px solid #00cccc; border-radius: 0px; font-family: "Courier New", monospace; flex: 1;')
                self.reset_btn = ui.button('RESET', on_click=self.reset).props('flat').classes('w-full px-4 py-1 text-sm font-bold').style('background: #666666; color: #000000; border: 2px solid #444444; border-radius: 0px; font-family: "Courier New", monospace; flex: 1;')

    def toggle_start(self):
        if not self.running:
            if self.remaining_time == 0.0:
                hours = float(self.hours_input.value or 0)
                minutes = float(self.minutes_input.value or 0)
                seconds = float(self.seconds_input.value or 0)
                self.total_time = hours * 3600 + minutes * 60 + seconds
                self.remaining_time = self.total_time
                if self.total_time == 0:
                    ui.notify('⚠️ Please set a time!', type='warning', position='top')
                    return
            self.running = True
            self.start_time = datetime.now()
            self.start_btn.text = 'PAUSE'
            self.start_btn.style('background: #ffaa00; color: #000000; border: 2px solid #cc8800; border-radius: 0px;')
            self.hours_input.disable(); self.minutes_input.disable(); self.seconds_input.disable()
        else:
            self.running = False
            if self.start_time:
                elapsed = (datetime.now() - self.start_time).total_seconds()
                self.remaining_time = max(0, self.remaining_time - elapsed)
            self.start_btn.text = 'RESUME'
            self.start_btn.style('background: #00ffff; color: #000000; border: 2px solid #00cccc; border-radius: 0px;')

    def reset(self):
        self.running = False
        self.remaining_time = 0.0
        self.total_time = 0.0
        self.start_time = None
        self.update_display()
        self.start_btn.text = 'START'
        self.start_btn.style('background: #00ffff; color: #000000; border: 2px solid #00cccc; border-radius: 0px;')
        self.hours_input.enable(); self.minutes_input.enable(); self.seconds_input.enable()
        self.hours_input.value = 0; self.minutes_input.value = 0; self.seconds_input.value = 0
        if self.progress: self.progress.value = 0

    def get_remaining_time(self) -> float:
        if self.running and self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            remaining = max(0, self.remaining_time - elapsed)
            if remaining == 0 and self.remaining_time > 0:
                self.on_timer_complete()
            return remaining
        return self.remaining_time

    def on_timer_complete(self):
        self.running = False
        self.remaining_time = 0.0
        ui.notify('⏰ Timer Complete!', type='positive', position='top', timeout=5000)
        play_beep()
        self.start_btn.text = 'START'
        self.start_btn.style('background: #00ffff; color: #000000; border: 2px solid #00cccc; border-radius: 0px;')
        self.hours_input.enable(); self.minutes_input.enable(); self.seconds_input.enable()

    def format_time(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def update_display(self):
        if not self.time_label or not self.progress:
            return
        remaining = self.get_remaining_time()
        self.time_label.text = self.format_time(remaining)
        self.progress.value = (self.total_time - remaining) / self.total_time if self.total_time > 0 else 0
