import logging
import flask
from lsdserver import status


class MockSystem(object):
    logger = logging.getLogger('lsdserver.MockSystem')
    logger.setLevel(logging.DEBUG)

    def __init__(self):
        self.parameters = {}
        self.platforms = {}
        self.sensors = {}

    def get_platform(self, platform_id):
        data = None
        if platform_id in self.platforms:
            data = self.platforms[platform_id]
        else:
            flask.abort(status.NOT_FOUND)
        return data

    def get_sensor(self, platform_id, sensor_id):
        data = None
        if platform_id in self.platforms:
            if sensor_id in self.sensors:
                data = self.sensors[sensor_id]
            else:
                # no such sensor
                self.logger.debug('sensor not found:  ' + sensor_id)
                flask.abort(status.NOT_FOUND)
        else:
            # no such platform
            self.logger.debug('platform not found:  ' + platform_id)
            flask.abort(status.NOT_FOUND)
        return data

    def get_platforms(self):
        return self.platforms

    def update_platform(self, data):
        """replace whole platform"""
        platform_id = data["platform_id"]
        self.platforms[platform_id] = data

    def create_platform(self, data):
        platform_id = data["platform_id"]
        if platform_id in self.platforms:
            self.logger.debug('duplicate platform:  %s', platform_id)
            flask.abort(status.CONFLICT)
        else:
            self.logger.debug(
                'create_platform(%s, %s)', platform_id, str(data))
            self.platforms[platform_id] = data

    def create_sensor(self, data):
        platform_id = data["platform_id"]
        manufacturer = data["manufacturer"]
        model = data["model"]
        serial_number = data["serial_number"]
        sensor_id = manufacturer + model + serial_number
        if platform_id in self.platforms:
            if sensor_id in self.sensors:
                self.logger.debug('duplicate sensor:  %s', sensor_id)
                flask.abort(status.CONFLICT)
            else:
                self.logger.debug('create_sensor(%s, %s, %s)',
                    platform_id, sensor_id, str(data))
                self.sensors[sensor_id] = data
        else:
            flask.abort(status.NOT_FOUND)

    def delete_platform(self, platform_id):
        if platform_id in self.platforms:
            del self.platforms[platform_id]

    def delete_sensor(self, platform_id, sensor_id):
        if platform_id in self.platforms:
            if sensor_id in self.sensors:
                del self.sensors[sensor_id]
            else:
                flask.abort(status.NOT_FOUND)
        else:
            flask.abort(status.NOT_FOUND)

    def create_parameter(self, parameter_id, data):
        if parameter_id in self.parameters:
            self.logger.debug("duplicate parameter:  %s", parameter_id)
            flask.abort(status.CONFLICT)
        else:
            self.parameters[parameter_id] = data

    def get_parameter(self, parameter_id):
        if parameter_id in self.parameters:
            data = self.parameters[parameter_id]
        else:
            flask.abort(status.NOT_FOUND)
        return data

    def delete_parameter(self, parameter_id):
        if parameter_id in self.parameters:
            del self.parameters[parameter_id]
        else:
            flask.abort(status.NOT_FOUND)

    def get_parameters(self):
        return self.parameters
