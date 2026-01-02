"""HID USB Relay Controller - Professional Web Interface"""
import socket, logging, re
from typing import Optional, List
from functools import wraps
from dataclasses import dataclass
from argparse import ArgumentParser
from fastapi import HTTPException
from nicegui import ui, app
from hid_usb_relay.usb_relay import (
    set_relay_device_state, set_relay_device_relay_state,
    get_relay_device_state, get_relay_device_relay_state,
    set_default_relay_device_state, set_default_relay_device_relay_state,
    get_default_relay_device_state, get_default_relay_device_relay_state,
    enumerate_devices
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# UI Configuration - colors, gradients, and styling constants
@dataclass(frozen=True)
class CFG:
    # Brand colors
    PRIMARY: str = "#0ea5a4"
    SECONDARY: str = "#64748b"
    ACCENT: str = "#22c55e"
    CARD_WIDTH: str = "1400px"

    # Dark theme styles
    DARK_BG: str = "background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%)"
    DARK_PANEL: str = "background: rgba(30, 41, 59, 0.7)"
    DARK_BORDER: str = "1px solid rgba(255, 255, 255, 0.15)"

    # Light theme styles
    LIGHT_BG: str = "background: linear-gradient(135deg, #e2e8f0 0%, #f8fafc 100%)"
    LIGHT_PANEL: str = "background: rgba(255, 255, 255, 0.9)"
    LIGHT_BORDER: str = "1px solid rgba(0, 0, 0, 0.12)"

    BLUR: str = "backdrop-filter: blur(10px)"

cfg = CFG()

# Hardware abstraction layer for relay operations
class RelayService:
    """Service layer that encapsulates relay hardware operations"""

    @staticmethod
    def set_and_get_relay_state(relay_id: Optional[str], relay_number: str, state: str) -> str:
        """Set relay state and return the updated state"""
        state_upper = state.upper()
        is_all = relay_number.lower() == "all"

        # Set the relay state (specific device or default)
        if relay_id:
            ok = set_relay_device_state(relay_id, state_upper) if is_all else set_relay_device_relay_state(relay_id, relay_number, state_upper)
        else:
            ok = set_default_relay_device_state(state_upper) if is_all else set_default_relay_device_relay_state(relay_number, state_upper)

        if not ok:
            raise HTTPException(status_code=400, detail="Failed to set relay state")

        # Get and return the updated state
        if relay_id:
            return get_relay_device_state(relay_id) if is_all else get_relay_device_relay_state(relay_id, relay_number)
        return get_default_relay_device_state() if is_all else get_default_relay_device_relay_state(relay_number)

    @staticmethod
    def get_devices() -> List[dict]:
        """Enumerate all connected relay devices"""
        return enumerate_devices() or []

service = RelayService()

# REST API error handling decorator
def handle_rest_error(func):
    """Decorator to handle REST API errors consistently"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"REST error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    return wrapper

# REST API Endpoints
@app.get("/health")
@handle_rest_error
def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "ok", "device_count": len(service.get_devices())}

@app.get("/relay/{relay_id}/{relay_number}/{relay_state}")
@handle_rest_error
def relay_control_by_id(relay_id: str, relay_number: str, relay_state: str) -> dict:
    """Control specific relay on specific device"""
    return {"status": "success", "relay_state": service.set_and_get_relay_state(relay_id, relay_number, relay_state)}

@app.get("/relay/{relay_number}/{relay_state}")
@handle_rest_error
def default_relay_control(relay_number: str, relay_state: str) -> dict:
    """Control relay on default device"""
    return {"status": "success", "relay_state": service.set_and_get_relay_state(None, relay_number, relay_state)}

@app.get("/relay/devices")
@handle_rest_error
def list_relay_devices() -> dict:
    """List all connected relay devices"""
    devices = service.get_devices()
    return {"status": "success", "count": len(devices), "devices": devices}

# Theme management for dark/light mode switching
class ThemeManager:
    """Manages dark/light theme switching and applies styling to UI elements"""

    def __init__(self):
        self.dark_mode_obj = None
        self.body_style = None
        self.header_toggle_row = None
        self.status_card = None
        self.control_card = None
        self.device_card = None
        self.device_separator = None

    def init(self, start_dark: bool = False):
        """Initialize theme system with brand colors"""
        ui.colors(primary=cfg.PRIMARY, secondary=cfg.SECONDARY, accent=cfg.ACCENT)
        self.dark_mode_obj = ui.dark_mode(start_dark)
        self.body_style = ui.query('body').style(cfg.DARK_BG if start_dark else cfg.LIGHT_BG)

    def register_cards(self, status, control, device, toggle_row, separator=None):
        """Register UI cards for theme application"""
        self.status_card = status
        self.control_card = control
        self.device_card = device
        self.header_toggle_row = toggle_row
        self.device_separator = separator

    @property
    def is_dark(self) -> bool:
        """Check if dark mode is currently enabled"""
        return bool(self.dark_mode_obj and self.dark_mode_obj.value)

    def text_class(self) -> str:
        """Get appropriate text color class for current theme"""
        return "text-white" if self.is_dark else "text-grey-9"

    def _panel_style(self, extra: str = "") -> str:
        """Generate panel style based on current theme"""
        border = cfg.DARK_BORDER if self.is_dark else cfg.LIGHT_BORDER
        bg = cfg.DARK_PANEL if self.is_dark else cfg.LIGHT_PANEL
        return f"{bg}; {cfg.BLUR}; border: {border}; padding: 16px; {extra}".strip()

    def apply(self, ui_controller=None):
        """Apply current theme to all registered UI elements"""
        if not self.dark_mode_obj:
            return

        # Update background gradient
        self.body_style.style(cfg.DARK_BG if self.is_dark else cfg.LIGHT_BG)
        panel_style = self._panel_style()

        # Apply theme to cards
        if self.control_card:
            self.control_card.style(panel_style)
        if self.device_card:
            self.device_card.style(panel_style)
        if self.status_card:
            self.status_card.style(self._panel_style(f"border-left: 3px solid {cfg.PRIMARY}; padding: 8px 12px;"))

        # Update theme toggle button
        if self.header_toggle_row:
            self.header_toggle_row.clear()
            with self.header_toggle_row:
                ui.button(icon="light_mode" if self.is_dark else "dark_mode", on_click=self.toggle).props("flat dense round").classes("text-white")

        # Update separator styling
        if self.device_separator:
            self.device_separator.style(f"background: {'rgba(255,255,255,0.15)' if self.is_dark else 'rgba(0,0,0,0.12)'}; margin: 8px 0;")

        # Update text colors on all tracked elements
        if ui_controller:
            for el in ui_controller.text_elements + ui_controller.input_elements:
                if el:
                    el.classes(remove="text-white text-grey-9 text-primary")
                    el.classes(self.text_class())

    def toggle(self, ui_controller=None):
        """Toggle between dark and light mode"""
        try:
            if not self.dark_mode_obj:
                ui.notify("Dark mode not initialized", type="warning")
                return
            self.dark_mode_obj.value = not self.dark_mode_obj.value
            self.apply(ui_controller)
        except Exception as e:
            logger.error(f"Theme toggle error: {e}")

# Main UI controller for relay operations
class RelayController:
    """Manages the web UI for relay control and device management"""

    def __init__(self, theme: ThemeManager):
        self.theme = theme

        # Track UI elements for theme updates
        self.text_elements = []
        self.input_elements = []

        # UI component references
        self.relay_id_input = None
        self.relay_num_input = None
        self.status_label = None
        self.status_output = None
        self.devices_count = None
        self.devices_select = None
        self.devices_container = None
        self.header_toggle_row = None
        self.status_card = None
        self.control_card = None
        self.device_card = None

    async def control_relay(self, state: str):
        """Control relay state (ON/OFF) for specified device and relay number"""
        try:
            relay_id = self.relay_id_input.value.strip() or None
            relay_num = self.relay_num_input.value.strip()
            result = service.set_and_get_relay_state(relay_id, relay_num, state)
            device_label = relay_id or "Default"

            # Update status display
            self.status_label.set_text(f"{device_label} • Relay {relay_num.upper()} • {state.upper()}")
            self.status_output.set_text(str(result))
            ui.notify(f"✓ Relay {state.upper()}", type="positive")
        except Exception as e:
            logger.error(e)
            self.status_label.set_text("Error")
            self.status_output.set_text(str(e))
            ui.notify("Operation failed", type="negative")

    async def refresh_status(self):
        """Refresh and display current relay status"""
        try:
            relay_id = self.relay_id_input.value.strip() or None
            relay_num = self.relay_num_input.value.strip()
            is_all = relay_num.lower() == "all"

            # Get current status
            if relay_id:
                result = get_relay_device_state(relay_id) if is_all else get_relay_device_relay_state(relay_id, relay_num)
            else:
                result = get_default_relay_device_state() if is_all else get_default_relay_device_relay_state(relay_num)

            # Update display
            self.status_label.set_text(f"{relay_id or 'Default'} • Current Status")
            self.status_output.set_text(str(result))
            ui.notify("Status refreshed", type="info")
        except Exception as e:
            logger.error(e)
            self.status_label.set_text("Error")
            self.status_output.set_text(str(e))
    async def scan_devices(self):
        """Scan for connected devices and update the device manager UI"""
        try:
            # Get devices and update count
            devices = service.get_devices()
            count = len(devices)
            self.devices_count.set_text(f"{count} device{'s' if count != 1 else ''}")

            # Update device selector dropdown
            device_ids = [d.get("device_id") for d in devices if d.get("device_id")]
            self.devices_select.options = device_ids
            self.devices_select.value = device_ids[0] if device_ids else None
            self.devices_select.update()

            # Rebuild device cards
            self.devices_container.clear()
            with self.devices_container:
                if not devices:
                    # Show "no devices" message
                    with ui.card().classes("w-full").style(f"{self.theme._panel_style('padding: 24px; text-align: center;')}"):
                        ui.icon("error_outline", size="lg").classes("text-grey-5")
                        no_dev_lbl = ui.label("No devices detected").classes(f"text-subtitle2 {self.theme.text_class()}").style("opacity: 0.7;")
                        self.text_elements.append(no_dev_lbl)
                else:
                    # Create card for each device
                    for device in devices:
                        device_id = device.get("device_id", "Unknown")
                        relay_states = {k: v for k, v in device.items() if re.match(r"R\d+$", k, re.IGNORECASE)}
                        with ui.card().classes("w-full").style(f"{self.theme._panel_style(f'padding: 10px; border-left: 3px solid {cfg.PRIMARY};')}"):
                            # Device header with ID and bulk controls
                            with ui.row().classes("w-full items-center").style("margin-bottom: 6px;"):
                                dev_icon = ui.icon("developer_board", size="xs").classes(f"{self.theme.text_class() if self.theme.is_dark else 'text-primary'}")
                                lbl = ui.label(device_id).classes(f"text-body2 text-weight-medium {self.theme.text_class()}").style("margin-left: 6px;")
                                self.text_elements.extend([dev_icon, lbl])
                                ui.space()

                                # Bulk ON/OFF controls for all relays
                                async def bulk_control(state: str, dev=device_id):
                                    try:
                                        set_relay_device_state(dev, state)
                                        ui.notify(f"{dev}: All {state}", type="positive")
                                    except Exception as e:
                                        logger.error(e)
                                        ui.notify("Operation failed", type="negative")
                                        return

                                    # Rescan devices after bulk operation (context-safe)
                                    try:
                                        await self.scan_devices()
                                    except RuntimeError as e:
                                        if "parent element" not in str(e) and "deleted" not in str(e):
                                            logger.error(f"Scan error: {e}")
                                    except Exception as e:
                                        logger.error(f"Scan error: {e}")

                                ui.button("ON", icon="flash_on", color="positive", on_click=lambda d=device_id: bulk_control("ON", d)).props("dense outline size=xs")
                                ui.button("OFF", icon="flash_off", color="negative", on_click=lambda d=device_id: bulk_control("OFF", d)).props("dense outline size=xs")
                            if relay_states:
                                with ui.grid(columns="repeat(auto-fit, minmax(65px, 1fr))").classes("w-full").style("gap: 4px;"):
                                    for relay_name, state in sorted(relay_states.items(), key=lambda x: int(re.search(r"\d+", x[0]).group())):
                                        relay_num = re.search(r"\d+", relay_name).group()
                                        is_on = state.upper() == "ON"

                                        async def toggle(dev_id=device_id, num=relay_num, current=is_on):
                                            try:
                                                new_state = "OFF" if current else "ON"
                                                set_relay_device_relay_state(dev_id, num, new_state)
                                                ui.notify(f"R{num}: {new_state}", type="positive")
                                            except Exception as e:
                                                logger.error(e)
                                                ui.notify("Failed", type="negative")
                                                return

                                            # Rescan devices after toggle (context-safe)
                                            try:
                                                await self.scan_devices()
                                            except RuntimeError as e:
                                                if "parent element" not in str(e) and "deleted" not in str(e):
                                                    logger.error(f"Scan error: {e}")
                                            except Exception as e:
                                                logger.error(f"Scan error: {e}")

                                        color = "positive" if is_on else "grey-6"
                                        icon = "check_circle" if is_on else "circle"
                                        ui.button(f"R{relay_num}", icon=icon, color=color, on_click=toggle).props("push size=sm").style("width: 100%; font-weight: 500; font-size: 0.7rem;")
            try: ui.notify(f"Found {count} device{'s' if count != 1 else ''}", type="positive")
            except RuntimeError: pass
        except Exception as e: logger.error(f"Scan failed: {e}"); raise
    def build(self):
        """Build the complete UI with header, status bar, control panel, and device manager"""
        # Application header with branding and controls
        with ui.header(elevated=True).style(f"background: linear-gradient(90deg, {cfg.PRIMARY}, {cfg.ACCENT}); padding: 8px 16px;"):
            with ui.row().classes("w-full items-center").style("max-width: 1400px; margin: 0 auto;"): ui.icon("electric_bolt", size="sm").classes("text-white"); ui.label("HID USB Relay Controller").classes("text-white text-subtitle1 text-weight-bold"); ui.space(); ui.button(icon="api", on_click=lambda: self._api_dialog()).props("flat dense round").classes("text-white"); self.header_toggle_row = ui.row().style("margin-left: 8px;")

        # Main content area
        with ui.column().classes("w-full items-center").style("padding: 8px;"):
            with ui.column().style(f"width: {cfg.CARD_WIDTH}; max-width: 98vw;").classes("q-gutter-xs"):
                # Status bar showing current operation
                self.status_card = ui.card().classes("w-full").style(self.theme._panel_style(f"border-left: 3px solid {cfg.PRIMARY}; padding: 6px 12px;"))
                with self.status_card:
                    with ui.row().classes("w-full items-center"):
                        status_icon = ui.icon("radio_button_checked", size="xs").classes("text-positive")
                        self.status_label = ui.label("System Ready").classes(f"text-caption text-weight-medium {self.theme.text_class()}").style("margin-left: 8px;")
                        ui.space()
                        self.status_output = ui.label("No operations performed").classes(f"text-caption {self.theme.text_class()}").style("opacity: 0.7; font-size: 0.7rem;")
                        self.text_elements.extend([status_icon, self.status_label, self.status_output])

                # Side-by-side layout: Control panel (left) + Device manager (right)
                with ui.row().classes("w-full").style("gap: 12px; align-items: flex-start;"):
                    # Manual Control Panel (left, fixed width)
                    with ui.column().style("flex: 0 0 350px; min-width: 0;"):
                        self.control_card = ui.card().classes("w-full").style(self.theme._panel_style().replace("padding: 16px", "padding: 12px"))
                        with self.control_card:
                            with ui.row().classes("w-full items-center").style("margin-bottom: 8px;"):
                                ctrl_icon = ui.icon("tune", size="sm").classes(f"{self.theme.text_class() if self.theme.is_dark else 'text-primary'}")
                                t = ui.label("Control Relay").classes(f"text-subtitle1 text-weight-bold {self.theme.text_class()}").style("margin-left: 8px;")
                                self.text_elements.extend([ctrl_icon, t])

                            with ui.column().classes("w-full").style("gap: 8px;"):
                                l1 = ui.label("Device ID").classes(f"text-caption text-weight-bold {self.theme.text_class()}").style("opacity: 0.7; margin-bottom: 2px;")
                                self.text_elements.append(l1)
                                self.relay_id_input = ui.input(placeholder="Default device").props("outlined dense").classes("w-full")
                                self.input_elements.append(self.relay_id_input)

                                l2 = ui.label("Relay Number").classes(f"text-caption text-weight-bold {self.theme.text_class()}").style("opacity: 0.7; margin-bottom: 2px; margin-top: 8px;")
                                self.text_elements.append(l2)
                                self.relay_num_input = ui.input(value="all", placeholder="1-8 or 'all'").props("outlined dense").classes("w-full")
                                self.input_elements.append(self.relay_num_input)

                            with ui.row().classes("w-full justify-center q-gutter-sm").style("margin-top: 12px;"):
                                ui.button("ON", icon="power_settings_new", color="positive", on_click=lambda: self.control_relay("on")).props("unelevated").style("flex: 1; font-weight: 600;")
                                ui.button("OFF", icon="power_off", color="negative", on_click=lambda: self.control_relay("off")).props("unelevated").style("flex: 1; font-weight: 600;")

                            ui.button("Refresh Status", icon="refresh", on_click=self.refresh_status).props("flat dense size=sm").classes(f"w-full {self.theme.text_class()}").style("opacity: 0.7; margin-top: 4px;")

                    # Device Manager Panel (right, flexible width)
                    with ui.column().style("flex: 1; min-width: 0;"):
                        self.device_card = ui.card().classes("w-full").style(self.theme._panel_style().replace("padding: 16px", "padding: 12px"))
                        with self.device_card:
                            with ui.row().classes("w-full items-center").style("gap: 8px; margin-bottom: 8px;"):
                                dev_mgr_icon = ui.icon("devices", size="sm").classes(f"{self.theme.text_class() if self.theme.is_dark else 'text-primary'}")
                                t = ui.label("Device Manager").classes(f"text-subtitle1 text-weight-bold {self.theme.text_class()}")
                                self.text_elements.extend([dev_mgr_icon, t])
                                ui.space()
                                self.devices_count = ui.chip("0 devices", icon="info_outline").props(f"dense square color={'grey-7' if self.theme.is_dark else 'primary'} size=sm")
                                ui.button("Scan", icon="search", color="primary", on_click=self.scan_devices).props("unelevated dense")

                            with ui.row().classes("w-full q-gutter-xs").style("margin-bottom: 8px;"):
                                self.devices_select = ui.select([], label="Device", with_input=True).props("outlined dense").classes("col")
                                self.input_elements.append(self.devices_select)
                                ui.button(icon="input", on_click=lambda: self.relay_id_input.set_value(self.devices_select.value or "")).props("outline dense").classes(self.theme.text_class())
                                ui.button(icon="clear", on_click=lambda: self.relay_id_input.set_value("")).props("flat dense").classes(self.theme.text_class())

                            self.device_separator = ui.separator().style(f"background: {'rgba(255,255,255,0.15)' if self.theme.is_dark else 'rgba(0,0,0,0.12)'}; margin: 8px 0;")
                            self.devices_container = ui.column().classes("w-full").style("gap: 8px;")

        # Register cards with theme manager and apply initial theme
        if self.status_card and self.control_card and self.device_card and self.header_toggle_row:
            self.theme.register_cards(self.status_card, self.control_card, self.device_card, self.header_toggle_row, self.device_separator)
            self.theme.apply(self)

    def _api_dialog(self):
        """Open dialog showing available REST API endpoints"""
        try:
            endpoints = [
                {"method": "GET", "path": "/health", "desc": "Service health"},
                {"method": "GET", "path": "/relay/devices", "desc": "List devices"},
                {"method": "GET", "path": "/relay/{number}/{state}", "desc": "Default device control"},
                {"method": "GET", "path": "/relay/{id}/{number}/{state}", "desc": "Specific device control"}
            ]

            with ui.dialog() as dialog, ui.card().style(self.theme._panel_style("padding: 16px;")).classes("w-full"):
                ui.label("API Endpoints").classes(f"text-h6 text-weight-medium {self.theme.text_class()}")

                with ui.column().classes("w-full").style("gap: 6px;"):
                    for ep in endpoints:
                        with ui.row().classes("items-center w-full").style("gap: 8px;"):
                            ui.chip(ep["method"]).props("color=primary size=sm")
                            ui.label(ep["path"]).classes(f"text-body2 text-weight-medium {self.theme.text_class()}")
                            ui.space()
                            ui.label(ep["desc"]).classes(f"text-caption {self.theme.text_class()}").style("opacity: 0.7;")

                with ui.row().classes("w-full justify-end").style("margin-top: 12px;"):
                    ui.button("Close", icon="close", on_click=dialog.close).props("flat")

            dialog.open()
        except Exception as e:
            logger.error(f"Failed to open API dialog: {e}")

# Application entry point
@ui.page("/")
def index_page():
    """Main page - initialize theme and build UI"""
    theme = ThemeManager()
    theme.init(start_dark=False)
    controller = RelayController(theme)
    controller.build()

if __name__ in {"__main__", "__mp_main__"}:
    parser = ArgumentParser(description="HID USB Relay REST API Server")
    parser.add_argument("--host", type=str, default='0.0.0.0', help="Host address")
    parser.add_argument("--port", type=int, default=9400, help="Port number")
    parser.add_argument("--native", action="store_true", help="Run as native desktop app")
    args = parser.parse_args()
    ui.run(host=args.host, port=args.port, native=args.native)
