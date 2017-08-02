#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

from functools import wraps
from flask_login import current_user
from flask import abort
from .models import Permission

def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(func):
    return permission_required(Permission.ADMINISTER)(func)