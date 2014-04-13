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

class MockSystem():

    platforms = {}

    def get_platform(self, platform_id):
        data = None
        if platform_id in self.platforms:
            data = self.platforms[platform_id]
        else:
            flask.abort(status.NOT_FOUND)
        return data

    def create_platform(self, platform_id, data):
        print data
        self.platforms[platform_id] = data

    def delete_platform(self, platform_id):
        if platform_id in self.platforms:
            self.platforms[platform_id] = None

class TestRestApi(unittest.TestCase):
    """Unit tests for lsdserver."""
    app = None
    client = None
    sample_platform = dict(
            longitude="50",
            latitude="80",
            srs="epsg:4326",
            name="myplaform name",
            description="myplaform description",
            link="http://google.com"
        )

    def setUp(self):
        Config.system = MockSystem()
       # lsdserver.app.config['TESTING'] = True

        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass


    #
    # REST api tests
    #
    def test_invalid_platform(self):
        resp = self.client.get('/invalid_platform')
        print(resp.data)
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    def test_invalid_sensor(self):
        resp = self.client.get('/invalid_platform/invalid_sensor')
        print(resp.data)
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    def test_invalid_observation(self):
        resp = self.client.get('/invalid_platform/invalid_sensor/invalid_obs')
        print(resp.data)
        self.assertEqual(status.NOT_FOUND, resp.status_code)

    def test_platform_create(self):
        resp = self.client.post('/myplatform', data=self.sample_platform)
        self.assertEquals(status.CREATED, resp.status_code)

    def test_platform_delete(self):
        # put a platform...
        Config.system.create_platform("deleteme", "DATA")

        # then try to delete it
        resp = self.client.delete('/deleteme')
        self.assertEquals(status.OK, resp.status_code)

        # and check you get a 404 if you try to access old platform
        resp = self.client.get('/deleteme')
        self.assertEquals(status.NOT_FOUND, resp.status_code)

    def testPlatformRead(self):
        # put a platform...
        Config.system.create_platform("myplatform", self.sample_platform)

        resp = self.client.get('/myplatform')
        self.assertEquals(status.OK, resp.status_code)
        self.assertEquals(self.sample_platform, resp.data)

    def testPlatformReadItem(self):
        pass

    def testPlatformDelete(self):
        pass

    def testSensorCreate(self):
        pass

    def testSensorRead(self):
        pass

    def testSensorReadItem(self):
        pass

    def testSensorDelete(self):
        pass

    def testPhenomenaCreate(self):
        pass

    def testPhenomenaRead(self):
        pass

    def testPhenomenaDelete(self):
        pass



if __name__ == "__main__":
    unittest.main()

