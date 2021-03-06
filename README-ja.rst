Hyuki-CVS-Graph
===============
.. image:: https://travis-ci.org/yassu/hyuki-cvs-graph.svg?branch=master
    :target: https://travis-ci.org/yassu/hyuki-cvs-graph

Usage
=====

.. code:: bash

    hyuki-graph [option] [base_dir]

ここで, ``base_dir``\ はこのプログラムが見るもっとも上のディレクトリ.

``base_dir``\ は, デフォルトでは\ ``.``\ .


このプログラムは
結城先生が考えておられる\ `色つき星取表 <https://note.mu/hyuki/n/n9a6e7c1e0d7b>`__\ と同様のことを
CVSを用いて自動的に行うためのプログラムです.

.. figure:: https://raw.githubusercontent.com/yassu/hyuki-cvs-graph/master/imgs/example.gif
   :alt: example

このプログラムは,
現在ディレクトリの下にあるすべてのgitおよびhgのリポジトリからプロジェクト名を
縦, 日数を横に書いてある表を作成します.

また, ``hyuki_graph.json`` もしくは ``hyuki_graph.yaml`` という名前のファイルが,
見ているディレクトリにあれば,
その内容とCVSで得られたコミット数の総和を用いて表を作成します.

さらに, プロジェクト名p,
日数dが交差するところに赤色でDと書いてあった場合,
その日はそのプロジェクトにはコミットしていないことを表します.

黄色でMと書いてあった場合,
その日は9回以下のコミットがあったことを表しています.

緑色でLと書いてあった場合,
その日は10回以上のコミットがあったことを表しています.

例えば, 上の画像からは, Roque2.pyには七日前に10以上のコミットをして,
四日前に10回未満のコミットをしたが,
その後はコミットしていないことが分かります.

入力ファイルのシンタックス
=========================================

このプログラムは json形式ならば

.. code::

  {
    プロジェクト名: {
      日付: コミット数,
      日付: コミット数,
      e.t.c.
    },
    プロジェクト名: {
      日付: コミット数,
      日付: コミット数,
      e.t.c.
    },
    e.t.c.
  }

という形式のファイルを受け取ることができます.

ここで, 日付は2000/01/01, もしくは2000-01-01のような形式の文字列です.

また, yaml形式についても同様に

.. code::

  プロジェクト名:
    日付: コミット数
    日付: コミット数
    e.t.c.

  プロジェクト名:
    日付: コミット数
    日付: コミット数
    e.t.c.

という形式のファイルを受け取ることができます.

yaml形式を使う場合には, 明示的にPyYAMLパッケージをインストールしてください:

.. code:

  pip install PyYAML

Option
======

-  ``-n``, ``--day-num``: 何日前からコミットの状態を見るかを指定します.
   例えば, ``-n 14``\ とすると,
   二週間前からのコミットの状態を見ることができます.
-  ``-a``, ``--author``: コミッタの名前を指定します.
   空白区切りで複数のコミッタの名前を指定することもできます. 例えば
   ``-a yassu``\ とすると,
   yassuのコミットの状態だけを見ることができます.
-  ``-m``, ``--medium-sep``: この値以上のコミット数ならばLと表示します.
   デフォルト値は10です.
-  ``--DA``, ``--dead_or_alive``: D, M, Lを表示する代わりに D,
   Aだけを表示します. コミットがなければD,
   コミットがあればAを表示します.
- ``-M``, ``--monochrome``: 色を表示しません.
- ``--show-commit-numbers``, ``-c``: コミット数を表示します
- ``--log``: gitコマンドにおいて, reflogではなくlogコマンドを使う
- ``-f``, ``--file``: 入力ファイルをスペース区切りで指定します.
  デフォルトは "~/hyuki_graph.json ~/hyuki_graph.yaml hyuki_graph.json hyuki_graph.yaml" です.
- ``-t``, ``--file-type``: 入力ファイルのタイプを指定します.
  この値にはjsonかyamlのいずれかを指定してください.
- ``--FO, --file-only``: CVSを見ずに, 入力ファイルだけを見ます.
- ``-r, --only_running``: 動いている(すなわち, DEADだけではない)プロジェクトだけを表示します.
- ``--hide-status``: ステータスの情報を表示せずに, プロジェクト名のみを表示します.

これはオプションではないですが, 明示的に ``--file=""`` とすることで,
入力ファイルを見ないこともできます.

インストール方法
================

.. code:: bash

    % pip install hyuki-cvs-graph

もしくはこのプロジェクトをクローンして, このプロジェクトの直下で

.. code:: bash

    % python setup.py install

を実行して下さい.

必要なコマンド
==============

-  python
-  gitリポジトリを扱うなら, ``git``\ コマンド
-  hgリポジトリを扱うなら, ``hg``\ コマンド

LICENSE
=======

MIT
