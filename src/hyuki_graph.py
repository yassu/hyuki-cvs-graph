#!/usr/bin/env python3
# coding: UTF-8

import os
import datetime
import pprint
import subprocess
from PIL import Image, ImageDraw

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
        numbers[datetime.datetime(year, month, day)] = log.count(_format)
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
    today = datetime.datetime.today()
    for days in [7 - days for days in range(7 + 1)]:
        date = today - datetime.timedelta(days=days)
        yield datetime.datetime(date.year, date.month, date.day)

def main():
    commits = dict()
    projects = list(get_cvs_dirs('.'))
    for path in projects:
        commits[path] = get_commit_numbers(path)

    right_span = 10
    left_span = 10
    cell_width = 40
    cell_height = cell_width
    image_matrix = Image.new('RGB',
        (7 * cell_width, cell_height * (len(projects) - 1 + 1)),
        (255, 255, 255))
    draw = ImageDraw.Draw(image_matrix)

    for i, date in enumerate(get_dates()):
        # write date as text
        date_text = "%04d/%02d/%02d" % (date.year, date.month, date.day)
        draw.text((left_span + i * cell_width, 0), date_text, fill='#000000')

        for j, project in enumerate(projects):
            print(commits[project])
            print(date)
            print(type(date))

            if commits[project][date] != 0:
                draw.rectangle(
                    (
                        (i * cell_width, (j + 1) * cell_height),
                        ((i + 1) * cell_width, (j + 2) * cell_height)
                    ),
                    fill=(0, 0, 256), outline=(0, 0, 0))

    image_matrix.show()

main()
