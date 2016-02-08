#!/usr/bin/env python3
# coding: UTF-8

import os
import sys
import datetime
import pprint
import subprocess
from optparse import OptionParser

__VERSION__ = '0.0.1'

DEFAULT_NUMBER_OF_DAY = 7

def get_execuable_cvss():
    execuable_cvss = []
    try:
        subprocess.check_output(['git', '--version'])
        execuable_cvss.append('git')
    except FileNotFoundError as ex:
        pass

    try:
        subprocess.check_output(['hg', '--version'])
        execuable_cvss.append('hg')
    except FileNotFoundError as ex:
        pass

    return execuable_cvss

CVSS = get_execuable_cvss()

def get_commits_log(commits, day_num):
    dead = '\033[91m' + "D" + '\033[0m'
    alive = '\033[92m' + "A" + '\033[0m'
    dates = list(get_dates(day_num))
    projects = set()

    logs = dict()  # dictionary from tuple of projname and date to dead or alive
    for path, commits in commits.items():
        project = get_str_projname(path)
        for date, commit_num in commits.items():
            logs[(project, date)] = alive if (commit_num > 0) else dead
            projects.add(project)

    if projects == set():
        sys.stderr.write("WARNING: There doesn't exist repository which"
                         "this program can display.\n")
        sys.exit()

    splitted_logs = []
    proj_len = max(len(project) for project in projects) + 1

    date_log = ' ' * proj_len
    date_cnt = 0
    for date in dates:
        date_log += str(date_cnt) + ' '
        date_cnt += 1
    splitted_logs.append(date_log)

    proj_log = ''
    for proj in sorted(projects):
        proj_log = proj + ' ' * (proj_len - len(proj))
        for date in dates:
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


def get_commit_numbers(path, day_num):
    os.chdir(path)

    cvs = get_revision_cvs(path)
    if cvs is None:
        return {}

    if cvs == 'git':
        log = subprocess.check_output(
            ['git', 'log', '--oneline', '--date=short',
                '--pretty=format:\"%ad\"']).decode('utf-8')
    elif cvs == 'hg':
        log = subprocess.check_output(['hg', 'log', '--style=compact'])

    numbers = dict()

    for date in get_dates(day_num):
        year, month, day = date.year, date.month, date.day
        _format = "%04d-%02d-%02d" % (year, month, day)
        numbers[datetime.date(year, month, day)] = log.count(_format)
    return numbers


def get_children_dirs(path):
    yield os.path.abspath(path)
    for (root, dirs, _) in os.walk(path):
        yield os.path.abspath(root)


def get_cvs_dirs(path):
    for p in get_children_dirs(path):
        if os.path.isdir(p + '/.git'):
            yield p
        elif os.path.isdir(p + '/.hg'):
            yield p


def get_dates(day_num):
    today = datetime.date.today()
    for days in [day_num - days for days in range(day_num + 1)]:
        date = today - datetime.timedelta(days=days)
        yield datetime.date(date.year, date.month, date.day)


def get_str_projname(project):
    return project.split('/')[-1]


def get_parser():
    usage = "Usage: hyuki-graph [option] [base_dir]"
    parser = OptionParser(usage=usage, version=__VERSION__)
    parser.add_option(
        '--day-num', '-n',
        action='store',
        dest='day_num',
        type=int,
        help='number of considering day')
    return parser


def main():
    opts, args = get_parser().parse_args()
    if not opts.day_num:
        opts.day_num = DEFAULT_NUMBER_OF_DAY
    base_path = os.path.abspath('.' if len(args) == 0 else args[0])

    commits = dict()
    projects = list(get_cvs_dirs(base_path))
    for path in projects:
        commits[path] = get_commit_numbers(path, opts.day_num)

    commits_log = get_commits_log(commits, opts.day_num)
    print(commits_log)


if __name__ == '__main__':
    main()
