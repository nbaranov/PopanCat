#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

def startHour():
    hour = int(str(time.asctime())[11:13])
    if hour > 21:
        return 1, 'tomorrow'
    else: 
        return hour + 1, 'today'
