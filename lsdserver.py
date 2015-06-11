#!/usr/bin/env python
# settings for uwsgi/command line

import os
from lsdserver import create_app
app_dir = os.path.dirname(os.path.realpath(__file__))
app = create_app(app_dir)

if __name__ == '__main__':
    app.run()

