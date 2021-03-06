import logging
import flask
from lsdserver import status
from lsdserver.driver import LsdBackend


class MockSystem(LsdBackend):
    logger = logging.getLogger('lsdserver.MockSystem')
    logger.setLevel(logging.DEBUG)

    def __init__(self):
        self.parameters = {}
        self.platforms = {}
        self.sensors = {}
        self.phenomena = {}
        self.flags = {}

    def get_platform(self, platform_id):
        data = None
        if platform_id in self.platforms:
            data = self.platforms[platform_id]
        else:
            flask.abort(status.NOT_FOUND)
        return data

    def get_sensor(self, platform_id, manufacturer, model, serial_number):
        try:
            data = self.sensors[platform_id][manufacturer][model][serial_number]
        except KeyError:
            self.logger.debug(
                'sensor not found:  ' + platform_id + '/' + manufacturer + '/' +
                model + '/' + serial_number)
            flask.abort(status.NOT_FOUND)
        return data

    def get_sensors(self, platform_id=None, manufacturer=None, model=None):
        matched = {}
        for idx_platform_id in self.sensors:
            if (platform_id and idx_platform_id == platform_id) or platform_id is None:
                for idx_manufacturer in self.sensors[idx_platform_id]:
                    if (manufacturer and idx_manufacturer == manufacturer) or manufacturer is None:
                        for idx_model in self.sensors[idx_platform_id][idx_manufacturer]:
                            if (idx_model in self.sensors[idx_platform_id][idx_manufacturer]) or model is None:
                                for idx_serial_number in self.sensors[idx_platform_id][idx_manufacturer][idx_model]:
                                    matched[idx_serial_number]=self.sensors[idx_platform_id][idx_manufacturer][idx_model][idx_serial_number]
        return matched

    def get_parameters(self, platform_id=None, manufacturer=None, model=None, serial_number=None):
        matched = {}
        for idx_platform_id in self.parameters:
            if (platform_id and idx_platform_id == platform_id) or platform_id is None:
                for idx_manufacturer in self.parameters[idx_platform_id]:
                    if (manufacturer and idx_manufacturer == manufacturer) or manufacturer is None:
                        for idx_model in self.parameters[idx_platform_id][idx_manufacturer]:
                            if (idx_model in self.parameters[idx_platform_id][idx_manufacturer]) or model is None:
                                for idx_serial_number in self.parameters[idx_platform_id][idx_manufacturer][idx_model]:
                                    if (idx_serial_number in self.parameters[idx_platform_id][idx_manufacturer][idx_model]) or serial_number is None:
                                        for idx_phenomena in self.parameters[idx_platform_id][idx_manufacturer][idx_model][idx_serial_number]:
                                            matched[idx_phenomena]=self.parameters[idx_platform_id][idx_manufacturer][idx_model][idx_serial_number][idx_phenomena]

        return matched

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
        if platform_id in self.platforms:
            if platform_id not in self.sensors:
                self.sensors[platform_id] = {}

            if manufacturer not in self.sensors[platform_id]:
                self.sensors[platform_id][manufacturer] = {}

            if model not in self.sensors[platform_id][manufacturer]:
                self.sensors[platform_id][manufacturer][model] = {}

            if serial_number in self.sensors[platform_id][manufacturer][model]:
                flask.abort(status.CONFLICT)
            else:
                self.sensors[platform_id][manufacturer][model][serial_number] = data
        else:
            flask.abort(status.NOT_FOUND)

        #if platform_id in self.platforms:
        #    if sensor_id in self.sensors:
        #        self.logger.debug('duplicate sensor:  %s', sensor_id)
        #        flask.abort(status.CONFLICT)
        #    else:
        #        self.logger.debug('create_sensor(%s, %s, %s)',
        #            platform_id, sensor_id, str(data))
        #        self.sensors[sensor_id] = data
        #else:

    def update_sensor(self, data):
        """replace whole sensor"""
        try:
            self.sensors\
                [data["platform_id"]]\
                [data["manufacturer"]]\
                [data["model"]]\
                [data["serial_number"]] = data
        except KeyError:
            flask.abort(status.NOT_FOUND)

    def delete_platform(self, platform_id):
        if platform_id in self.platforms:
            del self.platforms[platform_id]

    def delete_sensor(self, platform_id, manufacturer, model, serial_number):
        try:
            del self.sensors[platform_id][manufacturer][model][serial_number]
        except KeyError:
            flask.abort(status.NOT_FOUND)

    def create_parameter(self, data):
        platform_id = data["platform_id"]
        manufacturer = data["manufacturer"]
        model = data["model"]
        serial_number = data["serial_number"]
        phenomena = data["phenomena"]
        if platform_id in self.platforms:
            if platform_id not in self.parameters:
                self.parameters[platform_id] = {}

            if manufacturer not in self.parameters[platform_id]:
                self.parameters[platform_id][manufacturer] = {}

            if model not in self.parameters[platform_id][manufacturer]:
                self.parameters[platform_id][manufacturer][model] = {}

            if serial_number not in self.parameters[platform_id][manufacturer][model]:
                self.parameters[platform_id][manufacturer][model][serial_number] = {}

            if phenomena in self.parameters[platform_id][manufacturer][model][serial_number]:
                flask.abort(status.CONFLICT)
            else:
                self.parameters\
                    [platform_id]\
                    [manufacturer]\
                    [model]\
                    [serial_number]\
                    [phenomena] = data
        else:
            flask.abort(status.NOT_FOUND)

    def get_parameter(self,
                      platform_id,
                      manufacturer,
                      model,
                      serial_number,
                      phenomena):
        try:
            data = self.parameters\
                    [platform_id]\
                    [manufacturer]\
                    [model]\
                    [serial_number]\
                    [phenomena]
        except KeyError:
            flask.abort(status.NOT_FOUND)
        return data

    def delete_parameter(self,
                         platform_id,
                         manufacturer,
                         model,
                         serial_number,
                         phenomena):
        try:
            del self.parameters\
                    [platform_id]\
                    [manufacturer]\
                    [model]\
                    [serial_number]\
                    [phenomena]
        except KeyError:
            flask.abort(status.NOT_FOUND)

    def create_phenomena(self, data):
        if data["term"] in self.phenomena:
            flask.abort(status.CONFLICT)
        else:
            self.phenomena[data["term"]] = data

    def get_phenomena(self, term):
        try:
            return self.phenomena[term]
        except KeyError:
            flask.abort(status.NOT_FOUND)

    def get_phenomenas(self):
        return self.phenomena

    def delete_phenomena(self, term):
        try:
            del self.phenomena[term]
        except KeyError:
            flask.abort(status.NOT_FOUND)

    def create_flag(self, data):
        if data["term"] in self.flags:
            flask.abort(status.CONFLICT)
        else:
            self.flags[data["term"]] = data

    def get_flag(self, term):
        try:
            return self.flags[term]
        except KeyError:
            flask.abort(status.NOT_FOUND)

    def get_flags(self):
        return self.flags

    def delete_flag(self, term):
        try:
            del self.flags[term]
        except KeyError:
            flask.abort(status.NOT_FOUND)

        