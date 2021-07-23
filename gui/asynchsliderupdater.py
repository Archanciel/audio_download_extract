import time

class AsynchSliderUpdater:
	def __init__(self,
	             audioSplitterGUI,
	             soundloaderMp3Obj,
	             slider,
	             stopSliderUpdaterThread):
		self.audioSplitterGUI = audioSplitterGUI
		self.soundloaderMp3Obj = soundloaderMp3Obj
		self.mp3PosSliderStop = self.soundloaderMp3Obj.length - audioSplitterGUI.sliderUpdateFrequency
		self.slider = slider
		self.stopSliderUpdaterThread = stopSliderUpdaterThread
	
	def updateSlider(self):
		"""
		This method updates the slider position every
		sliderUpdateFrequency seconds to reflect the current mp3
		playing position.
		:return:
		"""
		mp3Pos = self.soundloaderMp3Obj.get_pos()
		sliderUpdateFrequency = self.audioSplitterGUI.sliderUpdateFrequency
		
#		while not self.stopSliderUpdaterThread and mp3Pos < self.mp3PosSliderStop:
		while not self.stopSliderUpdaterThread:
			if self.audioSplitterGUI.userClickedOnSourceSoundPositionButton:
				# since the user clicked on one of the source sound position button
				# (<| << < Play Stop > >> |>), this avoids that the updateSlider()
				# method overwrite the user position modification action ...
				self.audioSplitterGUI.userClickedOnSourceSoundPositionButton = False
			else:
				self.slider.value = mp3Pos
				self.audioSplitterGUI.disablePlayButton()
				self.audioSplitterGUI.updateCurrentSoundPosTextInput(mp3Pos)
				#print('AsynchSliderUpdater.updateSlider() mp3 pos: {}'.format(mp3Pos))
				time.sleep(sliderUpdateFrequency)
				mp3Pos = self.soundloaderMp3Obj.get_pos()
