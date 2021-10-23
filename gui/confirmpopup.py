from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock


class ConfirmPopup(GridLayout):
	text = StringProperty()
	
	def __init__(self, **kwargs):
		# removing new line char which may cause an exception in Kivy
		text = kwargs['text']
		self.isPlaylist = kwargs['isPlaylist']
		
		# removing the isPlaylist arg is necessary otherwise the superclass
		# constructor will fail !
		del kwargs['isPlaylist']
		
		kwargs['text'] = text.replace("\n", " ")

		super(ConfirmPopup, self).__init__(**kwargs)

		self.register_event_type('on_answer')
		
		# WARNING: accessing MainWindow fields defined in kv file
		# in the __init__ ctor is no longer possible when using
		# ScreenManager. Here's the solution:
		# (https://stackoverflow.com/questions/26916262/why-cant-i-access-the-screen-ids)
		Clock.schedule_once(self._finish_init)
	
	def _finish_init(self, dt):
		if self.isPlaylist:
			self.addUploadDateChkBox.active = True
			self.addUploadDateChkBox.disabled = False
		else:
			self.addUploadDateChkBox.active = False
			self.addUploadDateChkBox.disabled = True

	def toggleAddUploadDate(self, isActive):
		containingPopup = self.parent.parent.parent

		if isActive:
			containingPopup.title = 'Ciao'
		else:
			containingPopup.title = 'Hola'

	def on_answer(self, *args):
		pass
