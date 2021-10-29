from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock


class ConfirmPopup(GridLayout):
	POPUP_TITLE_UPLOAD_DATE = ' (upload date added) ...'
	POPUP_TITLE_NO_UPLOAD_DATE = ' ...'
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
		
		# removing the isPlaylist arg is necessary otherwise the superclass
		# constructor will fail !
		del kwargs['isPlaylist']
		
		kwargs['text'] = self.textStr.replace("\n", " ")

		super(ConfirmPopup, self).__init__(**kwargs)

		self.register_event_type('on_answer')
		
		# WARNING: accessing MainWindow fields defined in kv file
		# in the __init__ ctor is no longer possible when using
		# ScreenManager. Here's the solution:
		# (https://stackoverflow.com/questions/26916262/why-cant-i-access-the-screen-ids)
		Clock.schedule_once(self._finish_init)
	
	def _finish_init(self, dt):
		self.editableTextInput.text = self.textStr
		
		if self.isPlaylist:
			self.addUploadDateChkBox.active = True
			self.addUploadDateChkBox.disabled = False
		else:
			self.addUploadDateChkBox.active = False
			self.addUploadDateChkBox.disabled = True

	def toggleAddUploadDate(self, isActive):
		containingPopup = self.parent.parent.parent

		if isActive:
			containingPopup.title = containingPopup.title.replace(self.POPUP_TITLE_NO_UPLOAD_DATE,
			                                                      self.POPUP_TITLE_UPLOAD_DATE)
		else:
			containingPopup.title = containingPopup.title.replace(self.POPUP_TITLE_UPLOAD_DATE,
			                                                      self.POPUP_TITLE_NO_UPLOAD_DATE)

	def on_answer(self, *args):
		pass
	
	def isUploadDateAdded(self):
		return self.addUploadDateChkBox.active
