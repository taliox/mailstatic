#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - https://taliox.io
# Robert Kamuda, robert@taliox.io

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from mailstatic.database import Base
from .email import Email
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash



class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(Integer, primary_key=True)
    account_mail = Column(String(256), index=True, unique=True)
    created = Column(DateTime)
    email_confirmed = Column(DateTime)

    emails = relationship("Email", backref="account")

    def __init__(self, account_mail, password=None):
        self.account_mail = account_mail

        if password:
            self.set_password(password)

        self.created = datetime.utcnow()

    def set_password(self, password):
        pass

