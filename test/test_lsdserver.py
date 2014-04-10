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

class MockSystem():

    def hello(self):
        return "hello mock"


class TestRestApi(unittest.TestCase):
    """Unit tests for lsdserver."""
    app = None
    client = None

    def setUp(self):
        #print("setup tests")
        Config.system = MockSystem()
        #self.db_fd, lsdserver.app.config['DATABASE'] = tempfile.mkstemp()
       # lsdserver.app.config['TESTING'] = True

        self.app = create_app()
        self.client = self.app.test_client()
#        lsdserver.init_db()

    def tearDown(self):
#        db.session.remove()
#        db.drop_all()
       # os.unlink(lsdserver.app.config['DATABASE'])
        pass

    #def test_empty_db(self):
        #rv = self.client.get('/')
        #assert 'Hello' in rv.data


    #
    # REST api tests
    #
    def testInvalidOperation(self):
        resp = self.client.get('/testInvalidOperation')
        print(resp.data)
        #self.assertEqual(status.NOT_FOUND,resp.status_code)
        pass

    def testPlatformCreate(self):
        resp = self.client.post('/mir', data=dict(
            identifier="abc123",
            longitude="0",
            latitude="0",
            srs="epsg:4326",
            name="abc plaform",
            description="abc test plaform",
            link="http://google.com"
        ))
        self.assertEquals(status.CREATED, resp.status_code)

    def testPlatformRead(self):
        pass

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

