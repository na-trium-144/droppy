#!/usr/bin/env python3
import time
import sys
import os
import pygame
from pygame.locals import *

from gdraw import *
from musicfile import *

class DSelect():
	def __init__(self, res_dir, music_dir, usr_dir, ddraw, se):
		self.ddraw = ddraw
		self.sel_items = dmusicfile_list(music_dir, res_dir, usr_dir)

		self.se = se

		# self.sel_items.append(DSelItem({"title":"あいうえおあいうえおああああabcde123456789", 'subtitle':"sub1", 'level_easy':"1", 'level_hard':"2"}))
		# self.sel_items.append(DSelItem({"title":"bbb", 'subtitle':"sub2", 'level_easy':"3", 'level_hard':"4"}))
		self.quit = False
		self.sel_num = 0
		self.ex = 0
		self.auto = False

	def main(self):
		self.ddraw.sel_init(self.sel_items, self.sel_num, self.ex, self.auto)

		self.clock = pygame.time.Clock()
		self.selected_item = None
		sel_cnt = 0
		self.bgm_stop_cnt = 0
		self.demo_end = None
		self.bgm_start_now = False
		redraw_select = False

		while (1):
			self.clock.tick(60)

			if sel_cnt == 20:
				self.bgm_start_now = True

			anim_ready = self.sel_items[self.sel_num].item_sp.anim_start is None and self.sel_items[0].item_sp.ofs_start is None

			if sel_cnt >= 15 and anim_ready and not redraw_select:
				self.ddraw.sel_redraw_select()
				redraw_select = True

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
					elif event.key in [K_UP, K_w] and self.sel_num > 0 and anim_ready:
						self.sel_num -= 1
						self.ddraw.set_sel_num(self.sel_num)
						sel_cnt = 0
						self.se['selmusic'].play()
						self.bgm_stop()
						self.bgm_start_now = True
						redraw_select = False
					elif event.key in [K_DOWN, K_s] and self.sel_num < len(self.sel_items) - 1 and anim_ready:
						self.sel_num += 1
						self.ddraw.set_sel_num(self.sel_num)
						sel_cnt = 0
						self.se['selmusic'].play()
						self.bgm_stop()
						self.bgm_start_now = True
						redraw_select = False
					elif event.key in [K_LEFT, K_a, K_RIGHT, K_d] and anim_ready:
						self.ex = 1 - self.ex
						self.ddraw.set_ex(self.ex)
						self.se['selhard'].play()
					elif event.key in [K_p]:
						self.auto = not self.auto
						self.ddraw.set_auto(self.auto)
						if self.auto:
							self.se['auto1'].play()
						else:
							self.se['auto0'].play()
					elif event.key in [K_SPACE, K_RETURN] and anim_ready:
						self.selected_item = self.sel_items[self.sel_num]
						self.bgm_stop()
						self.se['start'].play()
						# pygame.time.wait(1000)
						for t in range(60):
							self.clock.tick(60)
							self.ddraw.sel_redraw_start(t + 1)
							self.ddraw.sel_update()
						return
			self.ddraw.sel_update()

			if self.demo_end is not None and pygame.mixer.music.get_pos() >= self.demo_end * 1000:
				self.bgm_stop()
				# print(pygame.mixer.music.get_pos())

			sel_cnt += 1
			if not pygame.mixer.music.get_busy():
				self.bgm_stop_cnt += 1
			if self.bgm_stop_cnt >= 120 or self.bgm_start_now:
				self.bgm_start()

	def bgm_start(self):
		if pygame.mixer.music.get_busy():
			return
		pygame.mixer.music.load(self.sel_items[self.sel_num].bgm_file)
		pygame.mixer.music.set_volume(self.sel_items[self.sel_num].vol / 100)
		demo_range = self.sel_items[self.sel_num].demo_range
		demo_start = 0
		self.demo_end = None
		if demo_range is None or len(demo_range) < 1:
			demo_start = 0
		else:
			if len(demo_range) >= 2:
				self.demo_end = demo_range[1] - demo_range[0]
			demo_start = demo_range[0]
		print(f"demo: {demo_start}, {self.demo_end}")
		pygame.mixer.music.play(start=demo_start)
		self.bgm_stop_cnt = 0
		self.bgm_start_now = False
		print(f"hiscore: {self.sel_items[self.sel_num].dsavedat.score}")

	def bgm_stop(self):
		pygame.mixer.music.fadeout(1000)


if __name__ == "__main__":
	game_dir = os.path.dirname(__file__)

	#pygame.mixer.pre_init(44100, -16, 2, 64)
	#pygame.mixer.quit()

	pygame.init()
	pygame.mixer.init(44100, -16, 2, 64)
	ddraw = DDraw(game_dir)
	dselect = DSelect(game_dir, ddraw)
	dselect.main()
