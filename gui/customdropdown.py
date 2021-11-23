from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.utils import platform


class CustomDropDown(DropDown):
	saveButton = ObjectProperty(None)
	statusToRequestInputButton = ObjectProperty(None)
	
	def __init__(self, owner):
		super().__init__()
		self.owner = owner

	def showLoad(self):
		message = 'Data path ' + self.owner.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.owner.ensureDataPathExist(self.owner.audiobookPath, message):
			self.owner.openFileLoadPopup()

	def showSave(self):
		message = 'Data path ' + self.owner.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.owner.ensureDataPathExist(self.owner.audiobookPath, message):
			self.owner.openFileSavePopup()

	def showDelete(self):
		message = 'Data path ' + self.owner.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.owner.ensureDataPathExist(self.owner.audiobookPath, message):
			self.owner.openFileDeletePopup()

	def showClipAudioFile(self):
		message = 'Data path ' + self.owner.audiobookPath + ' as defined in the settings does not exist ! Either create the directory or change the data path value using the Settings menu.'

		if self.owner.ensureDataPathExist(self.owner.audiobookPath, message):
			self.owner.openFileToClipLoadPopup()

	def shareAudio(self):
		self.owner.openShareAudioPopup()
	
	def help(self):
		self.owner.displayHelp()
