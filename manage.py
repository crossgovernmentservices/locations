import os

from flask.ext.script import Server, Manager
from application.factory import create_app

manager = Manager(create_app)
manager.add_option("-c", "--config", dest="config_filename", required=True)
manager.add_command("runserver", Server(host='0.0.0.0', port=int(os.environ['PORT'])))

if __name__ == '__main__':
    manager.run()
