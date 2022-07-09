import os
import copy

from save import *

lowest_fps = 60
#これの1.25倍までの間(60~75)でfps変動

#scoreからデータ受け渡すためだけのclass
class DNoteInfo:
	def __init__(self, col, wav, vol, xp):
		self.col = int(col)
		self.xp = xp
		self.vol = vol
		self.wav = wav
		self.t1 = None
		self.t2 = None
		self.stat = None
		self.t1_by_sec = None
		self.t2_by_sec = None
		self.wav_key = (wav, vol)

	def set(self, game_fps, t1, t2, stat):
		self.t1 = t1
		self.t2 = t2
		self.stat = stat
		self.t1_by_sec = t1 / game_fps
		self.t2_by_sec = t2 / game_fps

	def __str__(self):
		return f"DNoteInfo [col={self.col}, wav={self.wav}, vol={self.vol}, xp={self.xp}, t1={self.t1}, t2={self.t2}, stat={self.stat}]"

class DEventType:
	Note = 0
	MusicPlay = 1
	MusicFadeOut = 2
	End = 3

# DEvent(イベント時刻, EventType, パラメーター)
# イベントの生成はDMusicFile.loaddat()
# イベントの処理はDMusic.update()
class DEvent:
	def __init__(self, start_t, type, args):
		self.start_t = start_t
		self.type = type
		self.args = args
	def __str__(self):
		return f"DEvent [start_t={self.start_t}, type={self.type}, args={self.args}]"

