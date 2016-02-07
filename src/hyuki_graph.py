#!/usr/bin/env python3
# coding: UTF-8
import os

def get_children_dirs(path):
    for (_, dirs, _) in os.walk(path):
        for d in dirs:
            yield os.path.abspath(d)

print(list(get_children_dirs('.')))
