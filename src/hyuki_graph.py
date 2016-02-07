#!/usr/bin/env python3
# coding: UTF-8

import os
import datetime
import pprint
import subprocess

def get_commit_numbers(path):
    os.chdir(path)
    if not os.path.isdir(path + '/.git'):
        return None

    log = subprocess.check_output(
        ['git', 'log', '--oneline', '--date=short',
            '--pretty=format:\"%ad\"']).decode('utf-8')

    numbers = dict()

    for date in get_dates():
        year, month, day = date.year, date.month, date.day
        _format = "%04d-%02d-%02d" % (year, month, day)
        numbers[date] = log.count(_format)
    return numbers

def get_children_dirs(path):
    for (_, dirs, _) in os.walk(path):
        for d in dirs:
            yield os.path.abspath(d)

def get_cvs_dirs(path):
    for p in get_children_dirs(path):
        if os.path.isdir(p + '/.git'):
            yield p

def get_dates():
    dates = []
    today = datetime.datetime.today()
    for days in [7 - days for days in range(7 + 1)]:
        yield today - datetime.timedelta(days=days)

pprint.pprint(get_commit_numbers('.'))
