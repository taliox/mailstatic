#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - https://taliox.io
# Robert Kamuda, robert@taliox.io

import random
import string


def generate_random_string(length=8, alphabet=string.digits + string.ascii_letters):
    return ''.join(random.choice(alphabet) for _ in range(length))
