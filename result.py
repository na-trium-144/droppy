import time

class DResult:
	def __init__(self, count, combo_large, dsavedat, ex):
		self.scgmaxs = 100000
		self.scgclrs = 80000
		self.scbase = 100000
		self.scbonus = 60000
		self.hntcount = {1: 0, 2: 0, 3: 0, 4: 0}
		self.combo = 0
		self.scadd = 0
		self.score = 0
		self.rest = count
		self.count = count
		self.combo_large = combo_large
		self.ex = ex
		self.dsavedat = dsavedat
		self.hiscore = dsavedat.score[ex]

	def save(self):
		self.dsavedat.save(self.ex, self.score, self.hntcount)

	def get_result(self):
		if self.score < self.scgclrs:
			return 0 # fail
		if self.rest + self.hntcount[3] + self.hntcount[4] > 0:
			return 1 # clear
		if self.rest + self.hntcount[2] + self.hntcount[3] + self.hntcount[4] > 0:
			return 2 # full combo
		return 3 # perfect

	def hit(self, h, stat):
		oldcombo = self.combo
		if (h == 1):
			self.hntcount[1] += 1
			self.combo += 1
			if (self.combo >= 100):
				scadd1 = self.scbase + self.scbonus
			else:
				scadd1 = self.scbase + self.combo * self.scbonus / 100
			self.scadd = round(scadd1 / self.count)
			self.score += self.scadd
			self.rest -= 1
		if (h == 2):
			self.hntcount[2] += 1
			self.combo += 1
			if (self.combo >= 100):
				scadd1 = self.scbase + self.scbonus
			else:
				scadd1 = self.scbase + self.combo * self.scbonus / 100
			self.scadd = round(scadd1 / self.count * .6)
			self.score += self.scadd
			self.rest -= 1
		if (h == 3):
			self.hntcount[3] += 1
			self.combo = 0
			self.rest -= 1
		if (h == 4):
			self.hntcount[4] += 1
			self.combo = 0
			self.scadd = -round(self.scbase / self.count)
			self.score += self.scadd
			self.rest -= stat
		if (self.score < 0):
			self.score = 0
		if oldcombo // 50 < self.combo // 50:
			self.combo_large()
