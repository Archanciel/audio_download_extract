from kivy.core.audio import SoundLoader

import threading, time

from audiopositiongui import AudioPositionGUI
from asynchsliderupdater import AsynchSliderUpdater
from audiocontroller import AudioController


class AudioSplitterGUI(AudioPositionGUI):
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
		self.splitAudioFilePathNameInitValue = ''
		
		# if set to True, avoids that the AsynchSliderUpdater.updateSlider()
		# method called by separate thread overwrites the user position
		# modification action ...
		self.userClickedOnSourceSoundPositionButton = False

	def initSoundFile(self, sourceAudioFilePathName):
		if 'mp3' != sourceAudioFilePathName[-3:]:
			return
		
		self.sourceAudioFilePathNameInitValue = sourceAudioFilePathName
		self.sourceAudioFilePathName.text = sourceAudioFilePathName

		self.soundloaderSourceMp3Obj = SoundLoader.load(sourceAudioFilePathName)
		soundLength = self.soundloaderSourceMp3Obj.length
		self.startTextInput.text = self.convertSecondsToTimeString(0)
		self.endTextInput.text = self.convertSecondsToTimeString(soundLength)

		self.audioSlider.value = 0
		self.audioSlider.max = soundLength
		
		# setting focus on startTextInput must be done here, not in
		# the _finish_init() method !
		self.startTextInput.focus = True
		
		self.initializeSliderUpdateSecondsNumber(soundLength)
	
	def initializeSliderUpdateSecondsNumber(self, soundLength):
		if soundLength < 30:
			self.sliderUpdateEverySecondsNumber = 1 / soundLength
		else:
			self.sliderUpdateEverySecondsNumber = 0.2
	
	def playSourceFile(self):
		"""
		Method called when pressing the source file Play button
		"""
