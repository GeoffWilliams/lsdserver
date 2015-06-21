import unittest
import sys
import os
APP_DIR = os.path.dirname(os.path.realpath(__file__)) + "/.."
sys.path.append(APP_DIR)
from lsdserver.validator import Validator

class TestValidator(unittest.TestCase):
    """
    Tests for identifier and data structure validator
    """
    invalid_identifier = "invalid!identifier%"
    valid_identifier = "valid_identifier"

    parameters = {
        "http://lsdserver.com/parameters/temperature": {
            "type": "float"
        },
        "http://lsdserver.com/parameters/relative_humidity": {
            "type": "float"
        }
    }

    def setUp(self):
        self.validator = Validator()
        self.validator.parameters = TestValidator.parameters

    def tearDown(self):
        pass

    def test_valid_identifier(self):
        self.assertTrue(
            self.validator.validate_identifier(
                TestValidator.valid_identifier))

    def test_invalid_identifier(self):
        self.assertFalse(
            self.validator.validate_identifier(
                TestValidator.invalid_identifier))

    def test_valid_parameter_types(self):
        self.assertTrue(self.validator.validate_parameter_type("int"))
        self.assertTrue(self.validator.validate_parameter_type("float"))
        self.assertTrue(self.validator.validate_parameter_type("bool"))

    def test_invalid_parameter_types(self):
        self.assertFalse(self.validator.validate_parameter_type("invalid"))

    def test_valid_location(self):
        self.assertTrue(self.validator.validate_position("POINT (50 50)"))
        self.assertTrue(self.validator.validate_position("POINT (-50 -50)"))
        self.assertTrue(self.validator.validate_position("POINT (+50 +50)"))
        self.assertTrue(self.validator.validate_position("POINT (-5.1 +5.92)"))

    def test_invalid_location(self):
        self.assertFalse(self.validator.validate_position("POINT(-5.1,+5.92)"))
        self.assertFalse(self.validator.validate_position("nonsense"))

    def test_valid_time_string(self):
        self.assertTrue(self.validator.validate_time_string(
            "2013-11-26T20:25:12.014Z") is not None)

    def test_invalid_time_string(self):
        self.assertFalse(self.validator.validate_time_string(
            "2013-30-11T20:25:12.014Z"))
        self.assertFalse(self.validator.validate_time_string(
            "nonsense"))

    def test_valid_platform(self):
        # try populating all available fields
        platform = {
            "name": "name",
            "manufacturer": "manufacturer",
            "model": "model",
            "serial_number": "serial_number",
            "description": "description",
            "link": "http://www.google.com",
            "position": "POINT (40.0024 -52.005)"
        }
        self.assertTrue(self.validator.validate_platform(platform))

        # test minmal field set (empty)
        platform = {}
        self.assertTrue(self.validator.validate_platform(platform))

    def test_invalid_platform(self):
        # invalid 'position' value
        platform = {
            "position": "invalid position wkt"
        }
        self.assertFalse(self.validator.validate_platform(platform))

        # unsupported field 'foo'
        platform = {
            "foo": "BAR"
        }
        self.assertFalse(self.validator.validate_platform(platform))

    def test_valid_parameter(self):
        # try populating each available field
        parameter = {
            "name": "name",
            "description": "description",
            "type": "int",
            "uom": "uom",
            "min_value": -50,
            "max_value": 50,
            "link": "http://www.google.com"
        }
        self.assertTrue(self.validator.validate_parameter(parameter))

        # try the minimal field list
        parameter = {
            "name": "name",
            "type": "int",
        }
        self.assertTrue(self.validator.validate_parameter(parameter))

    def test_invalid_parameter(self):
        # unknown field 'foo'
        parameter = {
            "name": "name",
            "description": "description",
            "type": "invalid",
            "uom": "uom",
            "min_value": -50,
            "max_value": 50,
            "link": "http://www.google.com",
            "foo": "BAR"
        }
        self.assertFalse(self.validator.validate_parameter(parameter))

        # invalid value for 'type'
        parameter = {
            "name": "name",
            "type": "unsupported",
        }
        self.assertFalse(self.validator.validate_parameter(parameter))

        # invalid value for 'min_value' and 'max_value'
        parameter = {
            "name": "name",
            "type": "unsupported",
            "min_value": "abc",
            "max_value": "-13ga",
        }
        self.assertFalse(self.validator.validate_parameter(parameter))

        # missing field 'type'
        parameter = {
            "name": True,
            "uom": "celcius",
            "description": "description",
        }
        self.assertFalse(self.validator.validate_parameter(parameter))

    def test_valid_sensor(self):
        # all supported fields
        sensor = {
            "name": "name",
            "manufacturer": "manufacturer",
            "model": "model",
            "serial_number": "serial_number",
            "description": "description",
            "parameters": ["http://lsdserver.com/parameters/temperature"],
            "link": "http://www.google.com",
        }
        self.assertTrue(self.validator.validate_sensor(sensor))

        # minimal fields
        sensor = {
            "parameters": ["http://lsdserver.com/parameters/temperature"],
        }
        self.assertTrue(self.validator.validate_sensor(sensor))

        # multiple parameters
        sensor = {
            "parameters": [
                "http://lsdserver.com/parameters/temperature",
                "http://lsdserver.com/parameters/relative_humidity"
            ]
        }
        self.assertTrue(self.validator.validate_sensor(sensor))

    def test_invalid_sensor(self):

        # invalid parameter
        sensor = {
            "parameters": [
                "http://lsdserver.com/parameters/temperature",
                "nothere"
            ]
        }
        self.assertFalse(self.validator.validate_sensor(sensor))

    def test_valid_observation(self):
        # 1 parameter, no time
        observation = {
            "http://lsdserver.com/parameters/temperature": 23.4
        }
        self.assertTrue(self.validator.validate_observation(observation))

        # 2 parameters, no time
        observation = {
            "http://lsdserver.com/parameters/temperature": 23.4,
            "http://lsdserver.com/parameters/relative_humidity": 55.4
        }
        self.assertTrue(self.validator.validate_observation(observation))

        # 2 parameters, time
        observation = {
            "time": "2013-11-26T20:25:12.014Z",
            "http://lsdserver.com/parameters/temperature": 23.4,
            "http://lsdserver.com/parameters/relative_humidity": 55.4
        }
        self.assertTrue(self.validator.validate_observation(observation))

    def test_invalid_observation(self):
        # invalid time
        observation = {
            "time": "2013-33-26T20:25:12.014Z",
            "http://lsdserver.com/parameters/temperature": 23.4,
        }
        self.assertFalse(self.validator.validate_observation(observation))

        # invalid parameter
        observation = {
            "nothere": 34.4,
        }
        self.assertFalse(self.validator.validate_observation(observation))

        # missing value
        observation = {
            "http://lsdserver.com/parameters/temperature": "",
        }
        self.assertFalse(self.validator.validate_observation(observation))

        # inappropriate value (should be float)
        observation = {
            "http://lsdserver.com/parameters/temperature": "abc",
        }
        self.assertFalse(self.validator.validate_observation(observation))

        # empty request
        observation = {}
        self.assertFalse(self.validator.validate_observation(observation))

    def test_value_valid(self):
        self.assertTrue(self.validator.validate_value("int", 12))
        self.assertTrue(self.validator.validate_value("float", 33.002))
        self.assertTrue(self.validator.validate_value("bool", True))

    def test_value_invalid(self):
        self.assertFalse(self.validator.validate_value("int", "abc"))
        self.assertFalse(self.validator.validate_value("float", "abc"))
