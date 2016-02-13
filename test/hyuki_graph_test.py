#!/usr/bin/env python
# coding: UTF-8

from unittest import TestCase
from nose.tools import raises
from hyuki_graph.hyuki_graph import(
    DEFAULT_MEDIUM_SEP,
    DEAD, ALIVE, MEDIUM, LARGE,
    StatusCell,
    get_dead_or_alive_number, get_dead_medium_or_large,
    is_correct_as_date, is_correct_as_inputfile_data,
    get_dates, get_str_projname, get_commits_from_text,
    get_ext,
    get_date_from_text, fill_commits_by_zero, update_as_commits
)
from datetime import date, timedelta
import os.path


def get_dead_medium_or_large_test0():
    assert(get_dead_medium_or_large(0) == DEAD)


def get_dead_medium_or_large_test2():
    assert(get_dead_medium_or_large(1) == MEDIUM)


def get_dead_medium_or_large_test3():
    assert(get_dead_medium_or_large(DEFAULT_MEDIUM_SEP - 1) == MEDIUM)


def get_dead_medium_or_large_test1():
    assert(get_dead_medium_or_large(DEFAULT_MEDIUM_SEP) == LARGE)


def get_dead_or_alive_number_test0():
    assert(get_dead_or_alive_number(0) == DEAD)


def get_dead_or_alive_number_test1():
    assert(get_dead_or_alive_number(1) == ALIVE)


def get_dead_or_alive_number_test2():
    assert(get_dead_or_alive_number(10) == ALIVE)

class StatusCellTestCase(TestCase):
    def color_test(self):
        c = StatusCell('D')
        c.set_color(91)
        assert(c.color == '91')

    def color_text_test(self):
        c = StatusCell('D')
        c.set_color(91)
        assert(c.colored_text == '\033[91m' + "D" + '\033[0m')


def is_correct_as_date_test0():
    assert(is_correct_as_date(set()) is False)

def is_correct_as_date_test1():
    assert(is_correct_as_date("2015/03/21") is True)


def is_correct_as_date_test2():
    assert(is_correct_as_date("2015-03-21") is True)


def is_correct_as_date_test3():
    assert(is_correct_as_date("2015/03-21") is False)

def is_correct_as_date_test4():
    assert(is_correct_as_date("2015/03/99") is False)


def is_correct_as_inputfile_data_test1():
    assert(is_correct_as_inputfile_data(1) is False)

def is_correct_as_inputfile_data_test2():
    assert(is_correct_as_inputfile_data({"proj": 2}) is False)


def is_correct_as_inputfile_data_test3():
    assert(is_correct_as_inputfile_data({"proj": "2015/03/20"}) is False)

def is_correct_as_inputfile_data_test4():
    assert(is_correct_as_inputfile_data({"proj": {"2015/03/20": 2}}) is True)


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


def get_date_from_text_test7():
    assert(get_date_from_text('2015-03-21') ==
           date(2015, 3, 21))


@raises(TypeError)
def get_date_from_text_test8():
    get_date_from_text('2015/03-21')

def get_ext_test1():
    assert(get_ext('json.json') == 'json')

def get_ext_test2():
    assert(get_ext('test.yaml') == 'yaml')

def get_ext_test3():
    assert(get_ext('test.yaml', 'json') == 'json')

def get_ext_test4():
    assert(get_ext('~/dev/') is None)


def get_commits_from_text_test0():
    text = '{}'
    assert(get_commits_from_text(text, 'json') == {})


def get_commits_from_text_test1():
    text = '{"proj1": {"2016/01/01": 3}}'
    assert(get_commits_from_text(text, 'json') ==
           {'proj1':
            {date(2016, 1, 1): 3}}
           )


def get_commits_from_text_test2():
    text = ('{"proj1": {"2016/01/01": 3,'
            '"2016/01/03": 5}}')
    assert(get_commits_from_text(text, 'json') ==
           {'proj1': {
            date(2016, 1, 1): 3,
            date(2016, 1, 3): 5}})


def get_commits_from_text_test3():
    text = ('{"proj1": {"2016/01/01": 3,'
            '"2016/01/03": 5},'
            ' "proj2": {"2016/01/02": 4,'
            '"2016/01/04": 6}}'
            )
    assert(get_commits_from_text(text, 'json') ==
           {'proj1': {
            date(2016, 1, 1): 3,
            date(2016, 1, 3): 5},
            'proj2': {
            date(2016, 1, 2): 4,
            date(2016, 1, 4): 6}})

@raises(TypeError)
def get_commits_from_text_test4():
    text = ('{"proj1": {"2016/01/01": 3,'
            '"2016/01/03": 5},'
            ' "proj2": {"2016/01/02": 4,'
            '"2016/01/04": 6}}'
            )
    get_commits_from_text(text, 'sjon')


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


def fill_commits_by_zero_test1():
    commits = {
        'proj1': {
            date(2016, 1, 1): 3,
            date(2016, 1, 3): 5},
        'proj2': {
            date(2016, 1, 2): 4,
            date(2016, 1, 4): 6}}
    assert(
        fill_commits_by_zero(commits, start_day=date(2016, 1, 4), days=3) == {
            'proj1': {
                date(2016, 1, 1): 3,
                date(2016, 1, 2): 0,
                date(2016, 1, 3): 5,
                date(2016, 1, 4): 0},
            'proj2': {
                date(2016, 1, 1): 0,
                date(2016, 1, 2): 4,
                date(2016, 1, 3): 0,
                date(2016, 1, 4): 6}
        }
    )


def update_as_commits_test():
    commits1 = {
        'proj1': {
            date(2016, 1, 1): 3,
            date(2016, 1, 3): 5},
        'proj2': {
            date(2016, 1, 2): 4,
            date(2016, 1, 4): 6}}
    commits2 = {
        'proj3': {
            date(2016, 1, 1): 2,
            date(2016, 1, 3): 3},
        'proj2': {
            date(2016, 1, 2): 1,
            date(2016, 1, 4): 9}}
    commits = update_as_commits(commits1, commits2)
    assert(commits == {
        'proj1': {
            date(2016, 1, 1): 3,
            date(2016, 1, 3): 5},
        'proj2': {
            date(2016, 1, 2): 5,
            date(2016, 1, 4): 15},
        'proj3': {
            date(2016, 1, 1): 2,
            date(2016, 1, 3): 3}
    })

    commits = update_as_commits(commits2, commits1)
    assert(commits == {
        'proj1': {
            date(2016, 1, 1): 3,
            date(2016, 1, 3): 5},
        'proj2': {
            date(2016, 1, 2): 5,
            date(2016, 1, 4): 15},
        'proj3': {
            date(2016, 1, 1): 2,
            date(2016, 1, 3): 3}
    })
