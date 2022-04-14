import os
import copy

from save import *

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
	def __init__(self, filename, music_dir, usr_dir):
		self.filename_r = os.path.relpath(filename, music_dir)
		self.filename = filename
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
					self.demo_range = [float(s) for s in l[6:].split(",")]
				elif l.startswith("#") and ":" in l:
					self.meta[l[1:l.find(":")]] = l[l.find(":")+1:].strip()
		self.dsavedat = DSaveDat(usr_dir, self)

	def loaddat(self, ex, game_fps):
		self.count = 0
		self.dat = []
		# start = False
		last_cnt = 0
		measure_cnt = (60 / self.bpm * 4) * game_fps
		note_l = 16
		self.notedef = [DNoteInfo(3,None,50,100) for _ in range(26)]

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
				elif l.startswith("@"):
					# color, wav, xp
					param = l[3:].split(",")
					param = [p.strip() for p in param]
					param[0] = int(param[0]) #col
					param[1] = os.path.join(os.path.dirname(self.filename), param[1])
					param[2] = float(param[2]) #vol
					param[3] = float(param[3]) #xp
					self.notedef[ord(l.lower()[1]) - ord("a")] = DNoteInfo(param[0], param[1], param[2], param[3])
					print(f"set @{l.lower()[1]} {self.notedef[ord(l.lower()[1]) - ord('a')]}")
				else:
					i = 0
					while i < len(l):
						c = l[i]
						if (ord(c) >= ord("a") and ord(c) <= ord("z")):
							t2 = round(last_cnt)
							t1 = round(last_cnt) - round(measure_cnt)
							last_cnt += (60 / self.bpm * 4 / note_l) * game_fps
							ninfo = copy.copy(self.notedef[ord(c) - ord("a")])
							ninfo.set(game_fps, t1, t2, 1)
							print(DEvent(t1, 0, ninfo))
							self.dat.append(DEvent(t1, 0, ninfo))
							self.count += 1
						if (ord(c) >= ord("A") and ord(c) <= ord("Z")):
							t2 = round(last_cnt)
							t1 = round(last_cnt) - round(measure_cnt)
							last_cnt += (60 / self.bpm * 4 / note_l) * game_fps
							# self.dat.append([ord(c) - ord("A"), 2])
							ninfo = copy.copy(self.notedef[ord(c) - ord("A")])
							ninfo.set(game_fps, t1, t2, 2)
							print(DEvent(t1, 0, ninfo))
							self.dat.append(DEvent(t1, 0, ninfo))
							self.count += 2
						elif (c == "."):
							last_cnt += (60 / self.bpm * 4 / note_l) * game_fps
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

def dmusicfile_list(music_dir, usr_dir):
	dfiles = []
	for root, dirs, files in sorted(os.walk(top=music_dir)):
		for file in files:
			if file.lower().endswith('.txt'):
				file = os.path.join(root, file)
				# print(f'filePath = {file}')
				dm = DMusicFile(file, music_dir, usr_dir)
				if dm.droppy:
					dfiles.append(dm)
	return dfiles
