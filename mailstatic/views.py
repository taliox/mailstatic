#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - https://taliox.io
# Robert Kamuda, robert@taliox.io

from flask import request, render_template, jsonify, url_for
from mailstatic import app
from mailstatic.models import Message, Email
from mailstatic.database import db_session
from sqlalchemy.orm.exc import NoResultFound
import requests
from mailstatic.utils.mailsender import MailSender
from gevent import Greenlet
import gevent
from mailstatic.utils.limit import redis, limit_by_key, LimitExceeded

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.errorhandler(NoResultFound)
def handle_noresult(e):
    return "Not found", 404


@app.errorhandler(LimitExceeded)
def handle_limit_exceeded(e):
    return "You got into a ratelimit.", 403


@app.route('/')
def index():
    return render_template("index.html")


def check_usercaptcha(response):
    r = requests.post(
        url="https://www.google.com/recaptcha/api/siteverify",
        data={
            'secret': app.config['RECAPTCHA_SECRET'],
            'response': response
        },
        timeout=1
    )

    r.raise_for_status()

    j = r.json()

    return j.get('success', False)


@app.route('/sendmail/<string:uuid>/', methods=['GET', 'POST'])
def sendmail(uuid):
    try:
        message = Message.query.filter(Message.message_uuid == uuid).one()
    except NoResultFound as e:
        raise

    if request.method == 'GET':
        return render_template("mailinfo.html", message=message)

    try:
        limit_by_key("mail-precaptcha:{}".format(uuid), limit=10, ttl=60)
    except LimitExceeded as e:
        return "Limit exceeded. {}".format(str(e))

    if message.time_send:
        return "Mail already sent."

    if check_usercaptcha(request.form.get("g-recaptcha-response")):
        message.set_captcha_success()
        message.set_send()
        db_session.commit()

        MailSender.send_mail(
            address=message.email.address,
            subject="Contact form",
            message=render_template("email_template.txt", message=message),
            replyto=message.replyto,
        )

        return render_template("mail_send.html", message=message)
    else:
        return "Captcha validation failed", 500


@app.route('/s/<string:email>', methods=['GET', 'POST'])
def send_mail(email):
    try:
        limit_by_key("premail:{}".format(email), limit=10, ttl=60)
    except LimitExceeded as e:
        return "Limit. {}".format(str(e))

    if request.method == 'GET':
        return 'Please use POST with parameters.'
    else:
        if not request.form.get('replyto') or not request.form.get('name') or not request.form.get('message'):
            return render_template("params_missing.html")

        try:
            email = Email.query.filter(Email.address == email).one()
        except NoResultFound as e:
            email = Email(email)
            db_session.add(email)
            db_session.commit()

        if not email.verified:
            limit_by_key("verimail:{}".format(email), limit=10, ttl=60*60*24)
            MailSender.send_mail(
                address=email.address,
                subject="Please verify your E-Mail",
                message='{}{}\nClick here\n\n'.format(app.config['SERVER_ADDRESS'], url_for('verify_email', token=email.verify_token)),
                replyto="noreply@byte.so"
            )
            return render_template("verify_email.html", verify_email=email.address)

        message = Message(
            name=request.form.get("name"),
            replyto=request.form.get("replyto"),
            message=request.form.get("message"),
            next=request.form.get("next") or None,
            subject=request.form.get("subject") or None,
            cc=request.form.get("cc") or None,
            language=request.form.get("language") or None
        )

        message.email = email
        message.validate()

        if app.config['USE_RECAPTCHA'] == 'false':
            MailSender.send_mail(
                address=message.email.address,
                subject="Contact form",
                message=render_template("email_template.txt", message=message),
                replyto=message.replyto,
            )
            message.set_send()

            db_session.add(message)
            db_session.commit()

            return render_template("mail_send.html", message=message)

        db_session.add(message)
        db_session.commit()

        return render_template("mail_captcha.html", message=message)


@app.route('/v/<string:token>/')
def verify_email(token):
    email = Email.query.filter(Email.verify_token == token).one()
    if email.verified:
        return "E-Mail already verified."

    email.verify()
    db_session.commit()

    return render_template("success_verify_email.html", email=email)
