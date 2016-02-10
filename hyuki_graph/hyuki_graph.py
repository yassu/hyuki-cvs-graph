#!/usr/bin/env python3
# coding: UTF-8

import os
import sys
import datetime
# import pprint
import subprocess
import re
from optparse import OptionParser
import json
from collections import defaultdict

DEFAULT_NUMBER_OF_DAY = 7
DEFAULT_MEDIUM_SEP = 10

__VERSION__ = '0.1.0'

def get_execuable_cvss():
    execuable_cvss = []
    try:
        subprocess.check_output(['git', '--version'])
        execuable_cvss.append('git')
    except FileNotFoundError:
        pass

    try:
        subprocess.check_output(['hg', '--version'])
        execuable_cvss.append('hg')
    except FileNotFoundError:
        pass

    return execuable_cvss

CVSS = get_execuable_cvss()

def get_date_from_text(text):
    if (len(text.split(os.path.sep)) != 3):
        raise TypeError('{} is illegal as a date.'.format(text))

    year, month, day = text.split(os.path.sep)
    if (not year.isdigit() or
            not month.isdigit() or
            not day.isdigit()):
        raise TypeError('{} is illegal as a date.'.format(text))
    try:
        return datetime.date(int(year), int(month), int(day))
    except ValueError:
        raise TypeError('{} is not in range for date.'.format(text))

def get_commits_from_text(text):
    jdata = json.loads(text)
    true_data = defaultdict(lambda: defaultdict(int))
    for proj, date_status in jdata.items():
        dates = date_status.keys()
        for date in dates:
            date_d = get_date_from_text(date)
            true_data[proj][date_d] = \
                date_status[date]
    return true_data


def get_commits_log(commits, day_num, medium_sep, dead_or_alive):
    dead = '\033[91m' + "D" + '\033[0m'     # dead commit
    medium = '\033[93m' + "M" + '\033[0m'   # medium commit
    large = '\033[92m' + "L" + '\033[0m'    # Large commit
    alive = '\033[92m' + "A" + '\033[0m'    # Alive commit
    dates = list(get_dates(day_num))
    projects = set()

    if dead_or_alive:
        status_func = lambda c: dead if c == 0 else alive
    else:
        status_func = lambda c: dead if c == 0 else \
            medium if c < medium_sep - 1 else \
            large

    logs = dict()  # dictionary from tuple of projname and date to status
    for path, commits in commits.items():
        project = get_str_projname(path)
        for date, commit_num in commits.items():
            logs[(project, date)] = status_func(commit_num)
            projects.add(project)

    if projects == set():
        sys.stderr.write("WARNING: There doesn't exist repository which "
                         "this program can display.\n")
        sys.exit()

    splitted_logs = []
    proj_len = max(len(project) for project in projects) + 1

    more_than_nine = (day_num >= 10)

    date_log = ' ' * proj_len
    date_cnt = 0
    space_digit = 2 if more_than_nine else 1
    for date in dates:
        # date_log += str(date_cnt) + ' '
        date_log += ('%' + str(space_digit) + 'd') % date_cnt + ' '
        date_cnt += 1
    splitted_logs.append(date_log)

    proj_log = ''
    for proj in sorted(projects, key=lambda s: s.lower()):
        proj_log = proj + ' ' * (proj_len - len(proj))
        for date in dates:
            if more_than_nine:
                proj_log += ' '
            proj_log += logs[(proj, date)] + ' '

        splitted_logs.append(proj_log)

    return '\n'.join(splitted_logs)


def get_revision_cvs(path):
    if ('git' in CVSS and os.path.isdir(os.path.join(path, '.git'))):
        return 'git'
    elif ('hg' in CVSS and os.path.isdir(os.path.join(path, '.hg'))):
        return 'hg'
    else:
        return None


def get_commit_numbers(path, day_num, author):
    first_chdir = os.getcwd()
    os.chdir(path)

    cvs = get_revision_cvs(path)
    if cvs is None:
        return {}

    if cvs == 'git':
        log = subprocess.check_output(
            ['git', 'reflog', '--oneline', '--date=short',
                '--pretty=format:%ad %an']).decode('utf-8')
    elif cvs == 'hg':
        log = subprocess.check_output(
            ['hg', 'log',
             '--template', r'{date|shortdate} {author|person}\n'
             ]).decode('utf-8')

    numbers = dict()

    for date in get_dates(day_num):
        year, month, day = date.year, date.month, date.day
        _format = "%04d-%02d-%02d" % (year, month, day)
        pat = r"\b" + _format + r"\b"
        if author is not None:
            pat += r" \b(" + "|".join(author.split()) + r")\b"
        numbers[datetime.date(year, month, day)] = len(re.findall(pat, log))
    os.chdir(first_chdir)
    return numbers


def get_children_dirs(path):
    yield os.path.abspath(path)
    for (root, dirs, _) in os.walk(path):
        yield os.path.abspath(root)


def get_cvs_dirs(path):
    for p in get_children_dirs(path):
        if os.path.isdir(os.path.join(p, '.git')):
            yield p
        elif os.path.isdir(os.path.join(p, '.hg')):
            yield p


def get_dates(day_num):
    today = datetime.date.today()
    for days in [day_num - days for days in range(day_num + 1)]:
        date = today - datetime.timedelta(days=days)
        yield datetime.date(date.year, date.month, date.day)


def get_str_projname(project):
    return os.path.abspath(project).split(os.path.sep)[-1]


def get_parser():
    usage = "Usage: hyuki-graph [option] [base_dir]"
    parser = OptionParser(usage=usage, version=__VERSION__)
    parser.add_option(
        '--day-num', '-n',
        action='store',
        dest='day_num',
        type=int,
        help='number of considering day')
    parser.add_option(
        '--author', '-a',
        action='store',
        dest='author',
        help='indicate author name')
    parser.add_option(
        '--medium-sep', '-m',
        action='store',
        default=DEFAULT_MEDIUM_SEP,
        type=int,
        help=('If number of commit is less than this value, '
              'M is written.')
    )
    parser.add_option(
        '--dead-or-alive', '--DA',
        action='store_true',
        dest='is_dead_or_alive',
        help=('show only D and A')
    )
    return parser


def main():
    opts, args = get_parser().parse_args()
    if not opts.day_num:
        opts.day_num = DEFAULT_NUMBER_OF_DAY
    base_path = os.path.abspath('.' if len(args) == 0 else args[0])

    commits = dict()
    projects = list(get_cvs_dirs(base_path))
    for path in projects:
        commits[path] = get_commit_numbers(path, opts.day_num, opts.author)

    commits_log = get_commits_log(commits, opts.day_num, opts.medium_sep,
                                  opts.is_dead_or_alive)
    print(commits_log)


if __name__ == '__main__':
    main()
