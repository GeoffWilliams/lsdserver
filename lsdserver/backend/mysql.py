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

from sqlalchemy import Sequence, Column, DateTime, String, Integer, ForeignKey, func, ForeignKeyConstraint
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
    manufacturer = Column(String(FIELD_LENGTH), primary_key=True)
    model = Column(String(FIELD_LENGTH), primary_key=True)
    serial_number = Column(String(FIELD_LENGTH), primary_key=True)
    phenomena = Column(String(100))
    observation_link = Column(Integer, unique=True, primary_key=True)
    __table_args__ = (ForeignKeyConstraint([platform_id, manufacturer, model, serial_number],
                                           [Sensor.platform_id, Sensor.manufacturer, Sensor.model, Sensor.serial_number]),
                      {})

class ObservationLink(Base):
    __tablename__ = 'observation_link'
    observation_link_id = Column(Integer, autoincrement=True, primary_key=True)

class Observation():
    timestamp = Column(DateTime, primary_key=True)
    value = Column(Integer)


class Mysql(LsdBackend):

    session = None

    def build_observation_table(self, link):
        classname = "o_" + str(link)
        table = type(classname, (Base, Observation), {'__tablename__' : classname})
        return table

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

    def create_sensor(self, data):
        sensor = Sensor()
        sensor.platform_id = data["platform_id"]
        sensor.manufacturer = data["manufacturer"]
        sensor.model = data["model"]
        sensor.serial_number = data["serial_number"]
        sensor.description = data["description"]
        sensor.info = data["info"]
        self.session.add(sensor)
        self.session.commit()

    def update_platform(self, data):
        pass

    def update_sensor(self, data):
        pass

    def delete_platform(self, platform_id):
        platform = self.session.query(Platform).filter_by(
            platform_id=platform_id).first()
        self.session.delete(platform)
        self.session.commit()

    def delete_sensor(self, platform_id, manufacturer, model, serial_number):
        sensor = self.session.query(Sensor).filter_by(
            platform_id=platform_id,
            manufacturer=manufacturer,
            model=model,
            serial_number=serial_number).first()
        self.session.delete(sensor)
        self.session.commit()

    def create_parameter(self, data):
        # Allocate a new observation table
        observation_link = ObservationLink()
        observation_link = self.session.merge(observation_link)

        parameter = Parameter()
        parameter.platform_id = data["platform_id"]
        parameter.manufacturer = data["manufacturer"]
        parameter.model = data["model"]
        parameter.serial_number = data["serial_number"]
        parameter.phenomena = data["phenomena"]
        parameter.observation_link = observation_link.observation_link_id
        self.session.add(parameter)
        self.session.commit()

        # once committed, there should be a value in parameter.observation_link
        self.build_observation_table(
            parameter.observation_link).__table__.create(self.session.bind) #bind=engine)

    def get_parameter(self, parameter_id):
        pass

    def delete_parameter(self,
                         platform_id,
                         manufacturer,
                         model,
                         serial_number,
                         phenomena):
        parameter = self.session.query(Parameter).filter_by(
            platform_id=platform_id,
            manufacturer=manufacturer,
            model=model,
            serial_number=serial_number,
            phenomena=phenomena
            ).first()
        if parameter:
            self.session.delete(parameter)
            self.session.commit()
        else:
            print "non found"

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
        data = self.session.query(Sensor).all()
        result = []
        for row in data:
            result.append(row.__dict__)
        return result

    def get_parameters(self, platform_id=None, manufacturer=None, model=None, serial_number=None):
        data = self.session.query(Parameter).all()
        result = []
        for row in data:
            result.append(row.__dict__)
        return result

    def get_flags(self):
        pass

    def get_phenomenas(self):
        pass


LsdBackend.register(Mysql)
