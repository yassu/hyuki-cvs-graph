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

__VERSION__ = '0.2.8'

PYTHON_VERSION = sys.version_info[0]    # major version

DEFAULT_NUMBER_OF_DAY = 7
DEFAULT_MEDIUM_SEP = 10
HOME_DIR = os.path.expanduser('~') + os.path.sep
DEFAULT_USE_FILENAME = " ".join([
                        os.path.join(HOME_DIR, 'hyuki_graph.json'),
                        os.path.join(HOME_DIR, 'hyuki_graph.yaml'),
                        'hyuki_graph.json',
                        'hyuki_graph.yaml'
                        ])


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


class StatusCell(str):

    def set_color(self, color):
        self._color = color

    @property
    def color(self):
        return str(self._color)

    @property
    def colored_text(self):
        return '\033[{}m{}\033[0m'.format(self.color, str(self))

DEAD = StatusCell('D')
DEAD.set_color('91')

MEDIUM = StatusCell('M')
MEDIUM.set_color(93)

LARGE = StatusCell('L')
LARGE.set_color(92)

ALIVE = StatusCell('A')
ALIVE.set_color(92)


def get_dead_or_alive_number(n, medium_sep=DEFAULT_MEDIUM_SEP):
    if n == 0:
        return DEAD
    else:
        return ALIVE


def is_correct_as_date(_date):
    _date = get_str(_date)
    if isinstance(_date, str) is False:
        return False

    if '/' in _date:
        sep = '/'
    elif '-' in _date:
        sep = '-'
    else:
        return False

    if len(_date.split(sep)) != 3:
        return False

    year, month, day = _date.split(sep)
    if not year.isdigit() or not month.isdigit() or not day.isdigit():
        return False

    year = int(year)
    month = int(month)
    day = int(day)

    try:
        datetime.date(year, month, day)
    except ValueError:
        return False
    return True


def get_str(s):
    # if s is object of unicode, return str(s)
    # else: return s
    if PYTHON_VERSION == 2 and isinstance(s, unicode):
        return str(s)
    else:
        return s


def is_correct_as_inputfile_data(data):
    if isinstance(data, dict) is False:
        return False

    for proj, commits_to_status in data.items():
        if isinstance(get_str(proj), str) is False:
            return False
        if isinstance(commits_to_status, dict) is False:
            return False
        for _date, num in commits_to_status.items():
            if is_correct_as_date(_date) is False:
                return False
            if isinstance(num, int) is False:
                return False

    return True


def get_date_from_text(text):
    if '/' in text:
        sep = '/'
    elif '-' in text:
        sep = '-'
    else:
        raise TypeError('{} is illegal as a date.'.format(text))

    if (len(text.split(sep)) != 3):
        raise TypeError('{} is illegal as a date.'.format(text))

    year, month, day = text.split(sep)
    if (not year.isdigit() or
            not month.isdigit() or
            not day.isdigit()):
        raise TypeError('{} is illegal as a date.'.format(text))
    try:
        return datetime.date(int(year), int(month), int(day))
    except ValueError:
        raise TypeError('{} is not in range for date.'.format(text))


def get_ext(path, default_ext=None):
    if default_ext is not None:
        return default_ext

    ext = os.path.splitext(path)[-1]
    if len(ext) >= 1:
        return ext[1:]
    else:
        return None


def get_commits_from_textfile(base_path, use_files=DEFAULT_USE_FILENAME,
                              file_type=None):
    use_filenames = use_files.split()
    for i in range(len(use_filenames)):
        use_filenames[i] = os.path.join(base_path, use_filenames[i])

    commits = dict()

    for fname in use_filenames:
        if not os.path.isfile(fname):
            continue

        with open(fname) as f:
            ext = file_type if file_type else get_ext(fname)
            if ext in {'json', 'yaml'}:
                try:
                    commits.update(get_commits_from_text(f.read(), ext))
                except TypeError as ex:
                    sys.stderr.write("WARNING: {}\n".format(ex.message))
                except ValueError:
                    sys.stderr.write("WARNING: {} has illegal format as {}.\n".
                                     format(fname, ext))
            else:
                sys.stderr.write('{} is a illegal file as input file.\n'.
                                 format(fname))
    return commits


def get_commits_from_text(text, ext):
    if ext == 'json':
        load_func = json.loads
    elif ext == 'yaml':
        load_func = yaml.load
    else:
        raise TypeError('extension {} is not supported.'.format(ext))

    try:
        commits = load_func(text)
    except ValueError:
        raise ValueError("Illegal data format")

    if not is_correct_as_inputfile_data(commits):
        raise TypeError('illegal data structure in input file')

    true_data = defaultdict(lambda: defaultdict(int))
    for proj, date_status in commits.items():
        dates = date_status.keys()
        for date in dates:
            date_d = get_date_from_text(date)
            true_data[proj][date_d] = date_status[date]
    return dict(true_data)

def get_digits(days, commits, show_commits_number):
        # if days >= 10: return 2
        # elif show_commits_number and max(proj[commits]) >= 10 return 2
        # else return 1
    if len(days) >= 10:
        return 2
    if not show_commits_number:
        # print('show commits number')
        return 1
    for proj, date_to_commitnum in commits.items():
        for _, commitnum in date_to_commitnum.items():
            if commitnum >= 10:
                return 2

    # print('last')
    return 1


