from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout


class YesNoPopup(GridLayout):
	text = StringProperty()

	def __init__(self, **kwargs):
		super(YesNoPopup, self).__init__(**kwargs)
		self.popup = None
	
	def yes(self, *args):
		self.popup.dismiss()
	
	def no(self, *args):
		self.popup.dismiss()
