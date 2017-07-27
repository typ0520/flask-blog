#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	bootstrap.init_app(app)
	moment.init_app(app)
	db.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app