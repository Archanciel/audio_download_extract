from datetime import datetime

from audiogui import AudioGUI

class AudioPositionGUI(AudioGUI):
	"""
	Abstract class hosting common methods of its sub classes.
	"""
	def __init__(self, **kw):
		super().__init__(**kw)
		
		self.isExtractFileDropDownMenuItemDisplayed = False
		self.isShareFileDropDownMenuItemDisplayed = False
		self.isSettingsDropDownMenuItemDisplayed = False

	def convertTimeStringToSeconds(self, timeString):
		dateTimeStart1900 = datetime.strptime(timeString, "%H:%M:%S")
		dateTimeDelta = dateTimeStart1900 - datetime(1900, 1, 1)
		
		return dateTimeDelta.total_seconds()
	
	def updateFileSoundPos(self,
	                       soundloaderMp3Obj,
	                       newSoundPos,
	                       soundFilePlayButton):
		"""
		This method avoids duplicating several time the same code.
		
		:param soundloaderMp3Obj:
		:param newSoundPos:
		:param soundFilePlayButton:
		"""
		soundloaderMp3Obj.seek(newSoundPos)
		
		if soundloaderMp3Obj.status == 'stop':
			# here, the mp3 was played until its end
			soundloaderMp3Obj.play()

		soundFilePlayButton.disabled = True
	
	def ensureTextNotChanged(self, id):
		"""
		Method called when the audio file path name.text is modified. The
		TextInput is not readonly, although it must not be modified. But
		in order to be able to move the cursor along the TextInput long text,
		its readonly attribute must be set to False. This method ensures that
		readonly is applied to the field.
		"""
		if id == 'source_file_path_name':
			self.sourceAudioFilePathName.text = self.sourceAudioFilePathNameInitValue
		elif id == 'shared_file_path_name':
			self.sharedAudioFilePathName.text = self.sharedAudioFilePathNameInitValue
		elif id == 'split_file_path_name':
			self.splitAudioFilePathName.text = self.splitAudioFilePathNameInitValue
