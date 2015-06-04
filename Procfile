#web: gunicorn --config=gunicorn.py application:app
#web: python manage.py runserver 
web: gunicorn application.app -b 0.0.0.0:$PORT -w 3
