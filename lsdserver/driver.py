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

from abc import ABCMeta, abstractmethod


class LsdBackend(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_platform(self, platform_id):
        pass

    @abstractmethod
    def get_sensor(self, platform_id, sensor_id):
        pass

    @abstractmethod
    def get_platforms(self):
        pass

    @abstractmethod
    def create_platform(self, platform_id, data):
        pass

    @abstractmethod
    def create_sensor(self, platform_id, sensor_id, data):
        pass

    @abstractmethod
    def delete_platform(self, platform_id):
        pass

    @abstractmethod
    def delete_sensor(self, platform_id, sensor_id):
        pass

    @abstractmethod
    def create_parameter(self, parameter_id, data):
        pass

    @abstractmethod
    def get_parameter(self, parameter_id):
        pass

    @abstractmethod
    def delete_parameter(self, parameter_id):
        pass

    @abstractmethod
    def get_parameters(self):
        pass
