import time

class AsynchSliderUpdater:
	def __init__(self,
	             audioClipperGUI,
	             soundloaderMp3Obj,
	             slider,
	             stopSliderUpdaterThread):
		self.audioClipperGUI = audioClipperGUI
		self.soundloaderMp3Obj = soundloaderMp3Obj
		self.mp3PosSliderStop = self.soundloaderMp3Obj.length - audioClipperGUI.sliderUpdateEverySecondsNumber
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
		sliderUpdateFrequency = self.audioClipperGUI.sliderUpdateEverySecondsNumber
		
		while not self.stopSliderUpdaterThread:
			if self.audioClipperGUI.userClickedOnSourceSoundPositionButton:
				# since the user clicked on one of the source sound position buttons
				# (<| << < Play Stop > >> |>), this avoids that the updateSlider()
				# method overwrite the user position modification action ...
				self.audioClipperGUI.userClickedOnSourceSoundPositionButton = False
			else:
				self.slider.value = mp3Pos
				self.audioClipperGUI.disablePlayButton()
				self.audioClipperGUI.updateCurrentSoundPosTextInput(mp3Pos)
				#print('AsynchSliderUpdater.updateSlider() mp3 pos: {}'.format(mp3Pos))

			time.sleep(sliderUpdateFrequency)
			mp3Pos = self.soundloaderMp3Obj.get_pos()
