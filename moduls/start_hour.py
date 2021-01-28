#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

def startHour():
    hour = int(str(time.asctime())[11:13])
    return hour + 1
