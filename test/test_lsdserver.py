#!/usr/bin/env python
#
# lsdserver -- Linked Sensor Data Server
# Copyright (C) 2014 Geoff Williams <geoff@geoffwilliams.me.uk>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import sys
import os
APP_DIR = os.path.dirname(__file__) + "/.."
sys.path.append(APP_DIR)
import unittest
import lsdserver
import tempfile
from lsdserver import create_app
from lsdserver import status
from lsdserver.validator import Validator
import flask
from flask import render_template, current_app
import json
import logging
from lsdserver.backend.mysql import Mysql
from lsdserver.driver import LsdBackend


class MockSystem(object):
    logger = logging.getLogger('lsdserver.MockSystem')
    logger.setLevel(logging.DEBUG)

    def __init__(self):
        self.parameters = {}
        self.platforms = {}
        self.sensors = {}

    def get_platform(self, platform_id):
        data = None
        if platform_id in self.platforms:
            data = self.platforms[platform_id]
        else:
            flask.abort(status.NOT_FOUND)
        return data

    def get_sensor(self, platform_id, sensor_id):
        data = None
        if platform_id in self.platforms:
            if sensor_id in self.sensors:
                data = self.sensors[sensor_id]
            else:
                # no such sensor
                self.logger.debug('sensor not found:  ' + sensor_id)
                flask.abort(status.NOT_FOUND)
        else:
            # no such platform
            self.logger.debug('platform not found:  ' + platform_id)
            flask.abort(status.NOT_FOUND)
        return data

    def get_platforms(self):
        return self.platforms

    def create_platform(self, platform_id, data):
        if platform_id in self.platforms:
            self.logger.debug('duplicate platform:  %s', platform_id)
            flask.abort(status.CONFLICT)
        else:
            self.logger.debug(
                'create_platform(%s, %s)', platform_id, str(data))
            self.platforms[platform_id] = data

    def create_sensor(self, platform_id, sensor_id, data):
        if platform_id in self.platforms:
            if sensor_id in self.sensors:
                self.logger.debug('duplicate sensor:  %s', sensor_id)
                flask.abort(status.CONFLICT)
            else:
                self.logger.debug('create_sensor(%s, %s, %s)',
                    platform_id, sensor_id, str(data))
                self.sensors[sensor_id] = data
        else:
            flask.abort(status.NOT_FOUND)

    def delete_platform(self, platform_id):
        if platform_id in self.platforms:
            del self.platforms[platform_id]

    def delete_sensor(self, platform_id, sensor_id):
        if platform_id in self.platforms:
            if sensor_id in self.sensors:
                del self.sensors[sensor_id]
            else:
                flask.abort(status.NOT_FOUND)
        else:
            flask.abort(status.NOT_FOUND)

    def create_parameter(self, parameter_id, data):
        if parameter_id in self.parameters:
            self.logger.debug("duplicate parameter:  %s", parameter_id)
            flask.abort(status.CONFLICT)
        else:
            self.parameters[parameter_id] = data

    def get_parameter(self, parameter_id):
        if parameter_id in self.parameters:
            data = self.parameters[parameter_id]
        else:
            flask.abort(status.NOT_FOUND)
        return data

    def delete_parameter(self, parameter_id):
        if parameter_id in self.parameters:
            del self.parameters[parameter_id]
        else:
            flask.abort(status.NOT_FOUND)

    def get_parameters(self):
        return self.parameters
LsdBackend.register(MockSystem)


