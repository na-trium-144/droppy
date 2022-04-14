#!/bin/bash
# https://qiita.com/Jacminik/items/a4c8fe20a4cba62f428b の@narumi18waさんのコメントを参考にしました

resfile="res/icon.png"
icnsdir="AppIcon.iconset"

array=(16 32 128 256 512)

mkdir $icnsdir
for i in "${array[@]}"
do
    sips -Z $i $resfile --out "$icnsdir/icon_${i}x${i}.png"
    sips -Z $((i*2)) $resfile --out "$icnsdir/icon_${i}x${i}@2x.png"
done

iconutil -c icns $icnsdir
rm -rf $icnsdir