#		example of audio file pathname:
#		D:\Users\Jean-Pierre\Downloads\Audiobooks\Various\Wear a mask. Help slow the spread of Covid-19..mp3
#       self.sourceAudioFilePathName.text was set either by
#       FileToSplitLoadFileChooserPopup.loadFile() or by
#       AudioDownloaderGUI._doOnStart().
		
		self.stopSplitFile()
		
		if self.soundloaderSourceMp3Obj is None:
			self.soundloaderSourceMp3Obj = SoundLoader.load(self.sourceAudioFilePathName.text)
			soundLength = self.soundloaderSourceMp3Obj.length
			self.audioSlider.max = soundLength
			self.initializeSliderUpdateSecondsNumber(soundLength)
		
		self.startSliderUpdateThread()
		self.sourceFilePlayButton.disabled = True
		self.soundloaderSourceMp3Obj.play()
	
	def playSplitFile(self):
		"""
		Method called when pressing the split file Play button
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
	
	def updateSourceFileSoundPos(self, newSoundPos):
		"""
		Method called by the slider every time its value changes. The
		value of the slider changes for four reasons:
			1/ the user moved the slider
			2/ the AsynchSliderUpdater.updateSlider() called by a
			   separate thread which updates the slider position
			   every self.sliderUpdateEverySecondsNumber seconds
			   to reflect the current mp3 playing position was
			   executed.
			3/ the user clicks on a move source audio file button
			   (<| << < Play Stop > >> |>)
			4/ the user edited the current pos FocusTextInput field
			   
		:param newSoundPos:
		"""
		if abs(self.soundloaderSourceMp3Obj.get_pos() - newSoundPos) > self.sliderUpdateEverySecondsNumber:
			# test required to avoid mp3 playing perturbation
			self.soundloaderSourceMp3Obj.seek(newSoundPos)
			if self.soundloaderSourceMp3Obj.status == 'stop':
				# here, the mp3 was played until its end
				self.soundloaderSourceMp3Obj.play()
				self.sourceFilePlayButton.disabled = True
				self.startSliderUpdateThread()
			else:
				# here, the user moved the slider to a position before end
				# of sound
				self.sourceFilePlayButton.disabled = True

		self.updateCurrentSoundPosTextInput(newSoundPos)
		
	def stopSourceFile(self):
		"""
		Method called when pressing the source file Stop button
		"""
		if self.soundloaderSourceMp3Obj:
			if self.audioSlider.value >= self.soundloaderSourceMp3Obj.length - 2 * self.sliderUpdateEverySecondsNumber:
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
		Method called when pressing the split file Stop button
		"""
		if self.soundloaderSplitMp3Obj:
			self.soundloaderSplitMp3Obj.stop()
			self.splitFilePlayButton.disabled = False
	
	def cancelSplitFile(self):
		"""
		Method called when Cancel button is pressed.
		"""
		self.stopSourceFile()
		self.stopSplitFile()
		self.startTextInput.text = ''
		self.currentTextInput.text = ''
		self.endTextInput.text = ''

	def disablePlayButton(self):
		"""
		Method called by AsynchSliderUpdater.updateSlider().
		"""
		self.sourceFilePlayButton.disabled = True
		
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
			self.outputResult('Invalid start ({}) or end ({}) position. Split file creation not performed.'.format(startPos, endPos))
			return
		
		audioController = AudioController(self, None)
		downloadVideoInfoDic = audioController.trimAudioFile(self.sourceAudioFilePathName.text, startPos, endPos, speed)
		createdSplitFilePathName = downloadVideoInfoDic.getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1, timeFrameIndex=1)
		self.splitAudioFilePathNameInitValue = createdSplitFilePathName
		self.splitAudioFilePathName.text = createdSplitFilePathName
		self.soundloaderSplitMp3Obj = SoundLoader.load(createdSplitFilePathName)
		self.enableSplitFileButtons()
		self.splitFilePlayButton.disabled = False
		self.splitFileShareButton.disabled = False

	def enableSplitFileButtons(self):
		self.splitFilePlayButton.disabled = False
		self.splitFileStartButton.disabled = False
		self.splitFileBackwardButton.disabled = False
		self.splitFileStopButton.disabled = False
		self.splitFileForwardButton.disabled = False
		self.splitFileEndButton.disabled = False
		
		self.splitFileShareButton.disabled = False

	def goToSourceFileStartPos(self):
		"""
		Method called when source file <| button is pressed.
		"""
		hhmmssStartPos = self.startTextInput.text
		
		try:
			# if set to True, avoids that the AsynchSliderUpdater.updateSlider()
			# method called by separate thread overwrites the user position
			# modification action ...
			self.userClickedOnSourceSoundPositionButton = True
			
			startPos = self.convertTimeStringToSeconds(hhmmssStartPos)
			self.updateSourceFileSoundPos(startPos)
		except ValueError as e:
			self.outputResult('Start position invalid. {}. Value ignored.'.format(e))
	
	def goToSourceFileEndPos(self):
		"""
		Method called when source file |> button is pressed.
		"""
		hhmmssEndPos = self.endTextInput.text
		
		try:
			# if set to True, avoids that the AsynchSliderUpdater.updateSlider()
			# method called by separate thread overwrites the user position
			# modification action ...
			self.userClickedOnSourceSoundPositionButton = True
			
			endPos = self.convertTimeStringToSeconds(hhmmssEndPos)
			self.updateSourceFileSoundPos(endPos)
		except ValueError as e:
			self.outputResult('End position invalid. {}. Value ignored.'.format(e))
	
	def goToSourceFileCurrentPos(self):
		"""
		Method called when currentTextInput value is changed manually
		(on_text_validate in kv file).
		"""
		hhmmssEndPos = self.currentTextInput.text
		
		try:
			currentPos = self.convertTimeStringToSeconds(hhmmssEndPos)
			self.updateSourceFileSoundPos(currentPos)
		except ValueError as e:
			self.outputResult('Current position invalid. {}. Value ignored.'.format(e))
	
	def forwardSourceFileTenSeconds(self):
		"""
		Method called when source file > button is pressed.
		"""
		# if set to True, avoids that the AsynchSliderUpdater.updateSlider()
		# method called by separate thread overwrites the user position
		# modification action ...
		self.userClickedOnSourceSoundPositionButton = True
		
		currentPos = self.soundloaderSourceMp3Obj.get_pos()
		currentPos += 10
		self.updateSourceFileSoundPos(currentPos)
	
	def forwardSourceFileThirtySeconds(self):
		"""
		Method called when source file >> button is pressed.
		"""
		# if set to True, avoids that the AsynchSliderUpdater.updateSlider()
		# method called by separate thread overwrites the user position
		# modification action ...
		self.userClickedOnSourceSoundPositionButton = True
		
		currentPos = self.soundloaderSourceMp3Obj.get_pos()
		currentPos += 30
		self.updateSourceFileSoundPos(currentPos)

	def backwardSourceFileTenSeconds(self):
		"""
		Method called when source file < button is pressed.
		"""
		# if set to True, avoids that the AsynchSliderUpdater.updateSlider()
		# method called by separate thread overwrites the user position
		# modification action ...
		self.userClickedOnSourceSoundPositionButton = True
		
		currentPos = self.soundloaderSourceMp3Obj.get_pos()
		currentPos -= 10
		self.updateSourceFileSoundPos(currentPos)

	def backwardSourceFileThirtySeconds(self):
		"""
		Method called when source file << button is pressed.
		"""
		# if set to True, avoids that the AsynchSliderUpdater.updateSlider()
		# method called by separate thread overwrites the user position
		# modification action ...
		self.userClickedOnSourceSoundPositionButton = True
		
		currentPos = self.soundloaderSourceMp3Obj.get_pos()
		currentPos -= 30
		self.updateSourceFileSoundPos(currentPos)
	
	def goToSplitFileStartPos(self):
		"""
		Method called when split file <| button is pressed.
		"""
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSplitMp3Obj,
		                        newSoundPos=0,
		                        soundFilePlayButton=self.splitFilePlayButton)
	
	def goToSplitFileEndPos(self):
		"""
		Method called when split file |> button is pressed.
		"""
		endPos = self.soundloaderSplitMp3Obj.length - 5
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSplitMp3Obj,
		                        newSoundPos=endPos,
		                        soundFilePlayButton=self.splitFilePlayButton)
	
	def forwardSplitFileTenSeconds(self):
		"""
		Method called when split file > button is pressed.
		"""
		currPos = self.soundloaderSplitMp3Obj.get_pos()
		newSoundPos = currPos + 10
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSplitMp3Obj,
		                        newSoundPos=newSoundPos,
		                        soundFilePlayButton=self.splitFilePlayButton)

	def backwardSplitFileTenSeconds(self):
		"""
		Method called when split file < button is pressed.
		"""
		currPos = self.soundloaderSplitMp3Obj.get_pos()
		newSoundPos = currPos - 10
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderSplitMp3Obj,
		                        newSoundPos=newSoundPos,
		                        soundFilePlayButton=self.splitFilePlayButton)
	
	def shareSplitFile(self):
		"""
		Method called when Share button is pressed.
		"""
		self.stopSourceFile()
		self.stopSplitFile()
		
		audioShareScreen = self.manager.get_screen('audioShareScreen')
		audioShareScreen.initSoundFile(self.splitAudioFilePathName.text)
		self.parent.current = "audioShareScreen"
		self.manager.transition.direction = "left"


if __name__ == '__main__':
	audioGUI = AudioSplitterGUI()
	time_string = "01:01:09"
	audioGUI.convertTimeStringToSeconds(time_string)