def get_commits_log(commits, day_num, medium_sep, dead_or_alive,
                    monochrome=False,
                    show_commits_number=False,
                    only_running=False,
                    is_hide_status=False):
    dates = list(get_dates(day_num))
    projects = set()

    if dead_or_alive:
        status_func = get_dead_or_alive_number
    else:
        status_func = get_dead_medium_or_large

    logs = dict()  # dictionary from tuple of projname and date to status
    for path, _commits in commits.items():
        project = get_str_projname(path)
        for date, commit_num in _commits.items():
            if not show_commits_number:
                logs[(project, date)] = status_func(commit_num, medium_sep)
            else:
                num = StatusCell(str(commit_num))
                color = status_func(commit_num, medium_sep).color
                num.set_color(color)
                logs[(project, date)] = num
            projects.add(project)

        if only_running and (
                (set([logs[(project, date)] for date in dates]) == set([DEAD]))
                or set([logs[(project, date)] for date in dates]) == set(['0'])
                    ):
            projects.remove(project)
            for date in dates:
                del(logs[(project, date)])

    if projects == set():
        sys.stderr.write("WARNING: There doesn't exist repository which "
                         "this program can display.\n")
        sys.exit()

    splitted_logs = []
    proj_len = max(len(project) for project in projects) + 1

    if not is_hide_status:
        date_log = ' ' * proj_len
        date_cnt = 0
        space_digit = get_digits(dates, commits, show_commits_number)
        for date in dates:
            # date_log += str(date_cnt) + ' '
            date_log += ('%' + str(space_digit) + 'd') % date_cnt + ' '
            date_cnt += 1
        splitted_logs.append(date_log)

    proj_log = ''
    for proj in sorted(projects, key=lambda s: s.lower()):
        proj_log = proj + ' ' * (proj_len - len(proj))
        if not is_hide_status:
            for date in dates:

                if monochrome:
                    s = logs[(proj, date)]
                else:
                    s = logs[(proj, date)].colored_text
                proj_log += ' ' * (space_digit - len(logs[(proj, date)])) + s + ' '

        splitted_logs.append(proj_log)

    return '\n'.join(splitted_logs)


def get_revision_cvs(path):
    if ('git' in CVSS and os.path.isdir(os.path.join(path, '.git'))):
        return 'git'
    elif ('hg' in CVSS and os.path.isdir(os.path.join(path, '.hg'))):
        return 'hg'
    else:
        return None


def get_commit_numbers(path, day_num, author, is_log=False):
    first_chdir = os.getcwd()
    os.chdir(path)

    cvs = get_revision_cvs(path)
    if cvs is None:
        return {}

    if cvs == 'git':
        log_cmd = 'log' if is_log else "reflog"
        log = subprocess.check_output(
            ['git', log_cmd , '--oneline', '--date=short',
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
    commits = deepcopy(commits)
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
            commits1[proj][_date] = commits1.get(
                proj, {}).get(_date, 0) + _status
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
        '-c', '--show-commit-numbers',
        action='store_true',
        default=False,
        dest='show_commit_numbers',
        help='show commit numbers for all projects'
    )
    parser.add_option(
        '--log',
        action='store_true',
        dest='is_log',
        help='use log (not reflog) command'
    )
    parser.add_option(
        '--monochrome', '-M',
        action='store_true',
        dest='monochrome',
        default=False,
        help="don't show color"
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
    parser.add_option(
        '-t', '--file-type',
        action='store',
        help="indicate type of input file (json or yaml)",
        dest='file_type',
    )
    parser.add_option(
        '-r', '--only-running',
        action='store_true',
        default=False,
        help="show only running projects",
        dest='only_running',
    )
    parser.add_option(
        '--hide-status',
        action='store_true',
        default=False,
        help='show only project name, without status',
        dest='is_hide_status'
    )
    return parser


def main():
    opts, args = get_parser().parse_args()

    if len(args) > 1:
        sys.stderr.write("Number of arguments should be zero or one.\n")
        sys.exit()

    if not opts.day_num:
        opts.day_num = DEFAULT_NUMBER_OF_DAY
    base_path = os.path.abspath('.' if len(args) == 0 else args[0])

    commits = dict()
    projects = list(get_cvs_dirs(base_path))

    if not opts.is_file_only:
        projects = list(get_cvs_dirs(base_path))
        for path in projects:
            commits[get_str_projname(path)] = get_commit_numbers(
                path, opts.day_num, opts.author, is_log=opts.is_log)

    try:
        commits_from_textfile = fill_commits_by_zero(
            get_commits_from_textfile(base_path, use_files=opts.filenames,
                                      file_type=opts.file_type))
    except ValueError as ex:
        sys.stderr.write(ex.message)

    commits = update_as_commits(commits, commits_from_textfile)
    # pprint.pprint(commits)

    commits_log = get_commits_log(commits, opts.day_num, opts.medium_sep,
                                  opts.is_dead_or_alive,
                                  monochrome=opts.monochrome,
                                  show_commits_number=opts.show_commit_numbers,
                                  only_running=opts.only_running,
                                  is_hide_status=opts.is_hide_status)
    print(commits_log)


if __name__ == '__main__':
    main()
