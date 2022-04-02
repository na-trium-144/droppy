#!/usr/bin/env python3
import sys
import os
import pygame
from pygame.locals import *

from gdraw import *

class DTitle():
	def __init__(self, res_dir, ddraw, se):
		self.ddraw = ddraw
		self.title_bgm_file = os.path.join(res_dir, "title.mp3")

		self.se = se

		self.quit = False

	def main(self):
		self.ddraw.tit_init()

		self.clock = pygame.time.Clock()
		self.bgm_stop_cnt = 0

		pygame.mixer.music.set_volume(0.8)
		pygame.mixer.music.load(self.title_bgm_file)
		self.bgm_start()

		while (1):
			self.clock.tick(60)

			for event in pygame.event.get():
				if event.type == VIDEORESIZE:
					self.ddraw.resize(event.dict['size'])
				if event.type == QUIT:          # 閉じるボタンが押されたとき
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN:       # キーを押したとき
					if event.key == K_ESCAPE:   # Escキーが押されたとき
						# pygame.quit()
						# sys.exit()
						self.quit = True
						self.bgm_stop()
						self.se['quit'].play()
						l = self.se['quit'].get_length()
						wait = 0
						while wait < l:
							wait += self.clock.tick(0) / 1000
						return
					else:
						self.bgm_stop()
						self.se['title'].play()
						pygame.time.wait(1000)
						return
			self.ddraw.tit_update()

			if not pygame.mixer.music.get_busy():
				self.bgm_stop_cnt += 1
			if self.bgm_stop_cnt >= 120:
				self.bgm_start()
	def bgm_start(self):
		pygame.mixer.music.play()
		self.bgm_stop_cnt = 0
	def bgm_stop(self):
		pygame.mixer.music.fadeout(1000)
