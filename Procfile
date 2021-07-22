web: gunicorn weather_remider.wsgi --log-file -
worker: celery -A weather_remider worker --beat --scheduler django --loglevel=info