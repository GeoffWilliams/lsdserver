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
from lsdserver.helper import Helper
import flask

sensor = Blueprint('sensor', __name__, template_folder='templates')

@sensor.route('/<platform_id>/<manufacturer>/<model>/<serial_number>', methods=['PUT'])
def create(platform_id, manufacturer, model, serial_number):
    return Helper.create(request, current_app.system.create_sensor, {
        "platform_id": platform_id,
        "manufacturer": manufacturer,
        "model": model,
        "serial_number": serial_number
    })


@sensor.route('/<platform_id>/<manufacturer>/<model>/<serial_number>/info', methods=['GET'])
def get_info(platform_id, manufacturer, model, serial_number):
    data = current_app.system.get_sensor(platform_id, manufacturer, model, serial_number)
    return Helper.info_redirect(data)

@sensor.route('/<platform_id>/<manufacturer>/<model>/<serial_number>/info', methods=['PUT'])
def put_info(platform_id, manufacturer, model, serial_number):
    data = current_app.system.get_sensor(platform_id, manufacturer, model, serial_number)
    update_function = current_app.system.update_sensor
    return Helper.put_info(data, request, update_function)

@sensor.route('/<platform_id>/<manufacturer>/<model>/<serial_number>', methods=['GET'])
def get(platform_id, manufacturer, model, serial_number):
    data = current_app.system.get_sensor(platform_id, manufacturer, model, serial_number)
    payload = flask.jsonify(data)
    return payload, status.OK

@sensor.route('/', methods=['GET'])
def get_list():
    data = current_app.system.get_sensors()
    payload = Helper.get_list("sensors.html", request, data)
    return payload, status.OK


@sensor.route('/<platform_id>', methods=['GET'])
def get_list_platform(platform_id):
    data = current_app.system.get_sensors(platform_id)
    payload = Helper.get_list("sensors.html", request, data)
    return payload, status.OK


@sensor.route('/<platform_id>/<manufacturer>', methods=['GET'])
def get_list_platform_manufacturer(platform_id, manufacturer):
    data = current_app.system.get_sensors(platform_id, manufacturer)
    payload = Helper.get_list("sensors.html", request, data)
    return payload, status.OK


@sensor.route('/<platform_id>/<manufacturer>/<model>', methods=['GET'])
def get_list_platform_manufacturer_model(platform_id, manufacturer, model):
    data = current_app.system.get_sensors(platform_id, manufacturer, model)
    payload = Helper.get_list("sensors.html", request, data)
    return payload, status.OK


@sensor.route('/<platform_id>/<manufacturer>/<model>/<serial_number>', methods=['DELETE'])
def delete(platform_id, manufacturer, model, serial_number):
    current_app.system.delete_sensor(platform_id, manufacturer, model, serial_number)
    return "result", status.NO_CONTENT