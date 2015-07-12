from flask import Blueprint, render_template, abort, current_app, redirect
from lsdserver import status
import flask

class Helper():

    @staticmethod
    def want_json(request):
        best = request.accept_mimetypes \
            .best_match(['application/json', 'text/html'])
        return best == 'application/json' and \
            request.accept_mimetypes[best] > \
            request.accept_mimetypes['text/html']

    @staticmethod
    def info_redirect(data):
        """Redirect to the info URI present in the `info` key or abort if missing"""
        if data["info"]:
            return redirect(data["info"])
        else:
            abort(status.NOT_FOUND)

    @staticmethod
    def put_info(data, request, update_function):
        request_data = request.get_data()
        result = None
        message = None
        if data:
            if request_data:
                data["info"] = request_data
                update_function(data)
                result = status.CREATED
                message = "OK"
            else:
                result = status.BAD_REQUEST
                message = "ERROR"
        else:
            message = "MISSING"
            result = status.NOT_FOUND
        return message, result

    @staticmethod
    def create(request, create_function, overrides):
        json = request.get_json()
        result = None
        if json:
            for field in overrides:
                json[field] = overrides[field]
            create_function(json)
            result = status.CREATED
            message = "OK"
        else:
            result = status.BAD_REQUEST
            message = "ERROR"

        return message, result

    @staticmethod
    def get_list(template, request, data):
        print("---->" + str(data))
        if data:
            if Helper.want_json(request):
                payload = flask.jsonify(data)
                print str(payload)
            else:
                payload = render_template(template, data=data)
        else:
            payload = "no data found"

        return payload