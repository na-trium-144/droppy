import os
import glob
import re

class DSaveDat:
	def __init__(self, usr_dir, dmusicfile):
		self.score = [0, 0]
		self.hntcount = [{1:0, 2:0, 3:0, 4:0} for _ in range(2)]
		self.dmusicfile = dmusicfile

		filename_r = dmusicfile.filename_r.replace("\\", "/").replace("./", "").replace("/", "_")
		path_r = os.path.join(usr_dir, filename_r)
		self.filename = path_r
		if os.path.exists(path_r):
			with open(path_r, "r") as f:
				dat = f.readlines()
			for l in dat:
				l = l.strip()
				ll = l.lower()
				if ll.startswith("#score"):
					h = int(ll[6])
					self.score[h] = int(ll[ll.find(":")+1:])
				elif ll.startswith("#hcount"):
					h = int(ll[7])
					hc_l = [int(c) for c in ll[ll.find(":")+1:].split(",")]
					self.hntcount[h] = {i+1:hc_l[i] for i in range(4)}
		else:
			title_match = False
			for fn in os.listdir(usr_dir):
				if fn.endswith(".txt"):
					with open(os.path.join(usr_dir, fn), "r") as f:
						dat = f.readlines()
					for l in dat:
						l = l.strip()
						ll = l.lower()
						if ll.startswith("#title"):
							t = l[l.find(":"):].strip()
							if t == dmusicfile.meta['title']:
								title_match = True
								break
					if title_match:
						self.filename = os.path.join(usr_dir, fn)
						for l in dat:
							l = l.strip()
							ll = l.lower()
							if ll.startswith("#score"):
								h = int(ll[6])
								self.score[h] = int(ll[ll.find(":")+1:])
							elif ll.startswith("#hcount"):
								h = int(ll[7])
								hc_l = [int(c) for c in ll[ll.find(":")+1:].split(",")]
								self.hntcount = {i+1:hc_l[i] for i in range(4)}
						break
			if not title_match:
				if os.path.exists(self.filename):
					i = 1
					while os.path.exists(self.filename.replace(".txt", f"_{i},txt")):
						i += 1
					self.filename = self.filename.replace(".txt", f"_{i}.txt")

	def save(self, ex, nscore, nhntcount):
		print(ex, nscore, nhntcount)
		self.score[ex] = nscore
		self.hntcount[ex] = nhntcount
		print(self.score, self.hntcount)
		with open(self.filename, "w") as f:
			f.write(f"#title:{self.dmusicfile.meta['title']}\n")
			for h in range(2):
				f.write(f"#score{h}:{self.score[h]}\n")
				f.write(f"#hcount{h}:{self.hntcount[h][1]},{self.hntcount[h][2]},{self.hntcount[h][3]},{self.hntcount[h][4]}\n")
