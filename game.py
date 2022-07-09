#!/usr/bin/env python3

import sys
import os

from music import *
from result import *
from gdraw import *
#from sounddev import *

class DGame():
	def __init__(self, ddraw, dmusicfile, ex, auto, se):
		self.ddraw = ddraw
		self.dmusicfile = dmusicfile
		self.game_fps = dmusicfile.game_fps()
		self.ex = ex
		self.auto = auto
		self.se = se

	def quit(self):
		self.dmusic.quit()
		self.se['quit'].play()
		pygame.time.wait(1500)

	def end(self):
		clr = self.dresult.get_result()

		self.ddraw.rslt_comboclear()
		self.ddraw.rslt_rank_t()
		self.clock.tick(3)
		for i in range(clr):
			self.ddraw.rslt_star(i)
			self.se['star'].play()
			self.clock.tick(3)
		self.ddraw.rslt_text(clr)
		self.se['result'+str(clr)].play()
		self.clock.tick(1)

		if not self.auto and self.dresult.score > self.dresult.hiscore:
			self.ddraw.rslt_hiscore()
			self.se['newscore'].play()
			self.dresult.save()

		while True:
			self.clock.tick(60)
			hitkey = 0
			for event in pygame.event.get():
				if event.type == VIDEORESIZE:
					self.ddraw.resize(event.dict['size'])
				if event.type == QUIT:          # 閉じるボタンが押されたとき
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN:       # キーを押したとき
					# if event.key == K_ESCAPE:   # Escキーが押されたとき
					# 	# pygame.quit()
					# 	# sys.exit()
					# 	self.quit()
					# 	return
					# else:
					hitkey += 1
					print(event.key)
				if event.type in [MOUSEBUTTONDOWN, JOYBUTTONDOWN]:
					hitkey += 1
			if hitkey:
				return

	def main(self):
		notes = [] #t2の順に並べ替え
		self.clock = pygame.time.Clock()

		# dsdev = DSoundDev()
		self.dmusic = DMusic(self.dmusicfile, self.ex)
		self.dmusic.start()
		self.dresult = DResult(self.dmusic.count, self.combo_large, self.dmusicfile.dsavedat, self.ex)
		# ddraw = DDraw(game_dir)
		self.ddraw.game_init(self.ex, self.auto, self.dmusic, self.dresult)

		self.clock.tick(0)

		finish_cnt = 0
		self.main_cnt = self.dmusicfile.start_cnt
		zero_time = time.time() - self.dmusicfile.start_cnt / self.game_fps

		timer_cnt = self.main_cnt

		while True:
			# self.clock.tick(self.game_fps)

			self.main_cnt += 1
			# 次のフレームまで待つ
			# 1fを少し超えちゃったらその次のフレームまで待つ
			while timer_cnt < self.main_cnt or (timer_cnt - self.main_cnt) % 1 > 0.1:
				timer_cnt += self.clock.tick(0) / 1000 * self.game_fps
			while timer_cnt - self.main_cnt > 1:
				self.main_cnt += 1

			if self.dmusic.reached_end:
				self.end()
				return

			#fread
			noteinfo = self.dmusic.update(self.main_cnt)
			for ninfo in noteinfo:
				notesp = DNoteSprite(ninfo, zero_time)
				notes.append(notesp)
				self.ddraw.addnote(notesp)

			#btn
			hitkey = 0
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
						self.quit()
						return
					else:
						hitkey += 1
						print(event.key)
				if event.type in [MOUSEBUTTONDOWN, JOYBUTTONDOWN]:
					hitkey += 1
			if (self.auto):
				hitkey = 0

			#move
			self.ddraw.game_update()

			#hnt
			for notesp in notes:
				if (notesp.stat <= 0):
					continue
				#if (notesp.stat < 0):
				#	notes.remove(notesp)
				diff_cnt = self.main_cnt - notesp.t2
				if diff_cnt < -round(0.25 * self.game_fps): #60fps15f=0.25 75fps19f=0.253
					break
				if hitkey == 0 and diff_cnt > round(0.08 * self.game_fps): #hnt4 miss 60fps5f=0.0833 75fps6f=0.080
					self.dresult.hit(4, notesp.stat)
					notesp.stat = 0
				else:
					while notesp.stat > 0 and (hitkey > 0 or self.auto and round(diff_cnt / self.game_fps * self.ddraw.actual_fps) >= 0):
						if notesp.wav is not None:
							#notesp.wav.play()
							self.dmusic.play_se(notesp.wav_key)
						hitkey -= 1
						#beep
						if notesp.stat == 1:
							notesp.stat = -1
						else:
							notesp.stat -= 1

						if abs(diff_cnt) <= round(0.03 * self.game_fps): #hnt1 good 60fps2f=0.0333 75fps2f=0.0267
							self.ddraw.game_create_effect(notesp, 0)
							self.dresult.hit(1, 1)
						elif abs(diff_cnt) <= round(0.06 * self.game_fps): #hnt2 ok 60fps4f=0.0667 75fps4f=0.0533, 5f=0.0667
							self.ddraw.game_create_effect(notesp, 1)
							self.dresult.hit(2, 1)
						else: #hnt3 bad
							self.dresult.hit(3, 1)
			if (hitkey > 0):
				#self.dmusic.se_default.play()
				self.dmusic.play_se_default()
			notes = [n for n in notes if n.stat >= 0]

			#beep

			#scor
	def combo_large(self):
		self.se['combo'].play()
		self.ddraw.combo_large()

if __name__ == "__main__":
	game_dir = os.path.dirname(__file__)
	res_dir = os.path.join(game_dir, "res")

	#pygame.mixer.pre_init(44100, -16, 2, 64)
	#pygame.mixer.quit()
	#pygame.mixer.init(44100, -16, 2, 64)
	pygame.init()
	pygame.mixer.init(44100, -16, 2, 64)

	ddraw = DDraw(res_dir)
	dgame = DGame(ddraw, None)
	dgame.main()
	pygame.quit()
