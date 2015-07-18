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

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref
#from sqlalchemy.ext.declarative import declarative_base
from lsdserver.base import Base

#fixme!! rename to sql alchemy

FIELD_LENGTH = 255

class Platform(Base):
    __tablename__ = "platform"
    platform_id = Column(String(FIELD_LENGTH), primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    info = Column(String(100))
    location = Column(String(100))

class Sensor(Base):
    __tablename__ = 'sensor'
    platform_id = Column(String(FIELD_LENGTH), ForeignKey("platform.platform_id"), primary_key=True)
    manufacturer = Column(String(FIELD_LENGTH), primary_key=True)
    model = Column(String(FIELD_LENGTH), primary_key=True)
    serial_number = Column(String(FIELD_LENGTH), primary_key=True)
    description = Column(String(100))
    info = Column(String(100))


class Parameter(Base):
    __tablename__ = 'parameter'
    platform_id = Column(String(FIELD_LENGTH), primary_key=True)
    manufacturer = Column(String(FIELD_LENGTH),primary_key=True)
    model = Column(String(FIELD_LENGTH), primary_key=True)
    serial_number = Column(String(FIELD_LENGTH), primary_key=True)
    phenomena = Column(String(100))
    __table_args__ = (ForeignKeyConstraint([platform_id, manufacturer, model, serial_number],
                                           [Sensor.platform_id, Sensor.manufacturer, Sensor.model, Sensor.serial_number]),
                      {})


class Mysql(LsdBackend):

    session = None

    def get_platform(self, platform_id):
        obj = self.session.query(Platform).filter(Platform.platform_id == platform_id).first()
        if obj:
            json = obj.__dict__
        else:
            json = None
        return json

    def get_sensor(self, platform_id, manufacturer, model, serial_number):
        obj = self.session.query(Sensor).filter(
            Sensor.platform_id == platform_id,
            Sensor.manufacturer == manufacturer,
            Sensor.model == model,
            Sensor.serial_number == serial_number).first()
        if obj:
            json = obj.__dict__
        else:
            json = None
        return json

    def get_platforms(self):
        data = self.session.query(Platform).all()
        result = []
        for row in data:
            result.append(row.__dict__)
        return result


    def create_platform(self, platform_dict):
        platform = Platform()
        platform.platform_id = platform_dict["platform_id"]
        platform.name = platform_dict["name"]
        platform.description = platform_dict["description"]
        platform.info = platform_dict["info"]
        platform.location = platform_dict["location"]
        self.session.add(platform)
        self.session.commit()

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

    def create_flag(self, data):
        pass

    def get_flag(self, term):
        pass

    def delete_flag(self, term):
        pass

    def get_sensors(self, platform_id=None, manufacturer=None, model=None):
        pass

    def get_parameters(self, platform_id=None, manufacturer=None, model=None, serial_number=None):
        pass

    def get_flags(self):
        pass

    def get_phenomenas(self):
        pass


LsdBackend.register(Mysql)
