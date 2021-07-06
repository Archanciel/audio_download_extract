import time

SLIDER_UPDATE_FRENQUENCY = 1

class AsynchSliderUpdater:
	def __init__(self,
	             soundloaderMp3Obj,
	             slider,
	             stopSliderUpdaterThread):
		self.soundloaderMp3Obj = soundloaderMp3Obj
		self.mp3PosSliderStop = self.soundloaderMp3Obj.length - SLIDER_UPDATE_FRENQUENCY
		self.slider = slider
		self.stopSliderUpdaterThread = stopSliderUpdaterThread
	
	def updateSlider(self):
		"""
		This method updates the slider position every
		SLIDER_UPDATE_FRENQUENCY seconds to reflect the current mp3
		playing position.
		:return:
		"""
		mp3Pos = self.soundloaderMp3Obj.get_pos()
		
		while not self.stopSliderUpdaterThread and mp3Pos < self.mp3PosSliderStop:
			self.slider.value = mp3Pos
			print('AsynchSliderUpdater.updateSlider() mp3 pos: {}'.format(mp3Pos))
			time.sleep(SLIDER_UPDATE_FRENQUENCY)
			mp3Pos = self.soundloaderMp3Obj.get_pos()
