Hyuki-CVS-Graph
===============

Usage
=====

.. code:: bash

    hyuki-graph [option] [base_dir]

where, ``base_dir``\ is a the most top directory which is watched by this program.

Note that default ``base_dir``\ is ``.``\ .


This is a tool like as  `taking-star-table with color <https://note.mu/hyuki/n/n9a6e7c1e0d7b>`__ (ja),
which considered by Mr. Hyuki.

This tool makes table which is written project-name, day number from today and commit-status.

Also, if there is ``hyuki_graph.json`` or ``hyuki_graph.yaml`` file in directory,
which this program watch, this program make a table
by using commits number which got by CVS and content of the file.

Furtheremore, if cross point which project-name and day number is written D by red color,
this means that the project does not committed.

If it is written M by yellow color, this means that the project is committed some times less than 10.

If it is written L by green color, this means that the project is committed some times more than or equal to 10.


Syntax of Input File
======================

This program receives following syntax files.

As json syntax:

.. code::

  {
    project name: {
      date: commit number,
      date: commit number,
      e.t.c.
    },
    project name: {
      date: commit number,
      date: commit number,
      e.t.c.
    }
    e.t.c.
  }

where, date is a string which has form like "2000/01/01" or "2000-01-01".

As yaml syntax, like json syntax:

.. code::

  project name:
    date: commit number
    date: commit number
    e.t.c.
  project name:
    date: commit number
    date: commit number
    e.t.c.

If you want to use yaml syntax, import PyYaml package in manually:

.. code::

    pip install PyYaml

Options
=========

- ``-n``, ``--day-num``: indicate number of day, whcih is watched by this program.
- ``-a``, ``--author``: indicate name of committer.
- ``-m``, ``--medium-sep``: If more than or equal to number of commit is committed, printted L.
   Default value is 10.
- ``--DA``, ``--dead_or_alive``: Showing D and A instead of showing D, M and L.
   If there is no commit, D is printted. And there is it, A is printted.
- ``-M``, ``--monochrome``: don't show color
- ``--show-commit-numbers``, ``-c``: show commit numbers
- ``-f``, ``--file``: indicate input files by separating by space.
  Default of this value is "hyuki_graph.json hyuki_graph.yaml".
- ``--FO, --file-only``: watch only input file not watching CVS
- ``--t``, ``--file-type``: indicate format of input files. Please indicate json or yaml.
- ``-r``, ``--only-running``: show only activate project

However this is not a option, we don't not watched input file by ``--file=""``.


How to install
================

.. code:: bash

    % pip install hyuki-cvs-graph

or

.. code:: bash

    % python setup.py install


Requirements
==============

-  python
-  If you deal with git-repository, ``git``\ command
-  If you deal with hg-repository, ``hg``\ command

LICENSE
=======

MIT
