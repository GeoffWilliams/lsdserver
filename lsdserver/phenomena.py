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

phenomena = Blueprint('phenomena', __name__, template_folder='templates')


@phenomena.route('/<path:term>', methods=['PUT'])
def create(term):
    return Helper.create(request, current_app.system.create_phenomena,
                         {"term": term})


@phenomena.route('/<path:term>', methods=['DELETE'])
def delete(term):
    current_app.system.delete_phenomena(term)
    return "processed", status.NO_CONTENT


@phenomena.route('/<path:term>', methods=['GET'])
def get(term):
    data = current_app.system.get_phenomena(term)
    payload = flask.jsonify(data)
    return payload, status.OK
