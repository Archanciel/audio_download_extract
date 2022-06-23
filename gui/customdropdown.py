import os

from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown

from gui.guiutil import GuiUtil


class CustomDropDown(DropDown):
	saveButton = ObjectProperty(None)
	statusToRequestInputButton = ObjectProperty(None)
	
	def __init__(self, rootGUI):
		super().__init__()

		self.rootGUI = rootGUI
		self.auto_width = False
		self.width = dp(self.rootGUI.configMgr.dropDownMenuWidth)

	def showLoad(self):
		"""
		Open the file load popup
		"""
		message = 'Data path ' + self.rootGUI.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.rootGUI.ensureDataPathExist(self.rootGUI.audiobookPath, message):
			self.rootGUI.openFileLoadPopup()

	def showSave(self):
		"""
		Open the file save popup
		"""
		message = 'Data path ' + self.rootGUI.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.rootGUI.ensureDataPathExist(self.rootGUI.audiobookPath, message):
			self.rootGUI.openFileSavePopup()

	def showDelete(self):
		"""
		Open the file delete popup. Files will be removed from playlist dir aswell as
		from playlist dictionary file.
		"""
		message = 'Data path ' + self.rootGUI.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.rootGUI.ensureDataPathExist(self.rootGUI.audiobookPath, message):
			self.rootGUI.openFileDeletePopup()

	def showClipAudioFile(self):
		"""
		Show file open popup in order to select file opened in clip audio file screen.
		"""
		message = 'Data path ' + self.rootGUI.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.rootGUI.ensureDataPathExist(self.rootGUI.audiobookPath, message):
			self.rootGUI.openFileToClipLoadPopup()

	def shareAudio(self):
		"""
		Show file open popup in order to select file opened in share audio file screen.
		"""
		self.rootGUI.openShareAudioPopup()
		
	def handleFailedVideosDownloading(self):
		"""
		Called by Down failed vids menu item defined in customdropdown.kv file.
		"""
		self.rootGUI.handleFailedVideosDownloading()
	
	def downloadHisto(self):
		"""
		Called by Downl histo menu item defined in customdropdown.kv file.
		
		Displays the download history in the output result label, i.e.
		for each playlist the file names of the files still present in the
		playlist dir ordered by date, most recent first. Fills the download
		history list so that list items can be deleted.
		"""
		self.rootGUI.handleDownloadHistory()
	
	def moveAudioFileToOtherPlaylist(self):
		"""
		Called by Chge playlst menu item defined in customdropdown.kv file.

		Move an audio file to another playlist and update the source and destination
		playlist dic file.
		"""
		self.rootGUI.moveAudioFileToOtherPlaylist()
	
	def help(self):
		self.rootGUI.displayHelp()
