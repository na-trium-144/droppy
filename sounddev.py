import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy import signal

class DSoundFile:
	def __init__(self, dsdev, filename):
		print("DSF init")
		(self.data, self.fs) = sf.read(filename, dtype='float32')
		if self.data.shape[0] > 100:
			self.data = self.data.transpose()
		if self.data.shape[0] < 2:
			self.data = np.resize(self.data, (2, self.data.shape[0]))
		print("DSF resample")
		self.data = np.array([signal.resample(self.data[i], int(self.data.shape[1] / self.fs * 44100)) for i in (0, 1)], dtype='float32')
		print("DSF resample finisied")
		self.data = self.data.transpose()
		self.dsdev = dsdev
	def play(self):
		self.dsdev.wavs.append(DSoundWav(self))
class DSoundWav:
	def __init__(self, dsf):
		self.data = dsf.data
		self.current = 0
		self.playing = True
class DSoundDev:
	def __init__(self):
		self.wavs = []
		self.stream = sd.OutputStream(samplerate=44100, blocksize=44100//60, latency=0, channels=2, callback=self.sd_callback)
		self.stream.start()
	def loadfile(self, filename):
		return DSoundFile(self, filename)
	def sd_callback(self, outdata, frames, time, status):
		if status:
			print(status)
		print("frames: {}".format(frames))
		mixdata = np.array([(0,0) for _ in range(frames)], dtype='float32')
		for dsw in self.wavs:
			if dsw.playing:
				chunksize = min(len(dsw.data) - dsw.current, frames)
				mixdata[:chunksize] += dsw.data[dsw.current: dsw.current + chunksize]
				dsw.current += chunksize
				if chunksize < frames:
					dsw.playing = False
		outdata[:] = mixdata
