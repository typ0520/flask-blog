#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, posts, users, comments, errors
