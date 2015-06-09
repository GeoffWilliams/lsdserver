# strange python workaround to make a kind-of-singleton
# from http://stackoverflow.com/questions/7478403/sqlalchemy-classes-across-files
# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()