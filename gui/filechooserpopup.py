import os
from os.path import sep

from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.utils import platform

from gui.abstractpopup import AbstractPopup
from gui.guiutil import GuiUtil
from dirutil import DirUtil

LOAD_AT_START_MSG = ' (load at start activated)'


class SelectableLabelFileChooser(RecycleDataViewBehavior, Label):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	
	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.index = index
		return super(SelectableLabelFileChooser, self).refresh_view_attrs(
			rv, index, data)
	
	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		if super(SelectableLabelFileChooser, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)
	
	def apply_selection(self, rv, index, is_selected):
		''' Respond to the selection of items in the view. '''
		self.selected = is_selected
		
		if is_selected:
			selectOrCreateDirFileChooserPopup = rv.parent.parent.parent.parent.parent
			selectedPath = rv.data[index]['pathOnly']
			
#			selectedPath = selectedPath + sep  # adding '\\' is required, otherwise,
			# on Windows, when selecting D:, the
			# directory hosting the utility is
			# selected ! On Android, the file save
			# text input field is not ended by '/'
			# which causes a bug corrected on 15.1.21
			
			selectOrCreateDirFileChooserPopup.fileChooser.path = selectedPath
			selectOrCreateDirFileChooserPopup.updateFilePathNameFields(selectedPath)


class SelectableRecycleBoxLayoutFileChooser(FocusBehavior, LayoutSelectionBehavior,
                                            RecycleBoxLayout):
	''' Adds selection and focus behaviour to the view. '''
	
	# required to authorise unselecting a selected item
	touch_deselect_last = BooleanProperty(True)


class FileChooserPopup(AbstractPopup):
	LOAD_FILE_POPUP_TITLE = "Select URL's file to load"
	SAVE_FILE_POPUP_TITLE = "Save URL's to file"
	SELECT_OR_CREATE_DIR_PLAYLIST_POPUP_TITLE = 'Select or create directory where the playlist video audios will be downloaded'
	SELECT_OR_CREATE_DIR_SINGLE_VIDEO_POPUP_TITLE = 'Select or create directory where the single video audio will be downloaded'
	SELECT_FILE_TO_CLIP = 'Select audio file to clip'
	SELECT_FILE_TO_DELETE = 'Select audio file to delete'
	SELECT_FILE_TO_SHARE = 'Select audio file to share'

	load = ObjectProperty(None)
#	save = OLOAD_FILE_POPUP_TITLEbjectProperty(None)
	cancel = ObjectProperty(None)
	
	def __init__(self, rootGUI, **kwargs):
		"""
		Constructor.

		:param rootGUI:
		:param kwargs: contains popup title, root gui load and cancel bound
					   methods. So, self.load() and self.cancel() in fact
					   execute the root gui load and cancel bound methods.
		"""
		super(FileChooserPopup, self).__init__(**kwargs)

		self.sdCardDir = None
		self.rootGUI = rootGUI
		self.audioRootPath = rootGUI.getRootAudiobookPath()

		# filling the drive list (on Windows) or memory list (on Android)
		self.fillDriveOrMemoryList()

		# sizing FileChooserPopup widgets. Method defined in sub classes
		self._sizeFileChooser()
		
		# specify pre-selected node by its index in the data
		self.diskRecycleBoxLayout.selected_nodes = [0]
	
	def _sizeFileChooser(self):
		"""
		This method sets the popup size and position values used by the rootGUI
		openFileLoadPopup() or openFileSavePopup() methods as well as the file
		chooser	fields size.
		"""
		if platform == 'android':
			if self.onSmartPhone():
				self.gridLayoutPathField.size_hint_y = 0.08
			else:
				self.gridLayoutPathField.size_hint_y = 0.05
		elif platform == 'win':
			self.gridLayoutPathField.size_hint_y = 0.12
	
	def fillDriveOrMemoryList(self):
		"""
		
		:return:
		"""
		if platform == 'android':
			self.pathList.data.append({'text': 'Data file location setting', 'selectable': True,
			                           'pathOnly': self.audioRootPath})
			self.pathList.data.append({'text': 'Main RAM', 'selectable': True, 'pathOnly': '/storage/emulated/0'})
			
			baseDir = GuiUtil.getSmartPhoneDir()
			
			if baseDir != None:
				# the app is executed on an Android smartphone
				self.sdCardDir = baseDir
			else:
				baseDir = GuiUtil.getTabletDir()
				if baseDir != None:
					# the app is executed on an Android tablet
					self.sdCardDir = baseDir
				else:
					raise OSError(
						'App is running on an Android device whose base directory is not known by the GuiUtil class. Please correct the code, adding a new base dir constant.')
			
			self.pathList.data.append({'text': 'SD card', 'selectable': True, 'pathOnly': self.sdCardDir})
		elif platform == 'win':
			import string
			available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
			
			self.pathList.data.append(
				{'text': 'Data file location setting', 'selectable': True, 'pathOnly': self.audioRootPath})
			
			for drive in available_drives:
				self.pathList.data.append({'text': drive, 'selectable': True, 'pathOnly': drive})
	
	def updateFilePathNameFields(self, selectedPath):
		"""
		Updates the file path and file name fields of the file chooser dialog.

		This method is called by SelectableLabelFileChooser.apply_selection() when the
		SelectOrCreateDirFileChooserPopup dialog is opened or when a disk item is
		selected.

		:param selectedPath: 'C:\\' or 'D:\\' or 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\'
		"""
		pass


