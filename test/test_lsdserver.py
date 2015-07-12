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
APP_DIR = os.path.dirname(os.path.realpath(__file__)) + "/.."
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
import urllib
from lsdserver.backend.mysql import Mysql
from lsdserver.driver import LsdBackend
from sample_data import SampleData
from support import MockSystem



LsdBackend.register(MockSystem)


class TestRestApi(unittest.TestCase):
    """Unit tests for lsdserver."""
    app = None
    client = None

    def setUp(self):
        self.app = create_app(APP_DIR)
        self.app.config['TESTING'] = True
        self.app.system = MockSystem()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    """
    #
    # REST api tests
    # ==============
    #
    """

    """
    #
    # Entry point
    # /
    """
    def test_entry_point(self):
        """check for webpage at /"""
        resp = self.client.get('/')
        self.assertEqual(status.OK, resp.status_code)

    def test_version(self):
        """check data returned for version"""
        resp = self.client.get('/version/')
        self.assertEqual(status.OK, resp.status_code)
        self.assertEqual("wip", resp.data)
    """
    #
    # Platform API
    # /platform/*
    """

    """
    # Listing
    """
    def test_platform_read_list(self):
        """load a platform and ensure it shows up in the list"""
        # put a platform...
        self.app.system.create_platform(SampleData.sample_platform)

        # ask for list of platforms in JSON
        resp = self.client.get('/platform/',
                               headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        # parse JSON data and check it is correct
        json_data = json.loads(resp.data)
        self.assertTrue(SampleData.sample_platform_id in json_data)

    """
    # Create
    """
    def test_platform_create(self):
        """create a platform"""
        resp = self.client.put('/platform/' + SampleData.sample_platform_id,
                               data=json.dumps(SampleData.sample_platform),
                               content_type='application/json')
        self.assertEquals(status.CREATED, resp.status_code)

    def test_platform_create_duplicate(self):
        """
        make a platform using api, then put identical one using REST and ensure
        it fails
        """
        self.app.system.create_platform(SampleData.sample_platform)
        resp = self.client.put('/platform/' + SampleData.sample_platform_id,
                               data=json.dumps(SampleData.sample_platform),
                               content_type='application/json')
        self.assertEquals(status.CONFLICT, resp.status_code)

    """
    # Read
    """
    def test_platform_read_item(self):
        """create a platform and read it back"""
        # put a platform...
        self.app.system.create_platform(SampleData.sample_platform)

        # ask for platform in JSON
        resp = self.client.get('/platform/' + SampleData.sample_platform_id,
                               headers={'Accept': 'application/json'})
        self.assertEquals(status.OK, resp.status_code)

        # parse the JSON
        json_data = json.loads(resp.data)
        self.assertEquals(SampleData.sample_platform, json_data)

    def test_invalid_platform(self):
        """lookup a platform that doesn't exis"""
        resp = self.client.get('/platform/invalid_platform')
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    """
    # Update (not supported - do a delete followed by a PUT)
    """

    """
    # Delete
    """
    def test_platform_delete(self):
        """load a platform then delete it"""
        # put a platform...
        self.app.system.create_platform(SampleData.sample_platform)
        uri = '/platform/' + SampleData.sample_platform_id

        # then try to delete it
        resp = self.client.delete(uri)
        self.assertEquals(status.NO_CONTENT, resp.status_code)

        # and check you get a 404 if you try to access old platform
        resp = self.client.get(uri)
        self.assertEquals(status.NOT_FOUND, resp.status_code)

    """
    #
    # Platform info
    # /platform/*/info
    """

    """
    # GET
    """
    def test_get_platform_info_uri(self):
        """set some platform info then check we get redirected to uri"""

        self.app.system.create_platform(SampleData.sample_platform)

        resp = self.client.get(
            "/platform/" + SampleData.sample_platform_id + "/info")
        self.assertEquals(status.REDIRECT, resp.status_code)


#    def test_get_platform_info_file(self):
#        """set some platform info then check we get redirected to uploaded local
#        file"""
#        resp = self.client.get(
#            "/platform" + SampleData.sample_platform_id + "/info")
#        self.assertEquals(status.OK, resp.status_code)

    """
    # PUT (URL)
    """
    def test_put_platform_info_uri(self):
        """test uploading an info URI"""
        # sample URL (will redirect)
        self.app.system.create_platform(SampleData.sample_platform)

        resp = self.client.put(
            "/platform/" + SampleData.sample_platform_id + "/info",
            data=SampleData.sample_uri)
        self.assertEquals(status.CREATED, resp.status_code)

#    def test_put_platform_info_file(self):
#        """test uploading a whole file to use for /info"""
#        # upload a file (store locally and redirect to it)
#        resp = self.client.put(
#            "/platform" + SampleData.sample_platform_id + "/info",
#            buffered=True,
#            content_type='multipart/form-data',
#            data=SampleData.sample_uri)
#        self.assertEquals(status.CREATED, resp.status_code)

    """
    # DELETE
    """
    def test_delete_platform_info(self):
        """dest deleting platform info"""
        self.app.system.create_platform(SampleData.sample_platform)
        resp = self.client.delete(
            "/platform" + SampleData.sample_platform_id + "/info")
        self.assertEquals(status.NOT_FOUND, resp.status_code)

    """
    # Platform location
    # /platform/*/location
    """

    """
    # GET
    """
    def test_get_platform_location(self):
        """create a platform with a location and read back the location"""
        self.app.system.create_platform(SampleData.sample_platform)
        resp = self.client.get(
            "/platform/" + SampleData.sample_platform_id + "/location")
        self.assertEquals(status.OK, resp.status_code)
        self.assertEquals(SampleData.sample_platform["location"], resp.data)


    """
    Filtering
    /platform/?FIELD=QUERY
    """

    def test_platform_filter_platform_id(self):
        """filter platforms by ID"""
        pass

    def test_platform_filter_platform_name(self):
        """filter platforms by name"""
        pass

    def test_platform_filter_platform_description(self):
        """filter platforms by description"""
        pass

    def test_platform_filter_platform_info(self):
        """filter platforms by info"""
        pass

    def test_platform_filter_platform_location(self):
        """filter platforms by location"""
        pass

    def test_platform_filter_sensor_manufacturer(self):
        """filter platforms by sensor manufacturer"""
        pass

    def test_platform_filter_sensor_model(self):
        """filter platforms by sensor model"""
        pass

    def test_platform_filter_sensor_serial_number(self):
        """filter platforms by serial number"""
        pass

    def test_platform_filter_sensor_description(self):
        """filter platforms by sensor description"""
        pass

    def test_platform_filter_sensor_info(self):
        """filter platforms by sensor info field"""
        pass

    def test_platform_filter_parameter_phenomena(self):
        """filter platforms by phenomena"""
        pass

    """
    #
    # Sensor API
    # /sensor/*
    """

    """
    # create
    """
    def test_sensor_create(self):
        # put a platform...
        self.app.system.create_platform(SampleData.sample_platform)

        resp = self.client.put(
            '/sensor/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number,
            data=json.dumps(SampleData.sample_sensor),
            content_type='application/json')
        self.assertEquals(status.CREATED, resp.status_code)

    def test_sensor_create_invalid(self):
        """attempt to create sensor associated with platform that has not been
        created"""
        resp = self.client.put(
            '/sensor/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number,
            data=json.dumps(SampleData.sample_sensor),
            content_type='application/json')
        self.assertEquals(status.NOT_FOUND, resp.status_code)

    """
    # read
    """
    def test_sensor_read(self):
        """register a platform and sensor, then try to read the sensor"""
        self.app.system.create_platform(SampleData.sample_platform)
        self.app.system.create_sensor(SampleData.sample_sensor)

        resp = self.client.get(
            '/sensor/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number)
        json_data = json.loads(resp.data)
        self.assertEqual(status.OK, resp.status_code)
        self.assertEqual(SampleData.sample_sensor, json_data)

    def test_sensor_read_invalid(self):
        """Try reading an unregistered sensor"""
        resp = self.client.get(
            '/sensor/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number)
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    """
    # delete
    """
    def test_sensor_delete(self):
        """register a platform and sensor, then try to delete the sensor"""
        self.app.system.create_platform(SampleData.sample_platform)
        self.app.system.create_sensor(SampleData.sample_sensor)

        resp = self.client.delete(
            '/sensor/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number)
        self.assertEqual(status.NO_CONTENT, resp.status_code)

    def test_sensor_delete_invalid(self):
        """attempt to delete an unregistered sensor"""
        resp = self.client.delete(
            '/sensor/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number)
        self.assertEqual(status.NOT_FOUND, resp.status_code)
    """
    # info
    # /sensor/*/info
    """
    def test_sensor_info_read(self):
        """register a platform and sensor, then try to read the sensor info"""
        self.app.system.create_platform(SampleData.sample_platform)
        self.app.system.create_sensor(SampleData.sample_sensor)

        resp = self.client.get(
            '/sensor/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number +
            "/info")

        self.assertEqual(SampleData.sample_sensor["info"], resp.location)
        self.assertEqual(status.REDIRECT, resp.status_code)


    def test_sensor_info_write(self):
       # sample URL (will redirect)
        self.app.system.create_platform(SampleData.sample_platform)
        self.app.system.create_sensor(SampleData.sample_sensor)

        resp = self.client.put(
            '/sensor/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number +
            "/info",
            data=SampleData.sample_uri)
        self.assertEqual(status.CREATED, resp.status_code)

    """
    #
    # Parameter API
    # /parameter
    """

    """
    # Create
    """
    def test_create_parameter(self):
        """create a parameter"""
        self.app.system.create_platform(SampleData.sample_platform)
        self.app.system.create_sensor(SampleData.sample_sensor)

        resp = self.client.put(
            '/parameter/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number + "/" +
            urllib.quote_plus(SampleData.sample_parameter_phenomena),
            data=json.dumps(SampleData.sample_parameter),
            content_type='application/json')
        self.assertEquals(status.CREATED, resp.status_code)


    def test_create_parameter_invalid(self):
        """attempt to create an invalid parameter"""
        resp = self.client.put(
            '/parameter/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number + "/" +
            urllib.quote_plus(SampleData.sample_parameter_phenomena),
            data=json.dumps(SampleData.sample_parameter),
            content_type='application/json')
        self.assertEquals(status.NOT_FOUND, resp.status_code)

    """
    # Read
    """
    def test_read_parameter(self):
        """read a valid parameter"""
        self.app.system.create_platform(SampleData.sample_platform)
        self.app.system.create_sensor(SampleData.sample_sensor)
        self.app.system.create_parameter(SampleData.sample_parameter)
        resp = self.client.get(
            '/parameter/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number + "/" +
            urllib.quote_plus(SampleData.sample_parameter_phenomena))

        json_data = json.loads(resp.data)
        self.assertEqual(status.OK, resp.status_code)
        self.assertEqual(SampleData.sample_parameter, json_data)

    def test_read_parameter_invalid(self):
        """read an invalid parameter"""
        resp = self.client.get(
            '/parameter/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number + "/" +
            urllib.quote_plus(SampleData.sample_parameter_phenomena))
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    """
    # Delete
    """
    def test_delete_parameter(self):
        """delete a parameter"""
        self.app.system.create_platform(SampleData.sample_platform)
        self.app.system.create_sensor(SampleData.sample_sensor)
        self.app.system.create_parameter(SampleData.sample_parameter)
        resp = self.client.delete(
            '/parameter/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number + "/" +
            urllib.quote_plus(SampleData.sample_parameter_phenomena))

        self.assertEqual(status.NO_CONTENT, resp.status_code)

    def test_delete_parameter_invalid(self):
        """attempt to delte an invalid parameter"""
        resp = self.client.delete(
            '/parameter/' + SampleData.sample_platform_id + "/" +
            SampleData.sample_sensor_manufacturer + "/" +
            SampleData.sample_sensor_model + "/" +
            SampleData.sample_sensor_serial_number + "/" +
            urllib.quote_plus(SampleData.sample_parameter_phenomena))

        self.assertEqual(status.NOT_FOUND, resp.status_code)

    """
    #
    # Phenomena API
    # /phenomena
    #
    """

    def test_list_phenomena(self):
        """list all phenomena"""
        pass

    """
    Create
    """
    def test_create_phenomena(self):
        """create a phenomena"""
        resp = self.client.put(
            '/phenomena/' + urllib.quote_plus(SampleData.sample_phenomena_term),
            data=json.dumps(SampleData.sample_parameter),
            content_type='application/json')

        self.assertEqual(status.CREATED, resp.status_code)


    def test_create_phenomena_invalid(self):
        """attempt to create an invalid phenomena"""
        pass

    """
    Read
    """
    def test_read_phenomena(self):
        """read a phenomena by id"""
        self.app.system.create_phenomena(SampleData.sample_phenomena)

        resp = self.client.get(
            '/phenomena/' + urllib.quote_plus(SampleData.sample_phenomena_term))

        json_data = json.loads(resp.data)
        self.assertEqual(status.OK, resp.status_code)
        self.assertEqual(SampleData.sample_phenomena, json_data)

    def test_read_phenomena_invalid(self):
        """attempt to read invalid phenomena"""
        resp = self.client.get(
            '/phenomena/' + urllib.quote_plus(SampleData.sample_phenomena_term))

        self.assertEqual(status.NOT_FOUND, resp.status_code)

    """
    Delete
    """
    def test_delete_phenomena(self):
        """delete a phenomena"""
        self.app.system.create_phenomena(SampleData.sample_phenomena)
        resp = self.client.delete(
            '/phenomena/' + urllib.quote_plus(SampleData.sample_phenomena_term))

        self.assertEqual(status.NO_CONTENT, resp.status_code)

    def test_delete_phenomena_invalid(self):
        """attempt to delete an invalid phenomena"""
        resp = self.client.delete(
            '/phenomena/' + urllib.quote_plus(SampleData.sample_phenomena_term))

        self.assertEqual(status.NOT_FOUND, resp.status_code)

    """
    # Flag API
    # /flag
    """

    """
    List
    """
    def test_list_flags(self):
        pass

    """
    Create
    """
    def test_flag_create(self):
        resp = self.client.put(
            '/flag/' + urllib.quote_plus(SampleData.sample_flag_term),
            data=json.dumps(SampleData.sample_flag),
            content_type='application/json')

        self.assertEqual(status.CREATED, resp.status_code)

    def test_flag_create_invalid(self):
        pass

    """
    Read
    """
    def test_flag_read(self):
        self.app.system.create_flag(SampleData.sample_flag)

        resp = self.client.get(
            '/flag/' + urllib.quote_plus(SampleData.sample_flag_term))

        json_data = json.loads(resp.data)
        self.assertEqual(status.OK, resp.status_code)
        self.assertEqual(SampleData.sample_flag, json_data)

    def test_flag_read_invalid(self):
        resp = self.client.get(
            '/flag/' + urllib.quote_plus(SampleData.sample_flag_term))

        self.assertEqual(status.NOT_FOUND, resp.status_code)

    """
    Delete
    """
    def test_flag_delete(self):
        self.app.system.create_flag(SampleData.sample_flag)
        resp = self.client.delete(
            '/flag/' + urllib.quote_plus(SampleData.sample_flag_term))

        self.assertEqual(status.NO_CONTENT, resp.status_code)

    def test_flag_delete_invalid(self):
        resp = self.client.delete(
            '/flag/' + urllib.quote_plus(SampleData.sample_flag_term))

        self.assertEqual(status.NOT_FOUND, resp.status_code)

    """
    #
    # Observation API
    # /observation
    """

    """
    Create
    """
    def test_create_observation(self):
        pass

    def test_create_observation_invalid(self):
        pass

    """
    Read
    """
    def test_read_observation(self):
        pass

    def test_read_observation_invalid(self):
        pass

    """
    Delete
    """
    def test_delete_observation(self):
        pass

    def test_delete_observation_invalid(self):
        pass

    """
    Platform observations - latest
    """
    def test_platform_latest_observation(self):
        pass

    """
    Sensor observations - latest
    """
    def test_sensor_latest_observation(self):
        pass







    #
    # SENSOR API
    #

##    def test_sensor_create(self):
        ## put a platform...
        #self.app.system.create_platform(
            #SampleData.sample_platform_id, SampleData.sample_platform)

##        # put a sensor
        #resp = self.client.post('/platform/' + SampleData.sample_platform_id +
                #"/" + SampleData.sample_sensor_id, data=SampleData.sample_sensor)
        #self.assertEquals(status.CREATED, resp.status_code)

##    def test_sensor_create_duplicate(self):
        #"""
        #make a platform using api, then put identical one using REST and ensure
        #it fails
        #"""
        #self.app.system.create_platform(
            #SampleData.sample_platform_id, SampleData.sample_platform)
        #self.app.system.create_sensor(
            #SampleData.sample_platform_id, SampleData.sample_sensor_id, SampleData.sample_sensor)
        #resp = self.client.post('/platform/' +
                #SampleData.sample_platform_id + "/" + SampleData.sample_sensor_id,
                #data=SampleData.sample_sensor,)
        #self.assertEquals(status.CONFLICT, resp.status_code)

##    def test_sensor_create_no_platform(self):
        ## put a sensor on a non-existant platform - must raise error
        #resp = self.client.post('/platform/nothere/' + SampleData.sample_sensor_id,
                #data=SampleData.sample_sensor)
        #self.assertEquals(status.NOT_FOUND, resp.status_code)

##    def test_sensor_read_item(self):
        ## put platform and sensor...
        #self.app.system.create_platform(
            #SampleData.sample_platform_id, SampleData.sample_platform)
        #self.app.system.create_sensor(
            #SampleData.sample_platform_id, SampleData.sample_sensor_id, SampleData.sample_sensor)

##        resp = self.client.get('/platform/' +
                #SampleData.sample_platform_id + '/' + SampleData.sample_sensor_id,
                #headers={'Accept': 'application/json'})
        #self.assertEquals(status.OK, resp.status_code)

##        # parse JSON data and check it is correct
        #json_data = json.loads(resp.data)
        #self.assertEquals(0, cmp(SampleData.sample_sensor, json_data))

##    def test_sensor_read_list(self):
        #pass

# #   def test_sensor_delete(self):
        ## register a platform and sensor
        #self.app.system.create_platform(
            #SampleData.sample_platform_id, SampleData.sample_platform)
        #self.app.system.create_sensor(
            #SampleData.sample_platform_id, SampleData.sample_sensor_id, SampleData.sample_sensor)

##        # delete it
        #resp = self.client.delete('/platform/' +
                #SampleData.sample_platform_id + '/' + SampleData.sample_sensor_id)
        #self.assertEquals(status.OK, resp.status_code)

##        # check get now gives not found
        #resp = self.client.get('/platform/' +
                #SampleData.sample_platform_id + '/' + SampleData.sample_sensor_id)
        #self.assertEquals(status.NOT_FOUND, resp.status_code)

##        # check platform wasn't accidentally deleted
        #resp = self.client.get('/platform/' + SampleData.sample_platform_id)
        #self.assertEquals(status.OK, resp.status_code)

#
    #
    # PARAMETER API
    #
    #def test_parameter_create(self):
        #resp = self.client.post('/parameter/' + SampleData.sample_parameter_id,
                #data=SampleData.sample_sensor)
        #self.assertEquals(status.CREATED, resp.status_code)

##    def test_parameter_create_duplicate(self):
        #"""
        #make a parameter using api, then put identical one using REST and
        #ensure it fails
        #"""
        #self.app.system.create_parameter(
            #SampleData.sample_parameter_id, SampleData.sample_parameter)
        #resp = self.client.post('/parameter/' + SampleData.sample_parameter_id,
                #data=SampleData.sample_parameter)
        #self.assertEquals(status.CONFLICT, resp.status_code)

##    def test_parameter_read_list(self):
        #self.app.system.create_parameter(
            #SampleData.sample_parameter_id, SampleData.sample_parameter)
        #resp = self.client.get('/parameter/',
                #headers={'Accept': 'application/json'})
        #self.assertEquals(status.OK, resp.status_code)

##        json_data = json.loads(resp.data)
        #self.assertTrue(SampleData.sample_parameter_id in json_data)

##    def test_parameter_read_item(self):
        #self.app.system.create_parameter(
            #SampleData.sample_parameter_id, SampleData.sample_parameter)
        #resp = self.client.get('/parameter/' + SampleData.sample_parameter_id,
                #headers={'Accept': 'application/json'})
        #self.assertEquals(status.OK, resp.status_code)

##        # parse JSON data and check it is correct
        #json_data = json.loads(resp.data)
        #self.assertEquals(0, cmp(SampleData.sample_parameter, json_data))

##    def test_parameter_delete(self):
        #self.app.system.create_parameter(
            #SampleData.sample_parameter_id, SampleData.sample_parameter)

##        # test delete succeeds
        #resp = self.client.delete('/parameter/' + SampleData.sample_parameter_id)
        #self.assertEquals(status.OK, resp.status_code)

##        # test item really deleted
        #resp = self.client.get('/parameter/' + SampleData.sample_parameter_id)
        #self.assertEquals(status.NOT_FOUND, resp.status_code)

##


if __name__ == "__main__":
    unittest.main()
