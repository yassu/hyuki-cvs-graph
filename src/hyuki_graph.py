#!/usr/bin/env python3
# coding: UTF-8

import os
import datetime
import pprint

def get_children_dirs(path):
    for (_, dirs, _) in os.walk(path):
        for d in dirs:
            yield os.path.abspath(d)

def get_dates():
    dates = []
    today = datetime.datetime.today()
    for days in [7 - days for days in range(7 + 1)]:
        yield today - datetime.timedelta(days=days)

pprint.pprint(list(get_dates()))
print(len(list(get_dates())))
