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

import flask
from lsdserver.driver import LsdBackend
from lsdserver.driver import Platform
from lsdserver.driver import Parameter
from lsdserver.driver import Sensor


#fixme!! rename to sql alchemy


class Mysql(LsdBackend):

    session = None

    def get_platform(self, platform_id):
        return self.session.query(Platform).filter(Platform.id == platform_id).first()

    def get_sensor(self, platform_id, manufacturer, model, serial_number):
        pass

    def get_platforms(self):
        return self.session.query(Platform).all()

    def create_platform(self, platform_id, data):
        pass

    def create_sensor(self, platform_id, sensor_id, data):
        pass

    def update_platform(self, data):
        pass

    def update_sensor(self, data):
        pass

    def delete_platform(self, platform_id):
        pass

    def delete_sensor(self, platform_id, sensor_id):
        pass

    def create_parameter(self, parameter_id, data):
        pass

    def get_parameter(self, parameter_id):
        pass

    def delete_parameter(self, parameter_id):
        pass

    def get_parameters(self):
        pass

    def create_phenomena(self, data):
        pass

    def get_phenomena(self, term):
        pass

    def delete_phenomena(self, term):
        pass

LsdBackend.register(Mysql)
