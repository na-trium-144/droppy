#!/usr/bin/env python3

import pygame
from pygame.locals import *
import os

from sselect import *
from game import *
from gdraw import *
from title import *

def main(game_dir):
	res_dir = os.path.join(game_dir, "res")
	music_dir = os.path.join(game_dir, "music")
	usr_dir = os.path.join(game_dir, "usr")
	if not os.path.exists(usr_dir):
		os.mkdir(usr_dir)
	se = {}
	for (id, file, vol) in [("selmusic", "se_selmusic.wav", 50),
			("selhard", "se_selhard.wav", 30),
			("auto0", "se_auto0.wav", 30),
			("auto1", "se_auto1.wav", 30),
			("start", "se_start.wav", 40),
			("quit", "se_quit.wav", 40),
			("combo", "se_combo.wav", 30),
			("star", "se_star.wav", 30),
			("result0", "se_result0.wav", 40),
			("result1", "se_result1.wav", 40),
			("result2", "se_result2.wav", 40),
			("result3", "se_result3.wav", 40),
			("newscore", "se_newscore.wav", 40),
			("title", "se_title.wav", 50)]:
		se[id] = pygame.mixer.Sound(os.path.join(res_dir, file))
		se[id].set_volume(vol / 100)

	ddraw = DDraw(res_dir)
	dtitle = DTitle(res_dir, ddraw, se)
	while True:
		dtitle.main()
		if dtitle.quit:
			break
		dselect = DSelect(res_dir, music_dir, usr_dir, ddraw, se)
		while not dselect.quit:
			dselect.main()
			if dselect.selected_item is not None:
				dgame = DGame(ddraw, dselect.selected_item, dselect.ex, dselect.auto, se)
				dgame.main()

if __name__ == "__main__":
	#pygame.mixer.pre_init(44100, -16, 2, 64)
	#pygame.mixer.quit()
	#pygame.mixer.init(44100, -16, 2, 64)
	pygame.init()
	pygame.mixer.init(44100, -16, 2, 64)
	print(sys.executable)
	if getattr(sys, "frozen", False):
	   datadir = os.path.dirname(sys.executable)
	else:
	   datadir = os.path.dirname(__file__)
	main(datadir)

	pygame.quit()
