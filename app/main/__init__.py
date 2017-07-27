#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, apis, errors