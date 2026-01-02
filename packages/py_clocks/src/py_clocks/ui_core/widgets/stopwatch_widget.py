from datetime import datetime
from typing import List, Optional
from nicegui import ui


class Stopwatch:
    def __init__(self):
        self.running = False
        self.elapsed_time = 0.0
        self.start_time: Optional[datetime] = None
        self.laps: List[float] = []
        self.time_label: Optional[ui.label] = None
        self.lap_container: Optional[ui.column] = None
        self.start_btn: Optional[ui.button] = None
        self.lap_reset_btn: Optional[ui.button] = None

    def render(self):
        with ui.card().classes('w-full').style('background: transparent; border: none; padding: 0; height: 100%; display: flex; flex-direction: column;'):
            self.time_label = ui.label('00:00:00.00').classes('font-bold text-center').style('color: #00ff00; font-family: "Courier New", monospace; font-size: 0.9rem; text-shadow: 0 0 8px rgba(0,255,0,0.6); margin-bottom: 0px;')
            with ui.row().classes('w-full gap-2 mb-1 items-center'):
                self.start_btn = ui.button('START', on_click=self.toggle_start).props('flat id=stopwatch-start').classes('w-full px-4 py-1 text-sm font-bold').style('background: #00ff00; color: #000000; border: 2px solid #00cc00; border-radius: 0px; font-family: "Courier New", monospace; flex: 1;')
                self.lap_reset_btn = ui.button('LAP', on_click=self.lap_reset).props('flat disabled id=stopwatch-lap').classes('w-full px-4 py-1 text-sm font-bold').style('background: #666666; color: #000000; border: 2px solid #444444; border-radius: 0px; font-family: "Courier New", monospace; flex: 1;')
            ui.label('LAPS').classes('text-xs font-bold text-center').style('color: #00ff00; font-family: "Courier New", monospace; margin-bottom: 0;')
            with ui.scroll_area().classes('w-full').style('flex: 1; min-height: 0; background-color: #000a00; border-radius: 0px; padding: 2px; border: 2px solid #00cc00;'):
                self.lap_container = ui.column().classes('w-full gap-1')

    def toggle_start(self):
        if not self.running:
            self.running = True
            self.start_time = datetime.now()
            self.start_btn.text = 'STOP'
            self.start_btn.style('background: #ff0000; color: #000000; border: 2px solid #cc0000; border-radius: 0px;')
            self.lap_reset_btn.props(remove='disabled')
            self.lap_reset_btn.style('background: #0000ff; color: #ffffff; border: 2px solid #0000cc; border-radius: 0px;')
            self.lap_reset_btn.text = 'LAP'
        else:
            self.running = False
            if self.start_time:
                self.elapsed_time += (datetime.now() - self.start_time).total_seconds()
            self.start_btn.text = 'START'
            self.start_btn.style('background: #00ff00; color: #000000; border: 2px solid #00cc00; border-radius: 0px;')
            self.lap_reset_btn.text = 'RESET'
            self.lap_reset_btn.style('background: #ffaa00; color: #000000; border: 2px solid #cc8800; border-radius: 0px;')

    def lap_reset(self):
        if self.running:
            current_time = self.get_current_time()
            self.laps.append(current_time)
            lap_number = len(self.laps)
            lap_time_str = self.format_time(current_time)
            with self.lap_container:
                with ui.row().classes('w-full justify-between items-center').style('background: #003300; border-radius: 0px; padding: 2px; border: 2px solid #00ff00;'):
                    ui.label(f'LAP {lap_number}').classes('font-bold').style('color: #00ff00; font-family: "Courier New", monospace; font-size: 0.75rem;')
                    ui.label(lap_time_str).classes('font-semibold').style('color: #00ff00; font-family: "Courier New", monospace; font-size: 0.75rem;')
        else:
            self.elapsed_time = 0.0
            self.laps.clear()
            self.lap_container.clear()
            self.update_display()
            self.lap_reset_btn.props('disabled')
            self.lap_reset_btn.style('background: #666666; color: #000000; border: 2px solid #444444; border-radius: 0px;')

    def get_current_time(self) -> float:
        if self.running and self.start_time:
            return self.elapsed_time + (datetime.now() - self.start_time).total_seconds()
        return self.elapsed_time

    def format_time(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 100)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:02d}"

    def update_display(self):
        if not self.time_label:
            return
        current_time = self.get_current_time()
        self.time_label.text = self.format_time(current_time)
