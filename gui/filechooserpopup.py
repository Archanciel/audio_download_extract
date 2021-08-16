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
			rootGUI = rv.parent.parent.parent.parent.parent
			selectedPath = rv.data[index]['pathOnly']
			
			selectedPath = selectedPath + sep  # adding '\\' is required, otherwise,
			# on Windows, when selecting D:, the
			# directory hosting the utility is
			# selected ! On Android, the file save
			# text input field is not ended by '/'
			# which causes a bug corrected on 15.1.21
			
			rootGUI.fileChooser.path = selectedPath
			rootGUI.currentPathField.text = selectedPath


class SelectableRecycleBoxLayoutFileChooser(FocusBehavior, LayoutSelectionBehavior,
                                            RecycleBoxLayout):
	''' Adds selection and focus behaviour to the view. '''
	
	# required to authorise unselecting a selected item
	touch_deselect_last = BooleanProperty(True)


class FileChooserPopup(AbstractPopup):
	LOAD_FILE_POPUP_TITLE = 'Select history file to load'
	SAVE_FILE_POPUP_TITLE = 'Save history to file'
	SELECT_OR_CREATE_DIR_POPUP_TITLE = 'Select or create directory where the single video audio will be downloaded'
	SELECT_FILE_TO_SPLIT = 'Select audio file to split'
	SELECT_FILE_TO_SHARE = 'Select audio file to share'

	load = ObjectProperty(None)
#	save = OLOAD_FILE_POPUP_TITLEbjectProperty(None)
	cancel = ObjectProperty(None)
	
	def __init__(self, rootGUI, **kwargs):
		super(FileChooserPopup, self).__init__(**kwargs)
		
		self.sdCardDir = None
		self.rootGUI = rootGUI
		
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
		dataLocationFromSetting = self.rootGUI.configMgr.dataPath
		
		if platform == 'android':
			self.pathList.data.append({'text': 'Data file location setting', 'selectable': True,
			                           'pathOnly': dataLocationFromSetting})
			self.pathList.data.append({'text': 'Main RAM', 'selectable': True, 'pathOnly': '/storage/emulated/0'})
			
			if self.onSmartPhone():
				self.sdCardDir = GuiUtil.SD_CARD_DIR_SMARTPHONE
			else:
				self.sdCardDir = GuiUtil.SD_CARD_DIR_TABLET
			
			self.pathList.data.append({'text': 'SD card', 'selectable': True, 'pathOnly': self.sdCardDir})
		elif platform == 'win':
			import string
			available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
			
			self.pathList.data.append(
				{'text': 'Data file location setting', 'selectable': True, 'pathOnly': dataLocationFromSetting})
			
			for drive in available_drives:
				self.pathList.data.append({'text': drive, 'selectable': True, 'pathOnly': drive})


class LoadFileChooserPopup(FileChooserPopup):
	"""
	
	"""
	def __init__(self, rootGUI, **kwargs):
		super(LoadFileChooserPopup, self).__init__(rootGUI, **kwargs)
		
	def loadFile(self, path, selection):
		self.load(path, selection)
		
	def onTouchDown(self):
		print("hello")


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
				self.loadAtStartChkBox.size_hint_x = 0.12
			else:
				self.loadAtStartChkBox.size_hint_x = 0.06
		elif platform == 'win':
			self.loadAtStartChkBox.size_hint_x = 0.06
	
	def save(self, pathOnly, pathFileName, isLoadAtStart):
		"""
		
		:param pathOnly:
		:param pathFileName:
		:param isLoadAtStart:
		:return:
		"""
		if pathOnly == pathFileName:
			# no file selected or file name defined. Load dialog remains open ..
			return

		self.rootGUI.saveHistoryToFile(pathOnly, pathFileName, isLoadAtStart)
		self.rootGUI.dismissPopup()

	def setCurrentLoadAtStartFile(self, loadAtStartFilePathName):
		self.loadAtStartFilePathName = loadAtStartFilePathName
	
	def updateLoadAtStartCheckBox(self):
		"""
		Method called when the currentPath TextInput field content is modified.
		"""

		# update load at start checkbox
		
		currentSaveFilePathName = self.currentPathField.text
		
		if currentSaveFilePathName == self.loadAtStartFilePathName:
			self.loadAtStartChkBox.active = True
		else:
			self.loadAtStartChkBox.active = False

		# update save file chooser popup title
		
		self._updateSaveFileChooserPopupTitle(currentSaveFilePathName, self.loadAtStartChkBox.active)
	
	def _updateSaveFileChooserPopupTitle(self, currentSaveFilePathName, isLoadAtStartChkboxActive):
		currentSaveFileName = currentSaveFilePathName.split(sep)[-1]
		
		if currentSaveFileName == '':
			# the case when opening the save file dialog after loading a file
			return
		
		if isLoadAtStartChkboxActive:
			self.rootGUI.popup.title = '{} {}'.format(FileChooserPopup.SAVE_FILE_POPUP_TITLE,
													  currentSaveFileName) + LOAD_AT_START_MSG
		else:
			self.rootGUI.popup.title = '{} {}'.format(FileChooserPopup.SAVE_FILE_POPUP_TITLE, currentSaveFileName)
	
	def toggleLoadAtStart(self, active):
		"""
		Method called when checking/unchecking the load at start checkbox

		:param active:
		"""
		self._updateSaveFileChooserPopupTitle(self.currentPathField.text, active)


class SelectOrCreateDirFileChooserPopup(FileChooserPopup):
	"""

	"""
	
	def __init__(self,
	             rootGUI,
	             playlistOrSingleVideoUrl,
			     singleVideoTitle,
			     **kwargs):
		super(SelectOrCreateDirFileChooserPopup, self).__init__(rootGUI, **kwargs)
		
		self.playlistOrSingleVideoUrl = playlistOrSingleVideoUrl
		self.singleVideoTitle = singleVideoTitle
		
	def selOrCreateDir(self, pathFileName):
		"""

		:param pathOnly:
		:param pathFileName:
		:param isLoadAtStart:
		:return:
		"""
		if os.path.isdir(pathFileName):
			pass
			#print("{} dir was selected".format(pathFileName))
		else:
			try:
				os.mkdir(pathFileName)
				#print("{} dir was created".format(pathFileName))
			except FileExistsError as e:
				print("{} dir already exists".format(pathFileName))
		
		self.rootGUI.singleVideoDownloadDir = pathFileName
		self.rootGUI.downloadPlaylistOrSingleVideoAudio(self.playlistOrSingleVideoUrl,
		                                                self.singleVideoTitle)
		self.rootGUI.dismissPopup()


class FileToSplitLoadFileChooserPopup(LoadFileChooserPopup):
	"""
	This file chooser popup is used to select the file which will be transmitted to the
	split audio file class.
	"""
	
	def __init__(self, rootGUI, **kwargs):
		super(FileToSplitLoadFileChooserPopup, self).__init__(rootGUI, **kwargs)
		self.loadButton.text = 'Split file'
		
	def loadFile(self, path, selection):
		audioSplitterScreen = self.rootGUI.manager.get_screen('audioSplitterScreen')
		audioSplitterScreen.initSoundFile(sourceAudioFilePathName=selection[0])
		self.rootGUI.dismissPopup()
		self.rootGUI.parent.current = "audioSplitterScreen"
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
