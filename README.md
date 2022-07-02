# Droppy
オリジナルの音楽ゲームです。

## 実行方法
* Windows/Mac用バイナリはReleasesからどうぞ
* ソースから動かす場合はPython3とPygameが必要です。
```
pip3 install pygame
./main.py
```
* Linuxで音ズレが訪れる場合はpactlとかいじると直るかも

## 遊び方
* GitHubのWikiに書きました

## バイナリの生成
* cx_Freezeでバイナリを作成します
```
pip3 install cx_Freeze
./setup.py build  #←windows, linux
./setup.py bdist_mac  #←mac
```
