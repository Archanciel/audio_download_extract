from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout


class ConfirmPopup(GridLayout):
	text = StringProperty()
	
	def __init__(self, **kwargs):
		# removing new line char which may cause an exception in Kivy
		text = kwargs['text']
		kwargs['text'] = text.replace("\n", " ")

		super(ConfirmPopup, self).__init__(**kwargs)

		self.register_event_type('on_answer')

	def toggleAddUploadDate(self, isActive):
		pass

	def on_answer(self, *args):
		pass
