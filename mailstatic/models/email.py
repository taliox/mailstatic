#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - https://taliox.io
# Robert Kamuda, robert@taliox.io

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from mailstatic.database import Base

from datetime import datetime
from mailstatic.utils.generators import generate_random_string

class Email(Base):
    __tablename__ = 'emails'
    email_id = Column(Integer, primary_key=True, index=True)
    address = Column(String(512))
    verified = Column(DateTime)
    added = Column(DateTime)
    verify_token = Column(String(128))

    account_id = Column(Integer, ForeignKey("accounts.account_id"))

    messages = relationship("Message", backref="email")

    def __init__(self, address):
        self.address = address
        self.added = datetime.utcnow()
        self.verify_token = generate_random_string(32)

    def verify(self):
        self.verified = datetime.utcnow()

    def validate(self):
        pass

    def __repr__(self):
        return '<Email:{} {} added:{}>'.format(self.email_id, self.address, self.added)