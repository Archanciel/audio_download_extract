from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout


class ConfirmPopup(GridLayout):
	text = StringProperty()
	
	def __init__(self, rootGUI, **kwargs):
		self.register_event_type('on_answer')
		super(ConfirmPopup, self).__init__(**kwargs)
		
		self.rootGUI = rootGUI
	
	def on_answer(self, *args):
		pass
	
	def setTextInputChanged(self):
		"""
		Method called if the editable text of the ConfirmPopup was changed.
		"""
		self.rootGUI.setConfirmPopupTextChanged()