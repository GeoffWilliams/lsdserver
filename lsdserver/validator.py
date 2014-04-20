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
from numbers import Number


class Validator:
    """
    Support for validation of identifiers and internal data structures
    """

    # define the supported fields for each data structure as a dictionary.
    # True/False indicate whether the parameter is mandatory or not
    parameter_supported_fields = {
        "name": True,
        "description": False,
        "type": True,
        "uom": False,
        "min_value": False,
        "max_value": False,
        "link": False
    }

    platform_supported_fields = {
        "name": False,
        "manufacturer": False,
        "model": False,
        "serial_number": False,
        "description": False,
        "link": False,
        "position": False
    }

    sensor_supported_fields = {
        "name": False,
        "manufacturer": False,
        "model": False,
        "serial_number": False,
        "description": False,
        "parameters": True,
        "link": False
    }

    observation_supported_fields = {
        "times": False,
        "parameters": True,
        "values": True
    }

    def parse_int_value(value):
        return int(value)

    def parse_float_value(value):
        return float(value)

    def parse_bool_value(value):
        return bool(value)

    parameter_type_support = {
        "int": parse_int_value,
        "float": parse_float_value,
        "bool": parse_bool_value
    }

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
        self.parameters = {}
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
        """
        Validate a parameter type by ensuring it is supported

        Returns
        -------
            boolean
                True if the parameter is supported otherwise False
        """
        return parameter_type in Validator.parameter_type_support

    def structure_validator(self, structure, instance):
        """
        Ensure passed in instance is valid according to passed in structure by
        checking that all keys are valid and no mandatory keys are missing

        Returns
        -------
            boolean
                True if instance is valid according to structure otherwise
                false
        """
        valid = True
        # first check all keys valid
        for key in instance:
            if key not in structure:
                valid = False

        # now check all required parameters are present
        for key in structure:
            if structure[key]:
                # (mandatory field)
                if key not in instance:
                    valid = False
        return valid

    def validate_parameter(self, parameter):
        """
        Validate a parameter structure by ensuring all required fields are
        present and no unknown fields exist

        Returns
        -------
            boolean
                True if the structure is valid otherwise False
        """
        valid = self.structure_validator(
            Validator.parameter_supported_fields, parameter)

        if valid:
            # type
            valid &= self.validate_parameter_type(parameter["type"])

            # min/max
            if "min_value" in parameter:
                # check is a number
                valid &= isinstance(parameter["min_value"], Number)

            if "max_value" in parameter:
                # check is a number
                valid &= isinstance(parameter["min_value"], Number)

        return valid

    def validate_identifier(self, identifier):
        """
        Validate an identifier

        Returns
        -------
            boolean
                True if the identifier is valid otherwise False
        """
        return Validator.identifier_regexp.match(identifier) is not None

    def validate_platform(self, platform):
        """
        Validate a platform data structure by ensuring all required fields
        are present and no unknown fields exist

        Returns
        -------
            boolean
                True if structure is valid otherwise False
        """
        valid = self.structure_validator(
            Validator.platform_supported_fields, platform)
        if valid:
            # additional field validation
            if "position" in platform:
                valid = self.validate_position(platform["position"])

        return valid

    def validate_sensor(self, sensor):
        """
        Validate a sensor data struture by ensuring all required fields are
        present and no unknown fields exist

        Returns
        -------
            boolean
                True if structure is valid otherwise False
        """
        valid = self.structure_validator(
            Validator.sensor_supported_fields, sensor)
        if valid:
            # check parameters are valid
            for parameter in sensor["parameters"]:
                parameter_valid = self.validate_parameter_id(parameter)
                if not parameter_valid:
                    valid = False
        return valid

    def validate_observation(self, observation):
        """
        Validate an observation data structure by ensuring all required fields
        are present and no unknown fields exist.

        Returns
        -------
            boolean
                True if structure is valid otherwise false
        """
        valid = True
        error_messages = []
        if observation:
            for key in observation:
                if key == "time":
                    # time was set - ensure its valid
                    if not self.validate_time_string(observation["time"]):
                        valid = False
                        error_messages.append("invalid time component: " + observation["time"])
                else:
                    # a parameter key - validate it
                    if not self.validate_parameter_id(key):
                        valid = False
                        error_messages.append("unknown parameter: " + key)
                    if valid:
                        # finally, check the payload is valid
                        value_type = self.parameters[key]["type"]
                        value = observation[key]
                        if not self.validate_value(value_type, value):
                            valid = False
                            error_messages.append("inappropriate value %s for parameter %s" % (str(value), key))
        else:
            # empty
            valid = False
            error_messages.append("no observation contained in structure")

        print "---------------------> " + str(error_messages)

        return valid

    def validate_value(self, value_type, value):
        try:
            parsed = self.parameter_type_support[value_type](value)
            valid = True
        except ValueError:
            valid = False
        except KeyError:
            print("$$$$$$$$$$$$$$$$$$$$$$ " + str(self.parameter_type_support.keys()) + "**** " + str(value_type))
            valid = False

        return valid

    def validate_parameter_id(self, parameter_id):
        return parameter_id in self.parameters
