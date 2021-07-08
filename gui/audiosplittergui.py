from kivy.core.audio import SoundLoader

import threading, time
from datetime import datetime

from audiogui import AudioGUI
from asynchsliderupdater import AsynchSliderUpdater
from audiocontroller import AudioController


class AudioSplitterGUI(AudioGUI):
	def __init__(self, **kw):
		super(AudioSplitterGUI, self).__init__(**kw)

	def _finish_init(self, dt):
		"""
		Due to using WindowManager for managing multiple screens, the content
		of this method can no longer be located in the __init__ ctor method,
		but must be called by Clock.schedule_once() (located in the base
		class).

		:param dt:
		"""
		self.soundloaderSourceMp3Obj = None
		self.soundloaderSplitMp3Obj = None
		self.sliderAsynchUpdater = None
		self.sliderUpdateFrequency = 1

	def initSoundFile(self, sourceAudioFilePathName):
		self.soundloaderSourceMp3Obj = None
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
		
		if self.soundloaderSourceMp3Obj is None:
			self.soundloaderSourceMp3Obj = SoundLoader.load(self.sourceAudioFilePathName.text)
			soundLength = self.soundloaderSourceMp3Obj.length
			#print('soundLength ', soundLength)
			self.audioSlider.max = soundLength
			
			if soundLength < 100:
				self.sliderUpdateFrequency = 1 / soundLength
				
		self.startSliderUpdateThread()
		self.sourceFilePlayButton.disabled = True
		self.soundloaderSourceMp3Obj.play()
	
	def playSplitFile(self):
		"""
		Executed by pressing the Play split file button.
		"""
		# self.sourceAudioFilePathName.text was set either by
		# FileToSplitLoadFileChooserPopup.loadFile() or by
		# AudioDownloaderGUI._doOnStart().
		
		if self.soundloaderSplitMp3Obj is None:
			self.soundloaderSplitMp3Obj = SoundLoader.load(self.splitAudioFilePathName.text)

		self.splitFilePlayButton.disabled = True
		self.soundloaderSplitMp3Obj.play()
	
	def startSliderUpdateThread(self):
		if self.sliderAsynchUpdater:
			self.sliderAsynchUpdater.stopSliderUpdaterThread = True
			
		self.sliderAsynchUpdater = AsynchSliderUpdater(self,
													   self.soundloaderSourceMp3Obj,
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
		if self.soundloaderSourceMp3Obj is not None:
			if abs(self.soundloaderSourceMp3Obj.get_pos() - value) > self.sliderUpdateFrequency:
				# test required to avoid mp3 playing perturbation
				#print('AudioSplitterGUI.updateSoundPos: {}'.format(value))
				self.soundloaderSourceMp3Obj.seek(value)
				if self.soundloaderSourceMp3Obj.status == 'stop':
					# here, the mp3 was played until its end
					self.soundloaderSourceMp3Obj.play()
					self.startSliderUpdateThread()
				else:
					# here, the user moved the slider to a position before end
					# of sound
					self.sourceFilePlayButton.disabled = True
	
	def stopAudioFile(self):
		"""
		Executed by pressing the Stop button
		"""
		if self.soundloaderSourceMp3Obj:
			#print('self.audioSlider.value ',self.audioSlider.value)
			if self.audioSlider.value >= self.soundloaderSourceMp3Obj.length - 2 * self.sliderUpdateFrequency:
				# here, the stop button is pressed when the sound file is at end. In this
				# case, pressing stop reposition the slider at sound beginning position.
				self.audioSlider.value = 0
			self.soundloaderSourceMp3Obj.stop()
			self.sliderAsynchUpdater.stopSliderUpdaterThread = True
			self.sliderUpdaterThread.join()
			self.sourceFilePlayButton.disabled = False
	
	def stopSplitFile(self):
		"""
		Executed by pressing the Stop button
		"""
		if self.soundloaderSplitMp3Obj:
			self.soundloaderSplitMp3Obj.stop()
			self.splitFilePlayButton.disabled = False
	
	def cancelSplitFile(self):
		self.stopAudioFile()
		self.startTextInput.text = ''
		self.currentTextInput.text = ''
		self.endTextInput.text = ''

	def disablePlayButton(self):
		self.sourceFilePlayButton.disabled = True
		
	def updateCurrentSoundPosTextInput(self, pos):
		self.currentTextInput.text = time.strftime('%H:%M:%S', time.gmtime(int(pos)))
		
	def createSplitFile(self):
		t = threading.Thread(target=self.createSplitFileOnNewThread, args=(), kwargs={})
		t.daemon = True
		t.start()

	def createSplitFileOnNewThread(self):
		startPos = self.startTextInput.text
		endPos = self.endTextInput.text
		
		if startPos == '' or endPos == '':
			self.outputResult('Invalid start ({}) or end ({}) position. Split file creation not performed.'.format(startPos, endPos))
			return
		
		audioController = AudioController(self, None)
		downloadVideoInfoDic = audioController.trimAudioFile(self.sourceAudioFilePathName.text, startPos, endPos)
		self.splitAudioFilePathName.text = downloadVideoInfoDic.getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1, timeFrameIndex=1)
		self.splitFilePlayButton.disabled = False
		self.soundloaderSplitMp3Obj = None
	
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
	
	def goToSplitFileEndPos(self):
		if self.soundloaderSplitMp3Obj:
			endPos = self.soundloaderSplitMp3Obj.length
			self.soundloaderSplitMp3Obj.seek(endPos - 5)

			if self.soundloaderSplitMp3Obj.status == 'stop':
				# here, the mp3 was played until its end
				self.soundloaderSplitMp3Obj.play()

			self.sourceFilePlayButton.disabled = True
		
	def forwardTenSeconds(self):
		currentPos = self.soundloaderSourceMp3Obj.get_pos()
		currentPos += 10
		self.updateSoundPos(currentPos)

	def forwardThirtySeconds(self):
		currentPos = self.soundloaderSourceMp3Obj.get_pos()
		currentPos += 30
		self.updateSoundPos(currentPos)

	def backwardTenSeconds(self):
		currentPos = self.soundloaderSourceMp3Obj.get_pos()
		currentPos -= 10
		self.updateSoundPos(currentPos)

	def backwardThirtySeconds(self):
		currentPos = self.soundloaderSourceMp3Obj.get_pos()
		currentPos -= 30
		self.updateSoundPos(currentPos)

	def convertTimeStringToSeconds(self, timeString):
		dateTimeStart1900 = datetime.strptime(timeString, "%H:%M:%S")
		dateTimeDelta = dateTimeStart1900 - datetime(1900, 1, 1)
		
		return dateTimeDelta.total_seconds()
	
	def goToStartPosSplitFile(self):
		if self.soundloaderSplitMp3Obj is not None:
			self.soundloaderSplitMp3Obj.seek(0)

			if self.soundloaderSplitMp3Obj.status == 'stop':
				# here, the mp3 was played until its end
				self.soundloaderSplitMp3Obj.play()

			self.splitFilePlayButton.disabled = True

if __name__ == '__main__':
	audioGUI = AudioSplitterGUI()
	time_string = "01:01:09"
	audioGUI.convertTimeStringToSeconds(time_string)