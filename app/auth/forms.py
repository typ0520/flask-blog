#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remeber_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ModifyPwdForm(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    new_password = PasswordField('New-password',
                                 validators=[Required(), EqualTo('new_password2', message='Passwords must match.')])
    new_password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Reset')


class ResetPwdForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])