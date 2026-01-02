from typing import Optional
from datetime import datetime
import pytz
import logging
from nicegui import ui


class ClockWidget:
    def __init__(self, timezone: str, label_text: str, bg_color: str, text_color: str):
        self.timezone = timezone
        self.label_text = label_text
        self.bg_color = bg_color
        self.text_color = text_color
        self.time_label: Optional[ui.label] = None
        self.date_label: Optional[ui.label] = None
        self.format_24h: bool = False
        self.date_format: str = 'ISO'

    def set_format(self, use_24h: bool):
        self.format_24h = use_24h

    def set_date_format(self, date_format: str):
        self.date_format = date_format

    def render(self):
        with ui.card().classes('w-full').style(
            f'background: {self.bg_color}; border-radius: 0px; padding: 1px; '
            f'border: 1px solid {self.text_color}; margin: 0;'
        ):
            ui.label(self.label_text).classes('text-xs font-bold text-center').style(
                f'color: {self.text_color}; margin-bottom: 0; font-family: "Courier New", monospace; font-size: 0.6rem; line-height: 1;'
            )
            self.time_label = ui.label('--:--:-- --').classes('text-center font-bold').style(
                f'color: {self.text_color}; font-family: "Courier New", monospace; font-size: 0.8rem; line-height: 1;'
            )
            self.date_label = ui.label('Loading...').classes('text-center').style(
                f'color: {self.text_color}; opacity: 0.9; margin-top: 0; font-family: "Courier New", monospace; font-size: 0.6rem; line-height: 1;'
            )

    def update(self):
        if not self.time_label or not self.date_label:
            return
        try:
            tz = pytz.timezone(self.timezone)
            now = datetime.now(tz)
            current_time = now.strftime("%H:%M:%S") if self.format_24h else now.strftime("%I:%M:%S %p")
            iso_week = f"CW {now.isocalendar()[1]}"
            self.time_label.text = f"{current_time} ({iso_week})"
            if self.date_format == 'Locale':
                date_str = now.strftime("%A, %x")
            else:
                date_str = now.strftime("%A, %Y-%m-%d")
            self.date_label.text = date_str
        except pytz.UnknownTimeZoneError:
            self.time_label.text = "Invalid Timezone"
            self.date_label.text = ""
            logging.error(f"Unknown timezone: {self.timezone} for {self.label_text}.")
        except Exception as e:
            self.time_label.text = "Error"
            self.date_label.text = ""
            logging.error(f"Error updating clock for {self.label_text}: {e}")
