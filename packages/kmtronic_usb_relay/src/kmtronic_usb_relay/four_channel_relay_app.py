"""KMTronic USB Relay - Web Interface with REST API"""
import os, socket, logging
from typing import Optional, Callable, Dict, List
from functools import wraps
from dataclasses import dataclass
from fastapi import HTTPException
from nicegui import ui, app
from kmtronic_usb_relay.four_channel_relay import RelayController
from kmtronic_usb_relay.com_utils import SerialComUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class UIConfig:
    PRIMARY: str = "#0ea5a4"
    SECONDARY: str = "#64748b"
    ACCENT: str = "#22c55e"
    CARD_WIDTH: str = "900px"
    POLL_INTERVAL: int = 0
    RELAY_SWITCH_DELAY: float = 0.01
    UI_REFRESH_DELAY: float = 0.01
    DARK_BG: str = "background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%)"
    DARK_PANEL: str = "background: rgba(30, 41, 59, 0.7)"
    DARK_BORDER: str = "1px solid rgba(255, 255, 255, 0.15)"
    DARK_TEXT: str = "text-white"
    LIGHT_BG: str = "background: linear-gradient(135deg, #e2e8f0 0%, #f8fafc 100%)"
    LIGHT_PANEL: str = "background: rgba(255, 255, 255, 0.9)"
    LIGHT_BORDER: str = "1px solid rgba(0, 0, 0, 0.12)"
    LIGHT_TEXT: str = "text-grey-9"
    BLUR: str = "backdrop-filter: blur(10px)"
    RELAY_ON_BG: str = "rgba(34, 197, 94, 0.15)"
    RELAY_OFF_BG: str = "rgba(239, 68, 68, 0.15)"
    RELAY_ON_BORDER: str = "rgba(34, 197, 94, 0.4)"
    RELAY_OFF_BORDER: str = "rgba(239, 68, 68, 0.4)"

CFG = UIConfig()

class RelayService:
    def __init__(self) -> None:
        self._controller: Optional[RelayController] = None
        self.current_port: Optional[str] = None

    @property
    def is_connected(self) -> bool:
        return bool(self._controller and self._controller.is_connected)

    def connect(self, com_port: str) -> None:
        if not com_port:
            raise ValueError("COM port is required")
        if self._controller:
            try:
                self._controller.close()
            except Exception as e:
                logger.warning(f"Error closing connection: {e}")
        self._controller = RelayController(com_port, switch_delay=CFG.RELAY_SWITCH_DELAY)
        if not self._controller.is_connected:
            raise RuntimeError(f"Failed to connect to {com_port}")
        self.current_port = com_port

    def disconnect(self) -> None:
        if self._controller:
            try:
                self._controller.close()
            finally:
                self._controller = None
                self.current_port = None

    def ensure(self) -> RelayController:
        if not self._controller or not self._controller.is_connected:
            raise HTTPException(status_code=503, detail="Relay controller not connected")
        return self._controller

    def statuses_int_keys(self) -> Dict[int, str]:
        raw = self.ensure().get_statuses()
        result: Dict[int, str] = {}
        for key, value in raw.items():
            try:
                relay_num = int(str(key).strip().lstrip('Rr'))
                result[relay_num] = value
            except (ValueError, AttributeError):
                continue
        return result

    def set(self, relay_number: int, on: bool) -> None:
        controller = self.ensure()
        (controller.turn_on if on else controller.turn_off)(relay_number)

    def bulk(self, on: bool) -> None:
        for relay_num in range(1, 5):
            self.set(relay_num, on)

    @staticmethod
    def available_ports() -> List[str]:
        return SerialComUtils.get_port_names() or []

service = RelayService()

def handle_rest_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"REST error in {func.__name__}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    return wrapper

@app.get("/health")
@handle_rest_error
def health_check() -> dict:
    return {"status": "ok", "connected": service.is_connected, "port": service.current_port}

@app.get("/relay/ports")
@handle_rest_error
def list_ports() -> dict:
    ports = RelayService.available_ports()
    return {"status": "success", "count": len(ports), "ports": ports}

@app.get("/relay/status")
@handle_rest_error
def get_status() -> dict:
    return {"status": "success", "relays": service.ensure().get_statuses()}

@app.post("/relay/{relay_number}/on")
@handle_rest_error
def turn_on(relay_number: int) -> dict:
    if not 1 <= relay_number <= 4:
        raise HTTPException(status_code=400, detail="Relay number must be between 1 and 4")
    service.set(relay_number, True)
    return {"status": "success", "relay": relay_number, "state": "ON"}

