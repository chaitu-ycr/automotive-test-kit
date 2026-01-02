from nicegui import ui

from py_uds_demo.core.client import UdsClient


class Web:
    """
    WebUi provides a NiceGUI-based web interface for interacting with the UDS (Unified Diagnostic Services) simulator.

    This class manages the UI components, handles user input, processes diagnostic requests, and logs interactions.
    """
    
    # UI Constants
    HEADER_HEIGHT = '60px'
    SIDEBAR_WIDTH = '400px'
    HEADER_PADDING = '0 20px'
    CARD_PADDING = '16px'
    CARD_HEADER_MARGIN = '12px'
    INNER_PADDING = '12px'
    SMALL_PADDING = '8px'
    HELP_INPUT_WIDTH = '180px'
    CHAT_MAX_WIDTH = '80%'
    SPACING_SM = '8px'
    SPACING_MD = '12px'
    SPACING_LG = '16px'
    
    # Color Scheme
    COLORS = {
        'header_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'primary': '#667eea',
        'primary_light': '#8b9efc',
        'secondary': '#f093fb',
        'success': '#4ade80',
        'success_light': '#86efac',
        'warning': '#fbbf24',
        'error': '#f87171',
        'info': '#60a5fa',
        'purple': '#a855f7',
        'pink': '#ec4899',
        'indigo': '#6366f1',
        'teal': '#14b8a6',
        'orange': '#f97316',
        'user_message': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'assistant_message': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'card_bg': '#ffffff',
        'card_shadow': '0 10px 40px rgba(0,0,0,0.1)',
        'card_shadow_hover': '0 20px 60px rgba(0,0,0,0.15)',
        'sidebar_bg': 'linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%)',
        'main_bg': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
    }
    
    # Animations
    TRANSITIONS = {
        'smooth': 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        'bounce': 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    }
    
    # Style Templates
    GLASS_CONTAINER = 'background: rgba(255,255,255,0.12); backdrop-filter: blur(12px); border-radius: 24px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s ease;'
    CARD_BORDER_RADIUS = '16px'
    CARD_ICON_RADIUS = '10px'
    SID_ITEM_RADIUS = '10px'
    
    # Quick Reference SIDs with icons and colors
    SID_REFERENCE = [
        ('settings', '0x10 - Diagnostic Session Control', '#667eea'),
        ('refresh', '0x11 - ECU Reset', '#14b8a6'),
        ('search', '0x22 - Read Data By Identifier', '#f97316'),
        ('lock', '0x27 - Security Access', '#f87171'),
        ('edit', '0x2E - Write Data By Identifier', '#a855f7'),
        ('build', '0x31 - Routine Control', '#6366f1'),
        ('favorite', '0x3E - Tester Present', '#ec4899'),
    ]

    def __init__(self):
        """
        Initialize the WebUi instance.

        Sets up the UdsClient and builds the UI components.
        """
        self.uds_client = UdsClient()
        self.logger = self.uds_client.server.logger
        self._build_ui()
    
    def _build_ui(self):
        """Build the complete UI interface."""
        self._build_header()
        self._build_main_content()
    
    # UI Helper Methods
    
    def _create_card_header(self, icon: str, title: str, color1: str, color2: str):
        """Create a card header with icon badge and gradient text.
        
        Args:
            icon: Material icon name
            title: Header title text
            color1: First gradient color
            color2: Second gradient color
        """
        with ui.row().classes('items-center gap-3').style(f'margin-bottom: {self.CARD_HEADER_MARGIN};'):
            with ui.card().classes('').style(f'padding: 8px; background: linear-gradient(135deg, {color1} 0%, {color2} 100%); border-radius: {self.CARD_ICON_RADIUS};'):
                ui.icon(icon, size='sm').classes('text-white')
            ui.label(title).classes('text-base font-bold').style(f'background: linear-gradient(135deg, {color1} 0%, {color2} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;')
    
    def _create_glass_container(self, content_builder, hover_class: str = 'hover:bg-white/20'):
        """Create a glass morphism container.
        
        Args:
            content_builder: Function to build content inside the container
            hover_class: CSS class for hover effect
        """
        with ui.row().classes(f'items-center gap-2 px-3 py-2 {hover_class}').style(self.GLASS_CONTAINER):
            content_builder()
    
    def _create_sid_item(self, icon: str, sid_info: str, color: str, click_handler):
        """Create a clickable SID reference item.
        
        Args:
            icon: Material icon name
            sid_info: SID information text
            color: Theme color for the item
            click_handler: Click event handler
        """
        with ui.card().classes('w-full').style(
            f'padding: {self.SPACING_SM} {self.SPACING_MD}; '
            f'background: linear-gradient(135deg, {color}15 0%, {color}05 100%); '
            f'border-radius: {self.SID_ITEM_RADIUS}; cursor: pointer; '
            f'transition: {self.TRANSITIONS["smooth"]}; border-left: 3px solid {color};'
        ).classes('hover:scale-105 hover:shadow-lg').on('click', click_handler):
            with ui.row().classes('items-center gap-3'):
                with ui.card().classes('').style(f'padding: 6px; background: {color}; border-radius: 8px;'):
                    ui.icon(icon, size='xs').classes('text-white')
                ui.label(sid_info).classes('text-xs font-medium').style(f'color: {color};')

    def run(self):
        """
        Launch the NiceGUI app for the UDS simulator UI.

        Starts the NiceGUI server.
        """
        ui.run(title="PY-UDS-DEMO SIM", favicon="🚗")

    def _build_header(self):
        """Build the application header with controls."""
        with ui.header().classes('text-white shadow-xl').style(
            f'height: {self.HEADER_HEIGHT}; padding: {self.HEADER_PADDING}; '
            f'background: {self.COLORS["header_gradient"]}; '
            f'box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3); '
            f'border-bottom: 1px solid rgba(255,255,255,0.1);'
        ):
            with ui.row().classes('w-full items-center justify-between'):
                self._build_header_branding()
                self._build_header_controls()
                self._build_header_help()
    
    def _build_header_branding(self):
        """Build the header branding section."""
        with ui.row().classes('items-center gap-4'):
            ui.icon('directions_car', size='lg').classes('text-white').style(
                'filter: drop-shadow(0 2px 8px rgba(255,255,255,0.3));'
            )
            ui.label('UDS Diagnostic Simulator').classes('text-lg font-bold text-white').style(
                'letter-spacing: 0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'
            )
    
    def _build_header_controls(self):
        """Build the header controls section."""
        with ui.row().classes('items-center gap-6 flex-grow justify-end'):
            with ui.row().classes('items-center gap-3 px-4 py-2 hover:bg-white/20').style(self.GLASS_CONTAINER):
                self.tester_present_checkbox = ui.checkbox(
                    'Tester Present',
                    value=False,
                    on_change=self._update_tester_present
                ).classes('text-white font-medium').props('dark').style('margin: 0; font-size: 13px;')
    
    def _build_header_help(self):
        """Build the header help section."""
        with ui.row().classes('items-center gap-2'):
            def build_help_content():
                ui.icon('help_outline', size='sm').classes('text-white').style('opacity: 0.9;')
                self.help_sid_input = ui.input(
                    placeholder='Search SID...',
                ).classes('text-sm').props('dark dense borderless').style(
                    f'width: {self.HELP_INPUT_WIDTH}; background: transparent; color: white;'
                ).on('keydown.enter', self._show_help)
                ui.button(icon='search', on_click=self._show_help).props('flat dense round').classes(
                    'text-white'
                ).tooltip('Search SID Help').style('transition: all 0.2s ease;').classes('hover:bg-white/20')
            
            self._create_glass_container(build_help_content)

    def _build_main_content(self):
        """Build the main content area with sidebar and chat."""
        with ui.row().classes('w-full gap-4 p-4').style(f'height: calc(100vh - {self.HEADER_HEIGHT}); background: {self.COLORS["main_bg"]}; overflow: hidden;'):
            self._build_sidebar()
            self._build_chat_area()

    def _build_sidebar(self):
        """Build the left sidebar with controls and reference."""
        with ui.column().classes('gap-4').style(f'width: {self.SIDEBAR_WIDTH}; height: 100%; overflow-y: auto; background: {self.COLORS["sidebar_bg"]}; padding: {self.SPACING_MD}; border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);'):
            self._build_diagnostic_request_card()
            self._build_quick_reference_card()

    def _build_diagnostic_request_card(self):
        """Build the diagnostic request input card."""
        with ui.card().classes('w-full shadow-lg').style(
            f'padding: {self.CARD_PADDING}; background: {self.COLORS["card_bg"]}; '
            f'border-radius: {self.CARD_BORDER_RADIUS}; border: 2px solid {self.COLORS["primary_light"]}; '
            f'box-shadow: {self.COLORS["card_shadow"]};'
        ):
            self._create_card_header('send', 'Diagnostic Request', self.COLORS['primary'], self.COLORS['purple'])
            
            self.diag_req_input = ui.input(
                placeholder='e.g., 22 F1 87',
            ).classes('w-full').props('outlined rounded dense').style(
                'font-size: 14px;'
            ).on('keydown.enter', self._handle_diagnostic_request)
            
            ui.button('Send Request', on_click=self._handle_diagnostic_request, icon='send').props(
                'rounded'
            ).classes('w-full hover:scale-105').style(
                f'background: linear-gradient(135deg, {self.COLORS["primary"]} 0%, {self.COLORS["purple"]} 100%); '
                f'color: white; font-weight: 600; padding: {self.INNER_PADDING}; '
                f'margin-top: {self.CARD_HEADER_MARGIN}; transition: {self.TRANSITIONS["smooth"]}; '
                f'box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);'
            )

    def _build_quick_reference_card(self):
        """Build the quick reference card with SID information."""
        with ui.card().classes('w-full flex-grow shadow-lg').style(
            f'padding: {self.CARD_PADDING}; background: {self.COLORS["card_bg"]}; '
            f'border-radius: {self.CARD_BORDER_RADIUS}; border: 2px solid {self.COLORS["indigo"]}; '
            f'box-shadow: {self.COLORS["card_shadow"]};'
        ):
            self._create_card_header('bookmarks', 'Quick Reference', self.COLORS['indigo'], self.COLORS['purple'])
            
            with ui.column().classes('gap-2'):
                for icon, sid_info, color in self.SID_REFERENCE:
                    sid_hex = sid_info.split(' ')[0]
                    self._create_sid_item(icon, sid_info, color, lambda sid=sid_hex: self._show_help_for_sid(sid))

    def _build_chat_area(self):
        """Build the chat display area."""
        with ui.column().classes('flex-1').style(
            f'height: 100%; overflow: hidden; '
            f'background: linear-gradient(135deg, rgba(236, 72, 153, 0.05) 0%, rgba(249, 168, 212, 0.05) 100%); '
            f'padding: {self.SPACING_MD}; border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);'
        ):
            with ui.card().classes('w-full shadow-lg').style(
                f'padding: {self.CARD_PADDING}; background: {self.COLORS["card_bg"]}; '
                f'border-radius: {self.CARD_BORDER_RADIUS}; border: 2px solid {self.COLORS["pink"]}; '
                f'height: 100%; display: flex; flex-direction: column; box-shadow: {self.COLORS["card_shadow"]};'
            ):
                with ui.row().classes('items-center gap-3').style(f'flex-shrink: 0; margin-bottom: {self.CARD_HEADER_MARGIN};'):
                    self._create_card_header('chat', 'Diagnostic Communication', self.COLORS['pink'], self.COLORS['secondary'])
                
                self.chat_container = ui.column().classes('w-full gap-2 rounded-lg').style(
                    f'flex: 1; overflow-y: auto; padding: {self.INNER_PADDING}; '
                    f'background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);'
                )

    def _add_message(self, role: str, content: str):
        """
        Add a message to the chat display.

        Args:
            role (str): Either 'user' or 'assistant'
            content (str): The message content
        """
        is_user = role == 'user'
        alignment = 'justify-end' if is_user else 'justify-start'
        sender_name = 'You' if is_user else '🤖 UDS Simulator'
        gradient = self.COLORS['user_message'] if is_user else self.COLORS['assistant_message']
        
        with self.chat_container:
            with ui.row().classes(f'w-full {alignment}').style(f'margin-bottom: {self.SPACING_SM}; animation: slideIn 0.3s ease-out;'):
                with ui.card().classes('shadow-md').style(f'max-width: {self.CHAT_MAX_WIDTH}; background: {gradient}; border-radius: 16px; padding: {self.INNER_PADDING}; box-shadow: 0 4px 20px rgba(0,0,0,0.15);'):
                    ui.label(sender_name).classes('text-xs font-bold text-white').style(f'margin-bottom: {self.SPACING_SM};')
                    ui.label(content).classes('text-sm text-white').style('word-break: break-word; white-space: pre-wrap;')
        
        # Add animation keyframes
        ui.add_head_html('''
            <style>
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
            </style>
        ''')
        
        self._scroll_chat_to_bottom()

    def _scroll_chat_to_bottom(self):
        """Scroll chat container to the bottom."""
        ui.run_javascript(f'getElement({self.chat_container.id}).scrollTop = getElement({self.chat_container.id}).scrollHeight')

    def _handle_diagnostic_request(self):
        """
        Handle diagnostic request submission and display response.
        """
        diagnostic_request = self.diag_req_input.value
        if not self._validate_input(diagnostic_request):
            return
        
        diagnostic_request_clean = diagnostic_request.replace(" ", "")
        
        try:
            diagnostic_request_stream = self._parse_hex_string(diagnostic_request_clean)
            user_sent_request = self.uds_client.format_request(diagnostic_request_stream)
            self._add_message('user', user_sent_request)
            
            diagnostic_response = self.uds_client.send_request(diagnostic_request_stream, True)
            self._add_message('assistant', diagnostic_response)
        except ValueError:
            self._handle_invalid_hex(diagnostic_request)
        except Exception as e:
            self._handle_request_error(diagnostic_request, e)
        finally:
            self.diag_req_input.value = ''

    def _show_help(self):
        """
        Display help information for a specific SID.
        """
        sid_str = self.help_sid_input.value
        if not self._validate_input(sid_str):
            return
        
        try:
            sid = int(sid_str, 16)
            service = self.uds_client.server.service_map.get(sid)
            
            self._add_message('user', f'Help for SID 0x{sid:02X}')
            
            help_text = service.__doc__ if service else f'No help found for SID 0x{sid:02X}.'
            if service and not service.__doc__:
                help_text = f'No documentation available for SID 0x{sid:02X}.'
            
            self._add_message('assistant', help_text)
        except (ValueError, IndexError):
            self._add_message('user', f'Help for SID {sid_str}')
            self._add_message('assistant', 'Invalid SID. Please enter a valid hex value.')
        finally:
            self.help_sid_input.value = ''

    def _show_help_for_sid(self, sid_hex: str):
        """Display help information for a clicked SID from Quick Reference.
        
        Args:
            sid_hex (str): The SID in hex format (e.g., '0x10')
        """
        try:
            sid = int(sid_hex, 16)
            service = self.uds_client.server.service_map.get(sid)
            
            self._add_message('user', f'Help for SID {sid_hex}')
            
            help_text = service.__doc__ if service else f'No help found for SID {sid_hex}.'
            if service and not service.__doc__:
                help_text = f'No documentation available for SID {sid_hex}.'
            
            self._add_message('assistant', help_text)
        except (ValueError, IndexError):
            self._add_message('user', f'Help for SID {sid_hex}')
            self._add_message('assistant', 'Invalid SID. Please enter a valid hex value.')

    def _update_tester_present(self, event):
        """
        Update the tester present flag in the UDS server and log the action.

        Args:
            event: NiceGUI event object containing the checkbox value
        """
        value = event.value
        self.uds_client.server.diagnostic_session_control.tester_present_active = value
        
        status = 'activated' if value else 'deactivated'
        icon = '✔️' if value else '✖️'
        self.logger.info(f'tester present [{icon}] {status}')
        
        ui.notify(
            f'Tester Present {status} {icon}',
            type='positive' if value else 'info'
        )

    # Validation & Parsing Helpers
    
    @staticmethod
    def _validate_input(value: str) -> bool:
        """Validate that input is not empty."""
        return bool(value and value.strip())

    @staticmethod
    def _parse_hex_string(hex_string: str) -> list[int]:
        """Parse hex string into list of integers."""
        return [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]
    
    # Error Handling Helpers

    def _handle_invalid_hex(self, diagnostic_request: str):
        """Handle invalid hex input."""
        self._add_message('user', diagnostic_request)
        self._add_message('assistant', 'Invalid hex input. Please enter a valid hex string.')
        self.logger.warning(f"Invalid Diagnostic Request 💉 {diagnostic_request}")

    def _handle_request_error(self, diagnostic_request: str, error: Exception):
        """Handle request processing error."""
        self._add_message('user', diagnostic_request)
        self._add_message('assistant', f'An error occurred while processing the request. {error}')
        self.logger.error(f"Error occurred while processing request 💉 {diagnostic_request}: {error}")


if __name__ in {"__main__", "__mp_main__"}:
    web_ui = Web()
    web_ui.run()
