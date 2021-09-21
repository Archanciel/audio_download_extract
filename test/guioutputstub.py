import os
from tkinter import Tk, TclError, Message
class GuiOutputStub:
	'''
	This class is used for testing only
	'''
	def getPlaylistUrlFromClipboard(self):
		pass
	
	def displayMessage(self, msgText):
		msgText = msgText.replace('[b]', '"').replace('[/b]', '"')
		
		print(msgText)
	
	def outputResult(self, msgText):
		msgText = msgText.replace('[b]', '"').replace('[/b]', '"')
		
		print(msgText)
	
	def displayError(self, msgText):
		msgText = msgText.replace('[b]', '"').replace('[/b]', '"')
		
		print(msgText)
	
	def clearClipboard(self):
		from tkinter import Tk
		Tk().clipboard_clear()