@app.post("/relay/{relay_number}/off")
@handle_rest_error
def turn_off(relay_number: int) -> dict:
    if not 1 <= relay_number <= 4:
        raise HTTPException(status_code=400, detail="Relay number must be between 1 and 4")
    service.set(relay_number, False)
    return {"status": "success", "relay": relay_number, "state": "OFF"}

class ThemeManager:
    def __init__(self) -> None:
        self.dark_mode_obj = None
        self.body_style = None
        self.header_toggle_row: Optional[ui.row] = None
        self.connection_card: Optional[ui.card] = None
        self.control_card: Optional[ui.card] = None
        self.status_card: Optional[ui.card] = None

    def init(self, start_dark: bool = False) -> None:
        ui.colors(primary=CFG.PRIMARY, secondary=CFG.SECONDARY, accent=CFG.ACCENT)
        self.dark_mode_obj = ui.dark_mode(start_dark)
        self.body_style = ui.query('body').style(CFG.DARK_BG if start_dark else CFG.LIGHT_BG)

    def register_cards(self, connection: ui.card, control: ui.card, status: ui.card, toggle_row: ui.row) -> None:
        self.connection_card = connection
        self.control_card = control
        self.status_card = status
        self.header_toggle_row = toggle_row

    @property
    def is_dark(self) -> bool:
        return bool(self.dark_mode_obj and self.dark_mode_obj.value)

    def text_class(self) -> str:
        return CFG.DARK_TEXT if self.is_dark else CFG.LIGHT_TEXT

    def apply_text_class(self, *elements) -> None:
        text_cls = self.text_class()
        for element in elements:
            if element:
                try:
                    element.classes(remove="text-white text-grey-9 text-grey-6 text-grey-4 text-grey-3")
                    element.classes(text_cls)
                except Exception:
                    pass

    def _panel_style(self, is_dark: bool, extra: str = "") -> str:
        bg = CFG.DARK_PANEL if is_dark else CFG.LIGHT_PANEL
        border = CFG.DARK_BORDER if is_dark else CFG.LIGHT_BORDER
        return f"{bg}; {CFG.BLUR}; border: {border}; padding: 16px; {extra}".strip()

    def _status_style(self, is_dark: bool) -> str:
        return self._panel_style(is_dark, f"border-left: 3px solid {CFG.PRIMARY}; padding: 8px 12px;")

    def apply(self, ui_controller=None) -> None:
        if not self.dark_mode_obj:
            return
        if self.body_style:
            self.body_style.style(CFG.DARK_BG if self.is_dark else CFG.LIGHT_BG)
        panel_style = self._panel_style(self.is_dark)
        if self.connection_card:
            self.connection_card.style(panel_style)
        if self.control_card:
            self.control_card.style(panel_style)
        if self.status_card:
            self.status_card.style(self._status_style(self.is_dark))
        if self.header_toggle_row:
            self.header_toggle_row.clear()
            with self.header_toggle_row:
                ui.button(icon="light_mode" if self.is_dark else "dark_mode",
                         on_click=self.toggle).props("flat dense round").classes("text-white")
        if ui_controller and hasattr(ui_controller, 'apply_theme_to_all_elements'):
            ui_controller.apply_theme_to_all_elements()

    def toggle(self, ui_controller=None) -> None:
        try:
            if not self.dark_mode_obj:
                ui.notify("Dark mode not initialized", type="warning")
                return
            self.dark_mode_obj.value = not self.dark_mode_obj.value
            self.apply(ui_controller)
        except Exception as e:
            logger.error(f"Theme toggle error: {e}")
            ui.notify("Theme toggle failed", type="warning")

