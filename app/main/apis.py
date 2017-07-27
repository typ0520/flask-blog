#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

from datetime import datetime
from flask import render_template,session, redirect, url_for

from . import main
from .. import db
from ..models import User

@main.route('/api', methods=['GET', 'POST'])
def api_index():
    return 'api2'