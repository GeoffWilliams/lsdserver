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
from flask import Flask, render_template
from lsdserver.platforms import platforms
from lsdserver.config import Config
from lsdserver import status

def create_app():
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)
    app.register_blueprint(platforms)
    app.debug = True
    file_handler = logging.FileHandler(filename='lsdserver.log')
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.system = Config.system
    # general stuff - error pages etc
    app.errorhandler(404)(not_found_error)
    app.errorhandler(500)(internal_error)
    return app


def not_found_error(error):
    return render_template('404.html'), status.NOT_FOUND


def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), status.SERVER_ERROR






