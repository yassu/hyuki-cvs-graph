#!/usr/bin/env python
# coding: UTF-8

from hyuki_graph.hyuki_graph import get_dates, get_str_projname
from datetime import date, timedelta
import os.path


def get_dates_test1():
    assert(
        list(get_dates(0)) == [date.today()]
    )


def get_dates_test2():
    today = date.today()
    assert(list(get_dates(2)) == [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today
    ])


def get_str_projname_test1():
    projname = get_str_projname('{sep}usr{sep}bin{sep}dev{sep}'.format(
        sep=os.path.sep))
    assert(projname == 'dev')


def get_str_projname_test2():
    projname = get_str_projname('{sep}usr{sep}bin{sep}dev'.format(
        sep=os.path.sep))
    assert(projname == 'dev')
