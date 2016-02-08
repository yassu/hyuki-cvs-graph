#!/usr/bin/env python3
# coding: UTF-8

import os
import datetime
import pprint
import subprocess
from PIL import Image, ImageDraw, ImageFont

class ImageList(list):
    # list of str objects
    # this object has image method, which returns image object

    def __init__(self):
        list.__init__(self)
        self._default_width = None

    @property
    def images(self, height=30, xpad=3, ypad=3):
        font_size = 13
        font = ImageFont.truetype('FreeSans.ttf', font_size)
        height = ypad + font_size + ypad
        for i in range(self):
            width = xpad + len(self[i]) + xpad
            img = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), self[i], font=font, fill="#000000")
            yield img

    @property
    def image(self, height=30, xpad=3, ypad=3):
        # width = sum()
        font_size = 13
        font = ImageFont.truetype('FreeSans.ttf', font_size)
        height = ypad + font_size + ypad
        if self:
            width = sum([len(s) for s in self]) * font_size + \
                (len(self) - 1)*xpad
        else:
            width = self._default_width
        img = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        for i in range(len(self)):
            draw.text(
                (sum(len(s) for s in self[:i]) * font_size,
                0),
                self[i],
                font=font, fill='#000000')
        return img

    def set_default_width(self, width):
        self._default_width = width

class ImageMatrix(list):
    # list of ImageList object
    # this object has image method, which returns image object

    @property
    def image(self):
        width = 0
        for img_y in self:
            width += max([img.size[0] for img in img_y])

        height = 0
        for x in range(len(self)):
            height += max([img.size[1] for img in
                [self[y][x] for y in range(len(self))]
            ])
        print(width, height)
        img = Image.new('RGB',
                (width, height),
                (255, 255, 255))

        return img

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

def get_str_projname(project):
    return project.split('/')[-1]

def main():
    commits = dict()
    projects = list(get_cvs_dirs('.'))
    pprint.pprint(projects)
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

            if commits[project][date] != 0:
                draw.rectangle(
                    (
                        ((i + 1) * cell_width, (j + 1) * cell_height),
                        ((i + 2) * cell_width, (j + 2) * cell_height)
                    ),
                    fill=(0, 0, 256), outline=(0, 0, 0))

    image_matrix.show()

if __name__ == '__main__':
    # main()
    img_list1 = ImageList()
    img_list1.append("Hello")
    img_list1.append("World")

    img_list2 = ImageList()
    img_list2.append("Hello2")
    img_list2.append("World2")

    img_mat = ImageMatrix()
    img_mat.append(img_list1)
    img_mat.append(img_list2)
    img = img_mat.image
    img.show()
