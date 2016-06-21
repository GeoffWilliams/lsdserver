FROM lbracken/flask-uwsgi:latest
EXPOSE 5000
VOLUME /var/www/app
CMD uwsgi --http :5000 --wsgi-file lsdserver.wsgi --callable app --processes 2 --threads 4
