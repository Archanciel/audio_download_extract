from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout


class OkPopup(GridLayout):
	text = StringProperty()

	def __init__(self, **kwargs):
		super(OkPopup, self).__init__(**kwargs)
		self.popup = None
	
	def close(self, *args):
		self.popup.dismiss()
