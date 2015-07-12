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
from lsdserver import status
from lsdserver.helper import Helper
import flask

platform = Blueprint('platform', __name__, template_folder='templates')




@platform.route('/', methods=['GET'])
def get_platform_list():
    """
    Get the list of platforms
    """
    current_app.logger.debug("get_platform_list()")
    data = current_app.system.get_platforms()
    if data:
        if Helper.want_json(request):
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
    if Helper.want_json(request):
        payload = flask.jsonify(data)
    else:
        payload = render_template('platform.html',
                                  platform_id=platform_id, data=data)
    current_app.logger.debug('payload: ' + str(payload))
    return payload, status.OK


@platform.route('/<platform_id>', methods=['PUT'])
def create(platform_id):
    return Helper.create(request, current_app.system.create_platform,
                         {"platform_id": platform_id})


@platform.route('/<platform_id>', methods=['DELETE'])
def delete(platform_id):
    current_app.system.delete_platform(platform_id)
    return render_template('platform.html'), status.NO_CONTENT


@platform.route('/<platform_id>/info', methods=['GET'])
def get_info(platform_id):
    data = current_app.system.get_platform(platform_id)
    return Helper.info_redirect(data)


@platform.route('/<platform_id>/info', methods=['PUT'])
def put_info(platform_id):
    data = current_app.system.get_platform(platform_id)
    update_function = current_app.system.update_platform
    return Helper.put_info(data, request, update_function)


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