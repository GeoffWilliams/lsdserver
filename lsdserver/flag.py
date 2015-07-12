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

flag = Blueprint('flag', __name__, template_folder='templates')


@flag.route('/<path:term>', methods=['PUT'])
def create(term):
    return Helper.create(request, current_app.system.create_flag,
                         {"term": term})


@flag.route('/<path:term>', methods=['DELETE'])
def delete(term):
    current_app.system.delete_flag(term)
    return "processed", status.NO_CONTENT


@flag.route('/<path:term>', methods=['GET'])
def get(term):
    data = current_app.system.get_flag(term)
    payload = flask.jsonify(data)
    return payload, status.OK


@flag.route('/', methods=['GET'])
def get_flag_list():
    """
    Get the list of platforms
    """
    data = current_app.system.get_flags()
    payload = Helper.get_list("flags.html", request, data)
    return payload, status.OK