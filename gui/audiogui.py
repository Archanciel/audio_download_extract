import os

from kivy import platform
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from gui.guiutil import GuiUtil


class AudioGUI(Screen):
	"""
	Base class for the audio downloader GUI classes.
	"""
	def __init__(self, **kw):
		super().__init__(**kw)

		# WARNING: accessing MainWindow fields defined in kv file
		# in the __init__ ctor is no longer possible when using
		# ScreenManager. Here's the solution:
		# (https://stackoverflow.com/questions/26916262/why-cant-i-access-the-screen-ids)
		Clock.schedule_once(self._finish_init)

	def _finish_init(self, dt):
		"""
		Due to using WindowManager for managing multiple screens, the content
		of this method can no longer be located in the __init__ ctor method,
		but must be called by Clock.schedule_once().

		:param dt:
		"""
		pass

	def outputResult(self, resultStr):
		markupBoldStart = '[b]'
		markupBoldEnd = '[/b]'
		
		if len(self.outputLabel.text) == 0:
			self.outputLabel.text = markupBoldStart + resultStr + markupBoldEnd
		else:
			self.outputLabel.text = self.outputLabel.text + '\n' + markupBoldStart + resultStr + markupBoldEnd

		# scrolling to end of output text
		self.outputScrollView.scroll_y = 0
	
	def displayPopupWarning(self, message):
		popupSize = None
		
		if platform == 'android':
			if GuiUtil.onSmartPhone():
				popupSize = (980, 350)
			else:
				popupSize = (980, 250)
		elif platform == 'win':
			popupSize = (330, 150)
		
		# this code ensures that the popup content text does not exceeds
		# the popup borders
		sizingLabel = Label(text=message)
		sizingLabel.bind(size=lambda s, w: s.setter('text_size')(s, w))
		
		popup = Popup(title='AudioDownloader WARNING', content=sizingLabel,
					  auto_dismiss=True, size_hint=(None, None),
					  size=popupSize)
		popup.open()
	
	def buildDataPathNotExistMessage(self, path):
		return 'Data path ' + path + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'
	
	def buildFileNotFoundMessage(self, filePathFilename):
		return 'Data file\n' + filePathFilename + '\nnot found. No history loaded.'
	
	def ensureDataPathExist(self, dataPath, message):
		'''
		Display a warning in a popup if the data path defined in the settings
		does not exist and return False. If path ok, returns True. This prevents
		exceptions at load or save or settings save time.
		:return:
		'''
		if not (os.path.isdir(dataPath)):
			self.displayPopupWarning(message)
			
			return False
		else:
			return True
	
	def ensureDataPathFileNameExist(self, dataPathFileName, message):
		'''
		Display a warning in a popup if the passed data path file name
		does not exist and return False. If dataPathFileName ok, returns True.
		This prevents exceptions at load or save or settings save time.
		:return:
		'''
		if not (os.path.isfile(dataPathFileName)):
			self.displayPopupWarning(message)
			
			return False
		else:
			return True