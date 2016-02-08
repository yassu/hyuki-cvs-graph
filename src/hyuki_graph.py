#!/usr/bin/env python3
# coding: UTF-8

import os
import datetime
import pprint
import subprocess
from optparse import OptionParser

__VERSION__ = '0.0.1'

def get_commits_log(commits):
    dead  = '\033[91m' + "D" + '\033[0m'
    alive = '\033[92m' + "A" + '\033[0m'
    dates = list(get_dates())
    projects = set()

    logs = dict() # dictionary from tuple of projname and date to dead or alive
    for path, commits in commits.items():
        project = get_str_projname(path)
        for date, commit_num in commits.items():
            logs[(project, date)] = alive if (commit_num > 0) else dead
            projects.add(project)

    splitted_logs = []
    proj_len = max(len(project) for project in projects) + 1

    date_log = ' ' * proj_len
    date_cnt = 0
    for date in dates:
        date_log += str(date_cnt) + ' '
        date_cnt += 1
    splitted_logs.append(date_log)

    proj_log = ''
    for proj in projects:
        proj_log = proj + ' ' * (proj_len - len(proj))
        for date in dates:
            proj_log += logs[(proj, date)] + ' '

        splitted_logs.append(proj_log)

    return '\n'.join(splitted_logs)

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
        numbers[datetime.date(year, month, day)] = log.count(_format)
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
    today = datetime.date.today()
    for days in [7 - days for days in range(7 + 1)]:
        date = today - datetime.timedelta(days=days)
        yield datetime.date(date.year, date.month, date.day)

def get_str_projname(project):
    return project.split('/')[-1]

def get_parser():
    parser = OptionParser(version=__VERSION__)
    return parser

def main():
    opts, args = get_parser().parse_args()
    base_path = '.'
    if len(args) >= 1:
        base_path = os.path.abspath(args[0])

    commits = dict()
    projects = list(get_cvs_dirs('.'))
    for path in projects:
        commits[path] = get_commit_numbers(path)

    commits_log = get_commits_log(commits)
    print(commits_log)


if __name__ == '__main__':
    main()
