#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)