class KMTronicUIController:
    def __init__(self, theme: ThemeManager) -> None:
        self.theme = theme
        self.com_port_input: Optional[ui.input] = None
        self.port_select: Optional[ui.select] = None
        self.status_output: Optional[ui.label] = None
        self.connection_status: Optional[ui.chip] = None
        self.header_status: Optional[ui.chip] = None
        self.relay_grid: Optional[ui.column] = None
        self.timer: Optional[ui.timer] = None
        self.header_toggle_row: Optional[ui.row] = None
        self.connection_card: Optional[ui.card] = None
        self.control_card: Optional[ui.card] = None
        self.status_card: Optional[ui.card] = None
        self.controls: List[ui.element] = []
        self.text_elements: List[ui.label] = []
        self.input_elements: List = []

    def apply_theme_to_all_elements(self) -> None:
        self.theme.apply_text_class(*self.text_elements)
        for element in self.input_elements:
            if element:
                self.theme.apply_text_class(element)

    def build(self) -> None:
        self._build_header()
        with ui.column().classes("w-full items-center").style("padding: 12px;"):
            with ui.column().style(f"width: {CFG.CARD_WIDTH}; max-width: 98vw;").classes("q-gutter-sm"):
                self._build_status_strip()
                self._build_connection_panel()
                self._build_control_panel()
        if self.connection_card and self.control_card and self.status_card and self.header_toggle_row:
            self.theme.register_cards(self.connection_card, self.control_card, self.status_card, self.header_toggle_row)
            self.theme.apply(self)

    def _update_status_chips(self, connected: bool, port: str = "") -> None:
        if self.connection_status:
            text, color, icon = (f"Connected: {port}", "positive", "check_circle") if connected else ("Disconnected", "grey", "power_off")
            self.connection_status.set_text(text)
            self.connection_status.props(f'color={color} icon={icon}')
        if self.header_status:
            text, color, icon = (port or "Connected", "positive", "lan") if connected else ("Disconnected", "grey", "power_off")
            self.header_status.set_text(text)
            self.header_status.props(f'color={color} icon={icon}')

    def _toggle_controls(self, enabled: bool) -> None:
        for control in self.controls:
            try:
                control.enable() if enabled else control.disable()
            except Exception:
                pass

    async def connect_relay(self) -> None:
        com_port = (self.com_port_input.value or "").strip() if self.com_port_input else ""
        if not com_port:
            ui.notify("Please enter a COM port", type="warning")
            return
        try:
            service.connect(com_port)
            self._update_status_chips(True, com_port)
            self._toggle_controls(True)
            if self.status_output:
                self.status_output.set_text(f"Connected to {com_port}")
            await self.refresh_status()
            if CFG.POLL_INTERVAL > 0 and not self.timer:
                self.timer = ui.timer(CFG.POLL_INTERVAL, self.refresh_status)
            ui.notify(f"✓ Connected to {com_port}", type="positive")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self._update_status_chips(False)
            self._toggle_controls(False)
            if self.status_output:
                self.status_output.set_text(f"Error: {str(e)}")
            ui.notify("Connection failed", type="negative")

    async def disconnect_relay(self) -> None:
        try:
            service.disconnect()
            self._update_status_chips(False)
            self._toggle_controls(False)
            if self.status_output:
                self.status_output.set_text("Disconnected")
            if self.timer:
                self.timer.cancel()
                self.timer = None
            ui.notify("Disconnected", type="info")
        except Exception as e:
            logger.error(f"Disconnect error: {e}")
            ui.notify("Disconnect failed", type="warning")

    async def control_relay(self, relay_num: int, state: str) -> None:
        try:
            service.set(relay_num, state.upper() == "ON")
            ui.notify(f"✓ R{relay_num} {state.upper()}", type="positive")
            ui.timer(CFG.UI_REFRESH_DELAY, self.refresh_status, once=True)
        except HTTPException as he:
            ui.notify(he.detail, type="negative")
        except Exception as e:
            logger.error(f"Control relay error: {e}")
            if self.status_output:
                self.status_output.set_text(f"Error: {str(e)}")
            ui.notify("Operation failed", type="negative")

    async def bulk_set(self, state: str) -> None:
        try:
            service.bulk(state.upper() == "ON")
            ui.notify(f"All {state.upper()}", type="positive")
            ui.timer(CFG.UI_REFRESH_DELAY, self.refresh_status, once=True)
        except Exception as e:
            logger.error(f"Bulk operation error: {e}")
            ui.notify("Bulk operation failed", type="negative")

    async def refresh_status(self) -> None:
        try:
            statuses = service.statuses_int_keys()
            if self.status_output:
                self.status_output.set_text(" | ".join([f"R{n}: {s}" for n, s in sorted(statuses.items())]))
            if self.relay_grid:
                self.relay_grid.clear()
                with self.relay_grid:
                    self._build_relay_buttons(statuses)
        except HTTPException as he:
            ui.notify(he.detail, type="warning")
        except Exception as e:
            logger.error(f"Status refresh error: {e}")
            if self.status_output:
                self.status_output.set_text(f"Error: {str(e)}")
            ui.notify("Failed to get status", type="warning")

    async def scan_ports(self) -> None:
        try:
            ports = RelayService.available_ports()
            if self.port_select:
                self.port_select.options = ports
                self.port_select.value = ports[0] if ports else None
                self.port_select.update()
            ui.notify(f"Found {len(ports)} port{'s' if len(ports) != 1 else ''}", type="positive")
        except Exception as e:
            logger.error(f"Port scan error: {e}")
            ui.notify("Scan failed", type="negative")

    def _build_header(self) -> None:
        style = f"background: linear-gradient(90deg, {CFG.PRIMARY}, {CFG.ACCENT}); padding: 8px 16px;"
        with ui.header(elevated=True).style(style):
            with ui.row().classes("w-full items-center").style("max-width: 1400px; margin: 0 auto;"):
                ui.icon("settings_input_component", size="sm").classes("text-white")
                ui.label("KMTronic Relay").classes("text-white text-subtitle1 text-weight-bold")
                ui.space()
                ui.button(icon="api", on_click=self.open_api_dialog).props("flat dense round").classes("text-white").tooltip("API Endpoints")
                self.header_toggle_row = ui.row().style("margin-left: 8px; margin-right: 12px;")
                with self.header_toggle_row:
                    ui.button(icon="light_mode" if self.theme.is_dark else "dark_mode",
                             on_click=lambda: self.theme.toggle(self)).props("flat dense round").classes("text-white").tooltip("Toggle Theme")
                self.header_status = ui.chip("Disconnected", icon="power_off").props("dense square color=grey")

    def _build_status_strip(self) -> None:
        strip_style = self.theme._status_style(self.theme.is_dark)
        self.status_card = ui.card().classes("w-full").style(strip_style)
        with self.status_card:
            with ui.row().classes("w-full items-center"):
                ui.icon("radio_button_checked", size="xs").classes("text-positive")
                self.status_output = ui.label("Ready").classes(f"text-caption {self.theme.text_class()}").style("margin-left: 8px;")
                self.text_elements.append(self.status_output)

    def _build_connection_panel(self) -> None:
        panel_style = self.theme._panel_style(self.theme.is_dark, extra="padding: 12px 16px;")
        self.connection_card = ui.card().classes("w-full").style(panel_style)
        with self.connection_card:
            with ui.row().classes("w-full items-center").style("gap: 12px;"):
                with ui.column().style("flex: 1; min-width: 0;"):
                    self.com_port_input = ui.input(placeholder="COM4").props("outlined dense").classes(f"w-full {self.theme.text_class()}").style("margin: 0;")
                    self.input_elements.append(self.com_port_input)
                with ui.column().style("flex: 1; min-width: 0;"):
                    self.port_select = ui.select([], label="Quick Select").props("outlined dense").classes(f"w-full {self.theme.text_class()}").style("margin: 0;")
                    self.input_elements.append(self.port_select)
                scan_btn = ui.button(icon="search", on_click=self.scan_ports).props("flat dense")
                connect_btn = ui.button("CONNECT", icon="link", color="positive", on_click=self._on_connect_click).props("dense unelevated")
                disconnect_btn = ui.button("DISCONNECT", icon="link_off", color="negative", on_click=self.disconnect_relay).props("dense outline")
                self.connection_status = ui.chip("OFF", icon="power_off").props("dense square color=grey").style("margin: 0;")
                self.controls.extend([disconnect_btn, scan_btn])

    def _on_connect_click(self) -> None:
        async def do_connect():
            if self.port_select and self.port_select.value and self.com_port_input:
                self.com_port_input.set_value(self.port_select.value)
            await self.connect_relay()
        return do_connect()

    def _build_control_panel(self) -> None:
        panel_style = self.theme._panel_style(self.theme.is_dark, extra="padding: 16px 20px;")
        self.control_card = ui.card().classes("w-full").style(panel_style)
        with self.control_card:
            with ui.row().classes("w-full items-center").style("margin-bottom: 16px;"):
                ui.icon("settings_input_component", size="sm").classes("text-primary")
                title = ui.label("Relay Control").classes(f"text-h6 text-weight-medium {self.theme.text_class()}").style("margin-left: 8px;")
                self.text_elements.append(title)
                ui.space()
                with ui.row().classes("q-gutter-sm"):
                    all_on = ui.button("All ON", icon="flash_on", color="positive", on_click=lambda: self.bulk_set("ON")).props("unelevated")
                    all_off = ui.button("All OFF", icon="flash_off", color="negative", on_click=lambda: self.bulk_set("OFF")).props("outline")
                    self.controls.extend([all_on, all_off])
            self.relay_grid = ui.column().classes("w-full")

    def _build_relay_buttons(self, statuses: Dict[int, str]) -> None:
        with ui.grid(columns=4).classes("w-full").style("gap: 12px;"):
            for relay_num in range(1, 5):
                self._build_single_relay_card(relay_num, statuses)

    def _build_single_relay_card(self, relay_num: int, statuses: Dict[int, str]) -> None:
        is_on = statuses.get(relay_num, "OFF").upper() == "ON"
        bg = CFG.RELAY_ON_BG if is_on else CFG.RELAY_OFF_BG
        border = CFG.RELAY_ON_BORDER if is_on else CFG.RELAY_OFF_BORDER
        color = "positive" if is_on else "negative"
        text = "ON" if is_on else "OFF"
        icon = "power" if is_on else "power_off"
        card_style = f"padding: 16px; background: {bg}; border: 2px solid {border}; border-radius: 12px; transition: all 0.3s ease;"
        with ui.card().classes("w-full").style(card_style):
            with ui.column().classes("w-full items-center").style("gap: 8px;"):
                relay_label = ui.label(f"Relay {relay_num}").classes(f"text-subtitle2 text-weight-bold text-center {self.theme.text_class()}")
                self.text_elements.append(relay_label)
                ui.chip(text, icon=icon).props(f"color={color} size=sm")
                btn = ui.button("Toggle", icon="power_settings_new", color="primary",
                               on_click=lambda num=relay_num, current=is_on: self.control_relay(num, "OFF" if current else "ON")
                               ).props("unelevated size=md").classes("w-full").style("font-size: 0.9rem;")
                self.controls.append(btn)

    def open_api_dialog(self) -> None:
        try:
            panel_style = self.theme._panel_style(self.theme.is_dark, extra="padding: 16px;")
            text_class = self.theme.text_class()
            endpoints = [{"method": "GET", "path": "/health", "desc": "Service health"},
                        {"method": "GET", "path": "/relay/ports", "desc": "Available COM ports"},
                        {"method": "GET", "path": "/relay/status", "desc": "Relay status"}]
            for n in range(1, 5):
                endpoints.append({"method": "POST", "path": f"/relay/{n}/on", "desc": f"Turn R{n} ON"})
                endpoints.append({"method": "POST", "path": f"/relay/{n}/off", "desc": f"Turn R{n} OFF"})
            with ui.dialog() as dialog:
                with ui.card().style(panel_style).classes("w-full"):
                    ui.label("API Endpoints").classes(f"text-h6 text-weight-medium {text_class}")
                    with ui.column().classes("w-full").style("gap: 6px;"):
                        for ep in endpoints:
                            with ui.row().classes("items-center w-full").style("gap: 8px;"):
                                method_color = "primary" if ep["method"] == "GET" else "orange"
                                ui.chip(ep["method"]).props(f"color={method_color} size=sm")
                                ui.label(ep["path"]).classes(f"text-body2 text-weight-medium {text_class}")
                                ui.space()
                                ui.label(ep["desc"]).classes(f"text-caption {text_class}").style("opacity: 0.7;")
                    with ui.row().classes("w-full justify-end").style("margin-top: 12px;"):
                        ui.button("Close", icon="close", on_click=dialog.close).props("flat")
            dialog.open()
        except Exception as e:
            logger.error(f"Failed to open API endpoints dialog: {e}")
            ui.notify("Failed to show API endpoints", type="warning")


@ui.page("/")
def index_page() -> None:
    theme = ThemeManager()
    theme.init(start_dark=False)
    KMTronicUIController(theme).build()

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="KMTronic USB Relay - Web Interface")
    parser.add_argument("com_port", nargs="?", default=None, help="COM port to auto-connect")
    parser.add_argument("--host", default='0.0.0.0', help="Server host")
    parser.add_argument("--port", type=int, default=9401, help="Server port")
    parser.add_argument("--native", action="store_true", help="Launch in native window")
    args = parser.parse_args()
    com_port = args.com_port or os.getenv("KMTRONIC_COM_PORT")
    if com_port:
        try:
            service.connect(com_port)
            logger.info(f"Auto-connected to {com_port}")
        except Exception as e:
            logger.warning(f"Failed to auto-connect to {com_port}: {e}")
    logger.info(f"Starting server on {args.host}:{args.port}")
    ui.run(host=args.host, port=args.port, native=args.native)


if __name__ in {"__main__", "__mp_main__"}:
    main()
