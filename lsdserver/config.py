from lsdserver.backend import mysql


class Config:
    system = mysql.Mysql()
