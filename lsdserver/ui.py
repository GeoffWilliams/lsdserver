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
from lsdserver.config import Config
from lsdserver import status
import flask

ui = Blueprint('ui', __name__,
                        template_folder='templates')


def want_json():
    current_app.logger.debug(
        "request.accept_mimetypes: " + str(request.accept_mimetypes))
    return 'application/json' in request.accept_mimetypes


@ui.route('/', methods=['GET'])
def index():
    """
    Get the list of platforms
    """
    payload = render_template('index.html')
    current_app.logger.debug('payload: ' + str(payload))
    return payload, status.OK