class LoadFileChooserPopup(FileChooserPopup):
	"""
	
	"""
	def __init__(self, rootGUI, **kwargs):
		"""
		Constructor.
		
		:param rootGUI:
		:param kwargs: contains popup title, root gui load and cancel bound
					   methods. So, self.load() and self.cancel() in fact
					   execute the root gui load and cancel bound methods.
		"""
		super(LoadFileChooserPopup, self).__init__(rootGUI, **kwargs)
		
	def loadFile(self, path, selection):
		"""
		Due to the load=self.load argument setting used in the
		AudioDownloaderGUI.openFileLoadPopup() method displayed below,
		when executing self.load(path, selection) in this method body,
		the AudioDownloaderGUI.load() method is called !
		
		def openFileLoadPopup(self):
			self.dropDownMenu.dismiss()
			popupTitle = self.buildFileChooserPopupTitle(FILE_ACTION_LOAD)
			self.fileChooserPopup = LoadFileChooserPopup(title=popupTitle,
														 rootGUI=self,
													>>>	 load=self.load,
														 cancel=self.dismissPopup)
		
		:param path:
		:param selection:
		"""
		self.load(path, selection)

class SaveFileChooserPopup(FileChooserPopup):
	"""
	
	"""
	def __init__(self, rootGUI, **kwargs):
		super(SaveFileChooserPopup, self).__init__(rootGUI, **kwargs)

		self.loadAtStartFilePathName = ''

	def _sizeFileChooser(self):
		"""
		
		:return:
		"""
		super()._sizeFileChooser()

		if platform == 'android':
			if self.onSmartPhone():
				self.loadAtStartChkBox.size_hint_x = 0.06
				self.gridLayoutPathField.size_hint_y = 0.16
			else:
				self.loadAtStartChkBox.size_hint_x = 0.06
				self.gridLayoutPathField.size_hint_y = 0.10
		elif platform == 'win':
			self.loadAtStartChkBox.size_hint_x = 0.06
			self.gridLayoutPathField.size_hint_y = 0.30

	def handleSelection(self, selection):
		selectionStr = selection[0]
		selectionElemLst = selectionStr.split(sep)
		
		if os.path.isfile(selectionStr):
			pathContainedInSelection = sep.join(selectionElemLst[:-1])
			fileNameContainedInSelection = selectionElemLst[-1]
		else:
			pathContainedInSelection = selectionStr
			fileNameContainedInSelection = ''
			
		self.currentPathField.text = pathContainedInSelection
		self.currentFileNameField.text = fileNameContainedInSelection

	def save(self, pathName, fileName, isLoadAtStart):
		"""
		
		:param pathName:
		:param isLoadAtStart:
		:return:
		"""
		if fileName == '':
			# no file selected or file name defined. Load dialog remains open ..
			return
			
		self.rootGUI.saveHistoryToFile(pathName + sep + fileName, isLoadAtStart)
		self.rootGUI.dismissPopup()

	def setCurrentLoadAtStartFile(self, loadAtStartFilePathName):
		self.loadAtStartFilePathName = loadAtStartFilePathName
	
	def updateLoadAtStartCheckBox(self):
		"""
		Method called when the currentPath or the currentFileName TextInput field
		content is modified.
		"""

		currentSavePath = self.currentPathField.text

		currentSaveFileName = self.currentFileNameField.text
		currentSavePathFileName = currentSavePath + sep + currentSaveFileName
		
		# update load at start checkbox
		
		if currentSavePathFileName == self.loadAtStartFilePathName:
			self.loadAtStartChkBox.active = True
		else:
			self.loadAtStartChkBox.active = False

		# update save file chooser popup title
		
		self._updateSaveFileChooserPopupTitle(currentSavePath,
		                                      currentSaveFileName,
		                                      self.loadAtStartChkBox.active)
	
	def _updateSaveFileChooserPopupTitle(self, currentSavePath, currentSaveFileName, isLoadAtStartChkboxActive):
		if currentSaveFileName == '':
			# the case when opening the save file dialog after loading a file
			return
		
		if isLoadAtStartChkboxActive:
			self.rootGUI.fileChooserPopup.title = '{} {}'.format(FileChooserPopup.SAVE_FILE_POPUP_TITLE,
			                                                     currentSaveFileName) + LOAD_AT_START_MSG
		else:
			self.rootGUI.fileChooserPopup.title = '{} {}'.format(FileChooserPopup.SAVE_FILE_POPUP_TITLE, currentSaveFileName)
	
	def toggleLoadAtStart(self, isChkBoxActive):
		"""
		Method called when checking/unchecking the load at start checkbox

		:param isChkBoxActive:
		"""
		self._updateSaveFileChooserPopupTitle(self.currentPathField.text,
		                                      self.currentFileNameField.text,
		                                      isChkBoxActive)


