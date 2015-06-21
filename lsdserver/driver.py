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
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
#from sqlalchemy.ext.declarative import declarative_base
from lsdserver.base import Base

#Base = declarative_base()

class Platform(Base):
    __tablename__ = "platform"
    id = Column(Integer, primary_key=True)
    position = Column(String(100))
    name = Column(String(100))
    description = Column(String(100))
    link = Column(String(100))
    mobile = Column(String(100))

class Parameter(Base):
    __tablename__ = 'parameter'
    id = Column(Integer, primary_key=True)
    type = Column(String(100))

class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey("platform.id"), nullable=False)
    manufacturer = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100))
    name = Column(String(100))
    description = Column(String(100))

class LsdBackend(object):
    """
    platform fields:
        "position": "POINT (50 80)",
        "name": "myplaform name",
        "description": "myplaform description",
        "link": "http://google.com",
        "mobile": False

    parameter fields:
        "description": "description",
        "type": "float"

    sensor fields:
        "manufacturer": "manufacturer",
        "model": "model",
        "serial_number": "serial_number",
        "name": "name",
        "description": "description"
    """


    __metaclass__ = ABCMeta

    @abstractmethod
    def get_platform(self, platform_id):
        """
        Lookup a platform by id
        return dictionary of data for platform_id or false
        """
        pass

    @abstractmethod
    def get_platforms(self, limit, offset):
        pass

    @abstractmethod
    def create_platform(self, data):
        pass

    def update_platform(self, data):
        pass


    def get_sensor(self, platform_id, sensor_id):
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
