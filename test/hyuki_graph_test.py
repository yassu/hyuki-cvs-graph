#!/usr/bin/env python
# coding: UTF-8

from nose.tools import raises
from hyuki_graph.hyuki_graph import(
    get_dates, get_str_projname, get_commits_from_text,
    get_date_from_text
    )
from datetime import date, timedelta
import os.path

def get_date_from_text_test1():
    assert(get_date_from_text('2015/03/21') ==
            date(2015, 3, 21))

@raises(TypeError)
def get_date_from_text_test2():
    get_date_from_text('bear')

@raises(TypeError)
def get_date_from_text_test3():
    get_date_from_text('year/02/03')


@raises(TypeError)
def get_date_from_text_test4():
    get_date_from_text('2015/month/03')

@raises(TypeError)
def get_date_from_text_test5():
    get_date_from_text('2015/02/day')

@raises(TypeError)
def get_date_from_text_test6():
    get_date_from_text('2015/02/99')

def get_commits_from_text_test0():
    text = '{}'
    assert(get_commits_from_text(text) == {})

def get_commits_from_text_test1():
    text = '{"proj1": {"2016/01/01": 3}}'
    assert(get_commits_from_text(text) ==
        {'proj1':
            {date(2016, 1, 1): 3}}
        )

def get_commits_from_text_test2():
    text = ('{"proj1": {"2016/01/01": 3,'
                      '"2016/01/03": 5}}')
    assert(get_commits_from_text(text) ==
        {'proj1': {
            date(2016, 1, 1): 3,
            date(2016, 1, 3): 5}})

def get_commits_from_text_test3():
    text = ('{"proj1": {"2016/01/01": 3,'
                      '"2016/01/03": 5},'
            ' "proj2": {"2016/01/02": 4,'
                       '"2016/01/04": 6}}'
            )
    assert(get_commits_from_text(text) ==
        {'proj1': {
            date(2016, 1, 1): 3,
            date(2016, 1, 3): 5},
         'proj2': {
            date(2016, 1, 2): 4,
            date(2016, 1, 4): 6}})

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
