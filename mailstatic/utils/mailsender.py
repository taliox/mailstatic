#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - https://taliox.io
# Robert Kamuda, robert@taliox.io

from mailstatic import app

import smtplib
from email.mime.text import MIMEText

class MailSender(object):
    @classmethod
    def send_mail(cls, address, subject, message, replyto, cc=None):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = app.config['FROM_ADDRESS']
        msg['To'] = address
        if replyto:
            msg['Reply-To'] = replyto

        s = smtplib.SMTP_SSL(app.config['SMTP_SERVER'], timeout=1)
        s.login(app.config['SMTP_USER'], app.config['SMTP_PASSWORD'])
        s.send_message(msg)
