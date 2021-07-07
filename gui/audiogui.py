from kivy.uix.screenmanager import Screen

class AudioGUI(Screen):
	def __init__(self, **kw):
		super().__init__(**kw)
	
	def outputResult(self, resultStr):
		markupBoldStart = '[b]'
		markupBoldEnd = '[/b]'
		
		if len(self.outputLabel.text) == 0:
			self.outputLabel.text = markupBoldStart + resultStr + markupBoldEnd
		else:
			self.outputLabel.text = self.outputLabel.text + '\n' + markupBoldStart + resultStr + markupBoldEnd
