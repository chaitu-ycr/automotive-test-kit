import pytest
from unittest.mock import MagicMock, patch

from tenma_ps.power_supply import TenmaPs

@pytest.fixture
def mock_device():
    # Create a mock device with all required methods
    device = MagicMock()
    device.getVersion.return_value = "v1.2.3"
    device.getStatus.return_value = "OK"
    device.runningVoltage.return_value = 12.34
    device.runningCurrent.return_value = 1.23
    device.setVoltage.return_value = None
    device.setCurrent.return_value = None
    device.ON.return_value = None
    device.OFF.return_value = None
    device.close.return_value = None
    return device

@patch("tenma_ps.power_supply.instantiate_tenma_class_from_device_response")
def test_init_calls_instantiate(mock_instantiate):
    mock_instantiate.return_value = MagicMock()
    ps = TenmaPs("COM4")
    mock_instantiate.assert_called_once_with("COM4")

@patch("tenma_ps.power_supply.instantiate_tenma_class_from_device_response")
def test_get_version(mock_instantiate, mock_device):
    mock_instantiate.return_value = mock_device
    ps = TenmaPs("COM4")
    assert ps.get_version() == "v1.2.3"
    mock_device.getVersion.assert_called_once()

@patch("tenma_ps.power_supply.instantiate_tenma_class_from_device_response")
def test_get_status(mock_instantiate, mock_device):
    mock_instantiate.return_value = mock_device
    ps = TenmaPs("COM4")
    assert ps.get_status() == "OK"
    mock_device.getStatus.assert_called_once()

@patch("tenma_ps.power_supply.instantiate_tenma_class_from_device_response")
def test_turn_on_and_off(mock_instantiate, mock_device):
    mock_instantiate.return_value = mock_device
    ps = TenmaPs("COM4")
    ps.turn_on()
    mock_device.ON.assert_called_once()
    ps.turn_off()
    mock_device.OFF.assert_called_once()

@patch("tenma_ps.power_supply.instantiate_tenma_class_from_device_response")
def test_read_voltage_and_current(mock_instantiate, mock_device):
    mock_instantiate.return_value = mock_device
    ps = TenmaPs("COM4")
    assert ps.read_voltage(1) == 12.34
    mock_device.runningVoltage.assert_called_once_with(1)
    assert ps.read_current(2) == 1.23
    mock_device.runningCurrent.assert_called_once_with(2)

@patch("tenma_ps.power_supply.instantiate_tenma_class_from_device_response")
def test_set_voltage_and_current(mock_instantiate, mock_device):
    mock_instantiate.return_value = mock_device
    ps = TenmaPs("COM4")
    ps.set_voltage(1, 5.0)
    mock_device.setVoltage.assert_called_once_with(1, 5.0 * ps.VOLTAGE_MULTIPLIER)
    ps.set_current(2, 2.5)
    mock_device.setCurrent.assert_called_once_with(2, 2.5 * ps.CURRENT_MULTIPLIER)

@patch("tenma_ps.power_supply.instantiate_tenma_class_from_device_response")
def test_close(mock_instantiate, mock_device):
    mock_instantiate.return_value = mock_device
    ps = TenmaPs("COM4")
    ps.close()
    mock_device.close.assert_called_once()

@patch("tenma_ps.power_supply.instantiate_tenma_class_from_device_response")
def test_context_manager(mock_instantiate, mock_device):
    mock_instantiate.return_value = mock_device
    with TenmaPs("COM4") as ps:
        assert isinstance(ps, TenmaPs)
    mock_device.close.assert_called_once()