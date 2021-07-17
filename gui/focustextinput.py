from kivy.uix.textinput import TextInput

class FocusTextInput(TextInput):
	"""
	This class replaces the TextInput class in the .kv files in order
	to enable using TAB to move from one TextInput field to the next
	one.
	
	In order for TAB to cycle through the TextIput fields, all the
	formulary TextInput fields must be replaced by FocusTextInput.
	
	WARNING:
	
	Defining class FocusTextInput(FocusBehavior, TextInput)
	raises a TypeError: Cannot create a consistent method resolution
	 order (MRO) for bases FocusBehavior, TextInput.

	The reason is that TextInput already inherits from FocusBehavior.
	"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.multiline = False
	
	def keyboard_on_key_down(self, window, keycode, text, modifiers):
		if keycode[1] == 'tab':
			self.get_focus_next().focus = True
		else:
			super().keyboard_on_key_down(window, keycode, text, modifiers)
