from flask import Flask
from distutils.command.config import config

def create_app(config_name):
    app = Flask(__name__)
    return app