#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - https://taliox.io
# Robert Kamuda, robert@taliox.io

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from mailstatic.database import Base
from datetime import datetime
import uuid


class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(512))
    replyto = Column(String(512))
    next = Column(String(1024))
    subject = Column(String(512))
    cc = Column(String(512))
    language = Column(String(128))
    message_uuid = Column(String(128), index=True)

    message = Column(Text)
    error = Column(String(512))

    captcha_success = Column(DateTime)
    time_send = Column(DateTime)

    email_id = Column(Integer, ForeignKey("emails.email_id"))

    def __init__(self, name, replyto, message, next=None, subject=None, cc=None, language="en"):
        self.name = name
        self.replyto = replyto
        self.message = message
        self.next = next
        self.subject = subject
        self.cc = cc
        self.language = language
        self.message_uuid = str(uuid.uuid4())

    def set_captcha_success(self):
        self.captcha_success = datetime.utcnow()

    def set_send(self):
        self.time_send = datetime.utcnow()

    def validate(self):
        pass
