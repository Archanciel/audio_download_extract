from kivy.clock import Clock
from kivy.core.audio import SoundLoader

import threading, time
from datetime import datetime

from audiogui import AudioGUI
from asynchsliderupdater import AsynchSliderUpdater
from audiocontroller import AudioController
from constants import *


class AudioSplitterGUI(AudioGUI):
	def __init__(self, **kw):
		super(AudioSplitterGUI, self).__init__(**kw)

		# WARNING: accessing MainWindow fields defined in kv file
		# in the __init__ ctor is no longer possible when using
		# ScreenManager. Here's the solution:
		# (https://stackoverflow.com/questions/26916262/why-cant-i-access-the-screen-ids)
		Clock.schedule_once(self._finish_init)

	def _finish_init(self, dt):
		self.soundloaderMp3Obj = None
		self.sliderAsynchUpdater = None
		self.sliderUpdateFrequency = 1

	def initSoundFile(self, sourceAudioFilePathName):
		self.soundloaderMp3Obj = None
		self.sourceAudioFilePathName.text = sourceAudioFilePathName
		self.audioSlider.value = 0
	
	def playAudioFile(self):
		"""
		Executed by pressing the Play button
		example of audio file pathname:
		D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\Various\\Wear a mask. Help slow the spread of Covid-19..mp3
		"""
		# self.sourceAudioFilePathName.text was set either by
		# FileToSplitLoadFileChooserPopup.loadFile() or by
		# AudioDownloaderGUI._doOnStart().
		
		if self.soundloaderMp3Obj is None:
			self.soundloaderMp3Obj = SoundLoader.load(self.sourceAudioFilePathName.text)
			soundLength = self.soundloaderMp3Obj.length
			#print('soundLength ', soundLength)
			self.audioSlider.max = soundLength
			
			if soundLength < 100:
				self.sliderUpdateFrequency = 1 / soundLength
				
		self.startSliderUpdateThread()
		self.playButton.disabled = True
		self.soundloaderMp3Obj.play()
	
	def startSliderUpdateThread(self):
		if self.sliderAsynchUpdater:
			self.sliderAsynchUpdater.stopSliderUpdaterThread = True
			
		self.sliderAsynchUpdater = AsynchSliderUpdater(self,
		                                               self.soundloaderMp3Obj,
		                                               self.ids.slider,
		                                               stopSliderUpdaterThread=False)
		self.sliderUpdaterThread = threading.Thread(target=self.sliderAsynchUpdater.updateSlider, args=())
		self.sliderUpdaterThread.daemon = True
		self.sliderUpdaterThread.start()
	
	def updateSoundPos(self, value):
		"""
		Method called by the slider every time its value changes. The
		value of the slider changes for two reasons:
			1/ the user moved the slider
			2/ the AsynchSliderUpdater.updateSlider() called by a
			   separate thread which updates the slider position
			   every second to reflect the current mp3 playing position
			   was executed.
		:param value:
		:return:
		"""
		if self.soundloaderMp3Obj is not None:
			if abs(self.soundloaderMp3Obj.get_pos() - value) > self.sliderUpdateFrequency:
				# test required to avoid mp3 playing perturbation
				#print('AudioSplitterGUI.updateSoundPos: {}'.format(value))
				self.soundloaderMp3Obj.seek(value)
				if self.soundloaderMp3Obj.status == 'stop':
					# here, the mp3 was played until its end
					self.soundloaderMp3Obj.play()
					self.startSliderUpdateThread()
				else:
					# here, the user moved the slider to a position before end
					# of sound
					self.playButton.disabled = True
	
	def stopAudioFile(self):
		"""
		Executed by pressing the Stop button
		"""
		if self.soundloaderMp3Obj:
			#print('self.audioSlider.value ',self.audioSlider.value)
			if self.audioSlider.value >= self.soundloaderMp3Obj.length - 2 * self.sliderUpdateFrequency:
				# here, the stop button is pressed when the sound file is at end. In this
				# case, pressing stop reposition the slider at sound beginning position.
				self.audioSlider.value = 0
			self.soundloaderMp3Obj.stop()
			self.sliderAsynchUpdater.stopSliderUpdaterThread = True
			self.sliderUpdaterThread.join()
			self.playButton.disabled = False

	def cancelSplitFile(self):
		self.stopAudioFile()
		self.startTextInput.text = ''
		self.currentTextInput.text = ''
		self.endTextInput.text = ''

	def disablePlayButton(self):
		self.playButton.disabled = True
		
	def updateCurrentSoundPosTextInput(self, pos):
		self.currentTextInput.text = time.strftime('%H:%M:%S', time.gmtime(int(pos)))
		
	def createSplitFile(self):
		startPos = self.startTextInput.text
		endPos = self.endTextInput.text
		
		if startPos == '' or endPos == '':
			self.outputResult('Invalid start ({}) or end ({}) position. Split file creation not performed.'.format(startPos, endPos))
			return
		
		audioController = AudioController(self, None)
		downloadVideoInfoDic = audioController.trimAudioFile(self.sourceAudioFilePathName.text, startPos, endPos)
		self.splitAudioFilePathName.text = downloadVideoInfoDic.getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1, timeFrameIndex=1)
	
	def goToStartPos(self):
		hhmmssStartPos = self.startTextInput.text
		
		try:
			startPos = self.convertTimeStringToSeconds(hhmmssStartPos)
			self.updateSoundPos(startPos)
		except ValueError as e:
			self.outputResult('Start position invalid. {}. Value ignored.'.format(e))
	
	def goToEndPos(self):
		hhmmssEndPos = self.endTextInput.text
		
		try:
			endPos = self.convertTimeStringToSeconds(hhmmssEndPos)
			self.updateSoundPos(endPos)
		except ValueError as e:
			self.outputResult('End position invalid. {}. Value ignored.'.format(e))

	def forwardTenSeconds(self):
		currentPos = self.soundloaderMp3Obj.get_pos()
		currentPos += 10
		self.updateSoundPos(currentPos)

	def forwardThirtySeconds(self):
		currentPos = self.soundloaderMp3Obj.get_pos()
		currentPos += 30
		self.updateSoundPos(currentPos)

	def backwardTenSeconds(self):
		currentPos = self.soundloaderMp3Obj.get_pos()
		currentPos -= 10
		self.updateSoundPos(currentPos)

	def backwardThirtySeconds(self):
		currentPos = self.soundloaderMp3Obj.get_pos()
		currentPos -= 30
		self.updateSoundPos(currentPos)

	def convertTimeStringToSeconds(self, timeString):
		dateTimeStart1900 = datetime.strptime(timeString, "%H:%M:%S")
		dateTimeDelta = dateTimeStart1900 - datetime(1900, 1, 1)
		
		return dateTimeDelta.total_seconds()
		
if __name__ == '__main__':
	audioGUI = AudioSplitterGUI()
	time_string = "01:01:09"
	audioGUI.convertTimeStringToSeconds(time_string)