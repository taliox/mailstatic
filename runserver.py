#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - http://taliox.io
# Robert Kamuda, robert@taliox.io

from mailstatic import app


if __name__ == '__main__':
    app.run(host='::', debug=True)