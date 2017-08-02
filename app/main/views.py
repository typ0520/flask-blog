#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

from datetime import datetime
from flask import render_template, session, redirect, url_for, abort
from flask_login import login_required
from . import main
from .. import db
from ..models import User, Permission
from ..decorators import permission_required, admin_required


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"


@main.route('/moderator')
@login_required
@permission_required(permission=Permission.MODERATE_COMMENTS)
def for_moderator_only():
    return "For comment moderator!"


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user);