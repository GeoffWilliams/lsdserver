# -*- coding: utf-8 -*-
# mysql driver tests
import unittest
import sys
import os
APP_DIR = os.path.dirname(__file__) + "/.."
sys.path.append(APP_DIR)
from lsdserver.backend.mysql import Mysql
import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
#from lsdserver.driver import Platform
from lsdserver.base import Base
from lsdserver.driver import Parameter
from lsdserver.driver import Sensor
from lsdserver.driver import Platform


class TestMysql(unittest.TestCase):

    backend = Mysql()
    db_host = "localhost"
    db_name = "lsdserver_test"
    db_super_user = "root"
    db_user = "lsdserver_test"
    db_service_name = "mysql"
    db_url = "mysql:///" + db_name

    def demo_platform_obj(self):
        platform = Platform()
        platform.id = 1
        platform.name = "platform_name"
        platform.description = "platform_description"
        platform.position = "(0,0)"
        platform.link = "http:///"
        platform.mobile = "no"
        return platform

    def demo_parameter_obj(self):
        parameter = Parameter()
        parameter.id = 2
        parameter.description = "paramter_description"
        parameter.type = "parameter_type"
        return parameter



    engine = None
    db_session = None

    def demo_sensor_obj(self):
        sensor = Sensor()
        sensor.id = 3
        sensor.manufacturer = "manufacturer"
        sensor.model = "model"
        sensor.serial_number = "serial_number"
        sensor.name = "name"
        sensor.description = "description"
        return sensor

    @classmethod
    def setUpClass(cls):
        cls.run_sql("DROP DATABASE IF EXISTS " + cls.db_name)
        cls.run_sql("CREATE DATABASE " + cls.db_name)


    def setUp(self):
        self.create_db()
        self.backend.session = self.db_session

    def tearDown(self):
        self.drop_db()

    @classmethod
    def run_sql(cls, sql):
        db = MySQLdb.connect(host=cls.db_host, db=cls.db_service_name,
            read_default_file="~/.my.cnf")
        cursor = db.cursor()
        cursor.execute(sql)

    def create_db(self):

        #print("CREATED")
        myDB = URL(drivername='mysql', host=self.db_host,
                database=self.db_name,
                query={'read_default_file': '~/.my.cnf'}
        )

        self.engine = create_engine(name_or_url=myDB)
        Base.metadata.create_all(self.engine)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=self.engine))

    def drop_db(self):
        self.db_session.query(Platform).delete()
        self.db_session.query(Parameter).delete()
        self.db_session.query(Sensor).delete()
        self.db_session.commit()
        self.db_session.remove()

    def demo_platform(self):
        platform = self.demo_platform_obj()
        self.db_session.add(platform)
        self.db_session.commit()
        return platform

    def demo_sensor(self):
        sensor = self.demo_sensor_obj()
        self.db.session.add(sensor)
        self.db.session.commit()
        return sensor

    def demo_parameter(self):
        parameter = self.demo_parameter_obj()
        self.db.session.add(parameter)
        self.db.session.commit()
        return parameter

    #
    # get_platform()
    #

    def test_get_platform_empty(self):
        """get_platform() when no data loaded"""
        data = self.backend.get_platform("abc")
        self.assertEqual(data, None)

    def test_get_platform_data(self):
        """get_platform() when data loaded"""
        platform = self.demo_platform()
        data = self.backend.get_platform(platform.id)
        self.assertEqual(data.id, platform.id)
        self.assertEqual(data.name, platform.name)
        self.assertEqual(data.description, platform.description)
        self.assertEqual(data.position, platform.position)
        self.assertEqual(data.link, platform.link)
        self.assertEqual(data.mobile, platform.mobile)

    #
    # get_platforms()
    #

    def test_get_platforms_empty(self):
        """ get_platforms() with no data loaded"""
        data = self.backend.get_platforms()
        self.assertEqual(len(data), 0)

    def test_get_platforms_data(self):
        """ get_platforms() with data loaded """
        self.demo_platform()
        data = self.backend.get_platforms()
        self.assertEqual(len(data), 1)

    #
    # get_sensor()
    #
    def test_get_sensor_no_data(self):
        """ get_sensor() with no data loaded """
        data = self.backend.get_sensor("abc")
        self.assertEqual(len(data), 0)

    def test_get_sensor_data(self):
        """ get_sensor() with data loaded"""
        sensor = self.demo_sensor()
        data = self.backend.get_sensor(sensor.id)
        self.assertTrue(data)
        self.assertEqual(data.id, sensor.id)
        self.assertEqual(data.manufacturer, sensor.manufacturer)
        self.assertEqual(data.model, sensor.model)
        self.assertEqual(data.serial_number, sensor.serial_number)
        self.assertEqual(data.name, sensor.name)
        self.assertEqual(data.description, sensor.description)
    #
    # create_platform()
    #

    def test_create_platform(self):
        pass

    def test_create_platform_dup(self):
        pass

    #
    # create_sensor()
    #
    def test_create_sensor(self):
        pass

    def test_create_sensor_dup(self):
        pass

    #
    # delete_platform()
    #
    def test_delete_platform_missing(self):
        pass

    def test_delete_platform(self):
        pass

    #
    # delete_sensor()
    #
    def test_delete_sensor_missing(self):
        pass

    def test_delete_sensor(self):
        pass

    #
    # create_parameter()
    #
    def test_create_parameter(self):
        pass

    def test_create_parameter_dup(self):
        pass

    #
    # get_parameter()
    #
    def test_get_parameter_no_data(self):
        """ get_sensor() with no data loaded """
        pass

    def test_get_parameter_data(self):
        """ get_sensor() with data loaded"""
        pass


    #
    # delete_parameter()
    #
    def test_delete_parameter_missing(self):
        pass

    def test_delete_parameter(self):
        pass

    #
    # get_parameters()
    #
    def test_get_parameters_no_data(self):
        """ get_parameters() with no data loaded """
        pass

    def test_get_parameters_data(self):
        """ get_parameters() with data loaded"""
        pass


if __name__ == "__main__":
    unittest.main()