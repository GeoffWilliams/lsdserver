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
from lsdserver import app

class Test(unittest.TestCase):
    """Unit tests for lsdserver."""

    def setUp(self):
        #app.config['TESTING'] = True
        #app.config['CSRF_ENABLED'] = False
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        #self.app = app.test_client()
        #db.create_all()

        self.db_fd, lsdserver.app.config['DATABASE'] = tempfile.mkstemp()
        lsdserver.app.config['TESTING'] = True
        self.app = lsdserver.app.test_client()
#        lsdserver.init_db()

    def tearDown(self):
#        db.session.remove()
#        db.drop_all()
        os.unlink(lsdserver.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Hello' in rv.data

if __name__ == "__main__":
    unittest.main()

