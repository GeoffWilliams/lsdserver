from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from lsdserver.config import Config
from lsdserver import status

platforms = Blueprint('platforms', __name__,
                        template_folder='templates')


@platforms.route('/<platform_id>')
def show(platform_id):
    print("hello " + platform_id)
    return Config.system.hello()

@platforms.route('/<platform_id>', methods=['POST'])
def platformsCreate(platform_id):
    return render_template('platforms.html'), status.CREATED
