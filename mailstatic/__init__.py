#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - https://taliox.io
# Robert Kamuda, robert@taliox.io


from flask import Flask
import os

app = Flask(__name__)

app.config.from_object("mailstatic.config.DevelopmentConfig")
app.config.from_envvar("MAILSTATIC_CONFIG", silent=True)

for k in ['RECAPTCHA_SITEKEY', 'RECAPTCHA_SECRET', 'SMTP_SERVER', 'SMTP_USER', 'SMTP_PASSWORD', 'SERVER_ADDRESS',
          'DATABASE_URI', 'FROM_ADDRESS', 'USE_CAPTCHA', 'USE_RATELIMIT']:
    if k in os.environ:
        app.config[k] = os.environ[k]

import mailstatic.views
