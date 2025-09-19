# import pytest for testing
import pytest
from py_uds_demo.core.client import UdsClient
from py_uds_demo.core.server import UdsServer
from py_uds_demo.core.utils.helpers import Sid, Sfid, Nrc

@pytest.fixture
def uds_client():
    return UdsClient()

@pytest.fixture
def uds_server():
    return UdsServer()

def test_send_request_positive_response(uds_client):
    # Use a supported SID (e.g., ReadDataByIdentifier = 0x22)
    sid = Sid().READ_DATA_BY_IDENTIFIER
    req = [sid, 0xFF, 0x01]
    resp = uds_client.send_request(req, False)
    # Should be a positive response: [sid+0x40, 0x00]
    assert resp == [sid + 0x40, 0xFF, 0x01, 0x01]

def test_send_request_formatted_response(uds_client):
    sid = Sid().READ_DATA_BY_IDENTIFIER
    req = [sid, 0xFF, 0x01]
    resp = uds_client.send_request(req, True)
    # Should be a formatted string starting with green dot
    assert resp.startswith("🟢 ")
    assert "%02X" % (sid + 0x40) in resp

def test_send_request_negative_response(uds_client):
    # Use an unsupported SID (e.g., 0x99)
    req = [0x99]
    resp = uds_client.send_request(req, False)
    # Should be a negative response: [0x7F, 0x99, NRC]
    assert resp[0] == 0x7F
    assert resp[1] == 0x99
    assert resp[2] == Nrc().SERVICE_NOT_SUPPORTED

def test_send_request_negative_response_formatted(uds_client):
    req = [0x99]
    resp = uds_client.send_request(req, True)
    # Should be a formatted string starting with red dot
    assert resp.startswith("🔴 ")
    assert "7F 99" in resp

def test_server_supported_services(uds_server):
    # Should contain all SIDs
    sids = uds_server.supported_services
    assert Sid().DIAGNOSTIC_SESSION_CONTROL in sids
    assert Sid().READ_DATA_BY_IDENTIFIER in sids

def test_server_process_request_positive(uds_server):
    sid = Sid().READ_DATA_BY_IDENTIFIER
    resp = uds_server.process_request([sid, 0xFF, 0x01])
    assert resp[0] == sid + 0x40

def test_server_process_request_negative(uds_server):
    resp = uds_server.process_request([0x99])
    assert resp[0] == 0x7F
    assert resp[1] == 0x99
    assert resp[2] == Nrc().SERVICE_NOT_SUPPORTED

# Tests for newly implemented services

def test_read_memory_by_address_positive(uds_client):
    req = [Sid().RMBA, 0x00, 0x00, 0x10, 0x00]
    resp = uds_client.send_request(req, False)
    assert resp == [Sid().RMBA + 0x40, 0x11, 0x22, 0x33, 0x44]

def test_read_memory_by_address_negative(uds_client):
    req = [Sid().RMBA, 0x00, 0x00, 0x30, 0x00] # Invalid address
    resp = uds_client.send_request(req, False)
    assert resp == [0x7F, Sid().RMBA, Nrc().REQUEST_OUT_OF_RANGE]

def test_write_data_by_identifier_positive(uds_client):
    did = 0xF199
    req = [Sid().WDBI, (did >> 8) & 0xFF, did & 0xFF, 0x20, 0x24, 0x01, 0x01]
    resp = uds_client.send_request(req, False)
    assert resp == [Sid().WDBI + 0x40, (did >> 8) & 0xFF, did & 0xFF]

def test_write_data_by_identifier_negative(uds_client):
    did = 0xAAAA # Invalid DID
    req = [Sid().WDBI, (did >> 8) & 0xFF, did & 0xFF, 0x20, 0x24, 0x01, 0x01]
    resp = uds_client.send_request(req, False)
    assert resp == [0x7F, Sid().WDBI, Nrc().REQUEST_OUT_OF_RANGE]

def test_clear_diagnostic_information_positive(uds_client):
    req = [Sid().CDTCI]
    resp = uds_client.send_request(req, False)
    assert resp == [Sid().CDTCI + 0x40]
    # Verify that DTCs are cleared
    req = [Sid().RDTCI, Sfid().RNODTCBSM, 0xFF]
    resp = uds_client.send_request(req, False)
    assert resp[-1] == 0 # No DTCs

def test_read_dtc_information_positive(uds_client):
    req = [Sid().RDTCI, Sfid().RNODTCBSM, 0xFF]
    resp = uds_client.send_request(req, False)
    assert resp[0] == Sid().RDTCI + 0x40
    assert resp[-1] > 0 # Should have at least one DTC initially

def test_input_output_control_by_identifier_positive(uds_client):
    did = 0xAE01
    req = [Sid().IOCBI, (did >> 8) & 0xFF, did & 0xFF, 0x03] # Return control to ECU
    resp = uds_client.send_request(req, False)
    assert resp == [Sid().IOCBI + 0x40, (did >> 8) & 0xFF, did & 0xFF]

def test_routine_control_positive(uds_client):
    routine_id = 0xFF00
    req = [Sid().RC, Sfid().STR, (routine_id >> 8) & 0xFF, routine_id & 0xFF]
    resp = uds_client.send_request(req, False)
    assert resp == [Sid().RC + 0x40, Sfid().STR, (routine_id >> 8) & 0xFF, routine_id & 0xFF]

def test_upload_download_negative(uds_client):
    req = [Sid().RD, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    resp = uds_client.send_request(req, False)
    assert resp == [0x7F, Sid().RD, Nrc().SERVICE_NOT_SUPPORTED]
