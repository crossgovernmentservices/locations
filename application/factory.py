# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask


def create_app(config_filename):
    ''' An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/
    '''
    app = Flask(__name__)
    app.config.from_object(config_filename)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from application.views import application
    app.register_blueprint(application)