class DeleteFileChooserPopup(FileChooserPopup):
	"""

	"""
	
	def __init__(self, rootGUI, **kwargs):
		super(DeleteFileChooserPopup, self).__init__(rootGUI, **kwargs)
		
		self.loadAtStartFilePathName = ''
	
	def _setPopupSize(self):
		popupSizeProportion_x = 0.98
		popupSizeProportion_y = 0.98
		popupPos_top = 0.98
		
		# defining FileChooserPopup size parameters
		
		if platform == 'android':
			popupSizeProportion_y = 0.62
			
			if self.onSmartPhone():
				popupSizeProportion_x = 0.98
				popupSizeProportion_y = 0.98
				popupPos_top = 0.98
			else:
				# on tablet
				popupSizeProportion_x = 0.8
				popupPos_top = 0.92
		elif platform == 'win':
			popupSizeProportion_x = 0.98
			popupSizeProportion_y = 0.98
			popupPos_top = 0.98
			
		return popupPos_top, popupSizeProportion_x, popupSizeProportion_y
	
	def _sizeFileChooser(self):
		"""

		:return:
		"""
	
	def handleSelection(self, selectionLst):
		"""
		Method called when selecting or unselecting a file or a dir if
		FileChooserIconView.dirselect is set to True in filechooser.kv.
		
		:param selectionLst:
		"""
		if selectionLst == []:
			self.deleteButton.disabled = True
			self.deletedFilesLabel.text = ''
			
			return
		
		fileNameLines = ''
		
		for pathFileName in selectionLst:
			shortedFilePathName = DirUtil.extractFileNameFromFilePathName(pathFileName=pathFileName)
			fileNameLines += shortedFilePathName + '\n'
		
		self.deleteButton.disabled = False
		self.deletedFilesLabel.text = fileNameLines
	
	def delete(self):
		"""
		Method called when clicking Delete button.
		"""
		self.rootGUI.deleteAudioFilesFromDirAndFromDic(self.fileChooser.selection)
		self.rootGUI.dismissPopup()

	def unselectAll(self):
		"""
		Method called when clicking Unselect all button.
		"""
		self.fileChooser.selection = []
		self.deleteButton.disabled = True
		self.deletedFilesLabel.text = ''


