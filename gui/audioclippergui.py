from os.path import sep
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

import threading, time

from audiopositiongui import AudioPositionGUI
from asynchsliderupdater import AsynchSliderUpdater
from audiocontroller import AudioController

# constants below were copied from AudioShareGUI and will be deleted
from gui.guiutil import GuiUtil

GO_TO_END_PREVIOUS_SECONDS = 3
NAME_LABEL_KEY = 'nameLabel'
EMAIL_LABEL_KEY = 'emailLabel'
PHONE_NUMBER_LABEL_KEY = 'phoneNumberLabel'

CONTACT_NAME_KEY = 'name'
CONTACT_EMAIL_KEY = 'email'
CONTACT_PHONE_NUMBER_KEY = 'phoneNumber'

class AudioClipperGUI(AudioPositionGUI):
	def __init__(self, **kw):
		super(AudioClipperGUI, self).__init__(**kw)

	def _finish_init(self, dt):
		"""
		Due to using WindowManager for managing multiple screens, the content
		of this method can no longer be located in the __init__ ctor method,
		but must be called by Clock.schedule_once() (located in the base
		class).

		:param dt:
		"""
		super(AudioClipperGUI, self)._finish_init(dt)
		
		if self.error:
			# Error set by base class.
			# The case if the configuration manager could not load the config file
			return
		
		self.soundloaderSourceMp3Obj = None
		self.soundloaderClipMp3Obj = None
		self.sliderAsynchUpdater = None
		self.sliderUpdaterThread = None
		self.sliderUpdateFrequency = 1
		self.sourceAudioFilePathNameInitValue = ''
		self.clipAudioFilePathNameInitValue = ''
		self.audioController = AudioController(self, self.configMgr)


		# if set to True, avoids that the AsynchSliderUpdater.updateSlider()
		# method called by separate thread overwrites the user position
		# modification action ...
		self.userClickedOnSourceSoundPositionButton = False
	
	def _refocusOnFirstTextInput(self, *args):
		'''
		Method temporarily copied from AudioShareGUI. Will be replaced since
		list on AudioExtractGUI contains other informations !

		This method is here to be used as callback by Clock and must not be called directly
		:param args:
		:return:
		'''
		self.nameTextInputField.focus = True
	
	def initSoundFile(self, sourceFilePathName):
		sourceFileExtension = sourceFilePathName[-3:]

		if 'mp3' != sourceFileExtension:
			if 'mp4' == sourceFileExtension or 'm4a' == sourceFileExtension:
				# the case if Mobizen video capture was applied to an Audible audoiobook
				sourceFilePathName = self.audioController.extractAudioFromVideoFile(sourceFilePathName)
			else:
				return
		
		self.sourceAudioFilePathNameInitValue = sourceFilePathName
		self.sourceAudioFilePathName.text = sourceFilePathName

		self.soundloaderSourceMp3Obj = SoundLoader.load(sourceFilePathName)
		soundLength = self.soundloaderSourceMp3Obj.length
		self.startTextInput.text = GuiUtil.convertSecondsToTimeString(0)
		self.endTextInput.text = GuiUtil.convertSecondsToTimeString(soundLength)

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
	
	def loadHistoryFromPathFilename(self, pathFileName):
		self.currentLoadedFathFileName = pathFileName
		dataFileNotFoundMessage = self.buildFileNotFoundMessage(pathFileName)
		
		if not self.ensureDataPathFileNameExist(pathFileName, dataFileNotFoundMessage):
			return
		
		with open(pathFileName) as stream:
			lines = stream.readlines()
		
		lines = list(map(lambda line: line.strip('\n'), lines))
		# histoLines = [{'text': val, 'selectable': True} for val in lines
		
		items = [{CONTACT_NAME_KEY: ' ', CONTACT_EMAIL_KEY: '',
		          CONTACT_PHONE_NUMBER_KEY: ''},
		         {CONTACT_NAME_KEY: '  ', CONTACT_EMAIL_KEY: '',
		          CONTACT_PHONE_NUMBER_KEY: ''}
		         ]
		
		histoLines = [{NAME_LABEL_KEY: str(x[CONTACT_NAME_KEY]), EMAIL_LABEL_KEY: str(x[CONTACT_EMAIL_KEY]),
		               PHONE_NUMBER_LABEL_KEY: str(x[CONTACT_PHONE_NUMBER_KEY]), 'selectable': True} for x in items]
		
		self.requestListRV.data = histoLines
		self.requestListRVSelBoxLayout.clear_selection()
		
		# Reset the ListView
		self.resetListViewScrollToEnd()
		
		self.manageStateOfGlobalRequestListButtons()
		self.refocusOnFirstRequestInput()
	
	def playSourceFile(self):
		"""
		Method called when pressing the source file Play button
		"""
