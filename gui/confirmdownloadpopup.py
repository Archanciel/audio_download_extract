import re

from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock


class ConfirmDownloadPopup(GridLayout):
	"""
	The advantage of using register_event_type is that the same class can be
	instantiated with binding 'on_answer' to different methods.
	"""
	POPUP_TITLE_PLAYLIST = 'Go on with processing playlist'
	POPUP_TITLE_VIDEO = 'Go on with downloading audio for video ...'
	POPUP_TITLE_NO_DOWNLOAD_DATE_UPLOAD_DATE = ' (adding upload date suffix) ...'
	POPUP_TITLE_DOWNLOAD_DATE_UPLOAD_DATE = ' (adding download date prefix and upload date suffix) ...'
	POPUP_TITLE_DOWNLOAD_DATE_NO_UPLOAD_DATE = ' (adding download date prefix) ...'
	POPUP_TITLE_NO_DOWNLOAD_DATE_NO_UPLOAD_DATE = ' ...'
	text = StringProperty()
	cols = ObjectProperty
	
	def __init__(self, **kwargs):
		text = kwargs['text']
		# removing new line char which may cause an exception in Kivy
		self.textStr = kwargs['text']
		cols = 1    # required to avoid [WARNING] <kivy.uix.gridlayout.GridLayout
					# object at 0x000001DE3BFBF3C0> have no cols or rows set,
					# layout is not triggered.
		self.isPlaylist = kwargs['isPlaylist']
		self.playlistOrSingleVideoUrl = kwargs['playlistOrSingleVideoUrl']
		
		# removing the additional args is necessary otherwise the superclass
		# constructor will fail !
		del kwargs['isPlaylist']
		del kwargs['playlistOrSingleVideoUrl']
		
		kwargs['text'] = self.textStr.replace("\n", " ")

		super(ConfirmDownloadPopup, self).__init__(**kwargs)

		self.register_event_type('on_answer')
		
		# WARNING: accessing MainWindow fields defined in kv file
		# in the __init__ ctor is no longer possible when using
		# ScreenManager. Here's the solution:
		# (https://stackoverflow.com/questions/26916262/why-cant-i-access-the-screen-ids)
		Clock.schedule_once(self._finish_init)
	
	def _finish_init(self, dt):
		self.editableTextInput.text = self.textStr

		if self.isPlaylist:
			self.addIndexChkBox.active = True
			self.addIndexChkBox.disabled = False
			self.addUploadDateChkBox.active = True
			self.addUploadDateChkBox.disabled = False
		else:
			self.addIndexChkBox.active = False
			self.addIndexChkBox.disabled = True
			self.addUploadDateChkBox.active = False
			self.addUploadDateChkBox.disabled = True

	def toggleAddUploadDate(self, isActive):
		containingPopup = self.parent.parent.parent
		isIndexChkboxActive = self.addIndexChkBox.active

		if isActive:
			if isIndexChkboxActive:
				containingPopup.title = self.POPUP_TITLE_PLAYLIST + self.POPUP_TITLE_DOWNLOAD_DATE_UPLOAD_DATE
			else:
				containingPopup.title = self.POPUP_TITLE_PLAYLIST + self.POPUP_TITLE_NO_DOWNLOAD_DATE_UPLOAD_DATE
		else:
			if isIndexChkboxActive:
				containingPopup.title = self.POPUP_TITLE_PLAYLIST + self.POPUP_TITLE_DOWNLOAD_DATE_NO_UPLOAD_DATE
			else:
				containingPopup.title = self.POPUP_TITLE_PLAYLIST + self.POPUP_TITLE_NO_DOWNLOAD_DATE_NO_UPLOAD_DATE

	def toggleAddIndex(self, isActive):
		containingPopup = self.parent.parent.parent
		isUploadDateChkboxActive = self.addUploadDateChkBox.active

		if isActive:
			if isUploadDateChkboxActive:
				containingPopup.title = self.POPUP_TITLE_PLAYLIST + self.POPUP_TITLE_DOWNLOAD_DATE_UPLOAD_DATE
			else:
				containingPopup.title = self.POPUP_TITLE_PLAYLIST + self.POPUP_TITLE_DOWNLOAD_DATE_NO_UPLOAD_DATE
		else:
			if isUploadDateChkboxActive:
				containingPopup.title = self.POPUP_TITLE_PLAYLIST + self.POPUP_TITLE_NO_DOWNLOAD_DATE_UPLOAD_DATE
			else:
				containingPopup.title = self.POPUP_TITLE_PLAYLIST + self.POPUP_TITLE_NO_DOWNLOAD_DATE_NO_UPLOAD_DATE

	def on_answer(self, *args):
		pass
	
	def isUploadDateAdded(self):
		return self.addUploadDateChkBox.active
	
	def isIndexAdded(self):
		return self.addIndexChkBox.active
