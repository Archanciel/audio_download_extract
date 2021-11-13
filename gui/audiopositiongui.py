from audiogui import AudioGUI

class AudioPositionGUI(AudioGUI):
	"""
	Abstract class hosting common methods of its sub classes (AudioClipperGUI,
	AudioShareGUI).
	"""
	def __init__(self, **kw):
		super().__init__(**kw)
		
		self.isExtractFileDropDownMenuItemDisplayed = False
		self.isShareFileDropDownMenuItemDisplayed = False
		self.isSettingsDropDownMenuItemDisplayed = False
		self.isDeleteDropDownMenuItemDisplayed = False

	def updateFileSoundPos(self,
	                       soundloaderMp3Obj,
	                       newSoundPos,
	                       soundFilePlayButton):
		"""
		This method avoids duplicating several time the same code. It updates
		the sound position of the clip file if called by AudioExtractGUI
		or the sound position of the shared file if called by AudioShareGUI.
		
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

	def _finish_init(self, dt):
		"""
		Due to using WindowManager for managing multiple screens, the content
		of this method can no longer be located in the __init__ ctor method,
		but must be called by Clock.schedule_once().

		:param dt:
		"""
		super(AudioPositionGUI, self)._finish_init(dt)
	
	def manageStateOfGlobalRequestListButtons(self):
		'''
		Enable or disable history request list related controls according to
		the status of the list: filled with items or empty.

		Only handles state of the request history list buttons which
		operates on the list globally, not on specific items of the list.

		Those buttons are:
			Display/hide request history list button
			Replay all button
			Save request history list menu item button
		'''
		if len(self.requestListRV.data) == 0:
			# request list is empty
			self.toggleHistoButton.state = 'normal'
			self.toggleHistoButton.disabled = True
			self.boxLayoutContainingRV.height = '0dp'
			self.dropDownMenu.saveButton.disabled = True
		else:
			self.toggleHistoButton.disabled = False
			self.dropDownMenu.saveButton.disabled = False