class DMusicFile():
	def __init__(self, filename, music_dir, res_dir, usr_dir):
		self.filename_r = os.path.relpath(filename, music_dir)
		self.filename = filename
		self.res_dir = res_dir
		self.meta = {
			'title':"",
			'subtitle':"",
			'level0':"0",
			'level1':"0"
		}
		self.bgm_file = ""
		self.vol = 50
		self.bpm = 120
		self.delay = 0
		self.demo_range = None
		self.droppy = False
		self.item_sp = None
		with open(self.filename, "r", encoding="utf-8") as dat_f:
			dat_l = dat_f.readlines()
			for l in dat_l:
				if "//" in l:
					l = l[:l.find("//")]
				l = l.strip()
				ll = l.lower()
				if ll.startswith("#droppy"):
					self.droppy = True
				elif ll.startswith("#bpm:"):
					self.bpm = float(l[5:])
				elif ll.startswith("#volume:"):
					self.vol = float(l[8:])
				elif ll.startswith("#offset:"):
					self.delay = float(l[8:])
				elif ll.startswith("#music:"):
					self.bgm_file = os.path.join(os.path.dirname(self.filename), l[7:].strip())
				elif ll.startswith("#level:"):
					level_sprit = l[7:].split(",")
					for (i,lv) in enumerate(level_sprit):
						self.meta['level'+str(i)] = lv.strip()
					# self.meta['level_easy'] = l[7:l.find(",")]
					# self.meta['level_hard'] = l[l.find(",")+1:]
				elif ll.startswith("#demo:"):
					self.demo_range = [s for s in l[6:].split(",")]
					try:
						self.demo_range[0] = float(self.demo_range[0])
					except:
						self.demo_range[0] = 0
					try:
						self.demo_range[1] = float(self.demo_range[1])
					except:
						self.demo_range = self.demo_range[:1]
				elif ll.startswith("#start"):
					break
				elif l.startswith("#") and ":" in l:
					self.meta[l[1:l.find(":")]] = l[l.find(":")+1:].strip()
		self.dsavedat = DSaveDat(usr_dir, self)

	def game_fps(self):
		l = 96 # 32分音符*3連符 までタイミングを刻む
		while True:
			game_fps = 1 / (lowest_fps / self.bpm * 4 / l)
			# lに2,3,5,7をかけてfpsを60〜75に抑える
			# 少なくとも8分音符くらいまではタイミングを同期できるので、すべて60fpsで判定するよりは安定
			if game_fps < lowest_fps/7*4:
				l *= 2
			elif game_fps < lowest_fps/3*2:
				l *= 7 / 4 # 34.3~40 -> 60~70
			elif game_fps < lowest_fps/5*4:
				l *= 3 / 2 # 40~48 -> 60~72
			elif game_fps < lowest_fps:
				l *= 5 / 4 # 48~60 -> 60~75
			elif game_fps < lowest_fps*1.25:
				return game_fps # 60~75
			else:
				l /= 2
				#bpm188あたりからlが2で割られて32分の成分が消える

	def loaddat(self, ex):
		self.count = 0
		self.dat = []
		# start = False
		last_cnt = 0
		game_fps = self.game_fps()
		measure_cnt = (60 / self.bpm * 4) * game_fps
		note_l = 16
		bpm_local = self.bpm
		self.notedef = [DNoteInfo(3,0,30,100) for _ in range(26)]

		self.dat.append(DEvent(-round(self.delay * game_fps), DEventType.MusicPlay, None))
		with open(self.filename, "r", encoding="utf-8") as dat_f:
			dat_l = dat_f.readlines()
			for i in range(ex):
				while not dat_l.pop(0).lower().startswith("#start"):
					pass
				while not dat_l.pop(0).lower().startswith("#end"):
					pass
			while not dat_l.pop(0).lower().startswith("#start"):
				pass
			for l in dat_l:
				if "//" in l:
					l = l[:l.find("//")]
				l = l.strip()
				ll = l.lower()
				print(l)
				if ll.startswith("#end"):
					#曲終了処理 これも譜面内のコマンドで設定可能にする?
					last_cnt += 60
					self.dat.append(DEvent(last_cnt, DEventType.MusicFadeOut, 5))
					last_cnt += 60
					self.dat.append(DEvent(last_cnt, DEventType.End, 0))
					break
				elif ll.startswith("#bpm"):
					bpm_local = float(ll[5:])
					print("bpm:" + str(bpm_local))
				elif l.startswith("@"):
					# color, wav, xp
					param = l[3:].split(",")
					param = [p.strip() for p in param]
					chr = ord(l.lower()[1]) - ord("a")
					if len(param) < 1 or param[0] == "":
						col = self.notedef[chr].col
					else:
						col = int(param[0])
					if len(param) < 2 or param[1] == "":
						wav_name = self.notedef[chr].wav
					else:
						if param[1].isdigit():
							wav_name = param[1]
						else:
							wav_name = os.path.join(os.path.dirname(self.filename), param[1])
					if type(wav_name) == int or wav_name.isdigit():
						wav = os.path.join(self.res_dir, f"se_def{wav_name}.wav")
					else:
						wav = wav_name
					if len(param) < 3 or param[2] == "":
						vol = self.notedef[chr].vol
					else:
						vol = float(param[2])
					if len(param) < 4 or param[3] == "":
						xp = self.notedef[chr].xp
					else:
						xp = float(param[3])
					self.notedef[chr] = DNoteInfo(col, wav, vol, xp)
					print(f"set @{chr} {self.notedef[chr]}")
				else:
					i = 0
					while i < len(l):
						c = l[i]
						if (ord(c) >= ord("a") and ord(c) <= ord("z")):
							t2 = round(last_cnt)
							t1 = round(last_cnt) - round(measure_cnt)
							last_cnt += (60 / bpm_local * 4 / note_l) * game_fps
							ninfo = copy.copy(self.notedef[ord(c) - ord("a")])
							ninfo.set(game_fps, t1, t2, 1)
							print(DEvent(t1, 0, ninfo))
							self.dat.append(DEvent(t1, 0, ninfo))
							self.count += 1
						if (ord(c) >= ord("A") and ord(c) <= ord("Z")):
							t2 = round(last_cnt)
							t1 = round(last_cnt) - round(measure_cnt)
							last_cnt += (60 / bpm_local * 4 / note_l) * game_fps
							# self.dat.append([ord(c) - ord("A"), 2])
							ninfo = copy.copy(self.notedef[ord(c) - ord("A")])
							ninfo.set(game_fps, t1, t2, 2)
							print(DEvent(t1, 0, ninfo))
							self.dat.append(DEvent(t1, 0, ninfo))
							self.count += 2
						elif (c == "."):
							last_cnt += (60 / bpm_local * 4 / note_l) * game_fps
							# self.dat.append([0, 0])
						elif (c == "#"):
							i += 1
							c = l[i]
							if c == "l" or c == "L":
								num = ""
								while i + 1 < len(l):
									c = l[i + 1]
									if num != "" and not c.isdigit():
										break
									if c.isdigit():
										num += c
									i += 1
								note_l = float(num)
								# self.dat.append(["#l", int(num)])
						i += 1
		list.sort(self.dat, key= lambda x: x.start_t)
		self.start_cnt = self.dat[0].start_t #min(self.dat, key= lambda x:x.start_t)

def dmusicfile_list(music_dir, res_dir, usr_dir):
	dfiles = []
	for root, dirs, files in sorted(os.walk(top=music_dir)):
		for file in files:
			if file.lower().endswith('.txt'):
				file = os.path.join(root, file)
				# print(f'filePath = {file}')
				dm = DMusicFile(file, music_dir, res_dir, usr_dir)
				if dm.droppy:
					dfiles.append(dm)
	return dfiles