#		example of audio file pathname:
#		D:\Users\Jean-Pierre\Downloads\Audiobooks\Various\Wear a mask. Help slow the spread of Covid-19..mp3
#       self.sourceAudioFilePathName.text was set either by
#       FileToClipLoadFileChooserPopup.loadFile() or by
#       AudioDownloaderGUI._doOnStart().
		
		self.stopClipFile()
		
		if self.soundloaderSourceMp3Obj is None:
			self.soundloaderSourceMp3Obj = SoundLoader.load(self.sourceAudioFilePathName.text)
			soundLength = self.soundloaderSourceMp3Obj.length
			self.audioSlider.max = soundLength
			self.initializeSliderUpdateSecondsNumber(soundLength)
		
		self.startSliderUpdateThread()
		self.sourceFilePlayButton.disabled = True
		self.soundloaderSourceMp3Obj.play()
	
	def playClipFile(self):
		"""
		Method called when pressing the clip file Play button
		"""
		# self.sourceAudioFilePathName.text was set either by
		# FileToClipLoadFileChooserPopup.loadFile() or by
		# AudioDownloaderGUI._doOnStart().
		
		self.stopSourceFile()
		
		if self.soundloaderClipMp3Obj is None:
			self.soundloaderClipMp3Obj = SoundLoader.load(self.clipAudioFilePathName.text)

		self.clipFilePlayButton.disabled = True
		self.soundloaderClipMp3Obj.play()
	
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
				self.stopClipFile()
				self.soundloaderSourceMp3Obj.play()
				self.sourceFilePlayButton.disabled = True
				self.startSliderUpdateThread()
			else:
				# here, the user moved the slider to a position before end
				# of sound
				self.sourceFilePlayButton.disabled = True

		self.updateCurrentSoundPosTextInput(newSoundPos)

	def updateFileSoundPos(self,
	                       soundloaderMp3Obj,
	                       newSoundPos,
	                       soundFilePlayButton):
		"""
		Method called when changing clip file sound position.
		
		:param soundloaderMp3Obj:
		:param newSoundPos:
		:param soundFilePlayButton:
		:return:
		"""
		self.stopSourceFile()
		super(AudioClipperGUI, self).updateFileSoundPos(soundloaderMp3Obj,
		                                                newSoundPos,
		                                                soundFilePlayButton)

	def stopSourceFile(self, unusedParm=None):
		"""
		Method called when pressing the source file Stop button or
		by kivy.Clock in goToSourceFileEndPos() method.
		
		:param unusedParm   when this method is called by kivy.Clock,
							it must accept one parm set by the caller.
							
		:return False       when this method is called by kivy.Clock,
							returning False ensures it is called only
							one time
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
			
		return False
	
	def stopClipFile(self):
		"""
		Method called when pressing the clip file Stop button
		"""
		if self.soundloaderClipMp3Obj:
			self.soundloaderClipMp3Obj.stop()
			self.clipFilePlayButton.disabled = False
	
	def cancelClipFile(self):
		"""
		Method called when Cancel button is pressed.
		"""
		self.stopSourceFile()
		self.stopClipFile()
		self.startTextInput.text = ''
		self.currentTextInput.text = ''
		self.endTextInput.text = ''

	def disablePlayButton(self):
		"""
		Method called by AsynchSliderUpdater.updateSlider().
		"""
		self.sourceFilePlayButton.disabled = True
		
	def updateCurrentSoundPosTextInput(self, seconds):
		self.currentTextInput.text = GuiUtil.convertSecondsToTimeString(seconds)
	
	def createClipFile(self):
		"""
		Method called when Save button is pressed.
		"""
		t = threading.Thread(target=self.createClipFileOnNewThread, args=(), kwargs={})
		t.daemon = True
		t.start()

	def createClipFileOnNewThread(self):
		startPos = self.startTextInput.text
		endPos = self.endTextInput.text
		speed = self.speedTextInput.text

		# handling bad speed definition ...
		try:
			speed = float(speed)
		except ValueError:
			speed = 1.0
		
		if startPos == '' or endPos == '':
			self.outputResult('Invalid start ({}) or end ({}) position. Clip file creation not performed.'.format(startPos, endPos))
			return
		
		downloadVideoInfoDic = self.audioController.clipAudioFile(self.sourceAudioFilePathName.text, startPos, endPos, speed)
		createdClipFilePathName = self.audiobookPath + sep + downloadVideoInfoDic.getExtractedFilePathNameForVideoIndexTimeFrameIndex(videoIndex=1, timeFrameIndex=1)
		self.clipAudioFilePathNameInitValue = createdClipFilePathName
		self.clipAudioFilePathName.text = createdClipFilePathName
		self.soundloaderClipMp3Obj = SoundLoader.load(createdClipFilePathName)
		self.enableClipFileButtons()
		self.clipFilePlayButton.disabled = False
		self.clipFileShareButton.disabled = False

	def enableClipFileButtons(self):
		self.clipFilePlayButton.disabled = False
		self.clipFileStartButton.disabled = False
		self.clipFileBackwardButton.disabled = False
		self.clipFileStopButton.disabled = False
		self.clipFileForwardButton.disabled = False
		self.clipFileEndButton.disabled = False
		
		self.clipFileShareButton.disabled = False

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
			
			startPos = GuiUtil.convertTimeStringToSeconds(hhmmssStartPos)
			self.updateSourceFileSoundPos(startPos)
		except ValueError as e:
			self.outputResult('Start position invalid. {}. Value ignored.'.format(e))
	
	def goToSourceFileEndPos(self):
		"""
		Method called when source file |> button or source file right c button
		is pressed.
		"""
		hhmmssEndPos = self.endTextInput.text
		
		try:
			# if set to True, avoids that the AsynchSliderUpdater.updateSlider()
			# method called by separate thread overwrites the user position
			# modification action ...
			self.userClickedOnSourceSoundPositionButton = True
			
			endPos = GuiUtil.convertTimeStringToSeconds(hhmmssEndPos)
			
			# subtracting a couple of seconds to the end position set in the
			# source file end position field so that the sound file is played
			# from endPosBefore to the end pos. This enables to test if the end
			# pos value is what we wants.
			endPosBefore = endPos - GO_TO_END_PREVIOUS_SECONDS
			
			self.updateSourceFileSoundPos(endPosBefore)
			
			# stops sound play after GO_TO_END_PREVIOUS_SECONDS
			Clock.schedule_once(self.stopSourceFile, GO_TO_END_PREVIOUS_SECONDS)
		
		except ValueError as e:
			self.outputResult('End position invalid. {}. Value ignored.'.format(e))
	
	def goToSourceFileCurrentPos(self):
		"""
		Method called when currentTextInput value is changed manually
		(on_text_validate in kv file).
		"""
		hhmmssEndPos = self.currentTextInput.text
		
		try:
			currentPos = GuiUtil.convertTimeStringToSeconds(hhmmssEndPos)
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
	
	def goToClipFileStartPos(self):
		"""
		Method called when clip file <| button is pressed.
		"""
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderClipMp3Obj,
		                        newSoundPos=0,
		                        soundFilePlayButton=self.clipFilePlayButton)
	
	def goToClipFileEndPos(self):
		"""
		Method called when clip file |> button is pressed.
		"""
		endPos = self.soundloaderClipMp3Obj.length - GO_TO_END_PREVIOUS_SECONDS
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderClipMp3Obj,
		                        newSoundPos=endPos,
		                        soundFilePlayButton=self.clipFilePlayButton)
	
	def forwardClipFileTenSeconds(self):
		"""
		Method called when clip file > button is pressed.
		"""
		currPos = self.soundloaderClipMp3Obj.get_pos()
		newSoundPos = currPos + 10
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderClipMp3Obj,
		                        newSoundPos=newSoundPos,
		                        soundFilePlayButton=self.clipFilePlayButton)

	def backwardClipFileTenSeconds(self):
		"""
		Method called when clip file < button is pressed.
		"""
		currPos = self.soundloaderClipMp3Obj.get_pos()
		newSoundPos = currPos - 10
		self.updateFileSoundPos(soundloaderMp3Obj=self.soundloaderClipMp3Obj,
		                        newSoundPos=newSoundPos,
		                        soundFilePlayButton=self.clipFilePlayButton)
	
	def shareClipFile(self):
		"""
		Method called when Share button is pressed.
		"""
		self.stopSourceFile()
		self.stopClipFile()
		
		audioShareScreen = self.manager.get_screen('audioShareScreen')
		audioShareScreen.initSoundFile(self.clipAudioFilePathName.text)
		self.parent.current = "audioShareScreen"
		self.manager.transition.direction = "left"
	
	def replaceRequest(self, *args):
		"""
		Method copied from AudioShareGUI. Will have to be changed !
		
		:param args:
		:return:
		"""
		# Remove the selected item
		self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)
		
		# Get new values from the TextInput fields
		name, email, phoneNumber = self.getInputContactValues()
		
		# Add the updated data to the list if not already in
		requestListEntry = {NAME_LABEL_KEY: name, EMAIL_LABEL_KEY: email, PHONE_NUMBER_LABEL_KEY: phoneNumber,
		                    'selectable': True}
		
		if not requestListEntry in self.requestListRV.data:
			self.requestListRV.data.insert(self.recycleViewCurrentSelIndex, requestListEntry)
		
		self.refocusOnFirstRequestInput()
	
	def getInputContactValues(self):
		'''
		Method copied from AudioShareGUI. Will have to be changed !
		
		Returns new values from the TextInput fields.

		:return: name, email, phoneNumber
		'''
		name = self.nameTextInputField.text
		email = self.emailTextInputField.text
		phoneNumber = self.phoneNumberTextInputField.text
		
		return name, email, phoneNumber
	
	def emptyRequestFields(self):
		"""
		Method copied from AudioShareGUI. Will have to be changed !
		
		:return:
		"""
		self.nameTextInputField.text = ''
		self.emailTextInputField.text = ''
		self.phoneNumberTextInputField.text = ''

	def copyCurrentToStart(self):
		"""
		Method called when pressing the left c button.
		"""
		self.startTextInput.text = self.currentTextInput.text
		self.goToSourceFileStartPos()

	def copyCurrentToEnd(self):
		"""
		Method called when pressing the right c button.
		"""
		self.endTextInput.text = self.currentTextInput.text
		self.goToSourceFileEndPos()

	def reduceEndPos(self):
		"""
		Method called when pressing the end pos - button
		"""
		hhmmssEndPos = self.endTextInput.text
		endPos = GuiUtil.convertTimeStringToSeconds(hhmmssEndPos)
		endPos -= 1
		self.endTextInput.text = GuiUtil.convertSecondsToTimeString(endPos)
		self.goToSourceFileEndPos()

	def increaseEndPos(self):
		"""
		Method called when pressing the end pos + button
		"""
		hhmmssEndPos = self.endTextInput.text
		endPos = GuiUtil.convertTimeStringToSeconds(hhmmssEndPos)
		endPos += 1
		self.endTextInput.text = GuiUtil.convertSecondsToTimeString(endPos)
		self.goToSourceFileEndPos()

	def reduceStartPos(self):
		"""
		Method called when pressing the start pos - button
		"""
		hhmmssStartPos = self.startTextInput.text
		startPos = GuiUtil.convertTimeStringToSeconds(hhmmssStartPos)
		startPos -= 1
		self.startTextInput.text = GuiUtil.convertSecondsToTimeString(startPos)
		self.goToSourceFileStartPos()

	def increaseStartPos(self):
		"""
		Method called when pressing the start pos + button
		"""
		hhmmssStartPos = self.startTextInput.text
		startPos = GuiUtil.convertTimeStringToSeconds(hhmmssStartPos)
		startPos += 1
		self.startTextInput.text = GuiUtil.convertSecondsToTimeString(startPos)
		self.goToSourceFileStartPos()


if __name__ == '__main__':
	audioGUI = AudioClipperGUI()
