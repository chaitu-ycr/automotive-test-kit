import pytest
from unittest.mock import MagicMock, patch
from kmtronic_usb_relay.four_channel_relay import RelayController

@pytest.fixture
def mock_serial_utils():
    """Fixture for a mock serial utility object."""
    mock = MagicMock()
    mock.open_connection.return_value = True
    mock.is_connected = True
    mock.close_connection.return_value = True
    return mock

# --- Initialization and Connection Tests ---

def test_init_sets_connected_flag(mock_serial_utils):
    """Test that RelayController sets is_connected when initialized with a mock serial utility."""
    controller = RelayController("COM4", serial_utils=mock_serial_utils)
    assert controller.is_connected

def test_close_calls_close_connection(mock_serial_utils):
    """Test that close() calls the serial utility's close_connection method."""
    controller = RelayController("COM4", serial_utils=mock_serial_utils)
    controller.close()
    mock_serial_utils.close_connection.assert_called_once()

# --- Relay Command Tests ---

def test_turn_on_sends_correct_command(mock_serial_utils):
    """Test that turn_on calls the internal _send_relay_command with correct arguments."""
    controller = RelayController("COM4", serial_utils=mock_serial_utils)
    with patch.object(controller, "_send_relay_command") as send_cmd:
        controller.turn_on(1)
        send_cmd.assert_called_once_with(1, True)

def test_turn_off_sends_correct_command(mock_serial_utils):
    """Test that turn_off calls the internal _send_relay_command with correct arguments."""
    controller = RelayController("COM4", serial_utils=mock_serial_utils)
    with patch.object(controller, "_send_relay_command") as send_cmd:
        controller.turn_off(2)
        send_cmd.assert_called_once_with(2, False)

# --- Status and Validation Tests ---

def test_get_statuses_returns_status_dict(mock_serial_utils):
    """Test that get_statuses returns a dictionary with relay statuses."""
    mock_serial_utils.send_command.return_value = b'\x01\x00\x01\x00'
    mock_serial_utils.receive.return_value = b'\x01\x00\x01\x00'
    controller = RelayController("COM4", serial_utils=mock_serial_utils)
    with patch.object(controller, "_send_relay_command"):
        statuses = controller.get_statuses()
    assert isinstance(statuses, dict)
    assert all(k in statuses for k in ["R1", "R2", "R3", "R4"])

def test_invalid_relay_number_raises_value_error(mock_serial_utils):
    """Test that invalid relay numbers raise ValueError."""
    controller = RelayController("COM4", serial_utils=mock_serial_utils)
    with pytest.raises(ValueError):
        controller.turn_on(0)
    with pytest.raises(ValueError):
        controller.turn_off(5)

# --- Context Manager Test ---

def test_context_manager_closes_on_exit(mock_serial_utils):
    """Test that using RelayController as a context manager calls close()."""
    controller = RelayController("COM4", serial_utils=mock_serial_utils)
    with patch.object(controller, "close") as close_mock:
        with controller:
            pass
        close_mock.assert_called_once()