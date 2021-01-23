#!/usr/bin/python3
# -*- coding: utf-8 -*-

def ends(count, a, b, c):
    if count % 10 == 1 and count % 100 != 11:
        return a
    elif 1 < count % 10 < 5:
        return b
    else:
        return c