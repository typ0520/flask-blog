#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

from flask import current_app
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegisterForm, ModifyPwdForm, ResetPwdForm, ResetPwdEditForm
from ..email import send_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        #current_user.ping()
        if not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

    # if current_user.is_authenticated \
    #         and not current_user.confirmed \
    #         and request.endpoint \
    #         and request.endpoint[:5] != 'auth.' \
    #         and request.endpoint != 'static':
    #     return redirect(url_for('auth.unconfirmed'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/modify_pwd', methods=['GET','POST'])
@login_required
def modify_pwd():
    form = ModifyPwdForm()
    if form.validate_on_submit():
        if not current_user.verify_password(form.password.data):
            flash('Invalid password.')
            return redirect(url_for('auth.modify_pwd'))
        current_user.password_hash = User(password=form.new_password.data).password_hash
        db.session.add(current_user)
        flash('Reset password success.')
        return redirect(url_for('main.index'))
    return render_template('auth/modify_pwd.html', form=form)


@auth.route('/reset_pwd', methods=['GET','POST'])
def reset_pwd():
    form = ResetPwdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('The mail does not exist.')
            return redirect(url_for('auth.reset_pwd'))
        s = Serializer(current_app.config['SECRET_KEY'], 3600)
        token = s.dumps({'user_id': user.id,'email': user.email})
        send_email(form.email.data, 'Reset password', 'auth/email/reset_pwd', user=user, token=token)
        flash('A verification email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_pwd.html', form=form)


@auth.route('/reset_pwd_edit/<token>', methods=['GET','POST'])
def reset_pwd_edit(token):
    form = ResetPwdEditForm()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        pass

    if data is None:
        flash('Invalid token.')
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        user_id = data.get('user_id')
        email = data.get('email')
        user = User.query.filter_by(id=user_id,email=email).first()

        if user:
            user.password = form.new_password.data
            db.session.add(user)
            flash('Reset password success.')
        else:
            flash('Invalid token.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_pwd_edit.html', form=form)