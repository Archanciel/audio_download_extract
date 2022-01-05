import os

from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.utils import platform

from gui.guiutil import GuiUtil


class CustomDropDown(DropDown):
	saveButton = ObjectProperty(None)
	statusToRequestInputButton = ObjectProperty(None)
	
	def __init__(self, rootGUI):
		super().__init__()
		self.rootGUI = rootGUI

		if os.name == 'posix':
			if GuiUtil.onSmartPhone():
				self.auto_width = False
				self.width = dp(self.rootGUI.configMgr.dropDownMenuWidth)

	def showLoad(self):
		message = 'Data path ' + self.rootGUI.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.rootGUI.ensureDataPathExist(self.rootGUI.audiobookPath, message):
			self.rootGUI.openFileLoadPopup()

	def showSave(self):
		message = 'Data path ' + self.rootGUI.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.rootGUI.ensureDataPathExist(self.rootGUI.audiobookPath, message):
			self.rootGUI.openFileSavePopup()

	def showDelete(self):
		message = 'Data path ' + self.rootGUI.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.rootGUI.ensureDataPathExist(self.rootGUI.audiobookPath, message):
			self.rootGUI.openFileDeletePopup()

	def showClipAudioFile(self):
		message = 'Data path ' + self.rootGUI.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.rootGUI.ensureDataPathExist(self.rootGUI.audiobookPath, message):
			self.rootGUI.openFileToClipLoadPopup()

	def shareAudio(self):
		self.rootGUI.openShareAudioPopup()
	
	def help(self):
		self.rootGUI.displayHelp()
