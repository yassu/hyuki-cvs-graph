Hyuki-CVS-Graph
=================

結城先生が考えておられる[色つき星取表](https://note.mu/hyuki/n/n9a6e7c1e0d7b)と同様のことを
CVSを用いて自動的に行うためのソフトです.

![example](https://raw.githubusercontent.com/yassu/hyuki-cvs-graph/master/imgs/example.gif)

このソフトは, gitからプロジェクト名を縦, 日数を横に書いてある表を作成します.

さらに, プロジェクト名p, 日数dが交差するところに赤色でDと書いてあった場合,
その日はそのプロジェクトにはコミットしていないことを表します.

黄緑色でAと書いてあった場合, その日はコミットしたことを表しています.

例えば, 上の画像からは, Roqueには七日前にコミットしたが, その後はコミットしていないことが分かります.

また, yassu.github.ioには昨日と五日前にはコミットしたが, その後はコミットしていないことが分かります.

残っているタスク
==========================

- gitが使えるかどうかを判定するコードを書く
- hgへの対応
- 任意のpathから再帰的にリポジトリを探せるようにする
- projectが0の場合のエラー処理
- 日数が10以上にしていされたときの描画を見やすくする
- コミット数を表示するか否かを検討する.

LICENSE
=========

MIT
