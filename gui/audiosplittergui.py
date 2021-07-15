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
		self.sliderUpdaterThread = None
		self.sliderUpdateFrequency = 1

	def initSoundFile(self, sourceAudioFilePathName):
		if 'mp3' == sourceAudioFilePathName[-4:]:
			return
		
		self.sourceAudioFilePathName.text = sourceAudioFilePathName

		self.soundloaderSourceMp3Obj = SoundLoader.load(sourceAudioFilePathName)
		soundLength = self.soundloaderSourceMp3Obj.length
		self.startTextInput.text = self.convertSecondsToTimeString(0)
		self.endTextInput.text = self.convertSecondsToTimeString(soundLength)

		self.audioSlider.value = 0
		self.audioSlider.max = soundLength
		
		if soundLength < 100:
			self.sliderUpdateFrequency = 1 / soundLength
	
	def playSourceFile(self):
		"""
		Executed by pressing the Play button
		example of audio file pathname:
		D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\Various\\Wear a mask. Help slow the spread of Covid-19..mp3
		"""
		# self.sourceAudioFilePathName.text was set either by
		# FileToSplitLoadFileChooserPopup.loadFile() or by
		# AudioDownloaderGUI._doOnStart().
		
		self.stopSplitFile()
		
		if self.soundloaderSourceMp3Obj is None:
			self.soundloaderSourceMp3Obj = SoundLoader.load(self.sourceAudioFilePathName.text)
			soundLength = self.soundloaderSourceMp3Obj.length
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
		
		self.stopSourceFile()
		
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
	
	def updateSourceFileSoundPos(self, value):
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
				self.soundloaderSourceMp3Obj.seek(value)
				if self.soundloaderSourceMp3Obj.status == 'stop':
					# here, the mp3 was played until its end
					self.soundloaderSourceMp3Obj.play()
					self.startSliderUpdateThread()
				else:
					# here, the user moved the slider to a position before end
					# of sound
					self.sourceFilePlayButton.disabled = True
	
	def stopSourceFile(self):
		"""
		Executed by pressing the Stop button
		"""
		if self.soundloaderSourceMp3Obj:
			if self.audioSlider.value >= self.soundloaderSourceMp3Obj.length - 2 * self.sliderUpdateFrequency:
				# here, the stop button is pressed when the sound file is at end. In this
				# case, pressing stop reposition the slider at sound beginning position.
				self.audioSlider.value = 0
			self.soundloaderSourceMp3Obj.stop()
			
			if self.sliderAsynchUpdater:
				self.sliderAsynchUpdater.stopSliderUpdaterThread = True

			if self.sliderUpdaterThread:
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
		self.stopSourceFile()
		self.stopSplitFile()
		self.startTextInput.text = ''
		self.currentTextInput.text = ''
		self.endTextInput.text = ''

	def disablePlayButton(self):
		self.sourceFilePlayButton.disabled = True
		
	def updateCurrentSoundPosTextInput(self, seconds):
		self.currentTextInput.text = self.convertSecondsToTimeString(seconds)
	
	def convertSecondsToTimeString(self, pos):
		return time.strftime('%H:%M:%S', time.gmtime(int(pos)))
	
	def createSplitFile(self):
		t = threading.Thread(target=self.createSplitFileOnNewThread, args=(), kwargs={})
		t.daemon = True
		t.start()

	def createSplitFileOnNewThread(self):
		startPos = self.startTextInput.text
		endPos = self.endTextInput.text
		speed = self.speedTextInput.text

		# handling bad speed definition ...
		try:
			speed = float(speed)
		except ValueError:
			speed = 1.0
		
		if startPos == '' or endPos == '':
			self.outputResult('Invalid start ({}) or end ({}) position. Split file creation not performed.'.format(startPos, endPos))
			return
		
		audioController = AudioController(self, None)
		downloadVideoInfoDic = audioController.trimAudioFile(self.sourceAudioFilePathName.text, startPos, endPos, speed)
		self.splitAudioFilePathName.text = downloadVideoInfoDic.getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1, timeFrameIndex=1)
		self.splitFilePlayButton.disabled = False
		self.soundloaderSplitMp3Obj = None
	
	def goToSourceFileStartPos(self):
		hhmmssStartPos = self.startTextInput.text
		
		try:
			startPos = self.convertTimeStringToSeconds(hhmmssStartPos)
			self.updateSourceFileSoundPos(startPos)
		except ValueError as e:
			self.outputResult('Start position invalid. {}. Value ignored.'.format(e))
	
	def goToSourceFileEndPos(self):
		hhmmssEndPos = self.endTextInput.text
		
		try:
			endPos = self.convertTimeStringToSeconds(hhmmssEndPos)
			self.updateSourceFileSoundPos(endPos)
		except ValueError as e:
			self.outputResult('End position invalid. {}. Value ignored.'.format(e))
	
	def forwardSourceFileTenSeconds(self):
		if self.soundloaderSourceMp3Obj is not None:
			currentPos = self.soundloaderSourceMp3Obj.get_pos()
			currentPos += 10
			self.updateSourceFileSoundPos(currentPos)
	
	def forwardSourceFileThirtySeconds(self):
		if self.soundloaderSourceMp3Obj is not None:
			currentPos = self.soundloaderSourceMp3Obj.get_pos()
			currentPos += 30
			self.updateSourceFileSoundPos(currentPos)

	def backwardSourceFileTenSeconds(self):
		if self.soundloaderSourceMp3Obj is not None:
			currentPos = self.soundloaderSourceMp3Obj.get_pos()
			currentPos -= 10
			self.updateSourceFileSoundPos(currentPos)

	def backwardSourceFileThirtySeconds(self):
		if self.soundloaderSourceMp3Obj is not None:
			currentPos = self.soundloaderSourceMp3Obj.get_pos()
			currentPos -= 30
			self.updateSourceFileSoundPos(currentPos)

	def convertTimeStringToSeconds(self, timeString):
		dateTimeStart1900 = datetime.strptime(timeString, "%H:%M:%S")
		dateTimeDelta = dateTimeStart1900 - datetime(1900, 1, 1)
		
		return dateTimeDelta.total_seconds()
	
	def goToSplitFileStartPos(self):
		if self.soundloaderSplitMp3Obj:
			self.changeSoundPos(soundloaderMp3Obj=self.soundloaderSplitMp3Obj,
			                    newSoundPos=0,
			                    soundPlayButton=self.splitFilePlayButton)
	
	def goToSplitFileEndPos(self):
		if self.soundloaderSplitMp3Obj:
			endPos = self.soundloaderSplitMp3Obj.length - 5
			self.changeSoundPos(soundloaderMp3Obj=self.soundloaderSplitMp3Obj,
			                    newSoundPos=endPos,
			                    soundPlayButton=self.splitFilePlayButton)
	
	def forwardSplitFileTenSeconds(self):
		if self.soundloaderSplitMp3Obj is not None:
			currPos = self.soundloaderSplitMp3Obj.get_pos()
			newSoundPos = currPos + 10
			self.changeSoundPos(soundloaderMp3Obj=self.soundloaderSplitMp3Obj,
			                    newSoundPos=newSoundPos,
			                    soundPlayButton=self.splitFilePlayButton)

	def backwardSplitFileTenSeconds(self):
		if self.soundloaderSplitMp3Obj is not None:
			currPos = self.soundloaderSplitMp3Obj.get_pos()
			newSoundPos = currPos - 10
			self.changeSoundPos(soundloaderMp3Obj=self.soundloaderSplitMp3Obj,
			                    newSoundPos=newSoundPos,
			                    soundPlayButton=self.splitFilePlayButton)
	
	def changeSoundPos(self, soundloaderMp3Obj,
	                   newSoundPos,
	                   soundPlayButton):
		"""
		This method avoids duplicating several time the same code.
		
		:param soundloaderMp3Obj: Caller method does ensure it is not None
		:param newSoundPos:
		:param soundPlayButton:
		:return:
		"""
		soundloaderMp3Obj.seek(newSoundPos)
		
		if soundloaderMp3Obj.status == 'stop':
			# here, the mp3 was played until its end
			soundloaderMp3Obj.play()
		
		soundPlayButton.disabled = True
	
	def currentPosChanged(self):
		print(self.currentTextInput.text)
		
if __name__ == '__main__':
	audioGUI = AudioSplitterGUI()
	time_string = "01:01:09"
	audioGUI.convertTimeStringToSeconds(time_string)