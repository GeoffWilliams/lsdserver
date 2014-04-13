from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from lsdserver.config import Config
from lsdserver import status
import flask

platforms = Blueprint('platforms', __name__,
                        template_folder='templates')


@platforms.route('/<platform_id>', methods=['GET'])
def get(platform_id):
    data=Config.system.get_platform(platform_id)
    return flask.jsonify(data)
    #return render_template('platform.html', platform_id=platform_id, data=data), status.OK


@platforms.route('/<platform_id>', methods=['POST'])
def create(platform_id):
    Config.system.create_platform(platform_id, flask.request.get_data())
    return render_template('platform.html'), status.CREATED


@platforms.route('/<platform_id>', methods=['DELETE'])
def delete(platform_id):
    Config.system.delete_platform(platform_id)
    return render_template('platform.html'), status.OK