class SelectOrCreateDirFileChooserPopup(FileChooserPopup):
	"""

	"""
	
	def __init__(self,
	             rootGUI,
	             playlistOrSingleVideoUrl,
	             originalPlaylistTitle,
	             originalSingleVideoTitle,
	             **kwargs):
		super(SelectOrCreateDirFileChooserPopup, self).__init__(rootGUI, **kwargs)

		self.playlistOrSingleVideoUrl = playlistOrSingleVideoUrl
		self.singleVideoTitle = originalSingleVideoTitle
		self.originalPlaylistTitle = originalPlaylistTitle
		self.originalSingleVideoTitle = originalSingleVideoTitle
	
	def _sizeFileChooser(self):
		"""

		:return:
		"""
		super()._sizeFileChooser()
		
		if platform == 'android':
			if self.onSmartPhone():
				self.gridLayoutPathField.size_hint_y = 0.16
			else:
				self.gridLayoutPathField.size_hint_y = 0.10
		elif platform == 'win':
			self.gridLayoutPathField.size_hint_y = 0.30
	
	def updateFilePathNameFields(self, selectedPath):
		"""
		Updates the file path and file name fields of the file chooser dialog.
		
		This method is called by SelectableLabelFileChooser.apply_selection() when the
		SelectOrCreateDirFileChooserPopup dialog is opened or when a disk item is
		selected.
		
		:param selectedPath: 'C:\\' or 'D:\\' or 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\'
		"""
		selectedPathWithoutRootDir = selectedPath.replace(self.rootGUI.configMgr.dataPath, '')
#		selectedPathWithoutRootDir = selectedPath.replace(self.audioRootPath, '')

		if self.originalPlaylistTitle is not None:
			# downloading a playlist
			self.currentPathField.text = selectedPathWithoutRootDir
			self.currentFileNameField.text = self.originalPlaylistTitle
		else:
			# downloading a single video
			# if selectedPathWithoutRootDir == '':
			# 	defaultSingleVideoSubDirName = DirUtil.getFullDirMinusRootDir(rootDir=self.rootGUI.configMgr.dataPath,
			# 	                                                              fullDir=self.audioRootPath)
			# 	self.currentPathField.text = defaultSingleVideoSubDirName
			# else:
			self.currentPathField.text = selectedPathWithoutRootDir

			self.currentFileNameField.text = self.singleVideoTitle

	def handleSelection(self, selection):
		"""
		This method is called when a dir item is selected.
		
		:param selection: ['D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks\\Hoppla']
		"""
#		selectedPathWithoutRootDir = selection[0].replace(self.audioRootPath + sep, '')
		selectedPathWithoutRootDir = selection[0].replace(self.rootGUI.configMgr.dataPath + sep, '')
		self.currentPathField.text = selectedPathWithoutRootDir

		if self.originalPlaylistTitle is not None:
			# downloading a playlist
			self.currentFileNameField.text = self.originalPlaylistTitle
		else:
			# downloading a single video
			self.currentFileNameField.text = self.singleVideoTitle
	
	def formatCurrentPathField(self):
		"""
		Method called when the currentPath TextInput field content is modified.
		"""
		currentSavePathValue = self.currentPathField.text
