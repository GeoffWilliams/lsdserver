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
from flask import Blueprint, render_template, abort, request, current_app, redirect
from jinja2 import TemplateNotFound
from lsdserver import status
import flask

sensor = Blueprint('sensor', __name__,
                        template_folder='templates')

@sensor.route('/<platform_id>/<manufacturer>/<model>/<serial_number>', methods=['PUT'])
def create(platform_id, manufacturer, model, serial_number):
    json = request.get_json()

    print "*****************************"
    import pprint
    pprint.pprint(json)
    result = None
    if json:
        # platform_id in URI overrides any platform URI present in json
        json["platform_id"] = platform_id
        json["manufacturer"] = manufacturer
        json["model"] = model
        json["serial_number"] = serial_number
        current_app.system.create_sensor(json)
        result = status.CREATED
    else:
        result = status.BAD_REQUEST
    return render_template('platform.html'), result

@sensor.route('/<platform_id>/<manufacturer>/<model>/<serial_number>', methods=['GET'])
def get(platform_id, manufacturer, model, serial_number):
    data = current_app.system.get_sensor(platform_id, manufacturer, model, serial_number)
    payload = flask.jsonify(data)
    return payload, status.OK

@sensor.route('/<platform_id>/<manufacturer>/<model>/<serial_number>', methods=['DELETE'])
def delete(platform_id, manufacturer, model, serial_number):
    current_app.system.delete_sensor(platform_id, manufacturer, model, serial_number)
    return render_template('platform.html'), status.OK