import unittest
from unittest.mock import Mock
import json

# Import functions from your main script
from app import (
    calculate_new_position,
    is_valid_next_stop_location,
    on_message,
    vehicleData
)

class TestVehicleFunctions(unittest.TestCase):

    def test_calculate_new_position_normal(self):
        result = calculate_new_position(10.0, 20.0)
        self.assertAlmostEqual(result, 11.0)

    def test_is_valid_next_stop_location_valid(self):
        payload = {"nextStopLocation": [12.3, 45.6]}
        self.assertTrue(is_valid_next_stop_location(payload))

    def test_is_valid_next_stop_location_invalid_type(self):
        payload = {"nextStopLocation": "not a list"}
        self.assertFalse(is_valid_next_stop_location(payload))

    def test_is_valid_next_stop_location_wrong_length(self):
        payload = {"nextStopLocation": [1.0]}
        self.assertFalse(is_valid_next_stop_location(payload))

    def test_is_valid_next_stop_location_non_numeric(self):
        payload = {"nextStopLocation": [1.0, "x"]}
        self.assertFalse(is_valid_next_stop_location(payload))


class TestMQTTCallbacks(unittest.TestCase):

    def test_on_message_valid_payload(self):
        mock_client = Mock()
        payload = {
            "nextStopLocation": [2.0, 3.0]
        }
        msg = Mock()
        msg.payload = json.dumps(payload).encode()
        on_message(mock_client, None, msg)
        self.assertNotEqual(vehicleData["location"], [1.0, 1.0])

    def test_on_message_invalid_payload(self):
        oldLocation=vehicleData["location"].copy()
        mock_client = Mock()
        payload = {
            "invalidKey": [2.0, 3.0]
        }
        msg = Mock()
        msg.payload = json.dumps(payload).encode()
        on_message(mock_client, None, msg)
        # No change expected in vehicleData['location']
        self.assertEqual(oldLocation, vehicleData["location"])

if __name__ == "__main__":
    unittest.main()