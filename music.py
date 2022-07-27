import pygame
from pygame.locals import *
import time
import copy
import os

from musicfile import *

class DMusic:
	def __init__(self, musicfile, ex):
		self.game_fps = musicfile.calc_game_fps()

		self.dat_pos = 0

		self.musicfile = musicfile
		musicfile.loaddat(ex)
		bgm_file = musicfile.bgm_file
		bgm_vol = musicfile.vol
		dat_file = musicfile.filename
		self.title = musicfile.meta['title']
		self.subtitle = musicfile.meta['subtitle']
		self.level = musicfile.meta['level'+str(ex)]
		self.bpm = musicfile.bpm
		self.delay = musicfile.delay
		self.dat = musicfile.dat
		self.count = musicfile.count

		pygame.mixer.music.load(bgm_file)
		pygame.mixer.music.set_volume(bgm_vol / 100)

		self.bgm_play = False
		self.se_wav = {}
		self.se_default = None
		# self.playing = []
		self.reached_end = False

	def play_se_default(self):
		if self.se_default is not None:
			# self.play_se(self.se_default)
			self.se_default.play()

	def play_se(self, wav_key):
		# if len(self.playing) >= 2:
		# 	self.playing[0].stop()
		# 	del self.playing[0]
		# self.playing.append(wav.play())
		self.se_wav[wav_key].play()

	def start(self):
		# self.startsec = time.time()
		# self.lastsec = self.startsec
		# self.mssec = 60 / self.bpm * 4
		self.ps = 0
		# self.note_l = 16
		# return self.startsec

	def quit(self):
		if self.bgm_play:
			pygame.mixer.music.fadeout(1500)

	def update(self, main_cnt):
		noteinfo = []

		while True:
			if self.dat_pos >= len(self.dat):
				break
			dat1 = self.dat[self.dat_pos]
			if dat1.start_t > main_cnt:
				break
			self.dat_pos += 1
			# print(dat1)
			if dat1.type == DEventType.Note:
				noteinfo.append(dat1.args)
				wav_key = dat1.args.wav_key
				if (wav_key not in self.se_wav):
					self.se_wav[wav_key] = pygame.mixer.Sound(dat1.args.wav)
					self.se_wav[wav_key].set_volume(dat1.args.vol / 100)
					if (self.se_default is None):
						self.se_default = self.se_wav[wav_key]
			if dat1.type == DEventType.MusicPlay and not self.bgm_play:
				pygame.mixer.music.play()
				self.bgm_play = True
			if dat1.type == DEventType.MusicFadeOut:
				pygame.mixer.music.fadeout(dat1.args * 1000)
			if dat1.type == DEventType.End:
				self.reached_end = True

		return noteinfo
