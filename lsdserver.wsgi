# settings for wsgi/apache (? - untested!)
import sys
import os
app_dir = os.path.dirname(__file__)
sys.path.append(app_dir)

from lsdserver import create_app
app = create_app(app_dir)
