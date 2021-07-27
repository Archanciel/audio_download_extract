from audiogui import AudioGUI

class AudioPositionGUI(AudioGUI):
	"""
	Abstract class hosting common methods of its sub classes.
	"""
	def __init__(self, **kw):
		super().__init__(**kw)