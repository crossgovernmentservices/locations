# -*- coding: utf-8 -*-
import os


class Config(object):
    DEBUG = False
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    REGISTER_DOMAIN = os.environ.get('REGISTER_DOMAIN')
    SCHOOL_REGISTER = os.environ.get('SCHOOL_REGISTER')
    ADDRESS_REGISTER = os.environ.get('ADDRESS_REGISTER')
    POSTCODE_REGISTER = os.environ.get('POSTCODE_REGISTER')
    POSTTOWN_REGISTER = os.environ.get('POSTTOWN_REGISTER')


class DockerConfig(Config):
    DEBUG = True
