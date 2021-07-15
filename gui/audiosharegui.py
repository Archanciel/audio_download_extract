from kivy.core.audio import SoundLoader

import threading, time
from datetime import datetime

from audiogui import AudioGUI
from asynchsliderupdater import AsynchSliderUpdater
from audiocontroller import AudioController


class AudioShareGUI(AudioGUI):
	def __init__(self, **kw):
		super(AudioShareGUI, self).__init__(**kw)
		
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
		self.splitAudioFilePathNameInitValue = ''
	
	def initSoundFile(self, sharedAudioFilePathName):
		if 'mp3' != sharedAudioFilePathName[-3:]:
			return
		
		self.sharedAudioFilePathNameInitValue = sharedAudioFilePathName
		self.sharedAudioFilePathName.text = sharedAudioFilePathName
		self.soundloaderSourceMp3Obj = SoundLoader.load(sharedAudioFilePathName)
	
	def playSharedFile(self):
		"""
		Method called when pressing the source file Play button
		"""
		#		example of audio file pathname:
		#		D:\Users\Jean-Pierre\Downloads\Audiobooks\Various\Wear a mask. Help slow the spread of Covid-19..mp3
		#       self.sharedAudioFilePathName.text was set either by
		#       FileToSplitLoadFileChooserPopup.loadFile() or by
		#       AudioDownloaderGUI._doOnStart().
		
		self.stopSplitFile()
		
		if self.soundloaderSourceMp3Obj is None:
			self.soundloaderSourceMp3Obj = SoundLoader.load(self.sharedAudioFilePathName.text)

		self.sharedFilePlayButton.disabled = True
		self.soundloaderSourceMp3Obj.play()
	
	def playSplitFile(self):
		"""
		Method called when pressing the split file Play button
		"""
		# self.sharedAudioFilePathName.text was set either by
		# FileToSplitLoadFileChooserPopup.loadFile() or by
		# AudioDownloaderGUI._doOnStart().
		
		self.stopSharedFile()
		
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
	
	def updateSharedFileSoundPos(self, value):
		"""
		Method called by the slider every time its value changes. The
		value of the slider changes for two reasons:
			1/ the user moved the slider
			2/ the AsynchSliderUpdater.updateSlider() called by a
			   separate thread which updates the slider position
			   every second to reflect the current mp3 playing position
			   was executed.
			3/ the user click on a move source audio file button
			   (<| << < Play Stop > >> |>)
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
				else:
					# here, the user moved the slider to a position before end
					# of sound
					self.sharedFilePlayButton.disabled = True
	
	def stopSharedFile(self):
		"""
		Method called when pressing the source file Stop button
		"""
		if self.soundloaderSourceMp3Obj:
			self.soundloaderSourceMp3Obj.stop()
			self.sharedFilePlayButton.disabled = False
	
	def stopSplitFile(self):
		"""
		Method called when pressing the split file Stop button
		"""
		if self.soundloaderSplitMp3Obj:
			self.soundloaderSplitMp3Obj.stop()
			self.splitFilePlayButton.disabled = False
	
	def cancelSplitFile(self):
		"""
		Method called when Cancel button is pressed.
		"""
		self.stopSharedFile()
	
	def disablePlayButton(self):
		self.sharedFilePlayButton.disabled = True
	
	def updateCurrentSoundPosTextInput(self, seconds):
		self.currentTextInput.text = self.convertSecondsToTimeString(seconds)
	
	def convertSecondsToTimeString(self, pos):
		return time.strftime('%H:%M:%S', time.gmtime(int(pos)))
	
	def createSplitFile(self):
		"""
		Method called when Save button is pressed.
		"""
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
			self.outputResult(
				'Invalid start ({}) or end ({}) position. Split file creation not performed.'.format(startPos,
				                                                                                     endPos))
			return
		
		audioController = AudioController(self, None)
		downloadVideoInfoDic = audioController.trimAudioFile(self.sharedAudioFilePathName.text, startPos, endPos,
		                                                     speed)
		createdSplitFilePathName = downloadVideoInfoDic.getExtractedFilePathNameForVideoIndexTimeFrameIndex(
			videoIndex=1, timeFrameIndex=1)
		self.splitAudioFilePathNameInitValue = createdSplitFilePathName
		self.splitAudioFilePathName.text = createdSplitFilePathName
		self.splitFilePlayButton.disabled = False
		self.splitFileShareButton.disabled = False
		self.soundloaderSplitMp3Obj = None
	
	def goToSharedFileStartPos(self):
		"""
		Method called when source file <| button is pressed.
		"""
		self.updateSharedFileSoundPos(0)
	
	def goToSharedFileEndPos(self):
		"""
		Method called when source file |> button is pressed.
		"""
		if self.soundloaderSourceMp3Obj is not None:
			endPos = self.soundloaderSourceMp3Obj.length
			self.updateSharedFileSoundPos(endPos)
	
	def goToSharedFileCurrentPos(self):
		"""
		Method called when currentTextInput value is changed manually
		(on_text_validate in kv file).
		"""
		hhmmssEndPos = self.currentTextInput.text
		
		try:
			currentPos = self.convertTimeStringToSeconds(hhmmssEndPos)
			self.updateSharedFileSoundPos(currentPos)
		except ValueError as e:
			self.outputResult('Current position invalid. {}. Value ignored.'.format(e))
	
	def forwardSharedFileTenSeconds(self):
		"""
		Method called when source file > button is pressed.
		"""
		if self.soundloaderSourceMp3Obj is not None:
			currentPos = self.soundloaderSourceMp3Obj.get_pos()
			currentPos += 10
			self.updateSharedFileSoundPos(currentPos)
	
	def forwardSharedFileThirtySeconds(self):
		"""
		Method called when source file >> button is pressed.
		"""
		if self.soundloaderSourceMp3Obj is not None:
			currentPos = self.soundloaderSourceMp3Obj.get_pos()
			currentPos += 30
			self.updateSharedFileSoundPos(currentPos)
	
	def backwardSharedFileTenSeconds(self):
		"""
		Method called when source file < button is pressed.
		"""
		if self.soundloaderSourceMp3Obj is not None:
			currentPos = self.soundloaderSourceMp3Obj.get_pos()
			currentPos -= 10
			self.updateSharedFileSoundPos(currentPos)
	
	def backwardSharedFileThirtySeconds(self):
		"""
		Method called when source file << button is pressed.
		"""
		if self.soundloaderSourceMp3Obj is not None:
			currentPos = self.soundloaderSourceMp3Obj.get_pos()
			currentPos -= 30
			self.updateSharedFileSoundPos(currentPos)
	
	def convertTimeStringToSeconds(self, timeString):
		dateTimeStart1900 = datetime.strptime(timeString, "%H:%M:%S")
		dateTimeDelta = dateTimeStart1900 - datetime(1900, 1, 1)
		
		return dateTimeDelta.total_seconds()
	
	def goToSplitFileStartPos(self):
		"""
		Method called when split file <| button is pressed.
		"""
		if self.soundloaderSplitMp3Obj:
			self.updateSplitFileSoundPos(newSoundPos=0)
	
	def goToSplitFileEndPos(self):
		"""
		Method called when split file |> button is pressed.
		"""
		if self.soundloaderSplitMp3Obj:
			endPos = self.soundloaderSplitMp3Obj.length - 5
			self.updateSplitFileSoundPos(newSoundPos=endPos)
	
	def forwardSplitFileTenSeconds(self):
		"""
		Method called when split file > button is pressed.
		"""
		if self.soundloaderSplitMp3Obj is not None:
			currPos = self.soundloaderSplitMp3Obj.get_pos()
			newSoundPos = currPos + 10
			self.updateSplitFileSoundPos(newSoundPos=newSoundPos)
	
	def backwardSplitFileTenSeconds(self):
		"""
		Method called when split file < button is pressed.
		"""
		if self.soundloaderSplitMp3Obj is not None:
			currPos = self.soundloaderSplitMp3Obj.get_pos()
			newSoundPos = currPos - 10
			self.updateSplitFileSoundPos(newSoundPos=newSoundPos)
	
	def updateSplitFileSoundPos(self,
	                            newSoundPos):
		"""
		This method avoids duplicating several time the same code.

		:param newSoundPos:
		:return:
		"""
		self.soundloaderSplitMp3Obj.seek(newSoundPos)
		
		if self.soundloaderSplitMp3Obj.status == 'stop':
			# here, the mp3 was played until its end
			self.soundloaderSplitMp3Obj.play()
		
		self.splitFilePlayButton.disabled = True
	
	def shareSplitFile(self):
		"""
		Method called when Share button is pressed.
		"""
		audioShareScreen = self.manager.get_screen('audioShareScreen')
		audioShareScreen.initSoundFile(self.splitAudioFilePathName.text)
		self.parent.current = "audioShareScreen"
		self.manager.transition.direction = "left"
	
	def ensureTextNotChanged(self, id):
		"""
		Method called when sharedAudioFilePathName.text is modified. The
		TextInput is readonly. But in order to be able to move the cursor
		along the TextInput long text, its readonly attribute must be set
		to False. This method ensures that readonly is applied to the field.
		"""
		if id == 'shared_file_path_name':
			self.sharedAudioFilePathName.text = self.sharedAudioFilePathNameInitValue
		elif id == 'split_file_path_name':
			self.splitAudioFilePathName.text = self.splitAudioFilePathNameInitValue
	
	if __name__ == '__main__':
		audioGUI = AudioShareGUI()
		time_string = "01:01:09"
		audioGUI.convertTimeStringToSeconds(time_string)