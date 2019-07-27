#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - https://taliox.io
# Robert Kamuda, robert@taliox.io


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:////tmp/test.db'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

def load_config():
    pass