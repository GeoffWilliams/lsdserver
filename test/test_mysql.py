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

    platform = Platform()
    platform.id = 1
    platform.name = "platform_name"
    platform.description = "platform_description"
    platform.position = "(0,0)"
    platform.link = "http:///"
    platform.mobile = "no"
    engine = None
    db_session = None

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

        print("CREATED")
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
        self.db_session.remove()

    def demo_platform(self):
        self.db_session.add(self.platform)
        self.db_session.commit()

    def test_get_platform_empty(self):
        data = self.backend.get_platform("abc")
        self.assertEqual(data, None)

    def test_get_platform_data(self):
        self.demo_platform()
        data = self.backend.get_platform(self.platform.id)
        self.assertEqual(data.id, 1)
        self.assertEqual(data.name, "platform_name")

if __name__ == "__main__":
    unittest.main()