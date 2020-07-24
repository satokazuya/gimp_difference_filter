#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://sites.google.com/site/non2title/#TOC-GIMP-7
# https://amekujira.seesaa.net/article/418318288.html
# https://shiroyuki-mot-says.blogspot.com/2019/01/gimp-layer-mode-enum-names.html

from gimpfu import *

import os, glob

# 画像ファイルの格納先フォルダ
path = "C:\\temp\\"
win10 = "win10.bmp"
win8 = "win8.bmp"

def plugin_main(image, layer):
	# 背景以外のレイヤーを全削除
	for image in gimp.image_list():
		for layer in image.layers:
			if layer.name != "背景":
				image.remove_layer( layer )
	
	# win10とwin8でwidthとheightが大きいほうの画像でイメージをリサイズ
	filename = path + win8
	image2 = pdb.gimp_file_load(filename, "image0")
	filename = path + win10
	image3 = pdb.gimp_file_load(filename, "image1")
	width = 0
	height = 0
	if image2.width > image3.width:
		width = image2.width
	else:
		width = image3.width
	
	if image2.height > image3.height:
		height = image2.height
	else:
		height = image3.height
	gimp.delete( image2 )
	gimp.delete( image3 )
	
	# イメージをリサイズ
	image = gimp.image_list()[0]
	pdb.gimp_image_scale(image, width, height)
	
	# win8画像をイメージとして読み込み既存イメージに追加
	filename = path + win8
	layer_win8 = pdb.gimp_file_load_layer(image, filename)
	image.add_layer(layer_win8, 0)
	
	# win10画像をレイヤーとして読み込み既存イメージに追加
	filename = path + win10
	layer_win10 = pdb.gimp_file_load_layer(image, filename)
	image.add_layer(layer_win10, 0)
	
	# 差の絶対値
	layer_win10.mode = DIFFERENCE_MODE
	
	# レイヤーを原点を左上とし移動(x, y)
	layer_win8.translate(0, 5)
	
	# 不透明度
	layer_win10.opacity = 85.0

register(
   "auto_subtract",#コマンドラインまたはスクリプトから呼び出す場合のコマンドの名前
   "Windows10とWindows8の非互換調査",#プラグインの説明
   "Windows10とWindows8の非互換調査",#プラグインの詳細な説明
   "k.sato",#プラグインの作成者
   "k.sato",#プラグインの著作権保有者 (通常は author と同じ)
   "2020/07/24",#著作権の日付
   "<Image>/自動差の絶対値", #メニューの中でプラグインに使用されるラベル
   "RGB*", #プラグインで処理する対象となる画像のタイプex. RGB*, GRAY* など
   [],#引数(型, 名前（プロシージャブラウザに表示される）,説明, 初期値)
   [], # 戻り値
   plugin_main) # メソッド名

main()
