# settings for uwsgi/command line
from lsdserver import create_app
app = create_app()

if __name__ == '__main__':
    app.run()

