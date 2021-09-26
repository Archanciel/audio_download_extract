from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout


class ConfirmPopup(GridLayout):
	text = StringProperty()
	
	def __init__(self, **kwargs):
		super(ConfirmPopup, self).__init__(**kwargs)

		self.register_event_type('on_answer')

	def on_answer(self, *args):
		pass
