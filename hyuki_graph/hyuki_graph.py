#!/usr/bin/env python3
# coding: UTF-8

import os
import sys
import datetime
from copy import deepcopy
# import pprint
import subprocess
import re
from optparse import OptionParser
import json
import yaml
from collections import defaultdict

__VERSION__ = '0.2.3'

DEFAULT_NUMBER_OF_DAY = 7
DEFAULT_MEDIUM_SEP = 10
DEFAULT_USE_FILENAME = ' hyuki_graph.json hyuki_graph.yaml'

DEAD = '\033[91m' + "D" + '\033[0m'     # dead commit
MEDIUM = '\033[93m' + "M" + '\033[0m'   # medium commit
LARGE = '\033[92m' + "L" + '\033[0m'    # Large commit
ALIVE = '\033[92m' + "A" + '\033[0m'    # Alive commit

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


def get_dead_medium_or_large(n, medium_sep=DEFAULT_MEDIUM_SEP):
    if n == 0:
        return DEAD
    elif n < medium_sep:
        return MEDIUM
    else:
        return LARGE

def get_dead_or_alive_number(n, medium_sep=DEFAULT_MEDIUM_SEP):
    if n == 0:
        return DEAD
    else:
        return ALIVE



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

def get_commits_from_textfile(base_path, use_files=DEFAULT_USE_FILENAME):
    use_filenames = use_files.split()
    for i in range(len(use_filenames)):
        use_filenames[i] = os.path.join(base_path, use_filenames[i])

    commits = dict()

    for fname in use_filenames:
        if not os.path.isfile(fname):
            continue

        with open(fname) as f:
            ext = (os.path.splitext(fname)[-1])[1:]
            commits.update(get_commits_from_text(f.read(), ext))
    return commits

def get_commits_from_text(text, ext):
    if ext == 'json':
        load_func = json.loads
    elif ext == 'yaml':
        load_func = yaml.load
    jdata = load_func(text)
    true_data = defaultdict(lambda: defaultdict(int))
    for proj, date_status in jdata.items():
        dates = date_status.keys()
        for date in dates:
            date_d = get_date_from_text(date)
            true_data[proj][date_d] = date_status[date]
    return dict(true_data)


def get_commits_log(commits, day_num, medium_sep, dead_or_alive):
    dates = list(get_dates(day_num))
    projects = set()

    if dead_or_alive:
        status_func = get_dead_or_alive_number
    else:
        status_func = get_dead_medium_or_large

    logs = dict()  # dictionary from tuple of projname and date to status
    for path, commits in commits.items():
        project = get_str_projname(path)
        for date, commit_num in commits.items():
            logs[(project, date)] = status_func(commit_num, medium_sep)
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

def fill_commits_by_zero(commits, start_day=datetime.date.today(),
        days=DEFAULT_NUMBER_OF_DAY):
        # commitsのstart_dayからdaysまでの間の
        # 未定義な要素を0としたdictを返す.
        ret_commits = dict()
        for proj, date_to_commitnum in commits.items():
            for j in range(days + 1):
                _date = start_day - datetime.timedelta(days=j)
                commits[proj][_date] = commits[proj].get(_date, 0)
        return commits

def update_as_commits(commits1, commits2):
    commits1 = deepcopy(commits1)
    for proj, _date_to_status in commits2.items():
        for _date, _status in _date_to_status.items():
            if proj not in commits1:
                commits1[proj] = dict()
            commits1[proj][_date] = commits1.get(proj, {}).get(_date, 0) + _status
    return commits1

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
    parser.add_option(
        '--file', '-f',
        action='store',
        default=DEFAULT_USE_FILENAME,
        dest='filenames',
        help='indicate all filenames that you want to use'
    )
    parser.add_option(
        '--FO', '--file-only',
        action='store_true',
        default=False,
        dest='is_file_only',
        help='this program not watch cvs directories.'
    )
    return parser


def main():
    opts, args = get_parser().parse_args()
    if not opts.day_num:
        opts.day_num = DEFAULT_NUMBER_OF_DAY
    base_path = os.path.abspath('.' if len(args) == 0 else args[0])

    commits = dict()
    projects = list(get_cvs_dirs(base_path))

    if not opts.is_file_only:
        projects = list(get_cvs_dirs(base_path))
        for path in projects:
            commits[get_str_projname(path)] = get_commit_numbers(
                path, opts.day_num, opts.author)

    commits_from_textfile = fill_commits_by_zero(
        get_commits_from_textfile(base_path, opts.filenames))

    commits = update_as_commits(commits, commits_from_textfile)
    # pprint.pprint(commits)

    commits_log = get_commits_log(commits, opts.day_num, opts.medium_sep,
                                  opts.is_dead_or_alive)
    print(commits_log)


if __name__ == '__main__':
    main()
