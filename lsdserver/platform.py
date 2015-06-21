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

platform = Blueprint('platform', __name__,
                        template_folder='templates')


def want_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


@platform.route('/', methods=['GET'])
def get_platform_list():
    """
    Get the list of platforms
    """
    current_app.logger.debug("get_platform_list()")
    data = current_app.system.get_platforms()
    if data:
        if want_json():
            payload = flask.jsonify(data)
        else:
            payload = render_template('platforms.html', data=data)

        current_app.logger.debug('payload: ' + str(payload))
    else:
        payload = "no data returned FIXME"
    return payload, status.OK


@platform.route('/<platform_id>', methods=['GET'])
def get_platform(platform_id):
    """
    Get a specific platform
    """
    current_app.logger.debug("get(%s)" % platform_id)
    data = current_app.system.get_platform(platform_id)
    if want_json():
        payload = flask.jsonify(data)
    else:
        payload = render_template('platform.html',
            platform_id=platform_id, data=data)
    current_app.logger.debug('payload: ' + str(payload))
    return payload, status.OK


@platform.route('/<platform_id>', methods=['PUT'])
def create(platform_id):
    json = request.get_json()

    print "*****************************"
    import pprint
    pprint.pprint(json)
    result = None
    if json:
        # platform_id in URI overrides any platform URI present in json
        json["platform_id"] = platform_id
        current_app.system.create_platform(json)
        result = status.CREATED
    else:
        result = status.BAD_REQUEST
    return render_template('platform.html'), result


@platform.route('/<platform_id>', methods=['DELETE'])
def delete(platform_id):
    current_app.system.delete_platform(platform_id)
    return render_template('platform.html'), status.OK


@platform.route('/<platform_id>/info', methods=['GET'])
def get_info(platform_id):
    data = current_app.system.get_platform(platform_id)
    if data["info"]:
        return redirect(data["info"])
    else:
        abort(status.NOT_FOUND)


@platform.route('/<platform_id>/info', methods=['PUT'])
def put_info(platform_id):
    data = current_app.system.get_platform(platform_id)
    request_data = request.get_data()
    result = None
    message = None
    if data:
        if request_data:
            data["info"] = request_data
            current_app.system.update_platform(data)
            result = status.CREATED
            message = "OK"
        else:
            result = status.BAD_REQUEST
            message = "ERROR"
    else:
        message = "MISSING"
        result = status.NOT_FOUND
    return message, result


@platform.route('/<platform_id>/info', methods=['DELETE'])
def delete_info(platform_id):
    data = current_app.system.get_platform(platform_id)
    data["info"] = None
    current_app.system.update_platform(data)
    return "OK", status.NO_CONTENT


@platform.route('/<platform_id>/location', methods=['GET'])
def get_location(platform_id):
    data = current_app.system.get_platform(platform_id)
    if data and data["location"]:
        return data["location"]
    else:
        abort(status.NOT_FOUND)

#@platform.route('/<platform_id>/<sensor_id>', methods=['GET'])
#def get_sensor(platform_id, sensor_id):
    #current_app.logger.debug("get_sensor(%s, %s)" % (platform_id, sensor_id))
    #data = current_app.system.get_sensor(platform_id, sensor_id)
    #if want_json():
        #payload = flask.jsonify(data)
    #else:
        #payload = render_template('sensor.html',
            #platform_id=platform_id, sensor_id=sensor_id, data=data)
    #current_app.logger.debug('payload: ' + str(payload))
    #return payload, status.OK

#
#@platform.route('/<platform_id>/<sensor_id>', methods=['POST'])
#def create_sensor(platform_id, sensor_id):
    #current_app.system.create_sensor(
        #platform_id, sensor_id, flask.request.get_data())
    #return render_template('sensor.html'), status.CREATED

##
#@platform.route('/<platform_id>/<sensor_id>', methods=['DELETE'])
#def delete_sensor(platform_id, sensor_id):
    #current_app.system.delete_sensor(platform_id, sensor_id)
    #return render_template('sensor.html'), status.OK
#