from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

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
