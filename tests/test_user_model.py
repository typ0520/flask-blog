#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'typ0520'

import unittest
from app.models import Role, User, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='typ0520')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='typ0520')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='typ0520')
        self.assertTrue(u.verify_password('typ0520'))
        self.assertFalse(u.verify_password('tong'))

    def test_password_salts_are_random(self):
        u = User(password='typ0520')
        u2 = User(password='typ0520')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='dsdsd@gmail.com', password='pwd')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
