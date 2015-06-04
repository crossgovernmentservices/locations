FROM python:3.4.2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD requirements/* /usr/src/app/requirements/
RUN pip install -r requirements/dev.txt

ADD . /usr/src/app

CMD ["python", "manage.py", "-c", "config.DockerConfig", "runserver"]
