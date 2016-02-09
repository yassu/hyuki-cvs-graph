Hyuki-CVS-Graph
===============
.. image:: https://travis-ci.org/yassu/hyuki-cvs-graph.svg?branch=master
    :target: https://travis-ci.org/yassu/hyuki-cvs-graph

This is a tool like as  `taking-star-table with color <https://note.mu/hyuki/n/n9a6e7c1e0d7b>`__ (ja),
which considered by Mr. Hyuki.

This tool makes table which is written project-name, day number from today and commit-status.

Furtheremore, if cross point which project-name and day number is written D by red color,
this means that the project does not committed.

If it is written M by yellow color, this means that the project is committed some times less than 10.

If it is written L by green color, this means that the project is committed some times more than or equal to 10.

Usage
=====

.. code:: bash

    hyuki-graph [option] [base_dir]

where, ``base_dir``\ is a the most top directory which is watched by this program.

Note that default ``base_dir``\ is ``.``\ .

Options
=========

-  ``-n``, ``--day-num``: indicate number of day, whcih is watched by this program.
-  ``-a``, ``--author``: indicate name of committer.
-  ``-m``, ``--medium-sep``: If more than or equal to number of commit is committed, printted L.
   Default value is 10.
-  ``--DA``, ``--dead_or_alive``: Showing D and A instead of showing D, M and L.
   If there is no commit, D is printted. And there is it, A is printted.

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
