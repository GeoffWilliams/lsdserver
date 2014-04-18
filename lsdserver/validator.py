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
import re
from dateutil import parser

class Validator:
    """
    Support for validation of identifiers and internal data structures
    """

    # define the supported fields for each data structure as a dictionary.
    # True/False indicate whether the parameter is mandatory or not
    parameter_supported_fields = dict(
        name=True,
        description=False,
        type=True,
        uom=False,
        min_value=False,
        max_value=False,
        link=False
    )

    platform_supported_fields = dict(
        name=False,
        manufacturer=False,
        model=False,
        serial_number=False,
        description=False,
        link=False,
        mobile=False,
        position=False
    )

    sensor_supported_fields = dict(
        name=False,
        manufacturer=False,
        model=False,
        serial_number=False,
        description=False,
        parameters=True,
        link=False,
        position=False
    )

    observation_supported_fields = dict(
        times=False,
        parameters=True,
        values=True
    )

    parameter_type_support = {"int", "float", "boolean"}

    # one or more letters, numbers and underscores
    identifier_regexp = re.compile('^\w+$')

    # positions should be specified as OGC WKT - at the moment we only support
    # points.  Complex movements (linestrings) can be computed from these point
    # values when stored in the database to show movement, etc.  We may one day
    # want to allow polygons here to indicate a coverage, etc
    position_regexp = re.compile(
        '^POINT \((\+|-)?\d+(\.\d+)? (\+|-)?\d+(\.\d+)?\)$'
    )

    def __init__(self):
        pass

    def validate_position(self, position):
        """
        Validate a position - it should specify a point using OGC WKT
        """
        return Validator.position_regexp.match(position) is not None

    def validate_time_string(self, time_string):
        """
        Validate a time string using the dateutil package

        Returns a datetime instance on successful parsing or False on error
        """
        try:
            value = parser.parse(time_string)
        except ValueError:
            value = False
        return value

    def validate_parameter_type(self, parameter_type):
        return parameter_type in Validator.parameter_type_support

    def validate_parameter(self, parameter_id, value):
        pass

    def validate_identifier(self, identifier):
        return Validator.identifier_regexp.match(identifier) is not None

    def validate_platform(self, platform):
        pass

    def validate_sensor(self, sensor):
        pass

    def validate_observation(self, sensor_id, observation):
        pass
