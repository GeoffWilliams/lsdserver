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


import logging
import os
from flask import Flask, render_template
from lsdserver.platform import platform
from lsdserver.parameter import parameter
from lsdserver.version import version
from lsdserver.sensor import sensor
from lsdserver.phenomena import phenomena
from lsdserver.flag import flag
from lsdserver.ui import ui
from lsdserver import status
from flask.ext.sqlalchemy import SQLAlchemy
from lsdserver.backend import mysql



# https://pythonhosted.org/Flask-Uploads/

def load_config(app, name, app_dir):
    """
    Read a config file from a well-known location
    """
    app.debug = True
    config_file = name + ".cfg"
    app.logger.info("app_name:%s; app_dir:%s;" % (name, app_dir))

    # /etc/NAME.cfg
    etc_config_file = "/etc/" + config_file
    rel_config_file = app_dir + "/" + config_file

    if os.path.isfile(etc_config_file):
        f = etc_config_file
    elif os.path.isfile(rel_config_file):
        f = rel_config_file
    else:
        f = False
        app.logger.warn("No %s found!" % config_file)

    if f:
        app.logger.info("config file: %s" % f)
        app.config.from_pyfile(f)

        if app.config["LOGDIR"]:
            logfile = app.config["LOGDIR"] + "/lsdserver.log"
            app.logger.info("logging to %s" % logfile)
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel(logging.DEBUG)
            app.logger.addHandler(file_handler)

def create_app(app_dir):
    app = Flask(__name__)
    load_config(app, __name__, app_dir)

    app.register_blueprint(version, url_prefix='/version')
    app.register_blueprint(platform, url_prefix='/platform')
    app.register_blueprint(parameter, url_prefix='/parameter')
    app.register_blueprint(sensor, url_prefix='/sensor')
    app.register_blueprint(phenomena, url_prefix='/phenomena')
    app.register_blueprint(flag, url_prefix='/flag')
    app.register_blueprint(ui, url_prefix="")

    # database
    app.system = mysql.Mysql()
    app.db = SQLAlchemy(app)
    app.system.session = app.db.session

    # general stuff - error pages etc
    app.errorhandler(404)(not_found_error)
    app.errorhandler(408)(conflict_error)
    app.errorhandler(500)(internal_error)

    return app


def not_found_error(error):
    return render_template('404.html'), status.NOT_FOUND


def conflict_error(error):
    return render_template('409.html'), status.CONFLICT


def internal_error(error):
    #app.db.session.rollback()
    return render_template('500.html'), status.SERVER_ERROR



