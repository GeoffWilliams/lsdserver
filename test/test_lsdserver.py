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
sys.path.append("..")
import unittest
import lsdserver
import tempfile
from lsdserver import create_app
from lsdserver import status
from lsdserver.config import Config
import flask
from flask import render_template, current_app
import json
import logging


class MockSystem():
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


class TestRestApi(unittest.TestCase):
    """Unit tests for lsdserver."""
    app = None
    client = None

    sample_parameter_id = "temperature"
    sample_parameter = dict(
        description="description",
        type="float"
    )

    sample_platform_id = "myplatform_id"
    sample_platform = dict(
            longitude="50",
            latitude="80",
            srs="epsg:4326",
            name="myplaform name",
            description="myplaform description",
            link="http://google.com",
            mobile=False
    )

    sample_sensor_id = "mysensor_id"
    sample_sensor = dict(
        manufacturer="manufacturer",
        model="model",
        serial_number="serial_number",
        name="name",
        description="description"
    )

    def setUp(self):
        print("RESET")
        Config.system = MockSystem()
        #print(len(Config.system.platforms))
        #print(len(Config.system.parameters))
        #print(len(Config.system.sensors))

        self.app = create_app()
        self.app.config['TESTING'] = True
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
        resp = self.client.get('/repository/invalid_platform')
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    def test_invalid_sensor(self):
        resp = self.client.get('/repository/invalid_platform/invalid_sensor')
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    def test_invalid_observation(self):
        resp = self.client.get(
            '/repository/invalid_platform/invalid_sensor/invalid_obs')
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    def test_platform_create(self):
        resp = self.client.post('/repository/' + self.sample_platform_id,
                data=self.sample_platform,)
        self.assertEquals(status.CREATED, resp.status_code)

    def test_platform_create_duplicate(self):
        """
        make a platform using api, then put identical one using REST and ensure
        it fails
        """
        Config.system.create_platform(
            self.sample_platform_id, self.sample_platform)
        resp = self.client.post('/repository/' + self.sample_platform_id,
                data=self.sample_platform,)
        self.assertEquals(status.CONFLICT, resp.status_code)

    def test_platform_delete(self):
        # put a platform...
        Config.system.create_platform("deleteme", "DATA")

        # then try to delete it
        resp = self.client.delete('/repository/deleteme')
        self.assertEquals(status.OK, resp.status_code)

        # and check you get a 404 if you try to access old platform
        resp = self.client.get('/repository/deleteme')
        self.assertEquals(status.NOT_FOUND, resp.status_code)

    def test_platform_read_item(self):
        # put a platform...
        Config.system.create_platform(
            self.sample_platform_id, self.sample_platform)

        # ask for platform in JSON
        resp = self.client.get('/repository/' + self.sample_platform_id,
                headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        # parse the JSON
        json_data = json.loads(resp.data)
        self.assertEquals(self.sample_platform, json_data)

    def test_platform_read_list(self):
        # put a platform...
        Config.system.create_platform(
            self.sample_platform_id, self.sample_platform)

        # ask for list of platforms in JSON
        resp = self.client.get('/repository/',
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
        Config.system.create_platform(
            self.sample_platform_id, self.sample_platform)

        # put a sensor
        resp = self.client.post('/repository/' + self.sample_platform_id +
                "/" + self.sample_sensor_id, data=self.sample_sensor)
        self.assertEquals(status.CREATED, resp.status_code)

    def test_sensor_create_duplicate(self):
        """
        make a platform using api, then put identical one using REST and ensure
        it fails
        """
        Config.system.create_platform(
            self.sample_platform_id, self.sample_platform)
        Config.system.create_sensor(
            self.sample_platform_id, self.sample_sensor_id, self.sample_sensor)
        resp = self.client.post('/repository/' +
                self.sample_platform_id + "/" + self.sample_sensor_id,
                data=self.sample_sensor,)
        self.assertEquals(status.CONFLICT, resp.status_code)

    def test_sensor_create_no_platform(self):
        # put a sensor on a non-existant platform - must raise error
        resp = self.client.post('/repository/nothere/' + self.sample_sensor_id,
                data=self.sample_sensor)
        self.assertEquals(status.NOT_FOUND, resp.status_code)

    def test_sensor_read_item(self):
        # put platform and sensor...
        Config.system.create_platform(
            self.sample_platform_id, self.sample_platform)
        Config.system.create_sensor(
            self.sample_platform_id, self.sample_sensor_id, self.sample_sensor)

        resp = self.client.get('/repository/' +
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
        Config.system.create_platform(
            self.sample_platform_id, self.sample_platform)
        Config.system.create_sensor(
            self.sample_platform_id, self.sample_sensor_id, self.sample_sensor)

        # delete it
        resp = self.client.delete('/repository/' +
                self.sample_platform_id + '/' + self.sample_sensor_id)
        self.assertEquals(status.OK, resp.status_code)

        # check get now gives not found
        resp = self.client.get('/repository/' +
                self.sample_platform_id + '/' + self.sample_sensor_id)
        self.assertEquals(status.NOT_FOUND, resp.status_code)

        # check platform wasn't accidentally deleted
        resp = self.client.get('/repository/' + self.sample_platform_id)
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
        Config.system.create_parameter(
            self.sample_parameter_id, self.sample_parameter)
        resp = self.client.post('/parameters/' + self.sample_parameter_id,
                data=self.sample_parameter)
        self.assertEquals(status.CONFLICT, resp.status_code)

    def test_parameter_read_list(self):
        Config.system.create_parameter(
            self.sample_parameter_id, self.sample_parameter)
        resp = self.client.get('/parameters/',
                headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        json_data = json.loads(resp.data)
        self.assertTrue(self.sample_parameter_id in json_data)

    def test_parameter_read_item(self):
        Config.system.create_parameter(
            self.sample_parameter_id, self.sample_parameter)
        resp = self.client.get('/parameters/' + self.sample_parameter_id,
                headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        # parse JSON data and check it is correct
        json_data = json.loads(resp.data)
        self.assertEquals(0, cmp(self.sample_parameter, json_data))

    def test_parameter_delete(self):
        Config.system.create_parameter(
            self.sample_parameter_id, self.sample_parameter)

        # test delete succeeds
        resp = self.client.delete('/parameters/' + self.sample_parameter_id)
        self.assertEquals(status.OK, resp.status_code)

        # test item really deleted
        resp = self.client.get('/parameters/' + self.sample_parameter_id)
        self.assertEquals(status.NOT_FOUND, resp.status_code)


if __name__ == "__main__":
    unittest.main()

