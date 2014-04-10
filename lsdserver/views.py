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

import json
#from lsdserver import app
#app.logger.debug("**** inside view.py ****")
from flask import render_template, current_app
from lsdserver import status
from lsdserver.config import system


#@app.route('/')
#def index():
    #"""
    #Main entry point
    #"""
    #system.hello()
    #return render_template('index.html')


#@app.route('/platforms', methods=['POST'])
#def platformsList():
    #return render_template('platforms.html'), status.CREATED


#@app.route('/platforms', methods=['GET'])
#def platformsItem():
    #return render_template('platforms.html'), status.CREATED


#@app.route('/platforms', methods=['GET'])
#def platformsCreate():
    #return render_template('platforms.html'), status.CREATED


#@app.route('/platforms', methods=['DELETE'])
#def platformsDelete():
    #return render_template('platforms.html'), status.CREATED

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), status.NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), status.SERVER_ERROR
