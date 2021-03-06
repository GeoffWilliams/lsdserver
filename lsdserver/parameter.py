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
from flask import Blueprint, render_template, abort, request, current_app
from jinja2 import TemplateNotFound
from lsdserver import status
from lsdserver.helper import Helper
import flask

parameter = Blueprint('parameter', __name__, template_folder='templates')


@parameter.route(
    '/<platform_id>/<manufacturer>/<model>/<serial_number>/<path:phenomena>',
    methods=['PUT'])
def create(platform_id, manufacturer, model, serial_number, phenomena):
    return Helper.create(request, current_app.system.create_parameter, {
        "platform_id": platform_id,
        "manufacturer": manufacturer,
        "model": model,
        "serial_number": serial_number,
        "phenomena": phenomena
    })


@parameter.route(
    '/<platform_id>/<manufacturer>/<model>/<serial_number>/<path:phenomena>',
    methods=['GET']
)
def get(platform_id, manufacturer, model, serial_number, phenomena):
    data = current_app.system.get_parameter(
        platform_id, manufacturer, model, serial_number, phenomena)
    payload = flask.jsonify(data)
    return payload, status.OK

@parameter.route(
    '/<platform_id>/<manufacturer>/<model>/<serial_number>/<path:phenomena>',
    methods=['DELETE']
)
def delete(platform_id, manufacturer, model, serial_number, phenomena):
    current_app.system.delete_parameter(
        platform_id, manufacturer, model, serial_number, phenomena)
    return "result", status.NO_CONTENT

@parameter.route('/', methods=['GET'])
def get_list():
    data = current_app.system.get_parameters()
    payload = Helper.get_list("parameters.html", request, data)
    return payload, status.OK


@parameter.route('/<platform_id>', methods=['GET'])
def get_list_platform(platform_id):
    data = current_app.system.get_parameters(platform_id)
    payload = Helper.get_list("parameters.html", request, data)
    return payload, status.OK


@parameter.route('/<platform_id>/<manufacturer>', methods=['GET'])
def get_list_platform_manufacturer(platform_id, manufacturer):
    data = current_app.system.get_parameters(platform_id, manufacturer)
    payload = Helper.get_list("parameters.html", request, data)
    return payload, status.OK


@parameter.route('/<platform_id>/<manufacturer>/<model>', methods=['GET'])
def get_list_platform_manufacturer_model(platform_id, manufacturer, model):
    data = current_app.system.get_parameters(platform_id, manufacturer, model)
    payload = Helper.get_list("parameters.html", request, data)
    return payload, status.OK


@parameter.route('/<platform_id>/<manufacturer>/<model>/<serial_number>', methods=['GET'])
def get_list_platform_manufacturer_model_serial_number(platform_id, manufacturer, model, serial_number):
    data = current_app.system.get_parameters(platform_id, manufacturer, model, serial_number)
    payload = Helper.get_list("parameters.html", request, data)
    return payload, status.OK

# ================================= old crud below========







@parameter.route('/', methods=['GET'])
def get_parameter_list():
    """
    Get the list of platforms
    """
    current_app.logger.debug("get_parameter_list()")
    data = current_app.system.get_parameters()
    if want_json():
        payload = flask.jsonify(data)
    else:
        payload = render_template('parameters.html', data=data)
    current_app.logger.debug('payload: ' + str(payload))
    return payload, status.OK


@parameter.route('/<parameter_id>', methods=['GET'])
def get_parameter_item(parameter_id):
    """
    Get the list of platforms
    """
    current_app.logger.debug("get_parameter_item(%s)" % parameter_id)
    data = current_app.system.get_parameter(parameter_id)
    if want_json():
        payload = flask.jsonify(data)
    else:
        payload = render_template('parameter.html', data=data)
    current_app.logger.debug('payload: ' + str(payload))
    return payload, status.OK


@parameter.route('/<parameter_id>', methods=['DELETE'])
def delete_parameter(parameter_id):
    """
    Get the list of platforms
    """
    current_app.logger.debug("delete_parameter(%s)" % parameter_id)
    data = current_app.system.delete_parameter(parameter_id)
    if want_json():
        payload = flask.jsonify(data)
    else:
        payload = render_template('parameter.html', data=data)
    current_app.logger.debug('payload: ' + str(payload))
    return payload, status.OK


@parameter.route('/<parameter_id>', methods=['POST'])
def create_parameter(parameter_id):
    """
    Get the list of platforms
    """
    current_app.logger.debug("create_parameter(%s)" % parameter_id)
    data = current_app.system.create_parameter(
            parameter_id, flask.request.get_data())
    if want_json():
        payload = flask.jsonify(data)
    else:
        payload = render_template('parameter.html', data=data)
    current_app.logger.debug('payload: ' + str(payload))
    return payload, status.CREATED