#		selectedPathWithoutRootDir = currentSavePathValue.replace(self.audioRootPath, '')
		selectedPathWithoutRootDir = currentSavePathValue.replace(self.rootGUI.configMgr.dataPath, '')

		if selectedPathWithoutRootDir != '' and selectedPathWithoutRootDir[0] == sep:
			# ensure path does not start with / or \ according to the OS
			self.currentPathField.text = selectedPathWithoutRootDir[1:]
		else:
			self.currentPathField.text = selectedPathWithoutRootDir

	def updateCurrentFileNameField(self):
		"""
		Method called when the currentFileNameField content is modified.
		"""
		currentFileNameFieldValue = self.currentFileNameField.text

		if self.originalPlaylistTitle is None:
			self.singleVideoTitle = currentFileNameFieldValue
		
	def selOrCreateDir(self, specifiedSubDirPath, playlistTitleOrVideoName):
		"""
		Method called after the user selected an existing dir or specified a new
		directory where to download the playlist or single video.
		
		:param  specifiedSubDirPath:        content of the currentPathField
		:param  playlistTitleOrVideoName:   content of the currentFileNameField, i.e,
											modified (or not) playlist title or
											modified (or not) video name
		"""
		if specifiedSubDirPath != '' and specifiedSubDirPath[-1] == sep:
			specifiedSubDirPath = specifiedSubDirPath[:-1]
			
		if self.originalPlaylistTitle is not None:
			# means we are downloading a playlist ...
			if specifiedSubDirPath != '':
				downloadPath = self.audioRootPath + sep + specifiedSubDirPath
			else:
				downloadPath = self.audioRootPath
			
			if playlistTitleOrVideoName == self.originalPlaylistTitle:
				# original playlist title was not modified
				self.rootGUI.modifiedPlaylistTitle = None
			else:
				self.rootGUI.modifiedPlaylistTitle = playlistTitleOrVideoName
		else:
			# a single video is downloaded ...
			rootDir = self.rootGUI.configMgr.dataPath
			downloadPath = rootDir + sep + specifiedSubDirPath

			if playlistTitleOrVideoName == self.originalSingleVideoTitle:
				# original single video title was not modified
				self.rootGUI.modifiedSingleVideoTitle = None
			else:
				self.rootGUI.modifiedSingleVideoTitle = playlistTitleOrVideoName

			# creating the video download path if not exist
			if os.path.isdir(downloadPath):
				pass
			else:
				targetAudioDirShort, dirCreationMessage = \
					DirUtil.createTargetDirIfNotExist(rootDir=rootDir,
					                                  targetAudioDir=downloadPath)
				
				if dirCreationMessage:
					# target dir was created
					self.rootGUI.outputResult(dirCreationMessage)
		
		indexAndDateSettingWarningMsg = self.rootGUI.getVideoTitlePrefixSuffixWarningMsg(
			self.playlistOrSingleVideoUrl, downloadPath)

		if indexAndDateSettingWarningMsg == '':
			self.rootGUI.addDownloadUrlToUrlList(downloadSubdir=downloadPath,
			                                     playlistOrSingleVideoUrl=self.playlistOrSingleVideoUrl)
			loadAtStartFilePathName, isLoadAtStart = self.rootGUI.getLoadAtStartFilePathName()
			self.rootGUI.saveHistoryToFile(loadAtStartFilePathName, isLoadAtStart)
		
		self.rootGUI.playlistOrSingleVideoDownloadPath = downloadPath
		self.rootGUI.downloadPlaylistOrSingleVideoAudio(self.playlistOrSingleVideoUrl)
		self.rootGUI.dismissPopup()


class FileToClipLoadFileChooserPopup(LoadFileChooserPopup):
	"""
	This file chooser popup is used to select the file which will be transmitted to the
	clip audio file class.
	"""
	
	def __init__(self, rootGUI, **kwargs):
		super(FileToClipLoadFileChooserPopup, self).__init__(rootGUI, **kwargs)
		self.loadButton.text = 'Clip file'
		
	def loadFile(self, path, selection):
		audioClipperScreen = self.rootGUI.manager.get_screen('audioClipperScreen')
		audioClipperScreen.initSoundFile(sourceFilePathName=selection[0])
		self.rootGUI.dismissPopup()
		self.rootGUI.parent.current = "audioClipperScreen"
		self.rootGUI.manager.transition.direction = "left"


class FileToShareLoadFileChooserPopup(LoadFileChooserPopup):
	"""
	This file chooser popup is used to select the file which will be transmitted to the
	share audio file class.
	"""
	
	def __init__(self, rootGUI, **kwargs):
		super(FileToShareLoadFileChooserPopup, self).__init__(rootGUI, **kwargs)
		self.loadButton.text = 'Share file'
	
	def loadFile(self, path, selection):
		audioShareScreen = self.rootGUI.manager.get_screen('audioShareScreen')
		audioShareScreen.initSoundFile(sharedAudioFilePathName=selection[0])
		self.rootGUI.dismissPopup()
		self.rootGUI.parent.current = "audioShareScreen"
		self.rootGUI.manager.transition.direction = "left"