class TestRestApi(unittest.TestCase):
    """Unit tests for lsdserver."""
    app = None
    client = None

    sample_parameter_id = "temperature"
    sample_parameter = {
        "description": "description",
        "type": "float"
    }

    sample_platform_id = "myplatform_id"
    sample_platform = {
            "position": "POINT (50 80)",
            "name": "myplaform name",
            "description": "myplaform description",
            "link": "http://google.com",
            "mobile": False
    }

    sample_sensor_id = "mysensor_id"
    sample_sensor = {
        "manufacturer": "manufacturer",
        "model": "model",
        "serial_number": "serial_number",
        "name": "name",
        "description": "description"
    }

    def setUp(self):
        self.app = create_app(APP_DIR)
        self.app.config['TESTING'] = True
        self.app.system = MockSystem()
        self.client = self.app.test_client()

    def tearDown(self):
        pass


    #
    # REST api tests
    # ==============
    #

    #
    # Platform API
    #
    def test_invalid_platform(self):
        resp = self.client.get('/platforms/invalid_platform')
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    def test_invalid_sensor(self):
        resp = self.client.get('/platforms/invalid_platform/invalid_sensor')
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    def test_invalid_observation(self):
        resp = self.client.get(
            '/platforms/invalid_platform/invalid_sensor/invalid_obs')
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    def test_platform_create(self):
        resp = self.client.post('/platforms/' + self.sample_platform_id,
                data=self.sample_platform,)
        self.assertEquals(status.CREATED, resp.status_code)

    def test_platform_create_duplicate(self):
        """
        make a platform using api, then put identical one using REST and ensure
        it fails
        """
        self.app.system.create_platform(
            self.sample_platform_id, self.sample_platform)
        resp = self.client.post('/platforms/' + self.sample_platform_id,
                data=self.sample_platform,)
        self.assertEquals(status.CONFLICT, resp.status_code)

    def test_platform_delete(self):
        # put a platform...
        self.app.system.create_platform("deleteme", "DATA")

        # then try to delete it
        resp = self.client.delete('/platforms/deleteme')
        self.assertEquals(status.OK, resp.status_code)

        # and check you get a 404 if you try to access old platform
        resp = self.client.get('/platforms/deleteme')
        self.assertEquals(status.NOT_FOUND, resp.status_code)

    def test_platform_read_item(self):
        # put a platform...
        self.app.system.create_platform(
            self.sample_platform_id, self.sample_platform)

        # ask for platform in JSON
        resp = self.client.get('/platforms/' + self.sample_platform_id,
                headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        # parse the JSON
        json_data = json.loads(resp.data)
        self.assertEquals(self.sample_platform, json_data)

    def test_platform_read_list(self):
        # put a platform...
        self.app.system.create_platform(
            self.sample_platform_id, self.sample_platform)

        # ask for list of platforms in JSON
        resp = self.client.get('/platforms/',
                headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        # parse JSON data and check it is correct
        json_data = json.loads(resp.data)
        self.assertTrue(self.sample_platform_id in json_data)

    #
    # SENSOR API
    #

    def test_sensor_create(self):
        # put a platform...
        self.app.system.create_platform(
            self.sample_platform_id, self.sample_platform)

        # put a sensor
        resp = self.client.post('/platforms/' + self.sample_platform_id +
                "/" + self.sample_sensor_id, data=self.sample_sensor)
        self.assertEquals(status.CREATED, resp.status_code)

    def test_sensor_create_duplicate(self):
        """
        make a platform using api, then put identical one using REST and ensure
        it fails
        """
        self.app.system.create_platform(
            self.sample_platform_id, self.sample_platform)
        self.app.system.create_sensor(
            self.sample_platform_id, self.sample_sensor_id, self.sample_sensor)
        resp = self.client.post('/platforms/' +
                self.sample_platform_id + "/" + self.sample_sensor_id,
                data=self.sample_sensor,)
        self.assertEquals(status.CONFLICT, resp.status_code)

    def test_sensor_create_no_platform(self):
        # put a sensor on a non-existant platform - must raise error
        resp = self.client.post('/platforms/nothere/' + self.sample_sensor_id,
                data=self.sample_sensor)
        self.assertEquals(status.NOT_FOUND, resp.status_code)

    def test_sensor_read_item(self):
        # put platform and sensor...
        self.app.system.create_platform(
            self.sample_platform_id, self.sample_platform)
        self.app.system.create_sensor(
            self.sample_platform_id, self.sample_sensor_id, self.sample_sensor)

        resp = self.client.get('/platforms/' +
                self.sample_platform_id + '/' + self.sample_sensor_id,
                headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        # parse JSON data and check it is correct
        json_data = json.loads(resp.data)
        self.assertEquals(0, cmp(self.sample_sensor, json_data))

    def test_sensor_read_list(self):
        pass

    def test_sensor_delete(self):
        # register a platform and sensor
        self.app.system.create_platform(
            self.sample_platform_id, self.sample_platform)
        self.app.system.create_sensor(
            self.sample_platform_id, self.sample_sensor_id, self.sample_sensor)

        # delete it
        resp = self.client.delete('/platforms/' +
                self.sample_platform_id + '/' + self.sample_sensor_id)
        self.assertEquals(status.OK, resp.status_code)

        # check get now gives not found
        resp = self.client.get('/platforms/' +
                self.sample_platform_id + '/' + self.sample_sensor_id)
        self.assertEquals(status.NOT_FOUND, resp.status_code)

        # check platform wasn't accidentally deleted
        resp = self.client.get('/platforms/' + self.sample_platform_id)
        self.assertEquals(status.OK, resp.status_code)


    #
    # PARAMETER API
    #
    def test_parameter_create(self):
        resp = self.client.post('/parameters/' + self.sample_parameter_id,
                data=self.sample_sensor)
        self.assertEquals(status.CREATED, resp.status_code)

    def test_parameter_create_duplicate(self):
        """
        make a parameter using api, then put identical one using REST and
        ensure it fails
        """
        self.app.system.create_parameter(
            self.sample_parameter_id, self.sample_parameter)
        resp = self.client.post('/parameters/' + self.sample_parameter_id,
                data=self.sample_parameter)
        self.assertEquals(status.CONFLICT, resp.status_code)

    def test_parameter_read_list(self):
        self.app.system.create_parameter(
            self.sample_parameter_id, self.sample_parameter)
        resp = self.client.get('/parameters/',
                headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        json_data = json.loads(resp.data)
        self.assertTrue(self.sample_parameter_id in json_data)

    def test_parameter_read_item(self):
        self.app.system.create_parameter(
            self.sample_parameter_id, self.sample_parameter)
        resp = self.client.get('/parameters/' + self.sample_parameter_id,
                headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        # parse JSON data and check it is correct
        json_data = json.loads(resp.data)
        self.assertEquals(0, cmp(self.sample_parameter, json_data))

    def test_parameter_delete(self):
        self.app.system.create_parameter(
            self.sample_parameter_id, self.sample_parameter)

        # test delete succeeds
        resp = self.client.delete('/parameters/' + self.sample_parameter_id)
        self.assertEquals(status.OK, resp.status_code)

        # test item really deleted
        resp = self.client.get('/parameters/' + self.sample_parameter_id)
        self.assertEquals(status.NOT_FOUND, resp.status_code)


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


class TestMysqlBackend(unittest.TestCase):

    def __init__(self):
        self.system = Mysql()


if __name__ == "__main__":
    unittest.main()
